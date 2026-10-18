import Mathlib.Basic.Real.Basic
import Mathlib.Algebra.Order.Group.Abs
import Mathlib.Algebra.Ring.CharZero

/-!
Existing mathematical kernels of FTS C01, C03, C04, C09 and C49.
All variables are real. These declarations do not formalize level semantics.
-/

set_option warningAsError true

namespace FTS

/-- C01: a value equals its arithmetic antiform exactly at zero. -/
theorem antiform_eq_iff_zero (a : ℝ) : a = -a ↔ a = 0 := by
  exact CharZero.eq_neg_self_iff

/-- C03: absolute value is invariant under reflection. -/
theorem abs_reflection (x : ℝ) : |(-x)| = |x| := by
  exact abs_neg x

/-- C04: the absolute-value fiber is the pair of mirror values. -/
theorem abs_fiber (a b : ℝ) : |a| = |b| ↔ a = b ∨ a = -b := by
  exact abs_eq_abs

/-- C09: squaring identifies distinct values 1 and -1. -/
theorem square_branch_collision :
    (1 : ℝ) ^ 2 = (-1 : ℝ) ^ 2 ∧ (1 : ℝ) ≠ -1 := by
  constructor
  · simp
  · intro h
    exact one_ne_zero (CharZero.eq_neg_self_iff.mp h)

/-- C49: the only real idempotents of squaring are 0 and 1. -/
theorem square_idempotents (x : ℝ) : x ^ 2 = x ↔ x = 0 ∨ x = 1 := by
  constructor
  · intro h
    have hprod : x * (x - 1) = 0 := by
      rw [mul_sub, mul_one, ← pow_two, sub_eq_zero]
      exact h
    rcases mul_eq_zero.mp hprod with hzero | hone
    · exact Or.inl hzero
    · exact Or.inr (sub_eq_zero.mp hone)
  · rintro (rfl | rfl) <;> simp

end FTS
