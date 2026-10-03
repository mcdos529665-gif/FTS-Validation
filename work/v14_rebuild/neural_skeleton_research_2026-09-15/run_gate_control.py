"""Non-uniqueness control for the v0.2 derived feature map."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, brier_score_loss
from sklearn.neural_network import MLPClassifier

from run_extended_probe import (
    HELD_OUT,
    SEEDS,
    TEST_N,
    TRAIN_N,
    fit,
    generate,
    parameter_count,
)

ROOT = Path(__file__).resolve().parent


def standard_symbolic_gate(raw: np.ndarray) -> np.ndarray:
    v0, v1, s0, s1, r1, r0 = raw.T
    valid = ((s0 == s1) & (r1 > 0)).astype(float)
    selected = np.where(valid > 0.0, v1, v0)
    return np.column_stack(
        (raw, v1 - v0, valid, selected, v0 >= 0.0, v1 >= 0.0)
    ).astype(float)


def score(model: MLPClassifier, x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    p = model.predict_proba(x)[:, 1]
    return {
        "accuracy": float(accuracy_score(y, p >= 0.5)),
        "brier": float(brier_score_loss(y, p)),
    }


def run(seed: int) -> dict:
    raw_train, structured_train, y_train, _ = generate(seed, TRAIN_N, True)
    raw_test, structured_test, y_test, patterns = generate(seed + 1000, TEST_N, False)
    control_train = standard_symbolic_gate(raw_train)
    control_test = standard_symbolic_gate(raw_test)
    map_error_train = float(np.max(np.abs(control_train - structured_train)))
    map_error_test = float(np.max(np.abs(control_test - structured_test)))
    reference = fit(structured_train, y_train, hidden=16, seed=seed)
    control = fit(control_train, y_train, hidden=16, seed=seed)
    held = np.all(patterns == np.asarray(HELD_OUT), axis=1)
    ref_all = score(reference, structured_test, y_test)
    ctl_all = score(control, control_test, y_test)
    ref_held = score(reference, structured_test[held], y_test[held])
    ctl_held = score(control, control_test[held], y_test[held])
    return {
        "seed": seed,
        "map_error_train": map_error_train,
        "map_error_test": map_error_test,
        "reference_all": ref_all,
        "control_all": ctl_all,
        "reference_held_out": ref_held,
        "control_held_out": ctl_held,
        "delta_accuracy_all": ctl_all["accuracy"] - ref_all["accuracy"],
        "delta_accuracy_held_out": ctl_held["accuracy"] - ref_held["accuracy"],
        "parameter_count": parameter_count(11, 16),
    }


def main() -> None:
    rows = [run(seed) for seed in SEEDS]
    all_deltas = np.asarray([r["delta_accuracy_all"] for r in rows])
    held_deltas = np.asarray([r["delta_accuracy_held_out"] for r in rows])
    code_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    protocol_hash = hashlib.sha256((ROOT / "GATE_CONTROL_PROTOCOL.md").read_bytes()).hexdigest()
    payload = {
        "protocol": "symbolic-gate-Mprime-control",
        "status": "equivalence_control",
        "script_sha256": code_hash,
        "protocol_sha256": protocol_hash,
        "rows": rows,
        "max_feature_map_error": max(
            max(r["map_error_train"], r["map_error_test"]) for r in rows
        ),
        "mean_delta_accuracy_all": float(all_deltas.mean()),
        "mean_delta_accuracy_held_out": float(held_deltas.mean()),
    }
    (ROOT / "gate_control_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Symbolic-gate M′ control — results",
        "",
        f"- Status: {payload['status']}",
        f"- Code SHA256: {code_hash}",
        f"- Protocol SHA256: {protocol_hash}",
        f"- Max feature-map error: {payload['max_feature_map_error']:.8f}",
        f"- Mean control minus reference delta, full test: {payload['mean_delta_accuracy_all']:.8f}",
        f"- Mean control minus reference delta, held-out: {payload['mean_delta_accuracy_held_out']:.8f}",
        "",
        "The control uses the same derived fields through an ordinary symbolic",
        "preprocessor. This is a non-uniqueness control, not another FTS-positive",
        "experiment.",
        "",
    ]
    (ROOT / "GATE_CONTROL_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

