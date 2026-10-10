# Группы вопросов проекта и то, на что они ссылаются

Дата: 2026-10-10. Источники: `work/OPEN_QUESTIONS.md` (103 пункта), `QUESTION_CARDS.jsonl` (402 вопроса к утверждениям), `work/DIALOGUE_NUANCE_JOURNAL.md` (1). Всего 506 вопросов. `AUTHOR_ANSWERS_60.md` содержит 60 тех же пунктов `OPEN_QUESTIONS.md` и отдельно не считается.

Группы назначены ассистентом: для открытых вопросов — вручную по тексту, для карточек — по семейству исходного утверждения. Ссылки (уровни, карточки, проверки, словарь, внешние области, данные, инфраструктура) извлечены автоматически по тексту вопроса и утверждения. Это навигация, не решение и не изменение статусов.

Построчно: [QUESTION_GROUPS.tsv](QUESTION_GROUPS.tsv). Связи карточек с открытыми вопросами: [QUESTION_CROSSREF.tsv](QUESTION_CROSSREF.tsv).

## Сводка

| Группа | Всего | Открытые вопросы (откр./част./закр.) | Карточки | На что ссылается прежде всего |
|---|---:|---|---:|---|
| G01. Грамматика лестницы: операторы, отсутствия, принципы | 45 | 2/0/2 | 41 | операторы `OP_*`, принципы `O_01…O_08`, аксиомы `A*` |
| G02. Нижняя полоса −1…6: смысл и формы уровней | 30 | 3/0/1 | 26 | карточки уровней −1…6 |
| G03. Уровень 7 и переход 6→7 | 26 | 0/1/1 | 24 | У7, `M_07`, `A_07`, `U7_*` |
| G04. Уровни 8–11: формы, тотализации, тесты | 36 | 8/2/0 | 26 | У8–У11, `C-34`, `C-44`, `C-100` |
| G05. Уровни 12–17: прогнозы и операторы | 45 | 9/2/1 | 33 | У12–У17, внешняя математика |
| G06. Зеркало, чётность и границы | 35 | 4/1/1 | 29 | `ADD_*`/`SP_*` зеркала, `Д11`, `C-49…C-60` |
| G07. Окна, узлы и арифметика окон | 63 | 12/2/1 | 48 | теория чисел и групп, Фано, `G60-*` |
| G08. Оверлеи и носители | 51 | 7/2/2 | 40 | комплексная фаза, χ, `O_14` |
| G09. Законы лестницы: словарь Д, правило П, пентады, порядок | 18 | 4/2/0 | 12 | `Д`, `O_07`, `F1`, `F3` |
| G10. Критерии допуска, фальсификация и цена | 35 | 7/1/1 | 26 | `F1…F5`, `O_09…O_19`, κ, цена |
| G11. Эмпирические тесты и данные | 31 | 3/3/0 | 25 | данные и прогоны, `O_20` |
| G12. Внешний контакт, литература и новизна | 14 | 3/1/1 | 9 | Blackwell, категории, HoTT |
| G13. Статусы, канон и инфраструктура проекта | 55 | 2/0/10 | 43 | граф, экспорт, К1–К5 |
| G14. Авторская механика: абсолютизация, противовес, счёт, ожидание | 22 | 1/0/0 | 20 | авторский диалог; канон не упоминается |

## G01. Грамматика лестницы: операторы, отсутствия, принципы — 45

**О чём спрашивает.** Как устроены операторы перехода (Tot, Tot±, Lift, Promote, Refuse, Sever, π/ι, Compress₂/Expand₂, Unpack), чем различаются ¬A, 0_A и −A и на каких принципах O_01…O_08 держится лестница.

**На что ссылается.** Почти только внутрь канона: карточки `OP_*`, `O_01…O_08`, `A0…A9`. Уровни и проверки C-NN почти не упоминаются — грамматика описана словами и операторами, а не формулами. Вовне — только категорный паспорт Lift.

Счётчики упоминаний — карточки: O_20 (1), OP_Lift (1), A3 (1); словарь и критерии: O_20 (1); внешнее: категории/HoTT (1), нейросети (1); данные: 1; инфраструктура: 0; явное «решение автора»: 0.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-level-specific-absence`](../../OPEN_QUESTIONS.md#oq-level-specific-absence), [`oq-lift-section-and-category`](../../OPEN_QUESTIONS.md#oq-lift-section-and-category).

Закрытые: `oq-typed-absence-finite-witness`, `oq-lift-typing-passport`.

Утверждения-источники карточек (34): `A0`, `A1`, `A2`, `A3`, `A4`, `A6`, `A7`, `A8`, `A9`, `OP_Compress2`, `OP_Expand2`, `OP_Lift`, `OP_Promote`, `OP_Refuse`, `OP_Sever`, `OP_Tot`, `OP_TotMinus`, `OP_TotPlus`, `OP_Unpack`, `OP_event0A`, `OP_iota`, `OP_pi`, `OQ25_SECTION_NATURALITY`, `O_01`, `O_02`, `O_03`, `O_04`, `O_05`, `O_06`, `O_07`, `O_08`, `O_10`, `O_11`, `PA-C07`.

## G02. Нижняя полоса −1…6: смысл и формы уровней — 30

**О чём спрашивает.** Что значит каждый уровень −1…6 в трёх регистрах, где проходят первые различения (ошибка/отсутствие, код/«ведёт к»), как хранить знак и направление под чётной степенью.

**На что ссылается.** Карточки `U_*`, `M_*`, `CH_*` строгой полосы и уровни 0–6. Внешних областей нет: вопросы обращены к самому канону.

Счётчики упоминаний — уровни: У3 (5), У6 (5), У2 (4), У0 (4), У4 (4), У5 (4), У-1 (3), У1 (3); карточки: CH_02 (1), CH_03 (1), M_02 (1), M_03 (1); проверки: C-65 (1), G60-22 (1); данные: 0; инфраструктура: 0; явное «решение автора»: 1.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-code-link-vs-leads-to`](../../OPEN_QUESTIONS.md#oq-code-link-vs-leads-to), [`oq-u0-absence-distinction-boundary`](../../OPEN_QUESTIONS.md#oq-u0-absence-distinction-boundary), [`oq-u6-direction-bit`](../../OPEN_QUESTIONS.md#oq-u6-direction-bit).

Закрытые: `oq-u5-cross-section`.

Утверждения-источники карточек (24): `CH_00`, `CH_01`, `CH_02`, `CH_03`, `CH_04`, `CH_05`, `CH_06`, `CH_m1`, `M_00`, `M_01`, `M_02`, `M_03`, `M_04`, `M_05`, `M_06`, `M_m1`, `U_00`, `U_01`, `U_02`, `U_03`, `U_04`, `U_05`, `U_06`, `U_m1`.

## G03. Уровень 7 и переход 6→7 — 26

**О чём спрашивает.** Что такое ответ как закрытие окна, чем У7 богаче У6, как соединить МУ7 (`|y|=x²`) с ЛУ7, нужен ли ресурс провенанса.

**На что ссылается.** Уровень 7 (19 упоминаний) и 6 (9); карточки `M_07`, `M_06`, `A_07`, `U7_*`, гейты `T7A–T7C`. Здесь больше всего вопросов, прямо требующих решения автора, и конечные модели вместо теорем.

Счётчики упоминаний — уровни: У7 (19), У6 (9), У4 (3), У5 (3), У0 (2), У1 (2), У2 (2), У3 (2); карточки: M_07 (3), M_06 (2), T7A (1), T7B (1), T7C (1); проверки: C-69 (1), G60-05 (1); внешнее: комплексные числа/фаза (1), нейросети (1); данные: 0; инфраструктура: 0; явное «решение автора»: 3.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-u6-u7-compositional-semantics`](../../OPEN_QUESTIONS.md#oq-u6-u7-compositional-semantics).

Закрытые: `oq-u6-u7-choice-products`.

Утверждения-источники карточек (16): `A_07`, `CH_07`, `M_07`, `OP_WindowClose`, `OQ25_RELATION_PRODUCT`, `OQ25_U6_PROVENANCE`, `U4_U7_TYPED_CANDIDATE`, `U6_Q_NOT_SUFFICIENT_FOR_U7`, `U6_VSTAR_BRIDGE_UNDERDETERMINED`, `U7_AGENTIC_GATE_LAYER`, `U7_FORGET_CLOSE`, `U7_LOGIC_GROUPING`, `U7_MATH_LOCAL_FORBID`, `U7_U8_ANSWER_QUESTION_BOUNDARY`, `U7_WINDOW_CORE`, `U_07`.

## G04. Уровни 8–11: формы, тотализации, тесты — 36

**О чём спрашивает.** Какие формы и операционные тесты у У8–У11, каковы тотализации 8–11 как коллапсы групп, обращение или поворот на шаге к МУ8, как читать МУ9.

**На что ссылается.** Уровни 8–11; проверки `C-34`, `C-44`, `C-100`; критерии `К1`, `К5`, `O_13`. Указывают на то, чего нет: формул π и полушагов выше 7 и уровневых тестов.

Счётчики упоминаний — уровни: У8 (10), У9 (9), У10 (6), У11 (6), У7 (4), У6 (2); карточки: O_13 (1), T7A (1), T7C (1); проверки: C-01 (1), C-21 (1), C-34 (1), G60-17 (1), G60-21 (1), C-44 (1); словарь и критерии: К1 (2), К5 (2), О1 (1), О3 (1), О8 (1), O_13 (1); данные: 0; инфраструктура: 2; явное «решение автора»: 1.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-formulas-7-11-done`](../../OPEN_QUESTIONS.md#oq-formulas-7-11-done), [`oq-pi-projection-above-u7`](../../OPEN_QUESTIONS.md#oq-pi-projection-above-u7), [`oq-u8-u10-optests`](../../OPEN_QUESTIONS.md#oq-u8-u10-optests), [`oq-forms8plus-ratio`](../../OPEN_QUESTIONS.md#oq-forms8plus-ratio), [`oq-tot-groups-8-11`](../../OPEN_QUESTIONS.md#oq-tot-groups-8-11), [`oq-pn-above-u7`](../../OPEN_QUESTIONS.md#oq-pn-above-u7), [`oq-window-7-9-irrational-test`](../../OPEN_QUESTIONS.md#oq-window-7-9-irrational-test), [`oq-mu8-inverse-vs-rotation`](../../OPEN_QUESTIONS.md#oq-mu8-inverse-vs-rotation), [`oq-mu9-opposite-inclusion`](../../OPEN_QUESTIONS.md#oq-mu9-opposite-inclusion), [`oq-mu9-projection-reading`](../../OPEN_QUESTIONS.md#oq-mu9-projection-reading).

Утверждения-источники карточек (19): `ADD_U11_EPI`, `CH_08`, `CH_09`, `CH_10`, `CH_11`, `CM-002`, `CM-003`, `CM-004`, `CM-005`, `M_08`, `M_09`, `M_10`, `M_11`, `SP_U8`, `SP_U9`, `U_08`, `U_09`, `U_10`, `U_11`.

## G05. Уровни 12–17: прогнозы и операторы — 45

**О чём спрашивает.** Какие формулы и операторы у У12–У17, свободен ли радиус r, каковы гейт анти-моды, агрегация миров, гиперболическое и эллиптическое прочтения.

**На что ссылается.** Уровни 12–17 и внешняя математика: комплексные числа, функции Якоби, гиперболические функции, Виета. Десять вопросов — пробелы `TBD`: выше 12 у лестницы больше вопросов, чем форм.

Счётчики упоминаний — уровни: У12 (12), У14 (8), У15 (7), У13 (6), У16 (4), У17 (3); карточки: A5 (1); проверки: G60-03 (2), G60-20 (1), C-28 (1), C-30 (1), C-83 (1); внешнее: комплексные числа/фаза (4), эллиптические функции/Якоби/℘ (3), гиперболические функции (3), Виета/многочлены (3); данные: 0; инфраструктура: 4; явное «решение автора»: 2.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-upper-12-17-done`](../../OPEN_QUESTIONS.md#oq-upper-12-17-done), [`oq-arity-window-13-14`](../../OPEN_QUESTIONS.md#oq-arity-window-13-14), [`oq-passport-u14-u15`](../../OPEN_QUESTIONS.md#oq-passport-u14-u15), [`oq-u12-radius-r`](../../OPEN_QUESTIONS.md#oq-u12-radius-r), [`oq-u12-antimode-gate`](../../OPEN_QUESTIONS.md#oq-u12-antimode-gate), [`oq-u13-boundary-union-op`](../../OPEN_QUESTIONS.md#oq-u13-boundary-union-op), [`oq-u14-worlds-agg-op`](../../OPEN_QUESTIONS.md#oq-u14-worlds-agg-op), [`oq-c83-parity-prediction`](../../OPEN_QUESTIONS.md#oq-c83-parity-prediction), [`oq-u16-phase-hyperbolic-pair`](../../OPEN_QUESTIONS.md#oq-u16-phase-hyperbolic-pair), [`oq-u14-jacobi-aggregation`](../../OPEN_QUESTIONS.md#oq-u14-jacobi-aggregation), [`oq-u12-hyperbolic-antimode-guard`](../../OPEN_QUESTIONS.md#oq-u12-hyperbolic-antimode-guard).

Закрытые: `oq-u12-antimode-authorfix`.

Утверждения-источники карточек (26): `ADD_U12_CIRCLE`, `CH_12`, `CH_13`, `CH_14`, `CH_15`, `CH_16`, `CH_17`, `CM-006`, `CM-007`, `CM-008`, `CM-012`, `M_12`, `M_13`, `M_14`, `M_15`, `M_16`, `M_17`, `PA-F08`, `PA-F09`, `SP_U12`, `U_12`, `U_13`, `U_14`, `U_15`, `U_16`, `U_17`.

## G06. Зеркало, чётность и границы — 35

**О чём спрашивает.** Почему F=−F ⟺ F=0, что сохраняет модуль, как бит ветви (Д11) различает то, что недоступно разности, есть ли третья граница, что такое φ- и константные границы.

**На что ссылается.** Карточки `ADD_MIRROR_WINDOW`, `ADD_ZERO_BOUNDARY`, `SP_WINDOW`, `SP_ZERO`; словарь `Д11`, `Д10`; проверки `C-49…C-52`, `C-60`, `C-76`. Математика здесь доказана; вопросы — о мосте к смыслу.

Счётчики упоминаний — уровни: У8 (4), У2 (1), У3 (1), У4 (1), У5 (1), У6 (1), У7 (1), У9 (1); карточки: ADD_MIRROR_WINDOW (2), SP_WINDOW (1), SP_ZERO (1), ADD_ZERO_BOUNDARY (1); проверки: C-49 (1), C-52 (1), G60-08 (1), C-21 (1), G60-14 (1), C-60 (1); словарь и критерии: Д11 (3), Д10 (1), О2 (1); внешнее: комплексные числа/фаза (4), Виета/многочлены (2), топология/χ_E/сфера/тор (2), логика/диагональ (1), кватернионы/октонионы/Фано (1), теория групп/Галуа/вычеты (1); данные: 0; инфраструктура: 2; явное «решение автора»: 0.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-d11-branch-bit-test`](../../OPEN_QUESTIONS.md#oq-d11-branch-bit-test), [`oq-third-boundary`](../../OPEN_QUESTIONS.md#oq-third-boundary), [`oq-const-statistics-code`](../../OPEN_QUESTIONS.md#oq-const-statistics-code), [`oq-unit-circle-z15`](../../OPEN_QUESTIONS.md#oq-unit-circle-z15), [`oq-vieta-cubic-s3`](../../OPEN_QUESTIONS.md#oq-vieta-cubic-s3).

Закрытые: `oq-parity-witness-done`.

Утверждения-источники карточек (19): `ADD_CONSTANTS`, `ADD_HALF_PHI`, `ADD_MIRROR_WINDOW`, `ADD_PARITY_TOPOLOGY`, `ADD_TOPO_INVARIANTS`, `ADD_ZERO_BOUNDARY`, `CM-001`, `CM-010`, `CM-013`, `CM-014`, `CM-016`, `PA-F01`, `PA-F02`, `PA-F03`, `PA-F06`, `PA-F07`, `PA-F11`, `SP_WINDOW`, `SP_ZERO`.

## G07. Окна, узлы и арифметика окон — 63

**О чём спрашивает.** Что значат семейства окон, пересечения и узлы, откуда канал mod 3, что значат √5, √−7, √−2 для окон, какие знаковые модели (H4/S4, O8/B8, Фано) подходят окнам 13/25.

**На что ссылается.** Сильнее всего вовне: теория чисел и групп (11), кватернионы/октонионы/Фано (10), комплексные числа (8), Серпинский (4); проверки `G60-*`, `C-102`, `C-103`. Мост «числа → уровни» не построен — вопросы ссылаются скорее на арифметику, чем на уровни.

Счётчики упоминаний — уровни: У7 (4), У15 (3), У12 (2), У6 (2), У17 (2), У5 (2), У11 (1), У13 (1); карточки: M_06 (2), M_07 (2), A0b (1), A6 (1), OP_Lift (1), U_15 (1); проверки: G60-23 (2), G60-11 (1), G60-15 (1), G60-24 (1), G60-28 (1), C-49 (1); словарь и критерии: О1 (1); внешнее: теория групп/Галуа/вычеты (11), кватернионы/октонионы/Фано (10), комплексные числа/фаза (8), фрактал/Серпинский (4), топология/χ_E/сфера/тор (3), эллиптические функции/Якоби/℘ (2); данные: 0; инфраструктура: 0; явное «решение автора»: 2.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-node11-asymmetry`](../../OPEN_QUESTIONS.md#oq-node11-asymmetry), [`oq-roots-of-unity-z368`](../../OPEN_QUESTIONS.md#oq-roots-of-unity-z368), [`oq-padic-carrier-channel`](../../OPEN_QUESTIONS.md#oq-padic-carrier-channel), [`oq-mod3-channel-origin`](../../OPEN_QUESTIONS.md#oq-mod3-channel-origin), [`oq-minimal-windows-projects-to`](../../OPEN_QUESTIONS.md#oq-minimal-windows-projects-to), [`oq-window25-sqrt-minus2`](../../OPEN_QUESTIONS.md#oq-window25-sqrt-minus2), [`oq-windows11-15-quadratic-meaning`](../../OPEN_QUESTIONS.md#oq-windows11-15-quadratic-meaning), [`oq-number-level-semantic-bridge`](../../OPEN_QUESTIONS.md#oq-number-level-semantic-bridge), [`oq-window-node-conjugation-origin`](../../OPEN_QUESTIONS.md#oq-window-node-conjugation-origin), [`oq-o1-environment-substitution`](../../OPEN_QUESTIONS.md#oq-o1-environment-substitution), [`oq-sierpinski-node-11`](../../OPEN_QUESTIONS.md#oq-sierpinski-node-11), [`oq-window-family-roles`](../../OPEN_QUESTIONS.md#oq-window-family-roles), [`oq-window-intersection-carrier`](../../OPEN_QUESTIONS.md#oq-window-intersection-carrier), [`oq-window-family-continuation`](../../OPEN_QUESTIONS.md#oq-window-family-continuation).

Закрытые: `oq-step48-symmetry`.

Утверждения-источники карточек (29): `A0b`, `AC_20261003_AUTHOR_DECISION`, `AC_20261003_WINDOWS_FIVES`, `AC_20261003_WINDOWS_SEVENS`, `AC_20261003_WINDOWS_TRIPLES`, `AC_20261003_WINDOW_FAMILIES`, `AC_20261003_WINDOW_FIVES_ALIGNMENT`, `CM-009`, `OQ25_UNITS48`, `PA-F04`, `WINDOW_ARITHMETIC_CATALOG`, `WINDOW_ARITHMETIC_LIMITS`, `WINDOW_BOUNDARY_22`, `WINDOW_CIRCLE_CANDIDATE`, `WINDOW_COMMON_NODE_CANDIDATE`, `WINDOW_FANO_NESTED`, `WINDOW_FANO_NUMBERING_LIMIT`, `WINDOW_FANO_SIGN_CYCLE`, `WINDOW_GROUPINGS`, `WINDOW_GROUPING_13`, `WINDOW_GROUPING_25`, `WINDOW_NESTING_SIERPINSKI`, `WINDOW_NODE_INNER_NONUNIQUE`, `WINDOW_NUMBER_ALGEBRA_SCOPE`, `WINDOW_RELATIVE_SIGN_PROBE`, `WINDOW_SIGN_INTERFACE_UNDEFINED`, `WINDOW_SIGN_MODELS_INEQUIVALENT`, `WINDOW_SIGN_SHADOW_INVARIANT`, `WINDOW_WEIERSTRASS_CONTEXT`.

## G08. Оверлеи и носители — 51

**О чём спрашивает.** Даёт ли носитель (χ-статистика, комплексный, тензорный, сфера/тор, ЦПТ и мир Леви, Фурье) роль сверх переописания; какие тесты (Д10, phase retrieval) это решают.

**На что ссылается.** Комплексные числа и фаза (21), χ-статистика (16), ЦПТ/Леви/Эджворт; критерии `O_14` (QuestionGain), `F3`. Общий риск группы — «оверлей = подстановка»: роль надо доказать тестом, а не статусом.

Счётчики упоминаний — уровни: У6 (9), У7 (6), У8 (6), У9 (6), У11 (4), У12 (4), У10 (3), У4 (3); карточки: O_14 (2), ADD_TOPO_INVARIANTS (2), COMPLEX_LADDER_U8 (1), F3 (1), ADD_PARITY_TOPOLOGY (1), CH_06 (1); проверки: C-53 (1), C-56 (1), C-19 (1), G60-13 (1), G60-25 (1), G60-27 (1); словарь и критерии: Д10 (1), Д11 (1), O_14 (2), F3 (1), К1 (1), O_19 (1); внешнее: комплексные числа/фаза (21), χ-статистика (16), топология/χ_E/сфера/тор (2), вероятность/ЦПТ/Леви/Эджворт (2), Фурье (1); данные: 1; инфраструктура: 1; явное «решение автора»: 1.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-phase-causal-u9`](../../OPEN_QUESTIONS.md#oq-phase-causal-u9), [`oq-d10-phase-test`](../../OPEN_QUESTIONS.md#oq-d10-phase-test), [`oq-d2-half-overlay`](../../OPEN_QUESTIONS.md#oq-d2-half-overlay), [`oq-synthesis-c-assembly`](../../OPEN_QUESTIONS.md#oq-synthesis-c-assembly), [`oq-sphere-u6-carrier`](../../OPEN_QUESTIONS.md#oq-sphere-u6-carrier), [`oq-fourier-questiongain`](../../OPEN_QUESTIONS.md#oq-fourier-questiongain), [`oq-zero-classes-chi-e`](../../OPEN_QUESTIONS.md#oq-zero-classes-chi-e), [`oq-levy-world`](../../OPEN_QUESTIONS.md#oq-levy-world), [`oq-edgeworth-u9`](../../OPEN_QUESTIONS.md#oq-edgeworth-u9).

Закрытые: `oq-chi-ladder-done`, `oq-8plus-only-refuted`.

Утверждения-источники карточек (34): `CHI_CARRIER`, `CHI_LADDER_U10`, `CHI_LADDER_U11`, `CHI_LADDER_U6`, `CHI_LADDER_U7`, `CHI_LADDER_U8`, `CHI_LADDER_U9`, `CHI_STAT_LADDER`, `CM-011`, `CM-015`, `COMPLEX_BRANCH_OVERLAY`, `COMPLEX_CARRIER`, `COMPLEX_LADDER_U10`, `COMPLEX_LADDER_U11`, `COMPLEX_LADDER_U12`, `COMPLEX_LADDER_U6`, `COMPLEX_LADDER_U7`, `COMPLEX_LADDER_U8`, `COMPLEX_LADDER_U9`, `OP_ChiCarrier`, `OP_ComplexBoundaryBranch`, `OP_ComplexBranchAccess`, `OP_ComplexNormReadout`, `OP_TensorContextMap`, `PA-C06`, `PA-C08`, `PA-F05`, `PA-F10`, `TENSOR_CARRIER`, `TENSOR_CONTEXT_OVERLAY`, `TENSOR_LADDER_U10`, `TENSOR_LADDER_U11`, `TENSOR_LADDER_U12`, `U12_CHI_PI_COMPLEX_BOUNDARY`.

## G09. Законы лестницы: словарь Д, правило П, пентады, порядок — 18

**О чём спрашивает.** Полон ли словарь Д, вынуждено ли правило П, повторяется ли пентада, как выбирается следующий вопрос, точна ли колонка неопределённости, есть ли диагональный аргумент антитотальности.

**На что ссылается.** Метауровень: `O_07`, `F1`, `F3`, `Д1…Д11`, `К1`, `К5`, `A0b`. Ничего не доказано; вопросы ищут закон, из которого лестница следовала бы.

Счётчики упоминаний — уровни: У9 (4), У14 (3), У5 (3), У6 (3), У10 (3), У7 (2), У13 (2), У-1 (1); карточки: O_07 (2), A0b (2), F1 (1), A1 (1), A2 (1), A3 (1); проверки: G60-11 (1), G60-18 (1); словарь и критерии: Д2 (1), Д3 (1), Д1 (1), Д11 (1), O_07 (2), К1 (2); внешнее: комплексные числа/фаза (3), теория групп/Галуа/вычеты (1), фрактал/Серпинский (1), нейросети (1), логика/диагональ (1); данные: 0; инфраструктура: 1; явное «решение автора»: 0.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-dict-d-completeness`](../../OPEN_QUESTIONS.md#oq-dict-d-completeness), [`oq-d4-column-precision`](../../OPEN_QUESTIONS.md#oq-d4-column-precision), [`oq-pentad-role-cycle`](../../OPEN_QUESTIONS.md#oq-pentad-role-cycle), [`oq-next-question-principle`](../../OPEN_QUESTIONS.md#oq-next-question-principle), [`oq-u0-u7-refinement-protocol`](../../OPEN_QUESTIONS.md#oq-u0-u7-refinement-protocol), [`oq-antitotality-diagonal-preconditions`](../../OPEN_QUESTIONS.md#oq-antitotality-diagonal-preconditions).

Утверждения-источники карточек (7): `CM-023`, `CM-024`, `PA-C01`, `PA-C02`, `PA-C03`, `PA-C04`, `PA-C05`.

## G10. Критерии допуска, фальсификация и цена — 35

**О чём спрашивает.** Что значит законное закрытие (κ), какие фальсификаторы F1–F5 и как работают, как устроена цена C(E) и веса, что должна покрыть альтернатива M′.

**На что ссылается.** Карточки `F1…F5`, `O_09`, `O_12…O_19`, `T7A–C`, `OP_kappa`; критерии `К2`, `К4`, `К5`, `О2`. Указывают на незавершённую модель цены и непроведённый M′-аудит.

Счётчики упоминаний — уровни: У7 (3), У12 (1), У4 (1), У5 (1), У6 (1); карточки: F3 (2), A1 (1), A2 (1), A6 (1), F1 (1), F5 (1); проверки: C-34 (1); словарь и критерии: Д11 (1), F3 (3), О2 (2), F6 (1), К2 (1), К4 (1); внешнее: нейросети (1), χ-статистика (1); данные: 0; инфраструктура: 0; явное «решение автора»: 0.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-ce-canon`](../../OPEN_QUESTIONS.md#oq-ce-canon), [`oq-kappa-provenance`](../../OPEN_QUESTIONS.md#oq-kappa-provenance), [`oq-redteam-dependent-guards`](../../OPEN_QUESTIONS.md#oq-redteam-dependent-guards), [`oq-ce-weights-proof`](../../OPEN_QUESTIONS.md#oq-ce-weights-proof), [`oq-cost-model-scope`](../../OPEN_QUESTIONS.md#oq-cost-model-scope), [`oq-mprime-audit`](../../OPEN_QUESTIONS.md#oq-mprime-audit), [`oq-ddelta-weights`](../../OPEN_QUESTIONS.md#oq-ddelta-weights), [`oq-two-channel-k245`](../../OPEN_QUESTIONS.md#oq-two-channel-k245).

Закрытые: `oq-redteam-f3-done`.

Утверждения-источники карточек (21): `A5`, `A5a`, `DR10_QG_WITNESS`, `F1`, `F2`, `F3`, `F4`, `F5`, `OP_kappa`, `O_09`, `O_12`, `O_13`, `O_14`, `O_15`, `O_16`, `O_17`, `O_18`, `O_19`, `T7A`, `T7B`, `T7C`.

## G11. Эмпирические тесты и данные — 31

**О чём спрашивает.** Подтверждается ли типизированное отсутствие, внешняя роль знака и фазы, рефлексия на примере поезда, нейросетевой scaffold; как поставить честный следующий тест.

**На что ссылается.** Данные и эксперименты (16 из 31 упоминают датасеты, предрегистрацию, прогоны): `o20/`, `d2_sign/`, `d10_phase/`, `train_reflection/`; критерий `O_20`. Внешние проверки O_20, D2 и Д10 дали отрицательный или смешанный итог; нейросетевой scaffold остаётся кандидатом на синтетических данных.

Счётчики упоминаний — уровни: У11 (1), У8 (1), У9 (1); карточки: O_20 (2); словарь и критерии: Д10 (1), O_20 (3), О3 (1); внешнее: комплексные числа/фаза (5), нейросети (3); данные: 16; инфраструктура: 0; явное «решение автора»: 0.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-o20-missing-benchmark`](../../OPEN_QUESTIONS.md#oq-o20-missing-benchmark), [`oq-reflection-label-internalization`](../../OPEN_QUESTIONS.md#oq-reflection-label-internalization), [`oq-train-reflection-test`](../../OPEN_QUESTIONS.md#oq-train-reflection-test), [`oq-o3-twolists`](../../OPEN_QUESTIONS.md#oq-o3-twolists), [`oq-d2-sign-retrieval-remainder`](../../OPEN_QUESTIONS.md#oq-d2-sign-retrieval-remainder), [`oq-typed-absence-provenance-benchmark`](../../OPEN_QUESTIONS.md#oq-typed-absence-provenance-benchmark).

Утверждения-источники карточек (15): `AF-005`, `AF-006`, `AF-007`, `AF-014`, `AF-015`, `AF-016`, `CM-020`, `CM-021`, `CM-022`, `NEURAL_T2_SCAFFOLD`, `NEURAL_T3_NOT_VERIFIED`, `O_20`, `PA-R03`, `PA-R04`, `PA-R05`.

## G12. Внешний контакт, литература и новизна — 14

**О чём спрашивает.** Есть ли у ФТС внешний контакт и новизна, переносятся ли Blackwell, категории и HoTT, годится ли жанр «кейсов разведения» как внешняя площадка.

**На что ссылается.** Внешняя литература: Blackwell (5), категории/HoTT (3); уровни 2–5 — единственная полоса с подтверждённым компонентным контактом (У1 — только якорь тождества, AF-018).

Счётчики упоминаний — уровни: У4 (8), У5 (7), У1 (6), У2 (6), У3 (6), У6 (2); карточки: O_14 (1), U_04 (1), U_06 (1); словарь и критерии: O_14 (1), К1 (1); внешнее: Blackwell/теория решений (5), категории/HoTT (3); данные: 0; инфраструктура: 1; явное «решение автора»: 0.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-systematic-literature-review`](../../OPEN_QUESTIONS.md#oq-systematic-literature-review), [`oq-canon-star-fate`](../../OPEN_QUESTIONS.md#oq-canon-star-fate), [`oq-divorce-cases-genre`](../../OPEN_QUESTIONS.md#oq-divorce-cases-genre), [`oq-blackwell-canonical-projection`](../../OPEN_QUESTIONS.md#oq-blackwell-canonical-projection).

Закрытые: `oq-blackwell-u4-u6-witness`.

Утверждения-источники карточек (5): `AF-008`, `AF-018`, `CM-025`, `PA-C09`, `PA-R07`.

## G13. Статусы, канон и инфраструктура проекта — 55

**О чём спрашивает.** Как повышаются статусы (SP, К1–К5), целостен ли граф канона, синхронны ли экспорт, MANIFEST и workbook, что проверено машинно и что воспроизводимо.

**На что ссылается.** Инфраструктура проекта (24 из 55 упоминают граф, экспорт, MANIFEST, проверки); `К1`, `К5` (по 10). Из 12 пунктов `OPEN_QUESTIONS.md` в этой группе 10 уже закрыты — это самая отработанная область.

Счётчики упоминаний — уровни: У7 (9), У12 (8), У9 (5), У10 (4), У8 (3), У11 (2); карточки: U_07 (3), U_12 (3), COMPLEX_LADDER_U9 (1), O_01 (1), O_05 (1), SP_ZERO (1); проверки: C-60 (4), C-28 (2), C-23 (1), G60-19 (1); словарь и критерии: К1 (10), К5 (10), O_01 (1), O_05 (1), О1 (1), О5 (1); внешнее: χ-статистика (5), топология/χ_E/сфера/тор (1), вероятность/ЦПТ/Леви/Эджворт (1), комплексные числа/фаза (1); данные: 0; инфраструктура: 24; явное «решение автора»: 0.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-audit-semantic-repromotion`](../../OPEN_QUESTIONS.md#oq-audit-semantic-repromotion), [`oq-graph-reference-definitions`](../../OPEN_QUESTIONS.md#oq-graph-reference-definitions).

Закрытые: `oq-machine-check-done`, `oq-full-audit-done`, `oq-export-refs-done`, `oq-strict-band-7-export`, `oq-witnesses-verif-done`, `oq-graph-dep-sync`, `oq-txp-verif-done`, `oq-clt-verif-done`, `oq-audit-status-promotions-done`, `oq-audit-canon-reference-repair`.

Утверждения-источники карточек (26): `ADDENDUM_V3`, `ADD_NOTATION_ABS`, `ADD_RESEARCH_FORMAT`, `AF-001`, `AF-002`, `AF-003`, `AF-004`, `AF-009`, `AF-010`, `AF-011`, `AF-012`, `AF-013`, `AF-017`, `AF-019`, `AF-020`, `CM-017`, `CM-018`, `CM-019`, `OQ25_DEFINITION_OPTIONS`, `PA-G01`, `PA-G02`, `PA-G03`, `PA-G04`, `PA-R01`, `PA-R02`, `PA-R06`.

## G14. Авторская механика: абсолютизация, противовес, счёт, ожидание — 22

**О чём спрашивает.** Как абсолютизация с У−1 держит уровни, как противовес переходит от У5 к У7, почему a→a не увеличивает счёт, чем первое полагание отличается от определений, что такое ожидание и внутренний контур.

**На что ссылается.** Авторские пояснения и журнал диалога. Ни одной ссылки на карточку канона или проверку C-NN: это слой, который ещё не связан с формальным аппаратом.

Счётчики упоминаний — уровни: У7 (5), У6 (4), У11 (4), У-1 (4), У0 (4), У1 (4), У8 (2), У9 (2); внешнее: топология/χ_E/сфера/тор (2); данные: 1; инфраструктура: 0; явное «решение автора»: 0.

Незакрытые пункты `OPEN_QUESTIONS.md`: [`oq-expectation-speed-fundamentality`](../../OPEN_QUESTIONS.md#oq-expectation-speed-fundamentality).

Утверждения-источники карточек (10): `DN_20260922_ABSENCE_LIFT`, `DN_20260922_GEOMETRY_SELF`, `DN_20260922_INTERNAL_CONTOUR`, `DN_20260922_SENSITIVITY_RESIDUAL`, `WINDOW_ABSOLUTIZATION_AUTHOR`, `WINDOW_COUNTERWEIGHT_AUTHOR`, `WINDOW_COUNTERWEIGHT_TRANSFER_CANDIDATE`, `WINDOW_COUNTING_AUTHOR`, `WINDOW_FIRST_DISTINCTION_AUTHOR`, `WINDOW_JOINT_SCOPE_DIRECTION`.

## Связи карточек с открытыми вопросами

Ручная сверка нашла 92 связи: тот же вопрос — 46, частный случай — 8, смежный — 30, уже отвечен закрытым пунктом — 7, предпосылка устарела — 1. Полный список — в [QUESTION_CROSSREF.tsv](QUESTION_CROSSREF.tsv).

Где карточки сходятся с одним открытым вопросом сильнее всего:

- `oq-node11-asymmetry` — 4
- `oq-d10-phase-test` — 4
- `oq-o20-missing-benchmark` — 4
- `oq-graph-reference-definitions` — 4
- `oq-u6-u7-compositional-semantics` — 3
- `oq-d2-sign-retrieval-remainder` — 3
- `oq-systematic-literature-review` — 3
- `oq-audit-semantic-repromotion` — 3
- `oq-u8-u10-optests` — 3
- `oq-d2-half-overlay` — 2

Уже отвечены (проверено по источнику, отмечено в `QUESTION_CARDS.jsonl`):

- `Q-AF-012.2` — расхождение JSONL и TSV снято 2026-10-03 (`oq-graph-dep-sync`).
- `Q-AF-013.2…4` — три цикла зависимостей разобраны 2026-10-03: у каждой пары сохранена предпосылка, обратная связь переименована (`applies_to`, `has_operator`). Во втором вопросе пара называется по исторической записи `M_07`; разобрана пара `A_07↔U7_MATH_LOCAL_FORBID`.
- `Q-AF-011.2` — частично: девять алиасов исправлены, остаток — четыре определения (`oq-graph-reference-definitions`).

Устаревшая предпосылка: `Q-M_12.2` спрашивает, почему r=2, а по решению автора от 2026-10-08 r — свободный параметр класса (`oq-u12-radius-r`). Текст карточки `M_12` этого ещё не отражает.

## Наблюдения

1. **Открытые вопросы и вопросы к утверждениям распределены по-разному.** Открытые пункты гуще всего в окнах (G07), верхних уровнях (G05), оверлеях (G08) и уровнях 8–11 (G04): там, где форм ещё нет. Вопросов к утверждениям больше всего в окнах (G07), инфраструктуре (G13), грамматике (G01) и оверлеях (G08). В G01 и G13 утверждений много, а незакрытых пунктов почти нет.
2. **Грамматика почти не спрашивается в `OPEN_QUESTIONS.md`.** У G01 41 вопрос к утверждениям и только два незакрытых пункта (секция Lift и уровневое чтение отсутствия). Операторы `OP_*` фактически считаются решёнными; в вопросах этой группы проверки C-NN не упоминаются ни разу.
3. **Авторская механика (G14) не связана с каноном.** 22 вопроса и ни одной ссылки на карточку или проверку. Это самый неустоявшийся слой: пояснения автора о противовесе, абсолютизации и ожидании пока не имеют формы.
4. **Окна (G07) ссылаются наружу, а не на уровни.** Теория чисел, группы, Фано и октонионы встречаются чаще уровней; мост «числа → уровни» (`oq-number-level-semantic-bridge`) остаётся открытым.
5. **Выше 12 у лестницы больше вопросов, чем форм.** Десять из 45 вопросов G05 — пробелы `TBD`.
6. **Инфраструктура (G13) отработана.** Из 12 пунктов закрыты 10; открыты повторная канонизация У7…У12 и четыре определения графа.
7. **Сквозная нить — бит ветви и Tot.** Она связывает G03 (МУ7 и `Tot(МУ7)=МУ6`), G06 (Д11, отношения ±1), G08 (фаза, phase retrieval) и G04 (тотализации 8–11 как коллапсы групп).

## Что не закрыто

- Группы назначены одной меткой; вопросы на стыке (например, Д11 между G06 и G08) отнесены к одной группе.
- Автоматическое извлечение ссылок пропускает упоминания без явного идентификатора (например, «уровень знания» без «У7») и иногда ловит лишнее; счётчики — ориентир, а не точный подсчёт.
- Связи карточек с открытыми вопросами собраны вручную по смыслу; полнота не гарантирована.
- Ответы не писались, статусы не менялись, `OPEN_QUESTIONS.md` и канон не изменялись.
