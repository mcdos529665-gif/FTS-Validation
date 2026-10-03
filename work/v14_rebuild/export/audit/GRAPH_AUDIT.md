# GRAPH AUDIT — v13 immutable export

## Найдено → зависимости → вывод → что не закрыто

**Найдено.** Канон содержит 161 карточку и 238 триплетов; уникальных предикатов — 27, дубликатов триплетов — 0.

**Зависимости.** Ссылкой на сущность считается объект, совпадающий с ID карточки. Буквальные объекты (`has_window`, `has_antimode`, scope labels, имена файлов и формулировки требований) не объявляются битой ссылкой. Все неразрешённые entity-ссылки перечислены в `CANON_REFERENCE_PATCH.tsv`.

**Вывод.** JSONL `depends_on` содержит 130 разрешённых entity-рёбер, TSV — 29. В TSV отсутствует 102 карточных рёбер; 1 TSV-ребро отсутствует в карточке. Это P2-разрыв двух представлений, а не основание молча считать TSV полным графом. Механический patch-план записан в `GRAPH_RELATION_PATCH.tsv`.

**Что не закрыто.** `source/` неизменяем. Применение patch-плана требует нового workbook round-trip и MANIFEST; циклы должны быть подтверждены автором как взаимные определения или разорваны направленным основанием.

## Предикаты и тип объектов

| Предикат | Всего | Entity-ID | Literal/неразрешённый | Правило |
|---|---:|---:|---:|---|
| `asks_branch_of` | 1 | 1 | 0 | entity reference |
| `candidate_supports` | 8 | 0 | 8 | literal/mixed по фактическому ID |
| `contains` | 6 | 6 | 0 | entity reference |
| `contrasts_with` | 5 | 5 | 0 | entity reference |
| `defeats_or_tests` | 8 | 0 | 8 | literal/mixed по фактическому ID |
| `depends_on` | 43 | 29 | 14 | entity reference |
| `does_not_promote_above` | 2 | 1 | 1 | entity или literal scope |
| `exports_to` | 3 | 0 | 3 | literal/mixed по фактическому ID |
| `has_agentic_gate` | 1 | 1 | 0 | entity reference |
| `has_antimode` | 11 | 0 | 11 | literal/mixed по фактическому ID |
| `has_antimode_detail` | 1 | 1 | 0 | entity reference |
| `has_boundary` | 1 | 1 | 0 | entity reference |
| `has_complex_overlay` | 7 | 7 | 0 | entity reference |
| `has_core` | 1 | 1 | 0 | entity reference |
| `has_local_forbid` | 1 | 1 | 0 | entity reference |
| `has_minimal_expression` | 19 | 19 | 0 | entity reference |
| `has_next` | 18 | 18 | 0 | entity reference |
| `has_operator` | 6 | 5 | 1 | entity reference |
| `has_private_expression` | 19 | 19 | 0 | entity reference |
| `has_statistical_overlay` | 6 | 6 | 0 | entity reference |
| `has_tensor_overlay` | 3 | 3 | 0 | entity reference |
| `has_window` | 19 | 0 | 19 | literal/mixed по фактическому ID |
| `projects_to` | 7 | 7 | 0 | entity reference |
| `promotes_status_of` | 6 | 6 | 0 | entity reference |
| `requires` | 2 | 0 | 2 | literal/mixed по фактическому ID |
| `supports` | 31 | 4 | 27 | literal/mixed по фактическому ID |
| `uses_carrier` | 3 | 3 | 0 | entity reference |

## Циклы card.depends_on

- `ADD_MIRROR_WINDOW ↔ ADD_ZERO_BOUNDARY`
- `M_07 ↔ U7_MATH_LOCAL_FORBID`
- `OP_WindowClose ↔ U7_WINDOW_CORE`

Три SCC не являются вычислительной ошибкой, но опровергают предположение, что `depends_on` уже является DAG. До авторского решения они маркируются как P2 и не используются для доказательства порядка оснований.

## Асимметрия depends_on

- Card-only edges: 102 (`ADD_TRIPLE` в patch-плане).
- Triple-only edges: 1 (`REVIEW_TRIPLE` в patch-плане).
- Конфликт: `ADD_U12_CIRCLE →depends_on→ U_10` есть только в TSV.

## Active register repair — 2026-10-03

The previous U7 mathematical SCC is now `A_07 ↔ U7_MATH_LOCAL_FORBID`.
`M_07` keeps the September logical form; `U7_LOGIC_GROUPING` is its distinct
constraint. The three documented SCCs remain three, with the mathematical
record correctly named. Current representation drift: 97 card-only and
1 triple-only dependency. These remain P2 limitations; no new unresolved
reference or status promotion is introduced. Historical measurements above
retain their original scope.
