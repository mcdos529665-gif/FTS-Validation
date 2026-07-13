# -*- coding: utf-8 -*-
"""Reproducible audit gates for the FTS v13/v14 review package.

Usage:
    python -X utf8 work/v14_rebuild/audit/run_audit.py integrity
    python -X utf8 work/v14_rebuild/audit/run_audit.py traceability
    python -X utf8 work/v14_rebuild/audit/run_audit.py formal
    python -X utf8 work/v14_rebuild/audit/run_audit.py empirical
    python -X utf8 work/v14_rebuild/audit/run_audit.py all

The runner never edits source/. P0/P1 findings make the process fail. Known
immutable-v13 reference defects are accepted only when explicitly classified in
CANON_REFERENCE_PATCH.tsv.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "source"
REBUILD = ROOT / "work" / "v14_rebuild"
PAPER = REBUILD / "FTS_v14_paper.md"
EXPORT = REBUILD / "export"


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    resolved: bool = False


FINDINGS: list[Finding] = []


def add(severity: str, code: str, message: str, *, resolved: bool = False) -> None:
    FINDINGS.append(Finding(severity, code, message, resolved))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_cards() -> list[dict]:
    return [json.loads(line) for line in (SOURCE / "fts_cards.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]


def read_triples() -> list[dict[str, str]]:
    with (SOURCE / "fts_triples.tsv").open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def read_reference_patch() -> set[tuple[str, str, str]]:
    with (HERE / "CANON_REFERENCE_PATCH.tsv").open(encoding="utf-8", newline="") as fh:
        return {
            (row["source"], row["reference_kind"], row["unresolved_target"])
            for row in csv.DictReader(fh, delimiter="\t")
        }


def check_integrity() -> None:
    manifest = json.loads((SOURCE / "MANIFEST.json").read_text(encoding="utf-8"))
    failures = []
    for item in manifest["files"]:
        path = SOURCE / item["path"]
        if not path.exists() or path.stat().st_size != item["size"] or sha256(path) != item["sha256"]:
            failures.append(item["path"])
    if failures:
        add("P0", "MANIFEST", f"Manifest mismatch: {failures}")

    cards = read_cards()
    required = {"id", "type", "text", "depends_on", "tags", "path", "status", "internal_ref", "symbol", "title"}
    ids = [card.get("id") for card in cards]
    if len(ids) != len(set(ids)):
        add("P0", "DUPLICATE_ID", "Duplicate card IDs found")
    for card in cards:
        missing = required - set(card)
        if missing:
            add("P1", "CARD_SCHEMA", f"{card.get('id')}: missing {sorted(missing)}")

    triples = read_triples()
    card_ids = set(ids)
    patch = read_reference_patch()
    for card in cards:
        for dep in card.get("depends_on", []):
            if dep not in card_ids and (card["id"], "depends_on", dep) not in patch:
                add("P1", "UNCLASSIFIED_DEP", f"{card['id']} depends_on missing {dep}")
    for row in triples:
        subject = row["subject"]
        if subject not in card_ids and row["predicate"] in {"depends_on", "promotes_status_of", "does_not_promote_above"}:
            if (subject, "triple_subject", subject) not in patch:
                add("P1", "UNCLASSIFIED_SUBJECT", f"Missing triple subject {subject}")

    diff = subprocess.run(
        ["git", "diff", "--quiet", "--", "source"], cwd=ROOT, check=False
    )
    if diff.returncode != 0:
        add("P0", "SOURCE_MUTATED", "source/ differs from the audit baseline")

    checksums = EXPORT / "CHECKSUMS.sha256"
    if checksums.exists():
        for line in checksums.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, name = line.split(maxsplit=1)
            name = name.lstrip("*")
            path = EXPORT / name
            if not path.exists() or sha256(path) != expected.lower():
                add("P1", "EXPORT_HASH", f"Checksum mismatch: {name}")


def expand_c_refs(value: str) -> set[str]:
    found: set[str] = set()
    for match in re.finditer(r"C[- ]?(\d{1,2})(?:\s*[–—-]\s*C?[- ]?(\d{1,2}))?", value):
        lo = int(match.group(1))
        hi = int(match.group(2) or lo)
        found.update(f"C{number:02d}" for number in range(lo, hi + 1))
    return found


def check_traceability() -> None:
    matrix = HERE / "CLAIM_MATRIX.tsv"
    if not matrix.exists():
        add("P1", "CLAIM_MATRIX_MISSING", "CLAIM_MATRIX.tsv is missing")
        return
    with matrix.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    required = {
        "claim_id", "claim", "domain", "source", "verification",
        "status_before", "status_after", "verdict", "resolution",
    }
    if not rows or set(rows[0]) != required:
        add("P1", "CLAIM_MATRIX_SCHEMA", f"Expected columns: {sorted(required)}")
        return
    claim_ids = [row["claim_id"] for row in rows]
    if len(claim_ids) != len(set(claim_ids)):
        add("P1", "CLAIM_ID_DUP", "Duplicate claim IDs in claim matrix")
    for row in rows:
        for field in required:
            if not row[field].strip():
                add("P1", "CLAIM_FIELD_EMPTY", f"{row['claim_id']}: empty {field}")

    covered = set().union(*(expand_c_refs(row["verification"]) for row in rows))
    expected = {f"C{number:02d}" for number in range(1, 63)}
    if covered != expected:
        add("P1", "CLAIM_COVERAGE", f"C coverage missing={sorted(expected-covered)}, extra={sorted(covered-expected)}")

    paper = PAPER.read_text(encoding="utf-8")
    if "59 машинных проверок" in paper:
        add("P2", "STALE_COUNT", "Current paper still says 59 machine checks")
    export_paper = EXPORT / "FTS_v14_paper.md"
    if export_paper.exists() and export_paper.read_bytes() != PAPER.read_bytes():
        add("P2", "EXPORT_PAPER_DRIFT", "Export paper differs from working paper")


def check_formal() -> None:
    source = (REBUILD / "verification.py").read_text(encoding="utf-8")
    if "or True" in source or "if False" in source:
        add("P1", "VACUOUS_CHECK", "verification.py contains a vacuous truth branch")
    ids = re.findall(r'check\("(C\d{2})"', source)
    expected = [f"C{number:02d}" for number in range(1, 63)]
    if ids != expected:
        add("P1", "FORMAL_IDS", "C IDs are missing, duplicated, or out of order")
    proc = subprocess.run(
        [sys.executable, "-X", "utf8", str(REBUILD / "verification.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        add("P1", "FORMAL_FAIL", proc.stdout[-2000:] + proc.stderr[-1000:])


def check_empirical() -> None:
    radio = REBUILD / "d10_phase" / "radioml" / "RML2016.10a_dict.pkl"
    expected = "b29ccc25b00d0718cd3b70ffa9158662ec83f6d9b63ffd845c7bcbe3b3096e8c"
    if not radio.exists() or sha256(radio) != expected:
        add("P1", "RADIOML_INPUT", "RadioML input is missing or has an unexpected hash")
    for path in [
        REBUILD / "o20" / "AUDIT_REANALYSIS.md",
        REBUILD / "d2_sign" / "AUDIT_REANALYSIS.md",
        HERE / "REPRODUCIBILITY.md",
    ]:
        if not path.exists():
            add("P1", "REANALYSIS_MISSING", f"Missing {path.relative_to(ROOT)}")


def run(mode: str) -> int:
    if mode in {"integrity", "all"}:
        check_integrity()
    if mode in {"traceability", "all"}:
        check_traceability()
    if mode in {"formal", "all"}:
        check_formal()
    if mode in {"empirical", "all"}:
        check_empirical()
    if mode not in {"integrity", "traceability", "formal", "empirical", "all"}:
        print(f"unknown mode: {mode}", file=sys.stderr)
        return 2

    for finding in FINDINGS:
        suffix = " [RESOLVED]" if finding.resolved else ""
        print(f"{finding.severity} {finding.code}: {finding.message}{suffix}")
    blockers = [f for f in FINDINGS if f.severity in {"P0", "P1"} and not f.resolved]
    print(f"AUDIT {mode}: findings={len(FINDINGS)} blockers={len(blockers)}")
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1] if len(sys.argv) > 1 else "all"))
