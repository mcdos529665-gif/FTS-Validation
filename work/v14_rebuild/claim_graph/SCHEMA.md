# FTS claim graph v1

Этот файл описывает авторитетный машинный слой в `claim_graph.json`. Он является
производным от карточек, таблиц и документов проекта. `source/` содержит
редактируемый активный канон; граф не повышает статусы и не заменяет
человеческую аргументацию.

## Основная цепочка

```text
OpenQuestion → Claim → grounds_in / verified_by / supported_by / limited_by
             → Level/Card/Source/Evidence → has_status → Assessment
```

Рёбра направленные. Несколько рёбер с одной парой концов разрешены: их отличают
`id`, `relation`, `source_file` и `source_location`. Простое неориентированное
представление Graphify является только просмотром и не считается авторитетным
хранилищем relation-мультимножества.

## Узлы

- `project` — постоянная сущность проекта `FTS` из корневого `PROJECT.json`;
  слой `project_definition`. Содержит задачу, смысл сложности и требования R1–R6.
  Четыре `scope` того же слоя описывают основания, лестницу, уровень и межуровневые
  связи. Статусы научных утверждений задаются в своих слоях.
- `card` — карточка v13; слой `canonical_v13`.
- `author_statement` — принятые авторские карточки AC-2026-09-21 (с историей
  AC-2026-09-19); слой
  `author_canon`, не объединённый с историческим `source/`.
- `claim_group` — адресуемая группа утверждений из `CLAIM_MATRIX.tsv`.
  Гранулярность явно равна `group`: дочерние атомарные claims не выдумываются.
- `claim` — рабочее исследовательское утверждение с явной областью и статусом.
- `source_document` — файл или документ.
- `source_reference` — буквальная, но пока не разрешённая ссылка из реестра.
  В таком случае `resolution_state=unresolved_reference` и
  `missing_reason=нет в артефактах`.
- `source_fragment` — точная запись существующего источника, найденная по
  листу и уникальному ключу либо по уникальному фрагменту. `fragment_record`
  сохраняет свидетельство; это документальный объект, а не новая карточка.
- `scope` — явно заданная область с существующими участниками. Исходная
  связь с областью сохраняет группировку; `contains` задаёт только членство.
- `literal` — буквальное значение с уточнённым типом, включая имена экспортов,
  метки области и требования. Требование не означает наличия реализующей модели.
- `verification` — адресуемая C-проверка или другой формальный протокол.
- `external_evidence` / `internal_evidence` — строка evidence-матрицы или
  внутренний результат с provenance и ограничением.
- `finding` — аудиторская находка, которая может ограничить claim.
- `status_assessment` — оценка claim/card с сохранённым текстом статуса,
  областью, источником и эффектом на St_FTS.
- `open_question`, `pattern`, `program`, `event`, `meta_pattern` — навигационный
  исследовательский слой.

## Отношения

`depends_on`, `has_next`, `projects_to`, `has_minimal_expression`,
`has_private_expression`, `supports`, `promotes_status_of` и остальные
канонные предикаты переносятся буквально из исходных TSV/JSONL.

`depends_on` задаёт явные предпосылки в собственной области записи; их наличие
не доказывает следствий. JSONL и TSV согласуются по всем адресатам. Цикл этих
предпосылок требует диагноза и вызывает P1. `applies_to` адресует применение
ограничения к выражению/оператору; `has_operator` задаёт представление;
`uses_analogy` сохраняет математическую аналогию в явно указанном регистре.
Обратные связи этих типов не служат доказательными предпосылками.

Реестр разрешения: `audit/REFERENCE_RESOLUTIONS.tsv`. Для отсутствующего или
неоднозначного объекта сохраняются результаты поиска, область и `next_step`.
Статусные фрагменты SP сохраняют историческую оценку и не выполняют нового
повышения. Файлы реестров решений входят в `input_digests` графа; проверка
фрагментов повторно сверяет точный адрес и текст с текущим источником.

Для второго слоя используются:

- `grounds_claim` — claim ссылается на заявленное основание из реестра;
- `verified_by` — claim связан с конкретной проверкой;
- `supported_by` — evidence даёт ограниченную поддержку в указанной области;
- `limited_by` — evidence/finding ограничивает силу или область claim;
- `refined_by` — рабочее утверждение уточнено документом исследования;
- `has_status`, `has_status_before`, `has_status_after` — адресуемая оценка;
- `documented_in` — claim/evidence/assessment имеет точный документальный источник;
- `opens_question`, `directly_traced_to`, `curated_bridge_to` — исследовательская
  навигация, а не доказательство.

`has_research_scope` связывает проект с четырьмя областями задачи;
`addresses_object` указывает их существующие канонические объекты.
Эти рёбра задают предмет исследования и не доказывают принадлежность отдельного
утверждения, связность лестницы или необходимость перехода. Их нельзя использовать
как обходной путь при проверке содержательной адресации claims.

Каждое inferred или curated-ребро содержит `confidence`, `scope`, `status_effect`
и provenance. `EXTRACTED` означает наличие буквальной записи в источнике; это не
означает истинность утверждения.

## Команды

Из корня репозитория:

```text
python -X utf8 tools/claim_graph.py build
python -X utf8 tools/claim_graph.py validate --idempotent
python -X utf8 tools/claim_graph.py coverage
python -X utf8 tools/claim_graph.py query CM-001 --depth 1
python -X utf8 tools/claim_graph.py query NEURAL_T2_SCAFFOLD --depth 1
python -X utf8 tools/claim_graph.py path CM-001 evidence_verification_c01
```

При обрыве маршрута query/path печатает последний узел и причину отсутствия
следующего адресуемого объекта.

Локальный просмотр: `claim_graph.html`. Он читает тот же JSON и показывает
поиск по узлам и relations вместе с provenance, не преобразуя мультимножество
в простой Graphify-граф.

## Active author integration — 2026-10-03

The compatibility layer name `canonical_v13` denotes active canonical records
from source/, currently release `v13_active_graph_reconciled_2026-10-03`.
Author inputs include both 2026-09-21 and 2026-10-03 packages. Canonical and
author-provenance nodes remain separate even when they share a card ID;
status assessment IDs are disambiguated by layer. Bare card-ID queries select
the active canonical node; explicit author node IDs remain available.
`adopts`, `has_family`, `requires_mapping_to`, and `has_math_expression` preserve
stored typed relations; they do not infer carrier identity or automatic status promotion.
