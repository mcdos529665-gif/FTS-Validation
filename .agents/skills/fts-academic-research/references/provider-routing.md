# Provider routing

## Consensus

Use for primary evidence discovery: peer-reviewed papers, reviews, meta-analyses, RCTs, and contradictory results. Keep the existing installed Consensus connector; do not register a duplicate MCP server. Call `search`, then `fetch` before citing or exporting a record. Store the Consensus result ID when present.

## Semantic Scholar

Use Academic Graph for identity and bibliography: DOI/S2 ID resolution, metadata normalization, references, citations, recommendations, and seed-set expansion. `S2_API_KEY` is optional and must never be committed or printed. Start at one request per second regardless of key presence. On `429`, honor `Retry-After`; if retries are exhausted, preserve the candidate as `uncertain` and continue with graceful degradation.

Run one lookup:

```powershell
python -X utf8 .agents/skills/fts-academic-research/scripts/s2_verify.py --doi "10.xxxx/example"
python -X utf8 .agents/skills/fts-academic-research/scripts/s2_verify.py --title "Exact paper title"
```

## ResearchRabbit

Use a human-controlled round-trip. Export verified seeds to `seed_set.bib`; the researcher explores citations, references, and similar papers; import the returned BibTeX, RIS, or CSV as a new file. Preserve the original export unchanged. Re-verify returned records through Semantic Scholar or DOI registries before inclusion. ResearchRabbit does not verify publication existence and does not carry FTS screening decisions.

## Wolfram

Keep `$fts-wolfram-audit` separate and explicitly invoked. Use it only for exact symbolic or statistical predicates after the literature phase identifies a formula worth checking. Its result can affect `St_math` only through the existing project gate and cannot increase `St_FTS`.
