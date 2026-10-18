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

1. `source/` is the editable active canon; write exploratory research in `work/`.
   Edit or replace canon when needed for the current task, without a separate
   author instruction or approval. Follow `PROJECT_INSTRUCTIONS.md#canon`.
   Правило автора 2026-10-18: если у кандидата нет альтернативы — писать в канон.
   Область, проверки, ограничения и происхождение сохранять; порядок — там же.
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
5. Avoid unintended byte changes; intentional canon edits are allowed. For Git:
   do not enable `core.autocrlf` or remove
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
| OpenResearch (`orx`) experiment, branch `orx/*` | [Experiment contract](experiments/AGENTS.md) — read first; write only `experiments/<slug>/` |

## Responses

For analysis: **Найдено → зависимости → вывод → что не закрыто.**
Report successful checks briefly; provide details on failure.

## Registers and canon-version comparisons

Registers of one level (M: minimal/logical expression, A: mathematical reading,
Ch: operational reading) refer to that level; consider their connections while
preserving their types.

- An author correction in one register leaves the others in force unless explicitly
  withdrawn. AC-2026-09-21 changes the logical U6/U7 forms; U7's mathematical
  reading `y=-x*x; y!=x*x` remains separately addressable.
- A discrepancy between registers creates a bridge obligation, not a missing ground.
- Judge withdrawal by the correction's explicit scope and dependency table. Text
  overwritten under the same card ID is a representation defect, not a withdrawal.
- Compare versions by level and register: explicitly revised / unaffected /
  overwritten in representation. Preserve the latter when integrating versions.
- Treat `local_forbid`, e.g. `y!=x*x`, as a structural part of the level (П5),
  rather than judging it only by its effect on the function value.
