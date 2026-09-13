# -*- coding: utf-8 -*-
"""
Машинная верификация формальных утверждений пересборки ФТС v14.
Каждая проверка C-NN соответствует утверждению в FTS_v14_paper.md.
Запуск:  python -X utf8 work/v14_rebuild/verification.py
Выход:   краткая строка при PASS; полный verification_report.md только при FAIL
          (+ код возврата 0 если все PASS)
"""
import io
import os
import re
import sys

import sympy as sp
from sympy import (Abs, And, Eq, Function, I, Rational, S, Symbol, cos, diff,
                   dsolve, exp, factorial, oo, pi, sign, simplify, sin, solve,
                   solveset, sqrt, symbols)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TRIPLES = os.path.join(ROOT, "source", "fts_triples.tsv")

x, y, a, b, t, th = symbols("x y a b t theta", real=True)
RESULTS = []


def check(cid, claim, ok, witness=""):
    RESULTS.append((cid, claim, bool(ok), witness))
    if not ok:
        print("FAIL", cid, "-", claim)


def parity(expr, var):
    """Возвращает 'even' | 'odd' | 'neither' для выражения expr(var)."""
    e_neg = expr.subs(var, -var)
    if simplify(e_neg - expr) == 0:
        return "even"
    if simplify(e_neg + expr) == 0:
        return "odd"
    return "neither"


# ---------------------------------------------------------------- Д1: минус = анти-форма
# C01: F = -F  <=>  F = 0  (нулевая граница — единственное совпадение формы с анти-формой)
# Формально: F = -F  <=>  2F = 0  <=>  F = 0 (поле R, характеристика 0). Проверяем
# алгебраическое ядро (F+F = 2F) и совпадение solveset (для cos множества сравниваются
# по печатной канонической форме: структурное == в sympy ложно срабатывает на dummy-переменных).
forms = {"x": x, "x**2": x**2, "Abs(x)": Abs(x), "x**3": x**3, "cos(x)": cos(x)}
ok = True
for name, F in forms.items():
    if simplify(F + F - 2 * F) != 0:          # F = -F  <=>  2F = 0
        ok = False
    sols = solveset(Eq(F, -F), x, domain=S.Reals)
    zeros = solveset(Eq(F, 0), x, domain=S.Reals)
    if not (sols == zeros or str(sols) == str(zeros)):
        ok = False
check("C01", "F = -F тогда и только тогда, когда F = 0 (для x, x², |x|, x³, cos x)", ok,
      "F=-F ⇔ 2F=0 ⇔ F=0 над R; solveset(F=-F) совпадает с solveset(F=0)")

# C02: пары лестницы (F, -F) пересекаются только на нулевой границе
pairs = [(x, -x), (Abs(x), -Abs(x)), (x**2, -(x**2))]
ok = all(solveset(Eq(F, G), x, domain=S.Reals) == sp.FiniteSet(0) for F, G in pairs)
check("C02", "Пары уровней (y=x|y=-x), (|x| | -|x|), (x² | -x²) совпадают только в x=0", ok)

# ---------------------------------------------------------------- Д2: модуль = удержание
# C03: |x| — инвариант зеркальной инволюции x -> -x
check("C03", "|x| = |-x| (модуль — инвариант зеркала)", simplify(Abs(-x) - Abs(x)) == 0)

# C04: |a| = |b|  <=>  a = b или a = -b  (модуль = фактор по зеркальной паре)
# solveset возвращает {|b|, -|b|}; как множество это и есть {b, -b}, поскольку |b| = ±b
# (свидетель: |b|² - b² = 0, т.е. (|b|-b)(|b|+b)=0 для любого вещественного b).
lhs = solveset(Eq(Abs(a), Abs(b)), a, domain=S.Reals)
two_candidates = lhs == sp.FiniteSet(Abs(b), -Abs(b)) or lhs == sp.FiniteSet(b, -b)
abs_is_pm = simplify(Abs(b)**2 - b**2) == 0
fwd = simplify(Abs(b) - Abs(-b)) == 0  # a=±b ⇒ |a|=|b|
check("C04", "|a|=|b| ⇔ a=±b (модуль хранит пару ветвей, стирает выбор)",
      two_candidates and abs_is_pm and fwd,
      "solveset даёт ровно пару {±|b|} = {±b}, т.к. (|b|-b)(|b|+b)=0")

# ---------------------------------------------------------------- Аудит чётности (сквозной)
# C05: чётность каждой формулы лестницы соответствует заявленной
expected = [
    ("U3:  y=-x", -x, "odd"),
    ("U4:  y=|x|", Abs(x), "even"),
    ("U5:  y=-|x|", -Abs(x), "even"),
    ("U6:  y=x^2", x**2, "even"),
    ("U7:  y=-x^2", -(x**2), "even"),
    ("U8:  y=sqrt(|x|)", sqrt(Abs(x)), "even"),
    ("U9:  y=x^3", x**3, "odd"),
    ("U10: y=cos(x)", cos(x), "even"),
    ("U11: y=e^x", exp(x), "neither"),
]
audit, ok = [], True
for label, F, want in expected:
    got = parity(F, x)
    audit.append(f"{label}: {got}")
    if got != want:
        ok = False
check("C05", "Аудит чётности: 3-odd, 4..8-even, 9-odd, 10-even, 11-neither", ok,
      "; ".join(audit))

# ---------------------------------------------------------------- Граница 7/8 (Д4: корень = вопрос)
# C06: sqrt(x^2) = |x| для всех вещественных x
check("C06", "Для вещественного x выполняется √(x²) = |x|",
      simplify(sqrt(x**2) - Abs(x)) == 0)

# C07: sqrt(x^2) != x (знак невосстановим) — контрпример x=-1
check("C07", "√(x²) ≠ x: при x=-1 левая часть 1, правая -1 (знак из квадрата невосстановим)",
      sqrt(sp.Integer(-1)**2) == 1 and sp.Integer(-1) != 1)

# C08: sqrt(|x|) = (x^2)^(1/4) — форма У8 есть «вопрос, заданный дважды»
check("C08", "Для вещественного x выполняется √|x| = (x²)^(1/4)",
      simplify(sqrt(Abs(x)) - (x**2)**Rational(1, 4)) == 0)

# C09: квадрат неинъективен: 1² = (-1)² при 1 ≠ -1 — у вопроса о прообразе два кандидата
check("C09", "Агрегат склеивает ветви: a²=b² при a≠b (a=1,b=-1) — прообраз двузначен",
      (1)**2 == (-1)**2 and 1 != -1)

# ---------------------------------------------------------------- У9: куб = выбор с основанием
check("C10", "Для вещественного x выполняется x³ = x·x²",
      simplify(x**3 - x * x**2) == 0)

cubic_positive = (sp.solve_univariate_inequality(x**3 > 0, x, relational=False)
                  == sp.Interval.open(0, oo))
cubic_negative = (sp.solve_univariate_inequality(x**3 < 0, x, relational=False)
                  == sp.Interval.open(-oo, 0))
cubic_zero = solveset(Eq(x**3, 0), x, domain=S.Reals) == sp.FiniteSet(0)
check("C11", "Для вещественного x выполняется sign(x³) = sign(x)",
      cubic_positive and cubic_negative and cubic_zero)

check("C12", "(x²)² = x⁴ — чётная функция; x³ и x⁴ не тождественны как функции",
      parity(x**4, x) == "even" and simplify(x**3 - x**4) != 0)

# ---------------------------------------------------------------- У10: оценка = взвешенное чередование со шкалой
# C13: cos x = sum (-1)^k x^(2k)/(2k)!  (чередование агрегата и анти-агрегата с факториальной ценой)
k = Symbol("k", integer=True, nonnegative=True)
cos_series = sp.summation((-1)**k * x**(2*k) / factorial(2*k), (k, 0, oo))
check("C13", "Для вещественного x: cos x = Σ_{k≥0}(-1)^k x^(2k)/(2k)!",
      simplify(cos_series - cos(x)) == 0)

# C14: БЕЗ весов ряд Σ(-1)^k x^(2k) расходится при |x|>=1 (частичные суммы при x=1: 1,0,1,0,...)
convergence_region = sp.solve_univariate_inequality(Abs(-x**2) < 1, x, relational=False)
check("C14", "Геометрический ряд Σ_{k≥0}(-1)^k x^(2k) сходится ровно при |x|<1 и расходится при |x|≥1",
      convergence_region == sp.Interval.open(-1, 1),
      f"область сходимости |−x²|<1: {convergence_region}")

# C15: единственность: f'' = -f, f(0)=1, f'(0)=0  =>  f = cos x
f = Function("f")
sol = dsolve(Eq(f(x).diff(x, 2), -f(x)), f(x), ics={f(0): 1, f(x).diff(x).subs(x, 0): 0})
check("C15", "ОДУ F''=−F при F(0)=1, F'(0)=0 имеет единственное решение cos x",
      simplify(sol.rhs - cos(x)) == 0, f"dsolve: {sol.rhs}")

# C16: |cos| <= 1 (первая шкала) и нули на решётке pi/2 + pi*k
zeros = solveset(Eq(cos(x), 0), x, domain=S.Reals)
n_zero = Symbol("n_zero", integer=True)
expected_zeros = sp.Union(
    sp.ImageSet(sp.Lambda(n_zero, 2*n_zero*pi + pi/2), S.Integers),
    sp.ImageSet(sp.Lambda(n_zero, 2*n_zero*pi + 3*pi/2), S.Integers),
)
cos_range = sp.calculus.util.function_range(cos(x), x, S.Reals)
check("C16", "Для вещественного x: |cos x|≤1, а нули равны x=π/2+πk",
      zeros.dummy_eq(expected_zeros) and cos_range == sp.Interval(-1, 1))

# C17: cos x = -cos x ровно на нулевой решётке (форма совпадает с анти-формой в точках равновесия)
# cos = -cos ⇔ 2cos = 0 ⇔ cos = 0; множества сравниваем по канонической печатной форме
# (структурное == в sympy различает dummy-переменные ImageSet).
eq_sets = solveset(Eq(cos(x), -cos(x)), x, domain=S.Reals)
check("C17", "Для вещественного x: cos x = −cos x ⇔ cos x = 0",
      str(eq_sets) == str(zeros) and simplify(cos(x) + cos(x) - 2 * cos(x)) == 0)

# ---------------------------------------------------------------- У11: Я = неподвижная точка различия
# C18: f' = f, f(0)=1  =>  f = e^x (единственность самотождества сквозь изменение)
sol = dsolve(Eq(f(x).diff(x), f(x)), f(x), ics={f(0): 1})
check("C18", "ОДУ F'=F при F(0)=1 имеет единственное решение e^x",
      simplify(sol.rhs - exp(x)) == 0, f"dsolve: {sol.rhs}")

# C19: e^x > 0 — вещественных нулей нет (изнутри Я не достигает собственного отсутствия)
check("C19", "Для вещественного x: e^x>0 и вещественных нулей нет",
      solveset(Eq(exp(x), 0), x, domain=S.Reals) == sp.EmptySet
      and sp.calculus.util.function_range(exp(x), x, S.Reals) == sp.Interval.open(0, oo))

# C20: e^x = Σ x^k/k! — все степени присутствуют (Я как тотал нижних форм)
exp_series = sp.summation(x**k / factorial(k), (k, 0, oo))
check("C20", "Для вещественного x: e^x = Σ_{k≥0}x^k/k!; все коэффициенты 1/k! ненулевые",
      simplify(exp_series - exp(x)) == 0)

# C21: e^x ни чётна, ни нечётна — первая форма лестницы с собственной ориентацией
check("C21", "Функция e^x не является ни чётной, ни нечётной", parity(exp(x), x) == "neither")

# ---------------------------------------------------------------- У12: окружность = замкнутая граница
circle1 = x**2 + (y - 2)**2 - 4
circle2 = x**2 + (y + 2)**2 - 4

# C22: окружность проходит через начало координат (касание общего отсутствия)
check("C22", "x²+(y-2)²=4 проходит через (0,0)", circle1.subs({x: 0, y: 0}) == 0)

# C23: тест вертикальной прямой: при x=0 два значения y => не график функции y=f(x)
ys = solveset(Eq(circle1.subs(x, 0), 0), y, domain=S.Reals)
check("C23", "При x=0 окружность имеет y={0,4}, поэтому не является графиком однозначной функции y=f(x)",
      ys == sp.FiniteSet(0, 4))

# C24: две ветви y = 2 ± sqrt(4 - x²) (удержание двух взаимоисключающих разрешений)
branches = solve(Eq(circle1, 0), y)
want = {sp.simplify(2 - sqrt(4 - x**2)), sp.simplify(2 + sqrt(4 - x**2))}
check("C24", "Решение окружности относительно y имеет две ветви y=2±√(4−x²)",
      {sp.simplify(s) for s in branches} == want)

# C25: вдоль границы x·dx = -(y-2)·dy (локальный конфликт: выигрыш одного — проигрыш другого)
dF = sp.Matrix([sp.diff(circle1, x), sp.diff(circle1, y)])
check("C25", "На окружности полный дифференциал даёт x·dx=−(y−2)·dy",
      dF[0] == 2 * x and dF[1] == 2 * (y - 2))

# C26: одиночная окружность ломает зеркало y -> -y; образ — вторая окружность
mirrored = sp.expand(circle1.subs(y, -y))
check("C26", "Подстановка y↦−y переводит x²+(y−2)²=4 в x²+(y+2)²=4, отличную от исходной окружности",
      simplify(mirrored - sp.expand(circle2)) == 0 and simplify(mirrored - sp.expand(circle1)) != 0)

# C27: две окружности касаются в (0,0): единственная общая точка, градиенты антипараллельны
common = solve([Eq(circle1, 0), Eq(circle2, 0)], [x, y], dict=True)
grads = (sp.Matrix([sp.diff(circle1, v) for v in (x, y)]).subs({x: 0, y: 0}),
         sp.Matrix([sp.diff(circle2, v) for v in (x, y)]).subs({x: 0, y: 0}))
antiparallel = simplify(grads[0] + grads[1]) == sp.Matrix([0, 0])
check("C27", "Союзы соприкасаются только в (0,0), градиенты (0,-4) и (0,4) антипараллельны (касание, не пересечение)",
      common == [{x: 0, y: 0}] and antiparallel)

# ---------------------------------------------------------------- У13 (предсказание): произведение границ
# C28: zero-product property over the real field, checked by exhaustive zero/nonzero cases.
a_nz = Symbol("a_nz", real=True, nonzero=True)
b_nz = Symbol("b_nz", real=True, nonzero=True)
zero_product_reals = (
    solveset(Eq(a * b_nz, 0), a, domain=S.Reals) == sp.FiniteSet(0)
    and solveset(Eq(a_nz * b, 0), b, domain=S.Reals) == sp.FiniteSet(0)
    and simplify(0 * b) == 0
    and simplify(a * 0) == 0
)
check("C28", "Над вещественными числами a·b=0 ⇔ a=0 или b=0",
      zero_product_reals, "проверены случаи нулевого и ненулевого второго множителя")

# C29: множество решений произведения — объединение двух окружностей; пересечение — только (0,0)
check("C29", "Нули произведения двух многочленов окружностей равны объединению окружностей; их общая точка — (0,0)",
      zero_product_reals and common == [{x: 0, y: 0}])

# C30: пара окружностей восстанавливает зеркальную симметрию y -> -y
pair = sp.expand(circle1 * circle2)
check("C30", "Произведение уравнений двух окружностей инвариантно относительно y↦−y",
      simplify(sp.expand(pair.subs(y, -y)) - pair) == 0)

# ---------------------------------------------------------------- У15 (эскиз предсказания): орбита симметрии
# C31: z = e^{i·theta}: |z| = 1, dz/dtheta = i·z (вращение без роста — статическая точка симметрии)
z = exp(I * th)
check("C31", "Для z=e^{iθ}: |z|=1 и dz/dθ=i·z",
      simplify(Abs(z) - 1) == 0 and simplify(diff(z, th) - I * z) == 0)

# ---------------------------------------------------------------- Структура окон (из канона v13)
# C32: окна канона перекрываются ровно в узлах 3, 7, 11, 15
def parse_windows(path):
    wins = {}
    with io.open(path, encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 3 and parts[1] == "has_window":
                wins.setdefault(parts[2], []).append(parts[0])
    return wins

nodes_overlap = False
windows_details = "source/fts_triples.tsv недоступен"
try:
    wins = parse_windows(TRIPLES)
    ordered_windows = ["(-1,0,1,2,3)", "(3,4,5,6,7)", "(7,8,9,10,11)",
                       "(11,12,13,14,15)", "(15,16,17,...)"]
    parsed = [set(map(int, re.findall(r"-?\d+", value))) for value in ordered_windows]
    adjacent = [parsed[i] & parsed[i+1] for i in range(len(parsed)-1)]
    nonadjacent_disjoint = all(not (parsed[i] & parsed[j])
                               for i in range(len(parsed)) for j in range(i+2, len(parsed)))
    nodes_overlap = (set(wins) == set(ordered_windows)
                     and adjacent == [{3}, {7}, {11}, {15}]
                     and nonadjacent_disjoint)
    windows_details = "; ".join(ordered_windows)
except FileNotFoundError:
    pass
check("C32", "Окна канона: (-1..3),(3..7),(7..11),(11..15),(15..) — перекрытие ровно в узлах 3/7/11/15",
      nodes_overlap, windows_details)

# C33: канонический projects_to имеет шаг -2 (U_01..U_07 -> U_m1..U_05)
projects_ok = False
projects_details = "source/fts_triples.tsv недоступен"
try:
    proj = []
    with io.open(TRIPLES, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 3 and parts[1] == "projects_to":
                proj.append((parts[0], parts[2]))
    def num(u):
        s = u.replace("U_", "")
        return -1 if s == "m1" else int(s)
    projects_ok = len(proj) == 7 and all(num(s) - num(o) == 2 for s, o in proj)
    projects_details = "; ".join(f"{s}→{o}" for s, o in proj)
except FileNotFoundError:
    pass
check("C33", "Канон: projects_to — ровно шаг 2 вниз (7 рёбер U_01→U_m1 ... U_07→U_05)",
      projects_ok, projects_details)

# C34: математические свидетели полушагов проекции: У4=У2∘π, У5=У3∘π, У6=У4·π, У7=У5·π, где π(x)=|x|
pi_q = Abs(x)
ok = (simplify(pi_q - Abs(x)) == 0                       # У4 = У2(π(x)) = |x|
      and simplify((-t).subs(t, pi_q) - (-Abs(x))) == 0   # У5 = У3(π(x)) = -|x|
      and simplify(Abs(x) * pi_q - x**2) == 0             # У6 = У4·π = |x|·|x| = x²
      and simplify(-Abs(x) * pi_q - (-(x**2))) == 0)      # У7 = У5·π = -|x|·|x| = -x²
check("C34", "Полушаги проекции: У4=У2∘π, У5=У3∘π, У6=У4·π, У7=У5·π при π(x)=|x| (шаг 4 = два шага 2)", ok)

# C35: пентадный свидетель узлов 3 и 7: один и тот же оператор «минус» (≠) поднят с кода на агрегат
check("C35", "В выбранной А-записи форм выполняется F3=−F2 и F7=−F6",
      simplify(-(x) - (-x)) == 0 and simplify(-(x**2) - (-(x**2))) == 0)

# C36: нижняя ветвь У12 локально содержит квадратичность У6: 2 - sqrt(4-x²) = x²/4 + O(x⁴)
# [канон: лист 31_Upper_12_17, строка U12_QUAD_CONTACT]
lower_branch = 2 - sqrt(4 - x**2)
ser = sp.series(lower_branch, x, 0, 4).removeO()
check("C36", "Ветвь y=2-√(4-x²) ~ x²/4 у нуля: союз локально содержит агрегат У6 (касание)",
      simplify(ser - x**2 / 4) == 0, f"ряд Тейлора: {ser}")

# C37: параметризация x=2cos t, y=2+2sin t лежит на окружности У12: У10 становится координатой У12
# [канон: лист 31_Upper_12_17, строка U10_TO_U12]
tt = symbols("t", real=True)
on_circle = simplify((2 * cos(tt))**2 + (2 + 2 * sin(tt) - 2)**2 - 4)
check("C37", "Параметризация x=2cos t, y=2+2sin t удовлетворяет x²+(y−2)²=4",
      on_circle == 0)

# ---------------------------------------------------------------- Д10: фаза — отдельный оператор (не анти-форма)
# C38: Rot_pi реализует вещественный минус: e^{i·pi} = -1 (точка совпадения операторов)
minus_angles = solveset(Eq(exp(I * th), -1), th, domain=sp.Interval.Ropen(0, 2*pi))
check("C38", "В фундаментальном интервале 0≤θ<2π равенство e^{iθ}=−1 выполняется ровно при θ=π",
      minus_angles == sp.FiniteSet(pi) and simplify(exp(I * pi) + 1) == 0)

# C39: зеркальное окно — вещественный след фазовой орбиты: e^{iθ}·x вещественно ⇔ θ∈{0,π};
# непрерывная U(1)-орбита в вещественном носителе дискретизируется до пары {F, −F}
xr = Symbol("x_r", real=True, positive=True)
real_trace = solveset(sin(th), th, domain=sp.Interval.Ropen(0, 2 * pi))
ends_ok = simplify(exp(I * 0) * xr - xr) == 0 and simplify(exp(I * pi) * xr + xr) == 0
check("C39", "Для x>0 и 0≤θ<2π: Im(e^{iθ}x)=0 ⇔ θ∈{0,π}; значения равны {x,−x}",
      real_trace == sp.FiniteSet(0, pi) and ends_ok,
      f"вещественные точки орбиты: theta in {real_trace}; e^(i0)x=x, e^(iπ)x=−x")

# C40: модуль стирает фазу: |e^{iθ}·z| = |z| — квадрат/норма не видит положения на орбите
zc = Symbol("z_c", complex=True)
check("C40", "Для комплексного z и вещественного θ выполняется |e^{iθ}z|=|z|",
      simplify(Abs(exp(I * th) * zc) - Abs(zc)) == 0)

# ---------------------------------------------------------------- красная команда (F3/O_09)
# C41: радиус У12 не выводится: ВСЕ свойства уровня выполняются для любого r>0
# (касание (0,0), две ветви, контакт нижней ветви ~ x²/(2r) — параметр свободен)
rr = Symbol("r", real=True, positive=True)
circle_r = x**2 + (y - rr)**2 - rr**2
through_zero = circle_r.subs({x: 0, y: 0}) == 0
branches_r = solve(Eq(circle_r, 0), y)
contact_r = sp.series(rr - sqrt(rr**2 - x**2), x, 0, 4).removeO()
check("C41", "Для любого r>0 окружность x²+(y−r)²=r² проходит через ноль, имеет две y-ветви и контакт x²/(2r)",
      through_zero and len(branches_r) == 2 and simplify(contact_r - x**2 / (2 * rr)) == 0,
      f"нижняя ветвь ~ {contact_r}; r=2 даёт x²/4, r=1/2 дал бы ровно У6")

# C42: куб обратим на R — «вопрос к кубу» имеет единственный ответ, т.е. не вопрос;
# квадрат необратим — прообраз двузначен. Поэтому У8 = √, а не ∛.
c_real = Symbol("c_real", real=True)
c_positive = Symbol("c_positive", positive=True)
cube_roots = solveset(Eq(t**3, c_real), t, domain=S.Reals)
square_roots = solveset(Eq(t**2, c_positive), t, domain=S.Reals)
check("C42", "Для каждого вещественного c у t³=c один вещественный корень; при c>0 у t²=c два",
      cube_roots == sp.FiniteSet(Abs(c_real)**Rational(1, 3) * sign(c_real))
      and square_roots == sp.FiniteSet(-sqrt(c_positive), sqrt(c_positive)))

# C43: общее решение Δ²F=−F есть {A·cos + B·sin}; требование чётности (П4) обнуляет B —
# cos отобран структурой уровня, sin (нечётный критерий = предвзятость) исключён
gen = dsolve(Eq(f(x).diff(x, 2), -f(x)), f(x)).rhs
C1, C2 = sorted(gen.free_symbols - {x}, key=lambda s: s.name)
odd_part = simplify(gen.subs(x, -x) - gen)
check("C43", "Общее решение F''=−F имеет вид A·sin x+B·cos x; чётность обнуляет sin-компоненту",
      odd_part.has(sin) and simplify(odd_part.subs(C1, 0)) == 0,
      f"общее решение: {gen}; нечётный остаток: {odd_part}")

# ---------------------------------------------------------------- Д11: регистр отношений (авторское расширение 2026-06-12)
# C44: унификация правых частей: отношение анти-формы к форме = -1 на всех парах лестницы;
# правая часть всякого уровня в ratio-регистре — одно утверждение «отношение ≠ 1»
ratio_x = Symbol("ratio_x", real=True, nonzero=True)
ratios = [simplify((-ratio_x) / ratio_x), simplify((-Abs(ratio_x)) / Abs(ratio_x)),
          simplify((-ratio_x**2) / ratio_x**2)]
check("C44", "Для вещественного x≠0: (−x)/x=(−|x|)/|x|=(−x²)/x²=−1≠1",
      all(rv == -1 for rv in ratios) and sp.Integer(-1) != 1,
      f"отношения пар: {ratios}")

# C45: ratio-канал хранит ветвь, стирает величину — двойник C-40 (Q хранит величину, стирает ветвь)
ratio_y = Symbol("ratio_y", real=True, nonzero=True)
ratio_a = Symbol("ratio_a", real=True, nonzero=True)
branch_kept = simplify(ratio_x / Abs(ratio_x) - sign(ratio_x)) == 0
magnitude_erased = simplify((ratio_a * ratio_x) / (ratio_a * ratio_y) - ratio_x / ratio_y) == 0
check("C45", "При x≠0: x/|x|=sign(x); при a,x,y≠0: (a·x)/(a·y)=x/y",
      branch_kept and magnitude_erased)

# C46: характер границы меняется: аддитивно формы ВСТРЕЧАЮТСЯ в нуле, в ratio-регистре ноль — ПОЛЮС
additive_meet = simplify((x - (-x)).subs(x, 0)) == 0
pole = (S.One / S.Zero) is S.ComplexInfinity
check("C46", "Разность x−(−x)=2x обращается в ноль при x=0, а отношение 1/0 не определено (полюс)",
      additive_meet and pole, "нулевая граница исключена из регистра отношений")

# C47: комплексный ratio-канал = оператор извлечения фазы; полярное разложение = произведение каналов
r2, t2 = symbols("r2 t2", positive=True), Symbol("t2", real=True)
r2 = Symbol("r2", positive=True)
zz = r2 * exp(I * t2)
check("C47", "Для z=r·e^{iθ}, r>0: z/|z|=e^{iθ} и z=|z|·(z/|z|)",
      simplify(zz / Abs(zz) - exp(I * t2)) == 0 and simplify(Abs(zz) * (zz / Abs(zz)) - zz) == 0)

# C48: лемма Tot: {+1,−1} — группа Z/2, бит ветви — групповое считывание (гомоморфизм);
# узловой оператор = умножение на −1 [C-35]; Tot («отношение ≡ 1») = коллапс Z/2 → {1}:
# элемента −1 нет — правые части (материал А+1) уничтожены
closure = all(sa * sb in (-1, 1) for sa in (-1, 1) for sb in (-1, 1))
mag_a = Symbol("mag_a", positive=True)
mag_b = Symbol("mag_b", positive=True)
homo = all(simplify(sign(sa * mag_a * sb * mag_b) - sign(sa * mag_a) * sign(sb * mag_b)) == 0
           for sa in (-1, 1) for sb in (-1, 1))
check("C48", "{+1,−1} замкнуто относительно умножения; для ненулевых вещественных a,b sign(ab)=sign(a)sign(b)",
      closure and homo)

# ---------------------------------------------------------------- единичная граница (авторское наблюдение 2026-06-12)
# C49: идемпотенты x²=x ⟺ x∈{0,1}; через zero-product x(x−1)=0 (связь с Д9)
idem = solveset(Eq(x**2, x), x, domain=S.Reals)
check("C49", "Над вещественными числами x²=x ⇔ x∈{0,1}; x²−x=x(x−1)",
      idem == sp.FiniteSet(0, 1) and sp.factor(x**2 - x) == x * (x - 1))

# C50: при x=1 полиномиальная лестница (У1..У9) схлопывается в бит {+1,−1} = R-канал
poly_levels = [S.One, x, -x, Abs(x), -Abs(x), x**2, -(x**2), sqrt(Abs(x)), x**3]
vals1 = [simplify(f.subs(x, 1)) for f in poly_levels]
check("C50", "Значения выбранных форм У1..У9 при x=1 принадлежат {+1,−1}",
      all(v in (sp.Integer(1), sp.Integer(-1)) for v in vals1),
      f"значения У1..У9 в x=1: {vals1}")

# C51: трансцендентные У10, У11 переживают единичную границу (не ±1) — бесконечные суммы степеней
surv = (simplify(cos(1)) not in (sp.Integer(1), sp.Integer(-1))
        and simplify(exp(1)) not in (sp.Integer(1), sp.Integer(-1)))
check("C51", "cos(1)≠±1 и e≠±1",
      surv, f"cos(1)={sp.N(cos(1), 4)}, e={sp.N(exp(1), 4)}")

# C52: деградация = пентада назад; носитель (умножение) тривиален ровно в x=1
deg = (simplify((x**2 - x).subs(x, 1)) == 0          # У6=У2
       and simplify((-x**2 - (-x)).subs(x, 1)) == 0   # У7=У3
       and simplify((sqrt(Abs(x)) - Abs(x)).subs(x, 1)) == 0)  # У8=У4
check("C52", "При x=1 совпадают пары форм (У6,У2), (У7,У3), (У8,У4); x²=x только при x∈{0,1}",
      deg and idem == sp.FiniteSet(0, 1))

# ---------------------------------------------------------------- χ-оверлей = А-регистр ∘ (x:=χ)
# C53: χ-лестница не добавляет содержания уровней — это А-регистр с подстановкой x:=χ
# [лист Chi_Stat_Ladder]. Формально: для каждого уровня χ-формула = flat-формула при x→χ.
chi = Symbol("chi", real=True)
flat_vs_chi = [
    ("3", -x, -chi),
    ("4", Abs(x), Abs(chi)),
    ("5", -Abs(x), -Abs(chi)),
    ("6", x * x, chi * chi),
    ("7", -x * x, -chi * chi),
    ("8", sqrt(Abs(x)), sqrt(Abs(chi))),
    ("9", x * x * x, chi * chi * chi),
]
overlay_ok = all(simplify(flat.subs(x, chi) - chiform) == 0 for _lvl, flat, chiform in flat_vs_chi)
check("C53", "Для перечисленных форм У3..У9 χ-формула получается точной подстановкой x:=χ",
      overlay_ok, "проверено совпадение семи пар форм после подстановки")

# C54: канонический toy-пример χ² (лист Chi_Stat_Ladder, строки 51–55) — независимое воспроизведение
O = [28, 20, 30, 22]
E = 25
chi_i = [sp.Rational(o - E) / sp.sqrt(E) for o in O]
chi2 = sum(c**2 for c in chi_i)
check("C54", "Toy-пример χ²: O=[28,20,30,22], E=25 ⟹ Σχᵢ² = 2.72 (воспроизведение канонической таблицы)",
      simplify(chi2 - sp.Rational(272, 100)) == 0, f"χ_i={[float(c) for c in chi_i]}, χ²={float(chi2)}")

# C55: гардрейл G_CHI_01 (x:=χ, НЕ χ²): подстановка x:=χ² превращает У6 в χ⁴ — деградация реальна
u6_correct = (x * x).subs(x, chi)          # = χ²  (правильно)
u6_wrong = (x * x).subs(x, chi**2)         # = χ⁴  (нарушение гардрейла)
check("C55", "Подстановка x:=χ в x² даёт χ², а подстановка x:=χ² даёт χ⁴; эти функции не тождественны",
      simplify(u6_correct - chi**2) == 0 and simplify(u6_wrong - chi**4) == 0 and simplify(chi**4 - chi**2) != 0)

# C56: нулевая граница в χ-носителе = идеальный fit; правые части наследуются
chi_zero = solveset(Eq(chi * chi, 0), chi, domain=S.Reals)
anti_meet = solveset(Eq(-chi**2, chi**2), chi, domain=S.Reals)
check("C56", "Для вещественного χ: χ²=0 ⇔ χ=0 и −χ²=χ² ⇔ χ=0",
      chi_zero == sp.FiniteSet(0) and anti_meet == sp.FiniteSet(0))

# ---------------------------------------------------------------- малая форма = проекция (автор, 2026-06-13)
# Определение: нижний уровень есть «малая форма» (проекция projects_to) верхнего через один;
# общий критерий — совпадение в ОБОИХ якорях (нуль И единица); вложение — сильный частный случай.

# C57: форм-нить У2→У4→У6 ({x,|x|,x²}) — проекция: совпадают в нуле и в единице, не зеркало;
# вложение У2⊂У4: x=|x| на всём луче x≥0
proj = [x, Abs(x), x**2]
anti = [-x, -Abs(x), -x**2]
both_anchors = all((a - b).subs(x, 0) == 0 and (a - b).subs(x, 1) == 0
                   for thread in (proj, anti) for a, b in zip(thread, thread[1:]))
not_mirror = all(simplify(a + b) != 0 for thread in (proj, anti) for a, b in zip(thread, thread[1:]))
embedding = solveset(Abs(x) - x, x, S.Reals) == sp.Interval(0, oo)
check("C57", "Соседние формы нитей {x,|x|,x²} и {−x,−|x|,−x²} совпадают при x=0,1, не являются зеркальными; x=|x| на [0,∞)",
      both_anchors and not_mirror and embedding)

# C58: зеркальные пары (±1) противоречат: встречаются ТОЛЬКО в нуле, противоположны в единице
mirror = [(x, -x), (Abs(x), -Abs(x)), (x**2, -(x**2))]
only_zero = all(solveset(Eq(f, g), x, S.Reals) == sp.FiniteSet(0) for f, g in mirror)
opp_unit = all(f.subs(x, 1) == -(g.subs(x, 1)) and f.subs(x, 1) != g.subs(x, 1) for f, g in mirror)
check("C58", "Пары (x,−x), (|x|,−|x|), (x²,−x²) совпадают только при x=0 и противоположны при x=1",
      only_zero and opp_unit)

# C59: единичная граница — ДИСКРИМИНАНТ противоречия vs проекции
# (в нуле неразличимы: все =0; в единице зеркало расходится ±1, проекция склеена)
zero_blind = all(f.subs(x, 0) == 0 for f in proj + anti)
unit_splits_mirror = all(f.subs(x, 1) != g.subs(x, 1) for f, g in mirror)
unit_keeps_proj = (len({f.subs(x, 1) for f in proj}) == 1
                   and len({f.subs(x, 1) for f in anti}) == 1)
check("C59", "При x=0 перечисленные формы равны нулю; при x=1 зеркальные пары различны, а формы каждой проекционной нити совпадают",
      zero_blind and unit_splits_mirror and unit_keeps_proj)

# C60–C62: два режима последовательного запрета (§8.1б) — формульная реализация
# связности О2 «тотализация уровня запрещает надстройку» (первая обнаруженная
# автором закономерность лестницы). Фолд 2026-07-05 (были пробы MIR/SEQ).

# C60: зеркальная половина: отражение чётного рунга (=↔≠, А-образ −F) ложится
# ровно на СЛЕДУЮЩИЙ рунг (партнёр = n XOR 1); с У8 пара рвётся
LF = {2: x, 3: -x, 4: Abs(x), 5: -Abs(x), 6: x**2, 7: -x**2,
      8: sqrt(Abs(x)), 9: x**3, 10: cos(x)}
mirror_next = all(simplify(-LF[2*k] - LF[2*k + 1]) == 0 for k in (1, 2, 3))
parity_updown = all(((n ^ 1) == n + 1) == (n % 2 == 0) for n in range(8))
break8 = simplify(-LF[8] - LF[9]) != 0 and simplify(-LF[9] - LF[10]) != 0
check("C60", "В таблице А-форм −F(2k)=F(2k+1) для пар {2,3},{4,5},{6,7}; для У8/У9 и У9/У10 равенство зеркала отсутствует",
      mirror_next and parity_updown and break8)

# C61: режим вырождения (шаги сборки): тотализация материала не опровергает
# следующую форму, а схлопывает её в нижнюю (потеря отдельности уровня)
deg34 = (solveset(Eq(Abs(x), x), x, S.Reals) == sp.Interval(0, oo)
         and solveset(Eq(Abs(x), 2), x, S.Reals) == sp.FiniteSet(-2, 2)
         and solveset(Eq(Abs(x), 2), x, sp.Interval(0, oo)) == sp.FiniteSet(2))
c_pos = symbols("c", positive=True)
pair_var = sp.Rational(1, 2) * ((c_pos - 0)**2 + (-c_pos - 0)**2)  # Var{c,−c}, среднее 0
tot_var = sp.Rational(1, 2) * ((c_pos - c_pos)**2 + (c_pos - c_pos)**2)  # Var{c,c}
deg56 = simplify(pair_var - c_pos**2) == 0 and simplify(tot_var) == 0
deg78 = (solveset(Eq(t**2, 4), t, S.Reals) == sp.FiniteSet(-2, 2)
         and solveset(Eq(t**2, 4), t, sp.Interval(0, oo)) == sp.FiniteSet(2)
         and solveset(Eq(t**2, -1), t, S.Reals) == S.EmptySet)
check("C61", "Три проверенных примера: |x| на [0,∞); Var{c,−c}=c² против Var{c,c}=0; вещественные прообразы t²=4 и отсутствие прообраза t²=−1",
      deg34 and deg56 and deg78)

# C62: булева тень: Tot(0_A)=¬A схлопывает двухканальную оценку A3 в один канал;
# средняя пара падает в полюса нижней: {4,5} → {0,1} (∅/ℝ)
shadow_and = sp.And(Eq(a, b), sp.Ne(a, b)) == sp.false
shadow_or = sp.Or(Eq(a, b), sp.Ne(a, b)) == sp.true
poles = (solveset(sp.Ne(x, x), x, S.Reals) == S.EmptySet
         and solveset(Eq(x, x), x, S.Reals) == S.Reals)
check("C62", "Булевы тождества: (a=b)∧(a≠b)=False, (a=b)∨(a≠b)=True; решения x≠x и x=x равны ∅ и ℝ",
      shadow_and and shadow_or and poles)

# ---------------------------------------------------------------- отчёт
def write_report():
    n_pass = sum(1 for _cid, _claim, ok, _witness in RESULTS if ok)
    n_fail = len(RESULTS) - n_pass

    def md_cell(value):
        """Экранирует разделитель Markdown-таблицы и не оставляет пустых ячеек с пробелом."""
        return str(value).replace("\\", "\\\\").replace("|", "\\|").strip() or "—"

    lines = [
        "# Отчёт машинной верификации — ФТС v14 rebuild",
        "",
        f"Запуск: `python -X utf8 work/v14_rebuild/verification.py` (sympy {sp.__version__})",
        "",
        f"**Итог: {n_pass} PASS / {len(RESULTS) - n_pass} FAIL из {len(RESULTS)}**",
        "",
    ]
    if n_fail:
        lines += [
            "Полная таблица записана, потому что обнаружен FAIL.",
            "",
            "| ID | Утверждение | Статус | Свидетель |",
            "|----|-------------|--------|-----------|",
        ]
        for cid, claim, ok, witness in RESULTS:
            lines.append(
                f"| {cid} | {md_cell(claim)} | {'PASS' if ok else '**FAIL**'} | {md_cell(witness)} |"
            )
        lines += [
            "",
            "Каждое C-NN привязано к утверждению в `FTS_v14_paper.md`. FAIL любой проверки",
            "означает, что соответствующее утверждение НЕ имеет права на статус formal_math_fact.",
        ]
    else:
        lines += [
            "Подробная таблица не создаётся: все проверки прошли.",
            "Полный отчёт автоматически появится при первом FAIL.",
        ]
    lines.append("")
    out = os.path.join(HERE, "verification_report.md")
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    if n_fail:
        print(f"FAIL verification: {n_pass} PASS / {n_fail} FAIL; полный отчёт: {out}")
        return False
    print(f"PASS verification: {n_pass} PASS / 0 FAIL")
    return True


if __name__ == "__main__":
    all_ok = write_report()
    sys.exit(0 if all_ok else 1)
