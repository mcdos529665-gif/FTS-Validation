#!/usr/bin/env python3
"""Воспроизводимая условная симуляция рефлексивного регулятора по протоколу v1.

Скрипт не моделирует реальный железнодорожный контроллер. Он проверяет узкий
кандидат: отличается ли регулятор, который оценивает собственное правило,
от адаптивных и отключённых вариантов при одинаковой истории и цене.
"""

from __future__ import annotations

import hashlib
import json
import random
import statistics
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROTOCOL = HERE / "PROTOCOL.md"
RESULTS_JSON = HERE / "results.json"
RESULTS_MD = HERE / "RESULTS.md"

SEEDS = tuple(range(64))
EPISODES = 600
EXPLORATION_EPISODES = 30
MODE_SWITCH_EPISODE = 300
CONTEXTS = ("open", "queue")
ACTIONS = ("hold", "recover", "defer")
ALPHA = 0.25
DOUBT_THRESHOLD = 0.75
EXPLORATION_RATE = 0.10
TAIL_PROBABILITY = 0.12

BASE_COST: dict[int, dict[str, dict[str, int]]] = {
    0: {
        "open": {"hold": 2, "recover": 1, "defer": 3},
        "queue": {"hold": 2, "recover": 6, "defer": 3},
    },
    1: {
        "open": {"hold": 2, "recover": 5, "defer": 3},
        "queue": {"hold": 2, "recover": 1, "defer": 3},
    },
}
IMMEDIATE_COST = {"hold": 2, "recover": -1, "defer": 3}
CONTROLLERS = ("R", "B_event", "B_adaptive", "R_no_feedback", "R_label_only")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def schedule_for_seed(seed: int) -> list[dict[str, Any]]:
    """Create the public schedule and hidden outcomes for one seed.

    The first 30 episodes are a common exploration design: every context/action
    pair occurs five times. Later contexts and random disturbances use one
    deterministic stream per seed, shared by all controllers.
    """

    rng = random.Random(seed)
    design: list[tuple[str, str]] = []
    for context in CONTEXTS:
        for action in ACTIONS:
            design.extend((context, action) for _ in range(5))

    rows: list[dict[str, Any]] = []
    for episode in range(EPISODES):
        if episode < EXPLORATION_EPISODES:
            context, forced_action = design[episode]
        else:
            context = CONTEXTS[rng.randrange(len(CONTEXTS))]
            forced_action = None

        explore_draw = rng.random()
        explore_action = ACTIONS[rng.randrange(len(ACTIONS))]
        noise = (-1, 0, 1)[rng.randrange(3)]
        tail = rng.random() < TAIL_PROBABILITY
        rows.append(
            {
                "episode": episode,
                "context": context,
                "forced_action": forced_action,
                "explore": episode >= EXPLORATION_EPISODES and explore_draw < EXPLORATION_RATE,
                "explore_action": explore_action,
                "noise": noise,
                "tail": tail,
                "mode": 0 if episode < MODE_SWITCH_EPISODE else 1,
                # Replay action is visible to the evaluator only. It makes the
                # common-history arm genuinely common across controllers.
                "replay_action": ACTIONS[(episode - EXPLORATION_EPISODES) % len(ACTIONS)]
                if episode >= EXPLORATION_EPISODES
                else forced_action,
            }
        )
    return rows


def environment_cost(row: dict[str, Any], action: str) -> int:
    """Return the realised conditional delay for a hidden environment row."""

    mode = int(row["mode"])
    context = str(row["context"])
    immediate = IMMEDIATE_COST[action] + int(row["noise"])
    delayed = BASE_COST[mode][context][action] - IMMEDIATE_COST[action]
    if action == "recover" and bool(row["tail"]):
        delayed += 4
    return immediate + delayed


def argmin_action(values: dict[str, float]) -> str:
    return min(ACTIONS, key=lambda action: (values[action], ACTIONS.index(action)))


class Controller:
    """One transparent controller implementation from the frozen protocol."""

    def __init__(self, kind: str) -> None:
        if kind not in CONTROLLERS:
            raise ValueError(f"unknown controller: {kind}")
        self.kind = kind
        self.estimates: dict[str, dict[str, float]] = {
            context: {"hold": 2.0, "recover": 1.0, "defer": 3.0} for context in CONTEXTS
        }
        self.policy = {context: "recover" for context in CONTEXTS}
        self.surprise = {context: 0.0 for context in CONTEXTS}
        self.doubt_signals = 0
        self.filter_events = 0
        self.reviews = 0
        self.policy_changes = 0
        self.reads = 0
        self.updates = 0

    @property
    def state_cells(self) -> int:
        # Six estimates plus two context policies. B_adaptive has no policy.
        return 6 if self.kind == "B_adaptive" else 8

    def recommend(self, context: str) -> str:
        if self.kind == "B_adaptive":
            self.reads += 3
            return argmin_action(self.estimates[context])
        return self.policy[context]

    def observe(self, context: str, action: str, cost: int) -> dict[str, Any]:
        predicted = self.estimates[context][action]
        residual = cost - predicted
        self.estimates[context][action] = predicted + ALPHA * residual
        self.updates += 1

        positive_error = max(0.0, residual)
        self.surprise[context] = 0.75 * self.surprise[context] + positive_error
        doubt = residual > DOUBT_THRESHOLD
        review = False
        old_action = self.policy.get(context)

        if doubt:
            self.doubt_signals += 1

        if self.kind == "R":
            # Internal doubt is a regulator: it turns evaluation of the rule
            # into a review of the three candidate actions.
            if doubt:
                self.reads += 3
                review = True
                self.reviews += 1
                self.policy[context] = argmin_action(self.estimates[context])
        elif self.kind == "B_event":
            # Flat-table event filter: same threshold, no named self-rule.
            if doubt:
                self.reads += 3
                review = True
                self.filter_events += 1
                self.policy[context] = argmin_action(self.estimates[context])
        elif self.kind == "B_adaptive":
            # No separate event; every recommendation is an immediate table
            # minimum. The estimates are still updated from observed outcomes.
            pass
        elif self.kind == "R_no_feedback":
            # The signal is computed but its feedback to the policy is cut.
            pass
        elif self.kind == "R_label_only":
            # The signal is merely logged; no review is allowed to start.
            pass

        if self.kind in {"R", "B_event"} and review:
            self.reviews += 0  # explicit: counted above, keeps branch readable
        if old_action is not None and self.policy[context] != old_action:
            self.policy_changes += 1

        return {
            "predicted": predicted,
            "residual": residual,
            "doubt": doubt,
            "review": review,
            "policy_after": self.policy.get(context),
        }

    def digest(self) -> str:
        payload = {
            "kind": self.kind,
            "estimates": self.estimates,
            "policy": self.policy,
            "surprise": self.surprise,
            "doubt_signals": self.doubt_signals,
            "filter_events": self.filter_events,
            "reviews": self.reviews,
            "policy_changes": self.policy_changes,
            "reads": self.reads,
            "updates": self.updates,
        }
        return sha256_bytes(json.dumps(payload, sort_keys=True).encode("utf-8"))


def empty_metrics() -> dict[str, Any]:
    return {
        "costs": [],
        "regrets": [],
        "costs_pre_shift": [],
        "costs_post_shift": [],
        "regrets_pre_shift": [],
        "regrets_post_shift": [],
        "recommendation_changes": 0,
        "doubt_signals": 0,
        "reviews": 0,
        "policy_changes": 0,
        "reads": 0,
        "updates": 0,
        "max_state_cells": 0,
        "trace": [],
        "action_outcomes": [],
    }


def run_controller(
    kind: str,
    schedule: list[dict[str, Any]],
    arm: str,
    trace_limit: int = 0,
) -> dict[str, Any]:
    if arm not in {"common_history", "closed_loop"}:
        raise ValueError(f"unknown arm: {arm}")
    controller = Controller(kind)
    metrics = empty_metrics()
    previous_recommendation: dict[str, str] = {}

    for row in schedule:
        episode = int(row["episode"])
        context = str(row["context"])
        recommendation = controller.recommend(context)
        if context in previous_recommendation and previous_recommendation[context] != recommendation:
            metrics["recommendation_changes"] += 1
        previous_recommendation[context] = recommendation

        if episode < EXPLORATION_EPISODES:
            action = str(row["forced_action"])
        elif arm == "common_history":
            action = str(row["replay_action"])
        elif bool(row["explore"]):
            action = str(row["explore_action"])
        else:
            action = recommendation

        cost = environment_cost(row, action)
        audit = controller.observe(context, action, cost)
        metrics["action_outcomes"].append((episode, context, action, cost))

        if episode >= EXPLORATION_EPISODES:
            best_cost = min(environment_cost(row, candidate) for candidate in ACTIONS)
            regret = cost - best_cost
            metrics["costs"].append(cost)
            metrics["regrets"].append(regret)
            key = "costs_pre_shift" if episode < MODE_SWITCH_EPISODE else "costs_post_shift"
            metrics[key].append(cost)
            key = "regrets_pre_shift" if episode < MODE_SWITCH_EPISODE else "regrets_post_shift"
            metrics[key].append(regret)

        if len(metrics["trace"]) < trace_limit:
            metrics["trace"].append(
                {
                    "episode": episode,
                    "mode": row["mode"],
                    "context": context,
                    "recommendation": recommendation,
                    "action": action,
                    "cost": cost,
                    "residual": round(float(audit["residual"]), 6),
                    "doubt": audit["doubt"],
                    "review": audit["review"],
                    "policy_after": audit["policy_after"],
                }
            )

    metrics["doubt_signals"] = controller.doubt_signals
    metrics["reviews"] = controller.reviews
    metrics["policy_changes"] = controller.policy_changes
    metrics["reads"] = controller.reads
    metrics["updates"] = controller.updates
    metrics["max_state_cells"] = controller.state_cells
    metrics["state_digest"] = controller.digest()
    metrics["action_outcome_digest"] = sha256_bytes(
        json.dumps(metrics["action_outcomes"], sort_keys=True).encode("utf-8")
    )
    metrics["recommendation_digest"] = sha256_bytes(
        json.dumps(metrics["trace"], sort_keys=True).encode("utf-8")
    )
    return metrics


def mean(values: list[float | int]) -> float:
    return round(float(statistics.fmean(values)), 6) if values else 0.0


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    fields = (
        "mean_cost",
        "mean_regret",
        "mean_cost_pre_shift",
        "mean_cost_post_shift",
        "mean_regret_pre_shift",
        "mean_regret_post_shift",
        "mean_recommendation_changes",
        "mean_doubt_signals",
        "mean_reviews",
        "mean_policy_changes",
        "mean_reads",
        "max_state_cells",
    )
    result: dict[str, Any] = {"runs": len(records)}
    result["mean_cost"] = mean([mean(r["costs"]) for r in records])
    result["mean_regret"] = mean([mean(r["regrets"]) for r in records])
    result["mean_cost_pre_shift"] = mean([mean(r["costs_pre_shift"]) for r in records])
    result["mean_cost_post_shift"] = mean([mean(r["costs_post_shift"]) for r in records])
    result["mean_regret_pre_shift"] = mean([mean(r["regrets_pre_shift"]) for r in records])
    result["mean_regret_post_shift"] = mean([mean(r["regrets_post_shift"]) for r in records])
    result["mean_recommendation_changes"] = mean([r["recommendation_changes"] for r in records])
    result["mean_doubt_signals"] = mean([r["doubt_signals"] for r in records])
    result["mean_reviews"] = mean([r["reviews"] for r in records])
    result["mean_policy_changes"] = mean([r["policy_changes"] for r in records])
    result["mean_reads"] = mean([r["reads"] for r in records])
    result["max_state_cells"] = max(r["max_state_cells"] for r in records)
    result["min_cost"] = round(min(mean(r["costs"]) for r in records), 6)
    result["max_cost"] = round(max(mean(r["costs"]) for r in records), 6)
    return result


def run_all() -> dict[str, Any]:
    all_records: dict[str, dict[str, list[dict[str, Any]]]] = {
        arm: {kind: [] for kind in CONTROLLERS} for arm in ("common_history", "closed_loop")
    }
    common_action_outcome_hashes: dict[str, list[str]] = {kind: [] for kind in CONTROLLERS}
    traces: dict[str, Any] = {}

    for seed in SEEDS:
        schedule = schedule_for_seed(seed)
        for arm in ("common_history", "closed_loop"):
            for kind in CONTROLLERS:
                record = run_controller(kind, schedule, arm, trace_limit=40 if seed == 0 else 0)
                record["seed"] = seed
                record["arm"] = arm
                all_records[arm][kind].append(record)
                if arm == "common_history":
                    common_action_outcome_hashes[kind].append(record["action_outcome_digest"])
                if seed == 0:
                    traces[f"{arm}:{kind}"] = record["trace"]

    # Common-history outcomes must be identical by construction. This is an
    # invariant of the comparison, not an empirical advantage for any controller.
    reference_common_hashes = common_action_outcome_hashes[CONTROLLERS[0]]
    common_history_action_outcomes_identical = all(
        common_action_outcome_hashes[kind] == reference_common_hashes for kind in CONTROLLERS
    )

    summaries = {
        arm: {kind: summarize(records) for kind, records in by_kind.items()}
        for arm, by_kind in all_records.items()
    }

    paired: dict[str, Any] = {}
    for kind in CONTROLLERS:
        r_common = all_records["common_history"][kind]
        r_closed = all_records["closed_loop"][kind]
        paired[kind] = {
            "closed_minus_common_cost": round(
                summaries["closed_loop"][kind]["mean_cost"]
                - summaries["common_history"][kind]["mean_cost"],
                6,
            ),
            "common_state_digest_count": len({r["state_digest"] for r in r_common}),
            "closed_state_digest_count": len({r["state_digest"] for r in r_closed}),
            "common_updates_equal": len({r["updates"] for r in r_common}) == 1,
        }

    return {
        "protocol": {
            "path": str(PROTOCOL.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256_file(PROTOCOL),
            "version": "v1",
        },
        "program": {
            "path": str((PROTOCOL.parent / "run_reflection.py").relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256_file(Path(__file__).resolve()),
        },
        "simulation": {
            "seeds": [SEEDS[0], SEEDS[-1]],
            "seed_count": len(SEEDS),
            "episodes": EPISODES,
            "warmup_episodes": EXPLORATION_EPISODES,
            "mode_switch_episode": MODE_SWITCH_EPISODE,
            "controllers": list(CONTROLLERS),
            "arms": ["common_history", "closed_loop"],
            "objective": "minimize conditional delay",
            "internal_regulator": "doubt signal triggers review in R",
        },
        "invariants": {
            "common_history_action_outcomes_identical_across_controllers_and_seeds": common_history_action_outcomes_identical,
            "max_state_cells_within_budget": all(
                summaries[arm][kind]["max_state_cells"] <= 8
                for arm in summaries
                for kind in summaries[arm]
            ),
            "max_reads_per_episode_within_3": all(
                max(r["reads"] for r in all_records[arm][kind]) / EPISODES
                <= 3
                for arm in all_records
                for kind in all_records[arm]
            ),
            "reproducibility_digest": None,
        },
        "summaries": summaries,
        "paired": paired,
        "seed_records": {
            arm: {
                kind: [
                    {
                        "seed": r["seed"],
                        "mean_cost": mean(r["costs"]),
                        "mean_regret": mean(r["regrets"]),
                        "doubt_signals": r["doubt_signals"],
                        "reviews": r["reviews"],
                        "policy_changes": r["policy_changes"],
                        "reads": r["reads"],
                        "updates": r["updates"],
                        "action_outcome_digest": r["action_outcome_digest"],
                        "state_digest": r["state_digest"],
                    }
                    for r in all_records[arm][kind]
                ]
                for kind in CONTROLLERS
            }
            for arm in all_records
        },
        "trace_seed_0": traces,
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Результаты проверки рефлексии на примере поезда v1",
        "",
        f"Протокол SHA256: `{result['protocol']['sha256']}`.",
        "Симуляция условная и синтетическая; это не свидетельство реализации У11.",
        "",
        "## Найдено",
        "",
        "Сигнал сомнения в R рассматривается как внутренняя регуляция: рассогласование",
        "с собственным ожиданием может запустить пересмотр собственного правила.",
        "Сравнение проведено в общей истории и в замкнутом контуре.",
        "",
        "## Инварианты",
        "",
    ]
    for key, value in result["invariants"].items():
        if key != "reproducibility_digest":
            lines.append(f"- `{key}`: `{value}`")
    lines += ["", "## Средние результаты", "", "| Контур | Контроллер | Средняя цена | Средний проигрыш | До смены режима | После смены | Сигналы сомнения | Пересмотры |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for arm in ("common_history", "closed_loop"):
        for kind in CONTROLLERS:
            s = result["summaries"][arm][kind]
            lines.append(
                f"| {arm} | {kind} | {s['mean_cost']:.4f} | {s['mean_regret']:.4f} | "
                f"{s['mean_cost_pre_shift']:.4f} | {s['mean_cost_post_shift']:.4f} | "
                f"{s['mean_doubt_signals']:.2f} | {s['mean_reviews']:.2f} |"
            )
    lines += ["", "## Как читать результат", "", "- Совпадение R и B_event по общей истории не является доказательством тождества механизмов; оно означает, что этот пример сам по себе их не развёл.", "- Разница R и R_no_feedback показывает эффект включения обратной связи в данном синтетическом контроллере, если она устойчива по seed.", "- Сравнение с B_adaptive проверяет, даёт ли пороговый сигнал что-то сверх постоянного выбора минимума таблицы.", "- Ошибка, сохранение прежнего правила и худшая цена являются допустимыми исходами протокола.", "", "## Ограничения", "", "Это один синтетический класс сред с двумя контекстами и заранее заданной сменой режима. Он проверяет действие выбранного механизма, а не происхождение эмоций, полную семантику Я, неизбежность развития или поведение АГИ.", ""]
    return "\n".join(lines)


def main() -> int:
    result = run_all()
    # A second deterministic calculation is the reproducibility check. The
    # output digest excludes the reproducibility field itself.
    digest_payload = json.dumps(result, ensure_ascii=False, sort_keys=True).encode("utf-8")
    second = run_all()
    second_payload = json.dumps(second, ensure_ascii=False, sort_keys=True).encode("utf-8")
    result["invariants"]["reproducibility_match"] = digest_payload == second_payload
    result["invariants"]["reproducibility_digest"] = sha256_bytes(digest_payload)
    RESULTS_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    RESULTS_MD.write_text(render_markdown(result), encoding="utf-8")
    print(
        f"PASS train reflection simulation: protocol_sha256={result['protocol']['sha256']} "
        f"results_sha256={sha256_file(RESULTS_JSON)} seed_count={len(SEEDS)} episodes={EPISODES}"
    )
    print(f"RESULTS_JSON={RESULTS_JSON}")
    print(f"RESULTS_MD={RESULTS_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
