# OQ-INTERSECTS — точки пересечения открытых вопросов (машинный слой)

Источник: work/OPEN_QUESTIONS.md · открытых 40 · генератор `tools/oq_pool.py --intersects`.
Хаб = признак, общий для ≥2 пунктов (ранг = вес признака × охват). Мост = ребро между пунктами из РАЗНЫХ курируемых пулов (OQ_TRIAGE).
Гардрейлы: χ-склейка запрещена; C-60 (политика) вне хабов/рёбер; **similarity ≠ зависимость** — типизацию «гейт/закрывает» ставит курируемый слой событий (шаг 3 плана), не эта машина.
Курируемый слой (события E1…E5, канонные предки, ТОП-5) — `work/OQ_TRIAGE.md` §«Точки пересечения». Этот файл машинный — регенерируем.

## Хабы (признак → пункты) — ранг = вес признака × охват

- **У8** (LVL, вес 2×охват 5=10) — `oq-u8-u10-optests` `oq-tot-groups-8-11` `oq-d2-half-overlay` `oq-synthesis-c-assembly` `oq-d2-sign-retrieval-remainder`
- **У9** (LVL, вес 2×охват 5=10) — `oq-phase-causal-u9` `oq-u8-u10-optests` `oq-tot-groups-8-11` `oq-d2-sign-retrieval-remainder` `oq-edgeworth-u9`
- **O_14** (ID, вес 3×охват 3=9) — `oq-d2-half-overlay` `oq-fourier-questiongain` `oq-divorce-cases-genre`
- **У12** (LVL, вес 2×охват 4=8) — `oq-u12-radius-r` `oq-u12-antimode-gate` `oq-u12-antimode-authorfix` `oq-synthesis-c-assembly`
- **У14** (LVL, вес 2×охват 4=8) — `oq-arity-window-13-14` `oq-passport-u14-u15` `oq-u14-worlds-agg-op` `oq-pentad-role-cycle`
- **У6** (LVL, вес 2×охват 4=8) — `oq-pi-projection-above-u7` `oq-sphere-u6-carrier` `oq-zero-classes-chi-e` `oq-levy-world`
- **ADD_TOPO_INVARIANTS** (ID, вес 3×охват 2=6) — `oq-sphere-u6-carrier` `oq-zero-classes-chi-e`
- **C-34** (C, вес 3×охват 2=6) — `oq-pi-projection-above-u7` `oq-redteam-dependent-guards`
- **O_20** (ID, вес 3×охват 2=6) — `oq-o20-missing-benchmark` `oq-o3-twolists`
- **О14** (OD, вес 2×охват 3=6) — `oq-d2-half-overlay` `oq-fourier-questiongain` `oq-divorce-cases-genre`
- **У13** (LVL, вес 2×охват 3=6) — `oq-arity-window-13-14` `oq-u13-boundary-union-op` `oq-pentad-role-cycle`
- **У15** (LVL, вес 2×охват 3=6) — `oq-passport-u14-u15` `oq-unit-circle-z15` `oq-pentad-role-cycle`
- **граница** (KW, вес 1×охват 5=5) — `oq-passport-u14-u15` `oq-third-boundary` `oq-const-statistics-code` `oq-unit-circle-z15` `oq-u13-boundary-union-op`
- **Д10** (OD, вес 2×охват 2=4) — `oq-unit-circle-z15` `oq-d10-phase-test`
- **О2** (OD, вес 2×охват 2=4) — `oq-redteam-dependent-guards` `oq-const-statistics-code`
- **О20** (OD, вес 2×охват 2=4) — `oq-o20-missing-benchmark` `oq-o3-twolists`
- **У10** (LVL, вес 2×охват 2=4) — `oq-u8-u10-optests` `oq-tot-groups-8-11`
- **У2** (LVL, вес 2×охват 2=4) — `oq-pi-projection-above-u7` `oq-divorce-cases-genre`
- **У3** (LVL, вес 2×охват 2=4) — `oq-pi-projection-above-u7` `oq-divorce-cases-genre`
- **У7** (LVL, вес 2×охват 2=4) — `oq-pi-projection-above-u7` `oq-sphere-u6-carrier`
- **оверлей** (KW, вес 1×охват 4=4) — `oq-phase-causal-u9` `oq-d10-phase-test` `oq-d2-half-overlay` `oq-synthesis-c-assembly`
- **Agg/агрегация** (KW, вес 1×охват 3=3) — `oq-u14-worlds-agg-op` `oq-sphere-u6-carrier` `oq-fourier-questiongain`
- **C(E)** (KW, вес 1×охват 3=3) — `oq-ce-canon` `oq-ce-weights-proof` `oq-ddelta-weights`
- **θ** (KW, вес 1×охват 3=3) — `oq-arity-window-13-14` `oq-passport-u14-u15` `oq-d10-phase-test`

## Мосты между пулами (порог 2; пары из РАЗНЫХ пулов)

- `oq-d2-half-overlay` (П4) ↔ `oq-divorce-cases-genre` (П10) — вес 5: O_14; О14
- `oq-fourier-questiongain` (П4) ↔ `oq-divorce-cases-genre` (П10) — вес 5: O_14; О14
- `oq-pi-projection-above-u7` (П3) ↔ `oq-sphere-u6-carrier` (П7) — вес 4: У6,7
- `oq-pi-projection-above-u7` (П3) ↔ `oq-divorce-cases-genre` (П10) — вес 4: У2,3
- `oq-pi-projection-above-u7` (П3) ↔ `oq-redteam-dependent-guards` (П12) — вес 3: C-34
- `oq-d2-half-overlay` (П4) ↔ `oq-d2-sign-retrieval-remainder` (П3/П8) — вес 2: У8
- `oq-d2-sign-retrieval-remainder` (П3/П8) ↔ `oq-edgeworth-u9` (Парк) — вес 2: У9
- `oq-phase-causal-u9` (П5) ↔ `oq-u8-u10-optests` (П3) — вес 2: У9
- `oq-phase-causal-u9` (П5) ↔ `oq-tot-groups-8-11` (П3) — вес 2: У9
- `oq-phase-causal-u9` (П5) ↔ `oq-d2-sign-retrieval-remainder` (П3/П8) — вес 2: У9
- `oq-phase-causal-u9` (П5) ↔ `oq-edgeworth-u9` (Парк) — вес 2: У9
- `oq-pi-projection-above-u7` (П3) ↔ `oq-zero-classes-chi-e` (П7) — вес 2: У6
- `oq-pi-projection-above-u7` (П3) ↔ `oq-levy-world` (Парк) — вес 2: У6
- `oq-redteam-dependent-guards` (П12) ↔ `oq-const-statistics-code` (П6) — вес 2: О2
- `oq-sphere-u6-carrier` (П7) ↔ `oq-levy-world` (Парк) — вес 2: У6
- `oq-synthesis-c-assembly` (П4) ↔ `oq-d2-sign-retrieval-remainder` (П3/П8) — вес 2: У8
- `oq-tot-groups-8-11` (П3) ↔ `oq-d2-half-overlay` (П4) — вес 2: У8
- `oq-tot-groups-8-11` (П3) ↔ `oq-synthesis-c-assembly` (П4) — вес 2: У8
- `oq-tot-groups-8-11` (П3) ↔ `oq-edgeworth-u9` (Парк) — вес 2: У9
- `oq-u12-antimode-authorfix` (П11) ↔ `oq-synthesis-c-assembly` (П4) — вес 2: У12
- `oq-u12-antimode-gate` (П11) ↔ `oq-synthesis-c-assembly` (П4) — вес 2: У12
- `oq-u12-radius-r` (П11) ↔ `oq-synthesis-c-assembly` (П4) — вес 2: У12
- `oq-u8-u10-optests` (П3) ↔ `oq-d2-half-overlay` (П4) — вес 2: У8
- `oq-u8-u10-optests` (П3) ↔ `oq-synthesis-c-assembly` (П4) — вес 2: У8
- `oq-u8-u10-optests` (П3) ↔ `oq-edgeworth-u9` (Парк) — вес 2: У9
- `oq-unit-circle-z15` (П2/П6) ↔ `oq-d10-phase-test` (П5) — вес 2: Д10
- `oq-zero-classes-chi-e` (П7) ↔ `oq-levy-world` (Парк) — вес 2: У6

