# FTS claim graph — coverage

Граф собран детерминированно из перечисленных в `input_digests` артефактов.
Он сохраняет канон, авторский supplement и research-layer раздельно.

## Покрытие

- `canonical_cards`: 169
- `canonical_triples`: 378
- `canonical_card_depends_on`: 167
- `canonical_input_assertions`: 595
- `author_cards`: 8
- `author_triples`: 32
- `audit_claim_groups`: 25
- `audit_findings`: 20
- `patterns`: 31
- `open_question_anchors`: 80
- `mapped_open_questions`: 64
- `verification_nodes`: 62
- `external_evidence_nodes`: 21
- `internal_evidence_nodes`: 7
- `research_claims`: 10
- `curated_research_bridges`: 14
- `project_entities`: 1
- `declared_research_scopes`: 4
- `nodes`: 802
- `edges`: 1881
- `unresolved_references`: 4

## Границы

- `CLAIM_MATRIX.tsv` покрыт на уровне 25 групп; атомарные claims внутри групп не выдумываются.
- C01–C62 представлены как verification-evidence; их PASS не повышает St_FTS.
- Неразрешённые ссылки сохранены как `source_reference`/`unresolved_reference` с `нет в артефактах`.
- Точные записи книги адресуются как `source_fragment`; scope/literal сохраняют группировку и тип, не создавая новых канонических карточек.
- Решения по ссылкам и отношениям: `audit/REFERENCE_RESOLUTIONS.tsv`, `audit/GRAPH_RELATION_PATCH.tsv`, `audit/DEPENDENCY_CYCLE_REVIEW.tsv`.
- Внешние evidence-строки без явного bridge остаются evidence-узлами без поддержки конкретного claim.
- Graphify не используется как authoritative storage, поскольку его простой граф может схлопывать параллельные relation-варианты.

## Обработанные слои

- `canonical_v13`: карточки и все направленные триплеты/`depends_on`.
- `author_canon`: AC-2026-09-21 и AC-2026-10-03 с отдельным provenance и статусом авторского принятия; прежние уточнения сохраняются исторически.
- `audit`: claims, findings, patterns, OQ и проверки.
- `external_research` и `internal_research`: evidence matrices и внутренние результаты.
- `research_bridge`: только явно записанные curated bridges из `RESEARCH_CLAIM_BRIDGES.tsv`.

Основной файл: `claim_graph.json`. Схема: `SCHEMA.md`.
