# Протокол внешней проверки FTS-skeleton

- protocol_id: FTS-NN-SKEL-2026-09-15
- status: active_first_wave
- question: см. RESEARCH_QUESTION.md
- source_of_truth: этот каталог + канон через точечные ссылки; не source/
- status_effect: внешний результат сам по себе не меняет St_FTS

## Дизайн

Смешанный контур из трёх частей:

1. **Формальная сверка.** Для каждого моста фиксируются объекты, операции,
   область, кванторы, условия и точная граница переноса.
2. **Архитектурная проверка.** Компонентные мосты переводятся в явную
   исследовательскую спецификацию, не в новую каноническую карточку.
3. **Различающий эксперимент.** FTS-skeleton сравнивается с M' и известными
   архитектурами при одинаковом контракте задач, параметрах/стоимости и
   заранее объявленных абляциях.

## Поисковая стратегия первой волны

### Источники

- первичные журнальные статьи и официальные страницы издателей;
- PMLR, NeurIPS, ACL Anthology, Nature/Springer, PubMed/PMC;
- arXiv только как точная версия первичного текста, с отдельной проверкой
  опубликованной версии, если она есть;
- локальный архив work/v14_rebuild/e5_literature_review/ — как уже
  проверенный внутренний материал, не как внешний источник.

### Поисковые семейства

- hierarchical predictive coding neural network residual feedback
- compositional modular neural network architecture learned modules
- missingness indicator neural network missing data architecture
- neural network external memory structured reasoning graph tasks
- abstract interpretation strong preservation minimal refinement language
- group equivariant neural network symmetry sample complexity
- global workspace recurrent neural architecture specialized processors

### Критерии включения

- источник существует и имеет проверяемую библиографическую запись;
- источник содержит формальный предикат, архитектуру или измеренный эффект, а не
  только совпадение слов;
- можно выписать объекты/операции/область и место ограничения;
- отношение к ФТС можно классифицировать как direct, limiting, alternative,
  refuting или analogy.

### Критерии исключения

- непроверяемая ссылка или только агрегатор без первичного текста;
- терминологическое совпадение без typed mapping;
- результат, который использует канонические предпосылки ФТС как внешнее
  подтверждение;
- benchmark без capacity-matched baseline или без воспроизводимой постановки,
  если он используется как доказательство преимущества.

## Схема карточки источника

Каждая строка EVIDENCE_MATRIX.tsv должна содержать:

FTS claim → external claim → objects/operations/domain → mapping →
strongest limitation/defeat → source quality → status effect.

analogy никогда не считается поддержкой. direct означает только локальный
контакт в указанной области, не перенос всей ФТС.

## Контроль смещений

- искать одновременно подтверждающие, ограничивающие и опровергающие источники;
- не считать число ссылок мерой силы основания;
- для каждого direct-моста искать независимый M' или альтернативную реализацию;
- разносить St_math, St_FTS и внешнюю evidence quality;
- записывать отрицательные и inconclusive результаты, а не удалять их.

## Порог перехода к эксперименту

Экспериментальный skeleton допускается только после:

- минимум четырёх локальных мостов с direct или alternative relation;
- минимум двух limiting/refuting записей;
- зафиксированного контракта M' и тестов поражения;
- замороженной архитектурной спецификации и стоимости.

Положительный benchmark без этих условий будет считаться только exploratory.

## Порог интерпретации

- T1: локальная внешняя опора;
- T2: candidate functional skeleton;
- T3: supported architecture only after capacity-matched evidence;
- T4: biological model only after neural data and a separate neuroscience
  protocol.

