# FTS-Skeleton v0.2 — результаты provenance/revision/memory пробы

- Статус: exploratory_inductive_bias
- SHA256 кода: 0b46ae12bf4693f6a6542f973ec9f7f1b25b85cd8c2e219357d435207602de68
- SHA256 протокола: 9a57adf1f5a9e86faa55fb119cf266653282dc98d5081611a3214c3935d0e052
- Parameter counts: raw M' = 209; structured = 209

| Контраст | mean delta | 95% half-width |
|---|---:|---:|
| Held-out pattern accuracy | 0.2964 | 0.1331 |
| Full test accuracy | 0.0516 | 0.0254 |

## Интерпретация

Проба проверяет локальный inductive-bias effect explicit gate and
selected-memory feature. Даже положительный результат не означает,
что gate уникален для ФТС: такую же операцию можно объявить стандартным
symbolic prior или включить в независимую M'.
