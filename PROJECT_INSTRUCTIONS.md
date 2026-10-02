# PROJECT_INSTRUCTIONS — FTS task procedures

[AGENTS.md](AGENTS.md) is the required short contract. Read only the relevant
section here. Current point: [STATE](work/STATE.md); research locations:
[document map](work/DOCUMENT_MAP.md).

| Task | Section |
|---|---|
| Author-requested active canon replacement | [Canon revision](#canon) |
| Evidence, status, ceiling, or FAIL | [Status procedure](#status) |
| Independent mathematical verification | [Wolfram](#wolfram) |
| External scientific grounding | [Academic research](#academic) |
| Card access and tools | [Commands](#commands) |
| Verification and derived outputs | [Checks](#checks) |
| Claim graph | [Graph](#graph) |
| arXiv article import | [arXiv sources](#arxiv) |
| Completing substantive work | [Saving](#save) |

<a id="canon"></a>
## Explicit canon revision

An explicit instruction such as «исправь», «замени канон», «исправь канон»,
«замени формулу в каноне», or an equivalent author request authorizes
**actual replacement**. Do not substitute a proposal, supplement, candidate patch,
or an update confined to `work/` for the requested replacement; do not ask for approval again.

1. Preserve the previous active release in `work/canon_history/<release-id>/`
   or another location specified by the user.
2. Make the smallest coherent replacement in the active `source/` release.
   If a historical version was specified, issue a new active release based on it
   rather than modifying the historical original.
3. Update all canon derivatives and `source/MANIFEST.json`, recording the base
   release, date, provenance, and release type. An author supplement may preserve
   history but does not replace the actual canonical change.
4. Run `tools/verify.py`, targeted `tools/query.py`, and relevant tests. If the user
   also said «заверши незавершённые изменения», complete all unfinished changes
   belonging to the request and identify unrelated work separately.

Canon changes require an explicit author request. Such authorization does not
permit silent changes to unrelated statuses, grounds, or cards.

<a id="status"></a>
## Evidence, revision, and status

The author-approved 2026-09-30 policy supersedes earlier procedural requirements,
including instructions embedded in release v13. Read canonical formulas and
recorded statuses from active cards; preserve the provenance of earlier rules.

Apply К1–К5 according to claim type:

- **К1 — appropriate evidence.** Mathematical claims need a checkable proof or
  formal witness for the exact predicate, domain, and quantifiers; C-NN records
  machine verification within its actual scope. Empirical claims need a protocol,
  data, metric, baseline, budget, and independent replications. Definitions need
  an explicit domain, consistency, and examined boundaries of application.
  Operational interpretations need a distinguishing role test, including an
  alternative/ablation. Accepting a definition does not prove its empirical consequences.
- **К2 — grounds.** Identify applicable grounds and dependencies. A discrepancy
  requires a justified revision and its consequences; retain the previous status
  and record the discrepancy until the new version is accepted.
- **К3 — scope of distinctions.** Preserve types, registers, and overlays. Local
  equivalence needs a stated carrier, projection, conditions, and witness; it
  does not automatically transfer to the original objects.
- **К4 — explanatory consistency.** Check lower levels and dependent results.
  Revision is allowed with grounds, scope, and a list of consequences; accept
  the new version consistently with those dependencies.
- **К5 — revision condition.** Specify a counterexample, distinguishing test,
  or definition-inconsistency condition under which the claim is withdrawn/narrowed.

Raising `St_FTS` requires a separate SP record: claim type, exact scope, evidence,
К1–К5, status before/after, and a justified decision within the author's assigned
scope. An already delegated decision needs no repeated approval. Record the result
in cards and the graph; follow `canon` for an active canon revision. Mathematical
proof, author acceptance, and empirical confirmation are separate axes.

`SP_LIMITS`, `SP_EPI`, and other ceilings record current missing grounds.
Research and proposed formulas are allowed at every level. To lift a ceiling,
address its specific gaps and pass SP/К1–К5. Neither the level number nor an old
ceiling blocks new evidence by itself. This policy does not promote existing cards.

Diagnose negative outcomes before making a status decision:

| Cause | Action |
|---|---|
| Reproducible counterexample to the exact claim within its domain | Withdraw/narrow the affected mathematical claim; record the witness in `REFUTED.md` |
| Check evaluates a different predicate/domain | Repair traceability; do not use that check as evidence for this claim |
| Implementation, data, or environment error | Repair the check; treat the affected computational evidence as unverified until restored |
| Unresolved CAS computation, CAS disagreement, or timeout | `inconclusive`; identify the unresolved issue |

FAIL alone is not a counterexample. Do not promote from doubtful evidence;
assess an independent valid proof separately. An unresolved FAIL/ERROR prevents
the affected result from being reported as verified.

<a id="wolfram"></a>
## Independent Wolfram check

Before a substantive mathematical conclusion, assess whether independent Wolfram
verification is needed. Within assigned research, select necessary checks without
requiring a separate skill invocation. Use `$fts-wolfram-audit` when an independent
CAS witness is needed for the conclusion and at least one condition applies:

- adding/changing `formal_math_fact`, C-NN, or a strong formula in the paper;
- dependence on domain, quantifiers, compatible assumptions, zero, poles,
  periodicity, principal branches, or degenerate cases;
- a counterexample may change `St_math`, a P0/P1 finding, or a promotion condition;
- the claim text and local SymPy/C-NN check may evaluate different predicates;
- local CAS results disagree or remain `inconclusive`.

Do not run Wolfram for editorial changes, literal data-presence checks, literature
search, empirical statistics without a symbolic claim, or unchanged predicates
already verified. The primary agent prepares a complete task packet and delegates
only the mechanical CAS step to `fts_wolfram_worker`; FTS meaning, traceability,
and status remain with the primary model. Do not delegate an incomplete packet.
Wait at most 60 seconds total for the external Wolfram call; then stop the worker
and record `provider_timeout → inconclusive`, without an automatic retry.

<a id="academic"></a>
## Academic research

Within an assigned search or external-grounding check, select the academic workflow
without requiring a separate skill invocation when at least one condition applies:

- prior art or a bounded novelty check is needed;
- a claim relies on a publication or needs supporting/contradicting evidence;
- a literature/systematic review or citation-network coverage is required;
- a publication is proposed as grounds for an FTS status change.

Do not use this skill for local canon checks, editing, export, or literal file
checks. Route purely mathematical claims to `$fts-wolfram-audit`. External sources
remain `[внешнее]`, do not automatically raise `St_FTS`, and do not replace canon
grounds. Send only search strings and bibliographic metadata to external services
by default.

Start with the smallest sufficient `quick`/`fact-check` mode. Derive the mode and
claim/OQ from the task and state them in a progress update. Expand for an identified
gap or on request. Stay within the assigned budget; obtain approval for paid work
beyond it or sharing private materials. Provider unavailability means the check
was not performed, not that the claim failed.

<a id="commands"></a>
## Commands

Run from the repository root. Windows scripts print Cyrillic and write UTF-8;
use **`-X utf8`** to avoid `UnicodeEncodeError`.

```
python -X utf8 tools/verify.py                          # Canon SHA256 integrity; must have 0 mismatch
python -X utf8 tools/query.py stats                     # Card counts by type/status
python -X utf8 tools/query.py card U_07                 # Card and incoming/outgoing edges
python -X utf8 tools/query.py context U_07 1            # Card and neighbours for session context
python -X utf8 tools/query.py find фаза                 # Search text/title/symbol
python -X utf8 tools/query.py deps OP_Lift              # Transitive depends_on
python -X utf8 tools/oq_pool.py --write                 # Overlapping OQ pools → work/OQ_POOLS.md; curated layer: work/OQ_TRIAGE.md

python -X utf8 work/v14_rebuild/verification.py          # Formal theory suite C01..C62
python -X utf8 work/v14_rebuild/verification.py --only C06 C29  # Selected diagnostics with prerequisites
python -X utf8 work/v14_rebuild/probes.py               # Candidate probes; diagnose negatives under status
python -X utf8 work/v14_rebuild/crosscheck.py grounds    # Paper/canon crosscheck: grounds|levels|sp|fails|find <q>|keys
python -X utf8 work/v14_rebuild/o20/run_o20.py           # Preregistered external empirical test

python -X utf8 tools/import_from.py "C:\путь\к\выгрузке" # Install/update canon from a folder, then verify
```

`verification.py` is the **theory test suite**: each formal paper claim maps to
`C-NN`. PASS prints one summary line and writes a short report; FAIL/ERROR/NOT_RUN
writes a detailed `verification_report.md`. Exit codes: 0 if all executed checks
PASS; 1 for FAIL; 2 for ERROR/NOT_RUN or invalid arguments. Diagnose negative
outcomes before deciding mathematical status under `status`.

`--only C06 C29` runs selected checks and prerequisites. It is partial diagnosis,
not a full-suite verdict. Its `verification_diagnostic.md` does not replace the
full report. `--report <path>` selects a report path. Run the full suite without
`--only` before completing formal changes.

Dependencies: Python 3.13; `sympy` for verification; `numpy`/`pandas`/`scipy`/
`scikit-learn` for o20. There is no requirements file; use the user's environment.

Graph commands: `python -X utf8 tools/claim_graph.py
build|validate|coverage|search|query|path`; see `--help`. Read a specific sheet in
the full dump/workbook only when cards are insufficient. For У0, У6/У7, and model
expectation, consult [accepted amendments](work/AUTHOR_CANON.md) and active cards.

<a id="checks"></a>
## Checks by change

Before substantive content work, verify active canon integrity with
`tools/verify.py --strict`. Repeat only after `source/` changes or an integrity
concern; bind reports to the verified version. Diagnose formal changes with affected
C-checks and prerequisites, then run C01–C62 before finalizing. Structure and
provenance do not prove FTS semantics. Rebuild only affected derivatives after
their inputs change. Full route, partial diagnosis, and recovery:
[PROJECT_CONSISTENCY.md](work/PROJECT_CONSISTENCY.md).

Editorial changes alone need no mathematical-suite rerun. For a small text/link
edit, review the diff and affected result. Batch Git status, diff, and necessary
checks; do not repeat successful checks without a new change or discovered issue.

<a id="graph"></a>
## Claim and source graph

`work/v14_rebuild/claim_graph/claim_graph.json` is the authoritative machine layer
for claims, sources, evidence, constraints, and status assessments. It preserves
direction and parallel predicates independently of `graphify-out/`; Graphify is
a navigation view. `CLAIM_MATRIX.tsv` contains grouped claims: atomization requires
a witness. C01–C62 provide evidence for formal predicates without automatically
raising `St_FTS`. Every curated bridge needs scope, provenance, and `status_effect`.

<a id="arxiv"></a>
## arXiv sources

Create a separate directory for each added [arXiv](https://arxiv.org/) article with:

- `source/` — original article source files;
- `original.pdf` — official PDF;
- `article.md` — derived Markdown.

`<каталог статьи>/source/` is an immutable primary source: do not edit,
reformat, or reconstruct it from Markdown. Root `source/` is the active FTS canon;
historical releases belong in `work/canon_history/`. arXiv sources belong only
in their article's nested `source/`.

When Markdown and LaTeX differ, LaTeX takes precedence. Use `original.pdf` to
check visual structure; correct `article.md` against source, never the reverse.

<a id="save"></a>
## Saving work

- Save completed increments to disk; do not retain unsaved analysis only in chat.
- Update STATE/journals when the task, conclusion, or next step changes; minor
  wording/link edits alone need no entry.
- `STATE.md`: current goal, next step, blockers, and links; keep completed history
  elsewhere. Decisions and reasons: `DECISIONS.md`; refutations: `REFUTED.md`;
  question closure: the existing OQ with a result link.
- Review the diff before committing and include only task files. Preserve unrelated
  changes. Commit a coherent completed result; related intermediate steps may be
  committed together.
- Place new material according to [DOCUMENT_MAP.md](work/DOCUMENT_MAP.md), which
  defines file purposes and startup-reading size guidelines.
