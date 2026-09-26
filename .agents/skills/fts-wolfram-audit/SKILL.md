---
name: fts-wolfram-audit
description: Independently check exact FTS mathematical claims with Wolfram Language, search for counterexamples, and compare with local C-NN/SymPy checks. Use when explicitly asked to audit a C-NN, formal_math_fact, formula, domain, quantifiers, zero, pole, periodicity, branch, degenerate case, or independent CAS result. Do not use for literature search, empirical work, interpretation of level meanings, or automatic FTS status promotion.
---

# FTS Wolfram Audit

## Contract

Work only from an explicitly stated mathematical predicate. Keep separate:

- the mathematical claim;
- its proposed FTS interpretation;
- current `St_math`;
- current `St_FTS`.

Treat Wolfram as independent external CAS evidence. It is not a source of canon, level semantics, or automatic status promotion. Do not edit `source/`.

Invoke this skill only explicitly. The advisory gate in the root `AGENTS.md` may suggest it but does not authorize a Wolfram call without the user's decision.

## Divide responsibilities

The primary agent retains responsibility for:

- extracting the claim from canon and audit matrices;
- stating the domain, quantifiers, assumptions, and defeat condition;
- comparing the predicate with C-NN;
- interpreting the result and deciding anything about `St_math` or `St_FTS`.

If the project agent `fts_wolfram_worker` is available and the task packet is complete, delegate only the mechanical Wolfram step. That worker may:

- check packet completeness;
- assemble self-contained Wolfram Language code using the templates below;
- call Wolfram and return the code, raw result, and witness.

Do not let the worker supply a missing domain, interpret FTS, assign the final verdict, edit files, or promote status. If the worker is unavailable or reports an error, record `inconclusive` or make an explicit decision on whether the primary model should retry the computation.

The primary agent maintains a watchdog: one `wolframcontext` attempt, one evaluator call, and at most 60 seconds total waiting for the external provider. After the limit, stop the worker and record `provider_timeout → inconclusive`; do not retry silently.

## Prepare an exact task

1. Complete the mandatory startup procedure in the root `AGENTS.md`.
2. Locate the claim by `claim_id`, `C-NN`, `PA-*`, or OQ in `CLAIM_MATRIX.tsv`, `PATTERN_ATLAS.tsv`, `PATTERN_OQ_MAP.tsv`, the paper, and `verification.py`.
3. Record variables, domain, quantifiers, assumptions, predicate, and defeat condition.
4. Record the FTS interpretation separately. Do not include it in the CAS predicate.
5. If the domain or term mapping is absent from artifacts, stop with `inconclusive`; do not import a conventional mathematical meaning.

Before delegation, assemble a packet without free-form paraphrase:

```text
claim_id:
local_check:
variables:
domain:
quantifiers:
assumptions:
predicate:
defeat_condition:
```

Missing any semantic field means `incomplete_packet`.

## Call Wolfram safely

1. Check whether Wolfram app tools are available.
2. On the first call or a topic change, call `wolframcontext` with detailed context. Use it only for navigation: semantic retrieval may be irrelevant and is not proof. Do not repeat a hung or failed context call.
3. Perform the main check through `wolframlanguageevaluator` with explicit Wolfram Language code. Make every call self-contained because the kernel is stateless.
4. Use `wolframalpha` only as a supplementary sanity check, never as the basis of a formal verdict.
5. Use exact values (`1/3`, `Pi`, `Sqrt[2]`) instead of machine decimals.

If Wolfram is unavailable or returns a provider error, timeout, or unevaluated expression, record `inconclusive`. Do not substitute a local CAS for the independent check or misreport provider failure as a negative result.

## Perform four checks

### 1. Satisfiable assumptions

Check that the task domain is nonempty:

```wl
Reduce[assumptions, vars, domain]
Resolve[Exists[vars, assumptions], domain]
```

If assumptions are inconsistent, record `vacuous_assumptions`, not PASS.

### 2. Universal formulation

Check exactly the stated quantifiers:

```wl
Resolve[ForAll[vars, Implies[assumptions, predicate]], domain]
```

Do not replace a universal claim with a finite sample.

### 3. Counterexample search

Search for a violation independently of the proof path:

```wl
Reduce[assumptions && Not[predicate], vars, domain]
FindInstance[assumptions && Not[predicate], vars, domain]
```

Failure of `FindInstance` to return an instance is not a proof. Check an explicit witness by substitution into the original predicate.

### 4. Domain boundaries

Check applicable cases separately:

- denominator zeros and poles;
- zero, one, and junction points;
- periodicity and choice of fundamental interval;
- principal branches of `Sqrt`, `Log`, fractional powers, and inverse functions;
- degenerate parameters and empty solution sets;
- real, complex, integer, and finite domains without silently transferring results;
- rings with zero divisors or characteristic 2 if the claim extends beyond a field.

Do not use `PowerExpand` or `GenerateConditions -> False`. Do not strip conditions produced by `Reduce`, `FunctionDomain`, `Assuming`, or `FullSimplify`.

## Compare with the project

1. Compare the checked predicate line by line with the claim text and current C-NN.
2. If a C-NN exists, run the complete `verification.py` suite rather than imitating a single check.
3. When Wolfram and the local suite agree, assign `confirmed_math` only to the exact predicate and domain.
4. For a counterexample, assign `refuted`.
5. For disagreement between CAS results, assign `cas_disagreement` and leave the issue for manual analysis.
6. Do not transfer any of these verdicts automatically to `St_FTS`.

Only the primary agent assigns the final verdict:

- `confirmed_math`: the exact predicate is confirmed in the stated domain;
- `refuted`: a counterexample was found and checked again;
- `inconclusive`: the computation or formulation gives no rigorous answer;
- `vacuous_assumptions`: assumptions are inconsistent or the domain is empty;
- `cas_disagreement`: Wolfram and the local check disagree.

The primary model must analyze every new or status-significant `confirmed_math` and every other outcome. The worker is not a reviewer.

## Record the result

Answer in Russian using the project form:

`Найдено → зависимости → вывод → что не закрыто.`

Always include:

- `WF-NNN`, date, and related `claim_id`/`C-NN`/`PA-*`/OQ;
- exact formula, domain, quantifiers, and assumptions;
- complete Wolfram Language code that was executed;
- raw result and counterexample when present;
- comparison with local C-NN;
- one permitted verdict assigned by the primary model;
- impact on `St_math` only;
- an explicit list of what the result does not establish in FTS.

For an analysis-only request, return the record in the answer. When explicitly asked to save or integrate the result, append a dated record to `work/v14_rebuild/audit/WOLFRAM_CHECKS.md` without rewriting history. Keep a new test separate from the main C suite initially. Move it into `verification.py` only by a separate decision with an exact claim → predicate → check trace.

If project files changed, check:

```text
python -X utf8 tools/verify.py
python -X utf8 work/v14_rebuild/verification.py
python -X utf8 work/v14_rebuild/audit/run_audit.py traceability
```

Ensure the diff under `source/` is empty.
