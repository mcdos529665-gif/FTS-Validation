---
name: fts-graph-guide
description: Explain FTS claims, grounds, evidence, limits, statuses, and open problems from the claim graph in Russian when the user asks about the theory.
---

# FTS Graph Guide

Answer in Russian. Hide commands unless requested.

## Workflow

For a substantial batch of independent lookups, delegate read-only queries to `fts-routine` (`tools/query.py`) or `skill_routine` with exact queries and source fields, only when useful work can continue in parallel. Keep single lookups local. The parent resolves ambiguity, interprets evidence, and answers. Do not delegate graph rebuilding.

1. From the project root, run `python -X utf8 tools/claim_graph.py validate`; report stale data. `work/v14_rebuild/claim_graph/claim_graph.json` is authoritative; Graphify is for navigation.
2. Find unknown IDs with `python -X utf8 tools/claim_graph.py search "<user terms>" --limit 8`. Select by meaning, layer, and source; ask once if genuinely ambiguous.
3. Use `query <ID> --depth 1`; use `path <FROM> <TO>` for a proposed chain.
4. Check `source_file` and `source_location` when meaning, scope, or inference needs confirmation.

## Interpret the result

- `grounds_claim`: a ground stated in the register;
- `verified_by`: a specific check, usually limited to its formal predicate;
- `supported_by`: limited support within the recorded scope;
- `limited_by`: evidence or a finding that limits claim strength;
- `has_status*`: an addressable status assessment with provenance;
- `EXTRACTED`: the relation is stated literally in the source;
- `CURATED`/`INFERRED`: the research layer established the mapping.

Provenance does not establish truth. Keep `St_math`, `St_FTS`, author acceptance, and empirical support distinct. C-NN checks establish only their tested predicate; external evidence does not raise `St_FTS` automatically. For unresolved references say `нет в артефактах`.

## User-facing answer

Use `Найдено → основания → свидетельства → ограничения → статус → что не закрыто`. Link relevant source files. Give both scopes when evidence conflicts. `contains`, topical proximity, and a shared document are not grounds.

For an explicit graph update, run `build`, then `validate --idempotent`, and report coverage changes. Canon corrections needed for the current task are allowed; follow `PROJECT_INSTRUCTIONS.md#canon` and the status procedure. Preserve historical author decisions.
