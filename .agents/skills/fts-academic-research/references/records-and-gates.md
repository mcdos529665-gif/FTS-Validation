# Records and checkpoints

## Canonical source record

Use these fields in candidate and evidence records:

`record_id,doi,s2_paper_id,consensus_id,title,year,provider,retrieved_at,query_id,claim_or_oq,screening_decision,screening_reason,fts_relation`

Rules:

- `screening_decision`: `include|exclude|uncertain`.
- `fts_relation`: `direct|limiting|alternative|analogy`.
- DOI: lowercase; remove resolver URLs and leading `doi:`.
- Retrieval date: ISO 8601 UTC.
- Preserve provider IDs verbatim.
- Do not place private notes or manuscript text in provider fields.

## Systematic-review checkpoints

1. `protocol_frozen`: research question, databases, queries, dates, criteria, and stopping rule fixed.
2. `seed_verified`: every seed has DOI or S2 ID, or an explicit unresolved reason.
3. `rr_roundtrip_received`: returned export stored byte-for-byte and DOI retention checked.
4. `screening_locked`: Codex and researcher files complete independently.
5. `adjudication_complete`: every disagreement has an author-approved resolution.
6. `synthesis_bounded`: evidence matrix and novelty claim include limitations and uncovered graph regions.

No checkpoint changes FTS status. Any proposed change must proceed through the existing SP/K1-K5 author workflow.
