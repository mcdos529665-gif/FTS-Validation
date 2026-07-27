# Записи и контрольные точки

## Каноническая запись источника

В записях кандидатов и свидетельств использовать поля:

`record_id,doi,s2_paper_id,consensus_id,title,year,provider,retrieved_at,query_id,claim_or_oq,screening_decision,screening_reason,fts_relation`

Правила:

- `screening_decision`: `include|exclude|uncertain`.
- `fts_relation`: `direct|limiting|alternative|analogy`.
- DOI: нижний регистр, без resolver URL и ведущего `doi:`.
- Дата получения: ISO 8601 UTC.
- ID провайдера сохранять дословно.
- Не помещать частные заметки или текст рукописи в provider fields.

## Контрольные точки systematic-review

1. `protocol_frozen`: зафиксированы вопрос, базы, запросы, даты, критерии и
   правило остановки.
2. `seed_verified`: у каждой seed-записи есть DOI/S2 ID либо явная причина
   неразрешённости.
3. `rr_roundtrip_received`: возвращённый экспорт сохранён byte-for-byte и
   проверено сохранение DOI.
4. `screening_locked`: файлы Codex и исследователя независимо завершены.
5. `adjudication_complete`: каждое расхождение имеет одобренное автором решение.
6. `synthesis_bounded`: evidence matrix и novelty claim включают ограничения и
   непокрытые области графа.

Ни одна контрольная точка не меняет статус ФТС. Любое предлагаемое изменение
проходит через действующий авторский процесс SP/K1–K5.

## Локальный полнотекстовый intake

Для пользовательских OCR/Markdown-файлов использовать `PAPER_INTAKE.tsv`.
Обязательны: существующий `record_id`, DOI при наличии, исходный путь, SHA256,
проектный путь, показатели OCR, русское досье и `intake_status=imported`.
Исходный файл сохраняется без правок. Досье является производным артефактом и не
закрывает второй screening-проход.
