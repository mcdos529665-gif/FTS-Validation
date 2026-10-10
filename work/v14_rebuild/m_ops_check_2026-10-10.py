# -*- coding: utf-8 -*-
"""Синтаксическая проверка: М-формы ЛУ2…ЛУ7 как композиции D (=↔≠, ∧↔∨), X∧D(X), X∨D(X).

Деревья сравниваются с учётом коммутативности (дети сортируются), БЕЗ ассоциативного
сплющивания и без поглощения — вложенная группировка сохраняется (U7_LOGIC_GROUPING).
"""
from itertools import product

EQ, NE = ("=",), ("≠",)

def And(a, b): return ("∧", a, b)
def Or(a, b): return ("∨", a, b)

def D(t):  # двойственность: = ↔ ≠, ∧ ↔ ∨ (без ¬)
    if t == EQ: return NE
    if t == NE: return EQ
    op = {"∧": "∨", "∨": "∧"}[t[0]]
    return (op, D(t[1]), D(t[2]))

def canon(t):  # только коммутативность
    if len(t) == 1: return t
    a, b = sorted([canon(t[1]), canon(t[2])], key=repr)
    return (t[0], a, b)

def same(x, y): return canon(x) == canon(y)

# активные формы из канона: M_02…M_07 (query.py card M_06 / M_07)
M2, M3 = EQ, NE
M4 = And(EQ, NE)
M5 = Or(EQ, NE)
M6 = And(M4, M5)
M7 = Or(M6, Or(M4, M5))

checks = {
    "M3 = D(M2)": same(M3, D(M2)),
    "M4 = M3 ∧ D(M3)": same(M4, And(M3, D(M3))),
    "M5 = D(M4)": same(M5, D(M4)),
    "M5 = M2 ∨ D(M2)": same(M5, Or(M2, D(M2))),
    "M6 = M5 ∧ D(M5)": same(M6, And(M5, D(M5))),
    "M7 = M6 ∨ D(M6)": same(M7, Or(M6, D(M6))),
    "M7 ≠ D(M6) буквально": not same(M7, D(M6)),
}

# поглощение: в любой решётке M7 ≡ D(M6). Проверка в булевой (2 зн.) и в Клини (3 зн., не булева)
def ev(t, v, lo, hi, neg):
    if t == EQ: return v
    if t == NE: return neg(v)
    a, b = ev(t[1], v, lo, hi, neg), ev(t[2], v, lo, hi, neg)
    return min(a, b) if t[0] == "∧" else max(a, b)

for name, vals in (("булева", (0, 1)), ("Клини", (0, 0.5, 1))):
    neg = lambda x: 1 - x
    checks[f"M7 ≡ D(M6) в {name} логике"] = all(ev(M7, v, 0, 1, neg) == ev(D(M6), v, 0, 1, neg) for v in vals)

bad = [k for k, ok in checks.items() if not ok]
for k, ok in checks.items():
    print(("PASS " if ok else "FAIL ") + k)
assert not bad, bad
print(f"{len(checks)} PASS / 0 FAIL")
