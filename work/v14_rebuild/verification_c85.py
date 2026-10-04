"""Проверки addendum_2026-10-04_windows_symmetry.md (номера C-85…C-92 предварительные).
Чистый Python. Запуск: python verification_c85.py"""
import math
from math import gcd, isqrt

res = []
def check(cid, desc, cond):
    res.append(bool(cond)); print("PASS" if cond else "FAIL", cid, desc)

def isp(p): return p > 1 and all(p % d for d in range(2, isqrt(p) + 1))
def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def rep(n, form, R):
    return n >= 0 and any(form(x, y) == n for x in range(-R, R + 1) for y in range(-R, R + 1))
def sq(a, p): return any((x * x - a) % p == 0 for x in range(p))

N = 400
two = lambda n: rep(n, lambda x, y: x * x + y * y, 21)
# C-85: суммы двух квадратов (5-окна, шаг 4)
ok = all(two(n) == all(e % 2 == 0 for p, e in factor(n).items() if p % 4 == 3) for n in range(1, N))
nodes = list(range(-1, 40, 4)); mids = [1, 5, 9, 13, 17]
ok &= all(not two(n) for n in nodes if n > 0)           # узлы ≡3 mod 4 (и −1) не суммы двух квадратов
ok &= all(two(n) for n in mids) and not two(21) and not two(3) and two(9)
check("C85", "5-окна: критерий Ферма (простые 4k+3 в чётной степени); узлы 3,7,11,15,19 выпадают; середины 1,5,9,13,17 суммы двух квадратов; 21 нет; 3 нет, 9=3² да", ok)

# C-86: суммы трёх квадратов (9-окна шаг 8), Лагранж
three = lambda n: n >= 0 and any(x*x + y*y + z*z == n for x in range(46) for y in range(46) for z in range(46))
def legendre_out(n):
    while n > 0 and n % 4 == 0: n //= 4
    return n % 8 == 7
M = 300
ok = all(three(n) == (not legendre_out(n)) for n in range(0, M))
ok &= all(not three(n) for n in (7, 15, 23, 31, 39)) and all(three(n) for n in (3, 11, 19, 27, 35))
ok &= all(any(a*a + b*b + c*c + d*d == n for a in range(18) for b in range(18) for c in range(18) for d in range(18)) for n in range(0, 300))
check("C86", "9-окна (шаг 8): суммы трёх квадратов = не 4ᵃ(8b+7); узлы 7,15,23,31,39 выпадают, середины 3,11,19,27,35 держатся; четыре квадрата — все n<300", ok)

# C-87: форма Эйзенштейна x²+xy+y² (7-окна, шаг 6)
eis = lambda n: rep(n, lambda x, y: x*x + x*y + y*y, 30)
ok = all(eis(n) == all(e % 2 == 0 for p, e in factor(n).items() if p % 3 == 2) for n in range(1, 300))
ok &= all(not eis(n) for n in (2, 5, 8, 11, 14, 17, 20, 23)) and all(n % 3 != 2 for n in range(0, 200) if eis(n))
check("C87", "7-окна (шаг 6): x²+xy+y² не принимает значений ≡2 mod 3; узлы 5,11,17,23 и середины 2,8,14,20 выпадают (критерий: простые ≡2 mod 3 в чётной степени)", ok)

# C-88: окно 13 (шаг 12): остаток простого mod 12 ↔ наличие √−1, √−3
tab = {}
for p in range(5, 3000):
    if isp(p): tab.setdefault(p % 12, set()).add((int(sq(-1, p)), int(sq(-3, p))))
check("C88", "окно 13 (шаг 12): p mod 12 → (√−1,√−3): 1→(1,1), 5→(1,0), 7→(0,1), 11→(0,0)",
      tab == {1: {(1, 1)}, 5: {(1, 0)}, 7: {(0, 1)}, 11: {(0, 0)}})

# C-89: окно 25 (шаг 24): три корня, восемь комбинаций; 24 — последний модуль «все единицы в квадрате 1»
t = {}
for p in range(5, 3000):
    if isp(p): t.setdefault(p % 24, set()).add(tuple(int(sq(a, p)) for a in (-1, -3, -2)))
U = [x for x in range(24) if gcd(x, 24) == 1]
good = [n for n in range(2, 600) if all(x * x % n == 1 for x in range(1, n) if gcd(x, n) == 1)]
ok = all(len(v) == 1 for v in t.values()) and len({next(iter(v)) for v in t.values()}) == 8 and len(t) == 8
ok &= t[23] == {(0, 0, 0)} and t[11] == {(0, 0, 1)} and t[5] == {(1, 0, 0)} and t[7] == {(0, 1, 0)} and t[1] == {(1, 1, 1)}
ok &= all(x * x % 24 == 1 for x in U) and good == [2, 3, 4, 6, 8, 12, 24]
check("C89", "окно 25 (шаг 24): 8 остатков ↔ 8 комбинаций (√−1,√−3,√−2); 23 без корней; 5,7,11 по одному; модули с (все единицы)²=1: 2,3,4,6,8,12,24", ok)

# C-90: сечения креста |y|=|x| по знаку x и группа меток
sg = lambda x: (x > 0) - (x < 0)
E = {"x": lambda x: 1, "−x": lambda x: -1, "|x|": sg, "−|x|": lambda x: -sg(x)}
xs = [-3, -1, -0.5, 0.5, 1, 2]
ok = all(abs(E[k](x) * x) == abs(x) for k in E for x in xs)
names = list(E); mult = {(a, b): next(c for c in names if all(E[a](x) * E[b](x) == E[c](x) for x in xs)) for a in names for b in names}
ok &= all(mult[(a, a)] == "x" for a in names) and all(mult[(a, b)] == mult[(b, a)] for a in names for b in names)
ok &= all(E["|x|"](x) * x == abs(x) and E["−|x|"](x) * x == -abs(x) for x in xs if x != 0)
check("C90", "сечения креста y=ε(x)x: ε∈{1,−1,sgn,−sgn} дают x,−x,|x|,−|x|; метки образуют V4 (все в квадрате 1); каждое сечение лежит на кресте", ok)

# C-91: группы порядка 4 и единицы колец
gi = {(1, 0), (-1, 0), (0, 1), (0, -1)}
mul = lambda a, b: (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])
ok = (mul((0, 1), (0, 1)) == (-1, 0)) and all(any(mul(a, b) == (1, 0) for b in gi) for a in gi)
ordr = lambda a: next(k for k in range(1, 9) if (lambda z: z)(__import__("functools").reduce(lambda u, _: mul(u, a), range(k - 1), a)) == (1, 0))
ok &= ordr((0, 1)) == 4 and ordr((-1, 0)) == 2
check("C91", "Z[i]: единицы {1,i,−1,−i}, i²=−1, порядок i равен 4 (циклическая C4); у V4 все порядки ≤2", ok)

# C-92: окна 11 (шаг 10) и 15 (шаг 14): поворотные группы, выпадение 5 и 7, корни из 5 и −7
def unit_order(x, m):
    k, y = 1, x % m
    while y != 1: y = y * x % m; k += 1
    return k
U10 = [x for x in range(1, 10) if gcd(x, 10) == 1]; U14 = [x for x in range(1, 14) if gcd(x, 14) == 1]
ok = U10 == [1, 3, 7, 9] and 3 * 3 % 10 == 9 and unit_order(3, 10) == 4          # 3² ≡ −1 mod 10: C4, не V4
ok &= U14 == [1, 3, 5, 9, 11, 13] and pow(3, 3, 14) == 13 and unit_order(3, 14) == 6  # 3³ ≡ −1 mod 14: C6
ok &= [x for x in range(1, 10, 2) if gcd(x, 10) != 1] == [5] and [x for x in range(1, 14, 2) if gcd(x, 14) != 1] == [7]
t10, t14 = {}, {}
for p in range(11, 3000):
    if isp(p):
        t10.setdefault(p % 10, set()).add(int(sq(5, p)))
        t14.setdefault(p % 14, set()).add(int(sq(-7, p)))
ok &= t10 == {1: {1}, 9: {1}, 3: {0}, 7: {0}} and t14 == {1: {1}, 9: {1}, 11: {1}, 3: {0}, 5: {0}, 13: {0}}
ok &= all(x % 2 == 0 or gcd(x, s) != 1 for x, s in ((4, 10), (14, 10), (24, 10), (6, 14), (20, 14), (34, 14)))
# середины окна длины n: n=5,9,13 — обратимый остаток; n=3,7,11,15 — необратимый
cent = {n: gcd((n - 1) // 2 - 1, n - 1) for n in (3, 5, 7, 9, 11, 13, 15)}
ok &= all(cent[n] == 1 for n in (5, 9, 13)) and all(cent[n] != 1 for n in (3, 7, 11, 15))
check("C92", "окно 11 (шаг 10): единицы {1,3,7,9}, 3²≡−1 (C4), выпадает 5, остаток→√5 (1,9 да; 3,7 нет); окно 15 (шаг 14): 3³≡−1 (C6), выпадает 7, остаток→√−7 (1,9,11 да; 3,5,13 нет); середина обратима только при длине 5,9,13", ok)

print(f"\nИТОГ: {sum(res)} PASS / {len(res) - sum(res)} FAIL")
