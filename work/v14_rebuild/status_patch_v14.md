# Патч-таблица статусов для канона v14

Предложение изменений к следующему экспорту канона (v13 → v14).
Канон v13 в `source/` не редактируется; патч применяется при сборке новой
выгрузки. Каждая строка опирается на FTS_v14_paper.md и verification_report.md
(35 PASS / 0 FAIL). Повышения оформлены через предусмотренные каноном
SP-карточки [триплеты SP_* → promotes_status_of → *].

## 1. Повышения статуса

| Карточка/сущность | v13 | v14 | Через | Свидетели |
|---|---|---|---|---|
| U_07 (ядро: К=≠С; y=−x²) | candidate_with_operational_gate | canonical | — (гейт κ/T7 остаётся операционным слоем) | C-35, C-05, C-01 |
| U_08 (А?=?(С); y=√\|x\|) | candidate_with_operational_gate | canonical | SP_U8 | C-06, C-07, C-08, C-09 |
| U_09 (П=Δ·С; y=x³) | FTS_candidate | canonical | SP_U9 | C-10, C-11, C-12 |
| U_10 (Δ²Ц=≠Ц; y=cos x) | reserved_underformalized | canonical (формула + характеризация) | новая карточка SP_U10 (создать) | C-13, C-14, C-15, C-16, C-17 |
| U_11 (ΔЯ=Я; y=eˣ) | reserved_underformalized | canonical | новая карточка SP_U11 (создать) | C-18, C-19, C-20, C-21 |
| U_12 (Inv(Я₁,Я₂)=c; окружность) | candidate_requires_formalization + canonical_alignment | canonical | SP_U12 | C-22…C-27; условие поражения U12_CIRCLE снято [C-23] |
| ADD_PARITY_TOPOLOGY (аудит чётности) | addendum | canonical-инвариант | SP_PARITY | C-05 |
| ADD_ZERO_BOUNDARY (F=−F ⟺ F=0) | addendum/derived_constraint | canonical-инвариант | SP_ZERO | C-01, C-02 |
| ADD_MIRROR_WINDOW (зеркальное окно {F,−F}) | addendum | canonical-инвариант | SP_WINDOW | C-02, C-03, C-04 |

## 2. Новые карточки (создать в v14)

| ID (предлож.) | Содержание | Статус |
|---|---|---|
| DICT_D1…D9 | Словарь конвертации Д (§5 статьи): Д1–Д5, Д7, Д8 — canonical; Д6, Д9 — candidate | по правилу |
| MAP_PENTAD | Пентадная рекурсия (шаг 4): окно k+1 = смыслы позиций окна k на новом носителе | canonical (C-32…C-35 + посвидетельная таблица §8.2) |
| MAP_PI_PROJ | Полушаги проекции π(x)=\|x\| для шага 2 (У2..У7) | canonical в диапазоне 2..7; open для 8+ (C-34) |
| RULE_P | Правило предсказания П (П1–П5, §8.4) | canonical как порождающее правило; предсказания им — candidate_prediction |
| NODE_SIGNATURES | Сигнатуры узлов 3/7/11/15 (анти-форма → неподвижная точка → инвариант группы) | candidate (асимметрия узла 11 не снята) |
| U12_ANTIMODE | Анти-мода У12: Поглощение / Разрыв | candidate (нет в артефактах v13 — требуется авторская фиксация) |
| U_13_FORMULA | ∏Bₖ=0; минимально (x²+(y−2)²−4)·(x²+(y+2)²−4)=0 | candidate_prediction (C-28…C-30) |
| U_14_FORMULA | Параметрическое семейство границ F(x,y;θ)=0 | projected_candidate |
| U_15_FORMULA | Орбита симметрии z=e^{iθ} | projected_candidate (C-31) |

## 3. Отброшено (discarded_v14)

| Утверждение | Причина |
|---|---|
| «y=−x² описывает мнимые числа» | нарушение гардрейла phase ≠ −A (провал К3) |
| «3-мерный крест / поле мерностей» для У4 | нет свидетеля (провал К1), нарушает минимальность |
| χ³ как формула ядра У9 | канон сам требует causal decomposition; остаётся оверлеем |
| Альтернативные М-регистры У8 (Link(0_K,M) и TBD-варианты) | сворачиваются к ?(С) по Д4 |
| Чтение У10 «периодическое сравнение» как определение | заменено характеризацией Δ²Ц=≠Ц (C-15) |
| Жёсткие формулы У16–У17 | провал К1 + запрет SP_LIMITS |

## 4. Без изменений

- У−1…У6: canonical_strict.
- χ-лестница и комплексный оверлей: overlay/gate (не канон уровней).
- SP_EPI: does_not_promote_above ADD_U11_EPI — соблюдено.
- SP_LIMITS: does_not_promote_above U_13_to_U_17 — соблюдено (13–15 только
  candidate_prediction / projected_candidate).
- Агентные тесты T7A/T7B/T7C, κ-гейт: операционный слой, не сущность уровня.
