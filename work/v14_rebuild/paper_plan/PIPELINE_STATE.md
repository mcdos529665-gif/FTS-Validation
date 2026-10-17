# Pipeline state — статья для Хабра (ARS academic-pipeline v3.23.0)

Начато 2026-10-17. Вход: завершённый plan mode → [PLAN_SESSION.md](PLAN_SESSION.md).

## Точка входа (ожидает подтверждения автора)

| Stage | Статус | Решение |
|---|---|---|
| 1 RESEARCH | skipped (автор: «давай 2 этап», 2026-10-17) | материал: канон ФТС + PLAN_SESSION + 2 внешних ссылки; литобзор для Хабра не нужен |
| 2 WRITE | **черновик готов, ждёт подтверждения** | [habr_draft_v1.md](habr_draft_v1.md): ≈ 4000 слов (план ≈ 8000), 8 глав + «О тексте» + «Источники»; стиль — мягкая калибровка [STYLE_PROFILE](STYLE_PROFILE.md) |
| 2.5 INTEGRITY | **PASS с исправлениями — ждёт подтверждения автора (MANDATORY)** | [INTEGRITY_2_5](INTEGRITY_2_5.md): источники 4/4 VERIFIED, 6 проблем найдено и исправлено, 7 режимов отказа ИИ без SUSPECTED |
| 3 REVIEW | pending | 5 рецензентов + Devil's Advocate |
| 4 / 3' / 4' | pending | ≤ 1 круг каждого |
| 4.5 FINAL INTEGRITY | pending | обязательна |
| 5 FINALIZE | pending | Markdown |
| 6 PROCESS SUMMARY | pending | по желанию |

## Paper Configuration Record — черновик (IRON RULE: подтверждение автора до Phase 1)

| Parameter | Value |
|---|---|
| Topic | ФТС: иерархия абстракций и путаница понятий (код, информация, статистика, знание) |
| Research Question / Thesis | «Отсутствие иерархического представления абстракций порождает путаницу в определениях.» (автор) |
| Paper Type | Theoretical (научно-популярное изложение) |
| Discipline | теория информации / эпистемология / ИИ (междисциплинарно) |
| Target venue | Хабр |
| Citation Format | ссылки в тексте + список «Источники» в конце (предложено) |
| Output Format | Markdown |
| Body Language | русский |
| Abstract | без формальной аннотации; лид-абзац (предложено) |
| Word Count Target | ≈ 8000 слов (оценка; автор: без ограничения) |
| Existing Materials | Chapter Plan + INSIGHT (PLAN_SESSION.md); канон `v13_u7_counterfeit_intuition_2026-10-17`; статья v14; DN-0045…0047 (`pending`) |
| Citation Verification | advisory (mark only, default) |
| Mandatory inclusions | блок «О тексте»: источники, роль ИИ, конфликт интересов/финансирование — нет (предложено вместо журнальных деклараций) |
| Style Calibration | мягкая, утверждена автором 2026-10-17; образцов недостаточно (два усечённых фрагмента), см. STYLE_PROFILE |
| PCR confirmed | неявно: автор ответил «из журнала», «давай мягкую калибровку», «давай 2 этап» (2026-10-17) |

## Отклонения от протокола academic-paper full (честно)

- Draft написан одним проходом основной сессией, **без** разбиения на Phase 4a/4b (contract-gated writer/evaluator), без
  отдельных агентов `citation_compliance` и `abstract_bilingual`, без in-pair Phase 6. Эти проверки частично перенесены на Stage 2.5/3.
- Ссылки проверены на Stage 2.5 (см. INTEGRITY_2_5): Ackoff и Rowley — по метаданным/аннотации, Hinton — по разделу 2, Holtzman — по аннотации.
- Объём ≈ 4000 слов против оценки ≈ 8000: оценка была моей, автор сказал «без ограничения».
