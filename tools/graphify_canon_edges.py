"""graphify_canon_edges.py - препроцессор: канон v13 -> EXTRACTED-рёбра для graphify.

Читает  source/fts_cards.jsonl  (161 карточка: id, depends_on, symbol, title, type, ...)
        source/fts_triples.tsv   (238 триплетов: subject  predicate  object)
и превращает КАНОНИЧЕСКУЮ структуру (depends_on, has_next, has_minimal_expression,
has_private_expression, projects_to, supports, has_operator, оверлеи, ...) в граф-
фрагмент {nodes, edges} с confidence = EXTRACTED (1.0) — без единой LLM-догадки.

Зачем это нужно
--------------
LLM-экстракция graphify из fts_cards.json недобирает рёбра: плоский JSON-массив
карточек почти не нарративен, поэтому связи между карточками теряются, узлы-
карточки повисают изолированными. Но канон УЖЕ содержит готовый edge-list
(fts_triples.tsv + поле depends_on). Этот тул инжектит его как EXTRACTED-слой —
плотный, канон-backed, без догадок и без узлов-двойников.

Выравнивание ID (важно!)
------------------------
Узлы именуются  source_fts_cards_<id-в-нижнем-регистре>  — ровно та схема, что
graphify присваивает карточкам при экстракции source/fts_cards.json (parent-dir
'source' + stem 'fts_cards' + entity). Поэтому канон-рёбра ложатся на СУЩЕСТВУЮЩИЕ
узлы графа (проверено: 161/161 совпадают), а не плодят двойники. Если graphify
сменит соглашение об ID — синхронизировать NODE_PREFIX ниже.

Резолвер алиасов
----------------
Канон местами ссылается на гранды без zero-padding: O2, O12, O(8). Резолвер
приводит O<n> / O(<n>) -> O_<nn> (напр. O2 -> O_02). Всё, что не резолвится в
карточку (окна-литералы (3,4,5,6,7); *.md; некарточные OP_*; висячие SP_*),
ПРОПУСКАЕТСЯ и логируется по причинам — не молча (см. no-smuggling / гардрейлы).

Usage (из корня репозитория; на Windows-консоли добавляй -X utf8):
  python -X utf8 tools/graphify_canon_edges.py            # -> graphify-out/canon_fragment.json + сводка
  python -X utf8 tools/graphify_canon_edges.py --stats    # только сводка, ничего не пишет
  python -X utf8 tools/graphify_canon_edges.py --out P    # свой путь вывода фрагмента
  python -X utf8 tools/graphify_canon_edges.py --inject   # влить фрагмент в graphify-out/graph.json,
                                                          #   рекластеризовать, перегенерить GRAPH_REPORT.md
                                                          #   (ТРЕБУЕТ graphify; затем: graphify export html)

Только stdlib для emit/--stats. graphify импортируется ЛЕНИВО и только для --inject.
"""
import json
import os
import re
import sys
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source")
CARDS = os.path.join(SRC, "fts_cards.jsonl")
TRIPLES = os.path.join(SRC, "fts_triples.tsv")
OUT_DIR = os.path.join(ROOT, "graphify-out")

# Должно совпадать с соглашением graphify об ID для source/fts_cards.json.
NODE_PREFIX = "source_fts_cards_"


def load_cards():
    if not os.path.exists(CARDS):
        sys.exit(f"нет в артефактах: {CARDS} — распакуй канон в source/ и прогони tools/verify.py")
    out = {}
    with open(CARDS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                c = json.loads(line)
                out[c["id"]] = c
    return out


def load_triples():
    edges = []
    if not os.path.exists(TRIPLES):
        return edges
    with open(TRIPLES, encoding="utf-8") as f:
        next(f, None)  # header: subject  predicate  object
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3:
                edges.append((p[0], p[1], p[2]))
    return edges


def nid(cid):
    """Card id -> graphify node id (must match graphify's fts_cards.json convention)."""
    return NODE_PREFIX + cid.lower()


def make_resolver(ids):
    """Return resolve(ref) -> real card id or None. Handles O<n>/O(<n>) -> O_<nn> aliases."""
    def resolve(ref):
        if ref in ids:
            return ref
        m = re.fullmatch(r"O\(?(\d+)\)?", ref)
        if m:
            n = int(m.group(1))
            for cand in (f"O_{n:02d}", f"O_{n}"):
                if cand in ids:
                    return cand
        return None
    return resolve


def build_fragment(cards, triples):
    """Return (nodes, edges, summary). Pure: no graphify, no I/O."""
    ids = set(cards)
    resolve = make_resolver(ids)

    nodes = [{
        "id": nid(cid),
        "label": (c.get("symbol", "") + " " + c.get("title", "")).strip() or cid,
        "file_type": "concept",
        "source_file": "source/fts_cards.jsonl",
        "source_location": c.get("path"),
        "source_url": None, "captured_at": None, "author": None, "contributor": None,
    } for cid, c in cards.items()]

    edges = []
    seen = set()
    skipped = collections.Counter()
    recovered = 0

    def add(s_id, pred, o_id, prov):
        key = (s_id, pred, o_id)
        if key in seen:
            return
        seen.add(key)
        edges.append({
            "source": nid(s_id), "target": nid(o_id), "relation": pred,
            "confidence": "EXTRACTED", "confidence_score": 1.0,
            "source_file": prov, "source_location": None, "weight": 1.0,
        })

    # 1) triples (subject predicate object)
    for s, pred, o in triples:
        rs, ro = resolve(s), resolve(o)
        if rs is None:
            skipped["bad_subject"] += 1
            continue
        if ro is None:
            skipped["literal_or_uncarded_object"] += 1
            continue
        if o not in ids:
            recovered += 1
        add(rs, pred, ro, "source/fts_triples.tsv")

    # 2) card depends_on (в каноне богаче, чем depends_on-триплеты; объединяем)
    for cid, c in cards.items():
        for d in (c.get("depends_on") or []):
            rd = resolve(d)
            if rd is None:
                skipped["dangling_dep"] += 1
                continue
            if d not in ids:
                recovered += 1
            add(cid, "depends_on", rd, "source/fts_cards.jsonl")

    summary = {
        "nodes": len(nodes),
        "edges": len(edges),
        "alias_recovered": recovered,
        "skipped": dict(skipped),
        "by_predicate": collections.Counter(e["relation"] for e in edges),
    }
    return nodes, edges, summary


def print_summary(summary):
    print(f"CANON fragment: {summary['nodes']} nodes, {summary['edges']} edges "
          f"(alias-recovered: {summary['alias_recovered']})")
    print(f"  skipped (logged, not silent): {summary['skipped']}")
    print("  edges by predicate:")
    for pr, k in summary["by_predicate"].most_common():
        print(f"    {k:3}  {pr}")


def inject(nodes, edges):
    """Влить фрагмент в graphify-out/graph.json, рекластеризовать, перегенерить отчёт.

    Требует graphify (импорт ленивый). Auto-лейблы (по самому связному узлу) —
    чтобы шаг был воспроизводим без ручной разметки. HTML не трогает: после
    выполнить `graphify export html`.
    """
    try:
        from graphify.build import build_from_json
        from graphify.cluster import cluster, score_all
        from graphify.analyze import god_nodes, surprising_connections, suggest_questions
        from graphify.report import generate
        from graphify.export import to_json
    except ImportError:
        sys.exit("--inject требует graphify (pip/uv tool install graphifyy). "
                 "Для чистого фрагмента используй режим по умолчанию (emit).")

    gpath = os.path.join(OUT_DIR, "graph.json")
    if not os.path.exists(gpath):
        sys.exit(f"нет {gpath} — сперва собери базовый граф: /graphify .")
    g = json.loads(open(gpath, encoding="utf-8").read())
    links = g.get("links", g.get("edges", []))

    # существующий граф -> extraction-формат, затем + канон-фрагмент (dedupe узлов по id)
    seen, merged_nodes = set(), []
    for n in g.get("nodes", []) + nodes:
        if n["id"] not in seen:
            seen.add(n["id"])
            merged_nodes.append(n)
    extraction = {
        "nodes": merged_nodes,
        "edges": [dict(e) for e in links] + edges,
        "hyperedges": g.get("hyperedges", []),
        "input_tokens": 0, "output_tokens": 0,
    }

    G = build_from_json(extraction)
    communities = cluster(G)
    cohesion = score_all(G, communities)
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)

    # auto-лейблы: имя самого связного узла сообщества (воспроизводимо)
    lab = {n["id"]: n.get("label", n["id"]) for n in merged_nodes}
    deg = collections.Counter()
    for e in extraction["edges"]:
        deg[e.get("source")] += 1
        deg[e.get("target")] += 1
    labels = {}
    for cid, members in communities.items():
        top = max(members, key=lambda i: deg.get(i, 0))
        s = re.split(r"\s[—-]\s|\s\(", lab.get(top, str(top)))[0].strip()
        labels[cid] = " ".join(s.split()[:5]) or str(top)

    questions = suggest_questions(G, communities, labels)
    detection = {"total_files": None, "total_words": None}
    report = generate(G, communities, cohesion, labels, gods, surprises,
                      detection, {"input": 0, "output": 0}, ".", suggested_questions=questions)
    open(os.path.join(OUT_DIR, "GRAPH_REPORT.md"), "w", encoding="utf-8").write(report)
    to_json(G, communities, gpath, force=True)
    open(os.path.join(OUT_DIR, ".graphify_labels.json"), "w", encoding="utf-8").write(
        json.dumps({str(k): v for k, v in labels.items()}, ensure_ascii=False))
    iso = sum(1 for n in G.nodes() if G.degree(n) <= 1)
    print(f"injected -> GRAPH: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, "
          f"{len(communities)} communities, {iso} isolated(<=1)")
    print("HTML не обновлён — выполни: graphify export html")


def main():
    args = sys.argv[1:]
    do_stats = "--stats" in args
    do_inject = "--inject" in args
    out_path = None
    if "--out" in args:
        i = args.index("--out")
        if i + 1 < len(args):
            out_path = args[i + 1]

    cards = load_cards()
    triples = load_triples()
    nodes, edges, summary = build_fragment(cards, triples)
    print_summary(summary)

    if do_inject:
        inject(nodes, edges)
        return
    if do_stats:
        return

    out_path = out_path or os.path.join(OUT_DIR, "canon_fragment.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"nodes": nodes, "edges": edges, "hyperedges": []}, f, ensure_ascii=False, indent=2)
    print(f"\nfragment -> {os.path.relpath(out_path, ROOT)}")


if __name__ == "__main__":
    main()
