# Claim graph change report

Текущий research-layer инкремент преобразован в адресуемые claims/evidence
и сохранён с provenance. Это отчёт изменения машинной карты, не решение о
повышении статуса ФТС.

## Claims

- `claim_dr10_qg_witness`: DR10_QG_WITNESS — Для q и r условие q(a)=q(b) и r(a)≠r(b) эквивалентно строгому уточнению ~(q,r) ⊊ ~q в объявленной математической области. — status `research_layer_derived; role_sufficiency_not_proved`; scope `research-layer; фиксированные q,r; не St_FTS`.
- `claim_neural_t2_scaffold`: NEURAL_T2_SCAFFOLD — ФТС имеет достаточные компонентные и первые интегральные основания, чтобы рассматриваться как кандидатный функциональный scaffold для искусственных нейронных архитектур. — status `candidate_functional_scaffold`; scope `искусственные обучаемые нейронные архитектуры; synthetic scope`.
- `claim_neural_t3_not_verified`: NEURAL_T3_NOT_VERIFIED — Поддержанный архитектурный claim T3 и биологическая модель пока не установлены. — status `T3_not_verified; biological_model_not_established`; scope `единый benchmark contract; capacity-matched evidence; отдельный neuroscience protocol`.

## Bridges

- `NB-001`: `NEURAL_T2_SCAFFOLD` —supported_by→ `NN-E01`; scope `component-level only`; status effect `no St_FTS change`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/EVIDENCE_MATRIX.tsv#NN-E01`.
- `NB-002`: `NEURAL_T2_SCAFFOLD` —supported_by→ `NN-E03`; scope `memory and structured tasks`; status effect `no St_FTS change`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/EVIDENCE_MATRIX.tsv#NN-E03`.
- `NB-003`: `NEURAL_T2_SCAFFOLD` —supported_by→ `neural_v03_transfer`; scope `1D/2D synthetic domains; capacity matched`; status effect `candidate support only`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/TARGET_INDEPENDENT_AUDIT.md#v0.3 transfer result`.
- `NB-004`: `NEURAL_T2_SCAFFOLD` —limited_by→ `neural_symbolic_gate_control`; scope `matched synthetic control`; status effect `limits uniqueness`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/GATE_CONTROL_RESULTS.md#v0.2 symbolic-gate control`.
- `NB-005`: `NEURAL_T2_SCAFFOLD` —limited_by→ `neural_typed_absence_nonconfirmation`; scope `one limited internal test`; status effect `limits one component claim`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/INTERNAL_EVIDENCE.md#I2 — O_20 typed-absence test`.
- `NB-006`: `NEURAL_T3_NOT_VERIFIED` —limited_by→ `neural_skeleton_consideration`; scope `benchmark, cost, ablations and independent prediction`; status effect `T3 remains unverified`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/CONSIDERATION_BRIEF.md#Что нужно для следующего уровня T3`.
- `NB-007`: `DR10_QG_WITNESS` —refined_by→ `deep_report_10_integration`; scope `fixed q,r mathematical scope`; status effect `no St_FTS change`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/DEEP_RESEARCH_REPORT_10_INTEGRATION.md#Уже определённые конструкции рабочего слоя`.

## Ограничения

- Все bridges помечены curated/extracted и не меняют `St_FTS`.
- Deep Research (10) представлен как уточнение research-layer claim и boundary, а не как новая эмпирика.
- Внутренние neural результаты остаются synthetic/internal evidence с локальной областью.
