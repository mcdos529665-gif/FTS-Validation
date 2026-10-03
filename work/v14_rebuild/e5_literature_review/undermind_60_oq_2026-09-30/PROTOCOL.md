# Протокол исследования 60 OQ через Undermind

Дата: 2026-09-30. Режим: `fact-check`. Задание: попытаться ответить на 60 вопросов из AUTHOR_ANSWERS_60.md с научными основаниями через Undermind.

## Входы и результат

- Набор вопросов: 60 уникальных `oq_anchor` из PATTERN_OQ_MAP.tsv, те же 60 разделов формы автора. На момент её составления: 49 открытых и 11 частично закрытых.
- Местный контекст: OPEN_QUESTIONS и адресные карточки/пакеты. Исторические проверки использованы с учётом их последующих аудитов.
- Основной результат: [ANSWERS_60.md](ANSWERS_60.md), 60 дословных исходных вопросов с рабочим ответом, оставшимся пробелом и основанием.
- Покрытие: [COVERAGE.tsv](COVERAGE.tsv). Библиография и уровни доступа: [SOURCES.md](SOURCES.md), [SOURCE_RECORDS.tsv](SOURCE_RECORDS.tsv).

## Запросы Undermind

Undermind получил общие научные постановки и библиографические идентификаторы. Сначала выполнены три глубоких поиска, затем адресные семантические запросы и проверка источников. Полный журнал направлений и формулировок — [QUERY_LOG.tsv](QUERY_LOG.tsv).

### D01. Representation cost and next query

[Открыть поиск в Undermind](https://app.undermind.ai/projects/dc244499-d113-4273-a491-111f79a873a8?path=%2FFTS%20open%20questions%202026-09-30%2FRepresentation%20cost%20and%20next%20query). Статус: completed. Выдача: 254 кандидатных работ; первоначально просмотрена страница из 10, у D02 дополнительно следующие 5.

> Understand how one can compare representations and reasoning procedures that trade information preservation, abstraction, and computational cost. I need rigorous frameworks in which loss of distinctions and the selection of a next query can be justified at equal total resource cost, and information-preserving relabeling is distinguished from a genuinely new discriminative capability. Clarify the assumptions and impossibility or identifiability limits of a universal complexity or cost measure.

### D02. Missingness mechanisms and provenance

[Открыть поиск в Undermind](https://app.undermind.ai/projects/dc244499-d113-4273-a491-111f79a873a8?path=%2FFTS%20open%20questions%202026-09-30%2FMissingness%20mechanisms%20and%20provenance). Статус: completed. Выдача: 186 кандидатных работ; первоначально просмотрена страница из 10, у D02 дополнительно следующие 5.

> Determine when recording reasons for missing data and provenance of those reasons yields predictive or decision information beyond a binary missingness indicator, and how this advantage can be tested without information leakage or unequal model capacity. I need empirical and theoretical work that distinguishes mechanism information from general feature capacity, including conditions under which nonignorable missingness cannot be identified from observed data alone.

### D03. Identifiable phase and branch information

[Открыть поиск в Undermind](https://app.undermind.ai/projects/dc244499-d113-4273-a491-111f79a873a8?path=%2FFTS%20open%20questions%202026-09-30%2FIdentifiable%20phase%20and%20branch%20information). Статус: completed. Выдача: 152 кандидатных работ; первоначально просмотрена страница из 10, у D02 дополнительно следующие 5.

> Determine how to design a learning or signal-processing task that makes phase or branch-sign information uniquely useful when the compared methods differ only in access to that information and have equal data, preprocessing, and total computational resources. Distinguish information loss and recoverability from optimization artifacts and nuisance phase or frequency offsets. Establish conditions under which a redundant representation cannot improve the information available to an optimal decision rule although it may help finite-budget learning.

В числах 254/186/152 отражена выдача сервиса; отбор и чтение ограничены избранными источниками. Итоговое резюме deep search само основано на аннотациях/метаданных; сильные условия переносились из проверенных первичных разделов.

## Чтение и проверка идентичности

Получены 22 первичных PDF через Undermind; ещё три ранее прочитанных источника повторно использованы из пакета 2026-09-12. Для пяти источников доступ ограничен аннотацией/метаданными. PDF hashes записаны в SOURCE_RECORDS.tsv. Вспомогательные извлечения из девяти первичных текстов рассмотрены основным агентом при подготовке ответов; это один исследовательский процесс, без заявления независимых репликаций.

Native read_pdfs вернул HTTP 504; использованы PDF download links того же провайдера. Semantic Scholar metadata verification остановлена после 429, S2ID не установлены; сверка библиографии продолжена по Crossref, первичным издателям и arXiv. Исправления годов, авторов и дублей перечислены в SOURCES.md.

Полные тексты, временные ссылки и рабочие материалы чтения находятся в кеше E:/Codex/FTS/undermind_60_oq_2026-09-30. В сохранённом пакете — собственные резюме и постоянные ссылки.

## Вывод и незакрытые зависимости

Получено: 33 рабочих формализации/проекта проверки, 19 уточнений границ, 6 проектных маршрутов, 1 найденное локальное решение, 1 редакционное предложение автору. Эти числа описывают разбор, а не закрытие 60 OQ.

Уточнение локального решения: фиксация анти-моды У12 уже есть в DECISIONS и статье от 2026-06-12. Устарела исходная формулировка oq-u12-antimode-authorfix; смысловая проверка анти-моды остаётся отдельным oq-u12-antimode-gate.

Необходимые следующие основания: ресурс У7/роль левого блока; независимая модель цены; операторы и семантика верхних уровней; реальные площадки для фазы/ветви; причинный след внутреннего применения окрашенного ярлыка. Эмпирический typed-absence запуск сохраняет прежнюю авторскую парковку.

Систематический screening всей выдачи, мировая новизна, общий закон единственности лестницы и статусное повышение ФТС здесь не установлены.
