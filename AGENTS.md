# AGENTS — FTS working contract

FTS research lives in `work/`; the main text is
`work/v14_rebuild/FTS_v14_paper.md`. Python provides access and checks.
Reply in plain Russian, with examples when useful. Follow explicit language requests.

## Startup

- Read `work/STATE.md` once before substantive FTS work and `work/notation.md`
  before substantive analysis.
- These rules are already supplied in context; do not reread `AGENTS.md`.
  Reread other files only if relevant content changed or needed context was lost.
  Simple questions, links, small editorial changes, and app configuration do not
  require STATE, notation, or the procedure reference.
- Select further reading from the table; do not recursively follow links.

## Standing rules

1. `source/` is the active canon; write research in `work/`. An explicit author
   instruction to correct/replace the canon authorizes the actual replacement
   without repeated approval; follow `PROJECT_INSTRUCTIONS.md#canon`.
2. Take FTS terms from its artifacts. Ground substantive conclusions in a
   card/triple/sheet or mark them `[внешнее]`. In a conflict, canon defines FTS
   content; record the discrepancy in `work/EXTERNAL_CONFLICTS.md`.
   Missing grounding: `нет в артефактах`.
3. The M-register is the minimal expression projection; the Ch-register is
   operational reading (Dist₃, Select, Agg, K). Preserve exact formulas and grouping.
   `branch access ≠ Lift`; `array ≠ tensor` without a transformation law.
   Distinguish registers from overlays; justify local equivalences within a stated scope.
4. Author acceptance, mathematical proof, and `St_FTS` are distinct. Promotion
   requires SP/К1–К5 with evidence appropriate to the claim type and a graph record.
   `SP_LIMITS` records revisable evidence gaps. A verified counterexample withdraws
   the affected math fact; a technical FAIL needs diagnosis. See procedure `status`.
5. Preserve canon and primary-source bytes: do not enable `core.autocrlf` or remove
   `-text` from `source/`, TSV, or JSONL. Run Python with `-X utf8`.
6. Save work to disk; commit coherent results using only task files. Keep `STATE.md`
   to the current point and links, without retelling history. File roles and size
   guidelines: `work/DOCUMENT_MAP.md`. For a small edit, review the diff and affected
   result once; batch independent checks. Update STATE/journals only when the task,
   conclusion, or next step changes.

## Task-specific reading

| Task | Read |
|---|---|
| Canon revision | [Replacement procedure](PROJECT_INSTRUCTIONS.md#canon) |
| Evidence / status / FAIL | [Status procedure](PROJECT_INSTRUCTIONS.md#status) |
| Substantive mathematical conclusion | [Wolfram check](PROJECT_INSTRUCTIONS.md#wolfram) |
| External scientific grounding | [Academic research](PROJECT_INSTRUCTIONS.md#academic) |
| Commands or verification | [Commands](PROJECT_INSTRUCTIONS.md#commands), [checks](PROJECT_INSTRUCTIONS.md#checks) |
| Graph / arXiv / completing work | Sections `graph` / `arxiv` / `save` in `PROJECT_INSTRUCTIONS.md` |
| Where to write new material | [Document map](work/DOCUMENT_MAP.md) |

## Responses

For analysis: **Найдено → зависимости → вывод → что не закрыто.**
Report successful checks briefly; provide details on failure.
