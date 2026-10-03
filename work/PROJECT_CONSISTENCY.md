# Reproducible FTS project consistency check

## One command

From the project root:

```text
python -X utf8 tools/check_project_consistency.py
```

The command reads the project without repairing `source/` or rebuilding the graph,
review package, or Graphify navigation. Exit `0` means all five required checks
passed; exit `1` means an error or a required check not run. `--verbose` shows full
output; `--json` returns the same collected result as JSON. `--only <id>` is partial
diagnosis, not a full verdict.

| Route ID | Command | Property checked | Exit code and outputs |
|---|---|---|---|
| `canon_manifest` | `python -X utf8 tools/verify.py --strict` | SHA256/size of every active `source/` file; no unaccounted files | 0: all accounted for; 1: missing/mismatch/extra; 2: no MANIFEST. Writes nothing. |
| `claim_graph` | `python -X utf8 tools/claim_graph.py validate --idempotent` | Directed edges, types, locators, all SHA256 inputs including `OPEN_QUESTIONS.md`, canonical assertion/parallel-predicate coverage, research claims/bridges, deterministic build | 0: PASS; nonzero: structural error or missing/changed/unaccounted input. Writes nothing. |
| `formal_suite` | `python -X utf8 work/v14_rebuild/verification.py` | Exact paper predicates C01–C62 | `0`: all PASS; `1`: FAIL; `2`: ERROR/NOT_RUN. Writes a short `verification_report.md` on PASS and detailed diagnostics for negative outcomes. |
| `audit` | `python -X utf8 work/v14_rebuild/audit/run_audit.py all` | Canon schema/links, claim/OQ/article traceability, review copies/checksums, static suite safeguards, historical artifacts | 0: no unresolved P0/P1; 1: P0/P1; 2: invalid mode. Writes nothing. |
| `research_export` | `python -X utf8 tools/build_research_export.py --check` | Combined export equals the deterministic build from current inputs byte-for-byte | 0: current; 1: missing/stale/invalid build. Writes nothing. |

`PASS_WITH_DOCUMENTED_LIMITATIONS` means exit 0 with a documented P2.
`FAIL` means a failed required check; `NOT_RUN` means a required check was not
performed. Both make the overall exit nonzero. The full route reports P2 separately
without masking them as unconditional success.

## Auxiliary tools outside the verdict

`verification.py --only C06 C29` runs selected predicates and prerequisites. Its
result and `verification_diagnostic.md` are explicitly partial and do not replace
the full report. Run the full suite before completing formal changes. Diagnose
FAIL/ERROR and its status effect under the [current procedure](../PROJECT_INSTRUCTIONS.md#status).

`work/v14_rebuild/crosscheck.py grounds|levels|sp|fails` displays selected canon
cards for manual reading; it has no reference-failure semantics and is not a
paper traceability check. `run_audit.py all` performs that role in the read-only
route. `graphify_audit_navigation.py --verify` writes a navigation fragment before
checking, so it belongs to explicit recovery rather than the read-only verdict.

## Explicit derivative recovery

After input changes, run only necessary actions, each separately. Discovered and
resolved P1 history: `work/project_consistency/BLOCKERS_2026-09-23.md`.

```text
python -X utf8 tools/claim_graph.py build
python -X utf8 tools/build_research_export.py --rebuild-package
E:\Codex\mcp\graphify\tools\graphifyy\Scripts\python.exe -X utf8 tools/graphify_audit_navigation.py --inject --verify
python -X utf8 tools/check_project_consistency.py
```

The first action rewrites authoritative claim-graph derivatives only
(`claim_graph.json`, coverage/change report, HTML). The second updates the explicit
review-copy list, combined export, and `CHECKSUMS.sha256`; it preserves staging
`v14_export_cards.jsonl`, `v14_export_triples.tsv`, and `README.md`. The third is
optional: Graphify is a navigation projection, not the source of truth. It writes
a fragment/graph/report and is therefore outside the read-only route. None
replaces the active canon. Before `claim_graph.py build`, select and track its
input versions; the build must not choose a research source-artifact version.
Any OQ change also requires a graph rebuild because OQ is in `input_digests`.

## Limits of automatic checks

The route does not prove FTS semantics, author acceptance, `St_FTS`, global
mathematical truth, biological relevance, external-literature completeness, or
new experimental results. It does not choose between conflicting substantive OQ
statuses. C01–C62 witness only their exact formal predicates; structural graph
PASS preserves provenance without replacing grounds or the author's decision.

Pre-existing unfinished work by others and the intended future commit boundary:
`work/project_consistency/BASELINE_UNFINISHED_2026-09-23.md`.
