# -*- coding: utf-8 -*-
"""
probes.py — прогон ВСЕХ кандидат-проб одной командой.

Это НЕ verification.py. Сьют — печать статьи («59 PASS = каждое формальное
утверждение статьи имеет машинного свидетеля»); его FAIL отзывает статус
formal_math_fact. Здесь — свидетели КАНДИДАТНЫХ утверждений из заметок
(candidate/analogy_only): их PASS ничего не повышает, их FAIL ничего у статьи
не отзывает, а означает «кандидат-проба сломалась» → строка в work/REFUTED.md
+ разбор в заметке-источнике.

Политика (П1, вариант A, DECISIONS 2026-07-04): проба переезжает в
verification.py как C-NN ТОЛЬКО когда её утверждение фолдится в статью через
К1–К5. Сьют растёт вслед за статьёй, не впереди неё.

Источники (этот файл — канонная исполняемая копия; в заметках — исторические
версии на дату прогона):
  H-4…H-col   — half_hypothesis.md §4  (колонка неопределённости)
  S-1…S-7     — half_hypothesis.md §7  (сборка ℂ)
  T-1…T-3     — topo_chi_note.md §1    (χ_E-слой; впервые реализованы здесь)
  P-1…P-4     — topo_chi_note.md §3    (Эйлер/шнуровка/Пик/DFT)
  CLT-1…CLT-5 — clt_u6_note.md §5      (там названы C-1…C-5; здесь переименованы,
                                        чтобы не путать с C-NN сьюта)

Запуск: python -X utf8 work/v14_rebuild/probes.py    (exit 0 ⟺ все PASS)
"""
import sys
from math import gcd

import numpy as np
import sympy as sp
from sympy import (Abs, Eq, I, Rational, S, cos, exp, pi, sign, simplify,
                   sin, solveset, sqrt, symbols)

SEED = 20260704
rng = np.random.default_rng(SEED)
RESULTS = []


def run(pid, source, desc, fn):
    try:
        ok = bool(fn())
    except Exception as e:  # проба, падающая исключением, тоже FAIL
        ok = False
        desc += f"  [EXC: {e}]"
    RESULTS.append((pid, source, desc, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {pid:7s} [{source}] {desc}")


# ----------------------------------------------------------------- H (колонка)
x, y, t = symbols('x y t', real=True)
rr = symbols('rr', positive=True)
th = symbols('th', real=True)

run("H-4", "half_hyp §4", "У4 |x|=2 → две веществ. ветви {−2,2} (знак открыт, в ℝ)",
    lambda: solveset(Eq(Abs(x), 2), x, S.Reals) == sp.FiniteSet(-2, 2))
run("H-8a", "half_hyp §4", "У8: обратить квадрат при <0 → нет веществ. корня",
    lambda: solveset(Eq(t**2, -1), t, S.Reals) == S.EmptySet)
run("H-8b", "half_hyp §4", "i — полуповорот: i²=−1, (e^{iπ/2})²=−1",
    lambda: simplify(I**2 + 1) == 0 and simplify(exp(I * pi / 2)**2 + 1) == 0)
run("H-8c", "half_hyp §4", "√ делит фазу: (√r·e^{iθ/2})² = r·e^{iθ}",
    lambda: simplify((sqrt(rr) * exp(I * th / 2))**2 - rr * exp(I * th)) == 0)
run("H-12", "half_hyp §4", "У12: при x=0 два y {0,4} — отношение, не функция",
    lambda: solveset(Eq(0**2 + (y - 2)**2 - 4, 0), y, S.Reals) == sp.FiniteSet(0, 4))
run("H-res", "half_hyp §4", "У9: куб возвращает знак (sign(v³)=sign(v))",
    lambda: all(sign(v**3) == sign(v) for v in (-2, -1, 1, 2)))
run("H-u8", "half_hyp §4", "У8 — единственная дробная ступень: √|x| = |x|^(1/2)",
    lambda: simplify(sqrt(Abs(x)) - Abs(x)**Rational(1, 2)) == 0)
run("H-col", "half_hyp §4", "колонка = node+1 = {0,4,8,12}, шаг +4",
    lambda: [n + 1 for n in (-1, 3, 7, 11)] == [0, 4, 8, 12])

# ----------------------------------------------------------------- S (сборка ℂ)
run("S-1", "half_hyp §7", "Z/2: веществ. корни единицы x²=1 → {±1}",
    lambda: solveset(Eq(x**2, 1), x, S.Reals) == sp.FiniteSet(-1, 1))
run("S-2", "half_hyp §7", "i=√(зеркала): i²=−1, i⁴=1 (Z/4), i вне ℝ",
    lambda: simplify(I**2 + 1) == 0 and simplify(I**4 - 1) == 0
    and solveset(Eq(x**2, -1), x, S.Reals) == S.EmptySet)
run("S-3", "half_hyp §7", "exp оборачивает ℝ на окружность: |e^{it}|=1",
    lambda: simplify(Abs(exp(I * t)) - 1) == 0)
run("S-4", "half_hyp §7", "Эйлер: e^{it} = cos t + i·sin t (мост)",
    lambda: simplify(exp(I * t) - (cos(t) + I * sin(t))) == 0)
run("S-5", "half_hyp §7", "круг У12 = сдвинутый образ e^{it}",
    lambda: simplify((2 * cos(t))**2 + (2 + 2 * sin(t) - 2)**2 - 4) == 0)
run("S-6", "half_hyp §7", "вложение Z/2 ⊂ Z/4 (⊂ U(1))",
    lambda: {1, -1} <= {1, I, -1, -I})
run("S-7", "half_hyp §7", "самоподобие: ветвь круга = знак параметра t (±t — тот же x)",
    lambda: simplify(2 * cos(t) - 2 * cos(-t)) == 0
    and simplify(2 * sin(t) + 2 * sin(-t)) == 0)

# ----------------------------------------------------------------- T (χ_E-слой)
def t1():
    # всякое R∈SO(3) имеет собственное значение 1 → ось → 2 неподвижные точки на S²
    for _ in range(3):
        a = rng.normal(size=3); a /= np.linalg.norm(a)
        ang = rng.uniform(0.2, 3.0)
        K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
        R = np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)
        if abs(np.linalg.det(R) - 1) > 1e-9:
            return False
        if np.linalg.norm(R @ a - a) > 1e-9 or np.linalg.norm(R @ (-a) + a) > 1e-9:
            return False  # ось ±a неподвижна (два антипода)
        if min(abs(np.linalg.eigvals(R) - 1)) > 1e-9:
            return False
    return True
run("T-1", "topo_chi §1", "сфера: любое вращение SO(3) держит ось (2 неподвижные точки, χ_E=2)", t1)

def t2():
    # сдвиг тора (x,y)→(x+a,y+b) mod 1, (a,b)∉Z² — неподвижных точек НЕТ (χ_E=0)
    pts = rng.random((200, 2))
    d = np.abs((pts + np.array([0.3, 0.7])) % 1.0 - pts)
    d = np.minimum(d, 1 - d)          # тор-метрика
    free = float(d.max(axis=1).min()) > 1e-9
    d0 = np.abs((pts + np.array([0.0, 0.0])) % 1.0 - pts).max()
    return free and d0 < 1e-12        # контраст: нулевой сдвиг фиксирует всё
run("T-2", "topo_chi §1", "тор: сдвиг свободен (нет неподвижных точек) — циклич. сдвиг возможен при χ_E=0", t2)

def t3():
    one_zero = solveset(x**2, x, S.Reals) == sp.FiniteSet(0)
    cos_lattice = (sp.cos(pi / 2) == 0 and sp.cos(3 * pi / 2) == 0
                   and not isinstance(solveset(cos(x), x, S.Reals), sp.FiniteSet))
    exp_none = solveset(exp(x), x, S.Reals) == S.EmptySet
    return one_zero and cos_lattice and exp_none
run("T-3", "topo_chi §1", "классы нулей [ADD_TOPO_INVARIANTS]: x² один · cos решётка · eˣ ни одного [C-19]", t3)

# ----------------------------------------------------------------- P (считывания)
f_ = symbols('f', real=True)
run("P-1", "topo_chi §3", "Эйлер с частотой: e^{i2πft} = cos+i·sin",
    lambda: simplify(exp(2 * I * pi * f_ * t) - cos(2 * pi * f_ * t)
                     - I * sin(2 * pi * f_ * t)) == 0)

def shoelace(pts):
    xa = np.array([p[0] for p in pts], float)
    ya = np.array([p[1] for p in pts], float)
    return 0.5 * np.sum(xa * np.roll(ya, -1) - np.roll(xa, -1) * ya)

run("P-2", "topo_chi §3", "шнуровка Гаусса: площадь знаковая, знак = ориентация обхода",
    lambda: shoelace([(0, 0), (3, 0), (3, 3), (0, 3)]) == 9
    and shoelace([(0, 3), (3, 3), (3, 0), (0, 0)]) == -9)

def p3():
    def on_seg(p, a, b):
        cr = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        return (cr == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
                and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))

    def interior(poly, N=12):
        c = 0
        for X in range(-N, N + 1):
            for Y in range(-N, N + 1):
                if any(on_seg((X, Y), poly[i], poly[(i + 1) % len(poly)])
                       for i in range(len(poly))):
                    continue
                ins = False
                for i in range(len(poly)):
                    (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
                    if (y1 > Y) != (y2 > Y) and X < x1 + (Y - y1) * (x2 - x1) / (y2 - y1):
                        ins = not ins
                c += ins
        return c

    for poly in ([(0, 0), (4, 0), (0, 4)], [(0, 0), (3, 0), (3, 3), (0, 3)]):
        A = abs(shoelace(poly))
        B = sum(gcd(abs(poly[(i + 1) % len(poly)][0] - poly[i][0]),
                    abs(poly[(i + 1) % len(poly)][1] - poly[i][1]))
                for i in range(len(poly)))
        if A != interior(poly) + B / 2 - 1:
            return False
    return True
run("P-3", "topo_chi §3", "Пик: A = I + B/2 − 1 (поправка −1 = −χ_E)", p3)

def p4():
    N = 4
    F = np.array([[np.exp(-2j * np.pi * j * k / N) for k in range(N)] for j in range(N)])
    Sh = np.roll(np.eye(N), 1, axis=0)
    D = F @ Sh @ np.linalg.inv(F)
    offdiag = np.max(np.abs(D - np.diag(np.diag(D))))
    eig = set(np.round(np.diag(D), 6))
    return offdiag < 1e-9 and eig == {1 + 0j, -1 + 0j,
                                      np.round(-1j, 6), np.round(1j, 6)}
run("P-4", "topo_chi §3", "DFT диагонализует циклич. сдвиг; собств. числа = корни единицы Z/4", p4)

# ----------------------------------------------------------------- CLT (У6)
def skew_kurt(v):
    v = (v - v.mean()) / v.std()
    return float((v**3).mean()), float((v**4).mean() - 3)

run("CLT-1", "clt_u6 §5", "Гаусс = неподвижная точка Agg+масштаб (хар. функция)",
    lambda: simplify(sp.exp(-t**2 / 2).subs(t, t / sp.sqrt(2))**2
                     - sp.exp(-t**2 / 2)) == 0)

def clt2():
    s = rng.exponential(1, size=(80000, 64)).sum(axis=1)
    g1, g2 = skew_kurt(s)
    return abs(g1 - 2 / 8) < 0.06 and abs(g2 - 6 / 64) < 0.09
run("CLT-2", "clt_u6 §5", "скорости стирания выше-x²: skew≈2/√n, kurt−3≈6/n (n=64)", clt2)

def clt3():
    for smp in (lambda sz: rng.uniform(0, 1, sz),
                lambda sz: rng.integers(0, 2, sz).astype(float),
                lambda sz: rng.exponential(1, sz)):
        g1, g2 = skew_kurt(smp((40000, 256)).sum(axis=1))
        if abs(g1) > 0.2 or abs(g2) > 0.2:
            return False
    return True
run("CLT-3", "clt_u6 §5", "универсальность (тотализация): 3 разных источника → один аттрактор", clt3)

def clt4():
    for n in (1, 100):
        m = rng.standard_cauchy((80000, n)).mean(axis=1)
        iqr = float(np.subtract(*np.percentile(m, [75, 25])))
        if not (1.8 < iqr < 2.2):
            return False
    return True
run("CLT-4", "clt_u6 §5", "defeat: Коши (нет V·V) — агрегат НЕ сжимается (IQR≈2 при любом n)", clt4)

def clt5():
    p_stay, N, n_blk = 0.9, 1_000_000, 1000
    lam = 2 * p_stay - 1
    flip = (rng.random(N) >= p_stay)
    flip[0] = False
    xs = (np.cumsum(flip) % 2).astype(float)
    r1 = float(np.corrcoef(xs[:-1], xs[1:])[0, 1])
    blocks = xs.reshape(-1, n_blk).sum(axis=1)
    g1, g2 = skew_kurt(blocks)
    nvar = float(n_blk * blocks.var() / n_blk**2)
    theo = 0.25 * (1 + lam) / (1 - lam)
    return (abs(r1 - lam) < 0.02 and abs(xs.mean() - 0.5) < 0.02
            and abs(g1) < 0.12 and abs(g2) < 0.2 and abs(nvar - theo) < 0.4)
run("CLT-5", "clt_u6 §5", "поправка Маркова: зависимость (λ=0.8) — аттрактор тот же; след связи = один V·V-скаляр", clt5)

# ----------------------------------------------------------------- итог
n_pass = sum(1 for r in RESULTS if r[3])
n_fail = len(RESULTS) - n_pass
print(f"\nИТОГ: {n_pass} PASS / {n_fail} FAIL (всего {len(RESULTS)}; кандидат-пробы, НЕ сьют)")
if n_fail:
    print("FAIL кандидат-пробы = строка в work/REFUTED.md + разбор в заметке-источнике.")
sys.exit(0 if n_fail == 0 else 1)
