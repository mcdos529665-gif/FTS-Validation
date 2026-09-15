"""Preregistered local probe for provenance/revision/memory gating.

Research-layer code only. The derived gate is an explicit inductive bias, not a
claim that the implementation is identical to any FTS canonical operator.
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
TRAIN_N = 800
TEST_N = 5000
HELD_OUT = (1, 0, 1)


def parameter_count(input_dim: int, hidden: int) -> int:
    return (input_dim + 1) * hidden + (hidden + 1)


def generate(seed: int, n: int, exclude_held_out: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    rows = []
    labels = []
    patterns = []
    while len(rows) < n:
        c0 = rng.choice((-1.0, 1.0))
        c1 = rng.choice((-1.0, 1.0))
        v0 = c0 + rng.normal(scale=0.8)
        v1 = c1 + rng.normal(scale=0.8)
        s0 = int(rng.integers(0, 2))
        s1 = int(rng.integers(0, 2))
        r1 = int(rng.integers(0, 2))
        pattern = (s0, s1, r1)
        if exclude_held_out and pattern == HELD_OUT:
            continue
        valid = float(s0 == s1 and r1 > 0)
        selected = v1 if valid else v0
        target = int((c1 if valid else c0) > 0)
        raw = [v0, v1, float(s0), float(s1), float(r1), 0.0]
        structured = raw + [v1 - v0, valid, selected]
        # One coarse readout makes the hierarchy/memory interface explicit.
        structured.append(float(v0 >= 0.0))
        structured.append(float(v1 >= 0.0))
        rows.append((raw, structured))
        labels.append(target)
        patterns.append(pattern)
    raw_x = np.asarray([r[0] for r in rows], dtype=float)
    structured_x = np.asarray([r[1] for r in rows], dtype=float)
    return raw_x, structured_x, np.asarray(labels, dtype=int), np.asarray(patterns)


def fit(x: np.ndarray, y: np.ndarray, hidden: int, seed: int) -> MLPClassifier:
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


def metrics(model: MLPClassifier, x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    p = model.predict_proba(x)[:, 1]
    return {
        "accuracy": float(accuracy_score(y, p >= 0.5)),
        "brier": float(brier_score_loss(y, p)),
    }


def run(seed: int) -> dict:
    raw_train, structured_train, y_train, _ = generate(seed, TRAIN_N, True)
    raw_test, structured_test, y_test, patterns = generate(seed + 1000, TEST_N, False)
    # Structured dimension = 11; raw dimension = 6.
    # Widths are chosen so both pairs have 209 trainable parameters.
    raw_model = fit(raw_train, y_train, hidden=26, seed=seed)
    structured_model = fit(structured_train, y_train, hidden=16, seed=seed)
    raw_all = metrics(raw_model, raw_test, y_test)
    structured_all = metrics(structured_model, structured_test, y_test)
    held = np.all(patterns == np.asarray(HELD_OUT), axis=1)
    raw_held = metrics(raw_model, raw_test[held], y_test[held])
    structured_held = metrics(structured_model, structured_test[held], y_test[held])
    return {
        "seed": seed,
        "held_out_pattern": list(HELD_OUT),
        "held_out_n": int(held.sum()),
        "raw_mprime": raw_all,
        "structured_skeleton": structured_all,
        "raw_mprime_held_out": raw_held,
        "structured_skeleton_held_out": structured_held,
        "delta_accuracy_all": structured_all["accuracy"] - raw_all["accuracy"],
        "delta_accuracy_held_out": structured_held["accuracy"] - raw_held["accuracy"],
        "delta_brier_all": raw_all["brier"] - structured_all["brier"],
        "delta_brier_held_out": raw_held["brier"] - structured_held["brier"],
        "raw_params": parameter_count(6, 26),
        "structured_params": parameter_count(11, 16),
    }


def summarize(rows: list[dict], key: str) -> dict[str, float]:
    values = np.asarray([row[key] for row in rows], dtype=float)
    sd = float(values.std(ddof=1))
    return {
        "mean": float(values.mean()),
        "sd": sd,
        "ci95_half_width": float(2.776 * sd / np.sqrt(len(values))),
    }


def main() -> None:
    rows = [run(seed) for seed in SEEDS]
    summary = {
        key: summarize(rows, key)
        for key in (
            "delta_accuracy_all",
            "delta_accuracy_held_out",
            "delta_brier_all",
            "delta_brier_held_out",
        )
    }
    code_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    protocol_hash = hashlib.sha256((ROOT / "EXTENDED_PROTOCOL.md").read_bytes()).hexdigest()
    payload = {
        "protocol": "FTS-Skeleton-v0.2",
        "status": "exploratory_inductive_bias",
        "script_sha256": code_hash,
        "protocol_sha256": protocol_hash,
        "seeds": list(SEEDS),
        "train_n": TRAIN_N,
        "test_n": TEST_N,
        "held_out_pattern": list(HELD_OUT),
        "rows": rows,
        "summary": summary,
        "parameter_counts": {"raw_mprime": parameter_count(6, 26), "structured": parameter_count(11, 16)},
    }
    (ROOT / "extended_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    held = summary["delta_accuracy_held_out"]
    full = summary["delta_accuracy_all"]
    lines = [
        "# FTS-Skeleton v0.2 — результаты provenance/revision/memory пробы",
        "",
        f"- Статус: {payload['status']}",
        f"- SHA256 кода: {code_hash}",
        f"- SHA256 протокола: {protocol_hash}",
        "- Parameter counts: raw M' = 209; structured = 209",
        "",
        "| Контраст | mean delta | 95% half-width |",
        "|---|---:|---:|",
        f"| Held-out pattern accuracy | {held['mean']:.4f} | {held['ci95_half_width']:.4f} |",
        f"| Full test accuracy | {full['mean']:.4f} | {full['ci95_half_width']:.4f} |",
        "",
        "## Интерпретация",
        "",
        "Проба проверяет локальный inductive-bias effect explicit gate and",
        "selected-memory feature. Даже положительный результат не означает,",
        "что gate уникален для ФТС: такую же операцию можно объявить стандартным",
        "symbolic prior или включить в независимую M'.",
        "",
    ]
    (ROOT / "EXTENDED_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
