# Свидетель к figures_note_2026-10-11.md (вне общего маршрута).
# Запуск: py -3.11 -X utf8 work/v14_rebuild/figures_check_2026-10-11.py
import sympy as sp
import mpmath as mp

ok = []


def check(tag, cond, info=""):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + tag + (" — " + info if info else ""))


x, y, w = sp.symbols('x y w')

# S1. Суперэллипс |x|^n+|y|^n=1: поворот на 90° (x,y)->(y,-x) сохраняет кривую при любом n;
#     непрерывный поворот на угол a сохраняет её только при n=2 (проверка на a=pi/6, n=4).
n = sp.Integer(4)
f = lambda X, Y: X**4 + Y**4
check("S1a x^4+y^4 инвариантна при (x,y)->(y,-x)", sp.expand(f(y, -x) - f(x, y)) == 0)
a = sp.pi / 6
Xr, Yr = x*sp.cos(a) - y*sp.sin(a), x*sp.sin(a) + y*sp.cos(a)
check("S1b x^4+y^4 не инвариантна при повороте на 30°", sp.simplify(sp.expand(f(Xr, Yr) - f(x, y))) != 0)
check("S1c x^2+y^2 инвариантна при повороте на 30°", sp.simplify(sp.expand(Xr**2 + Yr**2 - x**2 - y**2)) == 0)

# S2. Комплексные кривые Ферма x^n+y^n=1: род (n-1)(n-2)/2 = 0,1,3 при n=2,3,4.
check("S2a род Ферма n=2,3,4 = 0,1,3", [(k-1)*(k-2)//2 for k in (2, 3, 4)] == [0, 1, 3])
# S2b. Кубика Ферма — шестиугольный тор: X=12/(x+y), Y=36(x-y)/(x+y) переводит x^3+y^3=1 в Y^2=X^3-432 (j=0).
X = 12/(x + y); Y = 36*(x - y)/(x + y)
expr = sp.expand(sp.together(Y**2 - X**3 + 432).as_numer_denom()[0])
check("S2b x^3+y^3=1 -> Y^2=X^3-432", sp.rem(sp.Poly(expr, y), sp.Poly(x**3 + y**3 - 1, y)).is_zero)
j = lambda A, B: sp.Rational(1728) * 4 * A**3 / (4 * A**3 + 27 * B**2)
check("S2c j(Y^2=X^3-432)=0", j(0, -432) == 0)

# S3. Суперэллипсоид |x|^p+|y|^p+|z|^p=1 при p=1 — октаэдр: chi = 6-12+8 = 2 (как XE-3 topo_chi_note).
check("S3 октаэдр chi=2", 6 - 12 + 8 == 2)

# C1. Квадратная решётка Z[i]: wp(iu)=-wp(u) => wp((1+i)/2)=0, wp(i/2)=-wp(1/2) (численно, решёточная сумма).
def wp(u, N=60):
    s = 1/u**2
    for m in range(-N, N+1):
        for k in range(-N, N+1):
            if m == 0 and k == 0:
                continue
            L = m + 1j*k
            s += 1/(u - L)**2 - 1/L**2
    return s
v0, v1, vi = wp(0.5+0.5j), wp(0.5), wp(0.5j)
check("C1a wp((1+i)/2)≈0", abs(v0) < 1e-3, str(v0))
check("C1b wp(i/2)≈-wp(1/2)", abs(vi + v1) < 1e-3, f"{v1.real:.6f}")
# (Следствие C1a–b: в координате x=wp кривой y^2=x^3-x точки порядка 2 — x∈{∞, e, −e, 0};
#  поворот u->iu, т.е. t: x->−x, меняет ±e местами и держит 0 и ∞.)

# H1. Тор Клиффорда |z1|=|z2| отображением Хопфа z1/z2 переходит в экватор |q|=1.
p, q = sp.symbols('p q', real=True)
check("H1 |Hopf(Clifford)|=1", sp.simplify(sp.Abs(sp.exp(sp.I*p)/sp.exp(sp.I*q))) == 1)

# G1. Вершины куба (±1,±1,±1)/√3 при стереографической проекции — корни w^8+14w^4+1.
pts = [(sp.Integer(a1) + sp.I*b1)/sp.sqrt(3)/(1 - sp.Integer(c1)/sp.sqrt(3))
       for a1 in (1, -1) for b1 in (1, -1) for c1 in (1, -1)]
poly = sp.nsimplify(sp.simplify(sp.expand(sp.prod([w - t for t in pts]))))
check("G1 вершины куба -> w^8+14w^4+1", sp.expand(poly - (w**8 + 14*w**4 + 1)) == 0)
# G2. Угол Бонне гироида: arctan(K(1/4)/K(3/4)) ≈ 38.0148°.
th = mp.degrees(mp.atan(mp.ellipk(0.25)/mp.ellipk(0.75)))
check("G2 угол Бонне ≈ 38.0148°", abs(th - 38.0147739891) < 1e-8, str(th))

print(f"\n{sum(ok)}/{len(ok)} PASS")
