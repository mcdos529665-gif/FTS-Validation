# FTS v13 LLM export — START HERE

This package is an LLM-friendly export of `ФТС_табличный_канон_v13_complex_branch_overlay.xlsx`.

## Hard reading rules

- Treat the Excel v13 workbook as the immediate source snapshot for this export.
- Primary structured sources in this package: `fts_cards.jsonl`, `fts_triples.tsv`, `FTS.yaml`, `fts_v13_workbook_sheets.json`.
- Do not conflate `¬A`, `0_A`, and `−A`.
- Do not promote a candidate/overlay to canon unless status fields, local_forbid rules, Lift/defeat conditions, and graph/card evidence support it.
- For any conclusion, cite card IDs, graph triples, or sheet rows. If an entity is not found, say `нет в артефактах`.

## Current v13 snapshot

- Cards: `161`
- Triples: `238`
- Sheets: `54`
- Source SHA256: `32a6ed34febaf62a57f6aac986e8caf9716b09b7b8f14bc131e76f81d15acbd6`

## Reader view

### Что такое ФТС
ФТС — лестница различимости, где уровень получает смысл через собственное структурированное отсутствие, предел тотализации, ошибку/остаток и возможность Lift.

### Как читать Excel
Сначала 00/01/02, затем 03 уровни, 07 основания, 17 карточки, 18 граф. Для полного текста — 19. Для проверки — 33.

### Что не является ФТС
Не абсолютная метатеория мира; не доказанные 8+; не смешение ¬A/0_A/−A; не список красивых слов без ролей и условий поражения.

### М-регистр vs Ч-регистр
М-регистр — минимальная проекция выражения. Ч-регистр — частное/операциональное чтение: Dist₃, Select, Agg, K и т.д.

### Почему Excel может заменить файлы
Потому что теперь хранит атомы (17), граф (18), полный текст (19), метрику (20), proof sketch (23), M′ audit (24), manifest (32), validation (33), exports (34–37).

### Что всё ещё требует проверки
Канонизация C(E), machine-check proof, κ на provenance-aware inference, real missing-data benchmark, формулы 7–11, верхние уровни 12–17.

### Что изменено в v11
У7 теперь читается не как “ответ вставлен в ожидание”, а как сам акт закрытия ожидания ожиданием: Answer(W)=Close(W,W). κ/T7 — диагностический слой для агентных реализаций, не сущность уровня.

### Где χ²
Критерий χ² относится к статистике У6, но полезен как диагностический мост: он проверяет расхождение наблюдаемого O_i и ожидаемого E_i, не превращая p-value в знание.

### Что изменено в v12
Добавлена χ-лестница: χ берётся как нормированный остаток ожидания, а χ*χ=χ² фиксирует сильный аналог У6. Верхние χ-формы являются overlay/gate, не доказанной заменой У7–У11.

### Что изменено в v13
Добавлен комплексный overlay: вещественный квадрат прячет знак, комплексный Q(z)=|z|² прячет фазу; У8+ получает вопрос о ветви/branch/sheet, но phase не равен −A.

### Комплексные vs тензоры
Комплексные числа — скаляры с фазой/ветвью; тензоры — многоиндексные структуры отношений и преобразований. Первые полезнее для 7–9, вторые для 10–12+.

## Counts by card type

- `connectivity_ground`: 20
- `operator`: 20
- `level`: 19
- `minimal_expression`: 19
- `private_expression`: 19
- `axiom`: 12
- `complex_analog`: 7
- `statistical_analog`: 6
- `failure_condition`: 5
- `status_promotion`: 5
- `definition`: 4
- `test`: 3
- `overlay`: 3
- `tensor_analog`: 3
- `candidate_bundle`: 1
- `notation_rule`: 1
- `operator_candidate`: 1
- `boundary_candidate`: 1
- `topology_candidate`: 1
- `invariant_candidate`: 1
- `hypothesis_candidate`: 1
- `classification_candidate`: 1
- `level_variant_candidate`: 1
- `level_candidate`: 1
- `export_instruction`: 1
- `anti_mode`: 1
- `boundary`: 1
- `guardrail`: 1
- `constraint`: 1
- `candidate_overlay`: 1

## Counts by status

- `canonical`: 31
- `canonical_strict`: 24
- `candidate`: 12
- `canon/base`: 11
- `candidate_with_operational_gate`: 10
- `candidate_overlay`: 9
- `reserved_underformalized`: 6
- `projected_underformalized`: 6
- `speculative`: 6
- `FTS_candidate`: 4
- `candidate_requires_formalization + canonical_alignment`: 3
- `canonical_node_underformalized_semantics`: 3
- `derived_constraint`: 3
- `statistical_overlay_candidate`: 3
- `candidate_U12_overlay`: 3
- `formal_math_fact / derived_constraint`: 2
- `candidate_requires_formalization`: 2
- `candidate_core`: 2
- `candidate_bridge`: 2
- `FTS_candidate_guarded`: 2
- `reserved_underformalized_overlay`: 2
- `reserved_overlay`: 2
- `formal_math_fact / candidate_requires_formalization + canonical_alignment`: 1
- `canon/base_plus_user_refinement`: 1
- `candidate_requires_empirical_test`: 1
- `canonical_conceptual`: 1
- `canonical_extension`: 1
- `candidate_bundle`: 1
- `canonical_note`: 1
- `canonical_alignment`: 1
- `active_instruction`: 1
- `candidate_boundary`: 1
- `operational_diagnostic_layer`: 1
- `strong_statistical_analog`: 1
- `strong_overlay_for_U6`: 1

## File map

- `fts_cards.jsonl` — atomic entity cards. Best first source for IDs, status, text, dependencies, tags.
- `fts_cards.json` — same cards as JSON array.
- `fts_triples.tsv` — compact graph triples: subject/predicate/object.
- `fts_graph_full.tsv` — full graph sheet, including evidence/internal refs/status/comment/graph_id.
- `fts_cards_table.tsv` — full card table from sheet `17_Карточки`.
- `FTS.yaml` — workbook YAML export.
- `fts_v13_workbook_sheets.json` — full workbook sheet dump as structured JSON.
- `FTS_v13_LLM_FULL_DUMP.md` — all workbook sheets as Markdown tables.
- `LLM_IMPORT_PROMPT.txt` — compact prompt for another LLM.

## v13 overlay guardrails

- `Q(z)=|z|²` and `Q(χ)=Σ|χ_i|²` belong to U6 statistical/quadratic readout.
- U7+ may ask about phase/branch/sheet, but `phase != −A`.
- Branch access alone is not Lift.
- Complex numbers are scalars with phase/branch; tensors are multi-index relation/transform objects.
- `array != tensor` unless a transformation law is specified.
