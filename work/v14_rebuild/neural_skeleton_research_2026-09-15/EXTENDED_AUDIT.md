# Аудит FTS-Skeleton v0.2

- Протокол: EXTENDED_PROTOCOL.md
- Код: run_extended_probe.py
- Результат: EXTENDED_RESULTS.md, extended_results.json
- Дата прогона: 2026-09-15
- Статус: local_inductive_bias_support / non-unique

## Проверки

- python -X utf8 run_extended_probe.py завершился с кодом 0.
- python -X utf8 -m py_compile run_extended_probe.py завершился с кодом 0.
- Seeds: 13, 29, 47, 71, 97.
- Train/test: 800/5000 на seed.
- Held-out pattern присутствовал только в test; на seed число таких примеров
  было 583–664.
- Параметрический бюджет выровнен точно: raw M' = 209, structured = 209.
- SHA256 кода и протокола записаны в EXTENDED_RESULTS.md и extended_results.json.
- Held-out delta accuracy имеет положительный знак на каждом из пяти seeds.

## Результат

| Контраст | Mean delta | 95% half-width | Статус |
|---|---:|---:|---|
| Held-out pattern accuracy | 0.2964 | 0.1331 | локальная поддержка inductive bias |
| Full test accuracy | 0.0516 | 0.0254 | локальная поддержка |
| Held-out Brier improvement | 0.3011 | 0.1420 | согласуется с accuracy |

## Что именно проверено

Структурная модель явно вычисляет:

- residual = v1 - v0;
- valid = same provenance and newer revision;
- selected memory = v1 if valid else v0;
- coarse readouts.

Raw M' получает те же исходные события, но не получает эти derived fields.
Train split не показывает одну комбинацию source/revision; structured model
переносит объявленное правило на неё.

Это подтверждает более узкое утверждение:

> Если задача действительно требует заранее объявленного provenance/revision
> gate и selected-memory readout, явное включение такого inductive bias может
> улучшить compositional/OOD generalization при одинаковом числе параметров.

## Почему это не T3 и не уникальное доказательство ФТС

- Target generator сам использует тот же gate. Это construct-validity design, а не
  независимое открытие семантики.
- Обычная M' может получить те же derived fields как feature engineering или
  symbolic preprocessor; тогда различие исчезнет.
- Gate, selected-memory и provenance могут быть сформулированы без названий ФТС.
- Не измерена стоимость вычисления derived fields как отдельной части C′.
- Нет cross-domain replication, real data или независимого implementation team.
- Это не подтверждение 0_A, κ, Lift, Close, полного порядка уровней или
  биологической архитектуры.

## Вердикт

Результат переводит контур из чистого T1 component evidence к T2 candidate
functional scaffold for consideration в строго объявленном synthetic scope:
hierarchy/residual, typed state, provenance/revision gate и memory/readout имеют
внешние аналоги, спецификация исполнима, а один capacity-matched OOD test
поддерживает полезность интегрированного bias.

T3 supported architecture не закрыт. Следующий обязательный контроль — независимая
M' с тем же symbolic gate/derived fields и тест, где gate не совпадает с
генератором target, чтобы проверить, не является ли положительный результат
тривиальной утечкой inductive bias.

