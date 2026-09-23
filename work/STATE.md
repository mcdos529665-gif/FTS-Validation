# STATE — компактный handoff

> Диск — источник истины. Свежая сессия: сначала прочитать
> `PROJECT_INSTRUCTIONS.md`, затем этот файл и `work/notation.md`; после этого
> запускать только нужные точечные проверки.

## Активный канон

- Релиз: `v13_complex_branch_overlay_author_correction_2026-09-21`.
- Основание: `source/MANIFEST.json` (`release_kind: explicit_author_correction`,
  161 карточка, 238 триплетов, 54 листа; base workbook SHA256
  `32a6ed34febaf62a57f6aac986e8caf9716b09b7b8f14bc131e76f81d15acbd6`).
- Последняя read-only сверка: `python -X utf8 tools/verify.py --strict` →
  `13 ok / 0 missing / 0 mismatch / 0 extra`.
- `source/`, исторические релизы, формулировки и статусы в этом техническом
  инкременте не менялись.

## Текущая цель и состояние

Цель — воспроизводимый единый маршрут для канона, claim-графа, статьи и
исследовательской выгрузки. Запускать из корня:

```text
python -X utf8 tools/check_project_consistency.py
```

Маршрут read-only. На 2026-09-23 он даёт `3/5` обязательных PASS: канон,
claim-граф (`420/420` assertions, `idempotent=true`) и C01–C62 проходят;
аудит и экспорт корректно завершаются с ненулевым кодом из-за перечисленных
ниже P1. Полный контракт, коды и восстановление —
`work/PROJECT_CONSISTENCY.md`.

## Блокеры и незавершённая работа

1. `oq-u6-u7-compositional-semantics`: очередь фиксирует `partial`, а
   `PATTERN_OQ_MAP.tsv` — `open`. Это содержательное состояние, которое не
   выбирается автоматически. Оба источника и нужное решение записаны в
   `work/project_consistency/BLOCKERS_2026-09-23.md`.
2. Чистый checkout от `HEAD` не содержит integration Report-10, на который
   ссылается claim-граф, и ожидает иной SHA256, чем текущая неотслеживаемая
   версия. Нельзя выбирать версию report или пересобирать граф до решения по
   provenance; точные hashes записаны в `BLOCKERS_2026-09-23.md`.
3. Исходные незакоммиченные рабочие изменения сделали review-пакет и
   `CHECKSUMS.sha256` неактуальными. Они намеренно не включаются в текущий
   технический коммит; граница зафиксирована в
   `work/project_consistency/BASELINE_UNFINISHED_2026-09-23.md`.
4. После решения по пунктам 1–2 владелец рабочих изменений должен явно выполнить
   `python -X utf8 tools/build_research_export.py --rebuild-package` и, если
   менялись входы graph, `python -X utf8 tools/claim_graph.py build`; затем
   повторить единый маршрут. Graphify обновлять отдельно только штатным
   runtime-командой из `PROJECT_CONSISTENCY.md`.

## Содержательный следующий шаг вне технического инкремента

Для У6/У7 остаётся исполнимая композиционная семантика, сохраняющая составной
исход; не сворачивать актуальные авторские синтаксические деревья обычной
булевой редукцией. См. `work/OPEN_QUESTIONS.md` (якорь выше),
`work/v14_rebuild/u4_u7_bridge_2026-09-22/REVIEW.md` и датированные записи
`work/DECISIONS.md`. Выбор ресурса У7 и статус OQ требует автора; новая
теоретическая позиция здесь не принята.

## Быстрые ссылки и история

- Инструкция и границы автоматизации: `work/PROJECT_CONSISTENCY.md`.
- Технические блокеры: `work/project_consistency/BLOCKERS_2026-09-23.md`.
- Исходная граница dirty-tree: `work/project_consistency/BASELINE_UNFINISHED_2026-09-23.md`.
- Полная прежняя история STATE сохранена без редактирования:
  `work/state_history/STATE_2026-09-23_before_project_consistency.md`
  (SHA256 `c5cda179490cf9f79772013fd42a2b0fd4a64bc4a73b9c0285810a65d72cb511`).
- Очередь содержательной работы: `work/OPEN_QUESTIONS.md`; решения:
  `work/DECISIONS.md`; авторский мандат:
  `work/v14_rebuild/AUTHOR_CYCLE_CHARTER_2026-09-13.md`.
