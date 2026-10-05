"""Проверки addendum_2026-10-04_upper_levels.md (номера C-96…C-99 предварительные).
Чистый Python. Запуск: python verification_c96.py"""
import cmath, math
from fractions import Fraction as Fr

res = []
def check(cid, desc, cond):
    res.append(bool(cond)); print("PASS" if cond else "FAIL", cid, desc)

xs = [i / 10 for i in range(-30, 31)]
close = lambda a, b, e=1e-9: abs(a - b) <= e * max(1, abs(a), abs(b))

# C-96: окружность и гипербола; eˣ = cosh + sinh
ok = all(close(math.cosh(t) ** 2 - math.sinh(t) ** 2, 1) for t in xs)            # (cosh, sinh) на x²−y²=1
ok &= all(close(math.exp(t), math.cosh(t) + math.sinh(t)) for t in xs)            # У11 = чётная + нечётная часть
ok &= all(close(math.cosh(-t), math.cosh(t)) and close(math.sinh(-t), -math.sinh(t)) for t in xs)
ok &= all(close(cmath.cos(1j * t).real, math.cosh(t)) for t in xs)                # cosh x = cos(ix)
ok &= all(1 - x * x > 0 for x in [i / 100 for i in range(-99, 100)])              # при |x|<1 у x²−y²=1 решений нет: две ветви
ok &= all(close(math.cos(t) ** 2 + math.sin(t) ** 2, 1) for t in xs)              # окружность замкнута (период 2π)
check("C96", "гипербола x²−y²=1: (cosh,sinh) на ней, две ветви (|x|≥1), cosh x=cos(ix); eˣ=cosh x+sinh x (чётная + нечётная части)", ok)

# C-97: Якоби sn(u,k): (y')² = (1−y²)(1−k²y²); k=0 → sin, k=1 → tanh; четверть-период K(k) растёт до ∞
def d(f, u, h=1e-6): return (f(u + h) - f(u - h)) / (2 * h)
ode = lambda f, k, u: (d(f, u)) ** 2 - (1 - f(u) ** 2) * (1 - k * k * f(u) ** 2)
us = [i / 10 for i in range(-15, 16)]
ok = all(abs(ode(math.sin, 0, u)) < 1e-8 for u in us) and all(abs(ode(math.tanh, 1, u)) < 1e-8 for u in us)
def agm(a, b):
    for _ in range(60): a, b = (a + b) / 2, math.sqrt(a * b)
    return a
K = lambda k: math.pi / (2 * agm(1, math.sqrt(1 - k * k)))
ks = [0, 0.3, 0.6, 0.9, 0.99, 0.9999, 0.999999]
Ks = [K(k) for k in ks]
ok &= close(Ks[0], math.pi / 2) and all(a < b for a, b in zip(Ks, Ks[1:])) and Ks[-1] > 7
check("C97", "Якоби: sn(u,0)=sin u, sn(u,1)=tanh u удовлетворяют (y')²=(1−y²)(1−k²y²); K(0)=π/2, K(k)↑∞ при k→1 (период круга → незамкнутая гипербола)", ok)

# C-98: гиперболический поворот сохраняет x²−t² (как обычный поворот сохраняет x²+y²)
ok = True
for ph in (-2, -0.5, 0.7, 1.9):
    c, s = math.cosh(ph), math.sinh(ph)
    for x in (-1.3, 0.4, 2.0):
        for t in (-0.8, 0.0, 1.1):
            x2, t2 = c * x + s * t, s * x + c * t
            ok &= close(x2 * x2 - t2 * t2, x * x - t * t)
check("C98", "гиперболический поворот (cosh φ, sinh φ) сохраняет x²−t²", ok)

# C-99: точки порядка 2 на эллиптической кривой y²=x³−x вместе с ∞ образуют V4
O = None
def add(P, Q):
    if P is O: return Q
    if Q is O: return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and y1 == -y2: return O
    m = (3 * x1 * x1 - 1) / (2 * y1) if P == Q else (y2 - y1) / (x2 - x1)
    x3 = m * m - x1 - x2
    return (x3, m * (x1 - x3) - y1)
T = [O, (Fr(-1), Fr(0)), (Fr(0), Fr(0)), (Fr(1), Fr(0))]
ok = all(P is O or (P[1] ** 2 == P[0] ** 3 - P[0]) for P in T)
ok &= all(add(P, P) is O for P in T)                                               # все порядка ≤ 2
ok &= all(add(T[i], T[j]) == T[6 - i - j] for i in (1, 2, 3) for j in (1, 2, 3) if i != j)  # сумма двух = третья
check("C99", "y²=x³−x: {∞,(−1,0),(0,0),(1,0)} — группа, все элементы порядка ≤2, сумма двух = третья: V4 (группа Клейна) наверху", ok)

print(f"\nИТОГ: {sum(res)} PASS / {len(res) - sum(res)} FAIL")

if __name__ == "__main__":
    raise SystemExit(0 if all(res) else 1)
