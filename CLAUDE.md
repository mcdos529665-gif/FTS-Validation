# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Рабочий язык проекта — русский. Остальной файл написан по-русски, в тон
> `PROJECT_INSTRUCTIONS.md` и `work/`.

## Что это за репозиторий

Это **не обычная кодовая база, а проект развития теории ФТС** («лестница
различимости») с редактируемой активной канонической выгрузкой. Python-скрипты —
инструменты доступа и машинной проверки, а не продукт. «Продукт» — это статья,
карточки и решения теории в `work/` (прежде всего пересборка в `work/v14_rebuild/`).

Главный архитектурный принцип: **диск — источник истины, контекст LLM — расходник.**
Сессия может оборваться по лимиту токенов в любой момент, и потеря не должна стоить
больше одного маленького инкремента. Из этого вытекает весь рабочий процесс
(write-through на диск, STATE-handoff, частые коммиты, точечный доступ к канону).

## Первым делом в каждой сессии (обязательно)

Перед любой работой прочитать, в этом порядке:
1. **`AGENTS.md`** — короткий контракт (он же подаётся в контекст автоматически;
   повторно перечитывать не нужно).
2. **`work/STATE.md`** — «где мы»: текущая цель, следующий шаг, открытые нити.
3. **`work/notation.md`** — смысл перегруженных символов ФТС (`¬A`/`0_A`/`−A`,
   `⊖`/`Rot`, регистры М/Ч/А, каналы Q/ratio, оверлеи).

Дальше — по задаче: нужный раздел `PROJECT_INSTRUCTIONS.md` (канон, статусы,
Wolfram, академический поиск, команды, проверки, граф, arXiv, сохранение) и
`work/DOCUMENT_MAP.md` (куда читать и куда записывать новый материал). Ссылки
рекурсивно не раскрывать.

CLAUDE.md эти файлы не дублирует — он на них указывает и фиксирует то, что между
ними не записано.

## Окружение

- Нужен Python с **`sympy`**. По `work/PROJECT_CONSISTENCY.md` на машине автора
  системный `C:/Python313` sympy **не имеет**; рабочий интерпретатор — Python 3.11
  (SymPy 1.14.0). Запускать так: `py -3.11 -X utf8 ...` (или поставить нужный
  Python первым в PATH). Иначе `verification*.py` упадут с `ModuleNotFoundError`.
- Зависимости перечислены в `requirements.txt` в корне: `sympy` — для проверок
  теории; `numpy`/`pandas`/`scipy`/`scikit-learn` — для эксперимента o20.
- На Windows-консоли всегда **`-X utf8`** (иначе `UnicodeEncodeError` на кириллице).
- Git: **не включать `core.autocrlf`** (см. инвариант 2).
- Graphify (опциональная навигация) запускается отдельным интерпретатором, путь
  указан в `work/PROJECT_CONSISTENCY.md`; источником истины он не является.

## Команды

Запускать из корня репозитория.

```
python -X utf8 tools/verify.py --strict         # целостность канона по SHA256 (ОБЯЗАН быть 0 mismatch, 0 extra)
python -X utf8 tools/query.py stats             # обзор карточек по типам и статусам
python -X utf8 tools/query.py card U_07         # карточка + входящие/исходящие рёбра
python -X utf8 tools/query.py context U_07 1    # карточка + соседи, готово вставить в сессию
python -X utf8 tools/query.py find фаза         # поиск по тексту/заголовку/символу
python -X utf8 tools/query.py deps OP_Lift      # транзитивное depends_on
python -X utf8 tools/oq_pool.py --write         # пулы пересекающихся открытых вопросов → work/OQ_POOLS.md
                                                # (курируемый слой поверх — work/OQ_TRIAGE.md)

python -X utf8 tools/check_project_consistency.py   # одна команда: пять обязательных проверок (см. work/PROJECT_CONSISTENCY.md)
python -X utf8 tools/claim_graph.py validate        # граф утверждений (build|validate|coverage|search|query|path)

python -X utf8 work/v14_rebuild/verification.py                  # «тесты» теории: C01..C62 целиком
python -X utf8 work/v14_rebuild/verification.py --only C06 C29   # выбранные проверки + их предпосылки (ЧАСТИЧНАЯ диагностика)
python -X utf8 work/v14_rebuild/probes.py                        # кандидат-пробы (НЕ сьют; FAIL → строка в work/REFUTED.md)
python -X utf8 work/v14_rebuild/crosscheck.py grounds            # сверка ссылок статьи с каноном (grounds|levels|sp|fails|find <q>|keys)
python -X utf8 work/v14_rebuild/o20/run_o20.py                   # внешний эмпирический тест (по пред-регистрации)

python -X utf8 tools/import_from.py "C:\путь\к\выгрузке"         # доустановка/обновление канона из папки + verify
```

### Проверки C-63…C-99 (отдельные скрипты)

Эти проверки **не входят** в `verification.py` (он покрывает C01–C62) и, согласно
`work/PROJECT_CONSISTENCY.md`, в общий маршрут `check_project_consistency.py`.
Запускать вручную, каждый скрипт отдельно:

```
python -X utf8 work/v14_rebuild/verification_c63.py           # C-63…C-76 (двухканальное чтение)
python -X utf8 work/v14_rebuild/verification_c77.py           # C-77…C-84 (окна и номера уровней)
python -X utf8 work/v14_rebuild/verification_c85.py           # C-85…C-92 (окна разной длины, симметрия)
python -X utf8 work/v14_rebuild/verification_c93.py           # C-93…C-95
python -X utf8 work/v14_rebuild/verification_c96.py           # C-96…C-99 (верхние уровни)
python -X utf8 work/v14_rebuild/verification_windows_table.py # сверка work/v14_rebuild/windows_table.tsv
```

(Результаты на 2026-10-05: 14, 8, 8, 3, 4 PASS и сверка таблицы окон — PASS.)

### Что означает FAIL

`verification.py` — **тест-сьют теории**: каждое формальное утверждение статьи
привязано к проверке `C-NN`. Код возврата: 0 — все PASS; 1 — FAIL; 2 — ERROR/NOT_RUN.
Сейчас **62 PASS / 0 FAIL**. FAIL **не равен контрпримеру**: сначала диагностика
причины (см. `PROJECT_INSTRUCTIONS.md#status`); только воспроизводимый контрпример
к точному утверждению в его области лишает утверждение статуса `formal_math_fact`.
Частичный прогон `--only` не заменяет полный перед завершением формальных правок.

## Архитектура и поток данных

- **`source/`** — **активный редактируемый канон** (релиз
  `v13_active_logic_provenance_2026-10-03`: **169 карточек, 378 триплетов, 54
  листа**). Целостность задана `MANIFEST.json` + SHA256. Прямые правки разрешены;
  после них — обновить MANIFEST и производные (`tools/rebuild_canon.py`, см.
  `PROJECT_INSTRUCTIONS.md#canon`). Корпус велик (дамп ≈ 824 КБ, workbook ≈ 1 МБ) —
  целиком в контекст не грузить, только через `tools/query.py`. Модель карточки
  (`fts_cards.jsonl`): `id, type, status, title, symbol, text, depends_on, tags, ...`;
  граф — в `fts_triples.tsv` (`subject  predicate  object`).

- **`tools/`** — `verify.py` (SHA256-сверка), `query.py` (точечный graph-retrieval
  без БД), `import_from.py`, `rebuild_canon.py`, `claim_graph.py`,
  `check_project_consistency.py`, `build_research_export.py`, `oq_pool.py` и др.
  ROOT вычисляется от `__file__`, запуск работает из любого cwd.

- **`work/`** — **вся разработка**. `STATE.md` (handoff), `DECISIONS.md` (журнал
  решений), `OPEN_QUESTIONS.md` (очередь инкрементов), `REFUTED.md`,
  `notation.md`, `AUTHOR_CANON.md` и `author_canon/` (принятые авторские поправки).

- **`work/v14_rebuild/`** — **активный проект**: `FTS_v14_paper.md` (научная
  статья — основной артефакт), `verification.py` + `verification_c*.py`,
  `status_patch_v14.md`, `FTS_v14_register_map.md`, `red_team_F3.md`,
  `claim_graph/` (авторитетный граф утверждений), `audit/`, `e5_literature_review/`,
  `o20/` (внешний эмпирический тест: `PREREGISTRATION.md` коммитится ДО прогона),
  `addendum_2026-10-04_*.md` (текущие исследовательские пакеты).

Связи между артефактами: утверждение в `paper.md` → проверка `C-NN` → ссылка на
`[карточка ID]`/`[лист row]` в `source/`. Разрывать эту цепочку нельзя (см.
no-smuggling ниже).

## Агенты и навыки

- `.claude/agents/fts-routine.md` — субагент (haiku) для механического запуска
  разрешённых скриптов и возврата вывода без интерпретации. Не для оценки
  содержания, смены статусов, правок и мутирующих команд.
- `.agents/skills/` — `fts-wolfram-audit` (независимая CAS-проверка точного
  математического предиката), `fts-academic-research` (внешнее обоснование,
  `[внешнее]`), `fts-graph-guide` (ответы по графу утверждений),
  `arxiv-source-import`. Формат этих навыков — Codex; при необходимости читать их
  `SKILL.md` вручную или скопировать в `.claude/skills/`.
- `.claude/worktrees/` — старые рабочие каталоги; при поиске их дубликаты
  игнорировать.

## Инварианты, которые нельзя нарушать

1. **Canon is editable.** Править или заменять `source/` можно по необходимости
   текущей задачи без отдельного разрешения автора. Следовать
   `PROJECT_INSTRUCTIONS.md#canon`; обновлять MANIFEST и производные. Прежние
   правила неизменяемости отменены.

2. **Нормализация переводов строк в git ОТКЛЮЧЕНА** (`core.autocrlf=false` +
   `.gitattributes`: `source/** -text`, `*.tsv -text`, `*.jsonl -text`). SHA256
   требует байтовой идентичности. **Не включай autocrlf и не снимай `-text` с
   `source/`** — иначе verify покажет mismatch на ровном месте. Каталоги `source/`
   внутри статей arXiv — неизменяемые первоисточники.

3. **No-smuggling (главный риск теории).** У понятий ФТС нет априорного смысла в
   обучающих данных — нельзя молча подставить стандартный матсмысл перегруженного
   термина. Любой нетривиальный вывод помечать источником: `[карточка ID]`,
   `[триплет s→p→o]`, `[лист row]` либо `[внешнее]`. При конфликте внешнего знания
   с каноном **побеждает канон** (расхождение — в `work/EXTERNAL_CONFLICTS.md`).
   Чего нет в артефактах — писать дословно `нет в артефактах`, не выдумывать.

4. **Не смешивать сущности:** `¬A` ≠ `0_A` ≠ `−A`; `candidate`/`overlay` ≠
   `canonical_strict`; `phase ≠ −A`; `branch access ≠ Lift`; `array ≠ tensor`
   (пока не задан закон преобразования); М-регистр ≠ Ч-регистр ≠ оверлей.
   Полный список — в `AGENTS.md` и `work/notation.md`.

5. **Статусная дисциплина.** Повышение статуса — только через карточки `SP_*` и
   критерии К1–К5, с подтверждением в графе. Авторское принятие, математическое
   доказательство и эмпирическое подтверждение — **разные оси**. Предложения
   ассистента не приписываются автору по факту записи в `source/`. `SP_LIMITS`
   фиксирует пересматриваемые пробелы доказательств, а не вечный запрет.

6. **Формат вывода для анализа:** `Найдено → зависимости → вывод → что не закрыто.`

## Конец сессии (ритуал, при приближении лимита токенов)

1. Обновить `work/STATE.md`: что сделано, что в работе, следующий шаг, открытые
   нити — указателями, не пересказом (лимит стартового чтения — в
   `work/DOCUMENT_MAP.md`).
2. Значимое решение — строкой в `work/DECISIONS.md` (что и почему); отказ/
   опровержение/не-подтверждение — строкой в `work/REFUTED.md` (чем убито, остаток).
3. Закрытый пункт — отметить в `work/OPEN_QUESTIONS.md` со ссылкой на карточку/коммит.
4. `git add` только файлов задачи и осмысленный коммит; каждый шаг — отдельным
   коммитом (откат и diff всегда доступны). Дробить работу на единицы «одна лемма /
   одна карточка за раз»; писать на диск сразу (write-through), а не копить к концу.
