"""Детерминированный навигационный слой полного аудита для Graphify.

Этот тул не извлекает смысл LLM-моделью и не меняет канон. Он читает только
проверенные структурированные артефакты аудита:

* ``PATTERN_ATLAS.tsv`` — 31 закономерность;
* ``PATTERN_OQ_MAP.tsv`` — мосты к действующим OQ, программам и событиям;
* ``CLAIM_MATRIX.tsv`` и ``FINDINGS.tsv`` — трассировка утверждений и находок;
* ``OPEN_QUESTIONS.md`` — точные якоря OQ.

Дисциплина доверия:

* буквальная связь из атласа / таблицы -> ``EXTRACTED``;
* ``indirect`` и непрямой кусок ``mixed`` -> ``INFERRED`` (0.50);
* ``support`` -> ``EXTRACTED`` как служебная навигация, не теоретический вывод.

Использование (из корня репозитория):

    python -X utf8 tools/graphify_audit_navigation.py --stats
    python -X utf8 tools/graphify_audit_navigation.py
    E:\\Codex\\mcp\\graphify\\tools\\graphifyy\\Scripts\\python.exe -X utf8 \
        tools/graphify_audit_navigation.py --inject
    E:\\Codex\\mcp\\graphify\\tools\\graphifyy\\Scripts\\python.exe -X utf8 \
        tools/graphify_audit_navigation.py --verify

Первый режим только читает входы. Обычный режим пишет фрагмент, ``--inject``
добавляет его к существующему ``graph.json`` и обновляет HTML/отчёт. При реальном
изменении графа он создаёт резервный снимок Graphify. ``--inject`` требует
установленный ``graphifyy``; базовая проверка и emit держатся на stdlib.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "work" / "v14_rebuild" / "audit"
OPEN_QUESTIONS = ROOT / "work" / "OPEN_QUESTIONS.md"
OUT_DIR = ROOT / "graphify-out"
GRAPH_PATH = OUT_DIR / "graph.json"
LABELS_PATH = OUT_DIR / ".graphify_labels.json"
FRAGMENT_PATH = OUT_DIR / "audit_navigation_fragment.json"
OVERLAY_REPORT = OUT_DIR / "AUDIT_NAVIGATION.md"
OVERLAY_MANIFEST = OUT_DIR / "audit_navigation_manifest.json"

ATLAS_PATH = AUDIT / "PATTERN_ATLAS.tsv"
MAP_PATH = AUDIT / "PATTERN_OQ_MAP.tsv"
CLAIMS_PATH = AUDIT / "CLAIM_MATRIX.tsv"
FINDINGS_PATH = AUDIT / "FINDINGS.tsv"
REVIEW_PATH = AUDIT / "REVIEW_CONCLUSION.md"

NAV_HUB = "audit_navigation_hub"
DOC_IDS = {
    "atlas": "audit_document_pattern_atlas",
    "map": "audit_document_pattern_oq_map",
    "claims": "audit_document_claim_matrix",
    "findings": "audit_document_findings",
    "review": "audit_document_review_conclusion",
}
ANCHOR_SYSTEM = "work_open_questions_anchor_system"
ANCHOR_RE = re.compile(r"\{#(?P<anchor>oq-[a-z0-9-]+)\}")
OQ_REF_RE = re.compile(r"\boq-[a-z0-9-]+\b")
CLAIM_REF_RE = re.compile(r"\bCM-\d{3}\b")

META_LABELS = {
    "MP-A": "MP-A — баланс различимости (candidate)",
    "MP-B": "MP-B — оконный перенос (candidate)",
    "MP-C": "MP-C — независимое повышение статуса (candidate)",
    "MP-S": "MP-S — служебный контур целостности",
}


def rel(path: Path) -> str:
    """Вернуть единый repo-relative путь для Graphify."""
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compact(value: object, limit: int = 132) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def identifier(prefix: str, value: str) -> str:
    normal = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return f"{prefix}_{normal}"


def split_many(value: object) -> list[str]:
    return [part.strip() for part in str(value or "").split(";") if part.strip()]


def read_tsv(path: Path, required: set[str]) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"нет в артефактах: {rel(path)}")
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    fields = set(rows[0]) if rows else set()
    missing = sorted(required - fields)
    if missing:
        raise ValueError(f"{rel(path)}: отсутствуют поля {missing}")
    return rows


def read_oq_anchors() -> dict[str, dict[str, str]]:
    if not OPEN_QUESTIONS.is_file():
        raise FileNotFoundError(f"нет в артефактах: {rel(OPEN_QUESTIONS)}")
    anchors: dict[str, dict[str, str]] = {}
    for number, raw in enumerate(OPEN_QUESTIONS.read_text(encoding="utf-8").splitlines(), 1):
        for match in ANCHOR_RE.finditer(raw):
            anchor = match.group("anchor")
            if anchor in anchors:
                raise ValueError(f"{rel(OPEN_QUESTIONS)}: дубль якоря {anchor}")
            status = "unknown"
            if "- [ ]" in raw:
                status = "open"
            elif "- [~]" in raw:
                status = "partial"
            elif "- [x]" in raw.lower():
                status = "closed"
            text = ANCHOR_RE.sub("", raw)
            text = re.sub(r"^\s*-\s*\[[ xX~]\]\s*", "", text).strip()
            anchors[anchor] = {"line": f"L{number}", "status": status, "text": text}
    return anchors


def node(
    node_id: str,
    label: str,
    source: str,
    location: str | None,
    *,
    file_type: str = "concept",
    **extra: object,
) -> dict[str, object]:
    return {
        "id": node_id,
        "label": label,
        "file_type": file_type,
        "source_file": source,
        "source_location": location,
        "_origin": "audit_navigation",
        "navigation_layer": "audit",
        "navigation_only": True,
        **extra,
    }


def edge(
    source: str,
    relation: str,
    target: str,
    provenance: str,
    location: str | None,
    *,
    confidence: str = "EXTRACTED",
    score: float | None = None,
) -> dict[str, object]:
    if score is None:
        score = {"EXTRACTED": 1.0, "INFERRED": 0.5, "AMBIGUOUS": 0.2}[confidence]
    return {
        "source": source,
        "target": target,
        "relation": relation,
        "confidence": confidence,
        "confidence_score": score,
        "source_file": provenance,
        "source_location": location,
        "weight": 1.0,
        "navigation_layer": "audit",
        "navigation_only": True,
    }


def add_unique_node(nodes: list[dict[str, object]], seen: set[str], item: dict[str, object]) -> None:
    node_id = str(item["id"])
    if node_id in seen:
        raise ValueError(f"дублирующийся navigation node: {node_id}")
    seen.add(node_id)
    nodes.append(item)


def add_unique_edge(
    edges: list[dict[str, object]],
    seen: set[tuple[str, str, str]],
    item: dict[str, object],
) -> None:
    key = (str(item["source"]), str(item["relation"]), str(item["target"]))
    if key in seen:
        return
    seen.add(key)
    edges.append(item)


def validate_rows(
    atlas: list[dict[str, str]],
    mapping: list[dict[str, str]],
    claims: list[dict[str, str]],
    findings: list[dict[str, str]],
    anchors: dict[str, dict[str, str]],
) -> dict[str, object]:
    atlas_ids = [row["pattern_id"] for row in atlas]
    claim_ids = [row["claim_id"] for row in claims]
    finding_ids = [row["finding_id"] for row in findings]
    for name, values in (("pattern", atlas_ids), ("claim", claim_ids), ("finding", finding_ids)):
        duplicates = sorted(item for item, count in Counter(values).items() if count > 1)
        if duplicates:
            raise ValueError(f"{name}-ID дублируются: {duplicates}")

    atlas_by_id = {row["pattern_id"]: row for row in atlas}
    mapped_patterns = {pattern for row in mapping for pattern in split_many(row["pattern_ids"])}
    if mapped_patterns != set(atlas_by_id):
        raise ValueError(
            "coverage PATTERN_OQ_MAP не совпадает с атласом: "
            f"missing={sorted(set(atlas_by_id) - mapped_patterns)}, "
            f"extra={sorted(mapped_patterns - set(atlas_by_id))}"
        )

    for row in mapping:
        anchor = row["oq_anchor"]
        if anchor not in anchors:
            raise ValueError(f"PATTERN_OQ_MAP ссылается на отсутствующий OQ-якорь: {anchor}")
        if anchors[anchor]["status"] != row["oq_status"]:
            raise ValueError(
                f"статус OQ расходится для {anchor}: "
                f"OPEN_QUESTIONS={anchors[anchor]['status']}, MAP={row['oq_status']}"
            )
        bridge_type = row["bridge_type"]
        if bridge_type not in {"direct", "indirect", "mixed", "support"}:
            raise ValueError(f"неизвестный bridge_type {bridge_type!r} для {anchor}")
        for pattern in split_many(row["pattern_ids"]):
            if pattern not in atlas_by_id:
                raise ValueError(f"PATTERN_OQ_MAP: неизвестный pattern_id {pattern}")
            atlas_oqs = set(OQ_REF_RE.findall(atlas_by_id[pattern]["open_question"]))
            if bridge_type == "direct" and anchor not in atlas_oqs:
                raise ValueError(f"direct-мост {pattern} -> {anchor} отсутствует в PATTERN_ATLAS")

    return {"atlas_by_id": atlas_by_id, "claims_by_id": {row["claim_id"]: row for row in claims}}


def build_fragment() -> tuple[dict[str, object], dict[str, object]]:
    atlas = read_tsv(
        ATLAS_PATH,
        {"pattern_id", "name", "evidence_level", "domain", "statement", "open_question", "verdict"},
    )
    mapping = read_tsv(
        MAP_PATH,
        {
            "oq_anchor", "oq_status", "research_program", "meta_pattern", "pattern_ids",
            "bridge_type", "common_blocker", "resolution_event", "resolution_kind", "note",
        },
    )
    claims = read_tsv(
        CLAIMS_PATH,
        {"claim_id", "claim", "domain", "source", "verification", "status_before", "status_after", "verdict", "resolution"},
    )
    findings = read_tsv(
        FINDINGS_PATH,
        {"finding_id", "severity", "status", "area", "found", "dependencies", "conclusion", "unresolved", "resolution"},
    )
    anchors = read_oq_anchors()
    verified = validate_rows(atlas, mapping, claims, findings, anchors)
    atlas_by_id: dict[str, dict[str, str]] = verified["atlas_by_id"]  # type: ignore[assignment]
    claims_by_id: dict[str, dict[str, str]] = verified["claims_by_id"]  # type: ignore[assignment]

    nodes: list[dict[str, object]] = []
    edges: list[dict[str, object]] = []
    node_seen: set[str] = set()
    edge_seen: set[tuple[str, str, str]] = set()

    def add_node(item: dict[str, object]) -> None:
        add_unique_node(nodes, node_seen, item)

    def add_edge(item: dict[str, object]) -> None:
        add_unique_edge(edges, edge_seen, item)

    add_node(node(
        NAV_HUB,
        "Аудит 2026-07-13/14: закономерности ↔ OQ",
        rel(MAP_PATH),
        "L1",
        evidence_boundary="навигация; не канон и не повышение статуса",
    ))
    doc_specs = [
        ("atlas", "PATTERN ATLAS — 31 закономерность", ATLAS_PATH),
        ("map", "PATTERN ↔ OQ MAP — мосты, программы и события", MAP_PATH),
        ("claims", "CLAIM MATRIX — 25 групп утверждений", CLAIMS_PATH),
        ("findings", "FINDINGS — 20 аудиторских находок", FINDINGS_PATH),
        ("review", "REVIEW CONCLUSION — краткий вердикт", REVIEW_PATH),
    ]
    for key, label, path in doc_specs:
        add_node(node(DOC_IDS[key], label, rel(path), "L1", file_type="document"))
        add_edge(edge(NAV_HUB, "contains", DOC_IDS[key], rel(MAP_PATH), "L1"))

    add_edge(edge(DOC_IDS["review"], "summarizes", DOC_IDS["atlas"], rel(REVIEW_PATH), "L8"))
    add_edge(edge(DOC_IDS["review"], "summarizes", DOC_IDS["claims"], rel(REVIEW_PATH), "L7"))
    add_edge(edge(DOC_IDS["review"], "summarizes", DOC_IDS["findings"], rel(REVIEW_PATH), "L7"))
    add_edge(edge(DOC_IDS["review"], "summarizes", DOC_IDS["map"], rel(REVIEW_PATH), "L10"))

    # PATTERN_ATLAS: каждая закономерность остаётся на своей доказательной ступени.
    for row in atlas:
        pattern = row["pattern_id"]
        pattern_node = identifier("audit_pattern", pattern)
        add_node(node(
            pattern_node,
            f"{pattern} — {row['name']}",
            rel(ATLAS_PATH),
            pattern,
            evidence_level=row["evidence_level"],
            domain=row["domain"],
            statement=row["statement"],
            verdict=row["verdict"],
            open_question=row["open_question"],
        ))
        add_edge(edge(DOC_IDS["atlas"], "contains", pattern_node, rel(ATLAS_PATH), pattern))

    # PATTERN_OQ_MAP: OQ, программы, события, мета-паттерны и мосты.
    program_nodes: set[str] = set()
    event_nodes: set[str] = set()
    meta_nodes: set[str] = set()
    bridge_counts: Counter[str] = Counter()
    for row in mapping:
        anchor = row["oq_anchor"]
        oq_node = identifier("audit_oq", anchor)
        oq = anchors[anchor]
        add_node(node(
            oq_node,
            f"{anchor} — {compact(oq['text'])}",
            rel(OPEN_QUESTIONS),
            oq["line"],
            oq_anchor=anchor,
            oq_status=row["oq_status"],
            question=oq["text"],
            common_blocker=row["common_blocker"],
            resolution_kind=row["resolution_kind"],
            map_note=row["note"],
        ))
        add_edge(edge(DOC_IDS["map"], "indexes", oq_node, rel(MAP_PATH), anchor))
        add_edge(edge(ANCHOR_SYSTEM, "anchors", oq_node, rel(OPEN_QUESTIONS), oq["line"]))

        program = row["research_program"]
        program_node = identifier("audit_program", program)
        if program_node not in program_nodes:
            program_nodes.add(program_node)
            add_node(node(program_node, f"{program} — исследовательская программа", rel(MAP_PATH), program))
            add_edge(edge(DOC_IDS["map"], "contains", program_node, rel(MAP_PATH), program))
        add_edge(edge(oq_node, "belongs_to_program", program_node, rel(MAP_PATH), anchor))

        event_id = row["resolution_event"]
        event_node = identifier("audit_event", event_id)
        if event_node not in event_nodes:
            event_nodes.add(event_node)
            add_node(node(event_node, f"Событие {event_id}", rel(MAP_PATH), event_id))
            add_edge(edge(DOC_IDS["map"], "contains", event_node, rel(MAP_PATH), event_id))
        add_edge(edge(oq_node, "planned_resolution_event", event_node, rel(MAP_PATH), anchor))

        for meta in split_many(row["meta_pattern"]):
            meta_node = identifier("audit_meta", meta)
            if meta_node not in meta_nodes:
                meta_nodes.add(meta_node)
                add_node(node(meta_node, META_LABELS.get(meta, meta), rel(MAP_PATH), meta))
                add_edge(edge(DOC_IDS["map"], "contains", meta_node, rel(MAP_PATH), meta))
            add_edge(edge(oq_node, "grouped_by_meta_pattern", meta_node, rel(MAP_PATH), anchor))

        for pattern in split_many(row["pattern_ids"]):
            pattern_node = identifier("audit_pattern", pattern)
            atlas_oqs = set(OQ_REF_RE.findall(atlas_by_id[pattern]["open_question"]))
            bridge_type = row["bridge_type"]
            if bridge_type == "direct" or (bridge_type == "mixed" and anchor in atlas_oqs):
                relation, confidence, kind = "directly_traced_to", "EXTRACTED", "direct"
            elif bridge_type == "support":
                relation, confidence, kind = "navigation_support_for", "EXTRACTED", "support"
            else:
                relation, confidence, kind = "curated_bridge_to", "INFERRED", "indirect"
            bridge_counts[kind] += 1
            add_edge(edge(
                pattern_node,
                relation,
                oq_node,
                rel(MAP_PATH),
                anchor,
                confidence=confidence,
            ))
            for meta in split_many(row["meta_pattern"]):
                add_edge(edge(
                    pattern_node,
                    "belongs_to_meta_pattern",
                    identifier("audit_meta", meta),
                    rel(MAP_PATH),
                    pattern,
                ))

    # Claim matrix: отдельные, адресуемые группы утверждений.
    for row in claims:
        claim_id = row["claim_id"]
        claim_node = identifier("audit_claim", claim_id)
        add_node(node(
            claim_node,
            f"{claim_id} — {compact(row['claim'])}",
            rel(CLAIMS_PATH),
            claim_id,
            domain=row["domain"],
            verification=row["verification"],
            status_before=row["status_before"],
            status_after=row["status_after"],
            verdict=row["verdict"],
        ))
        add_edge(edge(DOC_IDS["claims"], "contains", claim_node, rel(CLAIMS_PATH), claim_id))

    # Findings: связь с claim-матрицей только при буквальной CM-ссылке в строке.
    finding_claim_links = 0
    for row in findings:
        finding_id = row["finding_id"]
        finding_node = identifier("audit_finding", finding_id)
        add_node(node(
            finding_node,
            f"{finding_id} [{row['severity']}, {row['status']}] — {compact(row['found'])}",
            rel(FINDINGS_PATH),
            finding_id,
            severity=row["severity"],
            finding_status=row["status"],
            area=row["area"],
            conclusion=row["conclusion"],
            unresolved=row["unresolved"],
        ))
        add_edge(edge(DOC_IDS["findings"], "contains", finding_node, rel(FINDINGS_PATH), finding_id))
        references = " ".join(row.values())
        for claim_id in sorted(set(CLAIM_REF_RE.findall(references))):
            if claim_id in claims_by_id:
                finding_claim_links += 1
                add_edge(edge(
                    finding_node,
                    "audits_claim",
                    identifier("audit_claim", claim_id),
                    rel(FINDINGS_PATH),
                    finding_id,
                ))

    hyperedges = [{
        "id": "audit_navigation_bundle",
        "label": "Аудиторский навигационный пакет: claims, findings, patterns и OQ",
        "nodes": [NAV_HUB, *DOC_IDS.values()],
        "relation": "organizes",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": rel(MAP_PATH),
    }]
    all_ids = {str(item["id"]) for item in nodes}
    missing_endpoints = sorted(
        {str(item[key]) for item in edges for key in ("source", "target")} - all_ids - {ANCHOR_SYSTEM}
    )
    if missing_endpoints:
        raise ValueError(f"фрагмент ссылается на отсутствующие узлы: {missing_endpoints}")

    summary: dict[str, object] = {
        "patterns": len(atlas),
        "open_questions": len(mapping),
        "claims": len(claims),
        "findings": len(findings),
        "programs": len(program_nodes),
        "events": len(event_nodes),
        "meta_patterns": len(meta_nodes),
        "nodes": len(nodes),
        "edges": len(edges),
        "hyperedges": len(hyperedges),
        "bridge_direct": bridge_counts["direct"],
        "bridge_indirect": bridge_counts["indirect"],
        "bridge_support": bridge_counts["support"],
        "finding_claim_links": finding_claim_links,
    }
    return {"nodes": nodes, "edges": edges, "hyperedges": hyperedges}, summary


def print_summary(summary: dict[str, object]) -> None:
    print(
        "AUDIT navigation fragment: "
        f"{summary['nodes']} nodes, {summary['edges']} edges, {summary['hyperedges']} hyperedges"
    )
    print(
        "  source coverage: "
        f"{summary['patterns']} patterns, {summary['open_questions']} OQ, "
        f"{summary['claims']} claims, {summary['findings']} findings"
    )
    print(
        "  bridges: "
        f"{summary['bridge_direct']} direct EXTRACTED, "
        f"{summary['bridge_indirect']} curated INFERRED, "
        f"{summary['bridge_support']} support EXTRACTED"
    )


def atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    temporary.replace(path)


def normalize_lf(path: Path) -> None:
    """Keep generated text stable across Windows and Unix checkouts."""
    payload = path.read_bytes()
    normalized = payload.replace(b"\r\n", b"\n")
    if normalized != payload:
        path.write_bytes(normalized)


def git_head() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def read_labels() -> dict[int, str]:
    if not LABELS_PATH.is_file():
        return {}
    raw = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
    return {int(key): value for key, value in raw.items()}


def edge_key(item: dict[str, object]) -> tuple[tuple[str, str], str]:
    endpoints = tuple(sorted((str(item["source"]), str(item["target"]))))
    return endpoints, str(item.get("relation", ""))


def merge_fragment(
    graph: dict[str, object], fragment: dict[str, object]
) -> tuple[dict[str, object], int, int, int, int]:
    nodes = list(graph.get("nodes", []))
    links_key = "links" if "links" in graph else "edges"
    links = list(graph.get(links_key, []))
    existing_nodes = {str(item["id"]): item for item in nodes if isinstance(item, dict) and item.get("id")}
    communities = [item.get("community") for item in nodes if isinstance(item, dict) and isinstance(item.get("community"), int)]
    fragment_communities = {
        prior.get("community")
        for item in fragment["nodes"]  # type: ignore[index]
        if (prior := existing_nodes.get(str(item["id"]))) is not None
        and isinstance(prior.get("community"), int)
    }
    if len(fragment_communities) > 1:
        raise ValueError("audit-навигация распределена по нескольким community")
    nav_community = next(iter(fragment_communities), max(communities, default=-1) + 1)

    added_nodes = 0
    for item in fragment["nodes"]:  # type: ignore[index]
        item = dict(item)
        node_id = str(item["id"])
        prior = existing_nodes.get(node_id)
        if prior is not None:
            if prior.get("label") != item.get("label"):
                raise ValueError(f"Graphify node collision: {node_id}")
            continue
        item["community"] = nav_community
        nodes.append(item)
        existing_nodes[node_id] = item
        added_nodes += 1

    if ANCHOR_SYSTEM not in existing_nodes:
        raise ValueError(f"базовый Graphify-граф не содержит {ANCHOR_SYSTEM}")
    known = set(existing_nodes)
    existing_edges = {edge_key(item) for item in links if isinstance(item, dict) and "source" in item and "target" in item}
    added_edges = 0
    for item in fragment["edges"]:  # type: ignore[index]
        item = dict(item)
        if str(item["source"]) not in known or str(item["target"]) not in known:
            raise ValueError(f"висячее audit-ребро: {item['source']} -> {item['target']}")
        key = edge_key(item)
        if key in existing_edges:
            continue
        links.append(item)
        existing_edges.add(key)
        added_edges += 1

    previous_hyperedges = list(graph.get("hyperedges", []))
    known_hyperedges = {item.get("id") for item in previous_hyperedges if isinstance(item, dict)}
    added_hyperedges = 0
    for item in fragment["hyperedges"]:  # type: ignore[index]
        if item["id"] not in known_hyperedges:
            previous_hyperedges.append(item)
            known_hyperedges.add(item["id"])
            added_hyperedges += 1

    graph["nodes"] = nodes
    graph[links_key] = links
    graph["hyperedges"] = previous_hyperedges
    graph_data = graph.setdefault("graph", {})
    if not isinstance(graph_data, dict):
        raise ValueError("graph.json: поле graph должно быть объектом")
    graph_data["hyperedges"] = previous_hyperedges
    overlays = list(graph_data.get("navigation_overlays", []))
    overlays = [item for item in overlays if item.get("id") != "audit_pattern_oq_v1"]
    overlays.append({
        "id": "audit_pattern_oq_v1",
        "kind": "deterministic_navigation_overlay",
        "confidence_boundary": "EXTRACTED literal / INFERRED curated; no canonical status effect",
        "sources": [rel(ATLAS_PATH), rel(MAP_PATH), rel(CLAIMS_PATH), rel(FINDINGS_PATH), rel(OPEN_QUESTIONS)],
        "community": nav_community,
    })
    graph_data["navigation_overlays"] = overlays
    head = git_head()
    if head:
        graph["built_at_commit"] = head
    return graph, nav_community, added_nodes, added_edges, added_hyperedges


def write_overlay_manifest(summary: dict[str, object], community: int, graph: dict[str, object]) -> None:
    inputs = [ATLAS_PATH, MAP_PATH, CLAIMS_PATH, FINDINGS_PATH, REVIEW_PATH, OPEN_QUESTIONS]
    payload = {
        "schema": "fts_graphify_audit_navigation/v1",
        "kind": "deterministic_navigation_overlay",
        "inputs": {rel(path): sha256(path) for path in inputs},
        "counts": summary,
        "community": community,
        "graph_nodes": len(graph.get("nodes", [])),
        "graph_edges": len(graph.get("links", graph.get("edges", []))),
        "built_at_commit": graph.get("built_at_commit"),
        "trust_boundary": {
            "EXTRACTED": "буквальные связи TSV/Markdown",
            "INFERRED": "курируемые indirect и непрямой фрагмент mixed",
            "status_effect": "нет; слой только навигационный",
        },
    }
    atomic_write(OVERLAY_MANIFEST, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def write_overlay_report(summary: dict[str, object], community: int, graph: dict[str, object]) -> str:
    text = f"""# Graphify — аудиторская навигация

Этот слой построен детерминированно из `PATTERN_ATLAS.tsv`,
`PATTERN_OQ_MAP.tsv`, `CLAIM_MATRIX.tsv`, `FINDINGS.tsv` и точных якорей
`OPEN_QUESTIONS.md`. Он не является каноном v14 и не меняет статусы ФТС.

## Покрытие

- {summary['patterns']} паттерн(ов) → {summary['open_questions']} действующих OQ;
- {summary['claims']} групп утверждений и {summary['findings']} находок аудита;
- {summary['programs']} программ, {summary['events']} событий и {summary['meta_patterns']} мета-паттерна;
- {summary['nodes']} новых узлов и {summary['edges']} новых рёбер.

## Доверие к мостам

- {summary['bridge_direct']} прямых мостов — `EXTRACTED`;
- {summary['bridge_indirect']} кураторских мостов — `INFERRED` с confidence 0.50;
- {summary['bridge_support']} служебных мостов — `EXTRACTED`, но без теоретической статусной силы.

`direct` восстанавливается буквально из `PATTERN_ATLAS.tsv`; `indirect` и
непрямая часть `mixed` остаются явными навигационными гипотезами. Граф предлагает
маршрут чтения, но не заменяет карточку, триплет, лист или аудиторский вердикт.

## Артефакты

- [Pattern Atlas](../work/v14_rebuild/audit/PATTERN_ATLAS.md)
- [Pattern ↔ OQ Map](../work/v14_rebuild/audit/PATTERN_OQ_MAP.md)
- [Claim Matrix](../work/v14_rebuild/audit/CLAIM_MATRIX.tsv)
- [Findings](../work/v14_rebuild/audit/FINDINGS.tsv)
- [Review Conclusion](../work/v14_rebuild/audit/REVIEW_CONCLUSION.md)

Состояние графа: {len(graph.get('nodes', []))} узлов, {len(graph.get('links', graph.get('edges', [])))} рёбер, community `{community}`.
"""
    atomic_write(OVERLAY_REPORT, text)
    return text


def write_graph_outputs(
    graph: dict[str, object],
    summary: dict[str, object],
    community: int,
    *,
    backup: bool,
) -> None:
    """Перегенерировать HTML и report без кластеризации и без LLM."""
    try:
        from graphify.analyze import god_nodes, surprising_connections
        from graphify.cluster import score_all
        from graphify.export import backup_if_protected, to_html
        from graphify.report import generate
        from networkx.readwrite import json_graph
    except ImportError as exc:
        raise RuntimeError("--inject требует runtime graphifyy; см. graphify-out/.graphify_python") from exc

    if backup:
        backup_if_protected(OUT_DIR)
    links_key = "links" if "links" in graph else "edges"
    try:
        graph_nx = json_graph.node_link_graph(graph, edges=links_key)
    except TypeError:  # NetworkX <= 3.1
        graph_nx = json_graph.node_link_graph(graph)
    graph_nx.graph["hyperedges"] = graph.get("hyperedges", [])
    communities: dict[int, list[str]] = defaultdict(list)
    for node_id, data in graph_nx.nodes(data=True):
        community_id = data.get("community")
        if not isinstance(community_id, int):
            community_id = 0
            data["community"] = community_id
        communities[community_id].append(node_id)

    labels = read_labels()
    labels[community] = "Аудит: закономерности ↔ OQ"
    detection = {"warning": "cluster-only mode — file stats not available"}
    cohesion = score_all(graph_nx, dict(communities))
    report = generate(
        graph_nx,
        dict(communities),
        cohesion,
        labels,
        god_nodes(graph_nx),
        surprising_connections(graph_nx, dict(communities)),
        detection,
        {"input": 0, "output": 0},
        ".",
        built_at_commit=graph.get("built_at_commit"),
        obsidian=True,
    )
    report += "\n\n## Audit Navigation Overlay (deterministic)\n\n"
    report += (
        f"- {summary['patterns']} patterns ↔ {summary['open_questions']} OQ; "
        f"{summary['claims']} claims; {summary['findings']} findings.\n"
        f"- Bridges: {summary['bridge_direct']} direct EXTRACTED; "
        f"{summary['bridge_indirect']} curated INFERRED; "
        f"{summary['bridge_support']} support EXTRACTED.\n"
        "- Boundary: this is navigation only; it neither amends the canon nor raises status.\n"
        "- See `AUDIT_NAVIGATION.md` and `audit_navigation_manifest.json`.\n"
    )
    atomic_write(GRAPH_PATH, json.dumps(graph, ensure_ascii=True, indent=2) + "\n")
    atomic_write(OUT_DIR / "GRAPH_REPORT.md", report)
    atomic_write(LABELS_PATH, json.dumps({str(key): value for key, value in labels.items()}, ensure_ascii=False) + "\n")
    to_html(graph_nx, dict(communities), str(OUT_DIR / "graph.html"), community_labels=labels)
    write_overlay_report(summary, community, graph)
    write_overlay_manifest(summary, community, graph)
    for generated in (
        GRAPH_PATH,
        OUT_DIR / "GRAPH_REPORT.md",
        LABELS_PATH,
        OUT_DIR / "graph.html",
        OVERLAY_REPORT,
        OVERLAY_MANIFEST,
    ):
        normalize_lf(generated)


def inject(fragment: dict[str, object], summary: dict[str, object]) -> None:
    if not GRAPH_PATH.is_file():
        raise FileNotFoundError(f"нет {rel(GRAPH_PATH)} — сперва собери базовый graphify-граф")
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    before_nodes = len(graph.get("nodes", []))
    before_edges = len(graph.get("links", graph.get("edges", [])))
    graph, community, added_nodes, added_edges, added_hyperedges = merge_fragment(graph, fragment)
    has_change = bool(added_nodes or added_edges or added_hyperedges)
    write_graph_outputs(graph, summary, community, backup=has_change)
    print(
        f"injected audit navigation -> GRAPH: {before_nodes}+{added_nodes}={len(graph['nodes'])} nodes, "
        f"{before_edges}+{added_edges}={len(graph.get('links', graph.get('edges', [])))} links, "
        f"{added_hyperedges} hyperedge, "
        f"community={community}"
    )


def verify(fragment: dict[str, object], summary: dict[str, object]) -> None:
    if not GRAPH_PATH.is_file():
        raise FileNotFoundError(f"нет {rel(GRAPH_PATH)}")
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    nodes = {str(item["id"]): item for item in graph.get("nodes", []) if isinstance(item, dict) and item.get("id")}
    required_nodes = {str(item["id"]) for item in fragment["nodes"]}  # type: ignore[index]
    missing = sorted(required_nodes - set(nodes))
    if missing:
        raise AssertionError(f"graph.json: не внесены узлы {missing[:5]} (всего {len(missing)})")
    links = list(graph.get("links", graph.get("edges", [])))
    link_index = {edge_key(item): item for item in links if isinstance(item, dict) and "source" in item and "target" in item}
    missing_edges = []
    wrong_confidence = []
    for item in fragment["edges"]:  # type: ignore[index]
        actual = link_index.get(edge_key(item))
        if actual is None:
            missing_edges.append(edge_key(item))
        elif actual.get("confidence") != item.get("confidence"):
            wrong_confidence.append((edge_key(item), actual.get("confidence"), item.get("confidence")))
    if missing_edges:
        raise AssertionError(f"graph.json: отсутствуют audit-рёбра {missing_edges[:5]} (всего {len(missing_edges)})")
    if wrong_confidence:
        raise AssertionError(f"graph.json: нарушена метка доверия {wrong_confidence[:3]}")
    expected = {"patterns": 31, "open_questions": 49, "claims": 25, "findings": 20}
    for key, value in expected.items():
        if summary[key] != value:
            raise AssertionError(f"неожиданное покрытие {key}: {summary[key]} != {value}")
    if not OVERLAY_REPORT.is_file() or not OVERLAY_MANIFEST.is_file():
        raise AssertionError("не созданы AUDIT_NAVIGATION.md или audit_navigation_manifest.json")
    print(
        f"AUDIT navigation verify: {len(required_nodes)} nodes and {len(fragment['edges'])} edges present; "
        f"{summary['bridge_direct']} direct EXTRACTED / {summary['bridge_indirect']} curated INFERRED"
    )


def main() -> int:
    args = sys.argv[1:]
    flags: set[str] = set()
    output: Path | None = None
    index = 0
    while index < len(args):
        arg = args[index]
        if arg in {"-h", "--help", "--stats", "--inject", "--verify"}:
            flags.add(arg)
            index += 1
            continue
        if arg == "--out":
            if output is not None or index + 1 >= len(args):
                raise SystemExit("--out требует ровно один путь")
            output = Path(args[index + 1])
            index += 2
            continue
        raise SystemExit(f"неизвестный аргумент: {arg}")
    if "-h" in flags or "--help" in flags:
        print(__doc__)
        return 0
    fragment, summary = build_fragment()
    print_summary(summary)
    if "--stats" in flags:
        return 0
    output = output or FRAGMENT_PATH
    atomic_write(output, json.dumps(fragment, ensure_ascii=False, indent=2) + "\n")
    print(f"fragment -> {output.relative_to(ROOT) if output.is_absolute() and output.is_relative_to(ROOT) else output}")
    if "--inject" in flags:
        inject(fragment, summary)
    if "--verify" in flags:
        verify(fragment, summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
