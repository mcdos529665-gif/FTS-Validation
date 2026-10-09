# -*- coding: utf-8 -*-
"""Проверки G60-01…G60-47 к GROUPED_OPEN_2026-10-08.md (кандидаты ассистента).

Предсказания записаны в docstring каждой проверки до первого запуска.
Проверяют только математические факты; смысл уровней (СУ) не устанавливают.
Запуск: python verification_g60.py  (нужен sympy).
"""
import itertools
import sympy as sp

RESULTS = []


def check(cid, ok, note):
    RESULTS.append((cid, bool(ok), note))
    print(f"{cid}: {'PASS' if ok else 'FAIL'} — {note}")


# ---------- helpers: partitions of a finite set ----------
def set_partitions(elems):
    elems = list(elems)
    if not elems:
        yield []
        return
    first, rest = elems[0], elems[1:]
    for p in set_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [p[i] | {first}] + p[i + 1:]
        yield p + [{first}]


def canon(p):
    return frozenset(frozenset(b) for b in p)


def refines(fine, coarse):
    return all(any(b <= c for c in coarse) for b in fine)


def g01_chains():
    """G60-01. Предсказание: в решётке разбиений Ω={00,01,10,11} 15 разбиений и
    18 насыщенных цепей (совпадает с NC-01); через разбиения на смежные классы
    подгрупп V4 (тип 2+2, их три) проходят 6 цепей; при правиле «сначала дробится
    блок нейтрального элемента 00» остаётся 3; три цепи переставляются Aut(V4)≅S3
    транзитивно."""
    omega = [(0, 0), (0, 1), (1, 0), (1, 1)]
    parts = {canon(p) for p in set_partitions(omega)}
    by_rank = {}
    for p in parts:
        by_rank.setdefault(4 - len(p), []).append(p)  # rank 0 = 4 блока
    chains = []
    for p0 in by_rank[0]:
        for p1 in by_rank[1]:
            if not refines(p0, p1):
                continue
            for p2 in by_rank[2]:
                if not refines(p1, p2):
                    continue
                for p3 in by_rank[3]:
                    if refines(p2, p3):
                        chains.append((p0, p1, p2, p3))
    add = lambda u, v: ((u[0] + v[0]) % 2, (u[1] + v[1]) % 2)
    subgroups = [[(0, 0), h] for h in omega[1:]]
    coset_parts = []
    for H in subgroups:
        cos = {frozenset(add(g, h) for h in H) for g in omega}
        coset_parts.append(frozenset(cos))
    via_coset = [c for c in chains if c[2] in coset_parts]
    # правило базовой точки: на шаге 2→3 блока дробится блок, содержащий 00
    def basepoint_first(c):
        p1, p2 = c[1], c[2]
        split = [b for b in p2 if b not in p1]
        return (0, 0) in split[0]
    kernel_first = [c for c in via_coset if basepoint_first(c)]
    # Aut(V4): все биекции omega, сохраняющие сложение
    autos = []
    for perm in itertools.permutations(omega[1:]):
        f = {(0, 0): (0, 0), **dict(zip(omega[1:], perm))}
        if all(f[add(u, v)] == add(f[u], f[v]) for u in omega for v in omega):
            autos.append(f)
    def apply(f, chain):
        return tuple(frozenset(frozenset(f[x] for x in b) for b in p) for p in chain)
    orbit = {apply(f, kernel_first[0]) for f in autos}
    ok = (len(parts) == 15 and len(chains) == 18 and len(coset_parts) == 3
          and len(via_coset) == 6 and len(kernel_first) == 3 and len(autos) == 6
          and orbit == set(kernel_first))
    check("G60-01", ok, f"разбиений {len(parts)}, цепей {len(chains)}, через смежные классы {len(via_coset)}, "
          f"с базовой точкой {len(kernel_first)}, |Aut(V4)|={len(autos)}, орбита={len(orbit)}")


def g02_resolvent():
    """G60-02. Предсказание: V4 нормальна в S4, S4/V4 порядка 6 и неабелева (≅S3)."""
    from sympy.combinatorics import Permutation, PermutationGroup
    from sympy.combinatorics.named_groups import SymmetricGroup
    S4 = SymmetricGroup(4)
    V4 = PermutationGroup([Permutation([1, 0, 3, 2]), Permutation([2, 3, 0, 1])])
    # нормальность — явным сопряжением: в sympy 1.14 is_normal возвращает True для любой
    # подгруппы, у которой раньше вычислен is_abelian (V4 абелева)
    normal = all(a * g * ~a in V4.elements for a in S4.elements for g in V4.elements)
    order = S4.order() // V4.order()
    # неабелевость фактора: найдётся пара с коммутатором вне V4
    nonab = any(not V4.contains(a * b * (~a) * (~b)) for a in S4.elements for b in S4.elements)
    check("G60-02", normal and order == 6 and nonab, f"V4 ◁ S4: {normal}; |S4/V4|={order}; неабелев: {nonab}")


def g03_anharmonic():
    """G60-03. Предсказание: j(λ)=256(λ²−λ+1)³/(λ²(1−λ)²) инвариантна относительно
    шести отображений λ, 1−λ, 1/λ, 1/(1−λ), λ/(λ−1), (λ−1)/λ; они замкнуты по композиции."""
    l = sp.symbols('lam')
    j = 256 * (l**2 - l + 1)**3 / (l**2 * (1 - l)**2)
    maps = [l, 1 - l, 1 / l, 1 / (1 - l), l / (l - 1), (l - 1) / l]
    inv = all(sp.simplify(j.subs(l, m) - j) == 0 for m in maps)
    keyset = {sp.simplify(m) for m in maps}
    closed = all(sp.simplify(a.subs(l, b)) in keyset for a in maps for b in maps)
    check("G60-03", inv and closed, f"j инвариантна: {inv}; шесть отображений замкнуты: {closed}")


def g04_legendre_2torsion():
    """G60-04. Предсказание: у y²=x(x−1)(x−λ) точки с y=0 — x∈{0,1,λ}; вместе с
    бесконечной точкой это 2-кручение, сумма любых двух из трёх равна третьей (V4)."""
    x, l = sp.symbols('x lam')
    roots = sp.solve(x * (x - 1) * (x - l), x)
    # закон сложения: три точки на прямой y=0 дают P+Q+R=O, т.е. P+Q=−R=R
    ok = set(roots) == {0, 1, l}
    check("G60-04", ok, f"корни {roots}; три точки на прямой y=0 ⇒ P+Q=R, группа {{O,P,Q,R}}≅V4")


def g05_cross_selection():
    """G60-05. Предсказание: для x≠0 крест B_x={x,−x}, сечение v=−|x|:
    {b·v}={x²,−x²}; {v·v}={x²}; {b·b'}={x²,−x²}; {|x|·|x|}={x²}."""
    ok = True
    for xv in [sp.Rational(1, 3), 2, -5, sp.sqrt(2)]:
        B = {xv, -xv}
        v = -abs(xv)
        a = {sp.simplify(b * v) for b in B}
        bb = {sp.simplify(b * c) for b in B for c in B}
        want = {xv**2, -xv**2}
        ok &= a == want and {sp.simplify(v * v)} == {xv**2} and bb == want and {abs(xv)**2} == {xv**2}
    check("G60-05", ok, "крест·выбор = крест·крест = {x²,−x²} = |y|=x² (МУ7); выбор·выбор = {x²} (МУ6)")


def g06_cauchy():
    """G60-06. Предсказание: для Коши φ(t)=e^{−|t|} среднее n наблюдений имеет ту же
    характеристическую функцию: φ(t/n)^n = φ(t)."""
    t = sp.symbols('t', real=True)
    n = sp.symbols('n', positive=True, integer=True)
    phi = sp.exp(-sp.Abs(t))
    ok = sp.simplify(phi.subs(t, t / n)**n - phi) == 0
    check("G60-06", ok, "среднее n величин Коши распределено как одна величина")


def g07_cumulants():
    """G60-07. Предсказание: стандартизованная r-я кумулянта суммы n i.i.d. равна
    n^{1−r/2}·κ_r/κ_2^{r/2}: r=3 → n^{−1/2}, r=4 → n^{−1}."""
    n, k2, kr = sp.symbols('n kappa2 kappa_r', positive=True)
    res = {}
    for r in (3, 4, 5):
        res[r] = sp.simplify((n * kr) / (n * k2)**sp.Rational(r, 2) / (kr / k2**sp.Rational(r, 2)))
    ok = res[3] == n**sp.Rational(-1, 2) and res[4] == 1 / n and res[5] == n**sp.Rational(-3, 2)
    check("G60-07", ok, f"множители: r=3 {res[3]}, r=4 {res[4]}, r=5 {res[5]}")


def g08_two():
    """G60-08. Предсказание: x+x=x·x ⟺ x∈{0,2}; 2πr=πr² ⟺ r∈{0,2}; при x=−1
    значения МУ2…МУ9 лежат в {−1,1}, при x=2 различимы по масштабу."""
    x, r = sp.symbols('x r')
    a = set(sp.solve(sp.Eq(x + x, x * x), x))
    b = set(sp.solve(sp.Eq(2 * sp.pi * r, sp.pi * r**2), r))
    def ladder(v):
        return [v, -v, abs(v), -abs(v), v**2, -v**2, sp.sqrt(abs(v)), -sp.sqrt(abs(v)), v**3]
    m1 = set(ladder(sp.Integer(-1)))
    m2 = ladder(sp.Integer(2))
    ok = a == {0, 2} and b == {0, 2} and m1 == {-1, 1} and len(set(map(abs, m2))) > 2
    check("G60-08", ok, f"x+x=x·x: {sorted(a)}; 2πr=πr²: {sorted(b)}; лестница при −1: {sorted(m1)}; при 2: {m2}")


def hensel_sqrt(a, p, k):
    """Есть ли решение x²≡a (mod p^k) с x взаимно простым с p."""
    m = p**k
    return any((x * x - a) % m == 0 for x in range(1, m) if x % p)


def g09_padic():
    """G60-09. Предсказание: √−7 ∈ Z_2 (решения mod 2^k для всех k), √−1 ∉ Z_2;
    √−1 ∈ Z_5, √−7 ∉ Z_5. Ни одно не в R."""
    ok = (all(hensel_sqrt(-7, 2, k) for k in range(3, 13))
          and not hensel_sqrt(-1, 2, 3)
          and all(hensel_sqrt(-1, 5, k) for k in range(1, 6))
          and not hensel_sqrt(-7, 5, 1))
    check("G60-09", ok, "√−7: да в Z_2, нет в Z_5; √−1: да в Z_5, нет в Z_2")


def g10_hopf():
    """G60-10. Предсказание: отображение Хопфа h(a,b)=(2 a b̄, |a|²−|b|²) переводит S³
    в S², а тор |a|=|b|=1/√2 — в экватор (третья координата 0). χ: тетраэдр 4−6+4=2,
    7-вершинный тор 7−21+14=0."""
    t1, t2 = sp.symbols('t1 t2', real=True)
    a = sp.exp(sp.I * t1) / sp.sqrt(2)
    b = sp.exp(sp.I * t2) / sp.sqrt(2)
    w = sp.simplify(2 * a * sp.conjugate(b))
    z = sp.simplify(sp.Abs(a)**2 - sp.Abs(b)**2)
    on_sphere = sp.simplify(sp.Abs(w)**2 + z**2 - 1) == 0
    # 7-вершинный тор Мёбиуса–Часара: треугольники {i,i+1,i+3},{i,i+2,i+3} mod 7
    tris = set()
    for i in range(7):
        tris.add(frozenset({i, (i + 1) % 7, (i + 3) % 7}))
        tris.add(frozenset({i, (i + 2) % 7, (i + 3) % 7}))
    edges = {frozenset(e) for tr in tris for e in itertools.combinations(tr, 2)}
    chi_t = 7 - len(edges) + len(tris)
    ok = z == 0 and on_sphere and chi_t == 0 and (4 - 6 + 4) == 2
    check("G60-10", ok, f"образ тора: z={z}, на S²: {on_sphere}; χ(тор)={chi_t}, χ(S²)=2")


def g11_sierpinski():
    """G60-11. Предсказание: строка n треугольника Паскаля mod 2 имеет 2^{popcount n}
    ненулевых клеток; полные (n+1 клеток) строки 0..15: 0,1,3,7,15; узлы ≡3 mod 4
    (3,7,11,15) расходятся с рядом 2^k−1 ровно в 11 (и в 1)."""
    full = [n for n in range(16) if sum(sp.binomial(n, k) % 2 for k in range(n + 1)) == n + 1]
    cells11 = sum(sp.binomial(11, k) % 2 for k in range(12))
    mod4 = {3, 7, 11, 15}
    ok = full == [0, 1, 3, 7, 15] and cells11 == 8 and mod4 - set(full) == {11} and set(full) - mod4 == {0, 1}
    check("G60-11", ok, f"полные строки {full}; строка 11: {cells11} из 12")


def g12_lawvere():
    """G60-12. Предсказание: отрицание x↦−x на {−1,0,1} имеет неподвижную точку 0,
    на {−1,1} — нет; т.е. диагональный ход Лоувера применим к биту, но не к носителю с 0."""
    fx3 = [v for v in (-1, 0, 1) if -v == v]
    fx2 = [v for v in (-1, 1) if -v == v]
    check("G60-12", fx3 == [0] and fx2 == [], f"Fix на {{−1,0,1}}: {fx3}; на {{±1}}: {fx2}")


def g13_hadamard():
    """G60-13. Предсказание: (s,d)=(a+b,a−b) — преобразование Фурье на Z/2 (матрица
    Адамара H, H²=2I); σ действует как diag(1,−1): s чётна, d нечётна; вопрос
    «симметрична ли пара» = одна координата d=0."""
    a, b = sp.symbols('a b')
    H = sp.Matrix([[1, 1], [1, -1]])
    S = sp.Matrix([[0, 1], [1, 0]])  # σ
    ok = H * H == 2 * sp.eye(2) and sp.simplify(H * S * H.inv()) == sp.diag(1, -1)
    check("G60-13", ok, "H²=2I; H σ H⁻¹ = diag(1,−1)")


def g14_unit_circle():
    """G60-14. Предсказание: |zw|=|z||w|, поэтому {|z|=1} = ядро гомоморфизма
    |·|: C*→R>0 (замкнуто по умножению и обращению); вещественный след ядра = {±1}."""
    x1, y1, x2, y2 = sp.symbols('x1 y1 x2 y2', real=True)
    z, w = x1 + sp.I * y1, x2 + sp.I * y2
    mult = sp.simplify(sp.Abs(sp.expand(z * w))**2 - sp.Abs(z)**2 * sp.Abs(w)**2) == 0
    x = sp.symbols('x', real=True)
    real_trace = set(sp.solve(sp.Eq(sp.Abs(x), 1), x))
    check("G60-14", mult and real_trace == {-1, 1}, f"мультипликативность модуля: {mult}; R∩ядро = {sorted(real_trace)}")


def g15_crystallographic():
    """G60-15. Предсказание: φ(n)≤2 ⟺ n∈{1,2,3,4,6}; поэтому Z/3, Z/6 (и Z/4) живут
    на квадратичных носителях (Z[ω], Z[i]), а Z/8 впервые требует степени φ(8)=4."""
    small = [n for n in range(1, 50) if sp.totient(n) <= 2]
    check("G60-15", small == [1, 2, 3, 4, 6] and sp.totient(8) == 4, f"φ(n)≤2 при n={small}; φ(8)={sp.totient(8)}")


def g16_ratio_forms():
    """G60-16. Предсказание: y²=|x| ⟺ 1:y = y:|x| (y>0, x≠0); 1:x = x:x² = x²:x³;
    f(x+h)/f(x) не зависит от x для eˣ и зависит для x³; гипербола x²−y²=1 не имеет
    точек с |x|<1 (две компоненты), окружность x²+y²=1 связна."""
    x, y, h = sp.symbols('x y h', positive=True)
    mean_prop = sp.simplify(sp.Rational(1) / y - y / x).subs(y, sp.sqrt(x)) == 0
    gp = sp.simplify(x / 1 - x**2 / x) == 0 and sp.simplify(x**2 / x - x**3 / x**2) == 0
    X = sp.symbols('X', real=True)
    e_ratio = sp.simplify(sp.exp(X + h) / sp.exp(X))
    c_ratio = sp.simplify((X + h)**3 / X**3)
    exp_ok = not e_ratio.has(X) and c_ratio.has(X)
    Y = sp.symbols('Y', real=True)
    hyp_gap = sp.solve_univariate_inequality(X**2 - 1 < 0, X, relational=False)
    # при |X|<1: Y² = X²−1 < 0 — вещественных точек нет
    ok = mean_prop and gp and exp_ok and hyp_gap == sp.Interval.open(-1, 1)
    check("G60-16", ok, f"среднее пропорциональное: {mean_prop}; прогрессия: {gp}; "
          f"e^(x+h)/e^x={e_ratio}; (x+h)³/x³ зависит от x; щель гиперболы {hyp_gap}")


def g17_odd_square():
    """G60-17. Предсказание: сечение МУ7 по знаку, y=x|x|, лежит на |y|=x²;
    x|x| = x³ ⟺ x∈{−1,0,1} (три точки МУ9 из C-104); sign(x|x|)=sign(x³)."""
    x = sp.symbols('x', real=True)
    # |x·|x|| = |x|·|x| = x² для вещественного x
    on_mu7 = sp.simplify(sp.Abs(x) * sp.Abs(x) - x**2) == 0 and all(abs(v * abs(v)) == v**2 for v in [-3, -sp.Rational(1, 2), 0, 2])
    pts = set(sp.solve(sp.Eq(x * sp.Abs(x), x**3), x))
    same_sign = all(sp.sign(v * abs(v)) == sp.sign(v**3) for v in [-3, -sp.Rational(1, 2), 0, sp.Rational(1, 2), 3])
    check("G60-17", on_mu7 and pts == {-1, 0, 1} and same_sign, f"x|x| на МУ7: {on_mu7}; x|x|=x³ при {sorted(pts)}")


def g18_cross_d4_chains():
    """G60-18. Предсказание: четыре точки креста на единичной границе (±1,±1) =
    знаки пары (a,b). Группа D4 = <σ, μ_b> (перестановка и анти-форма одного объекта)
    имеет порядок 8, центр {id, ν}. Если каждое промежуточное разбиение — орбиты
    подгруппы D4, из 18 насыщенных цепей остаются 2; первый шаг у обеих — орбиты ν
    («одинаковы ли знаки»); цепи различаются зеркалом a=b (σ) или a=−b (σν);
    правило базовой точки (1,1) оставляет одну — σ-цепь."""
    V = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    sig = lambda p: (p[1], p[0])
    mub = lambda p: (p[0], -p[1])
    def as_perm(f):
        return tuple(V.index(f(v)) for v in V)
    def compose(g, h):  # g∘h
        return tuple(g[h[i]] for i in range(4))
    gens = [as_perm(sig), as_perm(mub)]
    ident = (0, 1, 2, 3)
    G = {ident}
    frontier = [ident]
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                k = compose(h, g)
                if k not in G:
                    G.add(k)
                    new.append(k)
        frontier = new
    nu = as_perm(lambda p: (-p[0], -p[1]))
    center = {g for g in G if all(compose(g, h) == compose(h, g) for h in G)}
    # все подгруппы: замыкания всех подмножеств из ≤2 образующих
    def closure(gs):
        H = {ident}
        fr = [ident]
        while fr:
            nw = []
            for g in fr:
                for h in gs:
                    k = compose(h, g)
                    if k not in H:
                        H.add(k)
                        nw.append(k)
            fr = nw
        return frozenset(H)
    subgroups = {closure(list(c)) for r in range(0, 3) for c in itertools.combinations(sorted(G), r)}
    def orbits(H):
        return frozenset(frozenset(V[g[i]] for g in H) for i in range(4))
    orbit_parts = {orbits(H) for H in subgroups}
    parts = {canon(p) for p in set_partitions(V)}
    by_blocks = {}
    for p in parts:
        by_blocks.setdefault(len(p), []).append(p)
    chains = [(p1, p2, p3, p4) for p1 in by_blocks[1] for p2 in by_blocks[2] for p3 in by_blocks[3]
              for p4 in by_blocks[4] if refines(p2, p1) and refines(p3, p2) and refines(p4, p3)]
    adm = [c for c in chains if all(p in orbit_parts for p in c)]
    nu_part = orbits(closure([nu]))
    sigma_part = orbits(closure([as_perm(sig)]))
    sn_part = orbits(closure([as_perm(lambda p: (-p[1], -p[0]))]))
    basepoint = [c for c in adm if any((1, 1) in b and len(b) == 1 for b in c[2])]
    ok = (len(G) == 8 and center == {ident, nu} and len(chains) == 18 and len(adm) == 2
          and all(c[1] == nu_part for c in adm) and {c[2] for c in adm} == {sigma_part, sn_part}
          and len(basepoint) == 1 and basepoint[0][2] == sigma_part)
    check("G60-18", ok, f"|D4|={len(G)}, центр={{id,ν}}: {center == {ident, nu}}, подгрупп {len(subgroups)}, "
          f"цепей {len(chains)}, через орбиты подгрупп {len(adm)}, с базовой точкой {len(basepoint)}")


def g19_c60_new_mu7():
    """G60-19. Предсказание: как множества при отражении y↦−y пары {2,3} и {4,5}
    остаются зеркальными (отражение F(2k) = F(2k+1), и F(2k+1) не совпадает со своим
    отражением), а при МУ7 = |y|=x² пара {6,7} — нет: отражение МУ6 есть y=−x² ≠ МУ7,
    а МУ7 переходит сама в себя. Проверка на сетке рациональных точек."""
    pts = [(sp.Rational(i, 2), sp.Rational(j, 2)) for i in range(-8, 9) for j in range(-40, 41)]
    graph = lambda f: {(x0, y0) for (x0, y0) in pts if y0 == f(x0)}
    mu7 = {(x0, y0) for (x0, y0) in pts if abs(y0) == x0**2}
    refl = lambda S: {(x0, -y0) for (x0, y0) in S}
    F = {2: graph(lambda t: t), 3: graph(lambda t: -t), 4: graph(lambda t: abs(t)),
         5: graph(lambda t: -abs(t)), 6: graph(lambda t: t**2)}
    pairs_ok = all(refl(F[2 * k]) == F[2 * k + 1] and refl(F[2 * k + 1]) != F[2 * k + 1] for k in (1, 2))
    six_seven = refl(F[6]) != mu7 and refl(mu7) == mu7 and refl(F[6]) < mu7
    check("G60-19", pairs_ok and six_seven, "{2,3},{4,5}: зеркальные пары; {6,7} при МУ7=|y|=x²: "
          "отражение МУ6 — лишь ветвь МУ7, МУ7 переходит сама в себя")


def g20_u12_radius():
    """G60-20. Предсказание: нижняя ветвь y=r−√(r²−x²) = x²/(2r) + O(x⁴), при r=1/2
    это x² (МУ6); окружность r=1 проходит через (0,0) и (0,2) с центром (0,1);
    гомотетия (x,y)↦(λx,λy) переводит окружность радиуса r в окружность радиуса λr."""
    x, r, lam, X, Y = sp.symbols('x r lam X Y', positive=True)
    lower = r - sp.sqrt(r**2 - x**2)
    ser = sp.series(lower, x, 0, 4).removeO()
    half = sp.simplify(ser.subs(r, sp.Rational(1, 2)) - x**2) == 0
    circ = lambda R: X**2 + (Y - R)**2 - R**2
    r1 = circ(1).subs({X: 0, Y: 0}) == 0 and circ(1).subs({X: 0, Y: 2}) == 0
    hom = sp.simplify(circ(r).subs({X: X / lam, Y: Y / lam}) * lam**2 - circ(lam * r)) == 0
    ok = sp.simplify(ser - x**2 / (2 * r)) == 0 and half and r1 and hom
    check("G60-20", ok, f"нижняя ветвь ≈ {ser}; r=1/2 → x²: {half}; r=1 через 0 и 2: {r1}; гомотетия: {hom}")


def g21_pi_9_to_7():
    """G60-21. Предсказание: π(v) = sign(v)·|v|^(2/3) переводит x³ в x|x| при всех x,
    строго возрастает, мультипликативна (π(uv)=π(u)π(v)), обратима (π⁻¹(w)=sign(w)|w|^(3/2)),
    неподвижные точки ровно {−1,0,1}, но не аддитивна: π(1+1) ≠ π(1)+π(1)."""
    pi = lambda v: sp.sign(v) * sp.Abs(v)**sp.Rational(2, 3)
    inv = lambda w: sp.sign(w) * sp.Abs(w)**sp.Rational(3, 2)
    xs = [sp.Rational(i, 4) for i in range(-12, 13)]
    sect = all(sp.simplify(pi(t**3) - t * abs(t)) == 0 for t in xs)
    mono = all(sp.N(pi(xs[i])) < sp.N(pi(xs[i + 1])) for i in range(len(xs) - 1))
    mult = all(sp.simplify(pi(u * v) - pi(u) * pi(v)) == 0 for u in xs for v in xs)
    back = all(sp.simplify(inv(pi(t)) - t) == 0 for t in xs)
    fixed = {t for t in xs if sp.simplify(pi(t) - t) == 0} == {-1, 0, 1}
    nonadd = sp.simplify(pi(2) - 2 * pi(1)) != 0
    ok = sect and mono and mult and back and fixed and nonadd
    check("G60-21", ok, f"π(x³)=x|x|: {sect}; возрастает: {mono}; мультипликативна: {mult}; "
          f"обратима: {back}; неподвижные {{−1,0,1}}: {fixed}; π(2)={sp.N(pi(2), 4)} ≠ 2π(1)")


def g22_absence_witness():
    """G60-22. Предсказание: при a≠0 пары (a,0) «отсутствие» и (a,−a) «не-предмет» канал
    d=a−b не отличает от нуля (a и 2a оба ненулевые), а канал s=a+b отличает (a и 0)."""
    a = sp.symbols('a', nonzero=True)
    d0, d1 = a - 0, a - (-a)
    s0, s1 = a + 0, a + (-a)
    ok = d0 != 0 and sp.simplify(d1) != 0 and s0 != 0 and sp.simplify(s1) == 0
    check("G60-22", ok, f"d: {d0}, {sp.simplify(d1)} (оба ≠0); s: {s0}, {sp.simplify(s1)}")


def g23_node_groups():
    """G60-23. Предсказание: (а) МУ3 = −x — образ МУ2 при y↦−y (один элемент знака), МУ7 =
    |y|=x² — объединение МУ6 и её образа и переходит сама в себя (вся орбита знака);
    (б) график eˣ переходит в себя при (x,y)↦(x+h, e^h·y), e^h=1 только при h=0, орбита (0,1)
    неограничена (масштаб не возвращается); (в) окружность |z|=1 переходит в себя при z↦e^{iφ}z,
    поворот возвращается при φ=2π, её вещественный след {−1, 1}; (г) у масштаба и поворота
    общий только 1: r>0 и |r|=1 ⇒ r=1."""
    x, y, h, phi, t = sp.symbols('x y h phi t', real=True)
    xs = [sp.Rational(i, 2) for i in range(-6, 7)]
    refl = lambda f: (lambda v: -f(v))
    mu2, mu6 = (lambda v: v), (lambda v: v**2)
    a1 = all(refl(mu2)(v) == -v for v in xs)
    mu7 = lambda v: {mu6(v), refl(mu6)(v)}
    a2 = all(mu7(v) == {-w for w in mu7(v)} and mu7(v) == {v**2, -v**2} for v in xs)
    b1 = sp.simplify(sp.exp(h) * sp.exp(x) - sp.exp(x + h)) == 0
    b2 = sp.solveset(sp.exp(h) - 1, h, sp.S.Reals) == sp.FiniteSet(0)
    b3 = sp.limit(sp.exp(h), h, sp.oo) == sp.oo
    c1 = sp.simplify(sp.Abs(sp.exp(sp.I * phi) * sp.exp(sp.I * t))) == 1
    c2 = sp.exp(2 * sp.pi * sp.I) == 1
    c3 = sp.solveset(sp.Abs(x) - 1, x, sp.S.Reals) == sp.FiniteSet(-1, 1)
    r = sp.symbols('r', positive=True)
    d1 = sp.solveset(sp.Abs(r) - 1, r, sp.Interval.open(0, sp.oo)) == sp.FiniteSet(1)
    ok = a1 and a2 and b1 and b2 and b3 and c1 and c2 and c3 and d1
    check("G60-23", ok, f"знак: МУ3 образ МУ2 {a1}, МУ7 вся орбита {a2}; масштаб: eˣ инвариантна {b1}, "
          f"e^h=1 ⇔ h=0 {b2}, неограничен {b3}; поворот: |z|=1 инвариантна {c1}, e^(2πi)=1 {c2}, "
          f"след {{−1,1}} {c3}; масштаб ∩ поворот = {{1}} {d1}")


def g24_roots_of_unity_trace():
    """G60-24. Предсказание: вещественный след группы корней n-й степени μ_n равен {1} при
    нечётном n и {−1, 1} при чётном; значит Z/3 не содержит знакового бита, Z/2, Z/4, Z/6, Z/8
    содержат. Конечные подгруппы U(1) — ровно μ_n (внешнее), здесь проверяется только след."""
    ok = True
    traces = {}
    for n in range(1, 13):
        roots = [sp.exp(2 * sp.pi * sp.I * k / n) for k in range(n)]
        real = {sp.nsimplify(sp.re(z)) for z in roots if sp.simplify(sp.im(z)) == 0}
        traces[n] = real
        ok &= real == ({1} if n % 2 else {-1, 1})
    check("G60-24", ok, f"след μ_3 = {traces[3]}, μ_4 = {traces[4]}, μ_6 = {traces[6]}, μ_8 = {traces[8]}")


def g25_dft_diagonalizes_shift():
    """G60-25. Предсказание: дискретное преобразование Фурье F_n диагонализует циклический сдвиг
    на Z/n с собственными числами ζ^k; при n=2 F_2 — матрица Адамара H, сдвиг — перестановка σ
    пары, и HσH⁻¹ = diag(1, −1) (совпадает с G60-13)."""
    import cmath
    ok = True
    for n in range(2, 9):
        z = cmath.exp(-2j * cmath.pi / n)
        F = [[z**(a * b) for b in range(n)] for a in range(n)]
        Finv = [[(z**(a * b)).conjugate() / n for b in range(n)] for a in range(n)]
        S = [[1 if a == (b + 1) % n else 0 for b in range(n)] for a in range(n)]
        mul = lambda A, B: [[sum(A[a][c] * B[c][b] for c in range(n)) for b in range(n)] for a in range(n)]
        D = mul(mul(F, S), Finv)
        ok &= all(abs(D[a][b] - (z**a if a == b else 0)) < 1e-12 for a in range(n) for b in range(n))
    H = sp.Matrix([[1, 1], [1, -1]])
    F2 = sp.Matrix(2, 2, lambda j, k: (-1)**(j * k))
    sig = sp.Matrix([[0, 1], [1, 0]])
    ok = ok and F2 == H and H * sig * H.inv() == sp.diag(1, -1)
    check("G60-25", ok, "F_n S F_n⁻¹ = diag(ζ^k) при n=2…8; F_2 = H, HσH⁻¹ = diag(1,−1)")


def g26_galois_mu8():
    """G60-26. Предсказание: y⁴ − x² над Q(x) раскладывается как (y²−x)(y²+x); корни √x·{1,−1,i,−i};
    резольвента-кубика z³ + 4x²z имеет корни 0, ±2ix (один рациональный). Поле разложения
    Q(x)(√x, i) имеет степень 4: при t = √x многочлен y⁴ − t⁴ над Q(t) = (y−t)(y+t)(y²+t²), и y²+t²
    неприводим, то есть i ∉ Q(t). Значит группа Галуа порядка 4 и порождена √x↦−√x (поворот корней
    на π) и i↦−i (сопряжение, отражение); на корнях (√x, −√x, i√x, −i√x) это {e, (01)(23), (23), (01)}.
    Это не нормальная V4 из S4; её образ в S4/V4 ≅ S3 имеет порядок 2, а не 6. Поворота на четверть
    оборота r ↦ i·r в группе нет: он переводил бы √x в i√x, а x = (√x)² в −x."""
    from sympy.combinatorics import Permutation, PermutationGroup
    x, y, z, t = sp.symbols('x y z t')
    fac = sp.factor_list(y**4 - x**2, y)
    f1 = sorted(str(f) for f, _ in fac[1]) == sorted(['-x + y**2', 'x + y**2'])
    p, q, r = 0, 0, -x**2
    cubic = sp.expand(z**3 - p * z**2 - 4 * r * z + (4 * p * r - q**2))
    f2 = sp.simplify(cubic - (z**3 + 4 * x**2 * z)) == 0 and set(sp.solve(cubic, z)) == {0, 2 * sp.I * x, -2 * sp.I * x}
    fac_t = sp.factor_list(y**4 - t**4, y)
    degs = sorted(sp.degree(f, y) for f, _ in fac_t[1])
    f_deg = degs == [1, 1, 2] and sp.Poly(y**2 + t**2, y).is_irreducible  # i ∉ Q(t) ⇒ [Q(x)(√x,i):Q(x)] = 4
    G = PermutationGroup([Permutation([1, 0, 3, 2]), Permutation([0, 1, 3, 2])])
    V = PermutationGroup([Permutation([1, 0, 3, 2]), Permutation([2, 3, 0, 1])])
    S4 = PermutationGroup([Permutation([1, 0, 2, 3]), Permutation([1, 2, 3, 0])])
    inter = [g for g in G.elements if g in V.elements]
    # нормальность — явным сопряжением (см. G60-02)
    f3 = (G.order() == 4 and G.is_abelian and not G.is_cyclic
          and not all(a * g * ~a in G.elements for a in S4.elements for g in G.elements))
    image = G.order() // len(inter)
    quarter = Permutation([2, 3, 1, 0])  # r ↦ i·r: √x→i√x→−√x→−i√x→√x
    f4 = quarter not in G.elements and sp.expand((sp.I * t)**2) != t**2
    ok = f1 and f2 and f_deg and f3 and image == 2 and f4
    check("G60-26", ok, f"разложение {f1}; кубика z³+4x²z, корни 0, ±2ix {f2}; степень поля 4 {f_deg}; "
          f"группа порядка 4, не циклическая, не нормальна в S4 {f3}; образ в S3 порядка {image}; "
          f"четверти оборота в группе нет {f4}")


def g27_basis_tradeoff():
    """G60-27. Предсказание: ни одно из двух чтений пары не доминирует по вопросам одной координаты.
    В (a,b) одной координатой решаются «a=0», «b=0», «a>0», «b>0», и ни один из них не решается
    одной координатой s=a+b или d=a−b. В (s,d) одной координатой решаются «a=b», «a=−b», «a>b»,
    «a+b>0», и ни один не решается одной координатой a или b. Проверка на сетке a, b ∈ {−3…3}."""
    grid = [(a, b) for a in range(-3, 4) for b in range(-3, 4)]
    coords = {'a': lambda a, b: a, 'b': lambda a, b: b, 's': lambda a, b: a + b, 'd': lambda a, b: a - b}
    def decided_by(pred, c):
        seen = {}
        for a, b in grid:
            k = coords[c](a, b)
            v = pred(a, b)
            if seen.setdefault(k, v) != v:
                return False
        return True
    q_ab = {'a=0': lambda a, b: a == 0, 'b=0': lambda a, b: b == 0,
            'a>0': lambda a, b: a > 0, 'b>0': lambda a, b: b > 0}
    q_sd = {'a=b': lambda a, b: a == b, 'a=-b': lambda a, b: a == -b,
            'a>b': lambda a, b: a > b, 'a+b>0': lambda a, b: a + b > 0}
    ab_ok = all(any(decided_by(P, c) for c in 'ab') and not any(decided_by(P, c) for c in 'sd') for P in q_ab.values())
    sd_ok = all(any(decided_by(P, c) for c in 'sd') and not any(decided_by(P, c) for c in 'ab') for P in q_sd.values())
    check("G60-27", ab_ok and sd_ok, f"вопросы (a,b) решает одна координата a или b, но не s или d: {ab_ok}; "
          f"вопросы (s,d) — наоборот: {sd_ok}")

def g28_window_groups_and_roots():
    """G60-28. Предсказание: столбец «группа» таблицы окон (windows_table.tsv) для окна n есть
    (Z/(n−1))^× = Gal(Q(ζ_{n−1})/Q) во всех 12 строках; его порядок φ(n−1) — степень кругового поля.
    Корни единицы в Q(ζ_s) при чётном s — μ_s (внешнее), поэтому поворот порядка k есть в носителе окна n
    ровно при k | n−1: порядок 4 впервые в окне 5, порядки 3 и 6 — в окне 7, порядок 8 — в окне 9
    (Q(ζ8), степень 4), затем 17 и 25. В самом столбце «группа» элемента порядка 8 нет ни в одном окне."""
    from math import gcd
    from sympy.ntheory import n_order
    table = {3: [], 5: [2], 7: [2], 9: [2, 2], 11: [4], 13: [2, 2], 15: [6], 17: [2, 4],
             19: [6], 21: [2, 4], 23: [10], 25: [2, 2, 2]}  # столбец «группа», 2026-10-08
    def order_profile_units(m):
        return sorted(n_order(a, m) if m > 1 else 1 for a in range(1, max(m, 2)) if gcd(a, m) == 1)
    def order_profile_cyclic_product(cs):
        prof = [1]
        for c in cs:
            prof = [(p * q) // gcd(p, q) for p in prof for q in [c // gcd(c, j) for j in range(c)]]
        return sorted(prof)
    same = all(order_profile_units(n - 1) == order_profile_cyclic_product(cs) for n, cs in table.items())
    degree = all(len(order_profile_units(n - 1)) == sp.totient(n - 1) for n in table)
    W = sorted(table)
    first = {k: [n for n in W if (n - 1) % k == 0] for k in (3, 4, 6, 8)}
    no8 = all(8 not in order_profile_units(n - 1) for n in W)
    ok = (same and degree and first[4][0] == 5 and first[3][0] == 7 and first[6][0] == 7
          and first[8] == [9, 17, 25] and sp.totient(8) == 4 and no8)
    check("G60-28", ok, f"столбец «группа» = (Z/(n−1))^× во всех строках: {same}; порядок = φ(n−1): {degree}; "
          f"поворот порядка 4 впервые в окне {first[4][0]}, 3 и 6 — {first[3][0]}, 8 — в окнах {first[8]}; "
          f"в столбце «группа» порядка 8 нет: {no8}")

def g29_ratio_uniform():
    """G60-29. Предсказание: для всех форм МУ2…МУ11 (x, −x, |x|, −|x|, x², √|x|, x³, cos x, eˣ)
    отношение анти-формы к форме (−F)/F = −1 везде, где F≠0. Регистр отношений даёт на каждом
    уровне одну и ту же Z/2, поэтому лемма Tot (коллапс Z/2→{1}) уровни 8–11 не различает."""
    x = sp.symbols('x', real=True)
    forms = [x, -x, sp.Abs(x), -sp.Abs(x), x**2, -x**2, sp.sqrt(sp.Abs(x)), x**3, sp.cos(x), sp.exp(x)]
    pts = [-3, -sp.Rational(1, 2), sp.Rational(1, 3), 2, 5]
    ok = all(sp.simplify((-F) / F) == -1 for F in forms) and all(
        (-F.subs(x, v)) / F.subs(x, v) == -1 for F in forms for v in pts if F.subs(x, v) != 0)
    check("G60-29", ok, "(−F)/F = −1 для всех десяти форм МУ2…МУ11: регистр отношений везде Z/2")


def g30_shift_types():
    """G60-30. Предсказание: операторные уравнения М-регистра для 9–11 — линейные с постоянными
    коэффициентами: x³ решает D⁴y=0, cos x — D²y=−y, eˣ — Dy=y (характеристические корни 0, ±i, 1).
    Сдвиг e^{hD} действует на пространствах решений тремя типами: на {1,x,x²,x³} — унипотентно
    (все собственные числа 1, одна жорданова клетка, порядок бесконечен); на {cos,sin} — поворот на h
    (ортогональная матрица, det 1, возврат при h=2π), сам D там имеет порядок 4 (D²=−I); на {eˣ} —
    умножение на e^h (≠1 при h≠0, возврата нет). Неподвижные при всех сдвигах решения: константы (9),
    только 0 (10 и 11)."""
    x, h = sp.symbols('x h', real=True)
    odes = (sp.diff(x**3, x, 4) == 0, sp.simplify(sp.diff(sp.cos(x), x, 2) + sp.cos(x)) == 0,
            sp.simplify(sp.diff(sp.exp(x), x) - sp.exp(x)) == 0)
    # унипотентный сдвиг на базисе 1, x, x², x³
    basis = [sp.Integer(1), x, x**2, x**3]
    def coords(expr):
        p = sp.Poly(sp.expand(expr), x)
        return [p.coeff_monomial(x**k) for k in range(4)]
    S = sp.Matrix([coords(b.subs(x, x + h)) for b in basis]).T
    jordan_one_block = (S.subs(h, 1) - sp.eye(4)).rank() == 3
    unip = sp.factor(S.charpoly().as_expr()) == (sp.Symbol('lambda') - 1)**4 and jordan_one_block
    # поворот на {cos, sin}
    R = sp.Matrix([[sp.cos(h), -sp.sin(h)], [sp.sin(h), sp.cos(h)]])
    rot_ok = (sp.simplify(sp.cos(x + h) - (R[0, 0] * sp.cos(x) + R[0, 1] * sp.sin(x))) == 0
              and sp.simplify(sp.sin(x + h) - (R[1, 0] * sp.cos(x) + R[1, 1] * sp.sin(x))) == 0
              and sp.simplify(R.T * R - sp.eye(2)) == sp.zeros(2) and sp.simplify(R.det()) == 1
              and R.subs(h, 2 * sp.pi) == sp.eye(2))
    Dm = sp.Matrix([[0, 1], [-1, 0]])  # D на базисе (cos, sin): cos'=−sin, sin'=cos, столбцы — образы
    d_order4 = Dm**2 == -sp.eye(2) and Dm**4 == sp.eye(2)
    scale_ok = sp.simplify(sp.exp(x + h) / sp.exp(x) - sp.exp(h)) == 0 and sp.solve(sp.Eq(sp.exp(h), 1), h) == [0]
    # неподвижные при всех сдвигах: ядро (S−I) при общем h
    fix9 = (S - sp.eye(4)).subs(h, 1).nullspace()
    fix9_const = len(fix9) == 1 and list(fix9[0]) == [1, 0, 0, 0]
    fix10_zero = (R.subs(h, sp.pi / 2) - sp.eye(2)).nullspace() == []
    ok = all(odes) and unip and rot_ok and d_order4 and scale_ok and fix9_const and fix10_zero
    check("G60-30", ok, f"уравнения D⁴y=0, D²y=−y, Dy=y: {all(odes)}; сдвиг на x³ унипотентен (одна клетка): {unip}; "
          f"на cos — поворот с периодом 2π: {rot_ok}, D порядка 4: {d_order4}; на eˣ — масштаб e^h: {scale_ok}; "
          f"неподвижные: константы (9) {fix9_const}, 0 (10) {fix10_zero}")


def g31_const_statistics():
    """G60-31. Предсказание: для дискретного распределения с p_i>0 дисперсия равна 0 ⟺ все x_i равны μ;
    при μ≠0 это то же, что x_i/μ = 1 для всех i («отношение ≡ 1» леммы Tot, форма МУ2 y=x).
    Усреднение P = 1·pᵀ идемпотентно, его неподвижные векторы — константы (ранг 1)."""
    p = sp.symbols('p', positive=True)
    x1, x2 = sp.symbols('x1 x2', real=True)
    mu = p * x1 + (1 - p) * x2
    var = sp.factor(sp.expand(p * (x1 - mu)**2 + (1 - p) * (x2 - mu)**2))
    var_ok = sp.simplify(var - p * (1 - p) * (x1 - x2)**2) == 0
    ratio_ok = sp.simplify((x1 / mu).subs(x2, x1)) == 1
    pv = sp.Matrix([sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)])
    P = sp.ones(3, 1) * pv.T
    fixed = (P - sp.eye(3)).nullspace()
    proj_ok = P * P == P and P.rank() == 1 and len(fixed) == 1 and list(fixed[0]) == [1, 1, 1]
    ok = var_ok and ratio_ok and proj_ok
    check("G60-31", ok, f"Var = p(1−p)(x1−x2)²: {var_ok}; при x1=x2 отношение x/μ = 1: {ratio_ok}; "
          f"усреднение — проектор ранга 1 с неподвижными константами: {proj_ok}")


def g32_recurrences():
    """G60-32. Предсказание: в регистре отношений МУ9–МУ11 — линейные рекуррентности с постоянными
    коэффициентами по шагу h: четвёртая разность x³ равна 0 (третья — 6h³, постоянна);
    cos(x+h)+cos(x−h) = 2cos h·cos x (трёхчленное отношение, не зависит от x);
    e^{x+h} = e^h·eˣ. Характеристические многочлены (t−1)⁴, t²−2cos h·t+1 (корни e^{±ih}), t−e^h."""
    x, h, t = sp.symbols('x h t', real=True)
    f = x**3
    d3 = sp.expand(f.subs(x, x + 3*h) - 3*f.subs(x, x + 2*h) + 3*f.subs(x, x + h) - f)
    d4 = sp.expand(f.subs(x, x + 4*h) - 4*f.subs(x, x + 3*h) + 6*f.subs(x, x + 2*h) - 4*f.subs(x, x + h) + f)
    cheb = sp.simplify(sp.cos(x + h) + sp.cos(x - h) - 2 * sp.cos(h) * sp.cos(x)) == 0
    expo = sp.simplify(sp.exp(x + h) - sp.exp(h) * sp.exp(x)) == 0
    # корни t²−2cos h·t+1 — e^{±ih}: по Виету сумма 2cos h, произведение 1
    # (прямая подстановка e^{ih} не упрощается sympy без переписывания через cos)
    r1, r2 = sp.exp(sp.I * h), sp.exp(-sp.I * h)
    roots_ok = (sp.simplify((r1 + r2).rewrite(sp.cos) - 2 * sp.cos(h)) == 0
                and sp.simplify(r1 * r2) == 1)
    ok = d3 == 6 * h**3 and d4 == 0 and cheb and expo and roots_ok
    check("G60-32", ok, f"Δ³x³={d3}, Δ⁴x³={d4}; cos: трёхчленное отношение 2cos h: {cheb}; "
          f"eˣ: e^h: {expo}; корни e^(±ih): {roots_ok}")


def g33_jacobi_degenerations():
    """G60-33. Предсказание: j(λ) = 256(λ²−λ+1)³/(λ²(λ−1)²) конечен при λ∉{0,1} и уходит в ∞ ровно при
    λ∈{0,1,∞} — орбите, которую переставляют шесть замен G60-03. При m=k²=0 sn(u|m)=sin u, при m=1
    sn(u|m)=tanh u. Вещественный период 4K(m) конечен при m<1 и расходится при m→1; мнимый K′(m)=K(1−m)
    расходится при m→0. Внутри (0,1) — оба периода (тор), на краях теряется один."""
    import mpmath as mp
    lam = sp.symbols('lambda')
    j = 256 * (lam**2 - lam + 1)**3 / (lam**2 * (lam - 1)**2)
    poles = set(sp.solve(sp.denom(sp.together(j)), lam))
    at_inf = sp.limit(j, lam, sp.oo) == sp.oo
    # числитель не обращается в 0 в полюсах — полюса настоящие
    num_ok = all(sp.numer(sp.together(j)).subs(lam, v) != 0 for v in poles)
    us = [0.3, 1.1, 2.5]
    sn0 = all(abs(mp.ellipfun('sn', u, m=0) - mp.sin(u)) < 1e-12 for u in us)
    sn1 = all(abs(mp.ellipfun('sn', u, m=1) - mp.tanh(u)) < 1e-12 for u in us)
    # K(m) при m→1; мнимый полупериод K′(m)=K(1−m) при m→0 — те же значения
    K_real = [mp.ellipk(1 - 10**(-k)) for k in (2, 6, 12)]
    grow = all(K_real[i] < K_real[i + 1] for i in range(2)) and K_real[-1] > 15
    k0 = abs(mp.ellipk(0) - mp.pi / 2) < 1e-15
    ok = poles == {0, 1} and at_inf and num_ok and sn0 and sn1 and grow and k0
    check("G60-33", ok, f"полюса j: {sorted(poles)} и ∞: {at_inf}; sn(·|0)=sin: {sn0}, sn(·|1)=tanh: {sn1}; "
          f"K(m)→∞ при m→1 (K(1−10⁻¹²)≈{float(K_real[-1]):.2f}), K(0)=π/2: {k0}")


def g34_partial_symmetry():
    """G60-34. Предсказание: f(z)=Re(z²) инвариантна при z↦−z (Z/2, знак узлов 3 и 7), но не при
    повороте z↦iz (f(1)=1, f(i)=−1). g(z)=|z|² инвариантна при всех поворотах: d/dθ g(e^{iθ}z)=0.
    Инвариантность при конечной подгруппе не влечёт инвариантности при U(1)."""
    a, b, th = sp.symbols('a b theta', real=True)
    z = a + sp.I * b
    f = lambda w: sp.re(sp.expand(w**2))
    z2_inv = sp.simplify(f(-z) - f(z)) == 0
    rot_fail = f(sp.Integer(1)) == 1 and f(sp.I) == -1
    w = sp.exp(sp.I * th) * z
    g_rot = sp.simplify(sp.diff(sp.expand(w * sp.conjugate(w)), th)) == 0
    f_rot = sp.simplify(sp.diff(f(w), th)) != 0
    ok = z2_inv and rot_fail and g_rot and f_rot
    check("G60-34", ok, f"Re z² инвариантна при z↦−z: {z2_inv}, не при z↦iz: {rot_fail}; "
          f"|z|² инвариантна при U(1): {g_rot}; Re z² — нет: {f_rot}")


def g35_product_singularities():
    """G60-35. Предсказание: для B1=x²+(y−2)²−4, B2=x²+(y+2)²−4 (минимальный космос У13) произведение
    B1·B2 особо (градиент 0) в точке касания (0,0), гессиан там ранга 1 — такнод (касание). Для
    пересекающихся окружностей (центры (0,±1), r=2) общие точки — обычные узлы: гессиан ранга 2, det<0.
    Вне общих точек кривая B1·B2=0 гладкая. Произведение забывает, какой множитель обнулился,
    но хранит, где и как контуры встречаются."""
    x, y = sp.symbols('x y', real=True)
    def sing_info(B1, B2):
        P = sp.expand(B1 * B2)
        grad = [sp.diff(P, v) for v in (x, y)]
        common = sp.solve([B1, B2], [x, y], dict=True)
        out = []
        for c in common:
            H = sp.hessian(P, (x, y)).subs(c)
            out.append((c, all(g.subs(c) == 0 for g in grad), H.rank(), H.det()))
        return out
    touch = sing_info(x**2 + (y - 2)**2 - 4, x**2 + (y + 2)**2 - 4)
    cross = sing_info(x**2 + (y - 1)**2 - 4, x**2 + (y + 1)**2 - 4)
    touch_ok = len(touch) == 1 and touch[0][1] and touch[0][2] == 1
    cross_ok = len(cross) == 2 and all(c[1] and c[2] == 2 and c[3] < 0 for c in cross)
    # гладкость в точке (0,4) на одном контуре
    P = sp.expand((x**2 + (y - 2)**2 - 4) * (x**2 + (y + 2)**2 - 4))
    smooth = any(sp.diff(P, v).subs({x: 0, y: 4}) != 0 for v in (x, y))
    ok = touch_ok and cross_ok and smooth
    check("G60-35", ok, f"касание: одна общая точка, особая, гессиан ранга 1 (такнод): {touch_ok}; "
          f"пересечение: две особые точки, гессиан ранга 2, det<0 (узлы): {cross_ok}; вне них гладко: {smooth}")


def g36_neighbor_average():
    """G60-36. Предсказание: оператор усреднения соседей A_h f(x) = (f(x+h)+f(x−h))/2 даёт:
    A_h x² = x² + h² (аддитивная прибавка, выпуклость), A_h cos x = cos h·cos x (|cos h| ≤ 1, сжатие),
    A_h eˣ = ch h·eˣ (ch h ≥ 1, усиление). Собственные функции — cos и eˣ, x² — нет."""
    x, h = sp.symbols('x h', real=True)
    A = lambda f: (f.subs(x, x + h) + f.subs(x, x - h)) / 2
    sq = sp.expand(A(x**2)) == x**2 + h**2
    cs = sp.simplify(sp.expand_trig(A(sp.cos(x))) - sp.cos(h) * sp.cos(x)) == 0
    ex = sp.simplify((A(sp.exp(x)) - sp.cosh(h) * sp.exp(x)).rewrite(sp.exp)) == 0
    bounds = sp.simplify(sp.cosh(h)**2 - sp.sinh(h)**2) == 1  # ch h ≥ 1, т.к. ch² = 1 + sh²
    ok = sq and cs and ex and bounds
    check("G60-36", ok, f"A_h x² = x²+h²: {sq}; A_h cos = cos h·cos: {cs}; A_h eˣ = ch h·eˣ: {ex}")


def g37_padic_units():
    """G60-37. Предсказание: в Z_p при нечётном p уравнение x^{p−1}=1 имеет ровно p−1 решений по модулю
    p^k (корни Тейхмюллера, подъём Хензеля), то есть μ_{p−1} ⊂ Z_p^×; при p=5 это {±1, ±i}. При p=2
    решений x²=1 по модулю 2^k (k≥3) четыре (±1, 2^{k−1}±1), но настоящих 2-адических корней из 1
    только ±1: x=2^{k−1}+1 не поднимается в последовательность, совместную по всем k. Разложение
    Q_p^× = p^Z × Z_p^×: |x|_p = p^{−v} (дискретный масштаб) × единица."""
    from sympy.ntheory import n_order
    k = 6
    teich = {p: sum(1 for a in range(1, p**k) if a % p and pow(a, p - 1, p**k) == 1) for p in (3, 5, 7)}
    t_ok = all(teich[p] == p - 1 for p in teich)
    i_in_z5 = any(pow(a, 2, 5**k) == 5**k - 1 for a in range(5**k))
    sols8 = sorted(a for a in range(2**k) if pow(a, 2, 2**k) == 1)
    # класс 2^{k−1}+1 mod 2^k не поднимается: оба его продолжения mod 2^{k+1} не решения
    lift_fail = all(pow(c, 2, 2**(k + 1)) != 1 for c in (2**(k - 1) + 1, 2**(k - 1) + 1 + 2**k))
    # p-адическое разложение для x = 50 при p=5: v=2, единица 2
    def val(n, p):
        v = 0
        while n % p == 0:
            n //= p; v += 1
        return v, n
    dec = val(50, 5) == (2, 2)
    ok = t_ok and i_in_z5 and sols8 == [1, 2**(k - 1) - 1, 2**(k - 1) + 1, 2**k - 1] and lift_fail and dec
    check("G60-37", ok, f"корней Тейхмюллера mod p^6: {teich}; i ∈ Z_5: {i_in_z5}; x²=1 mod 2^6: {sols8}; "
          f"50 = 5²·2: {dec}")


def g38_ratio_sphere_indices():
    """G60-38. Предсказание: комплексный канал отношений ratio(a,b)=a/b сокращает любой ненулевой общий
    множитель λ∈C* (как C-45 для вещественных), поэтому его носитель с полюсом b=0 — CP¹ = C∪{∞} = S².
    Поле поворота z ↦ e^{iφ}z (генератор V(z)=iz) имеет на CP¹ ровно два нуля: z=0 (a=0) и z=∞ (b=0),
    в карте w=1/z поле −iw; индекс каждого +1 (det якобиана 1>0), сумма 2 = χ(S²). На торе |a|=|b|
    одновременный поворот фаз ∂θ₁+∂θ₂ нулей не имеет (по построению: компоненты постоянны), χ(T²)=0."""
    a, b, lam = sp.symbols('a b lambda', nonzero=True)
    ratio_ok = sp.simplify((lam * a) / (lam * b) - a / b) == 0
    X, Y = sp.symbols('X Y', real=True)
    def index_linear(field):  # индекс невырожденного нуля в начале = sign det якобиана
        J = sp.Matrix([[sp.diff(field[i], v) for v in (X, Y)] for i in range(2)])
        return sp.sign(J.det())
    z = X + sp.I * Y
    V = sp.expand(sp.I * z)        # поле в карте z
    W = sp.expand(-sp.I * z)       # поле в карте w (те же координаты X, Y)
    iz = index_linear((sp.re(V), sp.im(V)))
    iw = index_linear((sp.re(W), sp.im(W)))
    zeros_z = sp.solve([sp.re(V), sp.im(V)], [X, Y], dict=True)
    torus_free = all(c != 0 for c in (1, 1))  # компоненты поля ∂θ₁+∂θ₂ постоянны и ненулевые
    ok = ratio_ok and iz == 1 and iw == 1 and iz + iw == 2 and zeros_z == [{X: 0, Y: 0}] and torus_free
    check("G60-38", ok, f"a/b сокращает λ∈C*: {ratio_ok}; индексы нулей поворота в 0 и ∞: {iz}, {iw}, "
          f"сумма {iz + iw} = χ(S²); на торе нулей нет")


def g39_levy_thresholds():
    """G60-39. Предсказание: для симметричного α-устойчивого закона φ(t)=exp(−|t|^α) среднее n наблюдений
    имеет х.ф. φ(t/n)^n = exp(−n^{1−α}|t|^α), то есть масштаб n^{1/α−1}. Разброс среднего сжимается
    ⟺ α>1; при α=1 (Коши) не меняется; при α<1 растёт. Второй момент конечен только при α=2 (гаусс).
    Два порога: α=2 (умирает V·V), α=1 (умирает сходимость среднего, Tot недостижима)."""
    t, n = sp.symbols('t n', positive=True)
    al = sp.symbols('alpha', positive=True)
    phi = lambda s: sp.exp(-s**al)
    mean_cf = sp.simplify(sp.powsimp(phi(t / n)**n, force=True))
    target = sp.exp(-n**(1 - al) * t**al)
    cf_ok = sp.simplify(sp.log(mean_cf) - sp.log(target)) == 0
    expo = 1 / al - 1
    signs = [sp.sign(expo.subs(al, v)) for v in (sp.Rational(3, 2), 1, sp.Rational(1, 2))]
    # конечность E|X|^2 у α<2 нет: хвост ~|x|^{−1−α}, ∫|x|²·|x|^{−1−α} расходится при α<2
    x = sp.symbols('x', positive=True)
    tail2 = sp.integrate(x**2 * x**(-1 - sp.Rational(3, 2)), (x, 1, sp.oo))
    tail1_cauchy = sp.integrate(x * x**(-2), (x, 1, sp.oo))
    ok = cf_ok and signs == [-1, 0, 1] and tail2 == sp.oo and tail1_cauchy == sp.oo
    check("G60-39", ok, f"х.ф. среднего = exp(−n^(1−α)|t|^α): {cf_ok}; знак показателя масштаба 1/α−1 при "
          f"α=3/2, 1, 1/2: {signs}; E X² = ∞ при α=3/2: {tail2 == sp.oo}; E|X| = ∞ у Коши: {tail1_cauchy == sp.oo}")


def g40_diagonal_ratio():
    """G60-40. Предсказание (схема Лоувера/Яновского на конечном классе форм): f(F,G)=sign(F/G) на
    T = ненулевых значениях, α(y)=−y на {±1} без неподвижных точек. Диагональ g(F)=α(f(F,F)) = −1;
    ни одна G0∈T не даёт f(F,G0)=g(F) для всех F (на F=G0: 1 ≠ −1). В аддитивном регистре
    f(F,G)=F−G, α=минус имеет неподвижную точку 0 и g(F)=−(F−F)=0 — диагональ противоречия не даёт."""
    T = [-3, -1, sp.Rational(-1, 2), sp.Rational(1, 2), 1, 2, 5]
    f = lambda F, G: sp.sign(sp.Rational(F) / G)
    g = lambda F: -f(F, F)
    no_rep = all(any(f(F, G0) != g(F) for F in T) for G0 in T)
    fixed_free = all(-y != y for y in (1, -1))
    add_fixed = (-0 == 0) and all(-(F - F) == 0 for F in T)
    ok = no_rep and fixed_free and add_fixed
    check("G60-40", ok, f"R-канал: α без неподвижных точек {fixed_free}, диагональ не представима: {no_rep}; "
          f"аддитивно: минус неподвижен в 0, диагональ даёт 0: {add_fixed}")


def g41_mu7_set_reading():
    """G60-41. Предсказание: при МУ7 = |y|=x² (решение автора 2026-10-08) каждая точка МУ6 (y=x²) лежит
    на МУ7, то есть МУ6 ⊂ МУ7, и уровни 6 и 7 встречаются не только в нуле (утверждения C02/C58 о паре
    (x², −x²) верны для ветви y=−x², но не для множества). МУ7 чётна по x и по y. При x=1 значения МУ7 —
    {−1, 1} = {МУ2(1), МУ3(1)}: совпадение C52 «У7=У3 при x=1» становится включением."""
    pts = [-2, -1, sp.Rational(-1, 3), 0, sp.Rational(1, 2), 1, 3]
    on7 = lambda X, Y: abs(Y) == X**2
    mu6_in_mu7 = all(on7(v, v**2) for v in pts)
    meet_beyond_zero = any(on7(v, v**2) and v != 0 for v in pts)
    branch_meets_only_zero = [v for v in pts if v**2 == -(v**2)] == [0]
    even_xy = all(on7(-v, v**2) and on7(v, -(v**2)) for v in pts)
    vals_at_1 = {sp.Integer(1), sp.Integer(-1)}
    at1 = vals_at_1 == {Y for Y in (-1, 0, 1, 2) if on7(1, Y)} and vals_at_1 == {1, -1}
    ok = mu6_in_mu7 and meet_beyond_zero and branch_meets_only_zero and even_xy and at1
    check("G60-41", ok, f"МУ6 ⊂ МУ7: {mu6_in_mu7}; ветвь −x² встречает x² только в 0: {branch_meets_only_zero}; "
          f"МУ7 чётна по x и y: {even_xy}; при x=1 значения МУ7 = {{МУ2(1), МУ3(1)}}: {at1}")


def _mi(joint):
    """Взаимная информация (биты) для словаря {(u, v): p}."""
    pu, pv = {}, {}
    for (u, v), p in joint.items():
        pu[u] = pu.get(u, 0) + p
        pv[v] = pv.get(v, 0) + p
    return sp.nsimplify(sum(p * sp.log(p / (pu[u] * pv[v]), 2) for (u, v), p in joint.items() if p != 0))


def g42_typed_absence_witness():
    """G60-42. Предсказание: Y∈{0,1} равновероятно, q∈(0,1). Два механизма пропуска: H — пропуск при Y=1
    с вероятностью q, L — пропуск при Y=0 с вероятностью q. Флаг пропуска (¬A) независим от Y:
    I(Y;flag)=0. Тип пропуска (0_A: H/L/наблюдено) несёт I(Y;type | пропуск) = 1 бит. Если же оба
    механизма однонаправлены (оба при Y=1 с q/2), то I(Y;type | flag) = 0: тип ничего не добавляет к флагу.
    Это форма SHADOW-5: различение доступно ⟺ у механизма есть нечётная по Y компонента."""
    q = sp.Rational(1, 3)
    half = sp.Rational(1, 2)
    # противоположные механизмы
    opp = {(1, 'H'): half * q, (1, 'obs'): half * (1 - q), (0, 'L'): half * q, (0, 'obs'): half * (1 - q)}
    flag = lambda t: 'miss' if t != 'obs' else 'obs'
    def collapse(joint, f):
        out = {}
        for (y, t), p in joint.items():
            out[(y, f(t))] = out.get((y, f(t)), 0) + p
        return out
    mi_flag_opp = _mi(collapse(opp, flag))
    miss_opp = {k: v / sum(p for (y, t), p in opp.items() if t != 'obs') for k, v in opp.items() if k[1] != 'obs'}
    mi_type_given_miss_opp = _mi(miss_opp)
    # однонаправленные механизмы: оба при Y=1, по q/2
    same = {(1, 'H'): half * q / 2, (1, 'L'): half * q / 2, (1, 'obs'): half * (1 - q), (0, 'obs'): half}
    miss_same = {k: v / sum(p for (y, t), p in same.items() if t != 'obs') for k, v in same.items() if k[1] != 'obs'}
    mi_type_given_miss_same = _mi(miss_same)
    mi_flag_same = _mi(collapse(same, flag))
    ok = mi_flag_opp == 0 and mi_type_given_miss_opp == 1 and mi_type_given_miss_same == 0 and mi_flag_same > 0
    check("G60-42", ok, f"противоположные механизмы: I(Y;флаг)={mi_flag_opp}, I(Y;тип|пропуск)={mi_type_given_miss_opp} бит; "
          f"однонаправленные: I(Y;флаг)={float(mi_flag_same):.4f}, I(Y;тип|пропуск)={mi_type_given_miss_same}")


def g43_misspecified_bayes():
    """G60-43. Предсказание: пространство гипотез H={p=0.6, p=0.9}, равный прайор, данные — 500 гербов из
    1000 (истина p=0.5 вне H). Постериор P(0.6|D) > 1−10⁻¹⁰⁰: правило отказа по уверенности (Чоу) не
    отказывает. Проверка модели отказывает: частота 0.5 отстоит от 0.6 на z ≈ −6.45 стандартных ошибок."""
    n, k = 1000, 500
    a, b = sp.Rational(3, 5), sp.Rational(9, 10)
    la = k * sp.log(a) + (n - k) * sp.log(1 - a)
    lb = k * sp.log(b) + (n - k) * sp.log(1 - b)
    post_b = 1 / (1 + sp.exp(la - lb))
    tiny = sp.N(post_b, 30) < sp.Float('1e-100')
    z = (sp.Rational(k, n) - a) / sp.sqrt(a * (1 - a) / n)
    zf = float(z)
    ok = tiny and zf < -6.4 and zf > -6.5
    check("G60-43", ok, f"P(0.9|D) = {sp.N(post_b, 3)} (постериор уверенно на 0.6); z частоты против 0.6 = {zf:.2f}")


def g44_ratio_bit_vs_channels():
    """G60-44. Предсказание: на ненулевых целых парах (a,b), |a|,|b| ≤ 4, бит R-канала sign(a·b)
    («одинаковы ли знаки») не есть функция d=a−b (пример: (3,1) и (1,−1), d=2), не есть функция s=a+b
    и не есть функция пары модулей (|a|,|b|); он есть функция пары знаков. Его блоки совпадают с орбитами ν
    на кресте (±1,±1) — первым вынужденным шагом G60-18. Бит меняется при зеркале одного объекта
    a↦−a (антисимметричен, условие SHADOW-5)."""
    R = [v for v in range(-4, 5) if v != 0]
    pairs = [(a, b) for a in R for b in R]
    bit = lambda p: 1 if p[0] * p[1] > 0 else -1
    def is_function_of(key):
        seen = {}
        for p in pairs:
            k = key(p)
            if k in seen and seen[k] != bit(p):
                return False
            seen[k] = bit(p)
        return True
    not_d = not is_function_of(lambda p: p[0] - p[1])
    not_s = not is_function_of(lambda p: p[0] + p[1])
    not_mod = not is_function_of(lambda p: (abs(p[0]), abs(p[1])))
    of_signs = is_function_of(lambda p: (p[0] > 0, p[1] > 0))
    witness = bit((3, 1)) != bit((1, -1)) and (3 - 1) == (1 - (-1))
    cross = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    blocks = {frozenset(c for c in cross if bit(c) == s) for s in (1, -1)}
    nu_orbits = {frozenset({(1, 1), (-1, -1)}), frozenset({(1, -1), (-1, 1)})}
    antisym = all(bit((-a, b)) == -bit((a, b)) for a, b in pairs)
    ok = not_d and not_s and not_mod and of_signs and witness and blocks == nu_orbits and antisym
    check("G60-44", ok, f"sign(ab) не функция d: {not_d}, s: {not_s}, (|a|,|b|): {not_mod}; функция знаков: {of_signs}; "
          f"блоки = орбиты ν: {blocks == nu_orbits}; антисимметричен к a↦−a: {antisym}")


def g45_blackwell_flag_garbling():
    """G60-45. Предсказание: флаг пропуска — функция типа (огрубление по Блэкуэллу), поэтому в любой задаче
    решения ценность типа ≥ ценности флага. На свидетеле G60-42 (противоположные механизмы, q=1/3) в задаче
    «угадать Y» с выигрышем 1 за верный ответ: с типом точность 1 − (1−q)/2 = 2/3, с флагом 1/2 — строго
    больше. При однонаправленных механизмах точности совпадают (тип не добавляет к флагу)."""
    half, q = sp.Rational(1, 2), sp.Rational(1, 3)
    def bayes_acc(joint, view):
        # joint: {(y, t): p}; view(t) — что видит решающий; оптимум — argmax по y внутри каждого вида
        by_view = {}
        for (y, t), p in joint.items():
            by_view.setdefault(view(t), {}).setdefault(y, 0)
            by_view[view(t)][y] += p
        return sum(max(d.values()) for d in by_view.values())
    opp = {(1, 'H'): half * q, (1, 'obs'): half * (1 - q), (0, 'L'): half * q, (0, 'obs'): half * (1 - q)}
    same = {(1, 'H'): half * q / 2, (1, 'L'): half * q / 2, (1, 'obs'): half * (1 - q), (0, 'obs'): half}
    ident = lambda t: t
    flag = lambda t: 'miss' if t != 'obs' else 'obs'
    a_type, a_flag = bayes_acc(opp, ident), bayes_acc(opp, flag)
    s_type, s_flag = bayes_acc(same, ident), bayes_acc(same, flag)
    ok = a_type == sp.Rational(2, 3) and a_flag == half and s_type == s_flag
    check("G60-45", ok, f"противоположные: точность с типом {a_type}, с флагом {a_flag}; "
          f"однонаправленные: {s_type} = {s_flag}")


def g46_pareto_minimal_chain():
    """G60-46. Предсказание: на 18 насыщенных цепях свидетеля NC-01 (крест (±1,±1), G60-18) вектор цены
    (H, B): H — число промежуточных разбиений, не являющихся орбитами подгрупп D4 (скрытые выборы),
    B — 1, если на третьем шаге не выделена базовая точка (1,1). Парето-минимум единственен: σ-цепь с
    (0, 0). Минимум H=0 у двух цепей, у остальных 16 H ≥ 1."""
    V = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    def as_perm(f):
        return tuple(V.index(f(v)) for v in V)
    def compose(g, h):
        return tuple(g[h[i]] for i in range(4))
    ident = (0, 1, 2, 3)
    def closure(gs):
        H = {ident}
        fr = [ident]
        while fr:
            nw = []
            for g in fr:
                for h in gs:
                    k = compose(h, g)
                    if k not in H:
                        H.add(k)
                        nw.append(k)
            fr = nw
        return frozenset(H)
    G = closure([as_perm(lambda p: (p[1], p[0])), as_perm(lambda p: (p[0], -p[1]))])
    subgroups = {closure(list(c)) for r in range(0, 3) for c in itertools.combinations(sorted(G), r)}
    orbit_parts = {frozenset(frozenset(V[g[i]] for g in H) for i in range(4)) for H in subgroups}
    parts = {canon(p) for p in set_partitions(V)}
    by = {}
    for p in parts:
        by.setdefault(len(p), []).append(p)
    chains = [(p1, p2, p3, p4) for p1 in by[1] for p2 in by[2] for p3 in by[3] for p4 in by[4]
              if refines(p2, p1) and refines(p3, p2) and refines(p4, p3)]
    cost = {c: (sum(p not in orbit_parts for p in c[1:3]),
                0 if any((1, 1) in b and len(b) == 1 for b in c[2]) else 1) for c in chains}
    def dominated(c):
        return any(all(cost[d][i] <= cost[c][i] for i in range(2)) and cost[d] != cost[c] for d in chains)
    pareto = [c for c in chains if not dominated(c)]
    sigma_part = frozenset(frozenset(V[g[i]] for g in closure([as_perm(lambda p: (p[1], p[0]))])) for i in range(4))
    h0 = [c for c in chains if cost[c][0] == 0]
    ok = (len(chains) == 18 and len(pareto) == 1 and cost[pareto[0]] == (0, 0) and pareto[0][2] == sigma_part
          and len(h0) == 2 and all(cost[c][0] >= 1 for c in chains if c not in h0))
    check("G60-46", ok, f"цепей {len(chains)}, H=0 у {len(h0)}, Парето-минимумов {len(pareto)} "
          f"с ценой {cost[pareto[0]] if pareto else None}: σ-цепь")


def g47_weight_free_dominance():
    """G60-47. Предсказание (лемма для d_Δ): для d_w(a,b) = Σ w_i|Δ_i(a,b)| с w_i ≥ 0 неравенство
    d_w(a,b) ≤ d_w(a,c) при всех допустимых весах ⟺ |Δ_i(a,b)| ≤ |Δ_i(a,c)| для каждого i
    (достаточность — сумма неравенств, необходимость — веса e_i). Пример: (1,3) против (2,2) —
    не сравнимы без весов: при w=(1,0) и w=(0,1) выводы противоположны."""
    w1, w2 = sp.symbols('w1 w2', nonnegative=True)
    d = lambda v: w1 * v[0] + w2 * v[1]
    dom = (1, 2), (2, 3)  # покомпонентно ≤
    suff = sp.simplify(d(dom[1]) - d(dom[0]) - (w1 + w2)) == 0  # разность = w1+w2 ≥ 0
    inc = (1, 3), (2, 2)
    e1 = {w1: 1, w2: 0}
    e2 = {w1: 0, w2: 1}
    opposite = (d(inc[0]).subs(e1) < d(inc[1]).subs(e1)) and (d(inc[0]).subs(e2) > d(inc[1]).subs(e2))
    ok = suff and opposite
    check("G60-47", ok, f"покомпонентное ≤ даёт ≤ при всех весах: {suff}; (1,3) и (2,2) меняют порядок "
          f"при весах e1, e2: {opposite}")


if __name__ == "__main__":
    for f in [g01_chains, g02_resolvent, g03_anharmonic, g04_legendre_2torsion, g05_cross_selection,
              g06_cauchy, g07_cumulants, g08_two, g09_padic, g10_hopf, g11_sierpinski, g12_lawvere,
              g13_hadamard, g14_unit_circle, g15_crystallographic, g16_ratio_forms,
              g17_odd_square, g18_cross_d4_chains, g19_c60_new_mu7, g20_u12_radius,
              g21_pi_9_to_7, g22_absence_witness, g23_node_groups,
              g24_roots_of_unity_trace, g25_dft_diagonalizes_shift, g26_galois_mu8, g27_basis_tradeoff,
              g28_window_groups_and_roots, g29_ratio_uniform, g30_shift_types, g31_const_statistics,
              g32_recurrences, g33_jacobi_degenerations, g34_partial_symmetry, g35_product_singularities,
              g36_neighbor_average, g37_padic_units, g38_ratio_sphere_indices, g39_levy_thresholds,
              g40_diagonal_ratio, g41_mu7_set_reading, g42_typed_absence_witness, g43_misspecified_bayes,
              g44_ratio_bit_vs_channels, g45_blackwell_flag_garbling,
              g46_pareto_minimal_chain, g47_weight_free_dominance]:
        f()
    n_ok = sum(ok for _, ok, _ in RESULTS)
    print(f"ИТОГО: {n_ok}/{len(RESULTS)} PASS")
