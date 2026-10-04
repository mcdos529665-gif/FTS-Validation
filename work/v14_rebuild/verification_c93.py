"""Проверки §8 addendum_2026-10-04_windows_symmetry.md (номера C-93…C-95 предварительные).
Чистый Python, точная целочисленная арифметика в Z[ζ_s]. Запуск: python verification_c93.py

Метод. Для окна длины n шаг s = n−1; остаток простого p по модулю s есть его Фробениус в
круговом поле Q(ζ_s). Для каждой подгруппы H единиц (Z/s)^× строится многочлен по периодам
η_c = Σ_k W_k Σ_{c0∈c} ζ^(k·c0) (c — смежные классы по H, W — фиксированные целые веса):
его корни порождают подполе, неподвижное относительно H. p «расщепляется» в подполе, если
многочлен по модулю p имеет столько различных корней, какова степень. Профиль остатка —
набор таких флагов по всем подгруппам; два остатка различимы, если профили разные.
Простые, на которых многочлен по модулю p имеет кратный корень, пропускаются."""
import random
from math import gcd, isqrt

res = []
def check(cid, desc, cond):
    res.append(bool(cond)); print("PASS" if cond else "FAIL", cid, desc)

def isp(p): return p > 1 and all(p % d for d in range(2, isqrt(p) + 1))

def pdiv(a, b):                      # деление многочленов (старшие коэффициенты в конце), b унитарен
    a = a[:]; q = [0] * max(1, len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]; q[i] = c
        for j, bj in enumerate(b): a[i + j] -= c * bj
    return q, a[:len(b) - 1]
def cyclo(s):                        # Φ_s как список коэффициентов
    f = [-1] + [0] * (s - 1) + [1]
    for d in range(1, s):
        if s % d == 0: f, r = pdiv(f, cyclo(d)); assert not any(r)
    return f

def units(s): return [x for x in range(1, s) if gcd(x, s) == 1]
def subgroups(U, s):
    out = set()
    for a in U:
        for b in U:
            H, fr = {1}, [1]
            while fr:
                x = fr.pop()
                for g in (a, b):
                    y = x * g % s
                    if y not in H: H.add(y); fr.append(y)
            out.add(frozenset(H))
    return sorted(out, key=lambda h: (len(h), sorted(h)))

def period_poly(H, U, s, phi):
    cos, seen = [], set()
    for u in U:
        if u not in seen:
            c = frozenset(u * h % s for h in H); seen |= c; cos.append(c)
    rng = random.Random(1000 * len(H) + s)
    for _ in range(300):
        W = [rng.randint(-3, 3) for _ in range(s)]
        etas = []                    # η как вектор коэффициентов при ζ^j, j<s
        for c in cos:
            v = [0] * s
            for k in range(1, s):
                for c0 in c: v[k * c0 % s] += W[k]
            etas.append(v)
        red = [tuple(pdiv(v, phi)[1]) if len(v) >= len(phi) else tuple(v) for v in etas]
        if len(set(red)) == len(red): break
    poly = [[1] + [0] * (s - 1)]     # многочлен от X; коэффициенты в Z[ζ]/(ζ^s−1)
    for e in etas:
        new = [[0] * s for _ in range(len(poly) + 1)]
        for i, a in enumerate(poly):
            for j in range(s): new[i + 1][j] += a[j]          # X·a
            for j in range(s):
                if a[j]:
                    for k in range(s):
                        if e[k]: new[i][(j + k) % s] -= a[j] * e[k]   # −η·a
        poly = new
    co = []
    for a in poly:
        r = pdiv(a, phi)[1]; r += [0] * (len(phi) - 1 - len(r))
        assert all(x == 0 for x in r[1:]), "коэффициент не рационален"
        co.append(r[0])
    return co[::-1]                  # старший коэффициент первым

def ev(co, x, p):
    y = 0
    for c in co: y = (y * x + c) % p
    return y
def splits(co, p):
    d = len(co) - 1
    dco = [c * (d - i) for i, c in enumerate(co[:-1])]
    roots = [x for x in range(p) if ev(co, x, p) == 0]
    if any(ev(dco, x, p) == 0 for x in roots): return None   # кратный корень: пропустить p
    return len(roots) == d

def classes(n, P0=200, P1=1500):
    s = n - 1; U = units(s); phi = cyclo(s)
    polys = [period_poly(H, U, s, phi) for H in subgroups(U, s)]
    prof = {}
    for p in range(P0, P1):
        if not isp(p) or s % p == 0: continue
        key = tuple(splits(co, p) for co in polys)
        if None in key: continue
        prof.setdefault(p % s, set()).add(key)
    consistent = all(len(v) == 1 for v in prof.values()) and sorted(prof) == U
    cl = {}
    for r, v in prof.items(): cl.setdefault(next(iter(v)), []).append(r)
    return consistent, sorted(sorted(c) for c in cl.values()), polys

def inv(a, s): return next(b for b in range(1, s) if a * b % s == 1)
def pairs(s): return sorted(sorted({a, inv(a, s)}) for a in units(s) if a <= inv(a, s))
def order(a, s):
    k, y = 1, a % s
    while y != 1: y = y * a % s; k += 1
    return k

R = {n: classes(n) for n in (11, 13, 15, 17, 19, 21, 25)}

# C-93: окна 17 и 21 — предсказание, зафиксированное до счёта
ok = R[17][0] and R[17][1] == [[1], [3, 11], [5, 13], [7], [9], [15]]
ok &= R[21][0] and R[21][1] == [[1], [3, 7], [9], [11], [13, 17], [19]]
ok &= sorted(order(a, 16) for a in units(16)) == [1, 2, 2, 2, 4, 4, 4, 4]   # C2×C4: не цикл, не все порядка 2
ok &= sorted(order(a, 20) for a in units(20)) == [1, 2, 2, 2, 4, 4, 4, 4]
ok &= order(16 // 2 - 1, 16) <= 2 and order(20 // 2 - 1, 20) <= 2 and inv(15, 16) == 15 and inv(19, 20) == 19
check("C93", "окна 17 (шаг 16) и 21 (шаг 20), единицы C2×C4: 6 классов; неразличимы ровно {3,11},{5,13} и {3,7},{13,17}; узел (−1) и середина (7; 9) различимы отдельно", ok)

# C-94: во всех окнах неразличимы ровно остаток и обратный ему; в зеркальных окнах различимо всё
ok = all(R[n][0] and R[n][1] == pairs(n - 1) for n in R)
ok &= all(len(R[n][1]) == len(units(n - 1)) for n in (13, 25))
ok &= all(len(R[n][1]) < len(units(n - 1)) for n in (11, 15, 17, 19, 21))
check("C94", "окна 11,13,15,17,19,21,25: классы различимости = пары {a, a⁻¹} (теория Галуа [внешнее]); в 13 и 25 все остатки обратны сами себе и различимы", ok)

# C-95: узел окна (остаток −1) = комплексное сопряжение: среди остатков ровно 1 и −1 расщепляются
# в вещественном подполе Q(ζ_s)⁺ (неподвижном относительно {±1}); узлы пятёрок не видят √−1
ok = True
for n in (11, 13, 15, 17, 19, 21, 25):
    s = n - 1; U = units(s); phi = cyclo(s)
    co = period_poly(frozenset({1, s - 1}), U, s, phi)
    got = set()
    for p in range(200, 1500):
        if isp(p) and s % p:
            f = splits(co, p)
            if f: got.add(p % s)
    ok &= got == {1, s - 1}
ok &= all(not any((x * x + 1) % p == 0 for x in range(p)) for p in range(3, 400) if isp(p) and p % 4 == 3)
check("C95", "узел любого окна (остаток −1 по шагу) — Фробениус = сопряжение i↔−i: расщепляются в вещественном подполе только остатки 1 и −1; простые 4k+3 не имеют √−1 [внешнее]", ok)

print(f"\nИТОГ: {sum(res)} PASS / {len(res) - sum(res)} FAIL")
