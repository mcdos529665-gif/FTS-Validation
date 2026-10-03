# Источники и пределы ответов

Дата: 2026-09-30. Основной провайдер поиска — Undermind, workspace `dc244499-d113-4273-a491-111f79a873a8`. Включены 30 источников для ограниченных компонент 60 OQ. Их keys — идентификаторы Undermind, год в key может отличаться от года читаемой публикации.

## Доступ к тексту

- **22 полученных PDF:** проверены адресные разделы. Для Gyo23, Jag15, Gro22, Lam11, Hal95, Gen15, Nab20, Mar25c и Tis00 выполнено вспомогательное извлечение фактов из первичного текста; основной агент рассмотрел условия и допустимость переноса. Это машинное чтение, а не независимая научная рецензия.
- **3 прежних первичных чтения:** Ver23, Lor26, Win18b использованы из [проверенного пакета 2026-09-12](../../interpretation_descent_undermind_2026-09-12/EVIDENCE_MATRIX.md) и его [SOURCE_AUDIT](../../interpretation_descent_undermind_2026-09-12/SOURCE_AUDIT.md). Повторный поиск этих работ не считается новой репликацией.
- **5 опор по аннотации/метаданным:** Wil20, Old12, Voo25, Kar94, Rus89b. Они обозначают подходящие результаты/рамки с ограниченным доступом; численные эффекты и сильные теоремы без первичного текста не заимствуются.

Первый вызов `Undermind.read_pdfs` для семи работ завершился HTTP 504. PDF получены через `get_pdf_download_links` того же плагина и прочитаны локально. Временные ссылки доступа и полные тексты находятся в локальном исследовательском кеше на E:, в документе используются постоянные DOI/arXiv ссылки. Ссылка автора Rus89b ведёт на PostScript; этот формат web-reader не прочитал, использована аннотация издателя.

Проверка DOI через штатный Semantic Scholar дала 429 на первых запросах, дальнейшая серия остановлена. S2ID не установлен. Название, авторы, год и издание проверены через первичные страницы/Crossref/arXiv или ранее сохранённый аудит. Подтверждение библиографии является проверкой идентичности источника.

## Исправленные метаданные

| Key | Выдача / риск смешения | Использованная запись |
|---|---|---|
| Hai18 / Hai18b | Два результата с разными счётчиками цитирований | Один DOI, одна статья Scientific Reports 2018; дубль не считается отдельным свидетельством |
| Jia16b | Год 2016 | Препринт 2016; журнал Annals of Applied Statistics 2018 |
| Jag15 | Год 2015 | Препринт 2015; журнал IEEE 2016 |
| Gro22 | Год 2022 | Препринт 2022; журнал SIAM 2023 |
| Hal95 | Key 1995 вместе с DOI/страницами более позднего журнала | Читаемый текст — JAIR 2004. Отдельная IJCAI-версия 1995 не используется вместо него; в журнале есть исправление прежнего слишком сильного результата |
| Ver23 | Год онлайн-публикации и иной порядок авторов | Coelho Mollo, затем Vernazzani; онлайн 2023 / выпуск 2024 |
| Vel24 | Год 2024 | Онлайн 2024 / выпуск 2025; работа концептуальная |
| Rus89b / Bra92 | Конференционный год и, в другой записи, имена редакторов | Russell и Wefald, Artificial Intelligence 1991; Bra92 как самостоятельная опора исключён |
| Tis00 | Только год arXiv 2000 | Сборник Allerton 1999 / читаемый arXiv v1 2000 |

Кандидаты с неуточнённой идентичностью или неподходящим типом публикации не использованы как основные опоры: Wal26, Alp25, Mat09, Lib10, Liu19b. Kum26 и другие новые архитектурные препринты не потребовались для сильных выводов о роли фаз. Это ограниченный отбор, без заявления полного screening всей выдачи.

## Значение отношений

`direct` — совпадает указанная узкая задача/компонента; `limiting` — уточняет предел; `alternative` — предлагает иной аппарат; `analogy` — концептуальная связь. Ни одно из отношений само по себе не устанавливает всю роль уровня ФТС. Первичные факты и собственные предложения ассистента разведены в ответах.

## Проверенные источники

<a id="tis00"></a>

## Tis00 — The information bottleneck method

**Авторы:** Naftali Tishby; Fernando C. Pereira; William Bialek. **Год/версия:** 1999 / arXiv 2000. **Издание:** Allerton 1999; arXiv v1 2000.

**Источник:** [The information bottleneck method](https://arxiv.org/abs/physics/0004057).

**Доступ и место:** PDF: §3.1 Eq.15; §3.2; §3.4, с.8–15.

**Что можно использовать:** Минимизируется I(X;X̃)−βI(X̃;Y) при заданной совместной p(x,y) и выборе релевантной Y. Структура/кардинальность кодирования — отдельные ограничения.

**Предел переноса:** Это целевая статистическая оптимизация. Её β не задаёт веса C(E), цену аппаратного исполнения или всю смысловую область ФТС.

**Связь с ФТС:** alternative; поддерживается только указанная компонента. **Связанные OQ:** [oq-ce-canon](ANSWERS_60.md#oq-ce-canon), [oq-ce-weights-proof](ANSWERS_60.md#oq-ce-weights-proof).

<a id="coa17"></a>

## Coa17 — Coarse-Graining and the Blackwell Order

**Авторы:** Johannes Rauh; Pradeep Banerjee; Eckehard Olbrich; Jürgen Jost; Nils Bertschinger; David Wolpert. **Год/версия:** 2017. **Издание:** Entropy 19(10), 527.

**Источник:** [Coarse-Graining and the Blackwell Order](https://doi.org/10.3390/e19100527).

**Доступ и место:** PDF: §I, Th.1, с.1–4.

**Что можно использовать:** Blackwell сравнивает каналы одного входа по всем решениям через garbling выхода. Информационная ёмкость и полезность для решения задают разные сравнения; pre-garbling входа имеет собственные свойства.

**Предел переноса:** Порядок каналов частичный. Теорема не задаёт универсальную численную лестницу, а её κ — обозначение канала этой статьи.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-ce-canon](ANSWERS_60.md#oq-ce-canon), [oq-d11-branch-bit-test](ANSWERS_60.md#oq-d11-branch-bit-test), [oq-ce-weights-proof](ANSWERS_60.md#oq-ce-weights-proof), [oq-mprime-audit](ANSWERS_60.md#oq-mprime-audit), [oq-ddelta-weights](ANSWERS_60.md#oq-ddelta-weights), [oq-canon-star-fate](ANSWERS_60.md#oq-canon-star-fate), [oq-divorce-cases-genre](ANSWERS_60.md#oq-divorce-cases-genre), [oq-vieta-cubic-s3](ANSWERS_60.md#oq-vieta-cubic-s3), [oq-next-question-principle](ANSWERS_60.md#oq-next-question-principle).

<a id="gen15"></a>

## Gen15 — Bounded Rationality, Abstraction, and Hierarchical Decision-Making: An Information-Theoretic Optimality Principle

**Авторы:** Tim Genewein; Felix Leibfried; Jordi Grau-Moya; Daniel Alexander Braun. **Год/версия:** 2015. **Издание:** Frontiers in Robotics and AI 2, 27.

**Источник:** [Bounded Rationality, Abstraction, and Hierarchical Decision-Making: An Information-Theoretic Optimality Principle](https://doi.org/10.3389/frobt.2015.00027).

**Доступ и место:** PDF: Eq.2–5, с.2–3; Eq.34–36, с.18–20.

**Что можно использовать:** Цена адаптации политики задаётся через KL к исходной политике; оптимизация соединяет полезность и информационное усилие. В иерархии заданы цены отдельных каналов.

**Предел переноса:** KL — введённая мера усилия, без готового отображения в FLOPs, задержку, энергию и всю C(E). Иерархия модели не устанавливает уровни ФТС.

**Связь с ФТС:** alternative; поддерживается только указанная компонента. **Связанные OQ:** [oq-ce-canon](ANSWERS_60.md#oq-ce-canon), [oq-u8-u10-optests](ANSWERS_60.md#oq-u8-u10-optests), [oq-u14-worlds-agg-op](ANSWERS_60.md#oq-u14-worlds-agg-op), [oq-ce-weights-proof](ANSWERS_60.md#oq-ce-weights-proof), [oq-cost-model-scope](ANSWERS_60.md#oq-cost-model-scope), [oq-mprime-audit](ANSWERS_60.md#oq-mprime-audit).

<a id="jia16b"></a>

## Jia16b — Using missing types to improve partial identification with application to a study of HIV prevalence in Malawi

**Авторы:** Zhichao Jiang; Peng Ding. **Год/версия:** 2018 (препринт 2016). **Издание:** The Annals of Applied Statistics 12(3), 1831–1852.

**Источник:** [Using missing types to improve partial identification with application to a study of HIV prevalence in Malawi](https://doi.org/10.1214/17-AOAS1133).

**Доступ и место:** PDF: §2.2 Assumption1; §3; §5 Fig.3, с.4–7,14–16.

**Что можно использовать:** При условии partial MAR для выбранных типов и дополнительных продольных предпосылках причины пропуска сужают границы параметра. В приложении во многих подгруппах ширина уменьшается более чем наполовину.

**Предел переноса:** Это условная частичная идентификация распространённости, с чувствительностью к предпосылкам. Результат не утверждает универсальный выигрыш предсказания от любой типизации и не подтверждает o20 задним числом.

**Связь с ФТС:** direct; поддерживается только указанная компонента. **Связанные OQ:** [oq-kappa-provenance](ANSWERS_60.md#oq-kappa-provenance), [oq-o20-missing-benchmark](ANSWERS_60.md#oq-o20-missing-benchmark), [oq-u8-u10-optests](ANSWERS_60.md#oq-u8-u10-optests), [oq-o3-twolists](ANSWERS_60.md#oq-o3-twolists), [oq-typed-absence-provenance-benchmark](ANSWERS_60.md#oq-typed-absence-provenance-benchmark).

<a id="nab20"></a>

## Nab20 — Full Law Identification in Graphical Models of Missing Data: Completeness Results

**Авторы:** Razieh Nabi; Rohit Bhattacharya; Ilya Shpitser. **Год/версия:** 2020. **Издание:** ICML 2020, PMLR 119, 7153–7163.

**Источник:** [Full Law Identification in Graphical Models of Missing Data: Completeness Results](https://arxiv.org/abs/2004.04872).

**Доступ и место:** PDF: Th.1–4, с.7–9; обсуждение с.9–10.

**Что можно использовать:** Идентификация полного закона условна на графическую модель и positivity; препятствия self-censoring/colluder/colluding paths различаются по классу графов. Полный закон и целевой закон — разные задачи.

**Предел переноса:** Графические ограничения не выводятся автоматически из произвольных наблюдений. Запись причин пропуска сама не идентифицирует общий MNAR-механизм.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-kappa-provenance](ANSWERS_60.md#oq-kappa-provenance), [oq-o3-twolists](ANSWERS_60.md#oq-o3-twolists), [oq-typed-absence-provenance-benchmark](ANSWERS_60.md#oq-typed-absence-provenance-benchmark).

<a id="gro20"></a>

## Gro20 — Informative missingness in electronic health record systems: the curse of knowing

**Авторы:** Rolf H. H. Groenwold. **Год/версия:** 2020. **Издание:** Diagnostic and Prognostic Research 4, 8.

**Источник:** [Informative missingness in electronic health record systems: the curse of knowing](https://doi.org/10.1186/s41512-020-00077-0).

**Доступ и место:** PDF: The curse of knowing; Methods/Results, с.2–5.

**Что можно использовать:** Практика назначения измерений может нести предсказательную информацию; внедрение модели меняет эту практику и полезность пропусков. Явление показано синтетическими данными.

**Предел переноса:** Это ограничение переноса и feedback измерений, с иллюстративной симуляцией. Стабильность provenance между площадками и временем требует проверки.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-kappa-provenance](ANSWERS_60.md#oq-kappa-provenance), [oq-o20-missing-benchmark](ANSWERS_60.md#oq-o20-missing-benchmark), [oq-typed-absence-provenance-benchmark](ANSWERS_60.md#oq-typed-absence-provenance-benchmark).

<a id="ver23"></a>

## Ver23 — The Formats of Cognitive Representation: A Computational Account

**Авторы:** Dimitri Coelho Mollo; Alfredo Vernazzani. **Год/версия:** 2024 (онлайн 2023). **Издание:** Philosophy of Science 91(3), 682–701.

**Источник:** [The Formats of Cognitive Representation: A Computational Account](https://doi.org/10.1017/psa.2023.123).

**Доступ и место:** Ранее проверенный первичный текст: §§3.1–3.2, T1/T2; пакет 2026-09-12.

**Что можно использовать:** Формат представления описывается через вычислительно значимые свойства носителей, взаимные ограничения и доступные преобразования.

**Предел переноса:** Концептуальная теория форматов. Не задаёт числа уровней, полноту словаря Д или порядок ФТС.

**Связь с ФТС:** analogy; поддерживается только указанная компонента. **Связанные OQ:** [oq-formulas-7-11-done](ANSWERS_60.md#oq-formulas-7-11-done), [oq-u6-u7-compositional-semantics](ANSWERS_60.md#oq-u6-u7-compositional-semantics), [oq-code-link-vs-leads-to](ANSWERS_60.md#oq-code-link-vs-leads-to), [oq-node11-asymmetry](ANSWERS_60.md#oq-node11-asymmetry), [oq-dict-d-completeness](ANSWERS_60.md#oq-dict-d-completeness), [oq-passport-u14-u15](ANSWERS_60.md#oq-passport-u14-u15), [oq-u12-antimode-gate](ANSWERS_60.md#oq-u12-antimode-gate), [oq-const-statistics-code](ANSWERS_60.md#oq-const-statistics-code), [oq-unit-circle-z15](ANSWERS_60.md#oq-unit-circle-z15), [oq-canon-star-fate](ANSWERS_60.md#oq-canon-star-fate), [oq-d4-column-precision](ANSWERS_60.md#oq-d4-column-precision), [oq-pentad-role-cycle](ANSWERS_60.md#oq-pentad-role-cycle), [oq-u0-u7-refinement-protocol](ANSWERS_60.md#oq-u0-u7-refinement-protocol).

<a id="ham13"></a>

## Ham13 — Index Classes for Vector Fields and their Relation to Certain Characteristic Classes

**Авторы:** Oskar Hamlet. **Год/версия:** 2013. **Издание:** Mathematica Scandinavica 112(2), 216–224.

**Источник:** [Index Classes for Vector Fields and their Relation to Certain Characteristic Classes](https://doi.org/10.7146/math.scand.a-15241).

**Доступ и место:** PDF: Introduction, Th.1.1/1.3/1.4, с.1–2.

**Что можно использовать:** Для гладкого компактного ориентированного многообразия и поля с изолированными нулями, ненулевого на границе, относительная формула включает внутренние и граничные индексы.

**Предел переноса:** Нужны заданные многообразие, касательное поле и условия границы. Список нулей скалярной формы не устанавливает этих объектов или сферы У6.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-upper-12-17-done](ANSWERS_60.md#oq-upper-12-17-done), [oq-u12-radius-r](ANSWERS_60.md#oq-u12-radius-r), [oq-u12-antimode-gate](ANSWERS_60.md#oq-u12-antimode-gate), [oq-sphere-u6-carrier](ANSWERS_60.md#oq-sphere-u6-carrier), [oq-zero-classes-chi-e](ANSWERS_60.md#oq-zero-classes-chi-e).

<a id="lor26"></a>

## Lor26 — Causal and Compositional Abstraction

**Авторы:** Robin Lorenz; Sean Tull. **Год/версия:** 2026. **Издание:** arXiv v1, препринт.

**Источник:** [Causal and Compositional Abstraction](https://arxiv.org/abs/2602.16612).

**Доступ и место:** Ранее проверенный первичный текст: §4 Def.14–16 Eq.15; пакет 2026-09-12.

**Что можно использовать:** Согласуются переводы состояний, запросов и их результатов; направления переводов и условия отдельных предложений различаются.

**Предел переноса:** Препринт и кандидат аппарата сравнения. Не устанавливает конкретные π/Expand или оператор верхнего уровня ФТС.

**Связь с ФТС:** alternative; поддерживается только указанная компонента. **Связанные OQ:** [oq-upper-12-17-done](ANSWERS_60.md#oq-upper-12-17-done), [oq-u6-u7-compositional-semantics](ANSWERS_60.md#oq-u6-u7-compositional-semantics), [oq-node11-asymmetry](ANSWERS_60.md#oq-node11-asymmetry), [oq-pi-projection-above-u7](ANSWERS_60.md#oq-pi-projection-above-u7), [oq-arity-window-13-14](ANSWERS_60.md#oq-arity-window-13-14), [oq-passport-u14-u15](ANSWERS_60.md#oq-passport-u14-u15), [oq-tot-groups-8-11](ANSWERS_60.md#oq-tot-groups-8-11), [oq-u13-boundary-union-op](ANSWERS_60.md#oq-u13-boundary-union-op), [oq-u14-worlds-agg-op](ANSWERS_60.md#oq-u14-worlds-agg-op), [oq-canon-star-fate](ANSWERS_60.md#oq-canon-star-fate), [oq-synthesis-c-assembly](ANSWERS_60.md#oq-synthesis-c-assembly), [oq-pentad-role-cycle](ANSWERS_60.md#oq-pentad-role-cycle), [oq-u0-u7-refinement-protocol](ANSWERS_60.md#oq-u0-u7-refinement-protocol).

<a id="jag15"></a>

## Jag15 — STFT Phase Retrieval: Uniqueness Guarantees and Recovery Algorithms

**Авторы:** Kishore Jaganathan; Yonina C. Eldar; Babak Hassibi. **Год/версия:** 2016 (препринт 2015). **Издание:** IEEE Journal of Selected Topics in Signal Processing 10(4), 770–781.

**Источник:** [STFT Phase Retrieval: Uniqueness Guarantees and Recovery Algorithms](https://doi.org/10.1109/JSTSP.2016.2549507).

**Доступ и место:** PDF: §III Th.III.1, TableI; с.3–4.

**Что можно использовать:** Для определённых nonvanishing сигналов/окон, перекрытия и количества измерений STFT-модули определяют почти все сигналы с точностью до общей фазы. Уникальность зависит от ограниченного класса.

**Предел переноса:** Теорема не относится ко всем сигналам и параметрам. Модульные измерения могут уже содержать восстановимую фазу, поэтому преимущество phase-aware модели требует отдельной диагностики.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-phase-causal-u9](ANSWERS_60.md#oq-phase-causal-u9), [oq-unit-circle-z15](ANSWERS_60.md#oq-unit-circle-z15), [oq-d10-phase-test](ANSWERS_60.md#oq-d10-phase-test), [oq-synthesis-c-assembly](ANSWERS_60.md#oq-synthesis-c-assembly).

<a id="gro22"></a>

## Gro22 — Non-Uniqueness Theory in Sampled STFT Phase Retrieval

**Авторы:** Philipp Grohs; Lukas Liehr. **Год/версия:** 2023 (препринт 2022). **Издание:** SIAM Journal on Mathematical Analysis 55(5), 4695–4726.

**Источник:** [Non-Uniqueness Theory in Sampled STFT Phase Retrieval](https://doi.org/10.1137/22M1510224).

**Доступ и место:** PDF: Th.1.1, Cor.1.2, с.5.

**Что можно использовать:** Для оговорённых решёток и g∈L² существуют пары L²-сигналов с одинаковыми sampled STFT-модулями, не различающиеся лишь общей фазой.

**Предел переноса:** Неединственность на неограниченном L²-классе не исключает инъективности на заданном конечном/ограниченном классе данных. Перенос предпосылок необходимо проверять.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-phase-causal-u9](ANSWERS_60.md#oq-phase-causal-u9), [oq-d10-phase-test](ANSWERS_60.md#oq-d10-phase-test), [oq-d2-sign-retrieval-remainder](ANSWERS_60.md#oq-d2-sign-retrieval-remainder).

<a id="gyo23"></a>

## Gyo23 — Lossless Transformations and Excess Risk Bounds in Statistical Inference

**Авторы:** László Györfi; Tamás Linder; Harro Walk. **Год/версия:** 2023. **Издание:** Entropy 25(10), 1394.

**Источник:** [Lossless Transformations and Excess Risk Bounds in Statistical Inference](https://doi.org/10.3390/e25101394).

**Доступ и место:** PDF: Def.1 с.2; Th.1 с.4; Th.3 с.12.

**Что можно использовать:** При фиксированном законе универсальное сохранение Bayes minimum risk для всех потерь эквивалентно условной независимости Y и X при T(X). Сохранение одного loss слабее этого условия.

**Предел переноса:** Исполнитель в определении не ограничен вычислительным бюджетом. Для QuestionGain при конечной цене нужны дополнительные класс исполнителей и ресурсная модель.

**Связь с ФТС:** direct; поддерживается только указанная компонента. **Связанные OQ:** [oq-phase-causal-u9](ANSWERS_60.md#oq-phase-causal-u9), [oq-u0-absence-distinction-boundary](ANSWERS_60.md#oq-u0-absence-distinction-boundary), [oq-pi-projection-above-u7](ANSWERS_60.md#oq-pi-projection-above-u7), [oq-u8-u10-optests](ANSWERS_60.md#oq-u8-u10-optests), [oq-d11-branch-bit-test](ANSWERS_60.md#oq-d11-branch-bit-test), [oq-forms8plus-ratio](ANSWERS_60.md#oq-forms8plus-ratio), [oq-tot-groups-8-11](ANSWERS_60.md#oq-tot-groups-8-11), [oq-u13-boundary-union-op](ANSWERS_60.md#oq-u13-boundary-union-op), [oq-d10-phase-test](ANSWERS_60.md#oq-d10-phase-test), [oq-mprime-audit](ANSWERS_60.md#oq-mprime-audit), [oq-d2-half-overlay](ANSWERS_60.md#oq-d2-half-overlay), [oq-d2-sign-retrieval-remainder](ANSWERS_60.md#oq-d2-sign-retrieval-remainder), [oq-roots-of-unity-z368](ANSWERS_60.md#oq-roots-of-unity-z368), [oq-fourier-questiongain](ANSWERS_60.md#oq-fourier-questiongain), [oq-divorce-cases-genre](ANSWERS_60.md#oq-divorce-cases-genre), [oq-vieta-cubic-s3](ANSWERS_60.md#oq-vieta-cubic-s3), [oq-u0-u7-refinement-protocol](ANSWERS_60.md#oq-u0-u7-refinement-protocol).

<a id="win18b"></a>

## Win18b — Contextual predictability shapes signal autonomy

**Авторы:** James Winters; Simon Kirby; Kenny Smith. **Год/версия:** 2018. **Издание:** Cognition 176, 15–30.

**Источник:** [Contextual predictability shapes signal autonomy](https://doi.org/10.1016/j.cognition.2018.03.002).

**Доступ и место:** Ранее проверенный авторский PDF: §2.1, §§3.3–3.4, Fig.8–9, Table3–4; пакет 2026-09-12.

**Что можно использовать:** В коммуникационной игре предсказуемый контекст позволяет сигналам быть менее автономными при успешном различении. Дизайн — 120 участников/60 пар.

**Предел переноса:** Эксперимент не изучал сарказм и уровни ФТС. Контекст — часть конкретного механизма, его ресурсы необходимо учитывать.

**Связь с ФТС:** direct; поддерживается только указанная компонента. **Связанные OQ:** [oq-u6-u7-compositional-semantics](ANSWERS_60.md#oq-u6-u7-compositional-semantics), [oq-code-link-vs-leads-to](ANSWERS_60.md#oq-code-link-vs-leads-to), [oq-u0-absence-distinction-boundary](ANSWERS_60.md#oq-u0-absence-distinction-boundary), [oq-u0-u7-refinement-protocol](ANSWERS_60.md#oq-u0-u7-refinement-protocol).

<a id="har90"></a>

## Har90 — The symbol grounding problem

**Авторы:** Stevan Harnad. **Год/версия:** 1990. **Издание:** Physica D 42(1–3), 335–346.

**Источник:** [The symbol grounding problem](https://doi.org/10.1016/0167-2789(90)90087-6).

**Доступ и место:** PDF: §4–5, с.9–11.

**Что можно использовать:** Предложено связывать символические имена с сенсорными/iconic и категориальными представлениями, которые различают обозначаемые объекты.

**Предел переноса:** Это предложение grounding, а не проверка универсального словаря или интернализации окрашенного ярлыка. Авторский способ читать ФТС сверху им не опровергается.

**Связь с ФТС:** analogy; поддерживается только указанная компонента. **Связанные OQ:** [oq-code-link-vs-leads-to](ANSWERS_60.md#oq-code-link-vs-leads-to), [oq-const-statistics-code](ANSWERS_60.md#oq-const-statistics-code).

<a id="wil20"></a>

## Wil20 — Consistency just feels right: Procedural fluency increases confidence in performance.

**Авторы:** Elanor F. Williams; Kristen E. Duke; David Dunning. **Год/версия:** 2020. **Издание:** Journal of Experimental Psychology: General 149(12), 2395–2405.

**Источник:** [Consistency just feels right: Procedural fluency increases confidence in performance.](https://doi.org/10.1037/xge0000779).

**Доступ и место:** Аннотация Undermind; библиография сверена по APA/Crossref.

**Что можно использовать:** В аннотации сообщается, что процедурная согласованность повышает уверенность без повышения точности; эффекты зависят от представлений участников о fluency.

**Предел переноса:** Полный текст не получен; детали условий и численные эффекты не заимствуются. Не основание объективного закона фундаментальности.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-expectation-speed-fundamentality](ANSWERS_60.md#oq-expectation-speed-fundamentality).

<a id="old12"></a>

## Old12 — Can fluency be interpreted as novelty? Retraining the interpretation of fluency in recognition memory.

**Авторы:** Justin M. Olds; Deanne L. Westerman. **Год/версия:** 2012. **Издание:** Journal of Experimental Psychology: Learning, Memory, and Cognition 38(3), 653–664.

**Источник:** [Can fluency be interpreted as novelty? Retraining the interpretation of fluency in recognition memory.](https://doi.org/10.1037/a0026784).

**Доступ и место:** Аннотация Undermind; библиография сверена по APA/Crossref.

**Что можно использовать:** В аннотации описана обучаемая смена прочтения fluency, с зависимостью от явной обратной связи и конкретной манипуляции, без общего переноса на похожие суждения.

**Предел переноса:** Полный текст не получен. Работа ограничивает простое отождествление fluency, знания и универсальной фундаментальности.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-expectation-speed-fundamentality](ANSWERS_60.md#oq-expectation-speed-fundamentality).

<a id="ess22"></a>

## Ess22 — High fluency can improve recognition sensitivity based on learned metacognitive expectations

**Авторы:** Sarah Esser; Clarissa Lustig; Hilde Haider. **Год/версия:** 2022. **Издание:** Frontiers in Psychology 13, 958511.

**Источник:** [High fluency can improve recognition sensitivity based on learned metacognitive expectations](https://doi.org/10.3389/fpsyg.2022.958511).

**Доступ и место:** PDF: Introduction, с.1–2; основной дизайн и результат описаны также в аннотации.

**Что можно использовать:** 33 участника тренировались с чередованием fluent/nonfluent обработки последовательностей; чувствительность узнавания стала выше в fluent-условиях без обнаруженного ответного смещения.

**Предел переноса:** Эффект относится к заданной задаче и обучению. Он не превращает лёгкость обработки в универсальную меру истинности или фундаментальности.

**Связь с ФТС:** direct; поддерживается только указанная компонента. **Связанные OQ:** [oq-expectation-speed-fundamentality](ANSWERS_60.md#oq-expectation-speed-fundamentality).

<a id="hai18"></a>

## Hai18 — Metacognitive ability predicts learning cue-stimulus associations in the absence of external feedback

**Авторы:** Marine Hainguerlot; Jean-Christophe Vergnaud; Vincent de Gardelle. **Год/версия:** 2018. **Издание:** Scientific Reports 8, 5602.

**Источник:** [Metacognitive ability predicts learning cue-stimulus associations in the absence of external feedback](https://doi.org/10.1038/s41598-018-23936-9).

**Доступ и место:** PDF: дизайн с.2; Results с.3–4.

**Что можно использовать:** N=65; метакогнитивная эффективность в отдельной сессии связана с обучением cue-stimulus связям без сообщения правильности ответа. Связь сохранялась при контроле ряда различий участников.

**Предел переноса:** Корреляционный результат, а не интервенция в внутренний ярлык. Участники получали внешние стимулы. Hai18b имеет тот же DOI и не считается независимым источником.

**Связь с ФТС:** direct; поддерживается только указанная компонента. **Связанные OQ:** [oq-reflection-label-internalization](ANSWERS_60.md#oq-reflection-label-internalization), [oq-train-reflection-test](ANSWERS_60.md#oq-train-reflection-test).

<a id="vel24"></a>

## Vel24 — Metacognitive Feelings: A Predictive-Processing Perspective

**Авторы:** Pablo Fernández Velasco; Slawa Loev. **Год/версия:** 2025 (онлайн 2024). **Издание:** Perspectives on Psychological Science 20(4), 691–713.

**Источник:** [Metacognitive Feelings: A Predictive-Processing Perspective](https://doi.org/10.1177/17456916231221976).

**Доступ и место:** PDF: Introduction/Metacognitive Feelings, с.1–2; теоретическая постановка.

**Что можно использовать:** Предложен predictive-processing механизм метакогнитивных чувств и их направляющего действия; различаются implicit feelings и deliberate metacognitive judgments.

**Предел переноса:** Концептуальное предложение с обзором исследований. Не подтверждает причинную эффективность произвольного ярлыка или субъективное переживание у модели.

**Связь с ФТС:** analogy; поддерживается только указанная компонента. **Связанные OQ:** [oq-reflection-label-internalization](ANSWERS_60.md#oq-reflection-label-internalization), [oq-train-reflection-test](ANSWERS_60.md#oq-train-reflection-test).

<a id="voo25"></a>

## Voo25 — Metacognitive confidence and affect – two sides of the same coin?

**Авторы:** Alan Voodla; Andero Uusberg; Kobe Desender. **Год/версия:** 2025. **Издание:** Cognition and Emotion 39(8), 1857–1874.

**Источник:** [Metacognitive confidence and affect – two sides of the same coin?](https://doi.org/10.1080/02699931.2025.2451795).

**Доступ и место:** Аннотация Undermind; библиография сверена по издателю/Crossref.

**Что можно использовать:** Два перцептивных эксперимента в аннотации связывают оценки confidence и affect с evidence, accuracy и expectancy, допускаются разные механизмы объяснения.

**Предел переноса:** Полный текст не получен. Данные об оценках не устанавливают внутреннее использование окраски ярлыка.

**Связь с ФТС:** analogy; поддерживается только указанная компонента. **Связанные OQ:** [oq-reflection-label-internalization](ANSWERS_60.md#oq-reflection-label-internalization).

<a id="hal95"></a>

## Hal95 — Representation Dependence in Probabilistic Inference

**Авторы:** Joseph Y. Halpern; Daphne Koller. **Год/версия:** 2004 (отдельная конференционная версия 1995). **Издание:** Journal of Artificial Intelligence Research 21, 319–356.

**Источник:** [Representation Dependence in Probabilistic Inference](https://doi.org/10.1613/jair.1292).

**Доступ и место:** PDF: §4 Def.4.5/4.8–4.9; Th.4.11/4.16; с.12–16.

**Что можно использовать:** Сильные требования representation independence под faithful embeddings ограничивают недедуктивный вероятностный вывод; результаты требуют перечисленных предпосылок. Работа уточняет слишком сильный тезис версии 1995.

**Предел переноса:** В этом пакете key Hal95 указывает на прочитанный журнал 2004. Результат не доказывает невозможность любой ограниченной инвариантности или всякой иерархии.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-dict-d-completeness](ANSWERS_60.md#oq-dict-d-completeness), [oq-ddelta-weights](ANSWERS_60.md#oq-ddelta-weights).

<a id="xu20"></a>

## Xu20 — A Theory of Usable Information Under Computational Constraints

**Авторы:** Yilun Xu; Shengjia Zhao; Jiaming Song; Russell Stewart; Stefano Ermon. **Год/версия:** 2020. **Издание:** ICLR 2020; arXiv.

**Источник:** [A Theory of Usable Information Under Computational Constraints](https://arxiv.org/abs/2002.10689).

**Доступ и место:** PDF: §2 Def.1–3, Proposition1; с.2–4.

**Что можно использовать:** Предиктивная V-информация зависит от разрешённого семейства предикторов; вычисление может повысить её доступность. Без ограничений она сводится к обычной информационной постановке.

**Предел переноса:** Рост V-информации не означает создание новой Shannon-информации. Полная цена построения признаков и тождество классов исполнителей требуют собственного учёта.

**Связь с ФТС:** direct; поддерживается только указанная компонента. **Связанные OQ:** [oq-cost-model-scope](ANSWERS_60.md#oq-cost-model-scope), [oq-d2-half-overlay](ANSWERS_60.md#oq-d2-half-overlay), [oq-synthesis-c-assembly](ANSWERS_60.md#oq-synthesis-c-assembly), [oq-roots-of-unity-z368](ANSWERS_60.md#oq-roots-of-unity-z368), [oq-padic-carrier-channel](ANSWERS_60.md#oq-padic-carrier-channel), [oq-fourier-questiongain](ANSWERS_60.md#oq-fourier-questiongain).

<a id="con03"></a>

## Con03 — Definition and Complexity of Some Basic Metareasoning Problems

**Авторы:** Vincent Conitzer; Tuomas Sandholm. **Год/версия:** 2003. **Издание:** arXiv v1, 2003.

**Источник:** [Definition and Complexity of Some Basic Metareasoning Problems](https://arxiv.org/abs/cs/0307017).

**Доступ и место:** PDF: Introduction, с.1; формулировки задач из введения.

**Что можно использовать:** Распределение вычислительного времени, оценка альтернатив и выбор информационных действий имеют сложные частные случаи; метарассуждение само требует ресурсов.

**Предел переноса:** Нормативная полезность не даёт бесплатного алгоритма выбора вопроса. Сложностные утверждения относятся к заданным задачам статьи.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-cost-model-scope](ANSWERS_60.md#oq-cost-model-scope), [oq-next-question-principle](ANSWERS_60.md#oq-next-question-principle).

<a id="mar25c"></a>

## Mar25c — Learning with the p-adics

**Авторы:** André F. T. Martins. **Год/версия:** 2025. **Издание:** arXiv, исследовательский препринт.

**Источник:** [Learning with the p-adics](https://arxiv.org/abs/2512.22692).

**Доступ и место:** PDF: §§2–5, с.3–18; §§6–7, с.18–21.

**Что можно использовать:** При простом p заданы поле, ультраметрика, классификаторы через p-adic balls и алгоритмы регрессии; приведена конструкция Quillian-сети.

**Предел переноса:** Автор отмечает exploratory характер и открытые вопросы. Нет установленного универсального выигрыша, порядка уровней или отождествления Hensel lift с OP_Lift.

**Связь с ФТС:** alternative; поддерживается только указанная компонента. **Связанные OQ:** [oq-padic-carrier-channel](ANSWERS_60.md#oq-padic-carrier-channel).

<a id="kar94"></a>

## Kar94 — Hierarchical structures and asymmetric stochastic processes on p-adics and adeles

**Авторы:** Witold Karwowski; R. Vilela Mendes. **Год/версия:** 1994. **Издание:** Journal of Mathematical Physics 35(9), 4637–4650.

**Источник:** [Hierarchical structures and asymmetric stochastic processes on p-adics and adeles](https://doi.org/10.1063/1.530805).

**Доступ и место:** Аннотация Undermind; библиография сверена по AIP/Crossref.

**Что можно использовать:** В аннотации иерархические пространства состояний описываются ультраметрическими расстояниями и p-адическими стохастическими процессами, включая асимметричные переходы.

**Предел переноса:** Полный текст не получен. Применимость такого носителя к конкретной роли ФТС остаётся задачей.

**Связь с ФТС:** analogy; поддерживается только указанная компонента. **Связанные OQ:** [oq-padic-carrier-channel](ANSWERS_60.md#oq-padic-carrier-channel).

<a id="kni19"></a>

## Kni19 — Poincare Hopf for vector fields on graphs

**Авторы:** Oliver Knill. **Год/версия:** 2019. **Издание:** arXiv v1, препринт.

**Источник:** [Poincare Hopf for vector fields on graphs](https://arxiv.org/abs/1911.04208).

**Доступ и место:** PDF: §1.1–1.6 Th.1, с.1–2; §2, с.2–3.

**Что можно использовать:** Дискретная конструкция задаёт конечный симплициальный комплекс, карту доминирующей вершины и суммы энергий симплексов; сумма индексов сохраняет χ_E.

**Предел переноса:** Нужно сначала определить этот комплекс и карту. Скалярная форма или простой список корней их не задают; журнальная публикация не установлена.

**Связь с ФТС:** alternative; поддерживается только указанная компонента. **Связанные OQ:** [oq-sphere-u6-carrier](ANSWERS_60.md#oq-sphere-u6-carrier), [oq-zero-classes-chi-e](ANSWERS_60.md#oq-zero-classes-chi-e).

<a id="roe85"></a>

## Roe85 — Aggregation of independent Paretian random variables

**Авторы:** Bertrand Roehner; Peter Winiwarter. **Год/версия:** 1985. **Издание:** Advances in Applied Probability 17(2), 465–469.

**Источник:** [Aggregation of independent Paretian random variables](https://doi.org/10.2307/1427153).

**Доступ и место:** PDF: §3 Proposition2, с.3–5 (журнальные 467–469).

**Что можно использовать:** Для i.i.d. Pareto в диапазонах 0<α<1 и 1<α<2 выбраны масштабы n^(1/α) и соответствующая центровка, получен устойчивый предел; рассмотрены также хвосты конечных сумм.

**Предел переноса:** Пример показывает возможность иной агрегации при отсутствии дисперсии. Общие тяжёлые хвосты требуют условий области притяжения, а роль У6 отдельно не установлена.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-levy-world](ANSWERS_60.md#oq-levy-world).

<a id="lam11"></a>

## Lam11 — Corrections to the Central Limit Theorem for Heavy-tailed Probability Densities

**Авторы:** Henry Lam; Jose Blanchet; Damian Burch; Martin Z. Bazant. **Год/версия:** 2011. **Издание:** Journal of Theoretical Probability 24(4), 895–927.

**Источник:** [Corrections to the Central Limit Theorem for Heavy-tailed Probability Densities](https://doi.org/10.1007/s10959-011-0379-y).

**Доступ и место:** PDF: Eq.1 с.1; §2.1 Eq.4 с.5; Th.1/2 с.6–7.

**Что можно использовать:** Разобран конечнодисперсионный CLT и поправки Edgeworth при доступных моментах. Тяжёлые хвосты с показателями >2 требуют специальных последующих членов и регулярности.

**Предел переноса:** Теоремы этой статьи не переносятся на бесконечнодисперсионные stable limits. Кубическая кумулянта не устанавливает причинный смысл У9.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-levy-world](ANSWERS_60.md#oq-levy-world), [oq-edgeworth-u9](ANSWERS_60.md#oq-edgeworth-u9).

<a id="rus89b"></a>

## Rus89b — Principles of metareasoning

**Авторы:** Stuart Russell; Eric Wefald. **Год/версия:** 1991 (конференционная версия 1989). **Издание:** Artificial Intelligence 49(1–3), 361–395.

**Источник:** [Principles of metareasoning](https://doi.org/10.1016/0004-3702(91)90015-C).

**Доступ и место:** Аннотация издателя; список публикаций автора.

**Что можно использовать:** Метарассуждение выбирает вычислительные действия по их полезности для внешнего решения в условиях ограниченных ресурсов.

**Предел переноса:** Полный журнальный текст не получен; ссылка автора ведёт на PostScript, чтение через web не поддержано. Это опора общей постановки; единственность порядка ФТС не установлена.

**Связь с ФТС:** alternative; поддерживается только указанная компонента. **Связанные OQ:** [oq-next-question-principle](ANSWERS_60.md#oq-next-question-principle).

<a id="yan03"></a>

## Yan03 — A Universal Approach to Self-Referential Paradoxes, Incompleteness and Fixed Points

**Авторы:** Noson S. Yanofsky. **Год/версия:** 2003. **Издание:** The Bulletin of Symbolic Logic 9(3), 362–386.

**Источник:** [A Universal Approach to Self-Referential Paradoxes, Incompleteness and Fixed Points](https://doi.org/10.2178/bsl/1058448677).

**Доступ и место:** PDF: §2 Th.1, с.5 (журнальная 366).

**Что можно использовать:** Оценка f:T×T→Y и α:Y→Y без неподвижных точек дают диагональную функцию, не представленную этим f; доказательство и типы выписаны явно.

**Предел переноса:** Для ФТС ещё нужны кодирование, допустимость самоприменения и принадлежность диагональной функции разрешённому классу. Теорема не назначает следующий уровень.

**Связь с ФТС:** limiting; поддерживается только указанная компонента. **Связанные OQ:** [oq-antitotality-diagonal-preconditions](ANSWERS_60.md#oq-antitotality-diagonal-preconditions).
