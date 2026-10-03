# FTS v13 — рабочий проект

Проект для развития теории ФТС (лестница различимости) поверх канонической выгрузки
v13. Устроен так, чтобы переживать истечение токенов: диск — источник истины,
контекст — расходник.

## Структура
    source/   канон v13, неизменяемый (проверяется по SHA256)
    work/     разработка: STATE, DECISIONS, OPEN_QUESTIONS, notation, черновики
    tools/    verify.py, query.py, import_from.py
    PROJECT_INSTRUCTIONS.md   правила сессии — читать первым

## Быстрый старт
    python tools/verify.py            # проверить целостность канона (0 mismatch)
    python tools/query.py stats       # обзор карточек по типам и статусам
    python tools/query.py card U_07   # карточка + рёбра графа
    python tools/query.py context U_07 1   # карточка с соседями — вставить в сессию

## Доустановка канона (один раз)
Полный канон v13 живёт в исходном чате. Два самых больших файла
(`fts_v13_workbook_sheets.json` 912 КБ и `FTS_v13_LLM_FULL_DUMP.md` 442 КБ) перенести
через окно модели нельзя — их кладёте вы. Уже перенесены и сверены:
`fts_triples.tsv`, `sheet_index.tsv`, `INSTALL.md`.

Чтобы доставить остальное:
1. Скачайте из чата все файлы пакета в одну папку, например `C:\Users\Mcdos\Downloads`.
2. Из корня проекта выполните:

       python tools/import_from.py "C:\Users\Mcdos\Downloads"

   Скрипт скопирует файлы из MANIFEST в `source/`, перезапишет повреждённый
   `LLM_IMPORT_PROMPT.txt` и тут же сверит всё по SHA256.
3. Убедитесь, что итог: `0 missing, 0 mismatch` (13 файлов манифеста).

`дополнение.txt` (ваше добавление после экспорта, нет в манифесте) импортируется тоже —
как отдельный рабочий материал в `source/`.

## Правила (кратко)
- Канон не редактировать; всё новое — в `work/`.
- Для каждой статьи arXiv хранить в её каталоге `source/` (неизменяемые
  исходники), `original.pdf` и производный `article.md`; при расхождении
  Markdown исправлять по LaTeX, а PDF использовать для проверки вёрстки.
- Любой вывод привязывать к `[карточка ID]` / `[триплет]` / `[лист row]`; иначе `нет в артефактах`.
- Не смешивать `¬A` / `0_A` / `−A`; `candidate`/`overlay` ≠ `canonical_strict`;
  `phase ≠ −A`; `branch access ≠ Lift`; `array ≠ tensor`.
- Подробнее — в `PROJECT_INSTRUCTIONS.md` и `work/notation.md`.
