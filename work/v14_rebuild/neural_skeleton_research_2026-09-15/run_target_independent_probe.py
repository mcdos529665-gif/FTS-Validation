"""Target-independent and cross-domain probe for FTS-Skeleton v0.3."""
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
TRAIN_N = 1000
TEST_N = 5000
HELD_OUT = (1, 0, 1)


def params(input_dim: int, hidden: int) -> int:
    return (input_dim + 1) * hidden + (hidden + 1)


def generate(seed: int, n: int, dim: int, exclude_held_out: bool):
    rng = np.random.default_rng(seed)
    rows = []
    y_a = []
    y_b = []
    patterns = []
    while len(rows) < n:
        c0 = rng.choice((-1.0, 1.0), size=dim)
        c1 = rng.choice((-1.0, 1.0), size=dim)
        v0 = c0 + rng.normal(scale=0.8, size=dim)
        v1 = c1 + rng.normal(scale=0.8, size=dim)
        s0 = int(rng.integers(0, 2))
        s1 = int(rng.integers(0, 2))
        r1 = int(rng.integers(0, 2))
        pattern = (s0, s1, r1)
        if exclude_held_out and pattern == HELD_OUT:
            continue
        valid = float(s0 == s1 and r1 > 0)
        selected = v1 if valid else v0
        raw = np.concatenate((v0, v1, [float(s0), float(s1), float(r1), 0.0]))
        structured = np.concatenate(
            (raw, v1 - v0, [valid], selected)
        )
        residual0 = v1[0] - v0[0]
        target_a = int(selected[0] > 0.0)
        target_b = int((selected[0] + 0.5 * residual0) > 0.0)
        rows.append((raw, structured))
        y_a.append(target_a)
        y_b.append(target_b)
        patterns.append(pattern)
    raw_x = np.asarray([r[0] for r in rows], dtype=float)
    structured_x = np.asarray([r[1] for r in rows], dtype=float)
    return (
        raw_x,
        structured_x,
        np.asarray(y_a, dtype=int),
        np.asarray(y_b, dtype=int),
        np.asarray(patterns),
    )


def fit(x: np.ndarray, y: np.ndarray, hidden: int, seed: int):
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


def score(model, x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    p = model.predict_proba(x)[:, 1]
    return {
        "accuracy": float(accuracy_score(y, p >= 0.5)),
        "brier": float(brier_score_loss(y, p)),
    }


def run(seed: int, dim: int, target_name: str) -> dict:
    raw_train, structured_train, y_a_train, y_b_train, _ = generate(
        seed, TRAIN_N, dim, True
    )
    raw_test, structured_test, y_a_test, y_b_test, patterns = generate(
        seed + 1000, TEST_N, dim, False
    )
    y_train = y_a_train if target_name == "A" else y_b_train
    y_test = y_a_test if target_name == "A" else y_b_test
    if dim == 1:
        raw_hidden, structured_hidden = 22, 16
    else:
        raw_hidden, structured_hidden = 24, 16
    raw_model = fit(raw_train, y_train, raw_hidden, seed)
    structured_model = fit(structured_train, y_train, structured_hidden, seed)
    held = np.all(patterns == np.asarray(HELD_OUT), axis=1)
    raw_all = score(raw_model, raw_test, y_test)
    structured_all = score(structured_model, structured_test, y_test)
    raw_held = score(raw_model, raw_test[held], y_test[held])
    structured_held = score(structured_model, structured_test[held], y_test[held])
    return {
        "seed": seed,
        "dim": dim,
        "target": target_name,
        "held_out_n": int(held.sum()),
        "raw_params": params(raw_train.shape[1], raw_hidden),
        "structured_params": params(structured_train.shape[1], structured_hidden),
        "raw_all": raw_all,
        "structured_all": structured_all,
        "raw_held": raw_held,
        "structured_held": structured_held,
        "delta_accuracy_all": structured_all["accuracy"] - raw_all["accuracy"],
        "delta_accuracy_held": structured_held["accuracy"] - raw_held["accuracy"],
        "delta_brier_all": raw_all["brier"] - structured_all["brier"],
        "delta_brier_held": raw_held["brier"] - structured_held["brier"],
    }


def summarize(rows: list[dict], key: str) -> dict[str, float]:
    values = np.asarray([r[key] for r in rows], dtype=float)
    sd = float(values.std(ddof=1))
    return {
        "mean": float(values.mean()),
        "sd": sd,
        "ci95_half_width": float(2.776 * sd / np.sqrt(len(values))),
        "positive_seeds": int((values > 0).sum()),
    }


def main() -> None:
    rows = []
    for seed in SEEDS:
        for dim in (1, 2):
            for target in ("A", "B"):
                rows.append(run(seed, dim, target))
    summaries = {}
    for dim in (1, 2):
        for target in ("A", "B"):
            subset = [r for r in rows if r["dim"] == dim and r["target"] == target]
            key = f"dim{dim}_target{target}"
            summaries[key] = {
                "delta_accuracy_all": summarize(subset, "delta_accuracy_all"),
                "delta_accuracy_held": summarize(subset, "delta_accuracy_held"),
                "delta_brier_all": summarize(subset, "delta_brier_all"),
                "delta_brier_held": summarize(subset, "delta_brier_held"),
            }
    code_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    protocol_hash = hashlib.sha256(
        (ROOT / "TARGET_INDEPENDENT_PROTOCOL.md").read_bytes()
    ).hexdigest()
    payload = {
        "protocol": "FTS-Skeleton-v0.3",
        "status": "target_independent_cross_domain_probe",
        "script_sha256": code_hash,
        "protocol_sha256": protocol_hash,
        "seeds": list(SEEDS),
        "train_n": TRAIN_N,
        "test_n": TEST_N,
        "rows": rows,
        "summaries": summaries,
    }
    (ROOT / "target_independent_results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# FTS-Skeleton v0.3 — target-independent / cross-domain results",
        "",
        f"- Status: {payload['status']}",
        f"- Code SHA256: {code_hash}",
        f"- Protocol SHA256: {protocol_hash}",
        "",
        "| Domain | Readout | Held-out delta | Full delta | Positive held-out seeds |",
        "|---:|:---:|---:|---:|---:|",
    ]
    for key, summary in summaries.items():
        dim = key[3]
        target = key[-1]
        held = summary["delta_accuracy_held"]
        full = summary["delta_accuracy_all"]
        lines.append(
            f"| {dim}D | {target} | {held['mean']:.4f} ± {held['ci95_half_width']:.4f} | "
            f"{full['mean']:.4f} ± {full['ci95_half_width']:.4f} | {held['positive_seeds']}/5 |"
        )
    lines += [
        "",
        "Interpretation is limited to transfer of an explicit gate/selected-memory",
        "inductive bias. It does not establish FTS-specificity or biological validity.",
        "",
    ]
    (ROOT / "TARGET_INDEPENDENT_RESULTS.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

