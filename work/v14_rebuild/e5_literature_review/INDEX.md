# E5 · систематический литературный обзор

Рабочий контур для `oq-systematic-literature-review`. Исторический каталог
`../audit/` и его `LITERATURE_MATRIX.tsv` не изменяются.

Порядок: заморозить протокол → выполнить discovery → проверить и дедуплицировать
seed-set → ручной ResearchRabbit round-trip → два независимых screening-прохода →
явная adjudication → evidence matrix → ограниченная novelty boundary.

Ни один внешний источник автоматически не меняет `St_FTS` или статус карточки.
Передача наружу по умолчанию ограничена поисковыми строками и библиографическими
метаданными.

Wave 0: `PROTOCOL_AMENDMENT_001.md`, `PROTOCOL_AMENDMENT_002.md`,
`SEARCH_LOG.tsv`, `CANDIDATES.tsv`, `SCREENING_CODEX.tsv`, `PROVIDER_STATUS.md`,
`WAVE_0_STATUS.md` и `RESEARCHRABBIT_HANDOFF.md` образуют замороженный пакет до
adjudication. Независимый второй проход исследователя начинается в
`SCREENING_RESEARCHER.tsv`.

Шесть переданных полнотекстовых работ добавлены по
`IMPORT_PLAN.md`. Общий паспорт и контрольные суммы находятся в
`PAPER_INTAKE.tsv`, неизменённые OCR-оригиналы и русские читательские досье —
в `papers/`. Предварительные, неканонические точки сопряжения собраны в
`COUPLING_MAP.md`.

По отдельной авторской команде и поправке `PROTOCOL_AMENDMENT_003.md` оформлен
узкий `BLACKWELL_BRIDGE.md`: типизированный кандидат для У4–У6, точный пример,
контрпримеры и `check_blackwell_bridge.py`. Это не общий E5-синтез и не снимает
гейты второго screening-прохода и adjudication.

По поправке `PROTOCOL_AMENDMENT_004.md` добавлены ещё два раздельных проекта:
`TYPED_ABSENCE_BRIDGE.md` задаёт кандидатную запись `0_A` через тип, локус,
механизм, provenance и свидетельство; `LIFT_TYPING_PROJECT.md` задаёт паспорт
категориальной типизации `[OP_Lift]` и явно отделяет его от WFS lifting
property. Точные конечные пробы TA-01…TA-05 и LT-01…LT-05 находятся в
`check_absence_lift_projects.py` и `ABSENCE_LIFT_REPORT.md`. Эти проекты также
не меняют screening, общий синтез или `St_FTS`.
