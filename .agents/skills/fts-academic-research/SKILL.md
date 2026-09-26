---
name: fts-academic-research
description: Explicit FTS router for externally grounded academic research using Consensus, Semantic Scholar, a manual ResearchRabbit citation-graph round-trip, and optional separate Wolfram audit. Use only when the user explicitly invokes $fts-academic-research with a claim or OQ and mode quick, fact-check, lit-review, or systematic-review; apply it to prior-art searches, novelty checks, external evidence claims, systematic reviews, citation-network coverage, or proposed FTS status changes based on publications. Do not use it for local canon checks, editing, exports, or purely mathematical claims.
---

# FTS Academic Research

Route external evidence into FTS without importing external terminology or authority into the canon. Keep `source/` immutable and treat every publication as `[внешнее]` until the author makes a separate status decision.

## Required input

Require both an exact `claim` or OQ anchor and mode `quick`, `fact-check`, `lit-review`, or `systematic-review`. If either is missing, ask for it. Do not silently widen the question.

## Select the workflow

- `quick`: run a narrow Consensus discovery pass, fetch every result that may be cited, then verify identity in Semantic Scholar.
- `fact-check`: search supporting and contradicting evidence independently; record an evidence-bounded verdict, never a canon verdict.
- `lit-review`: use `$academic-research-suite` in its literature-review path after applying the FTS constraints below.
- `systematic-review`: freeze the protocol and Material Passport before discovery; maintain the E5 files; require two independent screening passes and explicit adjudication before synthesis.

Use `$academic-research-suite` directly for paper drafting or manuscript review. Do not activate ARS full-runtime, agent-team commands, or hooks.

## Apply the provider route

Read [provider-routing.md](references/provider-routing.md) before making provider calls.

1. Discover peer-reviewed candidates with Consensus. Fetch a result before citing it.
2. Resolve DOI/S2 ID and metadata with Semantic Scholar. Use `scripts/s2_verify.py`; start at one request per second and honor `429` plus `Retry-After`.
3. Deduplicate by normalized DOI, then S2 ID, then normalized title and year.
4. Export verified seeds to `seed_set.bib`. Ask the researcher to explore citations, references, and similar papers in ResearchRabbit and return BibTeX, RIS, or CSV.
5. Treat ResearchRabbit as discovery only, never as existence verification.
6. For an exact formula, domain, quantifier, branch, pole, or statistical expression, stop the literature route and advise a separate `$fts-wolfram-audit` call with a full claim/C-NN package.

Send only search strings and bibliographic metadata to external services by default. Do not send manuscripts, private notes, or the corpus without separate consent.

## Enforce FTS boundaries

- Label every non-canon inference `[внешнее]` and preserve the relation `direct|limiting|alternative|analogy`.
- Never raise `St_FTS`, `St_math`, or a claim status from a publication alone.
- Never equate an external term with an overloaded FTS term without a separately argued mapping.
- Record `нет в артефактах` when the local grounding is absent.
- Preserve `¬A ≠ 0_A ≠ −A`, register/channel/overlay distinctions, and all status gates from project instructions.
- Write active outputs only under `work/v14_rebuild/e5_literature_review/`; do not rewrite `work/v14_rebuild/audit/` or its historical `LITERATURE_MATRIX.tsv`.

## Record and screen

Read [records-and-gates.md](references/records-and-gates.md) for schemas and checkpoints. In systematic mode:

1. Complete and freeze `PROTOCOL.md` plus `MATERIAL_PASSPORT.yaml` before the first substantive search.
2. Append every query and candidate, including excluded and uncertain records.
3. Produce the Codex screening file without reading the researcher's decisions.
4. Have the researcher complete the second file from the same candidate set and criteria.
5. Reveal both files only at adjudication. Resolve every disagreement explicitly in `ADJUDICATION.tsv`.
6. Run `python -X utf8 .agents/skills/fts-academic-research/scripts/validate_e5_workspace.py work/v14_rebuild/e5_literature_review`.
7. Synthesize only adjudicated inclusions, include negative and limiting evidence, and state a bounded novelty boundary rather than world novelty.

Return findings in Russian in the project form: `Найдено → зависимости → вывод → что не закрыто.`
