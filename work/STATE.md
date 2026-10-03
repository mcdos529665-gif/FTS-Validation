# STATE — текущая точка

Обновлено 2026-10-03. Единое место работы:
`C:/Users/Mcdos/Desktop/FTS_v13_project`.

## Текущая работа

Выполнение плана согласования зависимостей и ссылок:
[результат](project_consistency/GRAPH_RECONCILIATION_2026-10-03.md),
[полный маршрут](project_consistency/GRAPH_CHECKS_2026-10-03.json),
[проверка требований](project_consistency/GRAPH_ACCEPTANCE_2026-10-03.json).

Активный релиз: `v13_active_graph_reconciled_2026-10-03`;
169 карточек, 378 триплетов, 54 листа. Тексты, символы и статусы сохранены.
Карточки и TSV содержат одинаковые 167 зависимостей; расхождение — 0 / 0,
циклов предпосылок — 0. Взаимосвязи сохраняются с уточнёнными типами.
Все 34 исходные ссылки разобраны; четыре точных объекта остаются без определения:
`Lambda_link`, `TA1`, `U12_CHI_PI_BOUNDARY`, `NODE_SIGNATURES`.

## Следующий содержательный шаг

[Определения для четырёх ссылок](OPEN_QUESTIONS.md#oq-graph-reference-definitions)
требуют адресной реконструкции и свидетелей своей области. Сам факт наличия
строки или её адресное исправление не повышает St_FTS. Далее сохраняется
работа с выбранным паспортом из [ответов на 60 OQ](v14_rebuild/e5_literature_review/undermind_60_oq_2026-09-30/ANSWERS_60.md)
и [AUTHOR_ANSWERS_60.md](AUTHOR_ANSWERS_60.md).

Открыты [мост У6/У7](OPEN_QUESTIONS.md#oq-u6-u7-compositional-semantics),
[роли окон](OPEN_QUESTIONS.md#oq-window-family-roles),
[Blackwell](OPEN_QUESTIONS.md#oq-blackwell-canonical-projection),
[Lift](OPEN_QUESTIONS.md#oq-lift-section-and-category),
[код / «ведёт к»](OPEN_QUESTIONS.md#oq-code-link-vs-leads-to) и
[интернализация ярлыка](OPEN_QUESTIONS.md#oq-reflection-label-internalization).

## Происхождение и история

[Слияние и резервные копии](project_consistency/MERGE_2026-10-03.md);
[интеграция AC-2026-10-03](author_canon/2026-10-03/INTEGRATION.md).
Математическое У7 — A_07/U7_MATH_LOCAL_FORBID, логическое — M_07/U7_LOGIC_GROUPING;
операциональное чтение остаётся отдельным. История сохранена в Git,
[решениях](DECISIONS.md) и [авторских поправках](AUTHOR_CANON.md).
