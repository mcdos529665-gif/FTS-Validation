# Проверки записки о рекурсивном различении

2026-09-12. Конечные внешние модели; не C-NN, не доказательство статусов ФТС.
PASS контрпримера подтверждает ограничение проверяемой внешней формулировки.

**8 PASS / 0 FAIL.**

| ID | Предикат | Результат | Свидетель |
|---|---|---|---|
| RN-01 | Байты исходной записки | PASS | {"bytes": 31284, "source_sha256": "30c38293a9cbedb2770e6ed00724fbe0f9b66e0840cff967365f1200289e017b"} |
| RN-02 | Активный вывод и доступный аппарат | PASS | {"from_active_readout": false, "from_available_state": true, "same_decoder_cost": 1} |
| RN-03 | Операция без сохранённых исходных данных | PASS | {"sign_operation_available": true, "original_sign_recoverable": false} |
| RN-04 | Рефлексивность ядра полного наблюдателя | PASS | {"total_observers_checked": 16, "can_have_Eq_a_a_false": false} |
| RN-05 | Допустимая погрешность не обязана быть транзитивной | PASS | {"witness": [0, 1, 2], "tolerance": 1, "transitive": false} |
| RN-06 | Исключённое третье не даёт известного ответа | PASS | {"known_excluded_middle": true, "known_either_answer": false} |
| RN-07 | Модель двух каналов без explosion | PASS | {"values": 4, "information_order_total": false, "explosion_under_positive_designation": false, "FTS_absence_semantics_proved": false} |
| RN-08 | Индексное перекрытие четырёх троек | PASS | {"triples": [[-1, 0, 1], [1, 2, 3], [3, 4, 5], [5, 6, 7]], "shared_boundary_levels": [1, 3, 5], "semantic_recursion_proved": false} |
