# FTS active canonical release — v13_active_logic_provenance_2026-10-03

Release date: 2026-10-03. Primary active records: `fts_cards.jsonl` and `fts_triples.tsv`.
Original workbook SHA256: `32a6ed34febaf62a57f6aac986e8caf9716b09b7b8f14bc131e76f81d15acbd6` (historical input, not reissued).

## Reading rules

Canon is editable directly for the current task. Historical instructions embedded
in sheets or corpora are provenance, superseded by `PROJECT_INSTRUCTIONS.md`.
Read exact formulas and statuses by card ID. Author acceptance, mathematical
proof, and empirical confirmation remain separate. Registers are connected but
not interchangeable; their mapping requires a scoped witness.
Presence in the active registry does not make a proposal author-accepted.
Read card types, statuses and provenance. Embedded original corpora retain their
historical wording; active structured card/axiom views take precedence.
The original workbook and embedded historical corpora are not claims that this
release was produced by a new workbook round-trip.

## Active changes

Author clarification: A1/A3 are possible external logical supplements; C_n and A5/A5a are assistant-proposed formalization, not author-adopted axioms. Four card types/statuses/provenance and four relations corrected; unrelated cards and mathematical predicates retained.

U6/U7 logical forms retain AC-2026-09-21. U7's mathematical reading is stored in
`A_07` / `U7_MATH_LOCAL_FORBID`; logical grouping in `U7_LOGIC_GROUPING`.
AC-2026-10-03 adds the exact finite triple/five/seven window families, with author
and editorial statuses retained. Intersections do not automatically define carriers.

Cards: 169. Triples: 378. Sheets: 54.

## Counts by card type

| type | count |
| --- | --- |
| alignment_note | 1 |
| anti_mode | 1 |
| author_decision | 1 |
| axiom | 8 |
| boundary | 1 |
| boundary_candidate | 1 |
| candidate_bundle | 1 |
| candidate_overlay | 1 |
| classification_candidate | 1 |
| complex_analog | 7 |
| connectivity_ground | 20 |
| constraint | 2 |
| definition | 4 |
| export_instruction | 1 |
| failure_condition | 5 |
| formalization_proposal | 2 |
| guardrail | 1 |
| hypothesis_candidate | 1 |
| invariant_candidate | 1 |
| level | 19 |
| level_candidate | 1 |
| level_variant_candidate | 1 |
| logical_supplement | 2 |
| mathematical_expression | 1 |
| minimal_expression | 19 |
| notation_rule | 1 |
| operator | 20 |
| operator_candidate | 1 |
| overlay | 3 |
| private_expression | 19 |
| statistical_analog | 6 |
| status_promotion | 5 |
| tensor_analog | 3 |
| test | 3 |
| topology_candidate | 1 |
| window_family | 3 |
| window_family_statement | 1 |

## Counts by status

| status | count |
| --- | --- |
| FTS_candidate | 4 |
| FTS_candidate_guarded | 2 |
| active_instruction | 1 |
| assistant_formalization_not_adopted | 2 |
| author_canonical_amendment | 5 |
| candidate | 12 |
| candidate_U12_overlay | 3 |
| candidate_boundary | 1 |
| candidate_bridge | 2 |
| candidate_bundle | 1 |
| candidate_core | 2 |
| candidate_logical_supplement | 2 |
| candidate_overlay | 9 |
| candidate_requires_empirical_test | 1 |
| candidate_requires_formalization | 2 |
| candidate_requires_formalization + canonical_alignment | 3 |
| candidate_with_operational_gate | 11 |
| canon/base | 11 |
| canon/base_plus_user_refinement | 1 |
| canonical | 29 |
| canonical_alignment | 1 |
| canonical_node_underformalized_semantics | 3 |
| canonical_note | 1 |
| canonical_strict | 24 |
| derived_constraint | 4 |
| editorial_check | 1 |
| formal_math_fact / candidate_requires_formalization + canonical_alignment | 1 |
| formal_math_fact / derived_constraint | 2 |
| operational_diagnostic_layer | 1 |
| projected_underformalized | 6 |
| reserved_overlay | 2 |
| reserved_underformalized | 6 |
| reserved_underformalized_overlay | 2 |
| speculative | 6 |
| statistical_overlay_candidate | 3 |
| strong_overlay_for_U6 | 1 |
| strong_statistical_analog | 1 |

## Added and restored records

| id | status | text |
| --- | --- | --- |
| U7_MATH_LOCAL_FORBID | derived_constraint | Математический аналог У7 обязан включать local_forbid: y=-x*x и y!=x*x; без правой части У7 схлопывается в У6. |
| A_07 | candidate_with_operational_gate | А-регистр для У(7): y=-x*x; y!=x*x. Математический аналог сохраняется отдельно от логической формы M_07; мост между регистрами открыт. |
| U7_LOGIC_GROUPING | derived_constraint | Активная каноническая форма У7 обязана сохранять всю вложенную группировку; обычная булева тень не заменяет эту форму. |
| AC_20261003_AUTHOR_DECISION | author_canonical_amendment | Окна строятся группами нечётной длины: минимальные тройки, пятёрки, семёрки. |
| AC_20261003_WINDOW_FAMILIES | author_canonical_amendment | Построение окон идёт группами нечётной длины; записаны тройки, пятёрки и семёрки, начинающиеся с уровня −1; соседние окна семейства пересекаются по одному уровню. |
| AC_20261003_WINDOW_FIVES_ALIGNMENT | editorial_check | Семейство пятёрок совпадает с окнами (-1,0,1,2,3)(3,4,5,6,7)(7,8,9,10,11)(11,12,13,14,15) из поля window карточек уровней активного канона v13 (узлы-носители 3, 7, 11, 15); открытое окно (15,16,17,…) карточки U_15 в авторское перечисление не входит. |
| AC_20261003_WINDOWS_TRIPLES | author_canonical_amendment | Точный конечный авторский перечень: (-1,0,1)(1,2,3)(3,4,5)(5,6,7)(7,8,9)(9,10,11). Пересечение окон само по себе не задаёт узел-носитель или обратную связь; продолжение за перечень не утверждается. |
| AC_20261003_WINDOWS_FIVES | author_canonical_amendment | Точный конечный авторский перечень: (-1,0,1,2,3)(3,4,5,6,7)(7,8,9,10,11)(11,12,13,14,15). Пересечение окон само по себе не задаёт узел-носитель или обратную связь; продолжение за перечень не утверждается. |
| AC_20261003_WINDOWS_SEVENS | author_canonical_amendment | Точный конечный авторский перечень: (-1,0,1,2,3,4,5)(5,6,7,8,9,10,11)(11,12,13,14,15,16,17). Пересечение окон само по себе не задаёт узел-носитель или обратную связь; продолжение за перечень не утверждается. |

### `40_Reader_View`

| section | reader_text |
| --- | --- |
| Что такое ФТС | ФТС — лестница различимости, где уровень получает смысл через собственное структурированное отсутствие, предел тотализации, ошибку/остаток и возможность Lift. |
| Как читать Excel | Сначала 00/01/02, затем 03 уровни, 07 основания, 17 карточки, 18 граф. Для полного текста — 19. Для проверки — 33. |
| Что не является ФТС | Не абсолютная метатеория мира; не доказанные 8+; не смешение ¬A/0_A/−A; не список красивых слов без ролей и условий поражения. |
| М-регистр vs Ч-регистр | М-регистр — минимальная проекция выражения. Ч-регистр — частное/операциональное чтение: Dist₃, Select, Agg, K и т.д. |
| Почему Excel может заменить файлы | Потому что теперь хранит атомы (17), граф (18), полный текст (19), метрику (20), proof sketch (23), M′ audit (24), manifest (32), validation (33), exports (34–37). |
| Что всё ещё требует проверки | Канонизация C(E), machine-check proof, κ на provenance-aware inference, real missing-data benchmark, формулы 7–11, верхние уровни 12–17. |
| Что изменено в v11 | У7 теперь читается не как “ответ вставлен в ожидание”, а как сам акт закрытия ожидания ожиданием: Answer(W)=Close(W,W). κ/T7 — диагностический слой для агентных реализаций, не сущность уровня. |
| Где χ² | Критерий χ² относится к статистике У6, но полезен как диагностический мост: он проверяет расхождение наблюдаемого O_i и ожидаемого E_i, не превращая p-value в знание. |
| Что изменено в v12 | Добавлена χ-лестница: χ берётся как нормированный остаток ожидания, а χ*χ=χ² фиксирует сильный аналог У6. Верхние χ-формы являются overlay/gate, не доказанной заменой У7–У11. |
| Что изменено в v13 | Добавлен комплексный overlay: вещественный квадрат прячет знак, комплексный Q(z)=\|z\|² прячет фазу; У8+ получает вопрос о ветви/branch/sheet, но phase не равен −A. |
| Комплексные vs тензоры | Комплексные числа — скаляры с фазой/ветвью; тензоры — многоиндексные структуры отношений и преобразований. Первые полезнее для 7–9, вторые для 10–12+. |

### `03_Уровни_У`

| Уровни У(-1..17): М-регистр, Ч-регистр и математический регистр |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Главный лист: уровни не равны основаниям. Здесь исправлены 7+ anti-mode и сохранены верхние направления как underformalized/speculative. |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |
| У | Пятёричное окно | Носитель/узел | Название уровня | −A / anti-mode | Статус | М-регистр: знак/логика | М-регистр: место/матем | Ч-регистр/операциональное чтение | Что разводится | Что теряется при тотальности | Основания | Комментарий |
| -1 | (-1,0,1,2,3) | pre-carrier | Шум / неизвестное | — | canonical_strict | a≈□[0_знака?] | y≈□ | Seg(W)=∅ / открытая сцена | знак, место, связь; 0_знака и 0_места ещё слиты | Если тотализировать: различий нет → невозможна ошибка/норма | О1–О4, О6–О8 | Стартовая сцена должна хранить пустой знак/пустое место, не только голую □ |
| 0 | (-1,0,1,2,3) | pre-carrier | Ошибка / 0_ошибки | 0_ошибки как норма/отсутствие ошибки | canonical_strict | a≠a | y≠y | Eq₀(a,a)=false / нарушение удержания | разводится сбой удержания от неопределённости | Ошибка/норма тотальны → сигнал не выделяется | О1–О4, О7, О13–О14 |  |
| 1 | (-1,0,1,2,3) | pre-carrier | Сигнал / 0_сигнала | 0_сигнала как пауза/молчание/значимое отсутствие | canonical_strict | a=a | y=y | сигнал / аксиома / стабилизация | самотождество отделяется от ошибки | Абсолютный сигнал → нет кода/прерываний | О1–О4, О8 | Не привязывать только к сигналу: аксиомы тоже частный случай a=a |
| 2 | (-1,0,1,2,3) | terminal pre-carrier | Код / 0_кода | 0_кода как ключ/метаданные/контекст чтения | canonical_strict | a=b | y=x | a=₂b / кодовое соответствие | соответствие отделяется от тождества | Абсолютный код → информация не извлекается | О1–О4, О8 |  |
| 3 | (3,4,5,6,7) | node-3: distinguishable objects | Информация / 0_информации | 0_информации как не-событие/контекст | canonical_strict | I=(a≠b; a-b) / Δ(a,b) | y=-1*x | Dist₃(A,B;0_A^C) | ≠, НЕ_A и 0_A начинают разводиться; a≠b → a-b | Абсолютная информация → вероятность не нужна | О1–О4, О8, О13–О18 | Dist₃ — частное строгое чтение, не замена минимума |
| 4 | (3,4,5,6,7) | node-3 interval | Вероятность / закономерная случайность | 0_вероятности как нераспределённая/нереализованная ветвь | canonical_strict | (a=b) ∧ (a≠b) | y=\|x\| | B=(a=₂b)∧(a≠₃b) | удержание взаимоисключающих положений | Абсолютная вероятность → выбор/случайность исчезают | О1–О4, О8, О13–О18 | B typed — частная форма; минимум: a=b and a≠b |
| 5 | (3,4,5,6,7) | node-3 interval | Выбор / случайность | 0_выбора как невыбранное/зависимость | canonical_strict | (a=b) ∨ (a≠b) | y=-1*\|x\| | Select(B) | из поля выделяется ветвь; девариация | Абсолютный выбор/хаос → статистика не формируется | О1–О4, О8, О13–О19 | Select(B) — операциональное чтение минимума OR |
| 6 | (3,4,5,6,7) | threshold-to-7 | Статистика / случайная закономерность | 0_статистики как out-of-sample/hidden variables | canonical_strict | ((a=b) ∧ (a≠b)) ∧ ((a=b) ∨ (a≠b)) | y=x*x | Agg_i(V_i) | повтор/умножение/агрегация выборов | Абсолютная статистика → знание редуцируется к корреляции | О1–О4, О8, О13–О20 | Agg_i — частное статистическое чтение |
| 7 | (3,4,5,6,7) | node-7: update rules and frames | Знание / Познание / Предсказание / Забывание(отказ от ожидания) | −A: забывание как Close(W,Refuse(W)); Sever — частный разрыв связи/переноса | candidate_with_operational_gate | (((a=b) ∧ (a≠b)) ∧ ((a=b) ∨ (a≠b))) ∨ (((a=b) ∧ (a≠b)) ∨ ((a=b) ∨ (a≠b))) | y=-1*x*x; y!=x*x | K_core=⟨W,0_W,Ans⟩; Answer(W)=Close(W,W); agentic gate: K=⟨S,0_S,κ⟩ | ответ не внешний объект: ответ = закрытие ожидания ожиданием; У7!=У6 | Абсолютное знание/предсказание → окно закрывается без удержания 0_W; У8-вопрос невозможен | О1–О5, О8, О13–О20 | v11: ядро У7 = самоподдерживающийся цикл ожидания; κ/T7 — диагностическая обвязка, не сущность |
| 8 | (7,8,9,10,11) | node-7 interval | Предположение / вера(отказ от вопросной формы) | −A: вера как превращение A? в A без честного закрытия окна ожидания | candidate_with_operational_gate | candidate: Hyp(W)=W[A?] / Link(0_K,M) / TBD | y=\|x\|^(1/2) | Hyp(W)=W[A?]; вопросная форма возможного ответа; не слабое предсказание | вопросность/открытое ожидание отделяется от ответа/закрытого ожидания | Тотальное предположение → вопрос незаконно закрывается как ответ/вера | О5, О8, О15–О20 | v11 boundary: Предположение = A?, не A с меньшей уверенностью. Нужны trace/defeat/test. |
| 9 | (7,8,9,10,11) | node-7 interval | Понимание / упрощение, оскорбление, отказ от сложности | −A: отказ от сложности; оскорбление/упрощение как ложное понимание | FTS_candidate | candidate: Analogy_κ(...) / TBD | y=x*x*x | Analogy_κ / causal-counterfactual reading | кубический избыток: x*x*x=x*(x*x), один дополнительный множитель над квадратом | Абсолютное понимание → сравнение/оценка невозможны | О5, О8, О15–О20 | Повышено v9: math ядро formal_math_fact; ФТС-слой FTS_candidate. Не выдавать за полное понимание без object-language. |
| 10 | (7,8,9,10,11) | threshold-to-11 | Сравнение, оценка / догматизм, отказ от сравнения | −A: догматизм как отказ от сравнения/метрики | reserved_underformalized | candidate: Compare_κ(...) / TBD | y=cos(x) | Compare_κ(options,criteria) | критерий/метрика отделяются от объяснения; cos имеет формальную нулевую решётку | Тотальная оценка → Я как участник контура не осознаётся | О5, О8, О15–О20 | Статус уровня не повышен; math факт о нулях cos(x) добавлен в математический регистр. |
| 11 | (7,8,9,10,11) | node-11: self-description coherence | Осознание Я / отказ от ответственности | −A: отказ от ответственности, разрыв решения и последствий | reserved_underformalized | candidate: Fix(E,Agent,Consequences;...) | y=e^x; window constant: e^pi (candidate) | self-reference / agent-in-loop | внутренний рост e^x не имеет нулевого сечения; e^pi остаётся оконной константой-кандидатом | Тотальное Я → нормативные/межсубъектные контуры закрываются | О5, О8, О15–О20 | e^x как math факт; e^pi не повышать выше candidate; complex Euler-formula = analogy_only без оператора i. |
| 12 | (11,12,13,14,15) | node-11 interval | Конфликт / Союз | anti-mode: нет в артефактах; требуется авторская фиксация | candidate_requires_formalization + canonical_alignment | TBD | x*x+(y-2)*(y-2)=4 | closed relation / circle boundary; center=(0,2), r=2, 0_F=(0,0) | closed relation / circle boundary; У12 получает сильное canonical_alignment, но ещё требует anti-mode/test | TBD | О8, О17? candidate | Повышено v9: У12 как окружность = formal_math_fact; ФТС-смысл = candidate_requires_formalization + canonical_alignment. |
| 13 | (11,12,13,14,15) | node-11 interval | Мир-Мы / Космос-острова | anti-mode: нет в артефактах; текущая гипотеза автора | projected_underformalized | TBD | TBD | TBD | коллективный/мировой носитель | TBD | О8, О17? candidate |  |
| 14 | (11,12,13,14,15) | threshold-to-15 | Воображение / Вычисления-Логика | anti-mode: нет в артефактах; текущая гипотеза автора | projected_underformalized | TBD | TBD | TBD | модельное пространство / вычисление | TBD | О8, О17? candidate |  |
| 15 | (15,16,17,...) | node-15: higher-order metacoherence | Красота | anti-mode: отказ от формы симметрии? current_user_hypothesis | canonical_node_underformalized_semantics | TBD | TBD | TBD | статическая/точечная симметрия? требует формализации | TBD | О17? candidate | Направление сохранено, но не формализовано |
| 16 | (15,16,17,...) | node-15 interval | Музыка | anti-mode: отказ от динамической точки симметрии? current_user_hypothesis | speculative | TBD | TBD | TBD | динамическая точка симметрии — текущая гипотеза | TBD | О17? candidate | Оставлено как направление |
| 17 | (15,16,17,...) | node-15 interval | Искусство | anti-mode: отказ от композиции симметрий? current_user_hypothesis | speculative | TBD | TBD | TBD | композиция форм симметрии? текущая гипотеза | TBD | О17? candidate | Требует отдельного модуля |

### `06_Мат_аналогии`

| Математические аналогии минимальных выражений: объёмы места |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Формулы записаны как аналогии, не как доказанные функции. Они отражают математический регистр места/объёма. |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
| У | Формула места/математики | Чтение | Связь с М-регистром | Статус | Что формализовать | local_forbid / правая часть | zero_boundary | mirror_window | window/cycle reading |
| -1 | y≈□ | место + связь + знак под ПУСТОЕ МЕСТО | аналог a≈□ в регистре места | current_user_hypothesis | точный тип пустого места 0_места | — | — | pre-window | пустое место до устойчивого зеркального запрета |
| 0 | y≠y | самонесовпадение величины | a≠a | working_minimum | режим ошибки величины | right_pair: y=-y | y=0 | self-contradiction window | ошибка как самонесовпадение/нулевая граница |
| 1 | y=y | самотождество величины | a=a | working_minimum | аксиоматическая стабилизация | y!=-y | y=0 | {y,-y} | самотождество задано через не-антиформу |
| 2 | y=x | соответствие величин | a=b | working_minimum | кодовая замена | y!=-x | x=0 | {x,-x} | кодовое соответствие не равно обратной ориентации |
| 3 | y=-1*x | ориентированная разность/инверсия | a≠b → a-b | working_minimum | не путать '-' с 7+ −A | y!=x | x=0 | {x,-x} | ориентированная разность не равна прямому соответствию |
| 4 | y=\|x\| | модуль из x: поле без знака направления | (a=b) ∧ (a≠b) | working_analogy | почему модуль является носителем вероятностного поля | y!=-abs(x) | x=0 | {abs(x),-abs(x)} | модуль не равен отрицательному модулю |
| 5 | y=-1*\|x\| | модуль из x, умноженный на -1 | (a=b) ∨ (a≠b) | working_analogy | связь с выбором/девариацией | y!=abs(x) | x=0 | {abs(x),-abs(x)} | отрицательный модуль не равен модулю |
| 6 | y=x*x | квадратичная агрегация/умножение | ((a=b) ∧ (a≠b)) ∧ ((a=b) ∨ (a≠b)) | working_analogy | что именно агрегируется | y!=-x*x | x=0 | {x*x,-x*x} | статистический агрегат не равен анти-ориентированному квадрату |
| 7 | y=-1*x*x | квадрат с противоположной ориентацией; локально y=-x*x и y!=x*x; оконное чтение: Answer(W)=Close(W,W) | (((a=b) ∧ (a≠b)) ∧ ((a=b) ∨ (a≠b))) ∨ (((a=b) ∧ (a≠b)) ∨ ((a=b) ∨ (a≠b))) | candidate_minimum / window_core_patch_v11 | развести '-' как orientation; y!=x*x как local_forbid; Answer(W) как самозакрытие окна | y!=x*x | x=0 | {x*x,-x*x} | У7: Answer(W)=Close(W,W); не статистический x*x |
| 8 | y=\|x\|^(1/2) | корень из модуля x; вопросная форма возможного ответа | Hyp(W)=W[A?] / Link(0_K,M) / TBD | formal_math_fact / candidate_with_operational_gate | Math: partial inverse; FTS: предположение=A?, не ответ A и не слабое предсказание | Hyp(W)=A? != Answer(W)=A | A? unresolved | {A,A?} | У8: вопросная форма возможного ответа, не слабое У7 |
| 9 | y=x*x*x | кубическая развёртка | понимание/сложность | formal_math_fact / FTS_candidate | Math: уникальный минимальный multiplicative surplus над x*x; FTS: нужен язык понимания/избытка. |  |  |  |  |
| 10 | y=cos(x) | периодическое сравнение/метрика | сравнение/оценка | formal_math_fact / canonical_alignment | Math: cos(x)=0 при x=pi/2+pi*k; FTS: сравнение/оценка ещё underformalized. |  |  |  |  |
| 11 | y=e^x | самоусиливающийся контур/экспонента | осознание Я | formal_math_fact / FTS_candidate | Math: e^x>0 и нет вещественных нулей; FTS: нужен внешний gate; e^pi не повышать. |  |  |  |  |
| 12 | x*x+(y-2)*(y-2)=4 | окружность/сдвинутая симметрия | конфликт/союз | formal_math_fact / candidate_requires_formalization + canonical_alignment | Math: окружность центр (0,2), r=2, касание (0,0); FTS: closed boundary candidate. |  |  |  |  |
| 13 | TBD | нет текущей формулы | мир/мы | projected_underformalized | задать |  |  |  |  |
| 14 | TBD | нет текущей формулы | воображение/вычисление | projected_underformalized | задать |  |  |  |  |
| 15 | TBD | нет текущей формулы | красота | speculative | статическая точка симметрии? |  |  |  |  |
| 16 | TBD | нет текущей формулы | музыка | speculative | динамическая точка симметрии |  |  |  |  |
| 17 | TBD | нет текущей формулы | искусство | speculative | композиция симметрий |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
| generic | export notation rule | В Markdown/TSV писать abs(x), -abs(x), sqrt(abs(x)) вместо \|x\| | сохраняет таблицы от поломки pipe-символом | canonical_note | ADD_NOTATION_ABS |  |  |  |  |
| generic | Window(F_n)={F_n,-F_n} | локальное зеркало уровня | y=F эквивалентно y!=-F только внутри окна и при F!=0 | candidate | ADD_MIRROR_WINDOW |  |  |  |  |
| generic | ZeroBoundary(F_n)={x:F_n(x)=0} | нулевая boundary | F=-F iff F=0; место схлопывания формы и анти-формы | derived_constraint | Повышено v9: работает как теорема локального двухветвевого окна при F!=0. |  |  |  |  |
| generic | EvenSpace/OddSpace | чётный/нечётный топологические слои | запреты локальны; соседний уровень не уничтожается глобально | formal_math_fact / derived_constraint | Повышено v9: F=-F iff F=0 как math fact; ZeroBoundary как следствие окна. |  |  |  |  |
| 11 | e^x / e^pi | динамический рост и оконная константа | e^pi не заменяет e^x; это sealed growth constant окна 11–15 | canonical_alignment | Повышено v9: не заменяет узлы 3/7/11/15, но согласуется с локально-проекционным чтением. |  |  |  |  |
| 12 | x*x+(y-2)*(y-2)=4 | окружность, closed relation, pi-boundary | центр (0,2), r=2, 0_F=(0,0), длина=4*pi, площадь=4*pi | FTS_candidate | Не повышать: e^pi требует отдельной sealing-меры; complex Euler требует оператора i. |  |  |  |  |

### `U7_Window_Cycles`

| U7_Window_Cycles — v11: ответ как самозамыкание окна ожидания |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |
| item_id | scope | formula | meaning | status | source/IDs | guardrail | defeat condition | where used |
| U7_CORE_V11 | У7 / node-7 | Answer(W)=Close(W,W) | Ответ/Знание/Познание/Предсказание есть не внешний объект, а сам акт закрытия ожидания ожиданием. | core_patch_candidate | Хабр: вопросы/ответы как циклы; Статистика→Знание; [U_07] | не читать ответ как предмет, вставленный в окно извне | если Answer(W) трактуется как внешний A без W-замыкания | 03_Уровни_У; 21_Переходы; 17_Карточки |
| U7_FORGET_V11 | anti-mode У7 | Forgetting(W)=Close(W,Refuse(W)) | Забывание = закрытие ожидания отказом от ожидания; не просто потеря памяти. | core_patch_candidate | [U_07]; [OP_Refuse]; [OP_Sever] | Refuse(W) не равен честному 0_W/незнанию | если отказ ожидать выдаётся за ответ или объективность | 04_7plus_minusA; 12_Отсутствия; 25_Операторы |
| U7_MATH_LOCAL_FORBID | математический регистр | U7_author | У7 обязан читаться с правой частью: не быть У6-квадратом в том же зеркальном окне. | derived_constraint | [M_07]; [SP_WINDOW]; [SP_ZERO] | local_forbid действует локально, не как глобальное уничтожение связи с У6 | если y=-x*x читается без y!=x*x и схлопывается в «ещё одну статистику» | 06_Мат_аналогии |
| U7_AGENTIC_GATE_LAYER | операционная обвязка | κ/T7 = diagnostic gate | κ, provenance, Refuse/Sever, T7A/T7B/T7C нужны для агентных/обновляемых воплощений, но не являются ядром У7. | operational_diagnostic_layer | [OP_kappa]; [T7A]; [T7B]; [T7C] | не назначать проверочную обвязку сущностью уровня | если без gate агентная система выдаёт confidence за знание | U7_Kappa_Gate; 29_7plus_tests |
| U7_U8_BOUNDARY | граница У7→У8 | Answer(W)=W[W] != Hyp(W)=W[A?] | Предсказание/ответ закрывает окно; предположение открывает окно вопросом. Предположение не слабое предсказание. | boundary_candidate | [U_07]; [U_08]; user_dialog_v11 | не переводить «не уверен» в ответ; это вопросная форма | если A? выдаётся за A без закрытия окна | 03_Уровни_У; 27_LevelMap_v2 |
| REVERSI_6_7_V11 | переход 6→7 | Stats -> expectation model; 0_Stats -> 0_W; Close(W,W) | Реверси Статистики даёт модели ожидания и пустое окно; знание возникает как самозамыкание окна. | canonical_reading_patch | 11_Reversi_О3; Хабр 4.6 | статистика остаётся средой, но не ядром ответа | если агрегат объявлен ответом без оконной комбинаторики | 11_Reversi_О3; 21_Переходы |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| Комбинаторика окна ожидания |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| state_id | notation | level reading | what closes what | not equal to | status | failure / anti-mode | source | comment |
| W_EMPTY | W[ ] | Незнание / пустое контекстное окно | ничего не закрыто | не ответ | base for U7 | Tot может стереть пустоту как «нет данных» | Хабр 4.6 | 0_Статистики как пустое контекстное окно |
| W_ANSWER | W[W] / Close(W,W) | Ответ / Знание / Познание / Предсказание | ожидание закрывается ожиданием | не статистический агрегат x*x | U7_core | ложный ответ как confidence | user_dialog_v11 | самоподдерживающийся цикл, продуктивная тавтология |
| W_FORGET | W[Refuse(W)] | Забывание | ожидание закрывается отказом от ожидания | не честное незнание | U7_antimode | Refuse/Sever маскируют провал | user_dialog_v11 + OP_Refuse | закрытие необходимости ожидать |
| W_HYP | W[A?] | Предположение / вопрос | окно открыто кандидатной формой | не ответ A | U8_boundary | вера превращает A? в A без закрытия | user_dialog_v11 | предположение задаёт вопрос, а не даёт ответ |
| W_FAITH | W[A!] без W-замыкания | Вера / псевдоответ | форма объявлена ответом без честного закрытия | не У7 | anti-mode U8 | ложное повышение −8→+9 / вера как понимание | categorical_errors | вера как незаконное превращение вопроса в ответ |
| AGG6 | Agg_i(V_i) / x*x | Статистика | агрегирует повторённые выборы | не W[W] | U6 | абсолютная статистика редуцирует знание к корреляции | [U_06] | среда для У7 |
| W_AGG | W(Agg) | переход 6→7 | статистическая регулярность становится окном ожидания | не само знание без Close(W,W) | transition | Promote if label only | T_06_07 | мост между y=x*x и y=-x*x |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| Guardrails v11 |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| guardrail_id | rule |  |  |  |  |  |  |  |
| G1 | У7 не повышать до canonical_strict; статус candidate_with_operational_gate. |  |  |  |  |  |  |  |
| G2 | κ/T7 не удалять: они остаются agentic diagnostic layer. |  |  |  |  |  |  |  |
| G3 | y=-x*x само по себе не доказывает знание; нужна оконная комбинаторика и, для агентных систем, diagnostic gate. |  |  |  |  |  |  |  |
| G4 | Предположение = A?, не слабое предсказание. |  |  |  |  |  |  |  |
| G5 | Забывание = Close(W,Refuse(W)), не простая потеря памяти. |  |  |  |  |  |  |  |
| G6 | y!=x*x действует локально в mirror_window {x*x,-x*x}. |  |  |  |  |  |  |  |
| G7 | Не смешивать математический минус '-', 0_A, −A и Refuse/Sever. |  |  |  |  |  |  |  |

### `ChiSquare_FTS`

| ChiSquare_FTS — χ² как статистический тест окна ожидания |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |
| item | FTS placement | formula / object | meaning | helps how | not equal to | guardrail | where used |
| Критерий χ² | У6: Статистика | χ² = Σ((O_i-E_i)^2/E_i) | мера расхождения наблюдаемых частот O_i и ожидаемых E_i | делает видимой несовпавшую структуру ожидания | не знание само по себе | p-value/χ² не превращать в Answer(W) без оконного закрытия | 06_Мат_аналогии; U7_Window_Cycles |
| Ожидаемые частоты E_i | мост У6→У7 | E_i as expectation model | ожидание, заданное моделью/нулевой гипотезой | даёт конкретный W для проверки | не ответ, если W не закрывается | ожидаемое ≠ истинное | U7 core examples |
| Наблюдаемые частоты O_i | У6: данные реализации | O_i | статистический агрегат случаев | показывает, где реализация не совпала с ожиданием | не гипотеза | не выдавать выборку за весь мир | AGG6 |
| Нулевая гипотеза H0 | У8-подобная вопросная рамка / У6 protocol | H0: распределение соответствует ожиданию | кандидатная форма, которую тест проверяет | отделяет вопрос от ответа | не знание и не предсказание | H0 не становится У7 от одного p-value | U7_U8_BOUNDARY |
| Решение reject / not reject | протокольное решение, не сущность У7 | p<α / p>=α | правило действия в заданном α, df, protocol | защищает от словесной каши «кажется/знаю» | не доказательство истинности | not reject H0 != H0 true | M′ audit |
| FTS-вывод | diagnostic bridge | χ² tests W vs observed counts | χ² относится к статистике, но помогает построить bridge к У7, если использовать его как тест закрытия/сбоя окна ожидания | показывает разницу: статистика считает; знание/предсказание закрывает W; предположение задаёт A? | не замена Close(W,W) | оставить как OP_ChiSquareDiagnostic | 25_Операторы |

### `Chi_Stat_Ladder`

| Chi_Stat_Ladder | χ как статистический носитель дополнительной лестницы |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Статус | statistical_overlay_candidate; локальный носитель ожидания/остатка: x:=χ, где χ — нормированный остаток ожидания; χ*χ=χ² даёт У6; это не замена основной лестницы. |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| def_id | symbol | formula | definition | level_role | source_ids | guardrail | core question |  |
| CHI_CONTEXT | W / H0 / protocol | W=(bins, E_i, df, α, protocol) | Окно ожидания статистического теста: модель, по которой ожидаются значения E_i. | sets expectation window | U7_WINDOW_CORE; OP_ChiSquareDiagnostic | W не равно истине; это заданное окно ожидания. | Какое ожидание вообще проверяется? |  |
| CHI_OBSERVED | O_i | observed count/state in cell i | Наблюдаемая реализация в ячейке/категории/состоянии i. | data side | U_06 | O_i не равны всему миру; это выборка/реализация. | Что пришло в окно наблюдения? |  |
| CHI_EXPECTED | E_i | expected count/state under W | Ожидаемое значение под моделью ожидания W/H0. | expectation side | U7_WINDOW_CORE; ChiSquare_FTS | E_i не ответ, пока W не закрыто. | Что окно ожидало получить? |  |
| CHI_RESIDUAL | χ_i | χ_i=(O_i-E_i)/sqrt(E_i) | Нормированный остаток ожидания: signed expectation residue, если знак сохраняется на уровне ячейки. | carrier x:=χ | OP_ChiCarrier | Не подставлять x:=χ²; иначе У6 станет χ⁴. | Как именно наблюдаемое расходится с ожидаемым? |  |
| CHI_VECTOR | χ | χ=(χ_i)_i | Вектор/семейство нормированных остатков; хранит компонентность, а не только сумму. | statistical carrier | CHI_RESIDUAL | Скаляр √χ² теряет знак/компоненты; применять только как coarse readout. | Какая структура остатка сохранена? |  |
| CHI_SQUARE | χ*χ | χ*χ=Σ_i χ_i²=χ² | Квадратичная агрегация остатков: стандартный χ²-статистический readout. | U6 statistic | OP_ChiSquareDiagnostic; U_06 | χ² не знание, не ответ и не предположение. | Насколько W не совпадает с O в агрегате? |  |
| CHI_FIT | χ²≈0 / small | low χ² under protocol | След согласованности O и E внутри W, но не доказательство истинности W. | diagnostic trace | ChiSquare_FTS | not reject H0 != H0 true; p-value не закрывает У7 сам. | Закрылось ли окно или только не обнаружен сбой? |  |
| CHI_MISFIT | χ² large | large χ² under protocol | След незакрытия окна ожидания статистикой; запускает вопрос/пересборку W. | U6→U8 trigger | U7_U8_ANSWER_QUESTION_BOUNDARY | Большой χ² не объяснение; он только показывает место сбоя. | Какой вопрос надо задать к W? |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| У | level name | flat formula | χ-stat formula | χ-overlay definition | local_forbid / not-this | core question | status | source IDs |
| -1 | Шум / неизвестное | y≈□ | χ undefined / no stable W | Нет стабильного окна ожидания и ячеек; остаток ещё нечем считать. | not χ=0; отсутствие χ не равно хорошему fit | Есть ли вообще различимое окно ожидания? | lower_projection | U_m1 |
| 0 | Ошибка / 0_ошибки | y≠y | χ not comparable / norm τχ absent | Ошибка появляется как несоответствие норме отклонения; без τχ нет ошибки χ. | error != absence of error; χ outside norm != global falsehood | Какая норма/τ отделяет допустимое отклонение от ошибки? | lower_projection | U_00 |
| 1 | Сигнал | y=y | χ-event registered | Остаток ожидания стал событием: отклонение зарегистрировано детектором/протоколом. | χ-event != silence/no event | Регистрируется ли отклонение как событие? | lower_projection | U_01 |
| 2 | Код | y=x | y=χ_i | Остаток закодирован как токен/ячейка/индекс i с протоколом парсинга. | χ_i != -χ_i within sign-sensitive protocol | Как остаток кодируется: bins, df, parser, units? | lower_projection | U_02 |
| 3 | Информация | y=-x | y=-χ | Знак/направление остатка сообщает, где избыток/недостаток относительно E_i. | -χ != χ except zero boundary | В какую сторону ожидание не совпало с наблюдением? | working_overlay | U_03 |
| 4 | Вероятность | y=\|x\| | y=\|χ\| | Модуль остатка даёт поле величин отклонения без направления. | \|χ\| != -\|χ\|; magnitude != answer | Какое поле допустимых отклонений задано моделью W? | working_overlay | U_04 |
| 5 | Выбор / случайность | y=-\|x\| | y=-\|χ\| | Выбор/отбор ячеек, хвостов или траекторий по величине отклонения. | -\|χ\| != \|χ\|; selection != explanation | Какие ячейки/траектории считаются значимыми для действия? | working_overlay | U_05 |
| 6 | Статистика | y=x*x | y=χ*χ=Σχ_i²=χ² | Статистика как квадратичная агрегация остатков ожидания. | χ² != -χ²; statistic != answer | Насколько наблюдаемое расходится с ожидаемым в агрегате? | strong_statistical_analog | U_06; OP_ChiSquareDiagnostic |
| 7 | Предсказание / Познание / Знание | U7_author | y=-χ*χ; y!=χ*χ | Окно ожидания развернуто от статистического readout к самозакрытию: Answer(W)=Close(W,W). | Answer(W) != χ²; p-value != knowledge | Закрылось ли W ожиданием, а не только статистическим fit/misfit? | candidate_bridge | U_07; U7_WINDOW_CORE; U7_MATH_LOCAL_FORBID |
| 8 | Предположение / Интуиция | y=sqrt(abs(x)) | y=sqrt(abs(χ)) / backtrace(χ²) | Если W не закрыто, χ-остаток открывает вопрос A?: какую правку E/W проверить? | A? != A; hypothesis != weak prediction | Какая гипотеза E' могла бы закрыть или объяснить остаток χ? | candidate_with_operational_gate | U_08; U7_U8_ANSWER_QUESTION_BOUNDARY |
| 9 | Понимание | y=x*x*x | y=χ*χ*χ only with causal/counterfactual decomposition | Кубический мотив допустим только как вход в объяснение структуры χ-остатков: почему именно эти χ_i и что изменит интервенция. | χ³ != understanding without causal model | Почему остаток имеет такую структуру и что изменится контрфактуально? | FTS_candidate / guarded | U_09; SP_U9 |
| 10 | Оценка | Compare(criteria) | Compare(E,E',loss,df,Δχ²,ΔR*) | Сравнение моделей ожидания и цен ошибок; статистический выигрыш не равен ценностной оценке без критерия. | comparison != refusal of comparison | Какая модель ожидания лучше по заданному loss/критерию? | reserved_underformalized_overlay | U_10; OP_dDelta |
| 11 | Осознание Я / ответственность | Own(update criterion) | Own(W,E,loss,α,protocol) | Субъект/система включает свой выбор окна, критерия и протокола в причинную петлю. | ownership != external excuse; α choice != neutral god-button | Кто отвечает за выбор W/E/loss/α и последствия ошибки? | reserved_underformalized_overlay | U_11; A0b |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| guardrail_id | rule | why it matters | defeat condition |  |  |  |  |  |
| G_CHI_01 | x:=χ, not x:=χ². | Так У6 остаётся χ*χ=χ², а не превращается в χ⁴. | Если x=χ², лестница становится степенями уже готовой статистики. |  |  |  |  |  |
| G_CHI_02 | χ² belongs to У6. | χ² считает агрегированное расхождение O и E; оно не является У7-ответом. | Если p-value объявлен знанием или предсказанием. |  |  |  |  |  |
| G_CHI_03 | У7 reads χ² through window closure. | Answer(W)=Close(W,W), а не χ²≈0. | Если низкий χ² трактуется как истинность W без правой части/границ. |  |  |  |  |  |
| G_CHI_04 | У8 is the question A?, not weak answer A. | Большой χ² запускает вопрос о гипотезе E', но не даёт понимание сам. | Если «не уверен» записан как ответ, а не как вопрос. |  |  |  |  |  |
| G_CHI_05 | У9 requires causal/counterfactual decomposition. | χ³ без модели причинности — просто степень, а не понимание. | Если большой/кубический остаток объявлен объяснением. |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| transition | χ-trigger | FTS question | not enough |  |  |  |  |  |
| У5→У6 | selected observations become χ_i corpus | Можно ли агрегировать остатки в устойчивую статистику? | единичный χ_i |  |  |  |  |  |
| У6→У7 | χ² fit/misfit relative to W | Закрывает ли W само себя ответом? | малый χ² / p-value |  |  |  |  |  |
| У7→У8 | W not closed or closure contested | Какой A? или E' надо проверить? | догадка без вопросной формы |  |  |  |  |  |
| У8→У9 | hypothesis changes χ-pattern | Почему эта гипотеза меняет остатки именно так? | подгонка E' без causal/counterfactual trace |  |  |  |  |  |
| У9→У10 | multiple explanations reduce χ² differently | По какому loss/критерию сравнивать объяснения? | лучший fit без цены ошибки |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| Toy check: χ as expectation residue (formula-driven) |  |  |  |  |  |  |  |  |
| bin | O_i observed | E_i expected | χ_i=(O_i-E_i)/sqrt(E_i) | χ_i² contribution |  |  |  |  |
| A | 28 | 25 | 0.6 | 0.36 |  |  |  |  |
| B | 20 | 25 | -1 | 1 |  |  |  |  |
| C | 30 | 25 | 1 | 1 |  |  |  |  |
| D | 22 | 25 | -0.6 | 0.36 |  |  |  |  |
| TOTAL χ² |  |  | Σχ_i² | 2.7199999999999998 |  |  |  |  |
| Reading | χ² here is only an У6 diagnostic. It may support questions for У7/У8, but it does not close W as Answer(W) by itself. |  |  |  |  |  |  |  |

### `Complex_Branch_Overlay`

| Complex_Branch_Overlay | комплексные числа как фазово-ветвевой overlay для 7+ |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Статус | candidate_overlay; не заменяет основную лестницу. Усиливает axis_A: quadratic-only readout vs full object/phase/branch access; B-axis/self-reference остаётся отдельным требованием 7+. |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| def_id | symbol | formula | definition | level_role | source_ids | guardrail | core question | status |
| CPLX_CARRIER | z / χ ∈ ℂ^n | z=r·e^{iθ}; χ_i∈ℂ | Комплексный носитель хранит модуль и фазу/ветвь; для χ-лестницы может быть вектором комплексных остатков. | carrier for branch/phase overlay | access_axes_layer; CHI_CARRIER | Комплексность не равна самореференции и не доказывает −A. | Какая фазовая/ветвевая структура была скрыта квадратом? | candidate_overlay |
| CPLX_READOUT_Q | Q(z), Q(χ) | Q(z)=\|z\|²; Q(χ)=Σ_i conjugate(χ_i)χ_i=Σ_i\|χ_i\|² | Неотрицательный квадратичный readout: то, что видит У6 как агрегат/энергия/модуль-квадрат. | U6 readout | U_06; OP_ChiCarrier | Q(χ) не равен χ; фаза/ветвь теряются. | Что именно сохраняет статистика, а что теряет? | working_definition |
| CPLX_PHASE | phase(z) | θ = arg(z) | Фаза, невидимая в \|z\|²; расширяет вещественный знак +/- до U(1)-ветви. | 7+ optional A-axis motif | TA1; access_axes_layer | phase != −A; phase alone does not give metacontrol. | Может ли система различить состояния с одинаковым Q, но разной фазой? | candidate |
| CPLX_BRANCH | branch/sheet | sqrt(z)=±√r·e^{iθ/2} | Корень комплексного носителя требует выбора ветви/листа; обход вокруг нуля может менять ветвь. | U8 branch question | M_08; CHI_LADDER_U8 | branch access != Lift by itself. | Какая ветвь могла породить наблюдаемое? | candidate |
| CPLX_INTERFERENCE | Σχ_i² vs Σ\|χ_i\|² | Σχ_i² may be complex; Σ\|χ_i\|² real | Если суммировать квадраты без сопряжения, появляются фазовые компенсации/интерференция; это не обычный χ²-тест. | interference motif | OP_ComplexNormReadout | Не смешивать complex interference overlay с χ² diagnostic. | Какие различия теряются при переходе к норме? | candidate |
| CPLX_U12_OUTSIDE | outside real boundary | if Q(χ)>R² then y=y0±i√(Q(χ)-R²) | Вне вещественной границы объект не исчезает, а уходит в комплексную/мнимую ветвь напряжения. | U12 conflict/union branch | U12_CHI_PI_BOUNDARY | Комплексное решение не равно вещественной совместимости. | Что делает контур с остатком, который не помещается в реальную границу? | candidate_U12_overlay |
|  |  |  |  |  |  |  |  |  |
| level | flat/χ formula | complex formula | complex reading | not-this / local_forbid | question | status | source_ids | notes |
| У6 | χ*χ=χ² | Q(χ)=Σ\|χ_i\|² | Статистика видит норму/энергию/модуль-квадрат, но не фазу. | Q(χ)!=χ; low Q!=knowledge | Какой агрегат наблюдаем без доступа к фазе? | strong_overlay_for_U6 | U_06; CHI_LADDER_U6 | комплексный аналог χ² |
| У7 | -χ*χ; !=χ*χ | -Q(χ); !=Q(χ) + phase/branch access as optional A-axis | Ответ/знание не сводится к квадратичному readout; может требовать различения скрытой ветви. | phase!=-A; branch access!=self-reference | Что закрывает окно, если статистический readout одинаков? | candidate_bridge | U_07; U7_WINDOW_CORE; access_axes_layer | B-axis/T7 remains separate |
| У8 | sqrt(abs(χ)); W[A?] | sqrt(χ)=±√r·e^{iθ/2}; A_k? | Предположение становится вопросом о ветви/фазе/листе, а не слабым ответом. | A_k? != A; hypothesis != prediction | Какая ветвь могла бы закрыть W? | candidate | U_08; CHI_LADDER_U8 | ветвь как вопрос |
| У9 | χ*χ*χ guarded | phase/branch causal-counterfactual model | Понимание объясняет, почему эта фаза/ветвь/branch cut существенна и что изменится при другом пути. | χ³ alone != understanding | Почему именно эта ветвь, а не другая? | FTS_candidate_guarded | U_09; SP_U9 | не метафора, нужен causal model |
| У10 | Compare(E,E',loss,df,Δχ²,ΔR*) | Compare(branch, phase, protocol, loss) | Оценка задаёт критерий выбора ветви, branch cut, протокола и цены ошибки. | branch preference != objective evaluation without criterion | По какому критерию выбирать ветвь/фазу? | reserved_overlay | U_10; CHI_LADDER_U10 | loss/protocol explicit |
| У11 | Own(W,E,loss,α,protocol) | observer/protocol fixes branch | Осознание/ответственность включает протокол, который фиксирует фазу/ветвь и делает её воспроизводимой. | observer != arbitrary subjectivism | Кто/какой протокол фиксирует ветвь? | reserved_overlay | U_11; CHI_LADDER_U11 | protocol ownership |
| У12 | χ²(π_k)+(y-2)^2=4 | Q(χ(π_k))+(y-2)^2=4; complex outside branch | Замкнутая граница получает вещественную и комплексную ветвь; Conflict/Union не схлопываются без branch. | Union!=χ²=0; Conflict!=big χ² alone | Когда остаток становится реальной совместимостью, а когда мнимым напряжением? | candidate_U12_overlay | U_12; SP_U12; U12_CHI_PI_BOUNDARY | requires branch=sign/phase/sheet |
|  |  |  |  |  |  |  |  |  |
| guardrail_id | rule | why it matters | failure if violated | level_range | source_ids | status |  |  |
| CPLX_G1 | complex phase != −A | Фаза относится к A-axis; −A требует B-axis/metacontrol. | i/phase объявляют знанием или отказом. | 7+ | access_axes_layer; A8 | blocking |  |  |
| CPLX_G2 | Q(χ)=Σ\|χ_i\|² belongs to U6 readout | Не дать статистике захватить У7–У12. | χ² / p-value выдают за ответ, понимание или конфликт. | 6→12 | U_06; CHI_LADDER_U6 | blocking |  |  |
| CPLX_G3 | branch access != Lift by itself | Ветвь должна дать definability gain, иначе это motif. | Появилась новая буква, но не появился новый вопрос/тест. | 7→9 | A6; Lift_family | blocking |  |  |
| CPLX_G4 | sqrt(z) requires branch tracking | Без ветви У8 схлопывается в плоский sqrt(abs(x)). | A? превращается в A или в чистую арифметику. | 8+ | M_08; U7_U8_ANSWER_QUESTION_BOUNDARY | blocking |  |  |
| CPLX_G5 | complex outside != real compatibility | Комплексное решение при Q>R² не означает вещественную совместимость. | Outside объявлен Union без смены контура. | 12 | U12_CHI_PI_BOUNDARY | blocking |  |  |
|  |  |  |  |  |  |  |  |  |
| toy_id | Q_chi | R2 | regime | y_plus_real | y_minus_real | y_plus_complex | y_minus_complex | FTS_reading |
| EX_inside | 1 | 4 | inside real boundary | 3.732050807568877 | 0.2679491924311228 |  |  | остаток помещается в реальную границу; две реальные ветви |
| EX_tangent | 4 | 4 | tangent | 2 | 2 |  |  | точка касания: ветви схлопнуты |
| EX_outside | 5 | 4 | outside complex branch |  |  | 2 + i*1.000 | 2 - i*1.000 | реальных y нет; возникает мнимая ветвь напряжения |

### `Tensor_Context_Overlay`

| Tensor_Context_Overlay | тензоры как контекстно-индексный overlay для 10+ |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Статус | candidate_overlay; не “ещё более сложные числа”, а многоиндексные структуры отношений/преобразований между осями, контекстами, критериями и наблюдателями. |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| def_id | symbol | formula | definition | level_role | source_ids | guardrail | core question | status |
| TENSOR_SCALAR | scalar | rank-0 tensor | Скаляр — частный случай тензора ранга 0; комплексное число может быть комплексным скаляром. | baseline | general math object | scalar != full tensor context | Какая минимальная размерность отношения? | working_definition |
| TENSOR_VECTOR | v_i | rank-1 tensor/vector | Вектор хранит компоненты по одной оси/индексу. | multi-component state | CHI_VECTOR | vector != tensor law automatically | Какая ось компонентности сохранена? | working_definition |
| TENSOR_MATRIX | M_ij | rank-2 tensor/matrix if transformation law defined | Матрица становится тензором, если задан закон преобразования между базисами/контекстами. | relation between two axes | Lambda_link; Sever | array != tensor without transformation rule | Какие два индекса реально связаны? | working_definition |
| TENSOR_CONTEXT | χ_{iα} | residue i in context/protocol α | Остатки становятся контекстно размеченными: ячейка i + протокол/наблюдатель/контур α. | 10+ context carrier | CHI_CARRIER; U_10; U_11 | more indices != more meaning | Как переносится остаток между контекстами? | candidate |
| TENSOR_TRANSFER | T_{ijαβ} | transfer/coupling between residues and contexts | Многоиндексный перенос: связь между i,j и контекстами α,β; родственен Λ, но богаче. | Sever/Λ extension | Sever; Lambda_link | tensor != Sever by itself | Какая связь разрезается или сохраняется? | candidate |
| TENSOR_CRITERION | L_{αβ} / G_{ij} | metric/loss tensor | Критерий/метрика может быть не одним числом, а формой сравнения по осям/контекстам. | U10 evaluation | U_10; OP_dDelta | metric tensor != evaluation without protocol | Какая цена ошибки по разным контурам? | candidate |
|  |  |  |  |  |  |  |  |  |
| level | tensor role | example | reading | local_forbid | question | status | source_ids | notes |
| У8–У9 | обычно не главный носитель | χ_i, phase_i | Можно использовать компоненты/фазы, но тензорность ещё не обязательна. | more indices != understanding | Какие зависимости действительно причинны? | supporting_only | U_08; U_09 | primary complex/branch overlay |
| У10 | критерии/метрики | G_{ij}, L_{αβ} | Оценка сравнивает модели/ветви по нескольким осям и loss-структурам. | score alone != evaluation | По какой метрике сравниваем? | candidate_overlay | U_10 | use with Compare(...) |
| У11 | протокол/наблюдатель | χ_{iα}, protocol α | Субъект/система включает собственный протокол как индекс и источник преобразования. | observer index != arbitrary truth | Кто задаёт базис/протокол? | candidate_overlay | U_11 | protocol ownership |
| У12 | контур совместимости | B(χ,c) with context tensor | Conflict/Union может зависеть от связи нескольких контуров, не от одного χ². | tensor boundary != proof of U12 | Как связаны разные контуры конфликта/союза? | candidate_U12_overlay | U_12; U12_CHI_PI_BOUNDARY | requires operator/test |
|  |  |  |  |  |  |  |  |  |
| comparison | complex numbers | tensors | FTS difference | do_not_confuse |  |  |  |  |
| what they are | scalar field ℂ: z=a+bi = r e^{iθ} | multi-index transformation object T_{ij...} | Комплексность хранит фазу/ветвь; тензорность хранит структуру отношений между осями. | complex != tensor |  |  |  |  |
| best for | 7–9 branch/phase under square/root | 10–12 criteria, protocols, transfer, contours | Комплексное число отвечает: какая ветвь? Тензор отвечает: между какими контекстами и по какому закону? | phase != context law |  |  |  |  |
| can combine | complex scalar/vector/tensor possible | components may be real or complex | Комплексный тензор хранит и фазу, и индексы отношений. | do not promote automatically |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
| guardrail_id | rule | why it matters | failure if violated | level_range | source_ids | status |  |  |
| TNS_G1 | array != tensor unless transformation law is specified | Иначе любой диапазон Excel становится “тензором”, а это уже уголовное дело против смысла. | таблица названа тензором без инварианта/преобразования. | 10+ | Tensor_Context_Overlay | blocking |  |  |
| TNS_G2 | more indices != higher level | Индексы не создают Lift без нового вопроса/оператора. | сложность записи выдана за понимание. | 8+ | A6; Promote | blocking |  |  |
| TNS_G3 | tensor context overlay != replacement of Λ/Sever | Тензор может расширять перенос, но не заменяет failure grammar. | Sever растворён в общей матрице. | 7+ | Lambda_link; Sever | blocking |  |  |
| TNS_G4 | complexity and tensorness are orthogonal | Комплексные числа и тензоры можно сочетать, но это разные свойства. | фаза и контекстный индекс перепутаны. | 7+ | Complex_Branch_Overlay | blocking |  |  |

### `28_CarrierNodes`

| node | carrier | interval | what unfolds | formal_status | guardrail | internal_ref |
| --- | --- | --- | --- | --- | --- | --- |
| pre -1..2 | primary distinguishability | pre-carrier genesis | noise→error→signal→code | canonical_strict | не считать carrier-node | CANON_EN |
| 3 | distinguishable objects | 3-6 | objects, distributions, selection, statistical aggregation | canonical_strict | 0_A object-level, not −A | CANON_EN |
| 7 | update rules and frames | 7-10 | self-reference, hypothesis, causal/counterfactual, comparison | candidate/reserved | −A internally definable only with metacontrol | CANON_EN |
| 11 | self-description coherence | 11-14 | agent in loop, responsibility, intersubjective contours | underformalized | не формализовать преждевременно | CANON_EN |
| 15 | higher-order metacoherence | 15-18? | higher-order symmetry/metacoherence | underformalized/speculative | красота/музыка/искусство не canonical_strict | CANON_EN/user_current |
