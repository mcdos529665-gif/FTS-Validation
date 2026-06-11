# -*- coding: utf-8 -*-
"""Сверка ссылок статьи v14 с полным каноном v13 (после import_from)."""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

cards = {}
with io.open(os.path.join(ROOT, "source", "fts_cards.jsonl"), encoding="utf-8") as f:
    for l in f:
        if l.strip():
            c = json.loads(l)
            cards[c.get("id")] = c

section = sys.argv[1] if len(sys.argv) > 1 else "grounds"

def show(c, fields=None):
    if not c:
        print("  (нет карточки)"); return
    fields = fields or [k for k in c.keys() if k != "id"]
    print(f"== {c['id']} ==")
    for k in fields:
        v = c.get(k)
        if v not in (None, "", []):
            print(f"  {k}: {v}")

if section == "keys":
    any_card = next(iter(cards.values()))
    print(sorted(any_card.keys()))
    # показать пример уровневой карточки целиком
    show(cards.get("U_07"))

elif section == "grounds":
    for i in range(1, 21):
        cid = f"O_{i:02d}"
        c = cards.get(cid)
        if c:
            print(f"{cid} | {c.get('status','')} | {c.get('title','')}")
            txt = c.get("text") or c.get("summary") or c.get("body") or ""
            if txt:
                print(f"     {str(txt)[:300]}")

elif section == "levels":
    for cid in ["U_07", "U_08", "U_09", "U_10", "U_11", "U_12", "U_13", "U_14", "U_15"]:
        show(cards.get(cid))
        print()

elif section == "sp":
    for cid, c in cards.items():
        if c.get("type") == "status_promotion" or (cid or "").startswith("SP_"):
            show(c); print()

elif section == "minexpr":
    for cid, c in sorted(cards.items()):
        if c.get("type") in ("minimal_expression",):
            print(f"{cid} | {c.get('title','')} | {c.get('text','')}"[:240])

elif section == "fails":
    for cid, c in cards.items():
        if c.get("type") in ("failure_condition", "test"):
            show(c); print()

elif section == "find":
    needle = sys.argv[2]
    for cid, c in cards.items():
        blob = json.dumps(c, ensure_ascii=False)
        if needle.lower() in blob.lower():
            print(f"--- {cid} | {c.get('type','')} | {c.get('title','')[:80]}")
