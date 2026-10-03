# notation.md — краткий словарь ФТС

Значения обозначений для старта работы. По конкретному вопросу открывать
указанный источник. Места для новых записей: [карта документов](DOCUMENT_MAP.md).

## Регистры и уровни

| Запись | Значение |
|---|---|
| `M_*` / М-регистр | Минимальная проекция выражения уровня |
| `CH_*` / Ч-регистр | Частное/операциональное чтение: Dist₃, Select, Agg, Close |
| А-регистр | Математическая запись/аналог; карта и области — [здесь](v14_rebuild/FTS_v14_register_map.md) |
| `У(n)`, `U_n` | Уровень; `U_m1` — У(−1) |
| `window` | Прежнее поле окна уровня: пятёрка соседних индексов; новые семейства троек/пятёрок/семёрок адресуются отдельно |
| carrier / pre-carrier | Носитель / предноситель различимости |

Регистры одного уровня связаны, но их типы и основания различаются.
М-регистр и Ч-регистр читать раздельно. Точные действующие формулы и статусы
получать по ID из `source/fts_cards.jsonl` через `tools/query.py`.
Формы У6/У7: [принятая поправка](author_canon/2026-09-21/AMENDMENT.md).

## Обозначения

| Запись | Значение и адрес подробностей |
|---|---|
| `¬A` | Логическое отрицание моды A |
| `0_A` | Структурированное отсутствие / нулевая мода |
| `⊖A` | Антимода, отказ уровня 7+; [разбор трёх отсутствий](v14_rebuild/FTS_v14_paper.md#notation-signs) |
| `−F`, `anti(F)` | Арифметический минус и анти-форма в вещественном чтении; там же §3.2a |
| `Rot_θ F`, `rot(theta,F)` | Фазовый поворот; там же §3.2a |
| `Q` | Модульный канал; конкретную нормировку (модуль/квадрат) читать в определении модели |
| `R`, `ratio(F,G)` | Канал отношений; [каналы и области](v14_rebuild/FTS_v14_register_map.md#readout-channels) |
| `χ` | Нормированный остаток ожидания; [χ- и другие оверлеи](v14_rebuild/FTS_v14_register_map.md#overlays) |

Локальное равенство не-предмета и отсутствия на У0 принято отдельно:
[область уточнения](author_canon/2026-09-19/AMENDMENT.md#u0).

## Статусы

Поле `status` читается из конкретной карточки. Принятый порядок обозначений:
`canonical_strict > canonical > canon/base > derived_constraint >
candidate_* / *_overlay / reserved_* / projected_* / speculative`.
Порядок проверки повышения — [патч-таблица статусов](v14_rebuild/status_patch_v14.md).

## Адреса прежних разделов

<a id="минимум-доступность-и-применение-уточнение-чтения-2026-09-12"></a>
Минимум, `Cap_n` и `Act_n`: [исследование наследования, §5–6](v14_rebuild/recursive_distinction_2026-09-12/REVIEW.md#minimum-capability).

<a id="траектория-противоположности-и-внутренняя-регуляция"></a>
<a id="траектория-противоположности-и-внутренняя-регуляция-авторское-уточнение-2026-09-15"></a>
Траектория и регуляция: [интеграция DN-0001–DN-0016](v14_rebuild/dialogue_semantics_2026-09-15.md#trajectory).

<a id="диалоговые-уточнения-dn-0017dn-0027-рабочий-слой-2026-09-22"></a>
DN-0017–DN-0027: [разбор по каждой записи](v14_rebuild/dialogue_integration_2026-09-22.md#результаты).

<a id="уровневое-равенство-рабочее-авторское-уточнение-2026-09-26"></a>
Виды равенства и отражение: [исследование, §6–8](v14_rebuild/m_register_grammar_2026-09-25/EQUALITY_REVIEW_2026-09-26.md#types-of-equality).

## Candidate research definitions retained from master

- `0_A*(ℓ)=⟨A,ℓ,m,p,w⟩`: candidate typed absence; `m` mechanism, `p` provenance,
  `w` witness. Its event/Tot shadow does not recover the structure.
  [Passport](v14_rebuild/e5_literature_review/TYPED_ABSENCE_BRIDGE.md).
- `L(X,R)=X×R`, `ι(x)=(x,r₀)`, `π(x,r)=x`, `ρ(x,r)=r`: candidate Set reading
  of Lift; a section/point `r₀` is required. `∄q:ρ=q∘π` states the residual gain.
  `Lift_FTS` and an external lifting property remain distinct.
  [Passport and L0–L7 obligations](v14_rebuild/e5_literature_review/LIFT_TYPING_PROJECT.md).

## Active integration (2026-10-03)

U7 mathematical reading: `A_07`, `U7_MATH_LOCAL_FORBID` (`y=-x*x; y!=x*x`).
The logical grouping obligation is `U7_LOGIC_GROUPING`; logical `M_07` and
operational `CH_07` retain their own scopes. The bridge remains open.
Level window families: [author statement and integration](author_canon/2026-10-03/INTEGRATION.md).
