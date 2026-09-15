# Аудит FTS-Skeleton v0.3

- Протокол: TARGET_INDEPENDENT_PROTOCOL.md
- Код: run_target_independent_probe.py
- Результат: TARGET_INDEPENDENT_RESULTS.md, target_independent_results.json
- Дата прогона: 2026-09-15
- Статус: transfer_support_in_synthetic_scope / non-unique

## Проверки

- Программа завершилась с кодом 0.
- py_compile завершился с кодом 0.
- 20 строк результатов: 5 seeds × 2 domains × 2 readouts.
- Точный parameter matching:
  - scalar: raw M' 177, structured 177;
  - vector: raw M' 241, structured 241.
- В каждом из четырёх условий held-out delta accuracy положителен на 5/5 seeds.

## Результаты

| Domain | Readout | Held-out delta | Full delta | Positive seeds |
|---:|:---:|---:|---:|---:|
| 1D | A | 0.3889 ± 0.1330 | 0.0572 ± 0.0161 | 5/5 |
| 1D | B | 0.2961 ± 0.0793 | 0.0468 ± 0.0139 | 5/5 |
| 2D | A | 0.4075 ± 0.0628 | 0.0658 ± 0.0136 | 5/5 |
| 2D | B | 0.3212 ± 0.0471 | 0.0565 ± 0.0074 | 5/5 |

## Допустимый вывод

Одна и та же явно заданная provenance/revision/selected-memory representation
переносит inductive bias между двумя readout и двумя размерностями контента.
Это сильнее, чем v0.2: эффект не исчезает при смене readout и domain.

Вместе с внешними component-level bridges и M′-audit результат даёт достаточное
основание рассматривать ФТС как кандидатный functional scaffold для искусственной
нейронной архитектуры в synthetic/algorithmic scope.

## Ограничения

- Derived fields по-прежнему вычисляются заранее; это explicit prior, а не
  learned discovery.
- Symbolic-gate M′ воспроизводит тот же v0.2 feature map exactly, поэтому
  transfer effect не является ФТС-специфичным.
- Векторный domain синтетический и не заменяет benchmark на независимых данных.
- Не проверены compute cost derived fields, DNC/GRU-D/NeuMiss baselines на общем
  контракте, nor full role ablations.
- Результат не повышает статусы ФТС и не подтверждает биологическую модель.

