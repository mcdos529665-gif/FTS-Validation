# Consideration brief: ФТС как кандидатный скелет нейросети

- Дата: 2026-09-15
- Контур: neural_skeleton_research_2026-09-15
- Итоговый статус: CONSIDER_AS_CANDIDATE_FUNCTIONAL_SCAFFOLD
- Не утверждается: established architecture, necessary architecture, biological model

## Решение

В объявленной области искусственных обучаемых нейронных архитектур сейчас
достаточно независимых оснований, чтобы рассматривать ФТС как кандидатный
функциональный scaffold — организующий каркас для иерархии представлений,
остатка/refinement, typed state, provenance/revision gate, памяти и
операционального readout.

Формулировка намеренно слабее тезисов «ФТС — уже нейросеть», «ФТС необходима»
или «ФТС описывает мозг».

## Матрица оснований

| Линия | Основание | Сила | Что реально следует |
|---|---|---|---|
| Hierarchy/residual | Rao–Ballard predictive-coding model | direct local bridge | hierarchical feedback + residual can be neural implementation pattern |
| Composition | Neural Module Networks | direct local bridge | reusable modules and task-conditioned assembly are implementable |
| Memory | DNC | alternative/direct architecture | recurrent controller + external memory can support structured tasks |
| Typed absence | NeuMiss, GRU-D | direct local bridges | masks/time-of-observation can be computationally relevant |
| Refinement | Ranzato–Tapparo | direct formal bridge | fixed-language preservation/refinement can be typed and audited |
| M′ | DR-09 finite factor | independent alternative | refinement/minimal factor is not uniquely FTS |
| Symmetry | G-CNN | limiting alternative | phase/group names need explicit actions and laws |
| Biological transfer | predictive-processing critique | limiting | local hierarchy does not imply one whole-brain ladder |
| Internal v0.1 | typed absence/module probe | inconclusive | no general advantage in first simple MLP test |
| Internal v0.2 | provenance/revision/memory | positive local | explicit gate prior improves one held-out synthetic contract |
| v0.2 control | symbolic-gate M′ | exact non-uniqueness | the positive effect is ordinary derived-feature inductive bias |
| Internal v0.3 | two readouts × 1D/2D | positive transfer | the same gate prior transfers across readouts/domains in synthetic data |

## Requirement audit for candidate consideration

| Требование | Evidence | Verdict |
|---|---|---|
| At least four independent component bridges | EVIDENCE_MATRIX.tsv: hierarchy, composition, absence, memory, refinement | PASS |
| Limiting/alternative evidence | MPRIME_AUDIT, G-CNN, predictive-processing critique, O_20 and v0.1 nulls | PASS |
| Explicit executable architecture | ARCHITECTURE_SPEC.md and run_* probes | PASS |
| Capacity-matched comparison | v0.1, v0.2 and v0.3 exact parameter pairs | PASS |
| Independent alternative | finite M′ plus symbolic-gate M′ control | PASS locally; full F3 remains open |
| Transfer beyond one target | v0.3: 1D/2D × readout A/B, 5/5 positive seeds | PASS in synthetic scope |
| Unique FTS necessity | symbolic-gate control reproduces effect exactly | FAIL / not claimed |
| Biological neural model | no neural data or anatomical mapping | NOT ESTABLISHED |

## Правильная сила итогового claim

Допустимо:

> ФТС имеет достаточные компонентные и первые интегральные основания, чтобы
> рассматриваться как кандидатный функциональный scaffold для искусственных
> нейронных архитектур: её роли сопоставимы с известными архитектурными и
> формальными механизмами, а явно заданный gate/memory inductive bias переносится
> между синтетическими readout и domain при capacity matching.

Недопустимо пока:

- «ФТС доказана как скелет любой нейросети»;
- «порядок уровней ФТС необходим»;
- «ФТС лучше DNC, GRU-D, NeuMiss или modular networks»;
- «ФТС описывает нейроанатомию или сознание»;
- повышение статусов канона на основании внешних мостов или synthetic results.

## Что нужно для следующего уровня T3

1. Один общий benchmark contract с FTS-skeleton, raw M′, symbolic-gate M′,
   DNC/GRU-D/NeuMiss или релевантными domain baselines.
2. Полная стоимость derived fields, memory, preprocessing, training и inference.
3. Preregistered ablations каждой заявленной роли.
4. Независимый dataset/domain или независимая реализация.
5. Предсказание, которое проигрывает при замене ФТС на сильную альтернативу.

До выполнения этих пунктов статус остаётся candidate functional scaffold,
но порог «можно рассматривать» пройден.

## Новый архитектурный инкремент: чередование суммирования и различения

Рабочее правило DN-0003 теперь разложено в research-layer specification:

    Aggregate → Normalize/Compete → Distinguish → Residual/Memory → Update

Чтобы приблизить ФТС к будущей электронной нейросети, ей нужны явные:

1. typed algebra of aggregators;
2. typed algebra of distinction/competition;
3. residual/refinement witness;
4. recurrent memory with provenance/revision;
5. normalization and stability law;
6. event-driven/local hardware mapping;
7. local or hybrid learning rule;
8. cost model and ablation suite.

Спецификация и 11 внешних мостов сохранены в:

- SUM_DISTINCTION_SPEC.md
- SUM_DISTINCTION_EVIDENCE.tsv
- SUM_DISTINCTION_PROTOCOL.md

Этот инкремент не повышает статусы и не превращает DN-0003 в новую аксиому.
