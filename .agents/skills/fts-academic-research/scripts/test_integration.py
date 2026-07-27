#!/usr/bin/env python3
"""Offline tests for S2 backoff and E5 DOI round-trip validation."""

from __future__ import annotations

import csv
import hashlib
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


def write_tsv(path: Path, header: list[str], rows: list[list[str]] | None = None) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows or [])


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


def test_fulltext_intake() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        for name, header in e5.REQUIRED.items():
            if name == "CANDIDATES.tsv":
                row = [
                    "E5-T01", "10.1/test", "", "", "Test", "2026", "local", "now",
                    "Q", "oq", "include", "reason", "direct",
                ]
                write_tsv(root / name, header, [row])
            else:
                write_tsv(root / name, header)

        paper_dir = root / "papers" / "E5-T01"
        paper_dir.mkdir(parents=True)
        source = paper_dir / "source.en.md"
        source.write_text("# Test\n", encoding="utf-8")
        dossier = paper_dir / "DOSSIER.ru.md"
        dossier.write_text("# Тест\n", encoding="utf-8")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        intake_row = [
            "E5-T01", "10.1/test", "", "Test", "2026", "local", "now", "Q", "oq",
            "include", "reason", "direct", str(source), digest,
            "papers/E5-T01/source.en.md", "1", "0", "0", "true",
            "papers/E5-T01/DOSSIER.ru.md", "imported",
        ]
        write_tsv(root / "PAPER_INTAKE.tsv", e5.PAPER_INTAKE_HEADER, [intake_row])
        assert e5.validate(root) == []

        source.write_text("# Changed\n", encoding="utf-8")
        assert "PAPER_INTAKE.tsv:E5-T01: project source SHA256 mismatch" in e5.validate(root)


if __name__ == "__main__":
    test_s2_backoff()
    test_e5_roundtrip()
    test_fulltext_intake()
    print("PASS S2 backoff, DOI normalization, ResearchRabbit round-trip, and full-text intake")
