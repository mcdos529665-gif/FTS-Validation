# Проверки основного DR-блока

Самостоятельный код; вложенный код отчётов не исполняется. Дата пакета: 2026-09-11.
PASS относится к предикату указанного конечного примера, не к ФТС и не к C-NN.

**18 PASS / 0 FAIL.**

| ID | Предикат | Итог | Свидетель |
|---|---|---|---|
| DRC-01 | Byte integrity of seven submitted reports | PASS | {"reports": 7, "hashes_match": true} |
| DRC-02 | Fibre criterion and fixed-pair minimality on four states | PASS | {"q_r_pairs": 256, "carrier_size": 4, "partitions_per_pair": 15} |
| DRC-03 | A minimum may skip covers; first queries may be incomparable | PASS | {"blocks": [2, 3, 4], "incomparable_first_queries": true} |
| DRC-04 | Partition cover has an intermediate Moore domain | PASS | {"domain_sizes": [2, 3, 4], "middle_closed_under_complement": false} |
| DRC-05 | Set questions can grow at unchanged singleton distinguishability | PASS | {"domain_sizes": [5, 6, 8], "singleton_observations_equal": true} |
| DRC-06 | One extra answer does not preserve the temporal language | PASS | {"one_question_blocks": 2, "language_blocks": 3, "denotations": 8} |
| DRC-07 | Independent six-state quotient, all partitions and denotations | PASS | {"partitions": 203, "stable": 4, "minimum_blocks": 4, "minimizers": 1, "all_language_denotations": 16} |
| DRC-08 | Scalar reversible recoding and missing sign | PASS | {"sample": [-4, -3, -2, -1, 0, 1, 2, 3, 4], "four_scalar_kernels_equal": true, "sign_recovery_from_modulus": false} |
| DRC-09 | Local sections and two anchors do not ensure coherence | PASS | {"route_mismatches": 4, "states": 8, "two_anchors_not_function_identity": true} |
| DRC-10 | Forward and backward completeness are independent | PASS | {"F_forward_backward": [true, false], "G_forward_backward": [false, true]} |
| DRC-11 | A dynamic quotient need not have a dynamic section | PASS | {"set_sections": 2, "transition_preserving_sections": 0} |
| DRC-12 | Statistical sufficiency does not recover an actual history | PASS | {"channel_law_reconstructed": true, "first_bit_error_from_count": "3/16"} |
| DRC-13 | Copying and a fresh observation differ in decision value | PASS | {"single_and_copy_brier": "3/16", "two_fresh_brier": "3/20"} |
| DRC-14 | An intermediate history record has two strict information gains | PASS | {"outputs": [2, 4, 6], "FTS_early_form_excluded": false} |
| DRC-15 | Full information and a restricted decoding budget differ | PASS | {"proper_coordinate_subsets": 15, "full_input_contains_answer": true, "adaptive_lower_bound": "see REVIEW proof; not inferred from fixed subsets"} |
| DRC-16 | Exact nonfactorization may disappear almost surely | PASS | {"exact_decoder": false, "zero_error_almost_sure_decoder": true} |
| DRC-17 | Primary source compression and bounded square counterchecks | PASS | {"compressed_source_bytes": 47514, "decoded_bytes": 175032, "strict_sign_zero_counterexample": 0, "successive_power_witnesses": [4, 16, 256, 65536], "infinite_intersection": "analytical proof in SOURCE_AUDIT; not a finite test"} |
| DRC-18 | Strictly intermediate binary statistical experiment | PASS | {"optimal_01_risks": ["0", "1/4", "1/2"], "strict_intermediate_experiment": true} |
