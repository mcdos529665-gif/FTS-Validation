#!/usr/bin/env python3
"""Validate E5 schemas, screening adjudication, and BibTeX DOI retention."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from pathlib import Path

DECISIONS = {"include", "exclude", "uncertain"}
RELATIONS = {"direct", "limiting", "alternative", "analogy"}
REQUIRED = {
    "SEARCH_LOG.tsv": ["query_id", "provider", "retrieved_at", "claim_or_oq", "query", "result_count", "notes"],
    "CANDIDATES.tsv": ["record_id", "doi", "s2_paper_id", "consensus_id", "title", "year", "provider", "retrieved_at", "query_id", "claim_or_oq", "screening_decision", "screening_reason", "fts_relation"],
    "SCREENING_CODEX.tsv": ["record_id", "decision", "reason", "reviewer", "locked_at"],
    "SCREENING_RESEARCHER.tsv": ["record_id", "decision", "reason", "reviewer", "locked_at"],
    "ADJUDICATION.tsv": ["record_id", "codex_decision", "researcher_decision", "final_decision", "reason", "approved_by", "approved_at"],
    "CITATION_GRAPH.tsv": ["source_record_id", "target_record_id", "edge_type", "provider", "retrieved_at"],
    "EVIDENCE_MATRIX.tsv": ["record_id", "claim_or_oq", "finding", "direction", "fts_relation", "limitations", "source_pointer"],
}
PAPER_INTAKE_HEADER = [
    "record_id",
    "doi",
    "s2_paper_id",
    "title",
    "year",
    "provider",
    "retrieved_at",
    "query_id",
    "claim_or_oq",
    "screening_decision",
    "screening_reason",
    "fts_relation",
    "source_path",
    "source_sha256",
    "project_path",
    "lines",
    "display_math_delimiters",
    "image_links",
    "references_present",
    "russian_dossier",
    "intake_status",
]


def read_tsv(path: Path, expected: list[str]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != expected:
            raise ValueError(f"{path.name}: header mismatch: {reader.fieldnames!r}")
        return list(reader)


def bib_dois(path: Path) -> set[str]:
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    values = re.findall(r"\bdoi\s*=\s*[\{\"]([^}\"]+)", text, flags=re.IGNORECASE)
    return {v.strip().lower().removeprefix("https://doi.org/") for v in values}


def bib_has_entries(path: Path) -> bool:
    return path.exists() and bool(re.search(r"^\s*@", path.read_text(encoding="utf-8"), flags=re.MULTILINE))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_inside(root: Path, relative: str) -> Path | None:
    if not relative:
        return None
    candidate = (root / relative).resolve()
    resolved_root = root.resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        return None
    return candidate


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    rows: dict[str, list[dict[str, str]]] = {}
    for name, header in REQUIRED.items():
        path = root / name
        if not path.exists():
            errors.append(f"missing {name}")
            continue
        try:
            rows[name] = read_tsv(path, header)
        except ValueError as exc:
            errors.append(str(exc))

    candidates = rows.get("CANDIDATES.tsv", [])
    candidates_by_id = {row["record_id"]: row for row in candidates if row["record_id"]}
    ids = [row["record_id"] for row in candidates if row["record_id"]]
    if len(ids) != len(set(ids)):
        errors.append("CANDIDATES.tsv: duplicate record_id")
    for row in candidates:
        if row["screening_decision"] and row["screening_decision"] not in DECISIONS:
            errors.append(f"{row['record_id']}: invalid screening_decision")
        if row["fts_relation"] and row["fts_relation"] not in RELATIONS:
            errors.append(f"{row['record_id']}: invalid fts_relation")

    screens: dict[str, dict[str, str]] = {}
    for name in ("SCREENING_CODEX.tsv", "SCREENING_RESEARCHER.tsv"):
        current: dict[str, str] = {}
        for row in rows.get(name, []):
            if row["decision"] not in DECISIONS:
                errors.append(f"{name}:{row['record_id']}: invalid decision")
            current[row["record_id"]] = row["decision"]
        screens[name] = current

    adjudicated = {row["record_id"]: row for row in rows.get("ADJUDICATION.tsv", [])}
    shared = set(screens.get("SCREENING_CODEX.tsv", {})) & set(screens.get("SCREENING_RESEARCHER.tsv", {}))
    for record_id in shared:
        codex = screens["SCREENING_CODEX.tsv"][record_id]
        researcher = screens["SCREENING_RESEARCHER.tsv"][record_id]
        if codex != researcher:
            row = adjudicated.get(record_id)
            if not row or row["final_decision"] not in DECISIONS or not row["approved_by"]:
                errors.append(f"{record_id}: unresolved screening disagreement")

    seed_dois = bib_dois(root / "seed_set.bib")
    rr_dois = bib_dois(root / "researchrabbit_export.bib")
    if bib_has_entries(root / "researchrabbit_export.bib") and not seed_dois.issubset(rr_dois):
        errors.append("researchrabbit_export.bib: seed DOI loss")

    intake_path = root / "PAPER_INTAKE.tsv"
    if intake_path.exists():
        try:
            intake = read_tsv(intake_path, PAPER_INTAKE_HEADER)
        except ValueError as exc:
            errors.append(str(exc))
            intake = []

        intake_ids = [row["record_id"] for row in intake if row["record_id"]]
        if len(intake_ids) != len(set(intake_ids)):
            errors.append("PAPER_INTAKE.tsv: duplicate record_id")

        for row in intake:
            record_id = row["record_id"]
            candidate = candidates_by_id.get(record_id)
            if candidate is None:
                errors.append(f"PAPER_INTAKE.tsv:{record_id}: record absent from CANDIDATES.tsv")
            elif row["doi"].lower() != candidate["doi"].lower():
                errors.append(f"PAPER_INTAKE.tsv:{record_id}: DOI differs from CANDIDATES.tsv")

            if row["screening_decision"] not in DECISIONS:
                errors.append(f"PAPER_INTAKE.tsv:{record_id}: invalid screening_decision")
            if row["fts_relation"] not in RELATIONS:
                errors.append(f"PAPER_INTAKE.tsv:{record_id}: invalid fts_relation")
            if row["intake_status"] != "imported":
                errors.append(f"PAPER_INTAKE.tsv:{record_id}: intake_status must be imported")

            expected_hash = row["source_sha256"].lower()
            if not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
                errors.append(f"PAPER_INTAKE.tsv:{record_id}: invalid source_sha256")

            project_file = resolve_inside(root, row["project_path"])
            if project_file is None:
                errors.append(f"PAPER_INTAKE.tsv:{record_id}: project_path escapes workspace")
            elif not project_file.is_file():
                errors.append(f"PAPER_INTAKE.tsv:{record_id}: missing project source")
            elif re.fullmatch(r"[0-9a-f]{64}", expected_hash) and file_sha256(project_file) != expected_hash:
                errors.append(f"PAPER_INTAKE.tsv:{record_id}: project source SHA256 mismatch")

            source_file = Path(row["source_path"])
            if source_file.exists() and re.fullmatch(r"[0-9a-f]{64}", expected_hash):
                if file_sha256(source_file) != expected_hash:
                    errors.append(f"PAPER_INTAKE.tsv:{record_id}: external source SHA256 mismatch")

            dossier = resolve_inside(root, row["russian_dossier"])
            if dossier is None:
                errors.append(f"PAPER_INTAKE.tsv:{record_id}: russian_dossier escapes workspace")
            elif not dossier.is_file():
                errors.append(f"PAPER_INTAKE.tsv:{record_id}: missing russian dossier")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print("PASS E5 workspace schemas and checkpoints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
