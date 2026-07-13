# Журнал воспроизведения эмпирического слоя

Дата аудита: 2026-07-13 (Europe/Moscow). Базовая среда и исходный commit записаны в
`BASELINE.md`; версии закреплены в `requirements-audit.txt`. Все новые расчёты являются
**post-hoc audit reanalysis, not preregistered**.

## Найдено → зависимости → вывод → что не закрыто

**Найдено.** Исторические вычисления детерминированы, но исходный статистический вывод
O_20/D2 ошибочно использовал repeated-CV фолды как независимые наблюдения; D2 дополнительно
масштабировал весь X до CV. Д10 воспроизводится численно, однако его поколения имеют
интерпретационные конфаунды и стоп-артефакты.

**Зависимости.** Исправленные O_20/D2 используют fit всех преобразований только на train-fold,
Nadeau–Bengio corrected repeated-CV approximation внутри датасета, Holm внутри семейства
четырёх датасетов и один агрегированный эффект на независимый датасет для основного sign-test.
Д10 воспроизведён в отдельном output-каталоге без изменения истории.

**Вывод.** O_20 не подтверждён (1/4 побед, sign p=0.9375); D2 strong не подтверждён
(HistGB 2/4, sign p=0.6875); ни одна версия Д10 не даёт чистого внешнего вердикта о фазе.

**Что не закрыто.** Четыре независимых датасета дают минимальное one-sided sign p=0.0625
даже при 4/4. T3/T2 не capacity-matched. OpenML `cylinder-bands` data_id=33/version=1
помечен сервисом inactive. Новые подтверждающие эксперименты требуют отдельной предрегистрации
и не входят в этот аудит.

## Среда

- Python 3.13.14
- SymPy 1.14.0
- NumPy 2.4.6
- pandas 3.0.3
- SciPy 1.17.1
- scikit-learn 1.9.0

## Данные O_20

| Dataset | OpenML ID/version | OpenML MD5 | Materialized SHA256 |
|---|---|---|---|
| colic | 25 / 1 | `933f0487c0fa52a5483c39d85a351f93` | `db01eff30816464812a5d58e99d582f2bc826c753c56060a847dcd58d97aa1b7` |
| hepatitis | 55 / 1 | `7d82e0f546eaaf1c5cc128825fe5a0fb` | `b12570a6db8a1f32face807179bca6320e24d8374fd07fa3c834c686ce237bcc` |
| vote | 56 / 1 | `3c16059c5b92f6551f720f97d0eccc09` | `82288ed3c48b0f8ac48b12de441b5a194c9b522d8b806ab89616772ab941ab4a` |
| cylinder-bands | 33 / 1 (inactive) | `59ec3d17d1fb9fa79c3108a7a5a9bc5e` | `f48d6e6c9ac460b4e5ea9a9b2d6875c1d9d6501d26ad89230ac19b102aec59b5` |

Результат повторён дважды: SHA256 `audit_results.json` =
`ad8803327ffb066bbd39cbe93a39dce796e2e08d63735023086c53dad01a0261`.

## Данные D2

| Dataset | Source / ID/version | MD5 или materialized SHA256 |
|---|---|---|
| breast_cancer | sklearn 1.9.0 builtin | `a879b72e7876cd8d61068e07a172280b0561c48fe3a1551c48dc23f62f0c80b5` |
| ionosphere | OpenML 59 / 1 | MD5 `23dd3c8b5693e2848901fd1a0248ef42`; SHA256 `a5d1e73cc01d926c0eb14596b6fc303ce1b538120e4ecf6b9a5978e5a296b69f` |
| sonar | OpenML 40 / 1 | MD5 `3ab630fbbfe25ab48b9bb47ce5759203`; SHA256 `c1af5639c829f5d8f89c63a3ed084826d8e812cc9d7f4604c9cac895f488a886` |
| diabetes | OpenML 37 / 1 | MD5 `3cbaa3e54586aa88cf6aacb4033e4470`; SHA256 `21a617656ffa58cd28960a2a69f4d0d972d53891ea39ce1b9e4901ca9a2c3d34` |

Результат повторён дважды: SHA256 `audit_results.json` =
`9e72164612c45ad693b1675c32f6b7a5f912e3fcd5b85409781c1b0fc32e1d70`.

## RadioML и Д10

- `RML2016.10a_dict.pkl`: 640,919,653 bytes.
- SHA256: `b29ccc25b00d0718cd3b70ffa9158662ec83f6d9b63ffd845c7bcbe3b3096e8c`.
- Пять вариантов: `semantic_json_equal=true`, `byte_equal=true` для каждого.
- Runtime: synthetic-v1 2.0 s; synthetic-pilot 255.9 s; RadioML-v1 1069.0 s;
  RadioML-v2 1442.3 s; RadioML-v3 175.5 s.
- Машинный manifest: `reproductions/d10/run_manifest.json`.
- Интерпретационный вердикт: `../d10_phase/AUDIT_REANALYSIS.md`.

## Git-порядок предрегистрация → код → результат

| Эксперимент | Предрегистрация | Код | Результат | Аудит |
|---|---|---|---|---|
| O_20 | `b8cb6aa` | `b8cb6aa` | `e26defd` | порядок достаточен |
| D2 | `f473881` | `3fff80a` | `3fff80a` | P2: код и результат одним commit, промежуточный код git не удостоверяет |
| Д10 synthetic-v1 | `cd3fcf7` | `69e131d` | `335ceef` | P2: результат раньше commit кода |
| Д10 pilot | `8eb9255` | `8eb9255` | `fc621f9` | порядок достаточен |
| RadioML-v1 | `36de002` | `36de002` | `bce947e` | порядок достаточен |
| RadioML-v2 | `c1ac7c0` | `c1ac7c0` | `e13cfae` | порядок достаточен |
| RadioML-v3 | `d8b1de0` | `cad2393` | `7a95dfc` | строгий порядок соблюдён |

История не переписывается. P2-разрывы компенсированы консервативным статусом, полным rerun
и открытым условием повторной проверки; они не дают права повышать утверждения.

## Команды

```text
python -X utf8 work/v14_rebuild/o20/run_o20_audit.py
python -X utf8 work/v14_rebuild/d2_sign/run_d2_audit.py
python -X utf8 work/v14_rebuild/audit/reproduce_d10.py
python -X utf8 work/v14_rebuild/audit/run_audit.py empirical
```

OpenML cache задаётся `FTS_OPENML_CACHE`; без него используется временный каталог ОС.
Полные fold-level AUC и версии среды находятся в `o20/audit_results.json` и
`d2_sign/audit_results.json`. Полные stdout Д10 сохранены рядом с изолированными JSON.

