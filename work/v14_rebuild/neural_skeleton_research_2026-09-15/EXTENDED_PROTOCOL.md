# FTS-Skeleton v0.2 — provenance/revision/memory probe

- Date frozen: 2026-09-15
- Code: run_extended_probe.py
- Data: synthetic episodes only
- Status before run: preregistered exploratory inductive-bias test

## Claim under test

Can an explicit provenance/revision gate plus selected-memory readout improve
generalization to a held-out intervention pattern relative to an M' MLP that
receives the same raw event fields, when trainable parameter counts are equal?

This is a local architecture test. A positive result supports only the usefulness
of the declared gate prior; it does not establish that the gate is uniquely FTS.

## Episode generator

Each episode has two candidate observations:

- initial latent content c0 and noisy value v0;
- candidate updated content c1 and noisy value v1;
- initial source s0 and candidate source s1;
- candidate revision r1, with initial revision fixed at 0.

The update is valid iff s1 equals s0 and r1 is greater than zero. The target is
the sign of c1 when the update is valid and the sign of c0 otherwise.

The raw M' input is (v0, v1, s0, s1, r1, r0). The structured FTS-skeleton input
adds residual, validity gate, selected-memory value and two coarse sign readouts.
The derived fields are declared operations and are not treated as free evidence.

## Train/test split

- Training excludes one source-mismatch/revision combination:
  s0=1, s1=0, r1=1.
- Test is a fresh sample over all combinations, with a separate report for the
  held-out pattern and the full test distribution.
- Five seeds: 13, 29, 47, 71, 97.
- Train/test size: 800/5000 per seed.
- Both MLPs use tanh and lbfgs with max_iter=500.
- Parameter counts are exactly matched: structured 209, raw M' 209.

## Primary metrics and interpretation

Primary: paired held-out-pattern accuracy delta and full-test accuracy delta.
Secondary: Brier delta and per-pattern accuracy.

Predeclared interpretation:

- Positive delta on the held-out pattern supports a local inductive-bias effect
  of the explicit provenance/revision/memory computation.
- A null or unstable delta limits this architecture choice.
- A negative delta is a refuting result for this implementation and split.
- Even a positive delta does not establish FTS specificity, because a standard
  symbolic gate or a feature-engineered M' could reproduce the same computation.
