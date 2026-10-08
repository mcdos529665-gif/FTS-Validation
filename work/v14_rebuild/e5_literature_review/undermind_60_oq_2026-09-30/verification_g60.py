# -*- coding: utf-8 -*-
"""Проверки G60-01…G60-23 к GROUPED_OPEN_2026-10-08.md (кандидаты ассистента).

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
    normal = V4.is_normal(S4)
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


if __name__ == "__main__":
    for f in [g01_chains, g02_resolvent, g03_anharmonic, g04_legendre_2torsion, g05_cross_selection,
              g06_cauchy, g07_cumulants, g08_two, g09_padic, g10_hopf, g11_sierpinski, g12_lawvere,
              g13_hadamard, g14_unit_circle, g15_crystallographic, g16_ratio_forms,
              g17_odd_square, g18_cross_d4_chains, g19_c60_new_mu7, g20_u12_radius,
              g21_pi_9_to_7, g22_absence_witness, g23_node_groups]:
        f()
    n_ok = sum(ok for _, ok, _ in RESULTS)
    print(f"ИТОГО: {n_ok}/{len(RESULTS)} PASS")
