# Изолированные проверки маршрута — 2026-09-23

Проверки выполнены в одноразовых detached checkout’ах от `HEAD`, созданных в
системной временной папке и удалённых через `git worktree remove`. Рабочие
артефакты не менялись.

| Случай | Изолированное нарушение | Ожидаемый и полученный результат |
|---|---|---|
| Канон | В `source/` добавлена копия `INSTALL.md`, не учтённая MANIFEST | `--only canon_manifest` → exit `1`, `1 extra`. |
| Claim-граф | `source/fts_cards.jsonl` заменён копией другого source-файла | `--only claim_graph` → exit `1`, `stale provenance` с `hash_mismatch`. |
| OQ как вход графа | После PASS-графа `OPEN_QUESTIONS.md` заменён другим текстом | `--only claim_graph` → exit `1`, `stale provenance` для `work/OPEN_QUESTIONS.md`. |
| Трассируемость | Временно убран `audit/CLAIM_MATRIX.tsv` | `--only audit` → exit `1`, `P1 CLAIM_MATRIX_MISSING`. |
| Выгрузка | После `--rebuild-package` единая выгрузка заменена README | `--only research_export` → exit `1`, несовпадающие expected/actual SHA256. |

Дополнительно `--rebuild-package` успешно создал в изолированной копии 20
review-копий, список из 24 checksum-файлов и новую единую выгрузку. После
синхронизации карты OQ и штатной пересборки производных полный маршрут на
реальном рабочем дереве даёт **5/5 PASS** с двумя документированными P2.
