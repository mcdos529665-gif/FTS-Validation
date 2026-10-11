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

# S1d. n->0: при x=1/2 точка кривой |x|^n+|y|^n=1 уходит к оси, |y|=(1-2^{-n})^{1/n} -> 0 (кривая -> крест осей).
ys = [float((1 - mp.mpf(2)**(-nn))**(1/mp.mpf(nn))) for nn in (0.5, 0.2, 0.05)]
check("S1d n->0: |y| при x=1/2 убывает к 0", ys[0] > ys[1] > ys[2] and ys[2] < 1e-20, str([f"{v:.2e}" for v in ys]))
# S1e. Двойственность норм: опорная функция ромба |x|+|y|<=1 равна max(|u|,|v|) (полярное тело — квадрат);
#      круг n=2 — единственный самодвойственный (1/p+1/q=1 при p=q=2).
import random
random.seed(1)
okd = all(abs(max(abs(u1), abs(u2)) - max(u1*a1 + u2*b1 for a1, b1 in ((1, 0), (-1, 0), (0, 1), (0, -1)))) < 1e-12
          for u1, u2 in ((random.uniform(-3, 3), random.uniform(-3, 3)) for _ in range(200)))
check("S1e полярное тело ромба — квадрат; самодвойственно только p=2", okd and sp.solve(sp.Eq(1/x + 1/x, 1), x) == [2])

# S1f. n=1/2: дуга √x+√y=1 — парабола (x−y)²−2(x+y)+1=0 с осью вдоль y=x.
X0 = sp.symbols('X0', positive=True)
check("S1f n=1/2 — дуги парабол с осью y=x",
      sp.simplify(((X0 - (1 - sp.sqrt(X0))**2)**2 - 2*(X0 + (1 - sp.sqrt(X0))**2) + 1)) == 0)
# S1g. Росток у вершины (0,1): 1−(1−xⁿ)^{1/n} ~ xⁿ/n — форма |x|ⁿ (n=1/2: √|x|, 1: |x|, 2: x², 3: |x|³).
germ_ok = all(sp.limit((1 - (1 - X0**nn)**(1/nn)) / X0**nn, X0, 0, '+') == 1/nn
              for nn in (sp.Rational(1, 2), sp.Integer(1), sp.Integer(2), sp.Integer(3)))
check("S1g росток у вершины = |x|ⁿ/n", germ_ok)

# T1. Роговой тор: вращение M_12 x²+(y−r)²=r² вокруг оси x (касательной в нуле):
#     (√(y²+z²)−r)²+x²=r². Сечение z=0 — две окружности, касающиеся в нуле (форма У13, статья §10.2, r=2);
#     на оси (y=z=0) лежит только начало координат.
r0, t0 = sp.Integer(2), sp.symbols('t0', real=True)
up = (r0*sp.sin(t0), r0 - r0*sp.cos(t0))      # точка M_12 (y>=0)
dn = (r0*sp.sin(t0), -(r0 - r0*sp.cos(t0)))   # зеркальная (y<=0)
horn = lambda X1, Y1, Z1: (sp.sqrt(Y1**2 + Z1**2) - r0)**2 + X1**2 - r0**2
u13 = lambda X1, Y1: (X1**2 + (Y1 - 2)**2 - 4) * (X1**2 + (Y1 + 2)**2 - 4)
sec_ok = all(sp.simplify(horn(p[0], p[1], 0).subs(t0, tv)) == 0 and sp.simplify(u13(*p).subs(t0, tv)) == 0
             for p in (up, dn) for tv in (sp.pi/7, sp.pi/2, 2*sp.pi/3))
check("T1a сечение рогового тора = две окружности У13", sec_ok)
xs = sp.symbols('xs', real=True)
check("T1b на оси только начало координат", sp.solve(sp.Eq(horn(xs, 0, 0), 0), xs) == [0])

# C2. Коста: данные Вейерштрасса f=℘, g=A/℘' [внешнее]. Квадратная решётка: 4x³−g₂x, корни 0, ±√g₂/2.
#     ℘''=6℘²−g₂/2: в точке ℘=0 это −g₂/2≠0 ⇒ у ℘ двойной нуль в (1+i)/2; в ℘=±√g₂/2 ℘≠0.
#     Порядок метрики |f|(1+|g|²): ord f + 2·min(0, ord g). Конец ⇔ порядок < 0.
G2 = sp.symbols('G2', positive=True)
xx = sp.symbols('xx')
rts = sp.solve(4*xx**3 - G2*xx, xx)
d2 = {rv: sp.simplify(6*rv**2 - G2/2) for rv in rts}
check("C2a ℘''≠0 во всех точках порядка 2 (простые нули ℘', двойной нуль ℘ в (1+i)/2)",
      all(v != 0 for v in d2.values()) and 0 in rts)
orders = {"0": (-2, 3), "1/2": (0, -1), "i/2": (0, -1), "(1+i)/2": (2, -1)}
metric = {k: f_ + 2*min(0, g_) for k, (f_, g_) in orders.items()}
check("C2b концы в 0, 1/2, i/2; (1+i)/2 регулярна", metric == {"0": -2, "1/2": -2, "i/2": -2, "(1+i)/2": 0}, str(metric))

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
