# -*- coding: utf-8 -*-
"""Изолированное воспроизведение всех исторических вариантов Д10.

Скрипты Д10 исторически пишут результаты рядом с собой. Аудиторский запуск
динамически загружает каждый скрипт, перенаправляет его ``HERE`` в
``audit/reproductions/d10/<variant>`` и сравнивает новый JSON с исходным.
Предрегистрации и исторические результаты не изменяются.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import json
import os
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
import sklearn

from data_paths import (
    RADIOML_EXPECTED_SHA256,
    RADIOML_EXPECTED_SIZE,
    radioml_search_summary,
    resolve_radioml_path,
)


AUDIT_DIR = Path(__file__).resolve().parent
REBUILD_DIR = AUDIT_DIR.parent
D10_DIR = REBUILD_DIR / "d10_phase"
OUTPUT_ROOT = AUDIT_DIR / "reproductions" / "d10"
RADIOML = resolve_radioml_path()

VARIANTS = {
    "synthetic-v1": (D10_DIR / "run_d10.py", D10_DIR / "results.json", "results.json"),
    "synthetic-pilot": (D10_DIR / "pilot" / "run_pilot.py", D10_DIR / "pilot" / "results.json", "results.json"),
    "radioml-v1": (D10_DIR / "radioml" / "run_radioml.py", D10_DIR / "radioml" / "results.json", "results.json"),
    "radioml-v2": (D10_DIR / "radioml" / "run_radioml_v2.py", D10_DIR / "radioml" / "results_v2.json", "results_v2.json"),
    "radioml-v3": (D10_DIR / "radioml" / "run_radioml_v3.py", D10_DIR / "radioml" / "results_v3.json", "results_v3.json"),
}


def sha256(path: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def load_module(script: Path, name: str):
    spec = importlib.util.spec_from_file_location(f"fts_audit_{name.replace('-', '_')}", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_variant(name: str) -> dict:
    script, historical, output_name = VARIANTS[name]
    output_dir = OUTPUT_ROOT / name
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = output_dir / output_name
    if generated.exists():
        generated.unlink()

    module = load_module(script, name)
    module.HERE = str(output_dir)
    old_argv = sys.argv[:]
    if name.startswith("radioml"):
        sys.argv = [str(script), "--pkl", str(RADIOML)]
    else:
        sys.argv = [str(script)]

    started = time.perf_counter()
    stdout_path = output_dir / "stdout.txt"
    try:
        with stdout_path.open("w", encoding="utf-8", newline="\n") as stream, contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
            if name == "synthetic-v1":
                module.run()
            elif name == "synthetic-pilot":
                module.run()
            else:
                module.main()
    finally:
        sys.argv = old_argv
    runtime = time.perf_counter() - started

    if not generated.exists():
        raise RuntimeError(f"{name} did not create {generated}")
    historical_json = json.loads(historical.read_text(encoding="utf-8"))
    generated_json = json.loads(generated.read_text(encoding="utf-8"))
    record = {
        "variant": name,
        "script": str(script.relative_to(REBUILD_DIR.parent.parent)),
        "historical_result": str(historical.relative_to(REBUILD_DIR.parent.parent)),
        "generated_result": str(generated.relative_to(REBUILD_DIR.parent.parent)),
        "runtime_seconds": runtime,
        "historical_sha256": sha256(historical),
        "generated_sha256": sha256(generated),
        "semantic_json_equal": historical_json == generated_json,
        "byte_equal": historical.read_bytes() == generated.read_bytes(),
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("variants", nargs="*", choices=list(VARIANTS), help="по умолчанию — все варианты")
    args = parser.parse_args()
    selected = args.variants or list(VARIANTS)

    if any(name.startswith("radioml") for name in selected):
        if not RADIOML.exists():
            raise FileNotFoundError(f"RadioML не найден. Проверены: {radioml_search_summary()}")
        if RADIOML.stat().st_size != RADIOML_EXPECTED_SIZE:
            raise RuntimeError(f"RadioML size mismatch: {RADIOML.stat().st_size}")
        actual = sha256(RADIOML)
        if actual != RADIOML_EXPECTED_SHA256:
            raise RuntimeError(f"RadioML SHA256 mismatch: {actual}")

    records = []
    for name in selected:
        print(f"[D10] reproduce {name}", flush=True)
        record = run_variant(name)
        records.append(record)
        print(
            f"[D10] {name}: semantic_equal={record['semantic_json_equal']} "
            f"byte_equal={record['byte_equal']} runtime={record['runtime_seconds']:.1f}s",
            flush=True,
        )

    summary_path = OUTPUT_ROOT / "run_manifest.json"
    previous = {}
    if summary_path.exists():
        previous = {row["variant"]: row for row in json.loads(summary_path.read_text(encoding="utf-8"))["variants"]}
    previous.update({row["variant"]: row for row in records})
    try:
        radioml_manifest_path = str(RADIOML.relative_to(REBUILD_DIR.parent.parent))
    except ValueError:
        radioml_manifest_path = str(RADIOML)
    summary = {
        "analysis_kind": "isolated_historical_reproduction",
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "radioml": {
            "path": radioml_manifest_path,
            "size_bytes": RADIOML.stat().st_size if RADIOML.exists() else None,
            "sha256": sha256(RADIOML) if RADIOML.exists() else None,
        },
        "variants": [previous[name] for name in VARIANTS if name in previous],
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0 if all(row["semantic_json_equal"] for row in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
