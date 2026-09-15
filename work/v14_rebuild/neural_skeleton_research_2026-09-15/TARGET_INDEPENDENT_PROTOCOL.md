# FTS-Skeleton v0.3 — target-independent / cross-domain probe

- Date frozen: 2026-09-15
- Code: run_target_independent_probe.py
- Data: synthetic episodes only
- Status before run: preregistered exploratory transfer test

## Question

Does one shared provenance/revision/selected-memory representation transfer to
different readouts and different content dimensionality, while a raw M' with the
same parameter budget must relearn the gate from raw events?

This is stronger than v0.2 because the same gate is evaluated under two target
readouts and two input domains. It remains a local inductive-bias test, not a
test of FTS uniqueness.

## Common episode structure

Each episode contains initial content c0, candidate content c1, noisy observations
v0/v1, source identifiers s0/s1 and candidate revision r1. The update is valid
when s0=s1 and r1>0. Selected memory is v1 if valid and v0 otherwise. Training
excludes the same source-mismatch/new-revision combination as v0.2; test contains
it.

The raw M' receives values, source fields and revision. The structured model adds
only residual, validity and selected-memory fields. No target label is used to
compute the gate.

## Domains and readouts

1. scalar domain: c0/c1 are one-dimensional.
2. vector domain: c0/c1 are two-dimensional.

For each domain two targets are evaluated:

- readout A: sign of the first coordinate of selected memory;
- readout B: a different deterministic readout combining selected memory and
  residual, with the same gate and no new external event.

The gate is shared; only the readout changes.

## Capacity and metrics

- Seeds: 13, 29, 47, 71, 97.
- Train/test: 1000/5000 per domain, target and seed.
- Scalar: structured 177 parameters, raw M' 177.
- Vector: structured 241 parameters, raw M' 241.
- Primary metric: structured minus raw M' accuracy on held-out pattern.
- Secondary: full-test accuracy, Brier improvement, sign consistency across seeds.

## Predeclared interpretation

- Positive deltas across both domains and both readouts support transferability of
  the explicit gate/selected-memory inductive bias.
- A domain- or readout-specific effect is limiting, not general support.
- Null or negative deltas are retained as evidence against this implementation.
- Even a positive transfer result does not establish FTS-specificity: symbolic
  preprocessing, state abstraction or an M' with the same derived fields remains
  an allowed alternative.

