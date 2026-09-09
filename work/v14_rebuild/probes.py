# -*- coding: utf-8 -*-
"""
probes.py — прогон ВСЕХ кандидат-проб одной командой.

Это НЕ verification.py. Сьют — печать статьи («62 PASS = каждое формальное
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
  PAR-1…PAR-4 — ladder_table.md §отражение / DECISIONS 2026-06-17 («минус из
                равенства»: чётные регенерируют ±, нечётные выносят знак)
  T-1…T-3     — topo_chi_note.md §1    (χ_E-слой; впервые реализованы здесь)
  XE-1…XE-3   — topo_chi_note.md §1/§4 (инстансы Пуанкаре–Хопфа: классы нулей ↔ χ_E)
  P-1…P-4     — topo_chi_note.md §3    (Эйлер/шнуровка/Пик/DFT)
  CLT-1…CLT-5 — clt_u6_note.md §5      (там названы C-1…C-5; здесь переименованы,
                                        чтобы не путать с C-NN сьюта)
  QG-1…QG-3   — questiongain_criterion.md (гейт O_14 + worked-neg/pos)
  MIR-1…5, SEQ-1…4 — ФОЛДНУТЫ в сьют как C-60…C-62 (2026-07-05, статья §8.1б);
                                        первый рост сьюта по политике П1
  VIETA-1…5   — ladder_table.md §«Виета» (2026-07-09: [внешняя] теорема Виета
                → законы полосы 6→7→8; бит ветви — инстанс к oq-d11)
  SHADOW-1…5  — shadow_lemma.md (2026-07-09: лемма о нижней тени — карта П5;
                Z/2-разложение тень+бит, тень = инварианты Tot)
  EXT15-1…3   — external_bridge_u1_u5.md (2026-08-02: фактор |x|, секции
                представителей и конечная модель условной энтропии; [внешнее])

Запуск: python -X utf8 work/v14_rebuild/probes.py    (exit 0 ⟺ все PASS)
"""
import sys
from itertools import product
from math import gcd, log2

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

# ----------------------------------------------------- PAR («минус из равенства»)
def par1():
    even_samples = [(Abs(x), 2), (x**2, 2), (-x**2, 2), (sqrt(Abs(x)), 4), (cos(x), pi / 3)]
    for F, a in even_samples:
        if simplify(F.subs(x, -x) - F) != 0:          # чётность
            return False
        c = F.subs(x, a)                               # регенерация ±:
        if simplify(F.subs(x, -a) - c) != 0:           # F(a)=c ⟹ F(−a)=c
            return False
    return True
run("PAR-1", "DEC 06-17", "чётные формы: F(−x)=F(x) и уравнение F(x)=c регенерирует ±-пару", par1)

def par2():
    for F in (x, -x, x**3):
        if simplify(F.subs(x, -x) + F) != 0:           # нечётность: минус выносится
            return False
    return (solveset(Eq(x**3, 8), x, S.Reals) == sp.FiniteSet(2)          # пары НЕТ,
            and solveset(Eq(-x, 3), x, S.Reals) == sp.FiniteSet(-3))      # знак сохранён
run("PAR-2", "DEC 06-17", "нечётные формы: F(−x)=−F(x), знак проходит насквозь (x³=8→{2})", par2)

def par3():
    pairs = (solveset(Eq(x**2, 4), x, S.Reals) == sp.FiniteSet(-2, 2)
             and solveset(Eq(Abs(x), 2), x, S.Reals) == sp.FiniteSet(-2, 2))
    collapse = (solveset(Eq(x**2, 0), x, S.Reals) == sp.FiniteSet(0)
                and solveset(Eq(Abs(x), 0), x, S.Reals) == sp.FiniteSet(0))
    return pairs and collapse
run("PAR-3", "DEC 06-17", "±-пара живёт при c≠0 и схлопывается ровно на нулевой границе [SP_ZERO]", par3)

def par4():
    neither = (simplify(exp(-x) - exp(x)) != 0 and simplify(exp(-x) + exp(x)) != 0)
    sol = solveset(Eq(exp(x), 5), x, S.Reals) == sp.FiniteSet(sp.log(5))
    no_mirror = simplify(exp(-sp.log(5)) - 5) != 0     # у решения нет зеркального партнёра
    return neither and sol and no_mirror
run("PAR-4", "DEC 06-17", "eˣ вне механизма зеркала: ни регенерации, ни выноса (своя ориентация [C-21])", par4)

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

# -------------------------------------------------- XE (классы нулей ↔ χ_E, #40)
def xe1():
    # поле вращения w(p)=a×p на сфере: нули ровно ±a; индекс каждого = winding = +1
    a = np.array([0., 0., 1.]); u = np.array([1., 0., 0.]); v = np.array([0., 1., 0.])
    if np.linalg.norm(np.cross(a, a)) != 0 or np.linalg.norm(np.cross(a, -a)) != 0:
        return False
    winds = []
    for sgn in (+1.0, -1.0):
        eps, s = 0.1, np.linspace(0, 2 * np.pi, 721)
        p = (np.cos(eps) * sgn) * a[None, :] + np.sin(eps) * (
            np.cos(s)[:, None] * u + np.sin(s)[:, None] * v)
        w = np.cross(np.broadcast_to(a, p.shape), p)
        ang = np.unwrap(np.arctan2(w @ v, w @ u))
        winds.append((ang[-1] - ang[0]) / (2 * np.pi))
    return all(abs(w - 1) < 1e-6 for w in winds) and round(sum(winds)) == 2
run("XE-1", "topo_chi #40", "сфера: поле a×p — 2 нуля (±ось) индекса +1, сумма 2 = χ_E(S²) [инстанс П.–Хопфа]", xe1)

def xe2():
    ok_zeros = (sp.cos(pi / 2) == 0 and sp.cos(3 * pi / 2) == 0)   # решётка канона на S¹
    idx = [int(sp.sign(-sin(z))) for z in (pi / 2, 3 * pi / 2)]    # индекс 1D-нуля = sign(f')
    const_free = solveset(Eq(S.One, 0), x, S.Reals) == S.EmptySet  # беснулевое поле есть
    return ok_zeros and sorted(idx) == [-1, 1] and sum(idx) == 0 and const_free
run("XE-2", "topo_chi #40", "окружность: cos-поле — индексы −1/+1, сумма 0 = χ_E(S¹); класс eˣ (без нулей) ⟺ χ_E=0", xe2)

run("XE-3", "topo_chi #40", "χ_E комбинаторно: октаэдр(S²) 6−12+8=2 · клетка тора 1−2+1=0",
    lambda: (6 - 12 + 8 == 2) and (1 - 2 + 1 == 0))

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

# ------------------------------------------- QG (критерий QuestionGain / O_14)
# Гейт (операциональная форма defeat-клаузы [O_14] + «различающий ход»
# [clt_u6_note §4]): чтение R, претендующее на «роль сверх переописания null X»,
# проходит ⟺ есть ход m, ВЫВОДИМЫЙ из R и НЕ воспроизводимый из X при РАВНОЙ цене.
# Воспроизводим при равной цене ⇒ основание падает (analogy_only, не уровень/роль).
def qg_gate(move_derivable_from_R, move_reproducible_from_null_at_equal_cost):
    return bool(move_derivable_from_R) and not bool(move_reproducible_from_null_at_equal_cost)


def qg1():
    # структура гейта = таблица истинности; PASS только в клетке (ход есть, не воспроизводим)
    tbl = {(d, r): qg_gate(d, r) for d in (False, True) for r in (False, True)}
    return (tbl[(True, False)] is True and tbl[(True, True)] is False
            and tbl[(False, False)] is False and tbl[(False, True)] is False)
run("QG-1", "clt_u6 §4/O_14", "гейт QuestionGain = defeat-клауза O_14 (воспроизводим при равной цене → падает)", qg1)


def qg2():
    # worked NEGATIVE (форма D2/o20): null X=|a| (модуль); R добавляет sign(a).
    # y зависит ТОЛЬКО от |a| ⇒ при данном |a| знак не различает y ⇒ ход воспроизводим
    # при равной цене ⇒ QG-fail (ровно информационная эквивалентность D2).
    rng2 = np.random.default_rng(SEED)
    a = rng2.normal(size=40000)
    y = (a * a > 1.0).astype(float)
    s = np.sign(a); hi = np.abs(a) > 1.0
    p_pos = float(y[hi & (s > 0)].mean()); p_neg = float(y[hi & (s < 0)].mean())
    reproducible = abs(p_pos - p_neg) < 0.02 and p_pos > 0.99   # знак не даёт различения
    return reproducible and qg_gate(True, reproducible) is False
run("QG-2", "clt_u6 §4", "worked-neg D2: sign реконструируем из |·| при равной цене → QG-fail (analogy_only)", qg2)


def qg3():
    # worked POSITIVE (форма Марков–Некрасов): null «регулярность ⇒ независимость».
    # Ход = зависимая семья (lag-1 corr≠0) с ТОЙ ЖЕ регулярностью (среднее сходится):
    # null такое запрещает ⇒ не воспроизводим ⇒ QG-pass. Тип хода выведен из типа ошибки.
    rng2 = np.random.default_rng(SEED)
    N = 200000
    flip = rng2.random(N) >= 0.9; flip[0] = False
    xs = (np.cumsum(flip) % 2).astype(float)
    lag1 = float(np.corrcoef(xs[:-1], xs[1:])[0, 1])
    same_regularity = abs(xs.mean() - 0.5) < 0.02
    null_forbids = abs(lag1) > 0.2                 # зависимость null не воспроизводит
    move_derivable = same_regularity and null_forbids
    return move_derivable and qg_gate(True, not null_forbids) is True
run("QG-3", "clt_u6 §3-4", "worked-pos Марков: зависимая семья с той же регулярностью — ход не воспроизводим → QG-pass", qg3)

# --------------------------- MIR / SEQ: ФОЛДНУТЫ В СЬЮТ (2026-07-05)
# Пробы MIR-1…MIR-5 (ориентация ≠-отражения) и SEQ-1…SEQ-4 (режимы
# последовательного запрета) переехали в verification.py как C-60…C-62 —
# событие фолда их утверждения в статью (FTS_v14_paper.md §8.1б) по политике
# П1 (DECISIONS 2026-07-04 (4)): сьют растёт вслед за статьёй. Исторические
# версии проб — в git (коммиты 7545a9d, f295c45); разбор — ladder_table.md
# §«Ориентация отражения» и §«Режимы последовательного запрета».

# ------------------------------------------ VIETA (нижняя тень пары корней)
# [внешнее: теорема Виета — в каноне НЕТ] Перевод на записанные законы (разбор —
# ladder_table.md §«Виета», 2026-07-09, авторский вопрос «связано ли условие
# неприменимости Виеты с 6→7?»). Ядро: агрегаты пары корней e₁=r₁+r₂, e₂=r₁·r₂
# (Agg, Ч-регистр) слепы к ветви √D; школьное «D<0 — применять нельзя» склеивает
# два режима §8.1б: (x+p/2)²=D/4 при D<0 падает в образ анти-формы −x² (зеркало
# 6→7, C-60), а вопрос ветви теряет ℝ-носителя (вырождение 7→8, C-61 deg78) —
# разрешение не запрет, а Lift → У8 (i). D=(r₁−r₂)² = V·V пары [паттерн C-61
# deg56]; D=0 — нулевая граница пары [SP_ZERO; ср. PAR-3]; при D<0 Виета жива
# каналами: e₂=|z|² (Q), e₁=2·Re. Гардрейл: школьный D ≠ «дискриминант» C-59
# (единичная граница — внутренний термин v14, не смешивать).
p_v, q_v = symbols('p_v q_v', real=True)
D_v = p_v**2 - 4*q_v
vr1 = (-p_v + sqrt(D_v)) / 2   # ветвь +
vr2 = (-p_v - sqrt(D_v)) / 2   # ветвь −
w_v = symbols('w_v')           # без assumptions — для solveset в ℂ


def vieta1():
    # агрегаты пары не зависят от ветви: e1=−p (√D сокращается), e2=q (√D входит квадратом)
    return (simplify(vr1 + vr2 + p_v) == 0
            and simplify(vr1 * vr2 - q_v) == 0)
run("VIETA-1", "ladder_table §Виета", "агрегаты пары корней = −p, q — Agg-считывание слепо к ветви", vieta1)


def vieta2():
    # дискриминант = квадрат разности корней = «V·V пары» [C-61 deg56-паттерн];
    # дисперсия двухточечного носителя {r1,r2} = D/4 — в ℝ обязана быть ≥0 ⇒ D<0 = ℝ-пары нет
    m = (vr1 + vr2) / 2
    var = ((vr1 - m)**2 + (vr2 - m)**2) / 2
    return (simplify((vr1 - vr2)**2 - D_v) == 0
            and simplify(var - D_v / 4) == 0)
run("VIETA-2", "C-61 deg56-паттерн", "D = (r₁−r₂)² = V·V пары корней; дисперсия пары = D/4", vieta2)


def vieta3():
    # D=0 ⟺ r1=r2 — пара схлопнулась в двойной корень: нулевая граница ПАРЫ
    return simplify((vr1 - vr2).subs(q_v, p_v**2 / 4)) == 0
run("VIETA-3", "SP_ZERO/PAR-3", "D=0: пара корней схлопывается (двойной корень) — нулевая граница пары", vieta3)


def vieta4():
    # D<0 (пример x²+2x+2, D=−4): (x+1)²=−1 — правая часть в образе анти-формы −x²
    # (зеркало 6→7, C-60), в ℝ носителя нет (C-61 deg78: t²=−1→∅); в ℂ пара
    # сопряжённая (сопряжение = ветвевое зеркало) и Виета перечитывается каналами:
    # z·z̄ = q = |z|² (Q-канал), z+z̄ = −p = 2·Re
    z = -1 + I
    return (solveset(Eq(x**2 + 2*x + 2, 0), x, S.Reals) == S.EmptySet
            and solveset(Eq(x**2, -1), x, S.Reals) == S.EmptySet             # форма У6 не достигает
            and solveset(Eq(-x**2, -1), x, S.Reals) == sp.FiniteSet(-1, 1)   # анти-форма У7 достигает
            and solveset(Eq(w_v**2 + 2*w_v + 2, 0), w_v, S.Complexes) == sp.FiniteSet(-1 - I, -1 + I)
            and simplify(z * sp.conjugate(z) - 2) == 0                       # e₂ = |z|²
            and simplify(z + sp.conjugate(z) + 2) == 0)                      # e₁ = 2·Re
run("VIETA-4", "C-60/C-61/Q-канал", "D<0: вопрос в образе −x², в ℝ ∅; в ℂ Виета = каналы |z|² и 2·Re", vieta4)


def vieta5():
    # бит ветви невосстановим из агрегатов: смена ветви √D→−√D ОБМЕНИВАЕТ корни,
    # но (e₁,e₂) неизменны — worked-инстанс к oq-d11-branch-bit-test (аналог урока D2:
    # знак из |x| не вернёшь при равной цене)
    sw = {sqrt(D_v): -sqrt(D_v)}
    e1, e2 = vr1 + vr2, vr1 * vr2
    return (simplify(vr1.subs(sw) - vr2) == 0             # подстановка нетривиальна: r1↔r2
            and simplify(e1.subs(sw) - e1) == 0
            and simplify(e2.subs(sw) - e2) == 0)
run("VIETA-5", "oq-d11/урок D2", "бит ветви (какой корень) невосстановим из симметричных агрегатов", vieta5)

# ------------------------------------ SHADOW (лемма о нижней тени — карта П5)
# shadow_lemma.md (2026-07-09). Носитель — зеркальная пара с инволюцией σ (Z/2:
# обмен ветви / x↦−x / сопряжение). Любой функционал f разлагается единственно
# f = f_sym + f_anti; ТЕНЬ f_sym выражается через Agg-агрегаты пары ([внешнее:
# симметрические функции]; ФТС-чтение: тень = инварианты коллапса Tot Z/2→{1}
# [лемма Tot]); БИТ: f_anti кратна разности (±√D / 2x / 2i·Im z) — ровно один
# бит поверх тени при f_anti!=0 на данной орбите; КВАДРАТ: f_anti² — снова тень,
# для базовой разности это D = V·V пары [C-61 deg56]. Диагональ r₁=r₂ даёт нуль,
# но у детектора бывают дополнительные нули (EC-005/NC-04; SP_ZERO не меняется).
# Следствие-гейт (сцепка с QG [O_14]): различающий ход канала
# бита (Д11) может жить ТОЛЬКО в f_anti. Гардрейл: Z/2 ≠ U(1) (Rot ≠ −) —
# непрерывное содержание фазы Д10 лемма НЕ покрывает, только её дискретный след.
r1_, r2_ = symbols('r1 r2', real=True)
_f = r1_**2 * r2_ + 3*r1_                       # произвольный несимметричный функционал пары
_swap = {r1_: r2_, r2_: r1_}
_fs = (_f + _f.subs(_swap, simultaneous=True)) / 2   # тень
_fa = (_f - _f.subs(_swap, simultaneous=True)) / 2   # антиинвариант
_e1, _e2 = r1_ + r2_, r1_ * r2_


def shadow1():
    # разложение существует и единственно: f = f_sym + f_anti; σ-типы компонент верны
    return (simplify(_f - (_fs + _fa)) == 0
            and simplify(_fs.subs(_swap, simultaneous=True) - _fs) == 0
            and simplify(_fa.subs(_swap, simultaneous=True) + _fa) == 0)
run("SHADOW-1", "shadow_lemma §1", "разложение f = тень + антиинвариант (σ-чёт/σ-нечет) существует и единственно", shadow1)


def shadow2():
    # ТЕНЬ выражается через агрегаты пары: f_sym = (e₁e₂ + 3e₁)/2 — конструктивно
    return simplify(_fs - (_e1 * _e2 + 3 * _e1) / 2) == 0
run("SHADOW-2", "shadow_lemma §1а", "тень выражается через Agg-агрегаты e₁,e₂ (инварианты Tot-коллапса ветви)", shadow2)


def shadow3():
    # БИТ кратен разности: f_anti = (r₁−r₂)(e₂+3)/2; его КВАДРАТ — снова тень,
    # и в нём сам собой возникает D = e₁²−4e₂ (V·V пары [C-61 deg56]);
    # Диагональ даёт нуль; дополнительный множитель даёт нули вне неё.
    # Контрпример к прежнему общему iff: (1,-3), где e₂+3=0, а r₁-r₂=4.
    return (simplify(_fa - (r1_ - r2_) * (_e2 + 3) / 2) == 0
            and simplify(_fa**2 - (_e1**2 - 4*_e2) * (_e2 + 3)**2 / 4) == 0
            and simplify(_fa.subs(r2_, r1_)) == 0
            and _fa.subs({r1_: 1, r2_: -3}) == 0
            and (r1_ - r2_).subs({r1_: 1, r2_: -3}) == 4)
run("SHADOW-3", "C-61 deg56/SP_ZERO/EC-005", "антиинвариант кратен разности; квадрат — тень; у детектора есть нули вне диагонали", shadow3)


def shadow4():
    # след Д10/Д11 на сопряжении: (Re, |z|²) — тень, не различают z и z̄;
    # бит полуплоскости sign(Im) — антиинвариант. Гардрейл U(1): у e^{iπ/6} и
    # e^{iπ/3} равные |z| и бит, но разные θ — непрерывное содержание фазы
    # ВНЕ Z/2-леммы (Rot ≠ −), тест Д10 обязан целить именно его
    z0 = 1 + 2*I
    zc = sp.conjugate(z0)
    trace_blind = (sp.re(z0) == sp.re(zc) and simplify(sp.Abs(z0)**2 - sp.Abs(zc)**2) == 0
                   and sp.sign(sp.im(z0)) == 1 and sp.sign(sp.im(zc)) == -1)
    z1, z2 = sp.exp(I*pi/6), sp.exp(I*pi/3)
    beyond_bit = (simplify(sp.Abs(z1) - sp.Abs(z2)) == 0
                  and sp.im(z1) > 0 and sp.im(z2) > 0
                  and simplify(z1 - z2) != 0)
    return trace_blind and beyond_bit
run("SHADOW-4", "Д10/Д11, Rot≠−", "(Re,|z|²) слепы к сопряжению — бит=sign(Im); θ-содержание вне Z/2-леммы", shadow4)


def shadow5():
    # QG-сцепка: пара корней {1,−1} (p=0,q=−1) — тень (e₁,e₂)=(0,−1) ОДНА на оба
    # присвоения ветви; симметричная цель g=e₁ не различает присвоения (ход
    # воспроизводим из тени при равной цене → QG-fail), антисимметричная h=r₁−r₂
    # различает (±2; тень её не выражает → ход не воспроизводим). Различающий ход
    # Д11 живёт ТОЛЬКО в антисимметричной компоненте.
    a1 = {r1_: 1, r2_: -1}
    a2 = {r1_: -1, r2_: 1}
    shadow_same = (_e1.subs(a1) == 0 and _e1.subs(a2) == 0
                   and _e2.subs(a1) == -1 and _e2.subs(a2) == -1)
    h = r1_ - r2_
    bit_differs = h.subs(a1) == 2 and h.subs(a2) == -2
    return (shadow_same and bit_differs
            and qg_gate(True, True) is False    # симметричная цель: воспроизводима из тени
            and qg_gate(True, False) is True)   # антисимметричная: не воспроизводима
run("SHADOW-5", "shadow_lemma §1/O_14", "QG-сцепка: различающий ход канала бита живёт только в антиинварианте", shadow5)


# -------------------------------------------- EXT15 (внешний мост У1–У5)
# external_bridge_u1_u5.md. Это конечные sanity-пробы математического ядра,
# НЕ доказательство семантики уровней и НЕ основание для St_FTS.

def ext15_1():
    # q=|·|: ненулевой слой имеет две зеркальные ветви, нулевой — одну.
    return (solveset(Eq(Abs(x), 2), x, S.Reals) == sp.FiniteSet(-2, 2)
            and solveset(Eq(Abs(x), 0), x, S.Reals) == sp.FiniteSet(0)
            and Abs(-2) == Abs(2) and -2 != 2)
run("EXT15-1", "external_bridge §2", "q=|·|: слой r=2 есть {−2,+2}, слой 0 вырожден",
    ext15_1)


def ext15_2():
    # s± — две секции q на неотрицательном кодомене; s−∘q = −|x|.
    samples = (sp.Rational(0), sp.Rational(1, 2), sp.Rational(3))
    sections = all(Abs(r) == r and Abs(-r) == r for r in samples)
    selected = all(-Abs(v) == -abs(v) for v in (-3, -1, 0, 2, 5))
    return sections and selected
run("EXT15-2", "external_bridge §2", "s±(r)=±r — секции |·|; s−(|x|)=−|x| на пробной сетке",
    ext15_2)


def ext15_3():
    # Исчерпывающая конечная модель на {-2,-1,0,1,2}: веса 0/1/2.
    # H(X||X|)>0 должно быть эквивалентно существованию слоя ±r с обеими
    # положительными ветвями. Это sanity-check общей формулы, не её доказательство.
    values = (-2, -1, 0, 1, 2)
    for raw in product(range(3), repeat=len(values)):
        total = sum(raw)
        if total == 0:
            continue
        weights = dict(zip(values, raw))
        entropy = 0.0
        both = False
        for r in (1, 2):
            wp, wm = weights[r], weights[-r]
            layer = wp + wm
            if wp > 0 and wm > 0:
                both = True
            if layer:
                for w in (wp, wm):
                    if w:
                        p = w / layer
                        entropy -= (layer / total) * p * log2(p)
        if (entropy > 1e-12) != both:
            return False
        if entropy < -1e-12 or entropy > 1.0 + 1e-12:
            return False
    return True
run("EXT15-3", "external_bridge §3", "На всех весах 0/1/2: H(X||X|)>0 ⇔ есть положительные ±r; H≤1 bit",
    ext15_3)

# ----------------------------------------------------------------- итог
n_pass = sum(1 for r in RESULTS if r[3])
n_fail = len(RESULTS) - n_pass
print(f"\nИТОГ: {n_pass} PASS / {n_fail} FAIL (всего {len(RESULTS)}; кандидат-пробы, НЕ сьют)")
if n_fail:
    print("FAIL кандидат-пробы = строка в work/REFUTED.md + разбор в заметке-источнике.")
sys.exit(0 if n_fail == 0 else 1)
