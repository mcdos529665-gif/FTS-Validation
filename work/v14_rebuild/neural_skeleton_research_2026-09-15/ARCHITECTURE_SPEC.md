# FTS-Skeleton v0.1 — исследовательская архитектурная спецификация

Это не новая карточка и не предложение изменить канон. Это минимальная
операционализация для проверки вопроса из RESEARCH_QUESTION.md.

## Контракт

Система получает поток наблюдений x_t и вопрос/задачу q_t. На каждом шаге
она должна уметь:

1. хранить представление текущего состояния и его provenance;
2. отличать наблюдаемое значение от отсутствующего/неразрешённого состояния;
3. формировать предсказание и остаток относительно следующего чтения;
4. уточнять представление, когда остаток делает текущий вопрос невыразимым;
5. проецировать расширенное чтение обратно на нижний интерфейс;
6. удерживать состояние в рекуррентной памяти и выдавать ответ через readout;
7. отклонять или маркировать обновление, если provenance/revision gate не
   выполняется.

## Внешний computational interface

    encode(x_t, context) -> (h_0, provenance_0)
    typed_absence(h_n, mask_n, context_n) -> a_n
    predict(h_n) -> y_hat_n
    residual(y_n, y_hat_n) -> r_n
    refine(h_n, r_n, q_t) -> (h_(n+1), witness_n)
    project(h_(n+1), target=n) -> h_n_star
    memory_read_write(h_n_star, W_t) -> (state_t, W_(t+1))
    gate(state_t, provenance_t, revision_t) -> {accept, refuse, sever, defer}
    readout(state_t, q_t) -> answer_t

Имена typed_absence, residual, refine, project, memory и gate — внешние
программные роли. Они не объявляются тождественными 0_A, Res_n, Lift, π,
W/0_W или κ; каждое такое отождествление должно пройти отдельный
mapping-аудит.

## FTS mapping passport

| Рабочая роль | Кандидатная связь с ФТС | Что обязано быть доказано |
|---|---|---|
| nested context | O_01 | нижний носитель действительно нужен для данного вопроса, а не просто выбран дизайнером |
| residual/refinement | Res_n, O_03, O_14 | остаток сохраняется и создаёт новый выразимый вопрос, а не только новый слой |
| projection | O_08 | commuting/section law для конкретного интерфейса |
| typed absence | 0_A | механизм не сливает structured absence с ¬A, NaN или false |
| expectation/memory loop | W/0_W, U7 candidate | закрытие окна отличимо от confidence или внешнего label |
| revision/provenance gate | κ candidate | gate меняет допустимость обновления и имеет defeat test |
| symmetry/phase overlay | v13 overlay | explicit group/action law; иначе только analogy/alternative |

## Независимая M'

Основная M'‑семья — state abstraction/strong-preservation model с фиксированным
языком запросов. Она получает тот же вход, память, бюджет и набор наблюдаемых
вопросов, но не получает порядок У1–У11, 0_A или FTS-имена как предпосылки.
Вторая M'‑семья — обычная recurrent/memory-augmented baseline с matched
parameter count и теми же масками/данными.

Если M' проходит тот же контракт после распаковки без FTS-specific operator,
это ограничивает claim о необходимости ФТС. Если skeleton выигрывает только при
добавлении скрытого контекста или памяти, стоимость должна быть оплачена явно.

## Минимальный экспериментальный пакет

| Тест | Способность | Критическая абляция |
|---|---|---|
| HIER-PRED | предсказание нижнего уровня из верхнего и восстановление residual | убрать top-down/residual loop |
| COMP-QUERY | композиционное выполнение двух-трёх операторов | слить M/CH или заменить layout fixed M' |
| ABS-MECH | различить observed zero, structured absence и unobserved state | заменить typed mask одним boolean/NaN |
| MEM-GRAPH | удержание и поиск отношения после нескольких шагов | убрать external/recurrent memory |
| REFLECT | применение интернализированного label к собственной модели без нового внешнего исхода | убрать revision/provenance gate |

Каждый тест должен иметь synthetic generator, held-out compositional split,
capacity-matched baselines, минимум 5 независимых seeds, заранее объявленные
метрики и отрицательный контроль с нерелевантной маской.

## Метрики

- task loss/accuracy и calibration;
- sample efficiency и held-out compositional generalization;
- parameter count, FLOPs, wall-clock и memory footprint;
- error taxonomy: collapse, false promotion, absence conflation, provenance loss;
- устойчивость к distribution shift и controlled missingness;
- ablation effect с доверительным интервалом, а не только лучший seed.

