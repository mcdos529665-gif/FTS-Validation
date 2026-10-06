# WOLFRAM_CHECKS — записи независимых проверок

## WF-106 — 2026-10-06

Claims: `WINDOW_SIGN_SHADOW_INVARIANT`, `WINDOW_SIGN_MODELS_INEQUIVALENT`,
`WINDOW_NODE_INNER_NONUNIQUE`; арифметические кандидаты окон 13/25.
Verdict: **inconclusive**, `provider_error` в коде вызова, без математического
результата. Один context/evaluator, 27.202 с, повторов нет.
Полный пакет, фактически отправленный WL-код, сырой ответ, диагноз и
границы локальных доказательств:
[запись](../e5_literature_review/window_signed_products_2026-10-06/WOLFRAM.md).
Эффект на канонические `St_math`/`St_FTS`: отсутствует.

## WF-107 — 2026-10-06

Claim: `WINDOW_RELATIVE_SIGN_PROBE`; кандидат совместного сравнения путей.
Verdict: **confirmed_math** для `((s+t)²−(s−t)²)/4=st` на R²,
инвариантности общей смены знака и полной таблицы четырёх знаковых пар.
Один context/evaluator, 18.621 с, повторов нет. Полный код и сырой результат:
[запись](../e5_literature_review/window_signed_products_2026-10-06/WOLFRAM_107.md).
Смысл ФТС и выбор алгебры не подтверждены. WF-106 остаётся inconclusive;
канонические `St_math`/`St_FTS` не меняются.
