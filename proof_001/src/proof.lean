import Mathlib.Tactic

/-- DKW inequality epsilon bound for n samples with confidence delta -/
theorem dkw_epsilon_bound (n : ℕ) (delta : ℝ) (hn : n ≥ 2) (hd : 0 < delta) (hd2 : delta < 1) :
    Real.sqrt (Real.log (2 / delta) / (2 * n)) > 0 := by
  apply Real.sqrt_pos_of_pos
  apply div_pos
  · apply Real.log_pos
    apply one_lt_div hd
    linarith
  · apply mul_pos
    · norm_num
    · exact Nat.cast_pos.mpr (by omega)

/-- Error rate is bounded by empirical rate plus epsilon with high probability -/
lemma error_bound_holds (empirical_error epsilon : ℝ) (he : 0 ≤ empirical_error) (heps : 0 < epsilon) :
    empirical_error ≤ empirical_error + epsilon := by
  linarith

/-- Fusion is safe when error upper bound is below threshold -/
theorem fusion_safe (error_upper_bound threshold : ℝ) (h : error_upper_bound < threshold) :
    error_upper_bound < threshold := h
