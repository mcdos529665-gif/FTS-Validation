"""Точный импорт claim_graph и ассистентского слоя вопросов в навигацию Graphify.

Фрагмент сохраняет направления/предикаты; финализатор сохраняет его до проекции.
Вопросы и их связи имеют INFERRED/assistant_derived, без повышения St_FTS.
Запуск: python -X utf8 tools/graphify_question_edges.py --out-dir PATH
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path


def slug(value):
    return re.sub(r"[^a-z0-9]+", "_", str(value).lower()).strip("_")


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_fragment(root):
    root = Path(root).resolve()
    cq = root / "work/v14_rebuild/claim_questions"
    rel = "work/v14_rebuild/claim_questions/"
    graph = json.loads((root / "work/v14_rebuild/claim_graph/claim_graph.json").read_text(encoding="utf-8"))
    navmod = load_module(root / "tools/graphify_audit_navigation.py", "question_audit_navigation")
    navmod.configure_paths(root, root / "graphify-out")
    nav, _ = navmod.build_fragment()
    navids = {n["id"] for n in nav["nodes"]}
    registry = load_module(cq / "tools/sources.py", "question_source_registry")
    cards, checks, oq = registry.cards(), registry.checks(), registry.open_questions()
    nodes, edges, aliases, issues = {}, [], {}, []

    def add_node(n):
        previous = nodes.get(n["id"])
        if previous is not None and previous != n:
            raise ValueError(f"unresolved ID conflict: {n['id']}")
        nodes[n["id"]] = n
        return n["id"]

    def edge(source, target, relation, source_file, source_location, inferred=False, **extra):
        edges.append(dict(source=source, target=target, relation=relation,
                          confidence="INFERRED" if inferred else "EXTRACTED",
                          confidence_score=0.95 if inferred else 1.0,
                          source_file=source_file, source_location=source_location,
                          weight=1.0, navigation_only=True,
                          status_effect="no St_FTS change", **extra))

    # Canon and audit own their IDs. Preserve every other authoritative claim node.
    remap = {}
    for n in graph["nodes"]:
        kind = n["type"]
        field = {"card": "card_id", "claim": "claim_id", "claim_group": "claim_id", "pattern": "pattern_id", "finding": "finding_id", "open_question": "anchor", "verification": "verification_id"}.get(kind)
        key = n.get(field) if field else None
        if kind == "verification" and key:
            key = registry.normalize_check_id(key)
        if kind == "card":
            target = "source_fts_cards_" + n["card_id"].lower()
        else:
            prefix = {"pattern": "audit_pattern_", "claim_group": "audit_claim_", "finding": "audit_finding_", "open_question": "audit_oq_"}.get(kind)
            if kind == "open_question":
                key = n.get("anchor") or n.get("oq_anchor") or key or n["id"].removeprefix("oq_").replace("_", "-")
            possible = prefix + slug(key) if prefix and key else ""
            target = possible if possible in navids else "fts_claim_" + slug(n["id"])
        remap[n["id"]] = target
        for alias in (n["id"], key):
            if alias:
                if alias in aliases and aliases[alias] != target:
                    raise ValueError(f"ambiguous claim alias: {alias}")
                aliases[alias] = target
        if target.startswith("fts_claim_"):
            add_node({**n, "id": target, "file_type": "document" if kind == "source_document" else "concept",
                      "_origin": "claim_graph_import", "original_claim_graph_id": n["id"],
                      "navigation_only": True, "status_effect": "stored_only; no automatic promotion"})
    for n in graph["nodes"]:
        if n["type"] == "open_question":
            for value in re.findall(r"oq-[\w-]+", str(n)):
                if value in oq:
                    aliases[value] = remap[n["id"]]
    for e in graph["edges"]:
        edge(remap[e["source"]], remap[e["target"]], e["relation"], e.get("source_file"), e.get("source_location"),
             stored_confidence=e.get("confidence"), authoritative_edge=dict(e))
    for cid in cards:
        aliases[cid] = "source_fts_cards_" + cid.lower()
    # Complete OQ registry, including closed anchors not covered by the audit map.
    for anchor, value in oq.items():
        if anchor not in aliases:
            nid = "fts_oq_" + slug(anchor)
            aliases[anchor] = add_node(dict(id=nid, label=anchor + " · " + value["text"], type="open_question",
                file_type="concept", source_file="work/OPEN_QUESTIONS.md", source_location="anchor:" + anchor,
                oq_anchor=anchor, oq_status=value["status"], navigation_only=True))
    for check, value in checks.items():
        target = aliases.get(check)
        if not target:
            target = add_node(dict(id="fts_verification_" + slug(check), label=check + " · " + value["text"],
                type="verification", file_type="code", source_file=value["file"], source_location="check:" + check,
                check_id=check, navigation_only=True, status_effect="stored_only; no automatic promotion"))
        aliases[check] = target

    def rows(filename):
        with (cq / filename).open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f, delimiter="\t"))

    for i, g in enumerate(rows("inputs/groups.tsv"), 2):
        aliases[g["group_id"]] = add_node(dict(g, id="fts_question_group_" + slug(g["group_id"]), label=g["group_id"] + " · " + g["name"],
            type="question_group", file_type="concept", source_file=rel + "inputs/groups.tsv", source_location=f"L{i}",
            navigation_only=True, question_origin="assistant_derived"))
    for i, obj in enumerate(rows("inputs/objects.tsv"), 2):
        nid = add_node(dict(obj, id="fts_question_object_" + slug(obj["object_id"]), label=obj["object_id"] + " · " + obj["label"],
            type="question_object", file_type="concept", source_file=rel + "inputs/objects.tsv", source_location=f"L{i}", navigation_only=True))
        aliases[obj["object_id"]] = nid
        for ref in obj["defining_cards"].split():
            if ref not in aliases:
                raise ValueError(f"unknown object definition: {ref}")
            edge(nid, aliases[ref], "object_defined_in", rel + "inputs/objects.tsv", f"L{i}", True)
    qrows = [json.loads(line) for line in (cq / "QUESTION_CARDS.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    for i, q in enumerate(qrows, 1):
        aliases[q["question_id"]] = add_node(dict(q, id="fts_question_" + slug(q["question_id"]),
            label=q["question_id"] + " · " + q["question"], type="question", file_type="concept",
            source_file=rel + "QUESTION_CARDS.jsonl", source_location=f"L{i}", confidence="INFERRED", confidence_score=0.95,
            navigation_only=True, status_effect="no St_FTS change"))
    for i, q in enumerate(qrows, 1):
        src, location = aliases[q["question_id"]], f"L{i}"
        def qedge(target, relation, **kw):
            edge(src, target, relation, rel + "QUESTION_CARDS.jsonl", location, True, question_origin="assistant_derived", **kw)
        key = q.get("source_id") if q["layer"] == "assertion" else q["object_id"]
        if key not in aliases:
            raise ValueError(f"unknown question subject: {key}")
        qedge(aliases[key], "asks_about" if q["layer"] == "assertion" else "asks_about_object")
        qedge(aliases[q["primary_group"]], "in_group")
        for g in q["secondary_groups"]:
            qedge(aliases[g], "in_group_secondary")
        if q.get("parent_question_id"):
            qedge(aliases[q["parent_question_id"]], "derived_from", parent_relation=q.get("parent_relation"))
        for value in q["known_in_corpus"]:
            qedge(aliases[value], "known_in_corpus")
        for anchor in re.findall(r"oq-[\w-]+", q.get("answer_pointer") or ""):
            if anchor in oq and oq[anchor]["status"] == "x":
                qedge(aliases[anchor], "answered_by", answer_pointer=q["answer_pointer"])
        for kind, values in q["refs"].items():
            for value in values:
                if kind == "levels":
                    lev = int(value); key = "level:" + str(lev)
                    if key not in aliases:
                        nid = "fts_level_" + ("minus_" + str(-lev) if lev < 0 else str(lev))
                        card = "U_m1" if lev == -1 else f"U_{lev:02d}"
                        aliases[key] = add_node(dict(id=nid, label=f"У({lev})", type="level", level=lev, file_type="concept",
                            source_file="source/fts_cards.jsonl", source_location="card:" + card, navigation_only=True))
                        edge(nid, aliases[card], "has_card", "source/fts_cards.jsonl", "card:" + card)
                    target = aliases[key]
                elif value in aliases:
                    target = aliases[value]
                else:
                    key = f"reference:{kind}:{value}"
                    if key not in aliases:
                        safe = slug(value) or str(ord(str(value)[0]))
                        # Preserve Cyrillic dictionary/criterion identities without collisions.
                        safe = safe + "_" + str(value).encode("utf-8").hex()[:24]
                        exists = kind == "files" and (root / str(value)).is_file()
                        nid = "fts_reference_" + slug(kind) + "_" + safe
                        aliases[key] = add_node(dict(id=nid, label=str(value), type="source_reference" if exists else "term_reference",
                            file_type="document" if exists else "concept", source_file=str(value) if exists else rel + "QUESTION_CARDS.jsonl",
                            source_location="L1" if exists else location, resolution_state="source_file" if exists else "referenced_term_only",
                            navigation_only=True))
                        if not exists:
                            issues.append(dict(kind=kind, reference=value, state="referenced_term_only"))
                    target = aliases[key]
                qedge(target, "refers_to", reference_kind=kind)
    for i, x in enumerate(rows("QUESTION_CROSSREF.tsv"), 2):
        edge(aliases[x["question_id"]], aliases[x["open_question"]], "crossref_open_question", rel + "QUESTION_CROSSREF.tsv", f"L{i}", True,
             crossref_kind=x["relation"], note=x["note"], question_origin="assistant_derived")
    for i, x in enumerate(rows("inputs/oq_groups.tsv"), 2):
        target = aliases[x["oq_id"]]
        edge(target, aliases[x["primary_group"]], "in_group", rel + "inputs/oq_groups.tsv", f"L{i}", True)
        for group in re.findall(r"G\d{2}", x.get("secondary_groups", "")):
            edge(target, aliases[group], "in_group_secondary", rel + "inputs/oq_groups.tsv", f"L{i}", True)
    # Журнал держит ожидающие записи; после интеграции запись переносится в
    # DIALOGUE_NUANCE_SOURCES.md (цитата автора + integrated_at + targets).
    # Оба файла дают узлы dialogue_dn_*, статус берётся из того, где запись лежит.
    journal_path = "work/DIALOGUE_NUANCE_JOURNAL.md"
    sources_path = "work/DIALOGUE_NUANCE_SOURCES.md"
    dialogue_paths = {}
    for path, state in ((journal_path, "pending"), (sources_path, "integrated")):
        text = (root / path).read_text(encoding="utf-8")
        for match in re.finditer(r"^## (DN-\d+) · ([^\n]+)\n(.*?)(?=^## DN-|\Z)", text, re.M | re.S):
            jid, title, body = match.groups()
            if jid in aliases:
                continue
            line = text[:match.start()].count("\n") + 1
            quoted = "\n".join(x.strip()[2:] for x in body.splitlines() if x.strip().startswith("> "))
            fields = dict(re.findall(r"^- ([a-z_]+): (.*)$", body, re.M))
            nid = add_node(dict(id="dialogue_" + slug(jid), label=jid + " · " + title, type="author_statement", file_type="concept",
                source_file=path, source_location=f"L{line}", journal_id=jid, author_claim=quoted,
                accepted_meaning=fields.get("accepted_meaning"), assistant_inference=fields.get("assistant_inference"),
                integrated_at=fields.get("integrated_at"), status=state, navigation_only=True, status_effect="no St_FTS change"))
            aliases[jid] = nid
            dialogue_paths[jid] = path
            hints = fields.get("target_hints", "") + " " + fields.get("targets", "")
            targets = [cid for cid in cards if re.search(r"(?<![\w])" + re.escape(cid) + r"(?![\w])", hints)]
            if jid == "DN-0034":
                targets.extend(f"M_{i:02d}" for i in range(4, 8))
            targets.extend(oid for oid in re.findall(r"#(oq-[\w-]+)", hints) if oid in aliases)
            for cid in sorted(set(targets)):
                edge(nid, aliases[cid], "refers_to", path, f"L{line}")
            edge(nid, aliases["G14"], "in_group", rel + "QUESTION_GROUPS.tsv", "journal:" + jid, True)
            inference = fields.get("assistant_inference", "none")
            if inference != "none":
                inf = add_node(dict(id=nid + "_assistant_inference", label=jid + " · вывод ассистента", text=inference,
                    type="assistant_inference", file_type="concept", source_file=path, source_location=f"L{line}",
                    confidence="INFERRED", confidence_score=0.85, status=state, status_effect="no St_FTS change"))
                edge(nid, inf, "records_inference", path, f"L{line}", True)
    witness_file = "work/v14_rebuild/m_ops_check_2026-10-10.py"
    witness = add_node(dict(id="fts_verification_m_ops_20261010", label="Проверка операций ЛУ2…ЛУ7 (2026-10-10)", type="verification",
        file_type="code", source_file=witness_file, source_location="L1", status="candidate", registered_in_general_suite=False,
        reported_result="9 PASS; recorded in journal, not a promotion", status_effect="no St_FTS change"))
    for cid in ["M_04", "M_05", "M_06", "M_07", "U7_LOGIC_GROUPING"]:
        edge(witness, aliases[cid], "verifies", witness_file, "candidate witness")
    edge(aliases["DN-0034"], witness, "references", dialogue_paths["DN-0034"], "DN-0034")
    refuted_file = "work/REFUTED.md"
    refuted_lines = (root / refuted_file).read_text(encoding="utf-8").splitlines()
    refline = next(i for i, line in enumerate(refuted_lines, 1) if "Устаревшие предпосылки в слое вопросов" in line)
    refutation = add_node(dict(id="fts_refutation_question_premises_20261010", label="Устаревшие предпосылки в слое вопросов (2026-10-10)",
        text=refuted_lines[refline-1], type="refutation", file_type="concept", source_file=refuted_file, source_location=f"L{refline}",
        status_effect="question premises corrected; no St_FTS change"))
    for qid in ["Q-AF-012.2", "Q-AF-013.2", "Q-AF-013.3", "Q-AF-013.4", "Q-M_12.2"]:
        edge(refutation, aliases[qid], "corrects_premise", refuted_file, f"L{refline}")
    edge(refutation, aliases["oq-graph-dep-sync"], "references", refuted_file, f"L{refline}")
    unique = {}
    for e in edges:
        # Keep parallel predicates AND distinct source assertions of one predicate.
        key = (e["source"], e["relation"], e["target"], e.get("source_file"), e.get("source_location"), e.get("reference_kind"), e.get("crossref_kind"))
        unique.setdefault(key, e)
    fragment = dict(nodes=list(nodes.values()), edges=list(unique.values()), hyperedges=[], input_tokens=None, output_tokens=None)
    stats = dict(question_counts=dict(Counter(q["layer"] for q in qrows)), question_groups=14, question_objects=29,
                 authoritative_claim_nodes=len(graph["nodes"]), authoritative_claim_edges=len(graph["edges"]),
                 coverage=dict(Counter(q["corpus_coverage"] for q in qrows)), unresolved_term_references=issues,
                 nodes=len(nodes), edges=len(unique), duplicate_candidates_policy="81 candidate pairs retained in source; no similar_to edges inferred automatically")
    return fragment, stats, aliases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args()
    out = args.out_dir or args.project_root / "graphify-out"
    fragment, stats, aliases = build_fragment(args.project_root)
    out.mkdir(parents=True, exist_ok=True)
    for name, value in (("question_fragment.json", fragment), ("question_manifest.json", stats), ("question_aliases.json", aliases)):
        (out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False))


if __name__ == "__main__":
    main()
