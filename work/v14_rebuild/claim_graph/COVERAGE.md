# FTS claim graph — coverage

Граф собран детерминированно из перечисленных в `input_digests` артефактов.
Он сохраняет канон, авторский supplement и research-layer раздельно.

## Покрытие

- `canonical_cards`: 161
- `canonical_triples`: 238
- `canonical_card_depends_on`: 156
- `canonical_input_assertions`: 420
- `author_cards`: 5
- `author_triples`: 18
- `audit_claim_groups`: 25
- `audit_findings`: 20
- `patterns`: 31
- `open_question_anchors`: 76
- `mapped_open_questions`: 60
- `verification_nodes`: 62
- `external_evidence_nodes`: 21
- `internal_evidence_nodes`: 7
- `research_claims`: 10
- `curated_research_bridges`: 14
- `nodes`: 756
- `edges`: 1550
- `unresolved_references`: 34

## Границы

- `CLAIM_MATRIX.tsv` покрыт на уровне 25 групп; атомарные claims внутри групп не выдумываются.
- C01–C62 представлены как verification-evidence; их PASS не повышает St_FTS.
- Неразрешённые ссылки сохранены как `source_reference`/`unresolved_reference` с `нет в артефактах`.
- Внешние evidence-строки без явного bridge остаются evidence-узлами без поддержки конкретного claim.
- Graphify не используется как authoritative storage, поскольку его простой граф может схлопывать параллельные relation-варианты.

## Обработанные слои

- `canonical_v13`: карточки и все направленные триплеты/`depends_on`.
- `author_canon`: AC-2026-09-19 с отдельным provenance и статусом авторского принятия.
- `audit`: claims, findings, patterns, OQ и проверки.
- `external_research` и `internal_research`: evidence matrices и внутренние результаты.
- `research_bridge`: только явно записанные curated bridges из `RESEARCH_CLAIM_BRIDGES.tsv`.

Основной файл: `claim_graph.json`. Схема: `SCHEMA.md`.
