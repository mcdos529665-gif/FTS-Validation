"""Inspect recorded research addresses; do not infer proof or repair the graph."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

try:
    from .claim_graph import validate_graph
except ImportError:
    from claim_graph import validate_graph

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "work/v14_rebuild/claim_graph/claim_graph.json"
OUT = ROOT / "work/project_consistency"

# A claim cannot inherit a subject through a shared check, document or status.
# Evidence maps may be followed only in their recorded direction and scope.
OUTGOING = {
    "depends_on", "grounds_claim", "supports", "candidate_supports", "projects_to",
    "applies_to", "uses_analogy", "asks_branch_of", "defeats_or_tests",
    "promotes_status_of", "supported_by", "maps_to", "supports_claim", "limits_claim",
    "has_minimal_expression", "has_private_expression", "has_math_expression",
    "has_statistical_overlay", "has_complex_overlay", "has_tensor_overlay",
    "has_operator", "has_core", "has_antimode", "has_antimode_detail", "has_boundary",
    "has_local_forbid", "has_agentic_gate", "has_author_logical_expression",
    "has_author_scope_clarification", "has_author_expectation_clarification",
}
OWNERSHIP = {
    "has_minimal_expression", "has_private_expression", "has_math_expression",
    "has_statistical_overlay", "has_complex_overlay", "has_tensor_overlay",
    "has_operator", "has_core", "has_antimode", "has_antimode_detail", "has_boundary",
    "has_local_forbid", "has_agentic_gate", "has_author_logical_expression",
    "has_author_scope_clarification", "has_author_expectation_clarification",
}
ASSERTION_TYPES = {"card", "author_statement", "claim", "claim_group"}
BLOCKED_TYPES = {"source_document", "status_assessment", "source_reference",
                 "unresolved_reference", "literal", "verification", "finding", "project"}
AUXILIARY_IDS = {"ADD_NOTATION_ABS", "ADD_RESEARCH_FORMAT", "CM-019"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def address_routes(graph: dict, entity: dict) -> list[dict]:
    nodes = {node["id"]: node for node in graph["nodes"]}
    by_card = {node["card_id"]: node["id"] for node in nodes.values()
               if node["type"] == "card" and node.get("card_id")}
    anchors = defaultdict(set)
    for category in entity["scope_categories"]:
        for card_id in category["anchor_card_ids"]:
            anchors[by_card[card_id]].add(category["id"])
    # Existing explicit range objects are addresses; document collections are not.
    for node in nodes.values():
        if node["type"] == "scope" and node.get("layer") != "project_definition":
            if node.get("members") and all(member in by_card for member in node["members"]):
                anchors[node["id"]].add("ladder")
    adjacency = defaultdict(list)
    for edge in graph["edges"]:
        if edge["layer"] == "project_definition":
            continue
        source, target = nodes[edge["source"]], nodes[edge["target"]]
        if source["type"] in BLOCKED_TYPES or target["type"] in BLOCKED_TYPES:
            continue
        if edge["relation"] in OUTGOING:
            adjacency[source["id"]].append((target["id"], edge, "forward"))
        if edge["relation"] in OWNERSHIP:
            adjacency[target["id"]].append((source["id"], edge, "owner"))
        if edge["relation"] == "depends_on" and source["type"] in {"card", "author_statement"} and target["type"] in {"card", "author_statement"}:
            # The prerequisite contributes to its explicit dependent's subject.
            # This is address tracing, not a reversed proof implication.
            adjacency[target["id"]].append((source["id"], edge, "prerequisite_of"))
    result = []
    for node in sorted(nodes.values(), key=lambda item: item["id"]):
        if node["type"] not in ASSERTION_TYPES:
            continue
        record_id = node.get("card_id") or node.get("claim_id") or node["id"]
        queue = deque([(node["id"], [])])
        seen = {node["id"]}
        route, anchor = None, ""
        while queue:
            current, path = queue.popleft()
            if current in anchors:
                route, anchor = path, current
                break
            for next_id, edge, direction in sorted(adjacency[current], key=lambda item: item[1]["id"]):
                if next_id not in seen:
                    seen.add(next_id)
                    queue.append((next_id, path + [{"edge": edge["id"], "relation": edge["relation"],
                                  "direction": direction, "source_file": edge["source_file"],
                                  "source_location": edge.get("source_location", ""),
                                  "scope": edge.get("scope", ""), "confidence": edge.get("confidence", ""),
                                  "status_effect": edge.get("status_effect", ""),
                                  "rationale": edge.get("rationale", "")}]))
        address_state = "recorded_route" if route is not None else "no_recorded_route"
        if record_id in AUXILIARY_IDS:
            address_state = "auxiliary_record"
        elif node.get("status") == "assistant_formalization_not_adopted":
            address_state = "unadopted_formalization"
        result.append({
            "node_id": node["id"], "record_id": record_id, "type": node["type"],
            "layer": node["layer"], "label": node["label"],
            "address_state": address_state,
            "scope_categories": ";".join(sorted(anchors[anchor])) if anchor else "",
            "anchor": anchor, "route": json.dumps(route or [], ensure_ascii=False, separators=(",", ":")),
            "source_file": node.get("source_file", ""), "source_location": node.get("source_location", ""),
            "granularity": node.get("granularity", "card" if node["type"] in {"card", "author_statement"} else "statement"),
            "interpretation": "address trace only; source/role/domain/evidence require semantic review; no status promotion",
        })
    return result


def document_kind(path: str) -> str:
    parts = Path(path).parts
    if "export" in parts or path.startswith(("graphify-out/", "source/")):
        return "derived_or_navigation"
    if "canon_history" in parts or any(part.endswith("_history") for part in parts):
        return "historical"
    if "papers" in parts or "arxiv" in parts or "inputs" in parts:
        return "external_source"
    if path.startswith((".agents/", "work/project_consistency/", "work/author_canon/")):
        return "procedure_or_provenance"
    if path.startswith("work/v14_rebuild/audit/"):
        return "audit_support"
    if path.startswith("work/v14_rebuild/claim_graph/"):
        return "graph_support"
    return "active_research" if path.startswith("work/") else "project_description_or_procedure"


def document_inventory(graph: dict) -> list[dict]:
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0")
    inputs = {item["path"] for item in graph["input_digests"]}
    card_ids = [node["card_id"] for node in graph["nodes"] if node["type"] == "card"]
    card_regex = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(re.escape(item) for item in sorted(card_ids, key=len, reverse=True)) + r")(?![A-Za-z0-9_])")
    result = []
    for relative in sorted(set(tracked)):
        if not relative.endswith(".md") or relative.startswith("work/project_consistency/RESEARCH_SCOPE_"):
            continue
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        result.append({
            "path": relative, "kind": document_kind(relative), "graph_input": str(relative in inputs).lower(),
            "literal_card_mentions": ";".join(sorted(set(card_regex.findall(text)))),
            "level_mentions": ";".join(sorted(set(re.findall(r"У\s*\(?-?\d{1,2}\)?", text)))),
            "sha256": digest(path),
            "interpretation": "literal mentions are a screening aid, not a semantic address or proof",
        })
    return result


def write_tsv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write dated scope inventories; never repair source or graph")
    args = parser.parse_args()
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    validate_graph(graph)
    entity = json.loads((ROOT / "PROJECT.json").read_text(encoding="utf-8"))
    rows = address_routes(graph, entity)
    documents = document_inventory(graph)
    counters = {kind: dict(Counter(row["address_state"] for row in rows if row["type"] == kind))
                for kind in sorted(ASSERTION_TYPES)}
    summary = {
        "project_id": entity["project_id"], "graph_sha256": digest(GRAPH),
        "generator": "tools/audit_research_scope.py", "generator_sha256": digest(Path(__file__)),
        "project_entity_sha256": digest(ROOT / "PROJECT.json"),
        "assertion_records": len(rows), "by_type": counters,
        "documents": len(documents), "document_kinds": dict(Counter(row["kind"] for row in documents)),
        "active_research_documents": sum(row["kind"] == "active_research" for row in documents),
        "active_research_documents_outside_graph_inputs": sum(
            row["kind"] == "active_research" and row["graph_input"] == "false" for row in documents),
        "unrouted_records": [row["record_id"] for row in rows if row["address_state"] == "no_recorded_route"],
        "groups_require_atomization": sum(row["granularity"] == "group" for row in rows),
        "scope_of_verdict": "recorded address traces plus document inventory; not all atomic propositions",
        "full_semantic_conformance_proved": False,
        "shared_check_document_status_or_project_edges_used_as_ground": False,
    }
    if args.write:
        OUT.mkdir(parents=True, exist_ok=True)
        date = entity["recorded_on"]
        write_tsv(OUT / f"RESEARCH_SCOPE_ASSERTIONS_{date}.tsv", rows)
        write_tsv(OUT / f"RESEARCH_SCOPE_DOCUMENTS_{date}.tsv", documents)
        (OUT / f"RESEARCH_SCOPE_COUNTS_{date}.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
