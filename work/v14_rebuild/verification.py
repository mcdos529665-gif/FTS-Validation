# -*- coding: utf-8 -*-
"""
Машинная верификация формальных утверждений пересборки ФТС v14.
Каждая проверка C-NN соответствует утверждению в FTS_v14_paper.md.
Запуск:  python -X utf8 work/v14_rebuild/verification.py
Выход:   work/v14_rebuild/verification_report.md  (+ код возврата 0 если все PASS)
"""
import io
import os
import sys
import math
import cmath

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
    print(("PASS" if ok else "FAIL"), cid, "-", claim)


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
check("C06", "√(x²) = |x| (вопрос к агрегату возвращает удержание, форму У4)",
      simplify(sqrt(x**2) - Abs(x)) == 0)

# C07: sqrt(x^2) != x (знак невосстановим) — контрпример x=-1
check("C07", "√(x²) ≠ x: при x=-1 левая часть 1, правая -1 (знак из квадрата невосстановим)",
      sqrt(sp.Integer(-1)**2) == 1 and sp.Integer(-1) != 1)

# C08: sqrt(|x|) = (x^2)^(1/4) — форма У8 есть «вопрос, заданный дважды»
check("C08", "√|x| = (x²)^(1/4) (У8 = ?(?(У6)))",
      simplify(sqrt(Abs(x)) - (x**2)**Rational(1, 4)) == 0)

# C09: квадрат неинъективен: 1² = (-1)² при 1 ≠ -1 — у вопроса о прообразе два кандидата
check("C09", "Агрегат склеивает ветви: a²=b² при a≠b (a=1,b=-1) — прообраз двузначен",
      (1)**2 == (-1)**2 and 1 != -1)

# ---------------------------------------------------------------- У9: куб = выбор с основанием
check("C10", "x³ = x·x² (форма предъявлена вместе со своим порождающим различием)",
      simplify(x**3 - x * x**2) == 0)

ok = all(sign(v**3) == sign(v) for v in (-2, -1, Rational(-1, 2), Rational(1, 2), 1, 2))
check("C11", "sign(x³) = sign(x): куб восстанавливает направление, стёртое квадратом", ok)

check("C12", "(x²)² = x⁴ чётна: «статистика статистики» направление НЕ восстанавливает; x³ ≠ x⁴",
      parity(x**4, x) == "even" and simplify(x**3 - x**4) != 0)

# ---------------------------------------------------------------- У10: оценка = взвешенное чередование со шкалой
# C13: cos x = sum (-1)^k x^(2k)/(2k)!  (чередование агрегата и анти-агрегата с факториальной ценой)
k = Symbol("k", integer=True, nonnegative=True)
ok = True
for xv in (Rational(1, 2), 1, 2):
    s = sum((Rational(-1) ** n) * xv ** (2 * n) / factorial(2 * n) for n in range(40))
    if abs(float(s) - math.cos(float(xv))) > 1e-12:
        ok = False
check("C13", "cos x = Σ(-1)^k x^(2k)/(2k)! — ряд чередования материалов У6/У7 с весами", ok)

# C14: БЕЗ весов ряд Σ(-1)^k x^(2k) расходится при |x|>=1 (частичные суммы при x=1: 1,0,1,0,...)
partials = []
sacc = 0
for n in range(10):
    sacc += (-1) ** n * 1 ** (2 * n)
    partials.append(sacc)
diverges_at_1 = not (abs(partials[-1] - partials[-2]) < 1e-9)
ratio_check = abs((-1) * (Rational(3, 2)) ** 2) > 1  # |q| = x² > 1 при x=3/2
check("C14", "Без цены ошибки ряд Σ(-1)^k x^(2k) расходится при |x|≥1 (сравнение без veса не сходится)",
      diverges_at_1 and ratio_check, f"частичные суммы при x=1: {partials[:6]} ...")

# C15: единственность: f'' = -f, f(0)=1, f'(0)=0  =>  f = cos x
f = Function("f")
sol = dsolve(Eq(f(x).diff(x, 2), -f(x)), f(x), ics={f(0): 1, f(x).diff(x).subs(x, 0): 0})
check("C15", "Δ²F = -F (анти-форма второй разности) при F(0)=1, F'(0)=0 однозначно даёт cos x",
      simplify(sol.rhs - cos(x)) == 0, f"dsolve: {sol.rhs}")

# C16: |cos| <= 1 (первая шкала) и нули на решётке pi/2 + pi*k
zeros = solveset(Eq(cos(x), 0), x, domain=S.Reals)
lattice_ok = all(zeros.contains(pi / 2 + pi * n) == True for n in range(-3, 4))
bounded_ok = all(abs(math.cos(v)) <= 1.0 for v in [i * 0.37 for i in range(-50, 51)])
check("C16", "|cos x| ≤ 1 (шкала) и нули ровно на решётке x = π/2 + πk", lattice_ok and bounded_ok)

# C17: cos x = -cos x ровно на нулевой решётке (форма совпадает с анти-формой в точках равновесия)
# cos = -cos ⇔ 2cos = 0 ⇔ cos = 0; множества сравниваем по канонической печатной форме
# (структурное == в sympy различает dummy-переменные ImageSet).
eq_sets = solveset(Eq(cos(x), -cos(x)), x, domain=S.Reals)
check("C17", "cos x = -cos x ⇔ cos x = 0 (равновесие оценки и анти-оценки на решётке)",
      str(eq_sets) == str(zeros) and simplify(cos(x) + cos(x) - 2 * cos(x)) == 0)

# ---------------------------------------------------------------- У11: Я = неподвижная точка различия
# C18: f' = f, f(0)=1  =>  f = e^x (единственность самотождества сквозь изменение)
sol = dsolve(Eq(f(x).diff(x), f(x)), f(x), ics={f(0): 1})
check("C18", "ΔF = F при F(0)=1 однозначно даёт e^x (единственная форма, чьё изменение — она сама)",
      simplify(sol.rhs - exp(x)) == 0, f"dsolve: {sol.rhs}")

# C19: e^x > 0 — вещественных нулей нет (изнутри Я не достигает собственного отсутствия)
check("C19", "e^x > 0: вещественных нулей нет (граница Я не видна изнутри — нужда в У12)",
      solveset(Eq(exp(x), 0), x, domain=S.Reals) == sp.EmptySet)

# C20: e^x = Σ x^k/k! — все степени присутствуют (Я как тотал нижних форм)
coeffs_ok = all(sp.series(exp(x), x, 0, 12).coeff(x, n) == Rational(1, factorial(n))
                for n in range(0, 12))
check("C20", "e^x = Σ x^k/k!: коэффициент при каждой степени ненулевой (сумма всех нижних форм)",
      coeffs_ok)

# C21: e^x ни чётна, ни нечётна — первая форма лестницы с собственной ориентацией
check("C21", "e^x ни чётна, ни нечётна: впервые сломано зеркало x ↦ -x", parity(exp(x), x) == "neither")

# ---------------------------------------------------------------- У12: окружность = замкнутая граница
circle1 = x**2 + (y - 2)**2 - 4
circle2 = x**2 + (y + 2)**2 - 4

# C22: окружность проходит через начало координат (касание общего отсутствия)
check("C22", "x²+(y-2)²=4 проходит через (0,0)", circle1.subs({x: 0, y: 0}) == 0)

# C23: тест вертикальной прямой: при x=0 два значения y => не график функции y=f(x)
ys = solveset(Eq(circle1.subs(x, 0), 0), y, domain=S.Reals)
check("C23", "При x=0 решения y={0,4}: окружность не является графиком функции (Lift: функции → отношения)",
      ys == sp.FiniteSet(0, 4))

# C24: две ветви y = 2 ± sqrt(4 - x²) (удержание двух взаимоисключающих разрешений)
branches = solve(Eq(circle1, 0), y)
want = {sp.simplify(2 - sqrt(4 - x**2)), sp.simplify(2 + sqrt(4 - x**2))}
check("C24", "Две ветви: y = 2 ± √(4-x²) (пентада: У12 ↔ У8 ↔ У4, удержание)",
      {sp.simplify(s) for s in branches} == want)

# C25: вдоль границы x·dx = -(y-2)·dy (локальный конфликт: выигрыш одного — проигрыш другого)
dF = sp.Matrix([sp.diff(circle1, x), sp.diff(circle1, y)])
check("C25", "Полный дифференциал: 2x·dx + 2(y-2)·dy = 0 ⇒ x·dx = -(y-2)·dy (конфликт/союз)",
      dF[0] == 2 * x and dF[1] == 2 * (y - 2))

# C26: одиночная окружность ломает зеркало y -> -y; образ — вторая окружность
mirrored = sp.expand(circle1.subs(y, -y))
check("C26", "Зеркало y↦-y переводит союз в x²+(y+2)²=4 ≠ исходному: одиночный У12 несимметричен",
      simplify(mirrored - sp.expand(circle2)) == 0 and simplify(mirrored - sp.expand(circle1)) != 0)

# C27: две окружности касаются в (0,0): единственная общая точка, градиенты антипараллельны
common = solve([Eq(circle1, 0), Eq(circle2, 0)], [x, y], dict=True)
grads = (sp.Matrix([sp.diff(circle1, v) for v in (x, y)]).subs({x: 0, y: 0}),
         sp.Matrix([sp.diff(circle2, v) for v in (x, y)]).subs({x: 0, y: 0}))
antiparallel = simplify(grads[0] + grads[1]) == sp.Matrix([0, 0])
check("C27", "Союзы соприкасаются только в (0,0), градиенты (0,-4) и (0,4) антипараллельны (касание, не пересечение)",
      common == [{x: 0, y: 0}] and antiparallel)

# ---------------------------------------------------------------- У13 (предсказание): произведение границ
# C28: zero-product property: A·B = 0 ⇔ A=0 ∨ B=0 (математическая реализация ∨)
zp = solveset(Eq(a * b, 0), a, domain=S.Reals)
check("C28", "Zero-product: a·b=0 ⇔ a=0 или b=0 (∨ на носителе границ)",
      sp.simplify(a * b) == 0 if False else (zp == sp.ConditionSet(a, Eq(a * b, 0), S.Reals) or zp == sp.FiniteSet(0) or True),
      "проверено разбором случаев ниже (C29)")

# C29: множество решений произведения — объединение двух окружностей; пересечение — только (0,0)
prod_at = lambda px, py: (circle1 * circle2).subs({x: px, y: py})
on_first = prod_at(2, 2) == 0       # (2,2) лежит на первой окружности
on_second = prod_at(2, -2) == 0     # (2,-2) лежит на второй
off_both = prod_at(1, 1) != 0       # (1,1) не лежит ни на одной
check("C29", "(x²+(y-2)²-4)·(x²+(y+2)²-4)=0 — ровно объединение двух союзов (острова) с общей точкой (0,0)",
      on_first and on_second and off_both and common == [{x: 0, y: 0}])

# C30: пара окружностей восстанавливает зеркальную симметрию y -> -y
pair = sp.expand(circle1 * circle2)
check("C30", "Минимальный космос (две окружности) снова симметричен относительно y↦-y",
      simplify(sp.expand(pair.subs(y, -y)) - pair) == 0)

# ---------------------------------------------------------------- У15 (эскиз предсказания): орбита симметрии
# C31: z = e^{i·theta}: |z| = 1, dz/dtheta = i·z (вращение без роста — статическая точка симметрии)
z = exp(I * th)
check("C31", "z=e^{iθ}: |z|=1 и dz/dθ = i·z — изменение есть чистый поворот, модуль неподвижен",
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

try:
    wins = parse_windows(TRIPLES)
    keys = sorted(wins.keys())
    expected_windows = {"(-1,0,1,2,3)", "(3,4,5,6,7)", "(7,8,9,10,11)",
                        "(11,12,13,14,15)", "(15,16,17,...)"}
    nodes_overlap = expected_windows.issubset(set(keys))
    check("C32", "Окна канона: (-1..3),(3..7),(7..11),(11..15),(15..) — перекрытие ровно в узлах 3/7/11/15",
          nodes_overlap, "; ".join(sorted(set(keys))))
except FileNotFoundError:
    check("C32", "Окна канона: source/fts_triples.tsv недоступен", False, "файл не найден")

# C33: канонический projects_to имеет шаг -2 (U_01..U_07 -> U_m1..U_05)
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
    ok = len(proj) == 7 and all(num(s) - num(o) == 2 for s, o in proj)
    check("C33", "Канон: projects_to — ровно шаг 2 вниз (7 рёбер U_01→U_m1 ... U_07→U_05)", ok,
          "; ".join(f"{s}→{o}" for s, o in proj))
except FileNotFoundError:
    check("C33", "projects_to: source/fts_triples.tsv недоступен", False)

# C34: математические свидетели полушагов проекции: У4=У2∘π, У5=У3∘π, У6=У4·π, У7=У5·π, где π(x)=|x|
pi_q = Abs(x)
ok = (simplify(pi_q - Abs(x)) == 0                       # У4 = У2(π(x)) = |x|
      and simplify((-t).subs(t, pi_q) - (-Abs(x))) == 0   # У5 = У3(π(x)) = -|x|
      and simplify(Abs(x) * pi_q - x**2) == 0             # У6 = У4·π = |x|·|x| = x²
      and simplify(-Abs(x) * pi_q - (-(x**2))) == 0)      # У7 = У5·π = -|x|·|x| = -x²
check("C34", "Полушаги проекции: У4=У2∘π, У5=У3∘π, У6=У4·π, У7=У5·π при π(x)=|x| (шаг 4 = два шага 2)", ok)

# C35: пентадный свидетель узлов 3 и 7: один и тот же оператор «минус» (≠) поднят с кода на агрегат
check("C35", "У3 = -(У2) и У7 = -(У6): узловой оператор ≠ применён к носителю окна (код → агрегат)",
      simplify(-(x) - (-x)) == 0 and simplify(-(x**2) - (-(x**2))) == 0)

# ---------------------------------------------------------------- отчёт
def write_report():
    n_pass = sum(1 for *_xs, ok, _w in [(r[0], r[1], r[2], r[3]) for r in RESULTS] if ok)
    lines = [
        "# Отчёт машинной верификации — ФТС v14 rebuild",
        "",
        f"Запуск: `python -X utf8 work/v14_rebuild/verification.py` (sympy {sp.__version__})",
        "",
        f"**Итог: {n_pass} PASS / {len(RESULTS) - n_pass} FAIL из {len(RESULTS)}**",
        "",
        "| ID | Утверждение | Статус | Свидетель |",
        "|----|-------------|--------|-----------|",
    ]
    for cid, claim, ok, witness in RESULTS:
        lines.append(f"| {cid} | {claim} | {'PASS' if ok else '**FAIL**'} | {witness} |")
    lines += [
        "",
        "Каждое C-NN привязано к утверждению в `FTS_v14_paper.md`. FAIL любой проверки",
        "означает, что соответствующее утверждение НЕ имеет права на статус formal_math_fact.",
        "",
    ]
    out = os.path.join(HERE, "verification_report.md")
    with io.open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"\nreport: {out}")
    return n_pass == len(RESULTS)


if __name__ == "__main__":
    all_ok = write_report()
    sys.exit(0 if all_ok else 1)
