# Provider status · E5 wave 0

- checked_at: `2026-07-20`
- data boundary: only search strings and bibliographic metadata left the workspace;
  no manuscript, private note, or canon corpus was sent to a provider.

## Consensus

All registered discovery strings Q01–Q10 (plus the explicit Q09 synonym) were run.
Each returned ten visible records; title/abstract-relevant candidates were fetched before
being placed in `CANDIDATES.tsv`. The retrieval trace is `SEARCH_LOG.tsv`. Consensus is
used for discovery only, not as a status-changing authority.

## Semantic Scholar

The first DOI lookup in this wave returned `URLError`; an earlier pilot title lookup
for E5-0001 exhausted a documented `429` backoff. In accordance with the protocol,
there was no automatic retry and no guessed S2 paper ID. Records without a DOI or
publisher identity remain `uncertain` or `exclude` until a future successful lookup
or a researcher-supplied primary record.

## ResearchRabbit

No API/MCP route is assumed. `seed_set.bib` contains seven DOI-preserving seeds for a
manual, human-controlled citation-graph expansion. The round-trip is pending; see
`RESEARCHRABBIT_HANDOFF.md`. ResearchRabbit may expand a graph but never validates a
paper's existence by itself.

## Wolfram

Not invoked. This review contains no author-supplied exact predicate, domain, and
formula package; literature retrieval cannot trigger a Wolfram audit.
