# FTS-Skeleton v0.1 — preregistration for the first executable probe

- Date frozen: 2026-09-15
- Code: run_prototype.py
- Data: synthetic only; no external dataset
- Status: exploratory construct-validity probe, not T2/T3 evidence

## Purpose

Проверить, можно ли без скрытого переименования реализовать две роли из
ARCHITECTURE_SPEC: typed absence and compositional module selection. The probe
does not test the whole FTS ladder and cannot establish biological relevance.

## Models

1. 'typed_absence': MLP receives value vector plus an explicit missingness mask.
2. 'value_only': independent MLP receives values with missing entries encoded as
   zero and no mask.
3. 'compositional_modules': two independently trained operator modules selected
   by a question bit.
4. 'compositional_monolith': one MLP receives the same values and the question bit.

Hidden widths are chosen so that the reported first-layer parameter counts match
exactly within each pair. The modules still differ in training-data allocation;
this is recorded as a limitation rather than hidden.

## Data-generating processes

### ABS-MECH

Two latent variables z1 and z2 are sampled from a standard normal distribution.
The label is 1[z1 + z2 > 0].

- 'signal': z2 is hidden when z2 > 0.65; the hiddenness pattern is therefore
  informative about z2.
- 'null': hiddenness is sampled independently of z1 and z2.

The observed value for a hidden z2 is zero. The task contains an explicit observed
zero, so value-only cannot reconstruct the mask from the value.

Primary contrast: paired test accuracy and Brier score, typed_absence minus
value_only, separately for signal and null mechanisms.

### COMP-QUERY

The input is (a,b,q), where q selects one of two compositional decision rules:
q=0 uses a+b+0.25ab; q=1 uses a-b+0.25ab. The held-out split uses fresh
samples from the same generator.

Primary contrast: compositional_modules minus compositional_monolith. No directional
hypothesis is promoted to a claim; this is a feasibility and failure-surface probe.

## Seeds and metrics

Seeds: 13, 29, 47, 71, 97. Train/test sizes: 1800/2000 per task and seed.
Metrics: accuracy, Brier score, parameter count, and paired mean delta with a
95% t-style interval over seeds. lbfgs MLP training is bounded at 500 iterations.

## Predeclared interpretation

- A positive ABS-MECH signal contrast with null contrast near zero supports only
  the local proposition that explicit absence state can be computationally useful.
- A null contrast or unstable sign is evidence against treating typed absence as a
  universal advantage.
- COMP-QUERY results assess whether modular decomposition is implementable; either
  sign is informative and cannot by itself support FTS specificity.
- No outcome changes FTS statuses. A failure is recorded as a limitation, not
  silently repaired by changing the generator.

