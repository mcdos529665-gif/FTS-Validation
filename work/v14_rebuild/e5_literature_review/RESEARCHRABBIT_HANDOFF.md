# ResearchRabbit handoff · E5 wave 0

This is the one manual step in the citation-graph route. It is deliberately not
automated and it does not send any FTS manuscript, private note, or canon content.

1. In ResearchRabbit, create a collection named `FTS-E5-2026-07-20-W0`.
2. Import `seed_set.bib` without changing its seven DOI fields.
3. For each seed, inspect **references**, **citations**, and **similar papers**. Keep
   candidates only when they bear on one of Q01–Q10; do not treat a visual graph edge
   as proof that a paper exists or supports FTS.
4. Export the collection as BibTeX. Preserve the untouched provider export as
   `researchrabbit_export.bib` in this directory. If ResearchRabbit only provides
   RIS or CSV, retain that raw file beside it and state its filename in the next
   handoff; do not manufacture a BibTeX conversion in place of the raw export.
5. A second pass is optional in the current cycle. If it is offered as an
   independent check, do not expose Codex decisions before completing the frozen
   set in `SCREENING_RESEARCHER.tsv`; the same person or AI may perform that
   blinded replay. If the first decisions are known, record the result as
   `unblinded_replay`, not independent screening. Add graph-derived records as a
   clearly labelled next wave.

The validator will reject an export that drops any DOI from `seed_set.bib`.
Disagreements with `SCREENING_CODEX.tsv` must remain unexamined until an explicit
row is entered in `ADJUDICATION.tsv`.
