# Audited v14 status patch

This is a conservative proposal for a future v14 workbook export. It does not
edit the v13 canon in `source/`. The audit confirmed canon integrity
(`13 ok / 0 missing / 0 mismatch`) and 62 mathematical checks, but no new semantic
promotions. The two-axis rule is mandatory:

```text
PASS C-NN -> computational evidence only for the exact predicate in the checked domain
canonical_v14 -> К1–К5 passed separately and status encoded in the target SP card
```

The [current status procedure](../../PROJECT_INSTRUCTIONS.md#status), adopted
2026-09-30, selects К1 by claim type, allows justified lower-level revision with
consequences, and requires diagnosing FAIL. These tables preserve earlier audit
results; a new decision requires a new SP record.

## 1. Audit of proposed promotions

| Entity | v13 status / grounding | Earlier claim | Audit verdict | Requirement for reconsideration |
|---|---|---|---|---|
| U_07 / M_07 | `candidate_with_operational_gate` | Forms through У7: `canonical_strict` | **Do not promote**. C-35/C-60 show a formal pattern, not a forced rung or the meaning «Знание» | New SP card with separate form/semantic targets, К1–К5, operational test |
| U_08 | SP_U8 and U_08: `candidate_with_operational_gate` | `canonical_v14` | **Keep `candidate_with_operational_gate`**. `promotes_status_of` transfers a candidate, not canonical, status | Question-role ablation and new SP with `canonical_v14` |
| U_09 | SP_U9 and U_09: `FTS_candidate` | `canonical_v14` | **Keep `FTS_candidate`**; C-10…C-12 check the cube, not «Понимание» | Independent causal-grounding role test and new SP |
| U_10 | `reserved_underformalized`; no SP_U10 | `canonical_v14` from cos uniqueness | **Keep `reserved_underformalized`**; ODE/series/zeros are `formal_math_fact`, interpretation is candidate | Operational scale/assessment test and SP_U10 |
| U_11 | `reserved_underformalized`; no SP_U11 | `canonical_v14` from ODE `F'=F` | **Keep `reserved_underformalized`**; exponential is `formal_math_fact`, FTS selfhood unproven | К1–К5 for selfhood and SP_U11 |
| U_12 | SP_U12/U_12: `candidate_requires_formalization + canonical_alignment` | `canonical_v14` | **Keep the compound status**. Class geometry is `formal_math_fact`; «Конфликт/Союз» and gate remain candidate | Formalize semantics/gate and new SP satisfying all К1–К5 |

## 2. Open questions and traceability defects

| Node | Finding | Verdict |
|---|---|---|
| Q_LOGIC_7_11 | §7.3 proposes an object-language; completeness of dictionary Д and operational tests unproven | Do not close |
| U12_CIRCLE | C-23 proves “not a function graph”: mathematical expressivity, not an operational FTS role | Math part closed; semantics open |
| SP_PARITY | Subject `SP_PARITY` exists in `fts_triples.tsv` but no card in `fts_cards.jsonl` | Broken v13 reference; do not use for promotion; restore/remove in workbook v14 |
| O2/O12 and other missing IDs | `depends_on` has aliases/unresolved entities | Full patch: `audit/CANON_REFERENCE_PATCH.tsv`; do not canonize dependent claims |
| O_20 | Preregistered operationalization unconfirmed; audit: 1/4 dataset wins, sign `p=0.9375`, mean ΔAUC=-0.0079 | Preserve negative result; pooled fold-level p is not cross-dataset evidence |
| D2 sign/phase | Original scaler saw full X; train-only reanalysis: HistGB 2/4, sign `p=0.6875`, mean ΔAUC=-0.0012 | Strong external role unconfirmed; internal У8/У9 role not tested |
| Д10 / SP_COMPLEX | Five variants reproduced byte-equal, with representation/CFO/target confounds | No clean phase verdict; do not promote SP_COMPLEX |
| External contact / novelty | Additional 2026-08-02 check confirmed component-level contact У2–У5 (У1 limiting); absence of a full analogue is bounded to 28 original queries | As of 2026-09-13, do not assign novelty or claim external validation of the full ladder. A future predefined SP/K1–K5 evidence threshold may yield `promotion_ready`; until then literature does not change `St_FTS` |

## 3. Proposed cards for a future v14 export

| ID | Content | Allowed status after audit |
|---|---|---|
| DICT_D1…D11 | Conversion dictionary §5 | `candidate_v14`; specified C-NN math kernels: `formal_math_fact`; Д3 separately `canon-grounded` within U_06 |
| NOTATION_ANTIFORM | Distinguish `−F`, `Rot_θ`, `⊖A` | `proposed_note`; no level promotion |
| UNIT_BOUNDARY | `x²=x ⇔ x∈{0,1}` and pointwise coincidences | Equality: `formal_math_fact`; FTS boundary: `candidate_v14` |
| OVERLAY_AS_CARRIER / CHI_OVERLAY_VERIFIED | `x:=χ` substitution and guards | `candidate_overlay`; no level-status promotion |
| SMALL_FORM_PROJECTION / CONTRADICTION_LATTICE | Projections/mirror pairs | `candidate_v14`; C-57…C-59 check exact special-case predicates |
| EXTERNAL_BRIDGE_U1_U5 | Typed chain `Stable → E → Dist → μ на слое → section/decision rule`; `|x|` as alternative class, `−|x|` as fixed selector | `external_bridge_candidate`; direct component contact У2–У5, У1 limiting only; no `promotes_status_of`, level order/semantics unproven |
| EXPLICIT_ADDITIONS_20260905 | REFINE-MIN, DENSE-PARTITION, SELECT-SYMMETRY, ABS-GAIN, Lift/У0–У7 limits, new OQs | `external_research_integration`; exact finite math scopes checked EA-01…EA-08; no `promotes_status_of`, paper C-NN, or `St_FTS` increase |
| LEVEL_RETENTION_RULE | Consequence of О1+О3+О8: locally incompatible pairs through У7 retained in `У(2k+2)` as distinguishable modes | `derived_constraint` within `k∈{1,2,3}`; not an axiom or simultaneous truth; no U_08 promotion |
| SYMMETRY_ESCALATION_HYPOTHESIS | After У7: antiform → operator symmetry (`ΔF=F`, У11) → group invariant (У15) | `hypothesis_candidate`; A0b confirms only carrier change, C-18/C-31 local math facts; no general law |
| PROPOSAL_STRICT_BAND_7 | Hypothesis about the boundary of forms through У7 | `candidate_requires_canonization`; type `hypothesis_candidate`; no `promotes_status_of` |
| MAP_PENTAD / MAP_PI_PROJ / RULE_P | Pentad, projections, rule П | `candidate_v14`; state exact C-NN scopes in cards |
| U_13_FORMULA | `∏Bₖ=0` | `candidate_prediction`; zero-product: `formal_math_fact` |
| U_14_FORMULA | `F(x,y;θ)=0` | `projected_candidate` |
| U_15_FORMULA | `z=e^{iθ}` | `projected_candidate`; C-31 properties: `formal_math_fact` |

## 4. Discarded or downgraded

| Claim | Verdict |
|---|---|
| `y=−x²` «описывает мнимые числа» | `discarded_v14`: violates `Rot ≠ −` |
| «3-мерный крест / поле мерностей» for У4 | `discarded_v14`: no К1 witness |
| `χ³` as У9 core | `overlay_only`: canon requires causal/counterfactual decomposition |
| Reading У10 «периодическое сравнение» as definition | `discarded_v14`: decorative; ODE characterization retained as math fact, without canonizing meaning |
| Fixed У16–У17 formulas | `discarded_v14` for the earlier proposal: no К1 witness; new research candidates allowed |
| `canonical_v14` for U_07…U_12 from C-NN alone | Withdrawn as conflation of `St_math`/`St_FTS` |

## 5. Current boundaries

- У−1…У6: current `canonical_strict` retained; justified revision allowed in a new coherent version.
- χ ladder, complex/tensor layers: overlay/candidate, not canonical levels.
- SP_EPI/SP_LIMITS record current gaps; closing them permits SP/К1–К5 review. For now, У13–У15 remain prediction/projected; У16–У17 speculative.
- Preserve O_20, D2, D10 preregistrations and primary results; issue corrections as dated audit reanalyses.

This patch becomes canon only after an external workbook round-trip, a new
`MANIFEST.json`, and successful SHA256 verification. Until then it is a review artifact.

## 6. Separate author acceptance, 2026-09-19

The author's direct decision published
[AC-2026-09-21](../author_canon/2026-09-21/AMENDMENT.md): current У6/У7 forms.
AC-2026-09-19 remains for local non-object/absence equality at У0, expectation's
link to speed, and the model's indistinguishability of speed/fundamentality.
These new records have `author_status=accepted_into_author_canon`; they are not
the earlier AND/OR research candidates. Their `evidence_status` separately records
formal/empirical gaps. Each record links to the original message through `adopts`.
Historical U_07/M_07 and SP statuses and C-NN are not promoted. The combined
workbook is not yet released; when assembling it, transfer the supplement with
both status axes preserved.
