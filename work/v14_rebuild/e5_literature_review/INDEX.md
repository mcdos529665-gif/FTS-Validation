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
`WAVE_0_STATUS.md`, and `RESEARCHRABBIT_HANDOFF.md` form the frozen pre-adjudication
package. The researcher-only second pass begins in `SCREENING_RESEARCHER.tsv`.

Восстановленные самостоятельные проекты из единой исследовательской выгрузки:

- `DEEP_RESEARCH_REQUESTS_CONNECTIVITY.md` — готовые задания ChatGPT Deep
  Research для симметричного поиска подтверждений, ограничений, альтернатив и
  опровержений каждого основания O_01…O_20; `DR-00` маршрутизирует
  arXiv:cs/0401016v3 к O_07/O_08/O_09/O_14 без повышения статуса;
- `COUPLING_MAP.md` — предварительная карта сопряжений внешних работ с ФТС;
- `PROTOCOL_AMENDMENT_003.md`, `BLACKWELL_BRIDGE.md`,
  `check_blackwell_bridge.py`, `BLACKWELL_BRIDGE_REPORT.md` — ограниченный
  Blackwell-мост У4→У5→У6 (`candidate_external_bridge`);
- `PROTOCOL_AMENDMENT_004.md`, `TYPED_ABSENCE_BRIDGE.md`,
  `LIFT_TYPING_PROJECT.md`, `check_absence_lift_projects.py`,
  `ABSENCE_LIFT_REPORT.md` — раздельные кандидаты для `0_A` и `[OP_Lift]`.

Эти документы восстановлены как исследовательский слой. Они не завершают второй
screening, не запускают adjudication и не меняют `St_FTS`.
