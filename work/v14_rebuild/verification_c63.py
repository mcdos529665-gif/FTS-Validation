"""verification_c63.py — машинные проверки C-63…C-76 (двухканальное чтение У2–У9, 2026-10-04).

Статус всех утверждений, которые эти проверки поддерживают: кандидат (см.
addendum_2026-10-04_two_channels.md). Чистый Python, без внешних библиотек.
Полиномиальные тождества — точно (Fraction) на сетке; кусочные — перебор.
Запуск: python verification_c63.py  → строка на каждую проверку и итог.
"""
from fractions import Fraction as F
import math
import random

results = []


def check(cid, desc, cond):
    results.append((cid, desc, bool(cond)))
    print(("PASS" if cond else "FAIL"), cid, desc)


def sgn(x):
    return (x > 0) - (x < 0)


random.seed(1)
GRID = [F(n, 2) for n in range(-12, 13)]
PTS = [(a, b) for a in GRID for b in GRID]
PTS += [(F(random.randint(-900, 900), random.randint(1, 50)),
         F(random.randint(-900, 900), random.randint(1, 50))) for _ in range(3000)]

S = lambda p: p[0] + p[1]
D = lambda p: p[0] - p[1]
sig = lambda p: (p[1], p[0])
nu = lambda p: (-p[0], -p[1])
signu = lambda p: (-p[1], -p[0])
mub = lambda p: (p[0], -p[1])

# C-63
check("C63", "s=a+b, d=a−b: a=(s+d)/2, b=(s−d)/2; при b=−a сумма s=0 (синтез противоположностей не сумма)",
      all((S(p) + D(p)) / 2 == p[0] and (S(p) - D(p)) / 2 == p[1] for p in PTS)
      and all(S((a, -a)) == 0 for a in GRID))

# C-64
fix = lambda g: [p for p in PTS if g(p) == p]
check("C64", "V4: Fix(σ)=диагональ a=b, Fix(σν)=антидиагональ a=−b, Fix(ν)={(0,0)}; на антидиагонали σ=ν",
      all(p[0] == p[1] for p in fix(sig)) and all(p[0] == -p[1] for p in fix(signu))
      and set(fix(nu)) == {(F(0), F(0))} and all(sig((a, -a)) == nu((a, -a)) for a in GRID))


def ptype(f, g):
    out = set()
    for p in PTS:
        v, w = f(p), f(g(p))
        if v == 0:
            continue
        out.add('even' if v == w else ('odd' if v == -w else 'none'))
    return out


def char(f):
    return [ptype(f, g) for g in (sig, nu, signu)]


E, O = {'even'}, {'odd'}
check("C65", "Типы чётности (σ,ν,σν): s=(чёт,нечёт,нечёт), d=(нечёт,нечёт,чёт), s·d=(нечёт,чёт,нечёт); |s|,|d|,ab инвариантны",
      char(S) == [E, O, O] and char(D) == [O, O, E] and char(lambda p: S(p) * D(p)) == [O, E, O]
      and all(char(f) == [E, E, E] for f in (lambda p: abs(S(p)), lambda p: abs(D(p)), lambda p: p[0] * p[1])))

# C-66
check("C66", "Анти-форма одного объекта μ_b: b↦−b меняет каналы местами s↔d; a+b = a−(−b)",
      all(S(mub(p)) == D(p) and D(mub(p)) == S(p) for p in PTS))

# C-67
orbit = lambda p: {p, sig(p), nu(p), signu(p)}
GP = [(a, b) for a in GRID for b in GRID]
fib = {}
for p in GP:
    fib.setdefault((abs(S(p)), abs(D(p))), set()).add(p)
check("C67", "(|a+b|,|a−b|) — полный инвариант орбит V4 (в общем положении 4 точки = 2 бита); расстояние до прямой через 0 инвариантно при ν",
      all(f == orbit(next(iter(f))) for f in fib.values())
      and all(len(orbit(p)) == 4 for p in GP if p[0] != p[1] and p[0] != -p[1])
      and all(abs(al * p[0] + be * p[1]) == abs(al * nu(p)[0] + be * nu(p)[1])
              for p in PTS for al, be in ((1, 0), (0, 1), (1, 2))))

# C-68
NS = {"t": (lambda t: t, 2), "|t|": (abs, 2), "t²": (lambda t: t * t, 4)}
closed = {"t": lambda a, b: b, "|t|": lambda a, b: sgn(a) * sgn(b) * min(abs(a), abs(b)), "t²": lambda a, b: a * b}
ok = True
for k, (N, c) in NS.items():
    P = lambda a, b, N=N, c=c: (N(a + b) - N(a - b)) / c
    ok &= all(P(a, b) == closed[k](a, b) for a, b in PTS)
    ok &= all(P(x, x) == N(x) and P(x, -x) == -N(x) for x in GRID)
    ok &= all(P(a, -b) == -P(a, b) for a, b in PTS)
    ok &= P(F(1), F(1)) == 1
check("C68", "P_N=[N(a+b)−N(a−b)]/c, N∈{t,|t|,t²}: =b, sign(a)sign(b)min(|a|,|b|), ab; на a=b: x,|x|,x²; на a=−b: −x,−|x|,−x²; P_N(a,−b)=−P_N(a,b); P_N(1,1)=1", ok)

# C-69
check("C69", "На знаковых битах {−1,0,1}: sign(a)sign(b)min(|a|,|b|)=ab (min = произведение = ∧); вне битов различаются (a=b=2: 2 против 4)",
      all(sgn(a) * sgn(b) * min(abs(a), abs(b)) == a * b for a in (-1, 0, 1) for b in (-1, 0, 1))
      and sgn(2) * sgn(2) * min(2, 2) == 2 and 2 * 2 == 4)

# C-70
check("C70", "ab=((a+b)²−(a−b)²)/4, a²+b²=((a+b)²+(a−b)²)/2; sign(ab)=sign(|a+b|−|a−b|); ab=0 ⟺ |a+b|=|a−b|",
      all(p[0] * p[1] == (S(p) ** 2 - D(p) ** 2) / 4 and p[0] ** 2 + p[1] ** 2 == (S(p) ** 2 + D(p) ** 2) / 2
          and sgn(p[0] * p[1]) == sgn(abs(S(p)) - abs(D(p)))
          and (p[0] * p[1] == 0) == (abs(S(p)) == abs(D(p))) for p in PTS))

# C-71
mx = lambda u, v: (u + v + abs(u - v)) / 2
mn = lambda u, v: (u + v - abs(u - v)) / 2
check("C71", "Невязки p=|a−b|, q=|a+b|: «оба выполнены» (p+q+|p−q|)/2=0 ⟺ a=b=0; «одно из» (p+q−|p−q|)/2=0 ⟺ |a|=|b|",
      all((mx(abs(D(p)), abs(S(p))) == 0) == (p == (0, 0)) and
          (mn(abs(D(p)), abs(S(p))) == 0) == (abs(p[0]) == abs(p[1])) for p in PTS))

# C-72
check("C72", "Крест: |y|=|x| ⟺ y²=x² ⟺ (y−x)(y+x)=0; график y=|x| — верхняя половина креста; при x≠0 на вертикали две точки креста, функция берёт одну",
      all((abs(y) == abs(x)) == (y * y == x * x) == ((y - x) * (y + x) == 0) for x, y in PTS)
      and all(abs(abs(x)) == abs(x) for x in GRID)
      and all(len({y for y in (x, -x)}) == 2 for x in GRID if x != 0))

# C-73
check("C73", "(−|x|)·(−|x|) = |x|·|x| = x² (агрегат не различает повтор выбора и повтор удержания); |x|·(−|x|) = −x² (форма У7)",
      all((-abs(x)) * (-abs(x)) == abs(x) * abs(x) == x * x and abs(x) * (-abs(x)) == -x * x for x in GRID))

# C-74
roots_sq = [x for x in range(-10, 11) if x * x == x + 2]
real = [x for x in roots_sq if x + 2 >= 0 and math.isqrt(x + 2) ** 2 == x + 2 and math.isqrt(x + 2) == x]
anti = [x for x in roots_sq if x + 2 >= 0 and math.isqrt(x + 2) ** 2 == x + 2 and -math.isqrt(x + 2) == x]
check("C74", "√(x+2)=x: квадрат даёт {2,−1}; проверка подстановкой оставляет 2; −1 решает анти-уравнение −√(x+2)=x",
      sorted(roots_sq) == [-1, 2] and real == [2] and anti == [-1])

# C-75
ok = all(((B >= 0 and B * B == A) == (B * abs(B) == A)) for A in range(0, 40) for B in range(-7, 8))
ok &= all((-x) * abs(-x) == -(x * abs(x)) for x in GRID)            # x|x| нечётна
ok &= all(x ** 3 == x * x * x and sgn(x ** 3) == sgn(x) for x in GRID)  # У9: знак восстановлен
ok &= all((x + 2) ** 2 == x ** 4 for x in (-1, 2))                    # повторный квадрат лишний корень не убирает
ok &= ((-1) * abs(-1) != -1 + 2) and (2 * abs(2) == 2 + 2)          # B|B|=A отсекает −1 без проверки
check("C75", "Равносильный переход: при A≥0 √A=B ⟺ (A=B², B≥0) ⟺ B·|B|=A; x|x| нечётна, sign(x³)=sign(x); (x+2)²=x⁴ держит и −1", ok)

# C-76
check("C76", "Честное обращение У8: y²=|x| ⟺ y⁴=x² — две ветви ±√|x|; y=√|x| берёт одну (главную)",
      all((y * y == abs(x)) == (y ** 4 == x * x) for x in GRID for y in GRID)
      and all(len({y for y in GRID if y * y == abs(x)}) == 2 for x in (F(1), F(4), F(9, 4))))

n_pass = sum(r[2] for r in results)
print(f"\nИТОГ: {n_pass} PASS / {len(results) - n_pass} FAIL")

if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(results) else 1)
