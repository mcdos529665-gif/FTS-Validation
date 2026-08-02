# Журнал внешнего литературного поиска

Дата исходного поиска: 2026-07-13. Дополнительная claim-led проверка У1–У5:
2026-08-02. Режим: claim-driven web search; OpenAlex MCP в текущей среде
недоступен. Язык запросов — английский и русский. Поиск не претендует на исчерпывающую
систематическую библиографию.

## Критерии

Включались первичные статьи, официальные страницы издателей/конференций, авторские
тексты книг и методические обзоры с устойчивым идентификатором. Вторичные блоги,
Wikipedia, Reddit и SEO-страницы не использовались как основания. Для каждого источника
фиксировались: собственный тезис, сопоставление с ФТС, тип связи и ограничение переноса.

Исключались работы, где совпадало только слово; применение complex/group/category
методов без различающего утверждения; результаты, не отделяющие фазу от частоты,
ёмкости или механизма пропусков.

## Запросы

1. `Blackwell 1953 Equivalent comparisons of experiments DOI 10.1214 official`
2. `Nadeau Bengio 2003 Inference for the generalization error DOI corrected resampled t test`
3. `Rubin 1976 Inference and missing data DOI Biometrika missing at random`
4. `Cohen Welling 2016 Group Equivariant Convolutional Networks arXiv`
5. `site:projecteuclid.org Blackwell Equivalent Comparisons of Experiments 1953 10.1214/aoms/1177729032`
6. `Deep Complex Networks Trabelsi 2018 OpenReview complex valued neural networks`
7. `RadioML 2016.10a O'Shea Corgan Clancy convolutional radio modulation recognition paper arxiv`
8. `Homotopy Type Theory book official Awodey Warren homotopy theoretic models identity types DOI`
9. `"Equivalent Comparisons of Experiments" Blackwell 1953`
10. `site:projecteuclid.org "Equivalent Comparisons of Experiments"`
11. `Blackwell sufficiency comparison statistical experiments garbling theorem primary source`
12. `Sherman Stein Blackwell theorem comparison experiments survey`
13. `missing indicator method bias missing covariates primary study DOI missingness indicators prediction`
14. `Demšar 2006 Statistical Comparisons of Classifiers over Multiple Data Sets JMLR`
15. `RadioML 2016.10a carrier frequency offset dataset generation channel model paper`
16. `Harmonic Networks Deep Translation and Rotation Equivariance Worrall CVPR 2017 phase`
17. `Emily Riehl Category Theory in Context retract split idempotent PDF`
18. `Gambino Garner identity type weak factorization system 2008 DOI`
19. `homotopy type theory book retract definition official pdf`
20. `Karoubi envelope split idempotents category theory original paper`
21. `"лестница различимости" теория`
22. `"distinguishability ladder" information theory`
23. `"typed absence" missingness machine learning`
24. `"ФТС" "лестница различимости"`
25. `Worrall Harmonic Networks 2017 DOI 10.1109 CVPR`
26. `Groenwold White Donders missing indicator method DOI 10.1503/cmaj.110977`
27. `Trabelsi Deep Complex Networks OpenReview H1T2hmZAb`
28. `Representable Markov Categories Comparison Statistical Experiments DOI`

### Дополнительная проверка моста У1–У5 (2026-08-02)

Это не расширение exact-phrase novelty-поиска, а проверка шести конкретных
оснований из предложенного моста: оригинал Shannon; Lean `Eq.refl`; Mathlib
`Setoid.ker`/`quotientKerEquivOfRightInverse`; Mathlib `ProbabilityMeasure`/Dirac;
Lean `Or` против `Sum`/decidable branch; decision rule как переход
observation→action. Все шесть источников открыты и сверены по
первичному/официальному тексту; записи LIT-16…LIT-21 добавлены в
`LITERATURE_MATRIX.tsv`.

## Покрытие и решение

| Направление | Отобрано | Итог для ФТС |
|---|---:|---|
| Blackwell / sufficiency | 2 | Прямой мост возможен только с experiment/garbling/decision structure |
| Missingness / MNAR | 2 | 0_A/T3 не заменяет модель механизма пропусков |
| Repeated CV / model comparison | 2 | Исправленная единица вывода — dataset; folds зависимы |
| Z/2, U(1), group actions | 3 | Известный внешний формализм; нужны action/equivariance/capacity laws |
| Complex/phase-aware models | 3 | Complex representation не нова и не доказана необходимой для ФТС |
| RadioML/CFO | 1 первичный + локальные результаты | Benchmark не идентифицирует чистый фазовый claim без абляций |
| Retractions / HoTT | 4 | Нужны morphisms, identity/factorization laws и typed model |
| Нижняя цепочка У1–У5 | 6 дополнительных | У2–У5 имеют прямые component-level конструкции; У1 — только limiting identity-якорь |
| Граница новизны | 4 exact-phrase запроса | Точного аналога всей конструкции не найдено в пределах поиска; есть смежные работы |

## Граница новизны

Допустимая формулировка: **«В пределах 28 зафиксированных запросов на 2026-07-13 не
найдена работа, совпадающая с полной конструкцией ФТС v13/v14 (лестница, регистры,
каналы и статусная механика)».** Это отрицательный результат поиска, не доказательство
мировой новизны. Отдельные компоненты — сравнение экспериментов, missing indicators,
group equivariance, complex networks, categorical retracts и HoTT — имеют развитую
предшествующую литературу. Дополнение 2026-08-02 подтверждает component-level
formal contact нижней цепочки У2–У5 и limiting-якорь У1, но не меняет границу
новизны всей конструкции. Фраза `typed absence` также встречается вне ФТС.

Литературная матрица: `LITERATURE_MATRIX.tsv`. Ни один источник автоматически не
изменяет `St_FTS` или канонический статус.
