# GRAPH AUDIT — active canonical release

Релиз: `v13_active_graph_reconciled_2026-10-03`. Полное сравнение включает адресаты-карточки, фрагменты и неразрешённые определения.

**Найдено.** 169 карточек, 378 триплетов; предикатов — 33.

**Зависимости.** JSONL: 167; TSV: 167; card-only=0, triple-only=0.

**Вывод.** Циклов предпосылок — 0. Обратные отношения applies_to/has_operator и принадлежность источнику сохраняются отдельно от depends_on.

**Что не закрыто.** Lambda_link, TA1, U12_CHI_PI_BOUNDARY и NODE_SIGNATURES; определения и область должны быть восстановлены. Модели для двух causal/counterfactual требований также остаются обязательствами.

Решения: [GRAPH_RELATION_PATCH.tsv](GRAPH_RELATION_PATCH.tsv), [DEPENDENCY_CYCLE_REVIEW.tsv](DEPENDENCY_CYCLE_REVIEW.tsv), [REFERENCE_RESOLUTIONS.tsv](REFERENCE_RESOLUTIONS.tsv).
Полный разбор: [GRAPH_RECONCILIATION_2026-10-03](../../project_consistency/GRAPH_RECONCILIATION_2026-10-03.md).

## Предикаты

| Предикат | Число |
|---|---:|
| `adopts` | 1 |
| `applies_to` | 2 |
| `asks_branch_of` | 1 |
| `candidate_supports` | 8 |
| `contains` | 7 |
| `contrasts_with` | 5 |
| `defeats_or_tests` | 8 |
| `depends_on` | 167 |
| `does_not_promote_above` | 2 |
| `exports_to` | 3 |
| `has_agentic_gate` | 1 |
| `has_antimode` | 11 |
| `has_antimode_detail` | 1 |
| `has_boundary` | 1 |
| `has_complex_overlay` | 7 |
| `has_core` | 1 |
| `has_family` | 3 |
| `has_local_forbid` | 3 |
| `has_math_expression` | 1 |
| `has_minimal_expression` | 19 |
| `has_next` | 18 |
| `has_operator` | 6 |
| `has_private_expression` | 19 |
| `has_statistical_overlay` | 6 |
| `has_tensor_overlay` | 3 |
| `has_window` | 19 |
| `projects_to` | 7 |
| `promotes_status_of` | 6 |
| `requires` | 2 |
| `requires_mapping_to` | 5 |
| `supports` | 31 |
| `uses_analogy` | 1 |
| `uses_carrier` | 3 |

## Циклы depends_on

Не обнаружены.

## Реестр исходных 34 ссылок

| Решение | Число |
|---|---:|
| `ambiguous` | 1 |
| `card_alias` | 9 |
| `document_set` | 3 |
| `literal` | 7 |
| `missing` | 3 |
| `scope` | 2 |
| `sheet_record` | 9 |
