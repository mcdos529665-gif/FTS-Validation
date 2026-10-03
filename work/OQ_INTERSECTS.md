# OQ-INTERSECTS — точки пересечения открытых вопросов (машинный слой)

Источник: work/OPEN_QUESTIONS.md · открытых 49 · генератор `tools/oq_pool.py --intersects`.
Хаб = признак, общий для ≥2 пунктов (ранг = вес признака × охват). Мост = ребро между пунктами из РАЗНЫХ курируемых пулов (OQ_TRIAGE).
Гардрейлы: χ-склейка запрещена; **similarity ≠ зависимость** — типизацию «гейт/закрывает» ставит курируемый слой событий (шаг 3 плана), не эта машина. (Спецобработка C-60 снята 2026-07-09: после фолда C-60…C-62 — структурные проверки сьюта.)
Курируемый слой (события E1…E10, канонные предки, ТОП-5) — `work/OQ_TRIAGE.md` §«Точки пересечения». Этот файл машинный — регенерируем.

## Хабы (признак → пункты) — ранг = вес признака × охват

- **У8** (LVL, вес 2×охват 8=16) — `oq-formulas-7-11-done` `oq-u8-u10-optests` `oq-tot-groups-8-11` `oq-strict-band-7-export` `oq-d2-half-overlay` `oq-synthesis-c-assembly` `oq-d2-sign-retrieval-remainder` `oq-vieta-cubic-s3`
- **У12** (LVL, вес 2×охват 7=14) — `oq-upper-12-17-done` `oq-u12-radius-r` `oq-u12-antimode-gate` `oq-u12-antimode-authorfix` `oq-synthesis-c-assembly` `oq-padic-carrier-channel` `oq-audit-semantic-repromotion`
- **У14** (LVL, вес 2×охват 6=12) — `oq-upper-12-17-done` `oq-arity-window-13-14` `oq-passport-u14-u15` `oq-u14-worlds-agg-op` `oq-pentad-role-cycle` `oq-padic-carrier-channel`
- **У6** (LVL, вес 2×охват 6=12) — `oq-pi-projection-above-u7` `oq-mprime-audit` `oq-strict-band-7-export` `oq-sphere-u6-carrier` `oq-zero-classes-chi-e` `oq-levy-world`
- **У7** (LVL, вес 2×охват 6=12) — `oq-formulas-7-11-done` `oq-pi-projection-above-u7` `oq-mprime-audit` `oq-strict-band-7-export` `oq-sphere-u6-carrier` `oq-audit-semantic-repromotion`
- **У9** (LVL, вес 2×охват 6=12) — `oq-formulas-7-11-done` `oq-phase-causal-u9` `oq-u8-u10-optests` `oq-tot-groups-8-11` `oq-d2-sign-retrieval-remainder` `oq-edgeworth-u9`
- **У13** (LVL, вес 2×охват 5=10) — `oq-upper-12-17-done` `oq-arity-window-13-14` `oq-u13-boundary-union-op` `oq-pentad-role-cycle` `oq-padic-carrier-channel`
- **O_14** (ID, вес 3×охват 3=9) — `oq-d2-half-overlay` `oq-fourier-questiongain` `oq-divorce-cases-genre`
- **У10** (LVL, вес 2×охват 4=8) — `oq-formulas-7-11-done` `oq-u8-u10-optests` `oq-tot-groups-8-11` `oq-graph-dep-sync`
- **У15** (LVL, вес 2×охват 4=8) — `oq-upper-12-17-done` `oq-passport-u14-u15` `oq-unit-circle-z15` `oq-pentad-role-cycle`
- **граница** (KW, вес 1×охват 7=7) — `oq-passport-u14-u15` `oq-third-boundary` `oq-const-statistics-code` `oq-unit-circle-z15` `oq-u13-boundary-union-op` `oq-strict-band-7-export` `oq-padic-carrier-channel`
- **ADD_TOPO_INVARIANTS** (ID, вес 3×охват 2=6) — `oq-sphere-u6-carrier` `oq-zero-classes-chi-e`
- **C-19** (C, вес 3×охват 2=6) — `oq-formulas-7-11-done` `oq-sphere-u6-carrier`
- **C-34** (C, вес 3×охват 2=6) — `oq-pi-projection-above-u7` `oq-redteam-dependent-guards`
- **C-49** (C, вес 3×охват 2=6) — `oq-third-boundary` `oq-padic-carrier-channel`
- **C-60** (C, вес 3×охват 2=6) — `oq-strict-band-7-export` `oq-vieta-cubic-s3`
- **O_20** (ID, вес 3×охват 2=6) — `oq-o20-missing-benchmark` `oq-o3-twolists`
- **SHADOW** (ID, вес 3×охват 2=6) — `oq-d11-branch-bit-test` `oq-d10-phase-test`
- **U_07** (ID, вес 3×охват 2=6) — `oq-sphere-u6-carrier` `oq-audit-semantic-repromotion`
- **VIETA** (ID, вес 3×охват 2=6) — `oq-d11-branch-bit-test` `oq-vieta-cubic-s3`
- **Д11** (OD, вес 2×охват 3=6) — `oq-d11-branch-bit-test` `oq-d10-phase-test` `oq-mprime-audit`
- **О14** (OD, вес 2×охват 3=6) — `oq-d2-half-overlay` `oq-fourier-questiongain` `oq-divorce-cases-genre`
- **О2** (OD, вес 2×охват 3=6) — `oq-redteam-dependent-guards` `oq-const-statistics-code` `oq-mprime-audit`
- **У2** (LVL, вес 2×охват 3=6) — `oq-pi-projection-above-u7` `oq-strict-band-7-export` `oq-divorce-cases-genre`

## Мосты между пулами (порог 2; пары из РАЗНЫХ пулов)

- `oq-pi-projection-above-u7` (П3) ↔ `oq-mprime-audit` (П9) — вес 8: У4,5,6,7
- `oq-arity-window-13-14` (П2) ↔ `oq-padic-carrier-channel` (П5) — вес 5: У13,14; миры
- `oq-d2-half-overlay` (П4) ↔ `oq-divorce-cases-genre` (П10) — вес 5: O_14; О14
- `oq-fourier-questiongain` (П4) ↔ `oq-divorce-cases-genre` (П10) — вес 5: O_14; О14
- `oq-mprime-audit` (П9) ↔ `oq-sphere-u6-carrier` (П7) — вес 5: У6,7; Agg/агрегация
- `oq-third-boundary` (П6) ↔ `oq-padic-carrier-channel` (П5) — вес 5: C-49; граница,единичная
- `oq-d11-branch-bit-test` (П5) ↔ `oq-vieta-cubic-s3` (Парк) — вес 4: VIETA; зеркало
- `oq-pentad-role-cycle` (П2) ↔ `oq-padic-carrier-channel` (П5) — вес 4: У13,14
- `oq-pi-projection-above-u7` (П3) ↔ `oq-sphere-u6-carrier` (П7) — вес 4: У6,7
- `oq-pi-projection-above-u7` (П3) ↔ `oq-divorce-cases-genre` (П10) — вес 4: У2,3
- `oq-u14-worlds-agg-op` (П2) ↔ `oq-padic-carrier-channel` (П5) — вес 4: У14; Agg/агрегация,миры
- `oq-const-statistics-code` (П6) ↔ `oq-mprime-audit` (П9) — вес 3: О2; отсутствие
- `oq-d11-branch-bit-test` (П5) ↔ `oq-mprime-audit` (П9) — вес 3: Д11; ratio/отношения
- `oq-mprime-audit` (П9) ↔ `oq-levy-world` (Парк) — вес 3: У6; тотализация
- `oq-passport-u14-u15` (П2) ↔ `oq-padic-carrier-channel` (П5) — вес 3: У14; граница
- `oq-pi-projection-above-u7` (П3) ↔ `oq-redteam-dependent-guards` (П12) — вес 3: C-34
- `oq-u13-boundary-union-op` (П2) ↔ `oq-padic-carrier-channel` (П5) — вес 3: У13; граница
- `oq-const-statistics-code` (П6) ↔ `oq-padic-carrier-channel` (П5) — вес 2: граница,единичная
- `oq-d10-phase-test` (П5) ↔ `oq-mprime-audit` (П9) — вес 2: Д11
- `oq-d2-half-overlay` (П4) ↔ `oq-d2-sign-retrieval-remainder` (П3/П8) — вес 2: У8
- `oq-d2-half-overlay` (П4) ↔ `oq-vieta-cubic-s3` (Парк) — вес 2: У8
- `oq-d2-sign-retrieval-remainder` (П3/П8) ↔ `oq-edgeworth-u9` (Парк) — вес 2: У9
- `oq-d2-sign-retrieval-remainder` (П3/П8) ↔ `oq-vieta-cubic-s3` (Парк) — вес 2: У8
- `oq-mprime-audit` (П9) ↔ `oq-zero-classes-chi-e` (П7) — вес 2: У6
- `oq-phase-causal-u9` (П5) ↔ `oq-u8-u10-optests` (П3) — вес 2: У9
- `oq-phase-causal-u9` (П5) ↔ `oq-tot-groups-8-11` (П3) — вес 2: У9
- `oq-phase-causal-u9` (П5) ↔ `oq-d2-sign-retrieval-remainder` (П3/П8) — вес 2: У9
- `oq-phase-causal-u9` (П5) ↔ `oq-edgeworth-u9` (Парк) — вес 2: У9
- `oq-pi-projection-above-u7` (П3) ↔ `oq-zero-classes-chi-e` (П7) — вес 2: У6
- `oq-pi-projection-above-u7` (П3) ↔ `oq-levy-world` (Парк) — вес 2: У6
- `oq-redteam-dependent-guards` (П12) ↔ `oq-const-statistics-code` (П6) — вес 2: О2
- `oq-redteam-dependent-guards` (П12) ↔ `oq-mprime-audit` (П9) — вес 2: О2
- `oq-sphere-u6-carrier` (П7) ↔ `oq-levy-world` (Парк) — вес 2: У6
- `oq-synthesis-c-assembly` (П4) ↔ `oq-d2-sign-retrieval-remainder` (П3/П8) — вес 2: У8
- `oq-synthesis-c-assembly` (П4) ↔ `oq-padic-carrier-channel` (П5) — вес 2: У12
- `oq-synthesis-c-assembly` (П4) ↔ `oq-vieta-cubic-s3` (Парк) — вес 2: У8
- `oq-tot-groups-8-11` (П3) ↔ `oq-d2-half-overlay` (П4) — вес 2: У8
- `oq-tot-groups-8-11` (П3) ↔ `oq-synthesis-c-assembly` (П4) — вес 2: У8
- `oq-tot-groups-8-11` (П3) ↔ `oq-edgeworth-u9` (Парк) — вес 2: У9
- `oq-tot-groups-8-11` (П3) ↔ `oq-vieta-cubic-s3` (Парк) — вес 2: У8
- `oq-u12-antimode-authorfix` (П11) ↔ `oq-synthesis-c-assembly` (П4) — вес 2: У12
- `oq-u12-antimode-authorfix` (П11) ↔ `oq-padic-carrier-channel` (П5) — вес 2: У12
- `oq-u12-antimode-gate` (П11) ↔ `oq-synthesis-c-assembly` (П4) — вес 2: У12
- `oq-u12-antimode-gate` (П11) ↔ `oq-padic-carrier-channel` (П5) — вес 2: У12
- `oq-u12-radius-r` (П11) ↔ `oq-synthesis-c-assembly` (П4) — вес 2: У12
- `oq-u12-radius-r` (П11) ↔ `oq-padic-carrier-channel` (П5) — вес 2: У12
- `oq-u8-u10-optests` (П3) ↔ `oq-d2-half-overlay` (П4) — вес 2: У8
- `oq-u8-u10-optests` (П3) ↔ `oq-synthesis-c-assembly` (П4) — вес 2: У8
- `oq-u8-u10-optests` (П3) ↔ `oq-edgeworth-u9` (Парк) — вес 2: У9
- `oq-u8-u10-optests` (П3) ↔ `oq-vieta-cubic-s3` (Парк) — вес 2: У8
- `oq-unit-circle-z15` (П2/П6) ↔ `oq-d10-phase-test` (П5) — вес 2: Д10
- `oq-unit-circle-z15` (П2/П6) ↔ `oq-padic-carrier-channel` (П5) — вес 2: граница,единичная
- `oq-zero-classes-chi-e` (П7) ↔ `oq-levy-world` (Парк) — вес 2: У6

