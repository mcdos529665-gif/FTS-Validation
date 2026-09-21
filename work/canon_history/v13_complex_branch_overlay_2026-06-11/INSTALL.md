# INSTALL / use

This is a plain-text LLM export. No installation is required.

Recommended upload order to another LLM:
1. `START_HERE.md`
2. `fts_cards.jsonl`
3. `fts_triples.tsv`
4. `FTS.yaml`
5. `FTS_v13_LLM_CONTEXT.md`
6. `FTS_v13_LLM_FULL_DUMP.md` or `fts_v13_workbook_sheets.json` only if full sheet-level detail is needed.

For graph work:
- Use `fts_cards.jsonl` as the entity source.
- Use `fts_triples.tsv` for compact subject/predicate/object graph.
- Use `fts_graph_full.tsv` if graph IDs, evidence IDs, comments, statuses, or internal references are needed.

For exact workbook reconstruction:
- Use `fts_v13_workbook_sheets.json`.
