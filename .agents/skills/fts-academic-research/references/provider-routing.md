# Маршрутизация провайдеров

## Consensus

Использовать для первичного discovery свидетельств: рецензируемых статей,
обзоров, мета-анализов, RCT и противоречащих результатов. Сохранять существующий
коннектор Consensus и не регистрировать дубликат MCP. Перед цитированием или
экспортом записи выполнять `search`, затем `fetch`. Сохранять Consensus result ID,
если он доступен.

## Semantic Scholar

Использовать Academic Graph для идентичности и библиографии: разрешения DOI/S2 ID,
нормализации метаданных, references, citations, recommendations и расширения
seed-set. `S2_API_KEY` необязателен; его нельзя коммитить или печатать. Независимо
от наличия ключа начинать с одного запроса в секунду. При `429` соблюдать
`Retry-After`; после исчерпания повторов сохранять кандидата как `uncertain` и
продолжать в режиме graceful degradation.

Одиночная проверка:

```powershell
python -X utf8 .agents/skills/fts-academic-research/scripts/s2_verify.py --doi "10.xxxx/example"
python -X utf8 .agents/skills/fts-academic-research/scripts/s2_verify.py --title "Exact paper title"
```

## ResearchRabbit

Использовать управляемый исследователем round-trip. Экспортировать проверенные
seeds в `seed_set.bib`; исследователь изучает citations, references и similar
papers; возвращённый BibTeX, RIS или CSV импортировать как новый файл. Исходный
экспорт сохранять без изменений. До включения повторно проверять записи через
Semantic Scholar или DOI-реестр. ResearchRabbit не подтверждает существование
публикации и не переносит screening-решения ФТС.

## Wolfram

Сохранять `$fts-wolfram-audit` отдельным явно вызываемым навыком. Использовать
только для точных символических или статистических предикатов после того, как
литературная фаза выделила формулу для проверки. Результат может влиять на
`St_math` только через действующий проектный гейт и не может повышать `St_FTS`.
