"""Build, validate and query the FTS claim/evidence graph.

The graph in work/v14_rebuild/claim_graph/ is the authoritative directed
relation multiset for the second FTS structural layer. graphify-out/ remains a
view/navigation product. This tool is stdlib-only and deliberately keeps
canonical v13, author canon, audit, internal evidence and external research in
separate layers.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

try:
    from .reference_resolution import REGISTRY, fragment_witness, load_resolutions, validate_resolutions
except ImportError:
    from reference_resolution import REGISTRY, fragment_witness, load_resolutions, validate_resolutions


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "work" / "v14_rebuild" / "claim_graph"
GRAPH_PATH = OUT_DIR / "claim_graph.json"
COVERAGE_PATH = OUT_DIR / "COVERAGE.md"
CHANGE_REPORT_PATH = OUT_DIR / "CHANGE_REPORT.md"
SCHEMA_PATH = OUT_DIR / "SCHEMA.md"
HTML_PATH = OUT_DIR / "claim_graph.html"
PROJECT_ENTITY = ROOT / "PROJECT.json"

CANON_CARDS = ROOT / "source" / "fts_cards.jsonl"
CANON_TRIPLES = ROOT / "source" / "fts_triples.tsv"
AUTHOR_DIR = ROOT / "work" / "author_canon" / "2026-09-21"
AUTHOR_CARDS = AUTHOR_DIR / "cards.jsonl"
AUTHOR_TRIPLES = AUTHOR_DIR / "triples.tsv"
AUTHOR_PACKAGES = (AUTHOR_DIR, ROOT / "work" / "author_canon" / "2026-10-03")
AUDIT_DIR = ROOT / "work" / "v14_rebuild" / "audit"
CLAIMS = AUDIT_DIR / "CLAIM_MATRIX.tsv"
FINDINGS = AUDIT_DIR / "FINDINGS.tsv"
ATLAS = AUDIT_DIR / "PATTERN_ATLAS.tsv"
OQ_MAP = AUDIT_DIR / "PATTERN_OQ_MAP.tsv"
OPEN_QUESTIONS = ROOT / "work" / "OPEN_QUESTIONS.md"
VERIFICATION = ROOT / "work" / "v14_rebuild" / "verification.py"
RESEARCH_DIR = ROOT / "work" / "v14_rebuild" / "neural_skeleton_research_2026-09-15"
RESEARCH_CLAIMS = OUT_DIR / "RESEARCH_CLAIMS.tsv"
RESEARCH_BRIDGES = OUT_DIR / "RESEARCH_CLAIM_BRIDGES.tsv"
RESEARCH_EVIDENCE = OUT_DIR / "RESEARCH_EVIDENCE.tsv"
RELATION_REVIEWS = AUDIT_DIR / 'GRAPH_RELATION_PATCH.tsv'
CYCLE_REVIEWS = AUDIT_DIR / 'DEPENDENCY_CYCLE_REVIEW.tsv'

NEURAL_EVIDENCE = RESEARCH_DIR / "EVIDENCE_MATRIX.tsv"
SUM_EVIDENCE = RESEARCH_DIR / "SUM_DISTINCTION_EVIDENCE.tsv"
E5_EVIDENCE = ROOT / "work" / "v14_rebuild" / "e5_literature_review" / "EVIDENCE_MATRIX.tsv"
INTERNAL_EVIDENCE = RESEARCH_DIR / "INTERNAL_EVIDENCE.md"
RESEARCH_DOCS = [
    RESEARCH_DIR / "CONSIDERATION_BRIEF.md",
    RESEARCH_DIR / "DEEP_RESEARCH_REPORT_10_INTEGRATION.md",
    RESEARCH_DIR / "EXTENDED_AUDIT.md",
    RESEARCH_DIR / "GATE_CONTROL_RESULTS.md",
    RESEARCH_DIR / "TARGET_INDEPENDENT_AUDIT.md",
    INTERNAL_EVIDENCE,
]

ANCHOR_RE = re.compile(r"\{#(?P<anchor>oq-[a-z0-9-]+)\}")
CM_RE = re.compile(r"\bCM-\d{3}\b")
C_RE = re.compile(r"\bC\d{1,2}(?:\s*[-–]\s*C\d{1,2})?\b")
CHECK_RE = re.compile(r"check\(\s*[\"'](C\d{1,2})[\"']")

RELATION_RULES: dict[str, tuple[set[str], set[str]]] = {
    "has_research_scope": ({"project"}, {"scope"}),
    "addresses_object": ({"scope"}, {"card"}),
    "proposes_formalization_of": ({"card"}, {"card"}),
    "has_status": ({"card", "author_statement", "claim", "claim_group", "finding"}, {"status_assessment"}),
    "has_status_before": ({"claim", "claim_group"}, {"status_assessment"}),
    "has_status_after": ({"claim", "claim_group"}, {"status_assessment"}),
    "grounds_claim": ({"claim", "claim_group", "pattern", "author_statement"}, {"card", "source_document", "source_fragment", "scope", "source_reference", "author_statement"}),
    "documented_in": ({"project", "card", "claim", "claim_group", "author_statement", "external_evidence", "internal_evidence", "finding", "status_assessment", "verification"}, {"source_document"}),
    "verified_by": ({"claim", "claim_group", "pattern"}, {"verification", "external_evidence", "internal_evidence"}),
    "supported_by": ({"claim", "claim_group"}, {"external_evidence", "internal_evidence", "verification", "source_document"}),
    "limited_by": ({"claim", "claim_group"}, {"finding", "external_evidence", "internal_evidence", "source_reference", "source_document"}),
    "refined_by": ({"claim", "claim_group"}, {"source_document", "external_evidence", "internal_evidence"}),
    "audits_claim": ({"finding"}, {"claim", "claim_group"}),
    "contains": ({"source_document", "card", "author_statement", "scope"}, {"card", "author_statement", "claim", "claim_group", "finding", "pattern", "open_question", "verification", "external_evidence", "internal_evidence", "status_assessment", "source_reference", "source_fragment", "scope", "literal", "unresolved_reference"}),
    "opens_question": ({"pattern", "claim", "claim_group"}, {"open_question"}),
    "directly_traced_to": ({"pattern"}, {"open_question"}),
    "curated_bridge_to": ({"pattern"}, {"open_question"}),
    "navigation_support_for": ({"pattern"}, {"open_question"}),
    "belongs_to_program": ({"open_question"}, {"program"}),
    "planned_resolution_event": ({"open_question"}, {"event"}),
    "belongs_to_meta_pattern": ({"pattern"}, {"meta_pattern"}),
    "grouped_by_meta_pattern": ({"open_question"}, {"meta_pattern"}),
    "has_open_obligation": ({"author_statement", "claim"}, {"open_obligation"}),
    "has_local_forbid": ({"author_statement"}, {"constraint"}),
    "maps_to": ({"external_evidence", "internal_evidence"}, {"card", "claim", "claim_group"}),
    "supports_claim": ({"external_evidence", "internal_evidence", "verification"}, {"claim", "claim_group"}),
    "limits_claim": ({"external_evidence", "internal_evidence", "finding"}, {"claim", "claim_group"}),
    "depends_on": ({"card", "author_statement"}, {"card", "author_statement", "source_fragment", "literal", "unresolved_reference"}),
    "applies_to": ({"card", "author_statement"}, {"card", "author_statement"}),
    "uses_analogy": ({"card", "author_statement"}, {"card", "author_statement"}),
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slug(value: str) -> str:
    out = re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_").lower()
    return out or "empty"


def short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def compact(value: object, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if line.strip():
                item = json.loads(line)
                item["_line"] = line_no
                rows.append(item)
    return rows


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]


def find_line(path: Path, needle: str) -> str:
    if not path.is_file():
        return ""
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle and needle in line:
            return f"L{line_no}"
    return ""


def expand_checks(value: str) -> list[str]:
    result: list[str] = []
    for token in C_RE.findall(value or ""):
        token = token.replace("–", "-").replace(" ", "")
        if "-" not in token:
            result.append(token)
            continue
        left, right = token.split("-", 1)
        a, b = int(left[1:]), int(right[1:])
        result.extend(f"C{i:02d}" for i in range(a, b + 1))
    return sorted(set(result), key=lambda item: int(item[1:]))


def status_from_checkbox(line: str) -> str:
    if "- [ ]" in line:
        return "open"
    if "- [~]" in line:
        return "partial"
    if "- [x]" in line.lower():
        return "closed"
    return "unknown"


def read_oq_anchors() -> dict[str, dict[str, str]]:
    anchors: dict[str, dict[str, str]] = {}
    for line_no, raw in enumerate(OPEN_QUESTIONS.read_text(encoding="utf-8").splitlines(), 1):
        for match in ANCHOR_RE.finditer(raw):
            key = match.group("anchor")
            text = ANCHOR_RE.sub("", raw)
            text = re.sub(r"^\s*-\s*\[[ xX~]\]\s*", "", text).strip()
            anchors[key] = {"status": status_from_checkbox(raw), "text": text, "line": f"L{line_no}"}
    return anchors


def verification_locations() -> dict[str, str]:
    out: dict[str, str] = {}
    for line_no, raw in enumerate(VERIFICATION.read_text(encoding="utf-8").splitlines(), 1):
        for check_id in CHECK_RE.findall(raw):
            out.setdefault(check_id, f"L{line_no}")
    return out


class GraphBuilder:
    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: list[dict[str, Any]] = []
        self.edge_ids: set[str] = set()
        self.inputs: set[Path] = set()
        self.aliases: dict[str, str] = {}
        self.counts: Counter[str] = Counter()
        self.resolutions = load_resolutions()
        self.resolved_references: dict[str, str] = {}
        self.input(REGISTRY)

    def input(self, path: Path) -> None:
        if path.is_file():
            self.inputs.add(path)

    def node(self, node_id: str, node_type: str, label: str, layer: str, **attrs: Any) -> str:
        payload: dict[str, Any] = {
            "id": node_id,
            "type": node_type,
            "label": label,
            "layer": layer,
        }
        payload.update({key: value for key, value in attrs.items() if value is not None})
        prior = self.nodes.get(node_id)
        if prior is not None:
            if prior["type"] != node_type or prior["label"] != label:
                raise ValueError(f"node collision: {node_id}")
            for key, value in payload.items():
                if key not in prior:
                    prior[key] = value
        else:
            self.nodes[node_id] = payload
        return node_id

    def edge(
        self,
        edge_id: str,
        source: str,
        target: str,
        relation: str,
        layer: str,
        confidence: str,
        source_file: Path | str,
        source_location: str = "",
        **attrs: Any,
    ) -> None:
        if edge_id in self.edge_ids:
            raise ValueError(f"duplicate edge id: {edge_id}")
        if isinstance(source_file, Path):
            self.input(source_file)
            source_name = rel(source_file)
        else:
            source_name = source_file
        payload: dict[str, Any] = {
            "id": edge_id,
            "source": source,
            "target": target,
            "relation": relation,
            "layer": layer,
            "confidence": confidence,
            "source_file": source_name,
            "source_location": source_location,
        }
        payload.update({key: value for key, value in attrs.items() if value is not None and value != ""})
        self.edges.append(payload)
        self.edge_ids.add(edge_id)
        self.counts[relation] += 1

    def document(self, path: Path, label: str | None = None, layer: str = "research") -> str:
        self.input(path)
        node_id = f"doc_{slug(rel(path))}"
        return self.node(node_id, "source_document", label or rel(path), layer, source_file=rel(path))

    def source_reference(self, raw: str, source_file: Path, row: int) -> str:
        resolved = self.resolve_reference(raw, source_file, row, "research", as_source=True)
        if resolved is not None:
            return resolved
        node_id = f"source_ref_{short_hash(raw)}"
        return self.node(
            node_id,
            "source_reference",
            raw,
            "research",
            raw_reference=raw,
            resolution_state="unresolved_reference",
            missing_reason="нет в артефактах",
            source_file=rel(source_file),
            source_location=f"row:{row}",
        )

    def resolve_reference(self, raw: str, origin: Path, row: int, layer: str, *, as_source: bool = False) -> str | None:
        resolution = self.resolutions.get(raw)
        if resolution is None:
            return None
        if raw in self.resolved_references:
            return self.resolved_references[raw]
        kind = resolution['resolution']
        attrs = {
            'raw_reference': raw,
            'reference_resolution': kind,
            'resolution_evidence': resolution['evidence'],
            'resolution_registry': rel(REGISTRY),
            'scope': resolution['scope'],
            'status_effect': resolution['status_effect'],
        }
        if kind == 'card_alias':
            target = self.aliases.get(resolution['target'])
            if target is None:
                raise ValueError(f'Missing alias target: {raw} -> {resolution["target"]}')
        elif kind in {'sheet_record', 'document_fragment'}:
            location, witness = fragment_witness(ROOT, resolution)
            target = self.node(
                f'ref_resolved_{short_hash(raw)}', 'source_fragment', raw, layer,
                **attrs, resolution_state='resolved_fragment',
                source_file=resolution['target'], source_location=location,
                fragment_record=witness,
            )
            document = self.document(ROOT / resolution['target'], layer=layer)
            self.edge(f'resolution_contains_{short_hash(raw)}', document, target, 'contains',
                      'reference_registry', 'CURATED', REGISTRY, f'reference:{raw}',
                      scope=resolution['scope'], status_effect=resolution['status_effect'])
        elif kind == 'scope':
            members = json.loads(resolution['target'])
            target = self.node(f'ref_scope_{short_hash(raw)}', 'scope', raw, layer,
                               **attrs, resolution_state='resolved_scope', members=members,
                               source_file=rel(origin), source_location=f'row:{row}')
            for member in members:
                member_id = self.aliases.get(member)
                if member_id is None:
                    raise ValueError(f'Missing scope member: {raw} -> {member}')
                self.edge(f'scope_member_{short_hash(raw)}_{slug(member)}', target, member_id,
                          'contains', 'reference_registry', 'CURATED', REGISTRY,
                          f'reference:{raw}:member:{member}', scope=resolution['scope'],
                          status_effect='membership only; no independent support claim')
        elif kind == 'document_set':
            members = json.loads(resolution['target'])
            target = self.node(f'ref_documents_{short_hash(raw)}', 'source_document', raw, layer,
                               **attrs, resolution_state='resolved_document_set', members=members,
                               source_file=rel(REGISTRY), source_location=f'reference:{raw}')
            for member in members:
                document = self.document(ROOT / member, layer=layer)
                self.edge(f'document_member_{short_hash(raw)}_{short_hash(member)}', target, document,
                          'contains', 'reference_registry', 'CURATED', REGISTRY,
                          f'reference:{raw}:member:{member}', scope=resolution['scope'],
                          status_effect='source collection only; no independent support claim')
        elif kind == 'literal':
            target = self.node(f'literal_{short_hash(raw)}', 'literal', raw, layer, **attrs,
                               raw_value=raw, resolution_state='literal',
                               literal_kind=resolution['target'], source_file=rel(origin),
                               source_location=f'row:{row}')
        else:
            prefix = 'source_ref' if as_source else 'ref_unresolved'
            target = self.node(f'{prefix}_{short_hash(raw)}',
                               'source_reference' if as_source else 'unresolved_reference',
                               raw, layer, **attrs, resolution_state='unresolved_reference',
                               missing_reason='нет в артефактах', candidates=resolution['target'],
                               next_step=resolution['next_step'], source_file=rel(origin),
                               source_location=f'row:{row}')
        self.resolved_references[raw] = target
        return target

    def output(self) -> dict[str, Any]:
        inputs = [
            {"path": rel(path), "sha256": sha256(path)}
            for path in sorted(self.inputs, key=lambda item: rel(item))
        ]
        return {
            "schema": "fts_claim_graph/v1",
            "generator": "tools/claim_graph.py",
            "trust_boundary": {
                "project_definition": "user-defined research objective and scope; no evidence or status promotion",
                "canonical_v13": "active editable canon; versioned source-backed assertions",
                "author_canon": "accepted author supplement; separate versioned layer",
                "research": "curated claims and bridges with explicit scope",
                "external_evidence": "bibliographic or experimental evidence; no automatic St_FTS promotion",
                "graphify": "view/navigation only; this file preserves directed parallel edges",
            },
            "input_digests": inputs,
            "nodes": [self.nodes[key] for key in sorted(self.nodes)],
            "edges": sorted(self.edges, key=lambda item: item["id"]),
            "coverage": dict(self.counts),
        }


def canonical_card_id_map(cards: list[dict[str, Any]], prefix: str) -> dict[str, str]:
    return {str(card["id"]): f"{prefix}_{slug(str(card['id']))}" for card in cards}


def add_project_entity(builder: GraphBuilder, card_ids: dict[str, str]) -> None:
    """Record the research objective without assigning evidence or claim status."""
    data = json.loads(PROJECT_ENTITY.read_text(encoding="utf-8"))
    required = {"grounds", "ladder", "level", "interlevel"}
    categories = data.get("scope_categories", [])
    category_ids = [item.get("id") for item in categories]
    if data.get("schema") != "fts_project/v1" or data.get("project_id") != "FTS":
        raise ValueError("Invalid FTS project entity schema or ID")
    if set(category_ids) != required or len(category_ids) != len(required):
        raise ValueError("Project must declare all four distinct research scopes")
    if not data.get("objective") or not data.get("assertion_requirements"):
        raise ValueError("Project objective or assertion requirements missing")
    requirements = data["assertion_requirements"]
    if {item.get("id") for item in requirements} != {f"R{i}" for i in range(1, 7)} or len(requirements) != 6:
        raise ValueError("Project assertion requirements R1-R6 missing or duplicated")
    if any(not item.get("requirement") for item in requirements):
        raise ValueError("Empty project assertion requirement")
    description = ROOT / data["description_file"]
    if not description.resolve().is_relative_to(ROOT.resolve()) or not description.is_file():
        raise ValueError("Project description missing")
    builder.input(PROJECT_ENTITY)
    project = builder.node(
        "project_fts", "project", data["name"], "project_definition",
        project_id=data["project_id"], objective=data["objective"],
        complexity_meaning=data["complexity_meaning"], acceptance=data["acceptance"],
        assertion_requirements=data["assertion_requirements"],
        status_policy=data["status_policy"], provenance=data["provenance"],
        recorded_on=data["recorded_on"], source_file=rel(PROJECT_ENTITY),
        source_location="project_id:FTS", status_effect="research objective only; no status promotion",
    )
    for category in categories:
        anchors = category.get("anchor_card_ids", [])
        if not anchors or len(anchors) != len(set(anchors)) or set(anchors) - set(card_ids):
            raise ValueError(f"Invalid project anchors: {category['id']}")
        scope = builder.node(
            f"research_scope_{category['id']}", "scope", category["name"], "project_definition",
            scope_kind=category["id"], question=category["question"], members=anchors,
            source_file=rel(PROJECT_ENTITY), source_location=f"scope_categories:{category['id']}",
            status_effect="research address only; not evidence of connectivity",
        )
        builder.edge(
            f"project_scope_{category['id']}", project, scope, "has_research_scope",
            "project_definition", "EXTRACTED", PROJECT_ENTITY, f"scope_categories:{category['id']}",
            status_effect="declared objective; no automatic claim assignment",
        )
        for card_id in anchors:
            builder.edge(
                f"project_anchor_{category['id']}_{slug(card_id)}", scope, card_ids[card_id],
                "addresses_object", "project_definition", "EXTRACTED", PROJECT_ENTITY,
                f"scope_categories:{category['id']}:anchor:{card_id}",
                status_effect="declared research object; not a proof or prerequisite",
            )
    doc = builder.document(description, layer="project_definition")
    builder.edge("project_description", project, doc, "documented_in", "project_definition",
                 "EXTRACTED", PROJECT_ENTITY, "description_file",
                 status_effect="project description provenance only")


def build_graph() -> dict[str, Any]:
    for path in [CANON_CARDS, CANON_TRIPLES, CLAIMS, FINDINGS, ATLAS, OQ_MAP, OPEN_QUESTIONS, VERIFICATION, RESEARCH_CLAIMS, RESEARCH_EVIDENCE, RESEARCH_BRIDGES, *[directory / name for directory in AUTHOR_PACKAGES for name in ("cards.jsonl", "triples.tsv")]]:
        if not path.is_file():
            raise FileNotFoundError(f"нет в артефактах: {rel(path)}")

    canon_cards = read_jsonl(CANON_CARDS)
    author_packets = [(directory / "cards.jsonl", read_jsonl(directory / "cards.jsonl")) for directory in AUTHOR_PACKAGES]
    author_cards = [card for _path, packet in author_packets for card in packet]
    author_paths = {str(card["id"]): path for path, packet in author_packets for card in packet}
    if len(author_paths) != len(author_cards):
        raise ValueError("Duplicate author IDs across active author packages")
    canon_by_id = {str(card["id"]): card for card in canon_cards}
    author_by_id = {str(card["id"]): card for card in author_cards}
    card_ids = canonical_card_id_map(canon_cards, "card")
    author_ids = canonical_card_id_map(author_cards, "author")
    builder = GraphBuilder()
    builder.aliases.update(author_ids)
    builder.aliases.update(card_ids)
    validate_resolutions(ROOT, builder.resolutions, set(canon_by_id))
    reviews = {}
    for review_file in (RELATION_REVIEWS, CYCLE_REVIEWS):
        builder.input(review_file)
        for review_number, review in enumerate(read_tsv(review_file), 2):
            reviews[(review['final_subject'], review['final_predicate'], review['final_object'])] = {
                'scope': review['scope'], 'status_effect': review['status_effect'],
                'relationship_review_file': rel(review_file),
                'relationship_review_location': f'row:{review_number}',
                'review_confidence': 'CURATED',
            }

    def review_attrs(subject: str, predicate: str, obj: str, layer: str) -> dict:
        return reviews.get((subject, predicate, obj), {}) if layer == 'canonical_v13' else {}
    # OQ nodes and their statuses are extracted below; retain the file digest so
    # validation catches a stale graph after an OQ edit.
    builder.input(OPEN_QUESTIONS)
    builder.input(CANON_CARDS)
    builder.input(CANON_TRIPLES)
    for directory in AUTHOR_PACKAGES:
        builder.input(directory / "cards.jsonl")
        builder.input(directory / "triples.tsv")

    def ref_node(raw: str, layer: str, source_path: Path, row: int) -> str:
        raw = str(raw).strip()
        if layer == "author_canon" and raw in author_ids:
            return author_ids[raw]
        if raw in card_ids:
            return card_ids[raw]
        if raw in author_ids:
            return author_ids[raw]
        resolved = builder.resolve_reference(raw, source_path, row, layer)
        if resolved is not None:
            return resolved
        literal = raw.startswith("(") or raw.startswith("{") or raw.endswith(".md") or raw.startswith("scope:")
        if literal:
            return builder.node(
                f"literal_{short_hash(raw)}",
                "literal",
                raw,
                layer,
                raw_value=raw,
                resolution_state="literal",
                source_file=rel(source_path),
                source_location=f"row:{row}",
            )
        return builder.node(
            f"ref_unresolved_{short_hash(raw)}",
            "unresolved_reference",
            raw,
            layer,
            raw_reference=raw,
            resolution_state="unresolved_reference",
            missing_reason="нет в артефактах",
            source_file=rel(source_path),
            source_location=f"row:{row}",
        )

    def card_node(card: dict[str, Any], card_id: str, layer: str, node_type: str) -> str:
        node_id = card_id
        card_path = author_paths[str(card["id"])] if layer == "author_canon" else CANON_CARDS
        status_key = slug(str(card["id"]))
        if str(card["id"]) in card_ids and str(card["id"]) in author_ids:
            status_key = slug(layer) + "_" + status_key
        adoption = {key: card[key] for key in
                    ("formulation_origin", "author_status", "adoption_scope", "adoption_source")
                    if key in card} if card.get("adoption_source") else {}
        if card.get("adoption_source"):
            adoption["card_type"] = card["type"]
        builder.node(
            node_id,
            node_type,
            f"{card.get('symbol', '')} {card.get('title', card.get('id', ''))}".strip(),
            layer,
            card_id=card.get("id"),
            status=card.get("status"),
            tags=card.get("tags", []),
            text=card.get("text", ""),
            source_file=rel(card_path),
            source_location=f"card:{card.get('id')}",
            **adoption,
        )
        if card.get("adoption_source"):
            clarification = ROOT / card["adoption_source"]
            if not clarification.resolve().is_relative_to(ROOT.resolve()) or not clarification.is_file():
                raise ValueError(f"Missing author adoption source: {card['id']}")
            document = builder.document(clarification, layer="author_clarification")
            builder.edge(f"card_adoption_{slug(str(card['id']))}", node_id, document,
                         "documented_in", "author_clarification", "EXTRACTED", card_path,
                         f"card:{card['id']}:adoption_source",
                         scope=card["adoption_scope"],
                         status_effect="author provenance/adoption clarification; no evidence promotion")
        status_value = card.get("status") or card.get("author_status") or "unknown"
        if layer == "author_canon":
            status_value = card.get("author_status") or card.get("status") or "unknown"
            status_value = f"{status_value}; evidence_status={card.get('evidence_status', 'unknown')}"
        assessment_id = f"assessment_{status_key}_status"
        builder.node(
            assessment_id,
            "status_assessment",
            f"{card['id']} status: {status_value}",
            layer,
            status_text=status_value,
            status_axis="author_status" if layer == "author_canon" else "St_FTS",
            status_effect="stored_only; no automatic promotion",
            source_file=rel(card_path),
            source_location=f"card:{card['id']}",
        )
        builder.edge(
            f"status_{status_key}",
            node_id,
            assessment_id,
            "has_status",
            layer,
            "EXTRACTED",
            card_path,
            f"card:{card['id']}",
            status_effect="stored_only; no automatic promotion",
        )
        return node_id

    for card in canon_cards:
        card_node(card, card_ids[str(card["id"])], "canonical_v13", "card")
    for card in author_cards:
        card_node(card, author_ids[str(card["id"])], "author_canon", "author_statement")

    def add_card_dependencies(cards: list[dict[str, Any]], layer: str, source_path: Path, ids: dict[str, str]) -> None:
        for card in cards:
            source_id = ids[str(card["id"])]
            for index, dependency in enumerate(card.get("depends_on") or []):
                target_id = ref_node(str(dependency), layer, source_path, int(card.get("_line", 0) or 0))
                builder.edge(
                    f"{slug(layer)}_dependency_{slug(str(card['id']))}_{index:03d}",
                    source_id,
                    target_id,
                    "depends_on",
                    layer,
                    "EXTRACTED",
                    source_path,
                    f"card:{card['id']}:depends_on[{index}]",
                    assertion_kind="card_field",
                    **review_attrs(str(card['id']), 'depends_on', str(dependency), layer),
                )

    def add_triples(path: Path, layer: str) -> None:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row_no, row in enumerate(reader, 2):
                source_id = ref_node(row.get("subject", ""), layer, path, row_no)
                target_id = ref_node(row.get("object", ""), layer, path, row_no)
                attributes = review_attrs(row['subject'], row['predicate'], row['object'], layer)
                if layer == "canonical_v13":
                    record = next((card for card in canon_cards if card['id'] == row['subject']), {})
                    if record.get("adoption_source"):
                        attributes.update(scope=record["adoption_scope"],
                                          clarification_source=record["adoption_source"],
                                          status_effect="proposal/explanatory address only; no evidence or status promotion")
                builder.edge(
                    f"{slug(layer)}{'_' + slug(path.parent.name) if layer == 'author_canon' and path != AUTHOR_TRIPLES else ''}_triple_{row_no - 1:04d}",
                    source_id,
                    target_id,
                    row.get("predicate", ""),
                    layer,
                    "EXTRACTED",
                    path,
                    f"row:{row_no}",
                    assertion_kind="triple",
                    raw_subject=row.get("subject", ""),
                    raw_object=row.get("object", ""),
                    **attributes,
                )

    add_card_dependencies(canon_cards, "canonical_v13", CANON_CARDS, card_ids)
    add_triples(CANON_TRIPLES, "canonical_v13")
    for author_path, packet in author_packets:
        add_card_dependencies(packet, "author_canon", author_path, author_ids)
        add_triples(author_path.parent / "triples.tsv", "author_canon")

    for card in author_cards:
        source_id = author_ids[str(card["id"])]
        author_path = author_paths[str(card["id"])]
        for field in ("source", "clarification_source"):
            raw = str(card.get(field, "")).strip()
            if not raw:
                continue
            path = author_path.parent / raw
            if path.is_file():
                target = builder.document(path, layer="author_canon")
                builder.edge(
                    f"author_source_{slug(str(card['id']))}_{slug(field)}",
                    source_id,
                    target,
                    "documented_in",
                    "author_canon",
                    "EXTRACTED",
                    author_path,
                    f"card:{card['id']}:{field}",
                )
            else:
                target = builder.source_reference(raw, author_path, int(card.get("_line", 0) or 0))
                builder.edge(
                    f"author_source_ref_{slug(str(card['id']))}_{slug(field)}",
                    source_id,
                    target,
                    "grounds_claim",
                    "author_canon",
                    "EXTRACTED",
                    author_path,
                    f"card:{card['id']}:{field}",
                )
        for index, text in enumerate(card.get("open_obligations") or []):
            obligation = builder.node(
                f"obligation_{slug(str(card['id']))}_{index:02d}",
                "open_obligation",
                compact(text),
                "author_canon",
                source_file=rel(author_path),
                source_location=f"card:{card['id']}:open_obligations[{index}]",
            )
            builder.edge(
                f"obligation_{slug(str(card['id']))}_{index:02d}_edge",
                source_id,
                obligation,
                "has_open_obligation",
                "author_canon",
                "EXTRACTED",
                author_path,
                f"card:{card['id']}:open_obligations[{index}]",
            )
        for index, text in enumerate(card.get("local_forbid") or []):
            constraint = builder.node(
                f"constraint_{slug(str(card['id']))}_{index:02d}",
                "constraint",
                compact(text),
                "author_canon",
                source_file=rel(author_path),
                source_location=f"card:{card['id']}:local_forbid[{index}]",
            )
            builder.edge(
                f"constraint_{slug(str(card['id']))}_{index:02d}_edge",
                source_id,
                constraint,
                "has_local_forbid",
                "author_canon",
                "EXTRACTED",
                author_path,
                f"card:{card['id']}:local_forbid[{index}]",
            )

    claim_doc = builder.document(CLAIMS, label="CLAIM_MATRIX — адресуемые группы утверждений", layer="audit")
    claims = read_tsv(CLAIMS)
    claim_ids = {row["claim_id"]: f"claim_group_{slug(row['claim_id'])}" for row in claims}
    verification_loc = verification_locations()
    for row_no, row in enumerate(claims, 2):
        claim_id = row["claim_id"]
        node_id = builder.node(
            claim_ids[claim_id],
            "claim_group",
            f"{claim_id} — {compact(row['claim'])}",
            "audit",
            claim_id=claim_id,
            granularity="group",
            domain=row["domain"],
            verification=row["verification"],
            status_before=row["status_before"],
            status_after=row["status_after"],
            verdict=row["verdict"],
            resolution=row["resolution"],
            source_file=rel(CLAIMS),
            source_location=f"row:{row_no}",
        )
        builder.edge(f"claim_matrix_contains_{slug(claim_id)}", claim_doc, node_id, "contains", "audit", "EXTRACTED", CLAIMS, f"row:{row_no}")
        for index, raw_source in enumerate([part.strip() for part in row["source"].split(";") if part.strip()]):
            target = card_ids.get(raw_source) or author_ids.get(raw_source)
            if target is None:
                normalized = raw_source.replace("\\", "/")
                candidate = ROOT / normalized
                if candidate.is_file():
                    target = builder.document(candidate, layer="audit")
                elif "paper" in raw_source.lower() or "FTS_v14_paper" in raw_source:
                    target = builder.document(ROOT / "work" / "v14_rebuild" / "FTS_v14_paper.md", layer="research")
                else:
                    target = builder.source_reference(raw_source, CLAIMS, row_no)
            builder.edge(
                f"claim_ground_{slug(claim_id)}_{index:02d}",
                node_id,
                target,
                "grounds_claim",
                "audit",
                "EXTRACTED",
                CLAIMS,
                f"row:{row_no}:source[{index}]",
                raw_reference=raw_source,
                status_effect="source registry; not automatic truth",
            )
        for check_id in expand_checks(row["verification"]):
            verification_id = f"verification_{check_id.lower()}"
            builder.node(
                verification_id,
                "verification",
                check_id,
                "audit",
                verification_id=check_id,
                evidence_kind="formal_machine_check",
                source_file=rel(VERIFICATION),
                source_location=verification_loc.get(check_id, f"check:{check_id}"),
                status_effect="math predicate only; no automatic St_FTS promotion",
            )
            builder.edge(
                f"claim_verified_{slug(claim_id)}_{check_id.lower()}",
                node_id,
                verification_id,
                "verified_by",
                "audit",
                "EXTRACTED",
                CLAIMS,
                f"row:{row_no}:verification",
                scope="verification field in CLAIM_MATRIX",
                status_effect="math predicate only; no automatic St_FTS promotion",
            )
        for suffix, relation, status_value in (("before", "has_status_before", row["status_before"]), ("after", "has_status_after", row["status_after"])):
            assessment_id = f"assessment_{slug(claim_id)}_{suffix}"
            builder.node(
                assessment_id,
                "status_assessment",
                f"{claim_id} {suffix}: {compact(status_value)}",
                "audit",
                status_text=status_value,
                status_axis="status_before" if suffix == "before" else "status_after",
                status_effect="audit registry; no automatic promotion",
                source_file=rel(CLAIMS),
                source_location=f"row:{row_no}",
            )
            builder.edge(
                f"claim_{slug(claim_id)}_{suffix}_status",
                node_id,
                assessment_id,
                relation,
                "audit",
                "EXTRACTED",
                CLAIMS,
                f"row:{row_no}:status_{suffix}",
                status_effect="audit registry; no automatic promotion",
            )

    findings_doc = builder.document(FINDINGS, label="FINDINGS — аудиторские ограничения", layer="audit")
    findings = read_tsv(FINDINGS)
    finding_ids: dict[str, str] = {}
    for row_no, row in enumerate(findings, 2):
        finding_id = row["finding_id"]
        node_id = f"finding_{slug(finding_id)}"
        finding_ids[finding_id] = node_id
        builder.node(
            node_id,
            "finding",
            f"{finding_id} [{row['severity']}, {row['status']}] — {compact(row['found'])}",
            "audit",
            finding_id=finding_id,
            severity=row["severity"],
            finding_status=row["status"],
            area=row["area"],
            conclusion=row["conclusion"],
            unresolved=row["unresolved"],
            source_file=rel(FINDINGS),
            source_location=f"row:{row_no}",
        )
        builder.edge(f"findings_contains_{slug(finding_id)}", findings_doc, node_id, "contains", "audit", "EXTRACTED", FINDINGS, f"row:{row_no}")
        for claim_ref in sorted(set(CM_RE.findall(" ".join(row.values())))):
            target = claim_ids.get(claim_ref)
            if target is None:
                continue
            builder.edge(f"finding_{slug(finding_id)}_audits_{slug(claim_ref)}", node_id, target, "audits_claim", "audit", "EXTRACTED", FINDINGS, f"row:{row_no}")
            builder.edge(f"claim_{slug(claim_ref)}_limited_by_{slug(finding_id)}", target, node_id, "limited_by", "audit", "EXTRACTED", FINDINGS, f"row:{row_no}", status_effect=row["conclusion"])

    atlas_doc = builder.document(ATLAS, label="PATTERN_ATLAS — проверенные паттерны", layer="audit")
    atlas = read_tsv(ATLAS)
    pattern_ids: dict[str, str] = {}
    for row_no, row in enumerate(atlas, 2):
        pattern_id = row["pattern_id"]
        node_id = f"pattern_{slug(pattern_id)}"
        pattern_ids[pattern_id] = node_id
        builder.node(
            node_id,
            "pattern",
            f"{pattern_id} — {compact(row['name'])}",
            "audit",
            pattern_id=pattern_id,
            evidence_level=row["evidence_level"],
            domain=row["domain"],
            statement=row["statement"],
            verdict=row["verdict"],
            source_file=rel(ATLAS),
            source_location=f"row:{row_no}",
        )
        builder.edge(f"atlas_contains_{slug(pattern_id)}", atlas_doc, node_id, "contains", "audit", "EXTRACTED", ATLAS, f"row:{row_no}")
        for check_id in expand_checks(row["verification"]):
            verification_id = f"verification_{check_id.lower()}"
            builder.node(verification_id, "verification", check_id, "audit", verification_id=check_id, evidence_kind="formal_machine_check", source_file=rel(VERIFICATION), source_location=verification_loc.get(check_id, f"check:{check_id}"), status_effect="math predicate only; no automatic St_FTS promotion")
            builder.edge(f"pattern_{slug(pattern_id)}_verified_{check_id.lower()}", node_id, verification_id, "verified_by", "audit", "EXTRACTED", ATLAS, f"row:{row_no}:verification")

    anchors = read_oq_anchors()
    oq_ids: dict[str, str] = {}
    for anchor, data in anchors.items():
        oq_id = f"oq_{slug(anchor)}"
        oq_ids[anchor] = oq_id
        builder.node(oq_id, "open_question", f"{anchor} — {compact(data['text'])}", "audit", anchor=anchor, oq_status=data["status"], source_file=rel(OPEN_QUESTIONS), source_location=data["line"])

    map_doc = builder.document(OQ_MAP, label="PATTERN_OQ_MAP — маршруты вопросов", layer="audit")
    mapping = read_tsv(OQ_MAP)
    for row_no, row in enumerate(mapping, 2):
        anchor = row["oq_anchor"]
        oq_id = oq_ids.get(anchor)
        if oq_id is None:
            continue
        builder.edge(f"oq_map_contains_{slug(anchor)}", map_doc, oq_id, "contains", "audit", "EXTRACTED", OQ_MAP, f"row:{row_no}")
        program_id = builder.node(f"program_{slug(row['research_program'])}", "program", row["research_program"], "audit", source_file=rel(OQ_MAP), source_location=f"row:{row_no}")
        event_id = builder.node(f"event_{slug(row['resolution_event'])}", "event", row["resolution_event"], "audit", source_file=rel(OQ_MAP), source_location=f"row:{row_no}")
        builder.edge(f"oq_{slug(anchor)}_program", oq_id, program_id, "belongs_to_program", "audit", "EXTRACTED", OQ_MAP, f"row:{row_no}")
        builder.edge(f"oq_{slug(anchor)}_event", oq_id, event_id, "planned_resolution_event", "audit", "EXTRACTED", OQ_MAP, f"row:{row_no}")
        for meta in [part.strip() for part in row["meta_pattern"].split(";") if part.strip()]:
            meta_id = builder.node(f"meta_{slug(meta)}", "meta_pattern", meta, "audit", source_file=rel(OQ_MAP), source_location=f"row:{row_no}")
            builder.edge(f"oq_{slug(anchor)}_meta_{slug(meta)}", oq_id, meta_id, "grouped_by_meta_pattern", "audit", "EXTRACTED", OQ_MAP, f"row:{row_no}")
        relation = {"direct": "directly_traced_to", "indirect": "curated_bridge_to", "support": "navigation_support_for"}.get(row["bridge_type"], "curated_bridge_to")
        for pattern in [part.strip() for part in row["pattern_ids"].split(";") if part.strip()]:
            pattern_id = pattern_ids.get(pattern)
            if pattern_id:
                builder.edge(f"{slug(pattern)}_{slug(anchor)}_{relation}", pattern_id, oq_id, relation, "audit", "EXTRACTED" if row["bridge_type"] in {"direct", "support"} else "INFERRED", OQ_MAP, f"row:{row_no}", scope=row["common_blocker"], status_effect="navigation only; no status change")

    def add_external_evidence(path: Path, prefix: str, key_field: str) -> None:
        if not path.is_file():
            return
        rows = read_tsv(path)
        doc = builder.document(path, layer="external_research")
        for row_no, row in enumerate(rows, 2):
            record = row.get(key_field) or next(iter(row.values()), f"row-{row_no}")
            node_id = f"evidence_external_{slug(prefix)}_{slug(record)}"
            builder.node(node_id, "external_evidence", f"{record} — {compact(row.get('primary_claim') or row.get('claim') or row.get('source') or record)}", "external_research", evidence_id=record, evidence_relation=row.get("relation"), limitation=row.get("limitation") or row.get("strongest_limitation"), raw=row, source_file=rel(path), source_location=f"row:{row_no}")
            builder.edge(f"{slug(prefix)}_doc_contains_{slug(record)}", doc, node_id, "contains", "external_research", "EXTRACTED", path, f"row:{row_no}")
            haystack = " ".join(row.values())
            for card_id, target in card_ids.items():
                if re.search(rf"(?<![A-Za-z0-9_]){re.escape(card_id)}(?![A-Za-z0-9_])", haystack):
                    builder.edge(f"{slug(prefix)}_{slug(record)}_maps_{slug(card_id)}", node_id, target, "maps_to", "external_research", "EXTRACTED", path, f"row:{row_no}", mapping_field=haystack)

    add_external_evidence(NEURAL_EVIDENCE, "neural", "record_id")
    add_external_evidence(SUM_EVIDENCE, "sumdist", "record_id")
    add_external_evidence(E5_EVIDENCE, "e5", "record_id")

    for path in dict.fromkeys([INTERNAL_EVIDENCE, *RESEARCH_DOCS]):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"^##\s+(I\d+)\s*[—-]\s*(.+)$", text, re.MULTILINE):
            evidence_id = f"evidence_internal_{slug(path.stem)}_{slug(match.group(1))}"
            builder.node(evidence_id, "internal_evidence", f"{match.group(1)} — {compact(match.group(2))}", "internal_research", evidence_id=match.group(1), source_file=rel(path), source_location=f"L{text[:match.start()].count(chr(10)) + 1}", limitation="см. документ и локатор; результат ограничен заявленной средой")
            doc = builder.document(path, layer="internal_research")
            builder.edge(f"{slug(path.stem)}_contains_{slug(match.group(1))}", doc, evidence_id, "contains", "internal_research", "EXTRACTED", path, f"L{text[:match.start()].count(chr(10)) + 1}")

    for row_no, row in enumerate(read_tsv(RESEARCH_EVIDENCE), 2):
        source_path = ROOT / row["source_file"]
        doc = builder.document(source_path, layer="internal_research")
        evidence_id = f"evidence_internal_{slug(row['evidence_id'])}"
        builder.node(
            evidence_id,
            "internal_evidence",
            f"{row['evidence_id']} — {row['label']}",
            "internal_research",
            evidence_id=row["evidence_id"],
            evidence_kind=row["evidence_kind"],
            scope=row["scope"],
            limitation=row["limitation"],
            status_effect=row["status_effect"],
            source_file=rel(source_path),
            source_location=row["source_locator"],
        )
        builder.edge(f"research_evidence_contains_{slug(row['evidence_id'])}", doc, evidence_id, "contains", "internal_research", "EXTRACTED", RESEARCH_EVIDENCE, f"row:{row_no}")

    research_claim_doc_paths: dict[str, Path] = {}
    research_claims = read_tsv(RESEARCH_CLAIMS)
    research_claim_ids: dict[str, str] = {}
    for row_no, row in enumerate(research_claims, 2):
        claim_id = row["claim_id"]
        node_id = f"claim_{slug(claim_id)}"
        research_claim_ids[claim_id] = node_id
        source_path = ROOT / row["source_file"]
        research_claim_doc_paths[claim_id] = source_path
        doc = builder.document(source_path, layer="research")
        builder.node(node_id, "claim", f"{claim_id} — {compact(row['statement'])}", "research", claim_id=claim_id, granularity=row["granularity"], scope=row["scope"], status_axis=row["status_axis"], status_text=row["status_text"], source_file=rel(source_path), source_location=row["source_locator"])
        builder.edge(f"{slug(claim_id)}_documented_in", node_id, doc, "documented_in", "research", "EXTRACTED", source_path, row["source_locator"])
        assessment_id = f"assessment_{slug(claim_id)}"
        builder.node(assessment_id, "status_assessment", f"{claim_id}: {row['status_text']}", "research", status_text=row["status_text"], status_axis=row["status_axis"], status_effect="research status only; no St_FTS promotion", source_file=rel(source_path), source_location=row["source_locator"])
        builder.edge(f"{slug(claim_id)}_has_status", node_id, assessment_id, "has_status", "research", "EXTRACTED", source_path, row["source_locator"], status_effect="research status only; no St_FTS promotion")

    bridge_rows = read_tsv(RESEARCH_BRIDGES)
    bridge_target_aliases: dict[str, str] = {}
    for node_id, node in builder.nodes.items():
        if node.get("evidence_id"):
            bridge_target_aliases[str(node["evidence_id"])] = node_id
    # Explicit research bridges may point back to an exact canonical or author
    # card.  The TSV remains the curated assertion; this aliasing only resolves
    # the already existing graph node and does not infer a relation by name.
    bridge_target_aliases.update(card_ids)
    bridge_target_aliases.update(author_ids)
    bridge_target_aliases.update({
        "neural_skeleton_consideration": "doc_work_v14_rebuild_neural_skeleton_research_2026_09_15_consideration_brief_md",
        "deep_report_10_integration": "doc_work_v14_rebuild_neural_skeleton_research_2026_09_15_deep_research_report_10_integration_md",
    })
    for row_no, row in enumerate(bridge_rows, 2):
        source = research_claim_ids.get(row["claim_id"])
        if source is None:
            raise ValueError(f"bridge {row['bridge_id']} refers to unknown claim {row['claim_id']}")
        target = bridge_target_aliases.get(row["target_ref"])
        if target is None and row["target_type"] == "document":
            target = builder.document(ROOT / row["source_file"], layer="research")
        if target is None:
            raise ValueError(f"bridge {row['bridge_id']} target not found: {row['target_ref']}")
        bridge_source = ROOT / row["source_file"]
        builder.edge(row["bridge_id"], source, target, row["relation"], "research_bridge", row["confidence"].upper(), bridge_source, f"row:{row_no}", scope=row["scope"], status_effect=row["status_effect"], rationale=row["rationale"])

    add_project_entity(builder, card_ids)
    graph = builder.output()
    canonical_triple_count = len(read_tsv(CANON_TRIPLES))
    graph["coverage"] = {
        "canonical_cards": len(canon_cards),
        "canonical_triples": canonical_triple_count,
        "canonical_card_depends_on": sum(len(card.get("depends_on") or []) for card in canon_cards),
        "canonical_input_assertions": canonical_triple_count + sum(len(card.get("depends_on") or []) for card in canon_cards) + sum(len(read_tsv(directory / "triples.tsv")) for directory in AUTHOR_PACKAGES) + sum(len(card.get("depends_on") or []) for card in author_cards),
        "author_cards": len(author_cards),
        "author_triples": sum(len(read_tsv(directory / "triples.tsv")) for directory in AUTHOR_PACKAGES),
        "audit_claim_groups": len(claims),
        "audit_findings": len(findings),
        "patterns": len(atlas),
        "open_question_anchors": len(anchors),
        "mapped_open_questions": len(mapping),
        "verification_nodes": len([node for node in builder.nodes.values() if node["type"] == "verification"]),
        "external_evidence_nodes": len([node for node in builder.nodes.values() if node["type"] == "external_evidence"]),
        "internal_evidence_nodes": len([node for node in builder.nodes.values() if node["type"] == "internal_evidence"]),
        "research_claims": len(research_claims),
        "curated_research_bridges": len(bridge_rows),
        "project_entities": 1,
        "declared_research_scopes": 4,
        "nodes": len(builder.nodes),
        "edges": len(builder.edges),
        "unresolved_references": len([node for node in builder.nodes.values() if node["type"] in {"unresolved_reference", "source_reference"}]),
    }
    return graph


def write_markdown_reports(graph: dict[str, Any]) -> None:
    coverage = graph["coverage"]
    lines = [
        "# FTS claim graph — coverage",
        "",
        "Граф собран детерминированно из перечисленных в `input_digests` артефактов.",
        "Он сохраняет канон, авторский supplement и research-layer раздельно.",
        "",
        "## Покрытие",
        "",
    ]
    for key, value in coverage.items():
        lines.append(f"- `{key}`: {value}")
    lines += [
        "",
        "## Границы",
        "",
        "- `CLAIM_MATRIX.tsv` покрыт на уровне 25 групп; атомарные claims внутри групп не выдумываются.",
        "- C01–C62 представлены как verification-evidence; их PASS не повышает St_FTS.",
        "- Неразрешённые ссылки сохранены как `source_reference`/`unresolved_reference` с `нет в артефактах`.",
        "- Точные записи книги адресуются как `source_fragment`; scope/literal сохраняют группировку и тип, не создавая новых канонических карточек.",
        "- Решения по ссылкам и отношениям: `audit/REFERENCE_RESOLUTIONS.tsv`, `audit/GRAPH_RELATION_PATCH.tsv`, `audit/DEPENDENCY_CYCLE_REVIEW.tsv`.",
        "- Внешние evidence-строки без явного bridge остаются evidence-узлами без поддержки конкретного claim.",
        "- Graphify не используется как authoritative storage, поскольку его простой граф может схлопывать параллельные relation-варианты.",
        "",
        "## Обработанные слои",
        "",
        "- `canonical_v13`: карточки и все направленные триплеты/`depends_on`.",
        "- `author_canon`: AC-2026-09-21 и AC-2026-10-03 с отдельным provenance и статусом авторского принятия; прежние уточнения сохраняются исторически.",
        "- `audit`: claims, findings, patterns, OQ и проверки.",
        "- `external_research` и `internal_research`: evidence matrices и внутренние результаты.",
        "- `research_bridge`: только явно записанные curated bridges из `RESEARCH_CLAIM_BRIDGES.tsv`.",
        "",
        "Основной файл: `claim_graph.json`. Схема: `SCHEMA.md`.",
    ]
    COVERAGE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    bridge_rows = read_tsv(RESEARCH_BRIDGES)
    change_lines = [
        "# Claim graph change report",
        "",
        "Текущий research-layer инкремент преобразован в адресуемые claims/evidence",
        "и сохранён с provenance. Это отчёт изменения машинной карты, не решение о",
        "повышении статуса ФТС.",
        "",
        "## Claims",
        "",
    ]
    for node in graph["nodes"]:
        if node["type"] == "claim" and node.get("layer") == "research":
            change_lines.append(f"- `{node['id']}`: {node['label']} — status `{node.get('status_text')}`; scope `{node.get('scope')}`.")
    change_lines += ["", "## Bridges", ""]
    for row in bridge_rows:
        change_lines.append(f"- `{row['bridge_id']}`: `{row['claim_id']}` —{row['relation']}→ `{row['target_ref']}`; scope `{row['scope']}`; status effect `{row['status_effect']}`; source `{row['source_file']}#{row['source_locator']}`.")
    change_lines += [
        "",
        "## Ограничения",
        "",
        "- Все bridges помечены curated/extracted и не меняют `St_FTS`.",
        "- Deep Research (10) представлен как уточнение research-layer claim и boundary, а не как новая эмпирика.",
        "- Внутренние neural результаты остаются synthetic/internal evidence с локальной областью.",
    ]
    CHANGE_REPORT_PATH.write_text("\n".join(change_lines) + "\n", encoding="utf-8", newline="\n")


def write_graph(graph: dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    GRAPH_PATH.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_markdown_reports(graph)
    write_html_view(graph)


def write_html_view(graph: dict[str, Any]) -> None:
    payload = json.dumps(graph, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    template = r'''<!doctype html>
<meta charset="utf-8">
<title>FTS claim graph</title>
<style>
body{font:14px system-ui,sans-serif;margin:0;color:#17202a;background:#f6f7f9}
header{padding:18px 24px;background:#17202a;color:white}
main{display:grid;grid-template-columns:minmax(360px,1fr) minmax(420px,1fr);gap:16px;padding:16px 24px}
input,select{padding:8px;border:1px solid #bac2cc;border-radius:5px;margin:0 6px 8px 0;background:white}
table{width:100%;border-collapse:collapse;background:white} th,td{text-align:left;border-bottom:1px solid #e4e7eb;padding:7px;vertical-align:top}
tr{cursor:pointer} tr:hover{background:#eef5ff} code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12px}
.muted{color:#66717f}.tag{display:inline-block;padding:2px 6px;border-radius:10px;background:#e8edf3;margin:2px}.panel{background:white;border:1px solid #d9dee5;border-radius:7px;padding:12px;overflow:auto}.edge{padding:6px 0;border-bottom:1px solid #edf0f3}
@media(max-width:900px){main{grid-template-columns:1fr}}
</style>
<header><h1>FTS claim graph</h1><div id="summary" class="muted"></div></header>
<main><section class="panel"><input id="q" placeholder="поиск ID, label, source…" style="width:55%"><select id="layer"><option value="">все слои</option></select><select id="type"><option value="">все типы</option></select><select id="relation"><option value="">все relations</option></select><div id="table"></div></section><section class="panel"><div id="detail" class="muted">Выберите узел.</div></section></main>
<script id="graph-data" type="application/json">__GRAPH_DATA__</script>
<script>
const G=JSON.parse(document.getElementById('graph-data').textContent), N=Object.fromEntries(G.nodes.map(n=>[n.id,n]));
const $=id=>document.getElementById(id), values=key=>[...new Set(G.nodes.map(n=>n[key]).filter(Boolean))].sort();
for(const x of values('layer')) $('layer').insertAdjacentHTML('beforeend',`<option>${x}</option>`);
for(const x of values('type')) $('type').insertAdjacentHTML('beforeend',`<option>${x}</option>`);
for(const x of [...new Set(G.edges.map(e=>e.relation))].sort()) $('relation').insertAdjacentHTML('beforeend',`<option>${x}</option>`);
$('summary').textContent=G.nodes.length+' узлов · '+G.edges.length+' направленных рёбер · directed multiset · provenance сохранён';
function esc(x){return String(x??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}
function render(){const q=$('q').value.toLowerCase(), l=$('layer').value,t=$('type').value; const rows=G.nodes.filter(n=>(!q||JSON.stringify(n).toLowerCase().includes(q))&&(!l||n.layer===l)&&(!t||n.type===t)).slice(0,300); $('table').innerHTML='<table><thead><tr><th>ID</th><th>Тип</th><th>Слой</th><th>Label</th></tr></thead><tbody>'+rows.map(n=>'<tr data-id="'+esc(n.id)+'"><td><code>'+esc(n.id)+'</code></td><td>'+esc(n.type)+'</td><td>'+esc(n.layer)+'</td><td>'+esc(n.label)+'</td></tr>').join('')+'</tbody></table>'; for(const tr of document.querySelectorAll('tr[data-id]')) tr.onclick=()=>show(tr.dataset.id);}
function show(id){const n=N[id], es=G.edges.filter(e=>e.source===id||e.target===id); $('detail').innerHTML='<h2>'+esc(n.label)+'</h2><div><span class="tag">'+esc(n.type)+'</span><span class="tag">'+esc(n.layer)+'</span></div><p><code>'+esc(n.id)+'</code><br><span class="muted">'+esc(n.source_file||'нет source_file')+(n.source_location?'#'+esc(n.source_location):'')+'</span></p><h3>Связи ('+es.length+')</h3>'+es.map(e=>'<div class="edge"><code>'+esc(e.source)+'</code> —<b>'+esc(e.relation)+'</b>→ <code>'+esc(e.target)+'</code><br><span class="muted">'+esc(e.confidence)+' · '+esc(e.source_file)+'#'+esc(e.source_location||'')+'</span></div>').join('');}
for(const id of ['q','layer','type']) $(id).oninput=render; $('relation').onchange=()=>{const v=$('relation').value; document.querySelectorAll('.edge').forEach(x=>x.style.display=(!v||x.textContent.includes(v))?'':'none');}; render();
</script>
'''
    HTML_PATH.write_text(template.replace("__GRAPH_DATA__", payload), encoding="utf-8", newline="\n")


def load_graph() -> dict[str, Any]:
    if not GRAPH_PATH.is_file():
        raise FileNotFoundError(f"нет {rel(GRAPH_PATH)} — выполни build")
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def validate_graph(graph: dict[str, Any], idempotent: bool = False) -> dict[str, Any]:
    resolutions = load_resolutions()
    nodes = {str(node["id"]): node for node in graph.get("nodes", [])}
    edges = list(graph.get("edges", []))
    if len(nodes) != len(graph.get("nodes", [])):
        raise AssertionError("duplicate node IDs")
    edge_ids = [str(edge.get("id")) for edge in edges]
    if len(set(edge_ids)) != len(edge_ids):
        raise AssertionError("duplicate edge IDs")
    missing_endpoints = [edge for edge in edges if edge.get("source") not in nodes or edge.get("target") not in nodes]
    if missing_endpoints:
        raise AssertionError(f"missing edge endpoints: {missing_endpoints[:3]}")
    invalid_relations: list[tuple[str, str, str, str]] = []
    for edge in edges:
        if edge.get("layer") in {"canonical_v13", "author_canon"} and edge.get("assertion_kind") in {"triple", "card_field"}:
            continue
        rule = RELATION_RULES.get(str(edge.get("relation")))
        if rule is None:
            # Every canonical predicate is valid if it originated in a source layer.
            if edge.get("layer") not in {"canonical_v13", "author_canon"}:
                invalid_relations.append((edge["id"], edge["relation"], nodes[edge["source"]]["type"], nodes[edge["target"]]["type"]))
            continue
        source_type = nodes[edge["source"]]["type"]
        target_type = nodes[edge["target"]]["type"]
        if source_type not in rule[0] or target_type not in rule[1]:
            invalid_relations.append((edge["id"], edge["relation"], source_type, target_type))
    if invalid_relations:
        raise AssertionError(f"invalid relation types: {invalid_relations[:5]}")

    current_inputs = {item["path"]: item["sha256"] for item in graph.get("input_digests", [])}
    stale = []
    for path_text, expected_hash in current_inputs.items():
        path = ROOT / path_text
        if not path.is_file():
            stale.append((path_text, "missing"))
        elif sha256(path) != expected_hash:
            stale.append((path_text, "hash_mismatch"))
    if stale:
        raise AssertionError(f"stale provenance: {stale[:5]}")

    rebuilt_graph = build_graph()
    expected_inputs = {
        item["path"]: item["sha256"]
        for item in rebuilt_graph.get("input_digests", [])
    }
    if current_inputs != expected_inputs:
        added = sorted(set(expected_inputs) - set(current_inputs))
        removed = sorted(set(current_inputs) - set(expected_inputs))
        changed = sorted(
            path_text
            for path_text in set(current_inputs) & set(expected_inputs)
            if current_inputs[path_text] != expected_inputs[path_text]
        )
        raise AssertionError(
            "input digest manifest drift: "
            f"added={added[:5]} removed={removed[:5]} changed={changed[:5]}"
        )

    expected_project_nodes = {node["id"]: node for node in rebuilt_graph["nodes"]
                              if node.get("layer") == "project_definition"}
    actual_project_nodes = {node["id"]: node for node in graph["nodes"]
                            if node.get("layer") == "project_definition"}
    expected_project_edges = {edge["id"]: edge for edge in rebuilt_graph["edges"]
                              if edge.get("layer") == "project_definition"}
    actual_project_edges = {edge["id"]: edge for edge in edges
                            if edge.get("layer") == "project_definition"}
    if expected_project_nodes != actual_project_nodes or expected_project_edges != actual_project_edges:
        raise AssertionError("Project entity/scope projection is missing or stale")

    for node in graph.get("nodes", []):
        source_file = node.get("source_file")
        if source_file and not (ROOT / source_file).is_file():
            raise AssertionError(f"node source missing: {node['id']} -> {source_file}")
        if node.get('resolution_state') == 'resolved_fragment':
            resolution = resolutions.get(node.get('raw_reference'))
            if resolution is None:
                raise AssertionError(f'Unregistered fragment: {node["id"]}')
            location, witness = fragment_witness(ROOT, resolution)
            if (node.get('source_file'), node.get('source_location'), node.get('fragment_record')) != (resolution['target'], location, witness):
                raise AssertionError(f'Fragment witness drift: {node["id"]}')
        if node.get('resolution_state') == 'unresolved_reference':
            resolution = resolutions.get(node.get('raw_reference'))
            if resolution is None or resolution['resolution'] not in {'missing', 'ambiguous'} or not node.get('next_step'):
                raise AssertionError(f'Unclassified unresolved reference: {node["id"]}')
    for edge in edges:
        source_file = edge.get("source_file")
        if source_file and not (ROOT / source_file).is_file():
            raise AssertionError(f"edge source missing: {edge['id']} -> {source_file}")

    # Directional canonical completeness, including parallel relation variants.
    expected_signatures: list[tuple[str, str, str, str, str]] = []
    for path_text, prefix in [(rel(CANON_TRIPLES), "canonical_v13"), *[(rel(directory / "triples.tsv"), "author_canon") for directory in AUTHOR_PACKAGES]]:
        path = ROOT / path_text
        with path.open(encoding="utf-8", newline="") as handle:
            for row_no, row in enumerate(csv.DictReader(handle, delimiter="\t"), 2):
                source = _expected_ref_id(row["subject"], prefix, graph)
                target = _expected_ref_id(row["object"], prefix, graph)
                expected_signatures.append((source, target, row["predicate"], path_text, f"row:{row_no}"))
    for path_text, prefix in [(rel(CANON_CARDS), "canonical_v13"), *[(rel(directory / "cards.jsonl"), "author_canon") for directory in AUTHOR_PACKAGES]]:
        path = ROOT / path_text
        ids = _card_ids_for_prefix(path, prefix)
        for card in read_jsonl(path):
            source = ids[str(card["id"])]
            for index, dependency in enumerate(card.get("depends_on") or []):
                target = _expected_ref_id(dependency, prefix, graph)
                expected_signatures.append((source, target, "depends_on", path_text, f"card:{card['id']}:depends_on[{index}]"))
    actual_signatures = {(edge["source"], edge["target"], edge["relation"], edge["source_file"], edge.get("source_location", "")) for edge in edges if edge.get("assertion_kind") in {"triple", "card_field"}}
    missing_assertions = [signature for signature in expected_signatures if signature not in actual_signatures]
    if missing_assertions:
        raise AssertionError(f"lost directed assertions: {missing_assertions[:5]} (total {len(missing_assertions)})")
    expected_parallel: dict[tuple[str, str], set[str]] = {}
    actual_parallel: dict[tuple[str, str], set[str]] = {}
    for source, target, relation, _path, _location in expected_signatures:
        expected_parallel.setdefault((source, target), set()).add(relation)
    for edge in edges:
        if edge.get("assertion_kind") in {"triple", "card_field"}:
            actual_parallel.setdefault((edge["source"], edge["target"]), set()).add(edge["relation"])
    if expected_parallel != actual_parallel:
        differences = []
        for pair in sorted(set(expected_parallel) | set(actual_parallel)):
            if expected_parallel.get(pair, set()) != actual_parallel.get(pair, set()):
                differences.append((pair, sorted(expected_parallel.get(pair, set())), sorted(actual_parallel.get(pair, set()))))
        raise AssertionError(f"lost parallel relation variants: {differences[:5]} (total {len(differences)})")

    expected_research_claims = {f"claim_{slug(row['claim_id'])}" for row in read_tsv(RESEARCH_CLAIMS)}
    actual_research_claims = {node["id"] for node in graph.get("nodes", []) if node.get("type") == "claim" and node.get("layer") == "research"}
    if expected_research_claims != actual_research_claims:
        raise AssertionError(f"stale or missing derived claims: expected={sorted(expected_research_claims)} actual={sorted(actual_research_claims)}")
    expected_bridges = {row["bridge_id"] for row in read_tsv(RESEARCH_BRIDGES)}
    actual_bridges = {edge["id"] for edge in edges if edge.get("layer") == "research_bridge"}
    if expected_bridges != actual_bridges:
        raise AssertionError(f"stale or missing research bridges: expected={sorted(expected_bridges)} actual={sorted(actual_bridges)}")

    for node in graph.get("nodes", []):
        if node["type"] in {"card", "author_statement", "claim", "claim_group"}:
            outgoing = [edge for edge in edges if edge["source"] == node["id"] and edge["relation"].startswith("has_status")]
            if not outgoing:
                raise AssertionError(f"status without assessment edge: {node['id']}")

    result = {
        "nodes": len(nodes),
        "edges": len(edges),
        "canonical_assertions": len(expected_signatures),
        "canonical_assertions_present": len(expected_signatures) - len(missing_assertions),
        "parallel_relation_pairs": _parallel_relation_pairs(expected_signatures),
        "unresolved_nodes": sum(node["type"] in {"unresolved_reference", "source_reference"} for node in nodes.values()),
    }
    if idempotent:
        first = json.dumps(build_graph(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        second = json.dumps(build_graph(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        if first != second:
            raise AssertionError("build is not idempotent")
        result["idempotent"] = True
    return result


def _card_ids_for_prefix(path: Path, prefix: str) -> dict[str, str]:
    return {str(card["id"]): f"card_{slug(str(card['id']))}" if prefix == "canonical_v13" else f"author_{slug(str(card['id']))}" for card in read_jsonl(path)}


def _expected_ref_id(raw: str, layer: str, graph: dict[str, Any]) -> str:
    raw = str(raw).strip()
    for node in graph.get("nodes", []):
        if node.get("card_id") == raw and node.get("layer") == layer:
            return str(node["id"])
    for node in graph.get("nodes", []):
        if node.get("card_id") == raw:
            return str(node["id"])
    for node in graph.get("nodes", []):
        if node.get("raw_value") == raw or node.get("raw_reference") == raw:
            return str(node["id"])
    raise AssertionError(f"cannot resolve expected graph reference: {raw}")


def _parallel_relation_pairs(signatures: list[tuple[str, str, str, str, str]]) -> int:
    pairs: dict[tuple[str, str], set[str]] = {}
    for source, target, relation, _path, _loc in signatures:
        pairs.setdefault((source, target), set()).add(relation)
    return sum(len(relations) > 1 for relations in pairs.values())


def alias_map(graph: dict[str, Any]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in graph["nodes"]:
        node_id = str(node["id"])
        aliases[node_id] = node_id
        for key in ("project_id", "claim_id", "card_id", "anchor", "verification_id", "evidence_id", "finding_id", "pattern_id"):
            if node.get(key):
                aliases[str(node[key])] = node_id
        if node.get("type") == "source_document" and node.get("source_file"):
            document_stem = Path(str(node["source_file"])).stem
            aliases[slug(document_stem)] = node_id
            if document_stem == "DEEP_RESEARCH_REPORT_10_INTEGRATION":
                aliases["deep_report_10_integration"] = node_id
    # Prefer active canonical cards for public card-ID aliases; explicit author node IDs remain available.
    for node in graph["nodes"]:
        if node.get("type") == "card" and node.get("card_id"):
            aliases[str(node["card_id"])] = str(node["id"])
    return aliases


def normalize_search(value: object) -> str:
    text = str(value or "").lower().replace("ё", "е")
    text = re.sub(r"[^a-zа-я0-9]+", " ", text)
    return " ".join(text.split())


def search_graph(graph: dict[str, Any], text: str, limit: int = 10) -> str:
    query_text = normalize_search(text)
    terms = [term for term in query_text.split() if len(term) > 1]
    aliases = alias_map(graph)
    ranked: list[tuple[int, str, dict[str, Any]]] = []
    for node in graph["nodes"]:
        node_id = str(node["id"])
        id_text = normalize_search(node_id)
        label_text = normalize_search(node.get("label"))
        source_text = normalize_search(node.get("source_file"))
        body_text = normalize_search(json.dumps(node, ensure_ascii=False, sort_keys=True))
        score = 0
        if text in aliases and aliases[text] == node_id:
            score += 200
        if query_text and query_text == label_text:
            score += 120
        elif query_text and query_text in label_text:
            score += 60
        if query_text and query_text in id_text:
            score += 50
        for term in terms:
            if term in label_text:
                score += 18
            if term in id_text:
                score += 12
            if term in source_text:
                score += 4
            if term in body_text:
                score += 2
        if score:
            ranked.append((score, node_id, node))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    if not ranked:
        return f"ничего не найдено: {text}"
    lines = []
    for score, node_id, node in ranked[: max(1, limit)]:
        lines.append(
            f"{node_id}\t{node.get('type')}\t{node.get('layer')}\t"
            f"score={score}\t{node.get('label')}\t{node.get('source_file', '')}"
        )
    return "\n".join(lines)


def query(graph: dict[str, Any], target: str, depth: int = 1) -> str:
    aliases = alias_map(graph)
    node_id = aliases.get(target, aliases.get(target.upper(), target))
    nodes = {node["id"]: node for node in graph["nodes"]}
    if node_id not in nodes:
        return f"нет узла: {target}"
    edge_list = graph["edges"]
    selected = {node_id: 0}
    queue: deque[str] = deque([node_id])
    while queue:
        current = queue.popleft()
        if selected[current] >= depth:
            continue
        for edge in edge_list:
            if edge["source"] == current or edge["target"] == current:
                other = edge["target"] if edge["source"] == current else edge["source"]
                if other not in selected:
                    selected[other] = selected[current] + 1
                    queue.append(other)
    lines = [f"NODE {node_id}: {nodes[node_id].get('label')}", f"  type={nodes[node_id].get('type')} layer={nodes[node_id].get('layer')} source={nodes[node_id].get('source_file', 'n/a')}" ]
    for edge in edge_list:
        if edge["source"] in selected and edge["target"] in selected and (edge["source"] == node_id or edge["target"] == node_id or depth > 1):
            lines.append(f"EDGE {edge['source']} -[{edge['relation']}|{edge['confidence']}]-> {edge['target']} source={edge.get('source_file')}#{edge.get('source_location', '')}")
    return "\n".join(lines)


def path_query(graph: dict[str, Any], source: str, target: str) -> str:
    aliases = alias_map(graph)
    source_id = aliases.get(source, source)
    target_id = aliases.get(target, target)
    nodes = {node["id"]: node for node in graph["nodes"]}
    if source_id not in nodes or target_id not in nodes:
        return f"нет узла: {source if source_id not in nodes else target}"
    outgoing: dict[str, list[dict[str, Any]]] = {}
    for edge in graph["edges"]:
        outgoing.setdefault(edge["source"], []).append(edge)
    queue: deque[str] = deque([source_id])
    previous: dict[str, tuple[str, dict[str, Any]]] = {}
    seen = {source_id}
    while queue:
        current = queue.popleft()
        if current == target_id:
            break
        for edge in outgoing.get(current, []):
            other = edge["target"]
            if other not in seen:
                seen.add(other)
                previous[other] = (current, edge)
                queue.append(other)
    if target_id not in seen:
        return f"маршрут не найден: {source_id} → {target_id}; последний доступный подграф узлов={len(seen)}"
    steps: list[str] = []
    current = target_id
    while current != source_id:
        prior, edge = previous[current]
        steps.append(f"{prior} -[{edge['relation']}|{edge['confidence']}]-> {current} ({edge.get('source_file')}#{edge.get('source_location', '')})")
        current = prior
    return "\n".join(reversed(steps))


def main() -> int:
    parser = argparse.ArgumentParser(description="FTS directed claim/evidence graph")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("--idempotent", action="store_true")
    sub.add_parser("coverage")
    query_parser = sub.add_parser("query")
    query_parser.add_argument("target")
    query_parser.add_argument("--depth", type=int, default=1)
    search_parser = sub.add_parser("search")
    search_parser.add_argument("text")
    search_parser.add_argument("--limit", type=int, default=10)
    path_parser = sub.add_parser("path")
    path_parser.add_argument("source")
    path_parser.add_argument("target")
    args = parser.parse_args()
    if args.command == "build":
        graph = build_graph()
        write_graph(graph)
        print(f"CLAIM GRAPH built: {graph['coverage']['nodes']} nodes, {graph['coverage']['edges']} edges; {graph['coverage']['canonical_input_assertions']} canonical input assertions")
        return 0
    graph = load_graph()
    if args.command == "validate":
        result = validate_graph(graph, idempotent=args.idempotent)
        print("CLAIM GRAPH validate: " + json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "coverage":
        print(json.dumps(graph["coverage"], ensure_ascii=False, indent=2))
        return 0
    if args.command == "query":
        print(query(graph, args.target, depth=args.depth))
        return 0
    if args.command == "search":
        print(search_graph(graph, args.text, limit=args.limit))
        return 0
    if args.command == "path":
        print(path_query(graph, args.source, args.target))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
