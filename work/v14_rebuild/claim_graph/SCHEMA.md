# FTS claim graph v1

Этот файл описывает авторитетный машинный слой в `claim_graph.json`. Он является
производным от карточек, таблиц и документов проекта. `source/` остаётся
неизменяемым источником канона v13; граф не повышает статусы и не заменяет
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

- `card` — карточка v13; слой `canonical_v13`.
- `author_statement` — принятые авторские карточки AC-2026-09-19; слой
  `author_canon`, не объединённый с историческим `source/`.
- `claim_group` — адресуемая группа утверждений из `CLAIM_MATRIX.tsv`.
  Гранулярность явно равна `group`: дочерние атомарные claims не выдумываются.
- `claim` — рабочее исследовательское утверждение с явной областью и статусом.
- `source_document` — файл или документ.
- `source_reference` — буквальная, но пока не разрешённая ссылка из реестра.
  В таком случае `resolution_state=unresolved_reference` и
  `missing_reason=нет в артефактах`.
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
