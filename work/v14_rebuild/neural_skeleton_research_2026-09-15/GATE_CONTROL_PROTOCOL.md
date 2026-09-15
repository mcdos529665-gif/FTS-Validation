# Symbolic-gate M′ control

- Date frozen: 2026-09-15
- Code: run_gate_control.py
- Purpose: test non-uniqueness of the v0.2 derived-feature effect
- Status before run: preregistered control

## Design

Use the same raw episodes and held-out split as v0.2. Recompute residual,
validity, selected memory and coarse readouts in an ordinary feature-engineering
preprocessor with no FTS names or FTS assumptions. Train a standard MLP on those
features with the same 209-parameter budget and the same seeds.

The reference model is the v0.2 structured model. The control model is called
symbolic_gate_Mprime. The control is expected to match the reference because the
two feature maps are declared equivalent. A mismatch is an implementation defect,
not a theoretical result.

## Interpretation

- Matching performance: the v0.2 positive OOD effect is attributable to an
  explicit gate/selected-memory inductive bias, not to FTS-specific naming.
- Materially different performance: audit the feature maps and seeds before any
  scientific interpretation.
- This control does not test whether the raw M′ can learn the gate from fewer
  examples; that contrast was already measured in v0.2.

