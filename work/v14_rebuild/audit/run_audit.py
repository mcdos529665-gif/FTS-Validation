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

from data_paths import (
    RADIOML_EXPECTED_SHA256,
    RADIOML_EXPECTED_SIZE,
    radioml_search_summary,
    resolve_radioml_path,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "source"
REBUILD = ROOT / "work" / "v14_rebuild"
PAPER = REBUILD / "FTS_v14_paper.md"
EXPORT = REBUILD / "export"

ALLOWED_PREDICATES = {
    "asks_branch_of", "candidate_supports", "contains", "contrasts_with",
    "defeats_or_tests", "depends_on", "does_not_promote_above", "exports_to",
    "has_agentic_gate", "has_antimode", "has_antimode_detail", "has_boundary",
    "has_complex_overlay", "has_core", "has_local_forbid",
    "has_minimal_expression", "has_next", "has_operator",
    "has_private_expression", "has_statistical_overlay", "has_tensor_overlay",
    "has_window", "projects_to", "promotes_status_of", "requires", "supports",
    "uses_carrier",
}
LITERAL_OBJECT_PREDICATES = {
    "candidate_supports", "defeats_or_tests", "exports_to", "has_antimode",
    "has_window", "requires", "supports",
}
MIXED_OBJECT_PREDICATES = {"does_not_promote_above"}


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
        if not isinstance(card.get("id"), str) or not card.get("id"):
            add("P1", "CARD_ID_TYPE", f"Invalid card ID: {card.get('id')!r}")
        if not isinstance(card.get("depends_on"), list) or not all(
            isinstance(item, str) and item for item in card.get("depends_on", [])
        ):
            add("P1", "CARD_DEP_TYPE", f"{card.get('id')}: depends_on must be list[str]")
        if not isinstance(card.get("tags"), list) or not all(isinstance(item, str) for item in card.get("tags", [])):
            add("P1", "CARD_TAG_TYPE", f"{card.get('id')}: tags must be list[str]")

    triples = read_triples()
    if triples and set(triples[0]) != {"subject", "predicate", "object"}:
        add("P1", "TRIPLE_SCHEMA", f"Unexpected TSV fields: {sorted(triples[0])}")
    duplicate_count = len(triples) - len({(row["subject"], row["predicate"], row["object"]) for row in triples})
    if duplicate_count:
        add("P1", "DUPLICATE_TRIPLE", f"Duplicate triples: {duplicate_count}")
    unknown_predicates = sorted({row["predicate"] for row in triples} - ALLOWED_PREDICATES)
    if unknown_predicates:
        add("P1", "UNKNOWN_PREDICATE", f"Unknown predicates: {unknown_predicates}")
    for row in triples:
        if not all(isinstance(row.get(field), str) and row[field].strip() for field in ("subject", "predicate", "object")):
            add("P1", "TRIPLE_EMPTY", f"Malformed triple: {row}")

    card_ids = set(ids)
    patch = read_reference_patch()
    for card in cards:
        for dep in card.get("depends_on", []):
            if dep not in card_ids and (card["id"], "depends_on", dep) not in patch:
                add("P1", "UNCLASSIFIED_DEP", f"{card['id']} depends_on missing {dep}")
    for row in triples:
        subject, predicate, obj = row["subject"], row["predicate"], row["object"]
        if subject not in card_ids and (subject, "triple_subject", subject) not in patch:
            add("P1", "UNCLASSIFIED_SUBJECT", f"Missing triple subject {subject}")
        entity_required = predicate not in LITERAL_OBJECT_PREDICATES | MIXED_OBJECT_PREDICATES
        classified_object = (
            (subject, "triple_object", obj) in patch
            or (subject, predicate, obj) in patch
        )
        if entity_required and obj not in card_ids and not classified_object:
            add("P1", "UNCLASSIFIED_OBJECT", f"{subject} {predicate} missing entity {obj}")

    card_deps = {
        (card["id"], dep)
        for card in cards
        for dep in card.get("depends_on", [])
        if dep in card_ids
    }
    triple_deps = {
        (row["subject"], row["object"])
        for row in triples
        if row["predicate"] == "depends_on" and row["subject"] in card_ids and row["object"] in card_ids
    }
    if card_deps != triple_deps:
        add(
            "P2",
            "DEP_REPRESENTATION_DRIFT",
            f"card-only={len(card_deps-triple_deps)}, triple-only={len(triple_deps-card_deps)}; "
            "see GRAPH_RELATION_PATCH.tsv",
        )

    graph = {identifier: set() for identifier in card_ids}
    for source, target in card_deps:
        graph[source].add(target)
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    cycles: list[tuple[str, ...]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = low[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for neighbour in graph[node]:
            if neighbour not in indices:
                visit(neighbour)
                low[node] = min(low[node], low[neighbour])
            elif neighbour in on_stack:
                low[node] = min(low[node], indices[neighbour])
        if low[node] == indices[node]:
            component = []
            while True:
                item = stack.pop()
                on_stack.remove(item)
                component.append(item)
                if item == node:
                    break
            if len(component) > 1 or node in graph[node]:
                cycles.append(tuple(sorted(component)))

    for identifier in sorted(card_ids):
        if identifier not in indices:
            visit(identifier)
    expected_cycles = {
        ("ADD_MIRROR_WINDOW", "ADD_ZERO_BOUNDARY"),
        ("M_07", "U7_MATH_LOCAL_FORBID"),
        ("OP_WindowClose", "U7_WINDOW_CORE"),
    }
    if set(cycles) != expected_cycles:
        add("P1", "DEPENDENCY_CYCLE_DRIFT", f"Unexpected SCC set: {sorted(cycles)}")
    elif cycles:
        add("P2", "DEPENDENCY_CYCLES", f"Three documented SCCs: {sorted(cycles)}")

    for required_audit in (HERE / "GRAPH_AUDIT.md", HERE / "GRAPH_RELATION_PATCH.tsv"):
        if not required_audit.exists():
            add("P2", "GRAPH_AUDIT_MISSING", f"Missing {required_audit.name}")

    diff = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", "source"], cwd=ROOT, check=False
    )
    if diff.returncode != 0:
        add("P0", "SOURCE_MUTATED", "source/ differs from the audit baseline")

    checksums = EXPORT / "CHECKSUMS.sha256"
    if checksums.exists():
        listed_names: set[str] = set()
        for line in checksums.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            expected, name = line.split(maxsplit=1)
            name = name.lstrip("*")
            listed_names.add(name.replace("\\", "/"))
            path = EXPORT / name
            if not path.exists() or sha256(path) != expected.lower():
                add("P1", "EXPORT_HASH", f"Checksum mismatch: {name}")
        actual_names = {
            path.relative_to(EXPORT).as_posix()
            for path in EXPORT.rglob("*")
            if path.is_file() and path != checksums
        }
        if listed_names != actual_names:
            add(
                "P1", "EXPORT_CHECKSUM_COVERAGE",
                f"missing={sorted(actual_names-listed_names)}, stale={sorted(listed_names-actual_names)}",
            )


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

    if len(rows) < 25 or "CM-025" not in claim_ids:
        add("P1", "CLAIM_SCOPE", "Claim matrix does not cover the recorded 25 significant claim groups")

    findings_path = HERE / "FINDINGS.tsv"
    finding_fields = {
        "finding_id", "severity", "status", "area", "found", "dependencies",
        "conclusion", "unresolved", "resolution",
    }
    if not findings_path.exists():
        add("P1", "FINDINGS_MISSING", "FINDINGS.tsv is missing")
    else:
        with findings_path.open(encoding="utf-8", newline="") as fh:
            finding_rows = list(csv.DictReader(fh, delimiter="\t"))
        if not finding_rows or set(finding_rows[0]) != finding_fields:
            add("P1", "FINDINGS_SCHEMA", f"Expected columns: {sorted(finding_fields)}")
        else:
            finding_ids = [row["finding_id"] for row in finding_rows]
            if len(finding_ids) != len(set(finding_ids)):
                add("P1", "FINDINGS_DUP", "Duplicate finding IDs")
            for row in finding_rows:
                if any(not row[field].strip() for field in finding_fields):
                    add("P1", "FINDING_EMPTY", f"{row['finding_id']}: an audit field is empty")
                if row["severity"] not in {"P0", "P1", "P2", "P3"}:
                    add("P1", "FINDING_SEVERITY", f"{row['finding_id']}: {row['severity']}")
                if row["status"] not in {"resolved", "accepted_open", "external_step"}:
                    add("P1", "FINDING_STATUS", f"{row['finding_id']}: {row['status']}")
                if row["severity"] in {"P0", "P1"} and row["status"] != "resolved":
                    add(row["severity"], f"OPEN_{row['finding_id']}", row["conclusion"])
                if row["severity"] == "P2":
                    if row["status"] not in {"accepted_open", "external_step"}:
                        add("P1", "P2_UNCLASSIFIED", f"{row['finding_id']}: P2 must be explicitly open")
                    if "oq-" not in (row["unresolved"] + " " + row["resolution"]):
                        add("P1", "P2_WITHOUT_OQ", f"{row['finding_id']}: no open-question pointer")

    atlas_path = HERE / "PATTERN_ATLAS.tsv"
    atlas_fields = {
        "pattern_id", "name", "evidence_level", "domain", "statement", "sources",
        "verification", "counterexample_or_defeat", "open_question", "verdict",
    }
    allowed_levels = {"доказано", "канон-grounded", "кандидат", "опровергнуто/артефакт"}
    atlas_rows: list[dict[str, str]] = []
    atlas_valid = False
    if not atlas_path.exists():
        add("P1", "PATTERN_ATLAS_MISSING", "PATTERN_ATLAS.tsv is missing")
    else:
        with atlas_path.open(encoding="utf-8", newline="") as fh:
            atlas_rows = list(csv.DictReader(fh, delimiter="\t"))
        if not atlas_rows or set(atlas_rows[0]) != atlas_fields:
            add("P1", "PATTERN_ATLAS_SCHEMA", f"Expected columns: {sorted(atlas_fields)}")
        else:
            atlas_valid = True
            pattern_ids = [row["pattern_id"] for row in atlas_rows]
            if len(pattern_ids) != len(set(pattern_ids)):
                add("P1", "PATTERN_DUP", "Duplicate pattern IDs")
            actual_levels = {row["evidence_level"] for row in atlas_rows}
            if actual_levels != allowed_levels:
                add("P1", "PATTERN_LEVELS", f"Unexpected evidence levels: {sorted(actual_levels)}")
            oq_text = (ROOT / "work" / "OPEN_QUESTIONS.md").read_text(encoding="utf-8")
            oq_ids = set(re.findall(r"\{#(oq-[^}]+)\}", oq_text))
            for row in atlas_rows:
                if any(not row[field].strip() for field in atlas_fields):
                    add("P1", "PATTERN_EMPTY", f"{row['pattern_id']}: an atlas field is empty")
                if len([part for part in row["sources"].split(";") if part.strip()]) < 2:
                    add("P1", "PATTERN_SOURCES", f"{row['pattern_id']}: fewer than two recorded sources")
                used_oq = set(re.findall(r"oq-[a-z0-9-]+", row["open_question"]))
                if not used_oq or not used_oq.issubset(oq_ids):
                    add("P1", "PATTERN_OQ", f"{row['pattern_id']}: unknown/missing OQ {sorted(used_oq-oq_ids)}")

    map_path = HERE / "PATTERN_OQ_MAP.tsv"
    map_fields = {
        "oq_anchor", "oq_status", "research_program", "meta_pattern",
        "pattern_ids", "bridge_type", "common_blocker", "resolution_event",
        "resolution_kind", "note",
    }
    if not map_path.exists():
        add("P1", "PATTERN_OQ_MAP_MISSING", "PATTERN_OQ_MAP.tsv is missing")
    else:
        with map_path.open(encoding="utf-8", newline="") as fh:
            map_rows = list(csv.DictReader(fh, delimiter="\t"))
        if not map_rows or set(map_rows[0]) != map_fields:
            add("P1", "PATTERN_OQ_MAP_SCHEMA", f"Expected columns: {sorted(map_fields)}")
        else:
            oq_text = (ROOT / "work" / "OPEN_QUESTIONS.md").read_text(encoding="utf-8")
            active_pairs: list[tuple[str, str]] = []
            for marker, body in re.findall(
                r"(?ms)^- \[([ ~])\] (.*?)(?=^- \[[ x~]\] |\Z)", oq_text
            ):
                anchors = re.findall(r"\{#(oq-[^}]+)\}", body)
                if len(anchors) != 1:
                    add(
                        "P1", "OPEN_OQ_ANCHOR",
                        f"Active OQ must have one anchor; found {anchors} in {body[:80]!r}",
                    )
                    continue
                active_pairs.append((anchors[0], "partial" if marker == "~" else "open"))
            if len(active_pairs) != len({anchor for anchor, _ in active_pairs}):
                add("P1", "OPEN_OQ_DUP", "Duplicate active OQ anchors in OPEN_QUESTIONS.md")
            active_oq = dict(active_pairs)
            map_anchors = [row["oq_anchor"] for row in map_rows]
            if len(map_anchors) != len(set(map_anchors)):
                add("P1", "PATTERN_OQ_MAP_DUP", "Duplicate OQ anchors in pattern map")
            if set(map_anchors) != set(active_oq):
                add(
                    "P1", "PATTERN_OQ_MAP_COVERAGE",
                    f"OQ coverage missing={sorted(set(active_oq)-set(map_anchors))}, "
                    f"extra={sorted(set(map_anchors)-set(active_oq))}",
                )

            pattern_set = {row["pattern_id"] for row in atlas_rows} if atlas_valid else set()
            used_patterns: set[str] = set()
            map_by_oq: dict[str, tuple[dict[str, str], set[str]]] = {}
            for row in map_rows:
                anchor = row["oq_anchor"]
                if any(not row[field].strip() for field in map_fields):
                    add("P1", "PATTERN_OQ_MAP_EMPTY", f"{anchor}: an audit field is empty")
                if anchor in active_oq and row["oq_status"] != active_oq[anchor]:
                    add(
                        "P1", "PATTERN_OQ_MAP_STATUS",
                        f"{anchor}: map={row['oq_status']}, OPEN_QUESTIONS={active_oq[anchor]}",
                    )
                if row["research_program"] not in {f"RP-{number}" for number in range(1, 8)}:
                    add("P1", "PATTERN_OQ_MAP_PROGRAM", f"{anchor}: {row['research_program']}")
                meta = {part.strip() for part in row["meta_pattern"].split(";") if part.strip()}
                if not meta or not meta.issubset({"MP-A", "MP-B", "MP-C", "MP-S"}):
                    add("P1", "PATTERN_OQ_MAP_META", f"{anchor}: {sorted(meta)}")
                row_patterns = {
                    part.strip() for part in row["pattern_ids"].split(";") if part.strip()
                }
                invalid_patterns = row_patterns - pattern_set if atlas_valid else set()
                if not row_patterns or invalid_patterns:
                    add(
                        "P1", "PATTERN_OQ_MAP_PATTERN",
                        f"{anchor}: unknown/missing patterns {sorted(invalid_patterns)}",
                    )
                used_patterns.update(row_patterns)
                map_by_oq[anchor] = (row, row_patterns)
                if row["bridge_type"] not in {"direct", "mixed", "indirect", "support"}:
                    add("P1", "PATTERN_OQ_MAP_BRIDGE", f"{anchor}: {row['bridge_type']}")
                if row["resolution_event"] not in {
                    *(f"E{number}" for number in range(1, 11)), "PARK", "WATCH", "ROLLUP",
                }:
                    add("P1", "PATTERN_OQ_MAP_EVENT", f"{anchor}: {row['resolution_event']}")
                if row["resolution_kind"] not in {
                    "formalization", "experiment", "literature", "author_decision",
                    "export", "lemma", "watch",
                }:
                    add("P1", "PATTERN_OQ_MAP_KIND", f"{anchor}: {row['resolution_kind']}")

            if atlas_valid and used_patterns != pattern_set:
                add(
                    "P1", "PATTERN_OQ_MAP_PATTERN_COVERAGE",
                    f"Pattern coverage missing={sorted(pattern_set-used_patterns)}, "
                    f"extra={sorted(used_patterns-pattern_set)}",
                )

            direct_by_oq: dict[str, set[str]] = {}
            if atlas_valid:
                for row in atlas_rows:
                    for anchor in re.findall(r"oq-[a-z0-9-]+", row["open_question"]):
                        direct_by_oq.setdefault(anchor, set()).add(row["pattern_id"])
            for anchor, (map_row, mapped_patterns) in map_by_oq.items():
                direct_patterns = direct_by_oq.get(anchor, set())
                bridge_type = map_row["bridge_type"]
                if direct_patterns and bridge_type not in {"direct", "mixed"}:
                    add(
                        "P1", "PATTERN_OQ_MAP_DIRECT_TYPE",
                        f"{anchor}: direct atlas edge must be marked direct or mixed",
                    )
                if direct_patterns and not direct_patterns.issubset(mapped_patterns):
                    add(
                        "P1", "PATTERN_OQ_MAP_DIRECT_EDGE",
                        f"{anchor}: missing direct patterns {sorted(direct_patterns-mapped_patterns)}",
                    )
                if bridge_type == "direct" and mapped_patterns != direct_patterns:
                    add(
                        "P1", "PATTERN_OQ_MAP_DIRECT_EXACT",
                        f"{anchor}: direct row has non-literal patterns {sorted(mapped_patterns-direct_patterns)}",
                    )
                if bridge_type == "mixed" and (
                    not direct_patterns or not (mapped_patterns - direct_patterns)
                ):
                    add(
                        "P1", "PATTERN_OQ_MAP_MIXED",
                        f"{anchor}: mixed row must contain literal and curated patterns",
                    )
                if bridge_type in {"indirect", "support"} and direct_patterns:
                    add(
                        "P1", "PATTERN_OQ_MAP_INDIRECT_EXACT",
                        f"{anchor}: {bridge_type} row contains literal atlas edges",
                    )
            declared_direct = {
                anchor for anchor, (row, _) in map_by_oq.items()
                if row["bridge_type"] in {"direct", "mixed"}
            }
            live_direct = set(direct_by_oq) & set(active_oq)
            if declared_direct != live_direct:
                add(
                    "P1", "PATTERN_OQ_MAP_DIRECT_COVERAGE",
                    f"Declared direct missing={sorted(live_direct-declared_direct)}, "
                    f"extra={sorted(declared_direct-live_direct)}",
                )

    literature_path = HERE / "LITERATURE_MATRIX.tsv"
    literature_fields = {
        "lit_id", "direction", "source", "identifier", "source_claim",
        "fts_mapping", "relation", "audit_verdict",
    }
    if not literature_path.exists():
        add("P1", "LITERATURE_MATRIX_MISSING", "LITERATURE_MATRIX.tsv is missing")
    else:
        with literature_path.open(encoding="utf-8", newline="") as fh:
            literature_rows = list(csv.DictReader(fh, delimiter="\t"))
        if not literature_rows or set(literature_rows[0]) != literature_fields:
            add("P1", "LITERATURE_SCHEMA", f"Expected columns: {sorted(literature_fields)}")
        else:
            literature_ids = [row["lit_id"] for row in literature_rows]
            if len(literature_ids) != len(set(literature_ids)) or len(literature_rows) < 15:
                add("P1", "LITERATURE_COVERAGE", "Literature matrix must contain 15 unique recorded sources")
            for row in literature_rows:
                if any(not row[field].strip() for field in literature_fields):
                    add("P1", "LITERATURE_EMPTY", f"{row['lit_id']}: an audit field is empty")
                if row["relation"] not in {"direct", "limiting", "alternative", "analogy"}:
                    add("P1", "LITERATURE_RELATION", f"{row['lit_id']}: {row['relation']}")

    for required_audit in (
        HERE / "PATTERN_ATLAS.md", HERE / "PATTERN_OQ_MAP.md",
        HERE / "SEARCH_LOG.md", HERE / "AUDIT_REPORT.md", HERE / "REVIEW_CONCLUSION.md",
    ):
        if not required_audit.exists():
            add("P1", "AUDIT_ARTIFACT_MISSING", f"Missing {required_audit.name}")

    paper = PAPER.read_text(encoding="utf-8")
    if "59 машинных проверок" in paper:
        add("P2", "STALE_COUNT", "Current paper still says 59 machine checks")
    for phrase in ("1/4", "p=0.9375", "2/4", "p=0.6875"):
        if phrase not in paper:
            add("P1", "EMPIRICAL_PAPER_STALE", f"Current paper lacks corrected empirical value: {phrase}")
    if "не найдено в пределах" not in paper:
        add("P1", "NOVELTY_BOUNDARY_MISSING", "Current paper lacks the bounded novelty statement")
    export_paper = EXPORT / "FTS_v14_paper.md"
    if export_paper.exists() and export_paper.read_bytes() != PAPER.read_bytes():
        add("P2", "EXPORT_PAPER_DRIFT", "Export paper differs from working paper")
    sync_pairs = [
        (REBUILD / "status_patch_v14.md", EXPORT / "status_patch_v14.md"),
        (REBUILD / "verification_report.md", EXPORT / "verification_report.md"),
        *[
            (HERE / name, EXPORT / "audit" / name)
            for name in (
                "BASELINE.md", "AUDIT_REPORT.md", "REVIEW_CONCLUSION.md", "FINDINGS.tsv",
                "CLAIM_MATRIX.tsv", "PATTERN_ATLAS.md", "PATTERN_ATLAS.tsv",
                "PATTERN_OQ_MAP.md", "PATTERN_OQ_MAP.tsv",
                "LITERATURE_MATRIX.tsv", "SEARCH_LOG.md", "REPRODUCIBILITY.md",
                "GRAPH_AUDIT.md", "CANON_REFERENCE_PATCH.tsv", "GRAPH_RELATION_PATCH.tsv",
                "requirements-audit.txt",
            )
        ],
    ]
    for working, review in sync_pairs:
        if not review.exists() or review.read_bytes() != working.read_bytes():
            add("P2", "EXPORT_AUDIT_DRIFT", f"Review copy differs: {review.relative_to(EXPORT)}")


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
    radio = resolve_radioml_path()
    if not radio.exists():
        add("P1", "RADIOML_INPUT", f"RadioML input is missing; checked: {radioml_search_summary()}")
    elif radio.stat().st_size != RADIOML_EXPECTED_SIZE or sha256(radio) != RADIOML_EXPECTED_SHA256:
        add("P1", "RADIOML_INPUT", f"RadioML input has an unexpected size or hash: {radio}")
    for path in [
        REBUILD / "o20" / "AUDIT_REANALYSIS.md",
        REBUILD / "o20" / "audit_results.json",
        REBUILD / "d2_sign" / "AUDIT_REANALYSIS.md",
        REBUILD / "d2_sign" / "audit_results.json",
        REBUILD / "d10_phase" / "AUDIT_REANALYSIS.md",
        HERE / "REPRODUCIBILITY.md",
    ]:
        if not path.exists():
            add("P1", "REANALYSIS_MISSING", f"Missing {path.relative_to(ROOT)}")

    expected_results = {
        REBUILD / "o20" / "audit_results.json": "ad8803327ffb066bbd39cbe93a39dce796e2e08d63735023086c53dad01a0261",
        REBUILD / "d2_sign" / "audit_results.json": "9e72164612c45ad693b1675c32f6b7a5f912e3fcd5b85409781c1b0fc32e1d70",
    }
    for path, expected_hash in expected_results.items():
        if path.exists() and sha256(path) != expected_hash:
            add("P1", "REANALYSIS_HASH", f"Unexpected reanalysis result hash: {path.relative_to(ROOT)}")

    panel_expected = {
        "o20": {"colic": (25, 1), "hepatitis": (55, 1), "vote": (56, 1), "cylinder-bands": (33, 1)},
        "d2_sign": {"breast_cancer": (None, "1.9.0"), "ionosphere": (59, 1), "sonar": (40, 1), "diabetes": (37, 1)},
    }
    for folder, expected_panel in panel_expected.items():
        path = REBUILD / folder / "audit_results.json"
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("analysis_kind") != "post_hoc_audit_reanalysis_not_preregistered":
            add("P1", "REANALYSIS_LABEL", f"{folder}: missing post-hoc label")
        actual_panel = {item["name"]: (item.get("data_id"), item.get("version")) for item in payload.get("datasets", [])}
        if actual_panel != expected_panel:
            add("P1", "DATASET_IDENTITY", f"{folder}: {actual_panel}")
        if payload.get("cv") != {"splits": 5, "repeats": 4, "folds_per_dataset": 20}:
            add("P1", "CV_PROTOCOL", f"{folder}: unexpected CV protocol")
        for name, models in payload.get("raw_fold_auc", {}).items():
            for model, tiers in models.items():
                if any(len(values) != 20 for values in tiers.values()):
                    add("P1", "FOLD_COUNT", f"{folder}/{name}/{model}: expected 20 values per tier")

    manifest_path = HERE / "reproductions" / "d10" / "run_manifest.json"
    if not manifest_path.exists():
        add("P1", "D10_REPRO_MISSING", "D10 reproduction manifest is missing")
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        variants = manifest.get("variants", [])
        expected_variants = {"synthetic-v1", "synthetic-pilot", "radioml-v1", "radioml-v2", "radioml-v3"}
        if {row.get("variant") for row in variants} != expected_variants:
            add("P1", "D10_VARIANTS", "Not all five D10 variants were reproduced")
        for row in variants:
            if not row.get("semantic_json_equal") or not row.get("byte_equal"):
                add("P1", "D10_REPRO_DRIFT", f"D10 drift: {row.get('variant')}")
        radio_manifest = manifest.get("radioml", {})
        if (
            radio_manifest.get("sha256") != RADIOML_EXPECTED_SHA256
            or radio_manifest.get("size_bytes") != RADIOML_EXPECTED_SIZE
        ):
            add("P1", "D10_INPUT_DRIFT", "D10 manifest has unexpected RadioML identity")

    historical = [
        REBUILD / "o20" / "PREREGISTRATION.md", REBUILD / "o20" / "results.json", REBUILD / "o20" / "RESULTS.md",
        REBUILD / "d2_sign" / "PREREGISTRATION.md", REBUILD / "d2_sign" / "results.json", REBUILD / "d2_sign" / "RESULTS.md",
        REBUILD / "d10_phase" / "PREREGISTRATION.md", REBUILD / "d10_phase" / "results.json", REBUILD / "d10_phase" / "RESULTS.md",
        REBUILD / "d10_phase" / "pilot" / "PREREGISTRATION.md", REBUILD / "d10_phase" / "pilot" / "results.json",
        REBUILD / "d10_phase" / "radioml" / "PREREGISTRATION.md", REBUILD / "d10_phase" / "radioml" / "results.json",
        REBUILD / "d10_phase" / "radioml" / "PREREGISTRATION_v2.md", REBUILD / "d10_phase" / "radioml" / "results_v2.json",
        REBUILD / "d10_phase" / "radioml" / "PREREGISTRATION_v3.md", REBUILD / "d10_phase" / "radioml" / "results_v3.json",
    ]
    historical_rel = [str(path.relative_to(ROOT)) for path in historical]
    diff = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", *historical_rel], cwd=ROOT, check=False)
    if diff.returncode != 0:
        add("P1", "HISTORICAL_MUTATED", "A historical preregistration/result differs from HEAD")


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
