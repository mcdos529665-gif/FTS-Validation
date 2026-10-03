# Исходные незавершённые изменения — 2026-09-23

Снимок сделан до начала инкремента воспроизводимой проверки. Индекс был пуст;
все перечисленные изменения находились только в рабочем дереве. Это исходный
факт, а не оценка содержимого. Полный прежний `STATE` сохранён в
`work/state_history/STATE_2026-09-23_before_project_consistency.md`.

## Отслеживаемые файлы (`M`)

- `graphify-out/GRAPH_REPORT.md`
- `graphify-out/audit_navigation_manifest.json`
- `graphify-out/graph.json`
- `work/DECISIONS.md`
- `work/EXTERNAL_CONFLICTS.md`
- `work/OPEN_QUESTIONS.md`
- `work/STATE.md`
- `work/v14_rebuild/FTS_v14_paper.md`
- `work/v14_rebuild/claim_graph/claim_graph.html`
- `work/v14_rebuild/claim_graph/claim_graph.json`
- `work/v14_rebuild/code_information_recode_note.md`
- `work/v14_rebuild/export/CHECKSUMS.sha256`
- `work/v14_rebuild/export/FTS_research_project_for_AI.md`
- `work/v14_rebuild/neural_skeleton_research_2026-09-15/ARCHITECTURE_SPEC.md`
- `work/v14_rebuild/neural_skeleton_research_2026-09-15/CONSIDERATION_BRIEF.md`
- `work/v14_rebuild/neural_skeleton_research_2026-09-15/SUM_DISTINCTION_SPEC.md`
- `work/v14_rebuild/questiongain_criterion.md`

## Неотслеживаемые пути (`??`)

- `.codex/config.toml`
- `graphify-out/2026-09-19/`
- `work/deep-research-report (10).md`
- `work/v14_rebuild/neural_skeleton_research_2026-09-15/DEEP_RESEARCH_REPORT_10_INTEGRATION.md`

## Реклассификация после проверки зависимостей

Проверка `input_digests` и `build_research_export.INPUT_PATHS` показала, что
часть исходного списка — не несвязанная работа, а единый уже существовавший
пакет AC-2026-09-21 / Report-10, без которого нельзя воспроизвести активные
graph и export. В отдельный recovery-коммит входят его источники:

- `work/DECISIONS.md`, `work/EXTERNAL_CONFLICTS.md`, `work/OPEN_QUESTIONS.md`;
- `work/v14_rebuild/FTS_v14_paper.md`, `code_information_recode_note.md`,
  `questiongain_criterion.md`;
- `neural_skeleton_research_2026-09-15/{ARCHITECTURE_SPEC.md,CONSIDERATION_BRIEF.md,SUM_DISTINCTION_SPEC.md}`;
- raw `work/deep-research-report (10).md` и его integration-запись;
- синхронизированная `audit/PATTERN_OQ_MAP.tsv` и производные claim-graph,
  review-package и Graphify.

Остаются вне коммита: `.codex/config.toml` и резервный
`graphify-out/2026-09-19/`. Они не являются входами текущего verdict и не
нужны для его воспроизводимости.
