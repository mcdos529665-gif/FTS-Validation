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
