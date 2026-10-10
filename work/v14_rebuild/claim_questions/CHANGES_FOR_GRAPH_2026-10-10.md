# Изменения сессии 2026-10-09…10 для внесения в граф

Снимок базового Graphify-графа — коммит `2b9deec` (2026-10-09 15:43, построен от HEAD `eaebf22`). Всё, что
сделано после него, в графе отсутствует. Ниже — список по слоям: что изменилось, какие узлы и связи
добавить или обновить, как проверить. Статусы канона не менялись, кроме текста трёх карточек У12.

Источник: `git diff 2b9deec..HEAD` (33 файла, +4440/−90) и два коммита Codex (`0730dfb`).
Чужие незакоммиченные правки (`STATE.md`, `DECISIONS.md`, `tools/graphify_*.py`) сюда не входят.

## 0. Что уже в графе (не вносить повторно)
Коммиты `008e7fc`, `35e5e12`, `eaebf22` (2026-10-09): C-105…C-108 (`verification_c105.py`), пометки «ветвь»,
статья §3.4/§8.1б/§8.1в/§13 п.8, `clt_u6_note.md`, записи 04/52/38 — граф строился от `eaebf22`.
Проверить только, что узлы `C105…C108` и `candidate_c105` есть.

## 1. Канон (`source/`) — обновить 3 узла карточек, релиз
Коммит `f683340`, релиз `v13_u12_radius_free_2026-10-10` (было `v13_u7_forbid_lifted_2026-10-08b`).
Решение автора 2026-10-08/10: радиус окружности У12 — свободный параметр.

| Карточка | Что изменилось |
|---|---|
| `M_12` | текст: класс `x²+(y−r)²=r²`, r>0 свободный, r=2 — представитель; `symbol` `x*x+(y-r)*(y-r)=r*r` |
| `ADD_U12_CIRCLE` | то же; `depends_on` и статус прежние |
| `SP_U12` | `symbol` изменён; текст и статус прежние |

Действия: обновить `label`/`text` трёх узлов; обновить свойство релиза и `exported_at`/`canonical_update`
(MANIFEST); хэши `fts_cards.*`, `FTS.yaml`, `START_HERE.md`, `sheet_index.tsv` изменились — пересобрать узлы
`source_document`. Связи не менялись. Проверка: `verify.py --strict` 13/13.

## 2. claim_graph (`work/v14_rebuild/claim_graph/`)
Пересобран, 924 узла / 2250 рёбер (число прежнее). Изменились только 3 `sha256` входных файлов и `label`/`text`
двух карточек У12. Действие: перенести обновление; идемпотентность `claim_graph.py validate --idempotent`.

## 3. Журнал нюансов (`work/DIALOGUE_NUANCE_JOURNAL.md`)
| ID | Дата | Автор записи | Суть | Узел/связи |
|---|---|---|---|---|
| `DN-0033` | 2026-10-10 | Codex (`0730dfb`) | У7 обрабатывает ожидание: закрытие модели ожидания 1/0, удержание окна («знаю, чего жду») | `author_statement`; target: `U_07`, `U7_WINDOW_CORE`, `U7_FORGET_CLOSE`, `OP_WindowClose`, `O_15`, paper §§7.1–7.2 |
| `DN-0034` | 2026-10-10 | эта сессия | идея автора: лестница как последовательность элементарных операций симметрии («вдавить, вынуть, сложить 2 в 1, разделить 1 в 2, отразить, повернуть, вывернуть, разложить, продолжить»); вывод ассистента ЛУ7 = ЛУ6 ∨ D(ЛУ6) — `assistant_inference` | `author_statement`; target: paper §8.1б, `ladder_table.md`, `M_04…M_07`, `U7_LOGIC_GROUPING`; свидетель `m_ops_check_2026-10-10.py` |
Оба в статусе `pending`; статусов канона не меняют. Заголовок: `last issued DN-0034`.

## 4. Новый файл-свидетель
`work/v14_rebuild/m_ops_check_2026-10-10.py` (9 PASS): ЛУ3=D(ЛУ2), ЛУ4=X∧D(X), ЛУ5=D(ЛУ4), ЛУ6=X∧D(X),
ЛУ7=ЛУ6∨D(ЛУ6), ЛУ7≠D(ЛУ6) буквально, ЛУ7≡D(ЛУ6) в булевой логике и логике Клини. Узел `verification`
(`candidate`, вне общего маршрута, в `check_project_consistency.py` не зарегистрирован) → `verifies`
`M_04…M_07`, `U7_LOGIC_GROUPING`.

## 5. REFUTED (`work/REFUTED.md`, +2 строки)
Запись «2026-10-10 · Устаревшие предпосылки в слое вопросов»: `AF-012.2`, `AF-013.2…4` выведены из устаревшего
поля `unresolved`; `Q-M_12.2` исходил из r=2. Узел `refutation`; связи к вопросам `Q-AF-012.2`, `Q-AF-013.2…4`,
`Q-M_12.2` и к закрытому `oq-graph-dep-sync`.

## 6. Слой вопросов (`work/v14_rebuild/claim_questions/`) — новый
Подробности: `README.md`, `QUESTION_GROUPS.md`, `OBJECTS.md`. Единый файл `QUESTION_CARDS.jsonl` (536 записей:
`layer=assertion` 402, `layer=object` 134; все `question_origin=assistant_derived`, `author_review=none`).

### 6.1. Новые типы узлов
| Тип | Число | Откуда | Ключевые свойства |
|---|---:|---|---|
| `question` | 536 | `QUESTION_CARDS.jsonl` | `question_id`, `layer`, `question`, `question_kind`/`aspect`, `corpus_coverage`, `answer_status`, `primary_group`, `question_origin` |
| `question_group` | 14 | `inputs/groups.tsv` | `G01…G14`, имя, критерий включения |
| `question_object` | 29 | `inputs/objects.tsv` | `O-X2`, `O-MU7`, …, `T-TOT` …; `kind` формула/оператор/термин, определение или «в каноне нет» |

### 6.2. Новые рёбра
| Отношение | Число | Источник | Заметки |
|---|---:|---|---|
| `asks_about` (question → утверждение/карточка/паттерн/находка/группа) | 402 | `source_id` у `layer=assertion` | утверждения уже в графе (`card`, `claim`, `claim_group`, `finding`, `pattern`) |
| `asks_about_object` (question → question_object) | 134 | `object_id` | |
| `derived_from` (question → question) | по `parent_question_id` | 117 производных вопросов к утверждениям + `QO-ROLE.1` и 12 `instance` | |
| `in_group` (question → question_group), основная | 536 | `primary_group` | |
| `in_group_secondary` | у 48 вопросов | `secondary_groups` | |
| `refers_to` (question → card / verification / oq / level) | по `refs` | явные ссылки | уровни — к узлам `level` |
| `known_in_corpus` (question → verification/card/oq) | по `known_in_corpus` | вручную | `corpus_coverage`: covered 346, partial 32, open 150, answered_elsewhere 5, external 3 (по всему слою); ссылки проверены `check.py` |
| `crossref_open_question` (question → `open_question`) | 117 | `QUESTION_CROSSREF.tsv` | тип связи: same 55, related 44, instance 9, answered_by_closed 8, premise_outdated 1 |
| `answered_by` (question → open_question `[x]`) | 5–8 | `answer_pointer` | `AF-012.2`, `AF-013.2…4`, `AF-011.2` (частично) |
| `object_defined_in` (question_object → card) | по `objects.tsv` | | |

### 6.3. Особые пометки (свойства узлов)
- `external` (аспект): `QO-X2.17`, `QO-ABS.6`, `QO-SQRT.6` — [внешнее], не пробел ФТС.
- `premise_note`: `Q-M_12.2` (решение автора: r свободный).
- Почти-дубли: 81 пара в `DUPLICATE_CANDIDATES.tsv` — рёбра `similar_to` добавлять только после чтения.

## 7. Группы (`QUESTION_GROUPS.md/.tsv`)
640 строк: 536 карточек + 103 пункта `OPEN_QUESTIONS.md` + 1 пункт журнала. Для `open_question` добавить
свойства `question_group` (назначена вручную, `inputs/oq_groups.tsv`) и рёбра `in_group`.

## 8. Проверки после внесения
1. `py -3.11 -X utf8 tools/graphify_audit_navigation.py --verify` (ожидание: 31 паттерн, 82 OQ, 25 групп, 20 находок;
   после добавления слоя вопросов — отдельно проверить, что навигационные числа не изменились).
2. `claim_graph.py validate --idempotent` → `idempotent: true`, 924/2250, 601 утверждение.
3. `verify.py --strict` → 13/13; `check_project_consistency.py` → ожидаемо 12/13 из-за устаревшей выгрузки.
4. `work/v14_rebuild/claim_questions/tools/check.py` → `FAIL 0`.
5. Запросы MCP `fts_graphify`: узел `M_12` показывает свободный r; `DN-0034` и `QO-X2.*` находятся.
6. Идемпотентная повторная инъекция не добавляет узлов и связей.

## 9. Что не сделано и ждёт решения
- `research_export` устарел (проверка падает, пересборка отложена из-за чужих правок).
- Указатель на слой вопросов в `OPEN_QUESTIONS.md` откатан (хэш файла фиксируется производными).
- Фрагменты для `STATE.md`/`DECISIONS.md` лежат в `RECORDS_PENDING.md`.
- Узлы `DN-0033`/`DN-0034` вносить как `pending`; не связывать с повышением статусов.
- Семантически вопросы — гипотезы ассистента; в граф вносить с `confidence`/происхождением
  `assistant_derived` (INFERRED, не EXTRACTED).
