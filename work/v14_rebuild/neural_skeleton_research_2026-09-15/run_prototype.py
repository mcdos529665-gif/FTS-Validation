"""Small, reproducible construct-validity probe for FTS-Skeleton v0.1.

This is research-layer code. It does not implement the FTS canon and does not
claim that explicit masks or modules are unique to FTS.
"""
from __future__ import annotations

import hashlib
import json
import warnings
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, brier_score_loss
from sklearn.neural_network import MLPClassifier

warnings.filterwarnings("ignore", category=UserWarning)

ROOT = Path(__file__).resolve().parent
SEEDS = (13, 29, 47, 71, 97)
TRAIN_N = 1800
TEST_N = 2000


def parameter_count(input_dim: int, hidden: int) -> int:
    return (input_dim + 1) * hidden + (hidden + 1)


def fit_mlp(x: np.ndarray, y: np.ndarray, hidden: int, seed: int) -> MLPClassifier:
    model = MLPClassifier(
        hidden_layer_sizes=(hidden,),
        activation="tanh",
        solver="lbfgs",
        alpha=1e-4,
        max_iter=500,
        random_state=seed,
    )
    model.fit(x, y)
    return model


def absence_data(seed: int, n: int, mechanism: str) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    z1 = rng.normal(size=n)
    z2 = rng.normal(size=n)
    if mechanism == "signal":
        missing = z2 > 0.65
    elif mechanism == "null":
        missing = rng.random(n) < 0.35
    else:
        raise ValueError(mechanism)
    x = np.column_stack((z1, np.where(missing, 0.0, z2)))
    mask = missing.astype(float)[:, None]
    y = (z1 + z2 > 0.0).astype(int)
    return np.column_stack((x, mask)), y


def composition_data(seed: int, n: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    a, b = rng.uniform(-1.0, 1.0, size=(2, n))
    q = rng.integers(0, 2, size=n)
    score = np.where(
        q == 0,
        a + b + 0.25 * a * b,
        a - b + 0.25 * a * b,
    )
    x = np.column_stack((a, b, q.astype(float)))
    y = (score > 0.0).astype(int)
    return x, y


def score(model: MLPClassifier, x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    p = model.predict_proba(x)[:, 1]
    return {
        "accuracy": float(accuracy_score(y, p >= 0.5)),
        "brier": float(brier_score_loss(y, p)),
    }


def run_absence(seed: int, mechanism: str) -> dict:
    train, y_train = absence_data(seed, TRAIN_N, mechanism)
    test, y_test = absence_data(seed + 1000, TEST_N, mechanism)
    # x has 2 values + 1 explicit mask; baseline sees only 2 values.
    typed = fit_mlp(train, y_train, hidden=16, seed=seed)
    value_only = fit_mlp(train[:, :2], y_train, hidden=20, seed=seed)
    typed_score = score(typed, test, y_test)
    value_score = score(value_only, test[:, :2], y_test)
    return {
        "task": "ABS-MECH",
        "mechanism": mechanism,
        "seed": seed,
        "typed_absence": typed_score,
        "value_only": value_score,
        "delta_accuracy": typed_score["accuracy"] - value_score["accuracy"],
        "delta_brier": value_score["brier"] - typed_score["brier"],
        "typed_params": parameter_count(3, 16),
        "value_only_params": parameter_count(2, 20),
    }


def run_composition(seed: int) -> dict:
    train, y_train = composition_data(seed, TRAIN_N)
    test, y_test = composition_data(seed + 1000, TEST_N)
    x_train, q_train = train[:, :2], train[:, 2].astype(int)
    x_test, q_test = test[:, :2], test[:, 2].astype(int)
    modules = []
    for q in (0, 1):
        module = fit_mlp(
            x_train[q_train == q],
            y_train[q_train == q],
            hidden=8,
            seed=seed + q,
        )
        modules.append(module)
    module_proba = np.zeros(len(y_test), dtype=float)
    for q in (0, 1):
        idx = q_test == q
        module_proba[idx] = modules[q].predict_proba(x_test[idx])[:, 1]
    monolith = fit_mlp(train, y_train, hidden=13, seed=seed)
    mono_proba = monolith.predict_proba(test)[:, 1]
    module_score = {
        "accuracy": float(accuracy_score(y_test, module_proba >= 0.5)),
        "brier": float(brier_score_loss(y_test, module_proba)),
    }
    mono_score = {
        "accuracy": float(accuracy_score(y_test, mono_proba >= 0.5)),
        "brier": float(brier_score_loss(y_test, mono_proba)),
    }
    return {
        "task": "COMP-QUERY",
        "seed": seed,
        "compositional_modules": module_score,
        "compositional_monolith": mono_score,
        "delta_accuracy": module_score["accuracy"] - mono_score["accuracy"],
        "delta_brier": mono_score["brier"] - module_score["brier"],
        "modules_params": 2 * parameter_count(2, 8),
        "monolith_params": parameter_count(3, 13),
    }


def summarize(rows: list[dict], key: str) -> dict[str, float]:
    values = np.asarray([row[key] for row in rows], dtype=float)
    mean = float(values.mean())
    sd = float(values.std(ddof=1))
    half = float(2.776 * sd / np.sqrt(len(values)))  # t_0.975, df=4
    return {"mean": mean, "sd": sd, "ci95_half_width": half}


def main() -> None:
    rows = []
    for seed in SEEDS:
        for mechanism in ("signal", "null"):
            rows.append(run_absence(seed, mechanism))
        rows.append(run_composition(seed))

    summaries = {}
    for task, subset in (
        ("ABS-MECH/signal", [r for r in rows if r["task"] == "ABS-MECH" and r["mechanism"] == "signal"]),
        ("ABS-MECH/null", [r for r in rows if r["task"] == "ABS-MECH" and r["mechanism"] == "null"]),
        ("COMP-QUERY", [r for r in rows if r["task"] == "COMP-QUERY"]),
    ):
        summaries[task] = {
            "delta_accuracy": summarize(subset, "delta_accuracy"),
            "delta_brier": summarize(subset, "delta_brier"),
        }

    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    protocol_hash = hashlib.sha256((ROOT / "PROTOTYPE_PROTOCOL.md").read_bytes()).hexdigest()
    payload = {
        "protocol": "FTS-Skeleton-v0.1",
        "status": "exploratory_construct_validity",
        "script_sha256": script_hash,
        "protocol_sha256": protocol_hash,
        "seeds": list(SEEDS),
        "train_n": TRAIN_N,
        "test_n": TEST_N,
        "rows": rows,
        "summaries": summaries,
    }
    (ROOT / "results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# FTS-Skeleton v0.1 — результаты первой пробы",
        "",
        f"- Статус: {payload['status']}",
        f"- SHA256 кода: {script_hash}",
        f"- SHA256 протокола: {protocol_hash}",
        f"- Seeds: {', '.join(map(str, SEEDS))}",
        "",
        "## Сводка paired deltas",
        "",
        "| Тест | Δ accuracy (mean ± 95% half-width) | Δ Brier (mean ± 95% half-width) |",
        "|---|---:|---:|",
    ]
    for task, summary in summaries.items():
        da = summary["delta_accuracy"]
        db = summary["delta_brier"]
        lines.append(
            f"| {task} | {da['mean']:.4f} ± {da['ci95_half_width']:.4f} | "
            f"{db['mean']:.4f} ± {db['ci95_half_width']:.4f} |"
        )
    signal = summaries["ABS-MECH/signal"]["delta_accuracy"]
    null = summaries["ABS-MECH/null"]["delta_accuracy"]
    signal_lower = signal["mean"] - signal["ci95_half_width"]
    null_lower = null["mean"] - null["ci95_half_width"]
    lines += [
        "",
        "## Предварительный вердикт пробы",
        "",
        f"- ABS-MECH/signal: нижняя граница paired delta accuracy = {signal_lower:.4f}.",
        f"- ABS-MECH/null: нижняя граница paired delta accuracy = {null_lower:.4f}.",
        "- Оба интервала включают ноль; специфическое преимущество typed mask "
        "в этой постановке не установлено.",
        "- COMP-QUERY также не показывает устойчивого отличия модулей от "
        "capacity-matched monolith.",
        "",
        "## Ограничение интерпретации",
        "",
        "Это construct-validity probe двух ролей, а не доказательство T2/T3.",
        "Текущий исход — inconclusive/limiting: он не показывает, что явное",
        "состояние отсутствия даёт отличимый выигрыш, и не подтверждает тождество",
        "с 0_A или необходимость всей ФТС.",
        "Ограничение относится к этой генеративной постановке, числу seeds и",
        "MLP-конфигурации; исправлять его постфактум сменой генератора нельзя.",
        "",
    ]
    (ROOT / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
