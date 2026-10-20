# Graphify — аудиторская навигация

Этот слой построен детерминированно из `PATTERN_ATLAS.tsv`,
`PATTERN_OQ_MAP.tsv`, `CLAIM_MATRIX.tsv`, `FINDINGS.tsv` и точных якорей
`OPEN_QUESTIONS.md`. Он не является каноном v14 и не меняет статусы ФТС.

## Покрытие

- 31 паттерн(ов) → 97 действующих OQ;
- 25 групп утверждений и 20 находок аудита;
- 7 программ, 12 событий и 4 мета-паттерна;
- 203 новых узлов и 928 новых рёбер.

## Доверие к мостам

- 29 прямых мостов — `EXTRACTED`;
- 131 кураторских мостов — `INFERRED` с confidence 0.55;
- 39 служебных мостов — `EXTRACTED`, но без теоретической статусной силы.

`direct` восстанавливается буквально из `PATTERN_ATLAS.tsv`; `indirect` и
непрямая часть `mixed` остаются явными навигационными гипотезами. Граф предлагает
маршрут чтения, но не заменяет карточку, триплет, лист или аудиторский вердикт.

## Артефакты

- [Pattern Atlas](../work/v14_rebuild/audit/PATTERN_ATLAS.md)
- [Pattern ↔ OQ Map](../work/v14_rebuild/audit/PATTERN_OQ_MAP.md)
- [Claim Matrix](../work/v14_rebuild/audit/CLAIM_MATRIX.tsv)
- [Findings](../work/v14_rebuild/audit/FINDINGS.tsv)
- [Review Conclusion](../work/v14_rebuild/audit/REVIEW_CONCLUSION.md)

Состояние графа: 18311 узлов, 33941 рёбер, community `14`.
