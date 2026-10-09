# graphify_canon_edges — плотный канон-слой для graphify

Препроцессор, который превращает **канон v13** (`source/fts_cards.jsonl` +
`source/fts_triples.tsv`) в **EXTRACTED-рёбра** для графа graphify. Канон-backed,
без единой LLM-догадки. Инструмент — `tools/graphify_canon_edges.py`.

## Зачем

LLM-экстракция graphify из `fts_cards.json` недобирает связи: плоский JSON-массив
карточек почти не нарративен, поэтому карточки повисают изолированными. Но канон
уже содержит готовый edge-list (238 триплетов + поле `depends_on`). Тул инжектит
его. Эффект (эта сессия, при **0 токенов**):

| | LLM-граф | + канон-слой |
|---|---|---|
| рёбра | 699 | **838** |
| сообщества | 116 | **57** |
| EXTRACTED | 85% | **90%** |
| изоляты (≤1) | 234 | **180** |

Цепь `has_next` собирает лестницу в полосы (У1–У4, У6–У7, У10–У12, У13–У17),
`has_minimal_expression`/`has_private_expression` подшивают M_xx/CH_xx к уровням.

## Использование (из корня репо; на Windows-консоли добавляй `-X utf8`)

```
python -X utf8 tools/graphify_canon_edges.py            # → graphify-out/canon_fragment.json + сводка
python -X utf8 tools/graphify_canon_edges.py --stats    # только сводка (чистый stdlib, без graphify)
python -X utf8 tools/graphify_canon_edges.py --out P    # свой путь вывода фрагмента
python -X utf8 tools/graphify_canon_edges.py --inject   # влить в graphify-out/graph.json + рекластеризовать
python -X utf8 tools/graphify_canon_edges.py --inject --project-root ROOT --out-dir OUT  # изолированная сборка
```

`emit` и `--stats` — **только stdlib**. `graphify` импортируется лениво и нужен
исключительно для `--inject`.

## Как воспроизвести плотный граф с нуля

```
/graphify .                                       # 1. базовый граф из корпуса → graphify-out/graph.json
python -X utf8 tools/graphify_canon_edges.py --inject   # 2. влить канон-слой + рекластеризация (auto-лейблы)
graphify export html                              # 3. обновить интерактивный graph.html
```

`.graphifyignore` в корне репо уже исключает избыточные сериализации канона
(workbook/full-dump/context/yaml), чтобы не плодить узлы-двойники.

> `--inject` ставит **auto-лейблы** сообществ (по самому связному узлу) — ради
> воспроизводимости без ручной разметки. Красивые ручные имена — разовая полировка.

## Как устроено

- **Выравнивание ID.** Узлы именуются `source_fts_cards_<id>` — та же схема, что
  graphify даёт карточкам `fts_cards.json`. Проверено: **161/161** совпадает →
  канон-рёбра ложатся на существующие узлы, без двойников. Сменится схема graphify —
  правь `NODE_PREFIX` в туле.
- **Рёбра.** Триплеты `subject→object` (card→card) ∪ `depends_on` карточек, все
  `EXTRACTED` (score 1.0). Предикаты сохранены как в каноне (`depends_on`,
  `has_next`, `has_minimal_expression`, `projects_to`, `supports`, `has_operator`,
  оверлеи, …).
- **Резолвер алиасов.** `O2` / `O(8)` → `O_02` / `O_08` (канон местами без
  zero-padding). Вернул 31 ребро.
- **Пропуски — логируются по причинам, не молча:**
  - `literal_or_uncarded_object` (76): окна-литералы `(3,4,5,6,7)`, `*.md`,
    некарточные `OP_*`;
  - `bad_subject` (4): висячие `SP_EPI/LIMITS/PARITY/PHI` (нет карточек);
  - `dangling_dep` (12): `Lambda_link`, `TA1`, `OP_dDelta`, … — ссылки без карточек.

  Это реальные пробелы/внешние ссылки канона, а не баги тула.

## Инварианты

- Канон (`source/`) **не трогается** — тул только читает `fts_cards.jsonl` +
  `fts_triples.tsv`.
- `emit`/`--stats` держи на чистом stdlib (как `query.py`/`verify.py`).
- Пропуски печатай явно (no-smuggling: чего нет в каноне — не выдумывать; при
  доработках сохраняй лог причин).

## Аудиторская навигация (не канон)

После полного аудита v13/v14 отдельный инструмент
`tools/graphify_audit_navigation.py` добавляет в уже собранный Graphify-граф
**только навигационный** слой: паттерны, якоря OQ, программы, события, группы
утверждений и находки. Входы — структурированные TSV из `work/v14_rebuild/audit/`
и якоря из `work/OPEN_QUESTIONS.md`; `source/` не читается и не меняется.

```
python -X utf8 tools/graphify_audit_navigation.py --stats
python -X utf8 tools/graphify_audit_navigation.py
E:\Codex\mcp\graphify\tools\graphifyy\Scripts\python.exe -X utf8 tools/graphify_audit_navigation.py --inject
E:\Codex\mcp\graphify\tools\graphifyy\Scripts\python.exe -X utf8 tools/graphify_audit_navigation.py --verify
```

Маркировка намеренно консервативна: `direct` из атласа — `EXTRACTED`; `indirect`
и непрямая часть `mixed` — `INFERRED`; `support` — служебная навигация без
теоретической статусной силы. В `graphify-out/` остаются фрагмент, краткий отчёт
и manifest входных SHA256. При обновлении таблиц сначала запускай `--stats`, затем
`--inject` и `--verify`; это не заменяет `run_audit.py traceability`.
