"""Свидетель к статье для Хабра (гл. 2, XOR-обмен): проверка утверждений, приведённых в тексте.

Запуск: py -3.11 -X utf8 work/v14_rebuild/paper_plan/checks/xor_swap_check.py
Ожидаемый итог: PASS (0 расхождений из 100000; одна и та же ячейка даёт 0).
"""
import random

random.seed(1)
N = 100_000

mismatches = 0
for _ in range(N):
    a = random.getrandbits(32)
    b = random.getrandbits(32)
    x, y = a, b
    x ^= y
    y ^= x
    x ^= y
    if (x, y) != (b, a):
        mismatches += 1

# a и b — одна и та же ячейка: a ^= a обнуляет значение (оговорка из текста статьи)
cell = 12345
cell ^= cell
cell ^= cell
cell ^= cell

ok = mismatches == 0 and cell == 0
print(f"XOR-обмен, разные ячейки: расхождений {mismatches} из {N}")
print(f"XOR-обмен, одна ячейка: результат {cell} (ожидается 0)")
print("PASS" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
