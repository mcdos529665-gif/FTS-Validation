"""query.py - local retrieval over the FTS v13 canon (no DB required).

Reads:  source/fts_cards.jsonl   (entities: id,type,text,depends_on,tags,path,status,internal_ref,symbol,title)
        source/fts_triples.tsv    (graph: subject  predicate  object)

The point of this tool: never load the whole theory into an LLM context.
Pull only the cards/edges relevant to the current task.

Usage (from project root):
  python tools/query.py card  <ID>            full card + its outgoing/incoming edges
  python tools/query.py find  <substr>        cards whose text/title/symbol contains substr (case-insensitive)
  python tools/query.py type  <TYPE>          list cards of a type        (e.g. level, axiom, operator)
  python tools/query.py status <STATUS>       list cards by status substring (e.g. canonical_strict, candidate)
  python tools/query.py tag   <TAG>           list cards carrying a tag
  python tools/query.py neighbors <ID> [hops] subgraph around ID (default 1 hop)
  python tools/query.py deps  <ID>            transitive depends_on closure of ID
  python tools/query.py stats                 counts by type and status
  python tools/query.py context <ID> [hops]   compact bundle (card + neighborhood cards) ready to paste into a session
"""
import json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source")
CARDS = os.path.join(SRC, "fts_cards.jsonl")
TRIPLES = os.path.join(SRC, "fts_triples.tsv")


def load_cards():
    if not os.path.exists(CARDS):
        sys.exit(f"missing {CARDS} - place the package into source/ and run tools/verify.py")
    out = {}
    with open(CARDS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            c = json.loads(line)
            out[c["id"]] = c
    return out


def load_triples():
    edges = []
    if not os.path.exists(TRIPLES):
        return edges
    with open(TRIPLES, encoding="utf-8") as f:
        next(f, None)  # header
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                edges.append((parts[0], parts[1], parts[2]))
    return edges


def fmt(c):
    return (f"[{c['id']}] {c.get('symbol','')} {c.get('title','')}".rstrip()
            + f"\n  type={c.get('type')}  status={c.get('status')}"
            + (f"  deps={c['depends_on']}" if c.get('depends_on') else "")
            + (f"  tags={c.get('tags')}" if c.get('tags') else "")
            + f"\n  {c.get('text','')}")


def cmd_card(cards, edges, cid):
    if cid not in cards:
        sys.exit(f"нет в артефактах: {cid}")
    print(fmt(cards[cid]))
    out = [(p, o) for s, p, o in edges if s == cid]
    inc = [(s, p) for s, p, o in edges if o == cid]
    if out:
        print("\n  -- outgoing --")
        for p, o in out:
            print(f"     {p} -> {o}")
    if inc:
        print("\n  -- incoming --")
        for s, p in inc:
            print(f"     {s} -> {p}")


def cmd_find(cards, sub):
    s = sub.lower()
    for c in cards.values():
        blob = " ".join(str(c.get(k, "")) for k in ("id", "title", "symbol", "text"))
        if s in blob.lower():
            print(fmt(c)); print()


def cmd_type(cards, t):
    for c in cards.values():
        if c.get("type") == t:
            print(f"[{c['id']}] {c.get('symbol','')} {c.get('title','')}  ({c.get('status')})")


def cmd_status(cards, st):
    for c in cards.values():
        if st.lower() in str(c.get("status", "")).lower():
            print(f"[{c['id']}] {c.get('type')}: {c.get('title','')}  <{c.get('status')}>")


def cmd_tag(cards, tag):
    for c in cards.values():
        if tag in (c.get("tags") or []):
            print(f"[{c['id']}] {c.get('type')}: {c.get('title','')}")


def cmd_neighbors(cards, edges, cid, hops):
    seen = {cid}
    frontier = {cid}
    for _ in range(hops):
        nxt = set()
        for s, p, o in edges:
            if s in frontier:
                nxt.add(o)
            if o in frontier:
                nxt.add(s)
        frontier = nxt - seen
        seen |= nxt
    for s, p, o in edges:
        if s in seen and o in seen:
            print(f"{s}  {p}  {o}")


def cmd_deps(cards, cid):
    seen, order = set(), []
    def walk(x):
        for d in cards.get(x, {}).get("depends_on", []) or []:
            if d not in seen:
                seen.add(d); walk(d); order.append(d)
    walk(cid)
    for d in order:
        c = cards.get(d)
        print(f"[{d}] {c.get('title','') if c else 'нет в артефактах'}")


def cmd_stats(cards):
    by_t = collections.Counter(c.get("type") for c in cards.values())
    by_s = collections.Counter(c.get("status") for c in cards.values())
    print(f"cards: {len(cards)}\n-- by type --")
    for k, v in by_t.most_common():
        print(f"  {v:3}  {k}")
    print("-- by status --")
    for k, v in by_s.most_common():
        print(f"  {v:3}  {k}")


def cmd_context(cards, edges, cid, hops):
    seen = {cid}; frontier = {cid}
    for _ in range(hops):
        nxt = set()
        for s, p, o in edges:
            if s in frontier: nxt.add(o)
            if o in frontier: nxt.add(s)
        frontier = nxt - seen; seen |= nxt
    print(f"=== CONTEXT BUNDLE for {cid} ({hops} hop[s]) ===")
    for x in sorted(seen):
        if x in cards:
            print(fmt(cards[x])); print()


def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    cmd = sys.argv[1]; args = sys.argv[2:]
    cards = load_cards(); edges = load_triples()
    if cmd == "card" and args: cmd_card(cards, edges, args[0])
    elif cmd == "find" and args: cmd_find(cards, " ".join(args))
    elif cmd == "type" and args: cmd_type(cards, args[0])
    elif cmd == "status" and args: cmd_status(cards, args[0])
    elif cmd == "tag" and args: cmd_tag(cards, args[0])
    elif cmd == "neighbors" and args: cmd_neighbors(cards, edges, args[0], int(args[1]) if len(args) > 1 else 1)
    elif cmd == "deps" and args: cmd_deps(cards, args[0])
    elif cmd == "stats": cmd_stats(cards)
    elif cmd == "context" and args: cmd_context(cards, edges, args[0], int(args[1]) if len(args) > 1 else 1)
    else: print(__doc__)


if __name__ == "__main__":
    main()
