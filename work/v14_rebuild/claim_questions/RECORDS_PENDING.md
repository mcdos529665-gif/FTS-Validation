# Записи, ожидающие применения: work/STATE.md и work/DECISIONS.md

Дата: 2026-10-10. Файлы `work/STATE.md` и `work/DECISIONS.md` имеют незакоммиченные правки другой
работы (см. `git status` на начало сессии). Их не коммитили и не редактировали, чтобы не включить чужие
правки. Ниже — фрагменты, которые нужно дописать туда после того, как чужие правки будут зафиксированы.
`DECISIONS.md` в основном CRLF: дописывать через `cat >>` или Python по байтам.

## Фрагмент для work/STATE.md (указатели)

- Слой вопросов: `work/v14_rebuild/claim_questions/` — [README.md](v14_rebuild/claim_questions/README.md).
  Единый файл карточек `QUESTION_CARDS.jsonl` (536: 402 к утверждениям, 134 к объектам, поле `layer`),
  группы `QUESTION_GROUPS.md`, объекты `OBJECTS.md`, связи `QUESTION_CROSSREF.tsv`.
- Пересборка и проверка: `py -3.11 -X utf8 work/v14_rebuild/claim_questions/tools/build.py`, затем
  `py -3.11 -X utf8 work/v14_rebuild/claim_questions/tools/check.py`.
- Входы, которые правит человек или ассистент: `work/v14_rebuild/claim_questions/inputs/`.

## Фрагмент для work/DECISIONS.md (решение 2026-10-10)

**Решение: схема слоя вопросов и правила создания.** Вопросы хранятся в одном файле карточек с полем
`layer` (`assertion` для утверждений, `object` для объектов). Входы в `inputs/` правятся вручную, все
производные файлы перегенерируются `tools/build.py` (идемпотентно). Решётки аспектов фиксированы: для
утверждений — `answered|gap|bridge|obligation|test|limit|term|compare`, для объектов — `definition|identity|
symmetry|image|preimage|neighbor|mirror|uniqueness|role|external`. Понятия вне канона (производная,
гладкость, сходимость, дисперсия, мера) — аспект `external` и тег `[внешнее]`, не пробел ФТС.
Вопросы к формам о роли связаны с одним родителем `QO-ROLE.1`. Авторского решения эти записи не
принимают: все вопросы — `assistant_derived`, `author_review: none`. Статусы канона не менялись.

## Что не записано и почему

- Решение автора по `oq-u12-radius-r` (r свободный) уже зафиксировано в `DECISIONS.md` 2026-10-08;
  здесь только ссылка в тексте `Q-M_12.2`.
- Перенос открытых объектных вопросов в `OPEN_QUESTIONS.md`, внесение вопросов в `claim_graph` и
  исправление `M_12` в `source/` — вне этого шага (см. план, раздел «Вне плана»).

## Чужие незакоммиченные правки (не трогались, не коммитились)

- `work/STATE.md`
- `work/DECISIONS.md`
- `tools/graphify_audit_navigation.py`
- `tools/graphify_canon_edges.py`
- `.codex/config.toml` (неотслеживаемый)
