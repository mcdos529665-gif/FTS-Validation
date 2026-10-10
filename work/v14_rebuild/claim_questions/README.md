# Вопросы проекта: утверждения, объекты, группы, ссылки

Рабочий слой. Вопросы не меняют статусы канона и не являются ответами. Все вопросы сформулированы
ассистентом (`question_origin: assistant_derived`), авторской проверки не было.

## Что здесь

| Файл | Что это |
|---|---|
| `QUESTION_CARDS.jsonl` | **Единый файл карточек**, 536 записей: `layer: assertion` (402 вопроса к 285 утверждениям) и `layer: object` (134 вопроса к 29 объектам). |
| `OBJECT_QUESTION_CARDS.jsonl` | Производный вид: только `layer: object`. |
| `OBJECTS.md` | Реестр объектов (формулы МУ2–МУ15, операторы Δ, κ, Close, Refuse, Sever, π/ι, Lift, 0_A по уровням, термины) и их вопросы. |
| `QUESTION_GROUPS.md`, `QUESTION_GROUPS.tsv` | Группы всех вопросов проекта: 641 вопрос (карточки обоих слоёв, 103 пункта `OPEN_QUESTIONS.md`, 2 пункта журнала). Построчно — в TSV, с извлечёнными ссылками. |
| `QUESTION_CROSSREF.tsv` | Ручные связи вопросов с пунктами `OPEN_QUESTIONS.md`: 117 строк (`same`, `instance`, `related`, `answered_by_closed`, `premise_outdated`). |
| `DUPLICATE_CANDIDATES.tsv` | Почти-дубли для ручного решения (81 пара). Автоматически не исправляются. |
| `inputs/` | Входы, которые правит человек или ассистент (см. ниже). |
| `tools/` | Конвейер: `sources.py`, `build.py`, `check.py`. |

## Слои и решётки

- **assertion** (утверждения): 285 источников — карточки канона (172), утверждения графа (37 `claim`,
  25 `claim_group`, 20 `finding`, 31 `pattern`). Каждое утверждение имеет ровно один базовый вопрос
  `Q-<source_id>`; производные вопросы — `Q-<id>.N` с `parent_question_id`. Тип вопроса (`question_kind`):
  `answered | gap | bridge | obligation | test | limit | term | compare`.
- **object** (объекты): `QO-…`. Аспект из решётки: `definition | identity | symmetry | image | preimage |
  neighbor | mirror | uniqueness | role | external`. Прежний аспект сохранён в `aspect_detail`.
- **Покрытие** (`corpus_coverage`): `covered` — в корпусе есть источник, отвечающий на вопрос (источники в
  `known_in_corpus`); `partial` — ответ есть частично; `open` — ответа нет; `answered_elsewhere` — ответ в
  закрытом пункте `OPEN_QUESTIONS.md` (`answer_pointer`); `external` — понятие вне канона ФТС
  (производная, гладкость, сходимость, дисперсия), аспект `external`, тег `[внешнее]`, не считается пробелом.
- `covered` у утверждения с типом `answered` означает, что ответ — само утверждение; это не проверка верности.

## Поля карточки

`question_id, layer, parent_question_id, parent_relation, source_kind, source_id | object_id, source_status,
source_text (полный текст), question_kind | aspect, aspect_detail, question, primary_group, secondary_groups,
refs{levels,cards,checks,dict,criteria,oq,files}, classes, external_domains, known_in_corpus, corpus_coverage,
answer_status, answer_pointer, premise_note, checked, question_origin, author_review, added, revised,
previous_question`. Для объектов добавлены `object, object_role, object_kind`.

## Группы

Основная группа: утверждения — по семейству источника (правила в `tools/build.py`, `source_group`);
объекты — по полю `primary_group` в `inputs/objects.tsv`; пункты `OPEN_QUESTIONS.md` — вручную в
`inputs/oq_groups.tsv`. Вторичные группы (`secondary_groups`) назначаются автоматически по тематике текста:
внешние области, данные, инфраструктура, решение автора. Таксономия и критерии — `inputs/groups.tsv`.

Ссылки извлекаются регулярными выражениями с границами слов `(?<!\w)…(?!\w)`: уровни (`У/МУ/ЛУ/СУ n`,
диапазоны), карточки канона, проверки `C-NN` и `G60-NN`, словарь `Д1…Д11`, критерии `К1…К5`, `O_nn`,
`F1…F6`, якоря `oq-…`, пути файлов.

## Входы (`inputs/`, правятся вручную)

- `assertion_questions.txt` — вопросы к утверждениям (TSV, заголовок в первой строке). Тексты перенесены
  дословно из прежних карточек; правки отмечены `previous_question` и `revised`.
- `object_questions.txt` — вопросы к объектам (TSV).
- `objects.tsv` — реестр объектов: `object_id, label, role, kind, primary_group, aliases_regex,
  defining_cards, definition_note`. У каждого объекта — карточка-определение из канона или пометка
  «определения в каноне нет».
- `groups.tsv` — 14 групп: критерий включения одной строкой, о чём спрашивает, на что ссылается.
- `oq_groups.tsv` — группы пунктов `OPEN_QUESTIONS.md`.
- `crossref.tsv` — ручные связи с пунктами `OPEN_QUESTIONS.md`.

Источники (карточки, утверждения графа, проверки, пункты OQ, DN-журнал) читаются только на чтение
модулем `tools/sources.py` из `source/`, `work/v14_rebuild/claim_graph/` и `work/`. Проверки C-NN и
G60-NN берутся разбором AST вызовов `check(...)` во всех `verification*.py` под `work/v14_rebuild`.
`verification_windows_table.py` не содержит вызовов `check` (это таблица окон), в реестр проверок не входит.

## Как пересобрать и проверить

Из корня репозитория, Python 3.11 с UTF-8:

```
py -3.11 -X utf8 work/v14_rebuild/claim_questions/tools/build.py
py -3.11 -X utf8 work/v14_rebuild/claim_questions/tools/check.py
```

`build.py` перезаписывает только производные файлы и идемпотентен: повторный запуск не меняет SHA256
выходных файлов. Точный дубль текста вопроса — ошибка сборки; почти-дубли выводятся в
`DUPLICATE_CANDIDATES.tsv` (совпадение слов ≥ 0,6 внутри источника или ≥ 0,8 во всём наборе, служебные
слова не учитываются). `check.py` проверяет: 285 утверждений ↔ по одному базовому вопросу; уникальность
`question_id` и текстов; родителей; существование всех ID в `known_in_corpus`, `refs` и проверках;
`covered/partial` имеют источник; `answered_elsewhere` ссылается на закрытый `[x]` пункт; `external` ⇔
аспект `external` и тег `[внешнее]`; решётку аспектов; группы; состав `QUESTION_GROUPS.tsv`.

Предупреждения сборки (не ошибки): вопросы с темой «производная/гладкость/сходимость/дисперсия/мера»
без аспекта `external`. Они перечислены в выводе `build.py` и ждут решения.

## Правила создания вопросов

1. Один вопрос — один смысл. Новый вопрос — только из явного поля или фразы источника (`verdict`,
   `resolution`, `unresolved`, «не доказано», «требуется», `TBD`).
2. Перед вопросами `obligation` поле `unresolved` сверяется с закрытыми пунктами `OPEN_QUESTIONS.md`;
   если ответ есть — `answered_elsewhere` с `answer_pointer`.
3. Понятия вне канона — аспект `external`, тег `[внешнее]`.
4. Если форма задана построением (У6 = У4·π, C-34), вопрос ставится о вынужденности правила построения,
   а не о единственности формы.
5. Роль формы на уровне — один родительский вопрос `QO-ROLE.1`; частные вопросы — `instance`.
6. Авторские утверждения — только цитатой из журнала; формулировки ассистента — `assistant_derived`.

## Что не сделано

- Ответы не записаны; статусы канона не менялись (правило К1–К5 и SP_* не затронуто).
- Связи с `OPEN_QUESTIONS.md` собраны вручную; автоматический поиск кандидатов не использовался как
  источник таблицы. Полнота не гарантирована.
- Почти-дубли (81 пара) не решены; часть из них — намеренные варианты (например, `AF-013.2…4`, шаблонные
  `TBD` карточек `M_13…M_17`, `CH_13…CH_17`).
- Вопросы не добавлены в `claim_graph` и не записаны как открытые пункты `OPEN_QUESTIONS.md`: это требует
  пересборки графа и решения автора.
- Не проверены по существу автором.
- Предупреждения о теме «анализ» (см. выше) не разрешены.
