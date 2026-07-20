#!/usr/bin/env python3
"""Offline tests for S2 backoff and E5 DOI round-trip validation."""

from __future__ import annotations

import csv
import importlib.util
import sys
import tempfile
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


s2 = load("s2_verify", "s2_verify.py")
e5 = load("validate_e5_workspace", "validate_e5_workspace.py")


class Response:
    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return b'{"paperId":"S2-1","title":"Exact"}'


def test_s2_backoff() -> None:
    calls: list[int] = []
    sleeps: list[float] = []

    def opener(_request, timeout=0):
        calls.append(timeout)
        if len(calls) == 1:
            raise urllib.error.HTTPError("https://example", 429, "rate", {"Retry-After": "2"}, None)
        return Response()

    ticks = iter([0.0, 0.0, 2.0, 2.0])
    client = s2.SemanticScholarClient(opener=opener, sleeper=sleeps.append, clock=lambda: next(ticks), min_interval=1.0)
    result = client.by_doi("https://doi.org/10.1/ABC")
    assert result["paperId"] == "S2-1"
    assert 2.0 in sleeps
    assert s2.normalize_doi("DOI:10.1/ABC") == "10.1/abc"


def write_tsv(path: Path, header: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        csv.writer(handle, delimiter="\t", lineterminator="\n").writerow(header)


def test_e5_roundtrip() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        for name, header in e5.REQUIRED.items():
            write_tsv(root / name, header)
        entry = "@article{seed,\n  title={Seed},\n  doi={10.1/abc}\n}\n"
        (root / "seed_set.bib").write_text(entry, encoding="utf-8")
        (root / "researchrabbit_export.bib").write_text(entry, encoding="utf-8")
        assert e5.validate(root) == []
        (root / "researchrabbit_export.bib").write_text("@article{x,title={X}}\n", encoding="utf-8")
        assert "researchrabbit_export.bib: seed DOI loss" in e5.validate(root)


if __name__ == "__main__":
    test_s2_backoff()
    test_e5_roundtrip()
    print("PASS S2 backoff, DOI normalization, and ResearchRabbit round-trip")
