---
name: fts-graph-guide
description: Navigate the FTS claim graph in Russian for questions about claims, levels, grounds, evidence, limits, statuses, and open problems. Use when the user wants to understand the theory in ordinary language without knowing graph commands or IDs.
---

# FTS Graph Guide

Answer in Russian and hide command details unless the user asks for them. The user may ask in ordinary language where a question sits in the theory, what supports U7, why a status is candidate, what limits a neural claim, or what a report contributed.

## Workflow

For a substantial batch of independent graph lookups, use the project `fts-routine` agent (`gpt-6-luna`, low reasoning) for its permitted `tools/query.py` commands, or `skill_routine` (`gpt-6-luna`, medium reasoning) for read-only claim-graph retrieval. Supply exact queries and requested source fields. Delegate only when the parent can perform useful independent work; keep a single lookup local. The parent selects ambiguous nodes, interprets grounds and limitations, and writes the final answer. Do not pass graph rebuilding to a read-only worker.

1. Work from the project root. The authoritative machine layer is `work/v14_rebuild/claim_graph/claim_graph.json`; Graphify is a navigation view.
2. For a current answer, first run `python -X utf8 tools/claim_graph.py validate`. If the graph is stale, say so. Run `build` only when asked to update or repair the graph.
3. If the ID is unknown, find candidates with `python -X utf8 tools/claim_graph.py search "<user terms>" --limit 8`. Select by meaning, layer, and source. For genuine ambiguity, show a few concise options and ask one question.
4. Use `query <ID> --depth 1` for the selected node. Use `path <FROM> <TO>` to check a specific chain.
5. Open the exact `source_file` and `source_location` when the full meaning, scope, or inference needs checking. The graph routes to the source; it does not replace it.

## Interpret the result

- `grounds_claim`: a ground stated in the register;
- `verified_by`: a specific check, usually limited to its formal predicate;
- `supported_by`: limited support within the recorded scope;
- `limited_by`: evidence or a finding that limits claim strength;
- `has_status*`: an addressable status assessment with provenance;
- `EXTRACTED`: the relation is stated literally in the source;
- `CURATED`/`INFERRED`: the research layer established the mapping.

An edge provenance label does not establish truth. Keep `St_math`, `St_FTS`, author acceptance, and empirical support distinct. A passing C-NN check does not prove a level interpretation. External evidence does not automatically raise `St_FTS`. If a reference cannot be resolved, say exactly `нет в артефактах`.

## User-facing answer

Give a clear Russian account in this order:

`Найдено → основания → свидетельства → ограничения → статус → что не закрыто`.

Show only links that matter to the question and include clickable links to source files. If evidence conflicts, present both sides and their scopes. Do not treat `contains`, topical proximity, or a shared document as a chain of justification.

When asked to update the graph, run `build`, then `validate --idempotent`, and briefly report changes in coverage. Do not edit `source/`, author decisions, or statuses.
