# Claim graph change report

Текущий research-layer инкремент преобразован в адресуемые claims/evidence
и сохранён с provenance. Это отчёт изменения машинной карты, не решение о
повышении статуса ФТС.

## Claims

- `claim_dn_20260922_absence_lift`: DN_20260922_ABSENCE_LIFT — В рабочем авторском чтении внутреннее отсутствие связано с отказом выполнять функцию, а включение отсутствия в собственный контур является необходимым, но не достаточным условием… — status `author_clarification; working_layer; no St_FTS promotion`; scope `рабочий слой ФТС; DN-0017 и DN-0020`.
- `claim_dn_20260922_geometry_self`: DN_20260922_GEOMETRY_SELF — Линия У6–У12 и тороидальная опора Я остаются candidate/analogy_only: совпадение формул не устанавливает переходы, носитель, Я или сознание. — status `candidate_analogy_only; carrier_and_role_unresolved`; scope `рабочий слой ФТС; DN-0026 и DN-0027`.
- `claim_dn_20260922_internal_contour`: DN_20260922_INTERNAL_CONTOUR — В рабочем чтении вопрос, Вера, проекция, внутренний мотиватор, свобода инструмента и скорость/фундаментальность образуют кандидатный внутренний контур без единой выбранной метрики. — status `author_clarification; candidate bridge; no St_FTS promotion`; scope `рабочий слой ФТС; DN-0018, DN-0019, DN-0021, DN-0022, DN-0025`.
- `claim_dn_20260922_sensitivity_residual`: DN_20260922_SENSITIVITY_RESIDUAL — Формулы sensitivity и residual из приложенных разборов сохраняются как внешние кандидатные предложения и не устанавливают новый уровень, Lift или early exit. — status `external_candidate; typed_scope_required; no St_FTS promotion`; scope `research-layer; external attachments; DN-0023 и DN-0024`.
- `claim_dr10_qg_witness`: DR10_QG_WITNESS — Для q и r условие q(a)=q(b) и r(a)≠r(b) эквивалентно строгому уточнению ~(q,r) ⊊ ~q в объявленной математической области. — status `research_layer_derived; role_sufficiency_not_proved`; scope `research-layer; фиксированные q,r; не St_FTS`.
- `claim_neural_t2_scaffold`: NEURAL_T2_SCAFFOLD — ФТС имеет достаточные компонентные и первые интегральные основания, чтобы рассматриваться как кандидатный функциональный scaffold для искусственных нейронных архитектур. — status `candidate_functional_scaffold`; scope `искусственные обучаемые нейронные архитектуры; synthetic scope`.
- `claim_neural_t3_not_verified`: NEURAL_T3_NOT_VERIFIED — Поддержанный архитектурный claim T3 и биологическая модель пока не установлены. — status `T3_not_verified; biological_model_not_established`; scope `единый benchmark contract; capacity-matched evidence; отдельный neuroscience protocol`.
- `claim_u4_u7_typed_candidate`: U4_U7_TYPED_CANDIDATE — Переходы У4→У5→У6→У7 имеют совместную конечную candidate-реализацию на типизированном поле, следе выбора, семействе и агрегате при допущениях D1–D6. — status `candidate_model_consistent; assumptions_explicit; no St_FTS promotion`; scope `конечные двухсобытийные трассы; исследовательская модель; не определение ФТС`.
- `claim_u6_q_not_sufficient_for_u7`: U6_Q_NOT_SUFFICIENT_FOR_U7 — В объявленной конечной модели три исхода У7 не факторизуются через одну сводку У6 Q: следы EE и NN имеют Q=4 и разные исходы. — status `formal_model_counterexample; semantic_scope_limited`; scope `конечная модель D1–D6; Q=(Σ_i v_i)^2`.
- `claim_u6_vstar_bridge_underdetermined`: U6_VSTAR_BRIDGE_UNDERDETERMINED — Историческое V*V не задаёт единственный мост к активной У6: квадрат суммы и сумма квадратов оба теряют общий знак, но расходятся на совместном следе. — status `bridge_underdetermined; author_choice_and_typing_required`; scope `исторический M_06; конечные знаковые трассы; внешний математический перевод`.

## Bridges

- `NB-001`: `NEURAL_T2_SCAFFOLD` —supported_by→ `NN-E01`; scope `component-level only`; status effect `no St_FTS change`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/EVIDENCE_MATRIX.tsv#NN-E01`.
- `NB-002`: `NEURAL_T2_SCAFFOLD` —supported_by→ `NN-E03`; scope `memory and structured tasks`; status effect `no St_FTS change`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/EVIDENCE_MATRIX.tsv#NN-E03`.
- `NB-003`: `NEURAL_T2_SCAFFOLD` —supported_by→ `neural_v03_transfer`; scope `1D/2D synthetic domains; capacity matched`; status effect `candidate support only`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/TARGET_INDEPENDENT_AUDIT.md#v0.3 transfer result`.
- `NB-004`: `NEURAL_T2_SCAFFOLD` —limited_by→ `neural_symbolic_gate_control`; scope `matched synthetic control`; status effect `limits uniqueness`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/GATE_CONTROL_RESULTS.md#v0.2 symbolic-gate control`.
- `NB-005`: `NEURAL_T2_SCAFFOLD` —limited_by→ `neural_typed_absence_nonconfirmation`; scope `one limited internal test`; status effect `limits one component claim`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/INTERNAL_EVIDENCE.md#I2 — O_20 typed-absence test`.
- `NB-006`: `NEURAL_T3_NOT_VERIFIED` —limited_by→ `neural_skeleton_consideration`; scope `benchmark, cost, ablations and independent prediction`; status effect `T3 remains unverified`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/CONSIDERATION_BRIEF.md#Что нужно для следующего уровня T3`.
- `NB-007`: `DR10_QG_WITNESS` —refined_by→ `deep_report_10_integration`; scope `fixed q,r mathematical scope`; status effect `no St_FTS change`; source `work/v14_rebuild/neural_skeleton_research_2026-09-15/DEEP_RESEARCH_REPORT_10_INTEGRATION.md#Уже определённые конструкции рабочего слоя`.
- `UB-001`: `U4_U7_TYPED_CANDIDATE` —supported_by→ `u4_u7_probe_20260922`; scope `finite declared model only`; status effect `candidate support only`; source `work/v14_rebuild/u4_u7_bridge_2026-09-22/probe.py#P01–P12`.
- `UB-002`: `U6_Q_NOT_SUFFICIENT_FOR_U7` —supported_by→ `u4_u7_probe_20260922`; scope `Q=(Σ_i v_i)^2 on declared traces`; status effect `formal counterexample in model only`; source `work/v14_rebuild/u4_u7_bridge_2026-09-22/probe.py#P05–P07`.
- `UB-003`: `U6_VSTAR_BRIDGE_UNDERDETERMINED` —supported_by→ `u4_u7_probe_20260922`; scope `two explicit sign-blind translations`; status effect `limits historical bridge`; source `work/v14_rebuild/u4_u7_bridge_2026-09-22/probe.py#P08–P09`.
- `UB-004`: `U4_U7_TYPED_CANDIDATE` —grounds_claim→ `M_04`; scope `active U4 minimum`; status effect `no St_FTS change`; source `work/v14_rebuild/u4_u7_bridge_2026-09-22/REVIEW.md#§1; §3`.
- `UB-005`: `U4_U7_TYPED_CANDIDATE` —grounds_claim→ `M_05`; scope `active U5 minimum`; status effect `no St_FTS change`; source `work/v14_rebuild/u4_u7_bridge_2026-09-22/REVIEW.md#§1; §3`.
- `UB-006`: `U4_U7_TYPED_CANDIDATE` —grounds_claim→ `M_06`; scope `active U6 minimum`; status effect `no St_FTS change`; source `work/v14_rebuild/u4_u7_bridge_2026-09-22/REVIEW.md#§1; §3`.
- `UB-007`: `U4_U7_TYPED_CANDIDATE` —grounds_claim→ `M_07`; scope `active U7 minimum`; status effect `no St_FTS change`; source `work/v14_rebuild/u4_u7_bridge_2026-09-22/REVIEW.md#§1; §3`.

## Ограничения

- Все bridges помечены curated/extracted и не меняют `St_FTS`.
- Deep Research (10) представлен как уточнение research-layer claim и boundary, а не как новая эмпирика.
- Внутренние neural результаты остаются synthetic/internal evidence с локальной областью.
