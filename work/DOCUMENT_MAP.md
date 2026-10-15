<a id="где-читать-и-хранить-материалы-фтс"></a>
# Where to read and store FTS material

Use this index by task. Startup needs only the files listed in `AGENTS.md`;
following a link does not require loading neighbouring documents.

<a id="назначение-файлов"></a>
## File roles

| Material | Main location | When to read / what to write |
|---|---|---|
| Project objective and scope criteria | [PROJECT.json](../PROJECT.json), [README](../README.md#задача-проекта) | Persistent entity `FTS`; four research addresses, roles, evidence obligations and separate proof/status axes |
| Required short contract | [AGENTS.md](../AGENTS.md) | Startup and standing rules; supplied to the agent automatically |
| Task procedures | [PROJECT_INSTRUCTIONS.md](../PROJECT_INSTRUCTIONS.md) | Relevant section only: canon, gates, commands, graph, arXiv, saving |
| Current state | [STATE.md](STATE.md) | Once before substantive FTS work; goal, next step, blockers, links; history in a separate snapshot |
| Concise symbol meanings | [notation.md](notation.md) | Before substantive FTS analysis; symbol → meaning → source |
| Active canonical forms/statuses | `source/fts_cards.jsonl`, via `tools/query.py` | Read specific cards; edit as needed for the current task |
| Author-accepted amendments | [AUTHOR_CANON.md](AUTHOR_CANON.md), `author_canon/` | Exact wording, acceptance scope, provenance; journal new proposals first |
| New author contribution | [DIALOGUE_NUANCE_JOURNAL.md](DIALOGUE_NUANCE_JOURNAL.md) | Working queue: `pending`/`needs_author` only; quotation, reading, integration destination |
| Processed author contribution | [DIALOGUE_NUANCE_SOURCES.md](DIALOGUE_NUANCE_SOURCES.md) | Exact quotation and result location; full previous analysis in Git history |
| Research on a specific question | Thematic package in `v14_rebuild/` | Grounds, analysis, model, witness, limits; look for an existing package first |
| General theory presentation | [FTS_v14_paper.md](v14_rebuild/FTS_v14_paper.md) | Coherent result, links, status; intermediate detail stays in research packages |
| Open question | [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) | Unresolved issue, needed witness, next step; extend existing OQ where possible |
| Candidate proposals (collected, grouped) | [Candidate register](v14_rebuild/candidates_register_2026-10-15/REGISTER.md) | Index only: group, level address, references (cards, OQ, checks, DN); full text stays in the primary document; add rows via `src/G*.tsv` and `build_register.py` |
| Author answers to graph questions | [AUTHOR_ANSWERS_60.md](AUTHOR_ANSWERS_60.md) | 60 unique linked OQs: short text, context link, answer field |
| Research answers to 60 OQs | [Undermind review](v14_rebuild/e5_literature_review/undermind_60_oq_2026-09-30/ANSWERS_60.md) | Verbatim question, working assistant answer, missing grounds; sources/protocol in the same package |
| Additional seven-element window | [Torus and Klein group](v14_rebuild/seven_window_torus_klein_2026-09-30.md) | Author quotations, phase model ℤ₄ × ℤ₆, reflection group V₄, FTS correspondence limits, separate Wolfram record |
| Accepted work decision | [DECISIONS.md](DECISIONS.md) | Choice, reason, full-analysis link |
| Refuted working conclusion | [REFUTED.md](REFUTED.md) | Refuted claim, witness, remainder |
| External-source conflict | [EXTERNAL_CONFLICTS.md](EXTERNAL_CONFLICTS.md#правило-внесения) | Both sides, comparison domain, decision; procedure in the log |
| Status promotion | [status_patch_v14.md](v14_rebuild/status_patch_v14.md) and SP card | Promotion conditions; separate mathematical/semantic axes |
| Machine derivatives | `claim_graph/`, `export/` | Update with standard generators after changes to working source documents |
| Earlier document versions | `state_history/`, `notation_history/`, `instruction_history/`, Git | Transfer/recovery history; read when verifying an earlier version |

<a id="куда-отнесены-разделы-прежней-нотации"></a>
## Locations of former notation sections

Checked 2026-09-26. “Covered” means the substantive explanation already exists
at the listed location; no duplicate is needed. Earlier content:
[transfer history](notation_history/2026-09-26/README.md).

| Former topic | Working location | Review result |
|---|---|---|
| М/Ч/А, levels, `window`, status names | [Dictionary](notation.md); procedure: [status patch](v14_rebuild/status_patch_v14.md) | Concise meanings and notation order preserved |
| External-reading conflict | [EXTERNAL_CONFLICTS.md](EXTERNAL_CONFLICTS.md#правило-внесения) | Rule covered there; duplicate removed from dictionary |
| `¬A`, `0_A`, `⊖A`, `−`, `Rot` | Brief: [dictionary](notation.md); detail: paper [§3.2–3.2a](v14_rebuild/FTS_v14_paper.md#notation-signs) | Definitions retained; C-01/C-38/C-39 links covered in paper |
| Non-object/absence equality at У0 | [Accepted У0 amendment](author_canon/2026-09-19/AMENDMENT.md#u0) | Pointer to the equality's local scope preserved |
| Boundaries `x=0`, `x=1` | Paper [§3.5–3.6](v14_rebuild/FTS_v14_paper.md#notation-boundaries) | Mathematical analysis covered; excluded from startup dictionary |
| Q/R channels and relation pole | [Register map §2](v14_rebuild/FTS_v14_register_map.md#readout-channels), paper §5.1b | Covered; channel names remain in dictionary |
| v11, χ-, complex/tensor overlays | [Register map §3](v14_rebuild/FTS_v14_register_map.md#overlays), current `CH_07` | Brief v11–v13 history reference added; read statuses from cards |
| Four meanings of arbitrariness | [Non-arbitrariness review](v14_rebuild/nonarbitrariness_dialogue_2026-09-13/REVIEW.md#четыре-смысла-произвольности) | Covered; old M-forms in the dated review marked historical |
| Active У6/У7 forms | [2026-09-21 amendment](author_canon/2026-09-21/AMENDMENT.md#найдено-точная-замена-форм-у6у7), `M_06`, `M_07` | Read full formulas from active source |
| Speed and fundamentality | [Accepted wording](author_canon/2026-09-19/AMENDMENT.md#expectation); [bidirectional reading](v14_rebuild/m_register_grammar_2026-09-25/BIDIRECTIONAL_READING.md) | Accepted claim distinguished from later research proposal |
| Minimum, access, application, `Tri_k` | [Inheritance study §5–6](v14_rebuild/recursive_distinction_2026-09-12/REVIEW.md#minimum-capability) | Covered; `Cap_n`, `Act_n` are auxiliary notation |
| «Локально абсолютно, глобально относительно» and absence readings | [2026-09-12 author clarifications](v14_rebuild/recursive_distinction_2026-09-12/AUTHOR_QUESTIONS.md) | Quotation and revisions preserved |
| У3→У2, У2→У1 | [Descent study](v14_rebuild/interpretation_descent_undermind_2026-09-12/REVIEW.md#interpretation-descent) | Loss of interpretation degree distinguished from loss of the code move |
| Trajectory, separation/summation, refusals, upper windows, reflection | [DN-0001–DN-0016 integration](v14_rebuild/dialogue_semantics_2026-09-15.md#trajectory) | All eight former summary points covered in sections 1–6 |
| DN-0017–DN-0027 clarifications | [Batch integration](v14_rebuild/dialogue_integration_2026-09-22.md#результаты) | Each DN-ID has an analysis; duplicate dictionary summary removed |
| Level equality, reflection, code «ведёт к» | [Equality review §6–8](v14_rebuild/m_register_grammar_2026-09-25/EQUALITY_REVIEW_2026-09-26.md#types-of-equality), DN-0030/0031 | Exact author position and open question preserved |

<a id="правило-следующей-записи"></a>
## Where to add the next entry

1. Find the destination row and existing thematic document.
2. Store full content in one main location, with source and status.
3. Add only a new symbol and concise meaning to `notation.md`; the current step
   and link to `STATE.md`; the decision and reason to `DECISIONS.md`.
4. If material is already explained, link directly to its section. Keep exact
   author quotations in the journal/author packet; put the assistant's model in
   the research analysis with its own label.
5. Each rule has one main location: standing rules in `AGENTS.md`, procedures in
   the relevant `PROJECT_INSTRUCTIONS.md` section. Other files link there. Keep
   research results and completed history in thematic documents, without
   retelling them in startup files.

<a id="бюджет-стартового-чтения"></a>
## Startup reading budget

| File | Character guideline | If it grows |
|---|---:|---|
| `AGENTS.md` | 3 500 | Move commands, rare procedures, and detail to the reference |
| `STATE.md` | 2 500 | Save a snapshot; keep the current goal, next step, blockers, and locations |
| `notation.md` | 4 000 | Keep concise meanings; replace detailed explanations with links |

Sizes are editorial guidelines. Condense/move content while preserving history;
do not delete a needed rule to meet a character count. A link does not require
reading the entire document. Start with the contract; add STATE and notation for
substantive FTS work, then choose further reading by task. Original snapshots and
size comparison: [2026-09-27 optimization](instruction_history/2026-09-27/README.md).
