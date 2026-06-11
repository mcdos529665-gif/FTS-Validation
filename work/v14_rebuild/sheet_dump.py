# -*- coding: utf-8 -*-
"""Точечный дамп листа workbook v13: python -X utf8 sheet_dump.py <имя_листа> [строки]"""
import io, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
wb = json.load(io.open(os.path.join(ROOT, "source", "fts_v13_workbook_sheets.json"), encoding="utf-8"))
name = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 999

for s in wb["sheets"]:
    if s.get("name") == name or s.get("sheet") == name:
        rows = s.get("values") or []
        for i, row in enumerate(rows[:limit]):
            cells = [str(c) if c is not None else "" for c in row] if isinstance(row, list) else [str(row)]
            line = " | ".join(cells).rstrip(" |")
            if line.strip():
                print(f"{i}: {line}")
        break
else:
    print("лист не найден; ключи примера:", json.dumps(wb["sheets"][0], ensure_ascii=False)[:200])
