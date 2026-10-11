# Свидетель (candidate, вне общего маршрута) к sphere_holes_note_2026-10-11.md §5:
# отражение vs поворот (критические точки высоты), «линзирование» (3 точки + линза), тор из МУ7∩МУ8.
# Запуск: py -3.11 -X utf8 work/v14_rebuild/lens_torus_check_2026-10-11.py
import sympy as sp
import math
u,v,x,y,w,t,s,lam=sp.symbols('u v x y w t s lam')
I=sp.I; om=sp.Rational(-1,2)+sp.sqrt(3)/2*I   # ω, ω^3=1
ok_all=True
def check(name,cond):
    global ok_all
    ok_all&=bool(cond); print(('PASS ' if cond else 'FAIL ')+name)

# L1. Высота на торе (R=2, r=1) после наклона на угол α. α=0 (зеркально-симметричное положение):
#     критические множества — две окружности; α≠0: ровно 4 изолированные точки с индексами 0,1,1,2.
R,r=2,1
def crit(alpha):
    X=(R+r*sp.cos(v))*sp.cos(u); Z=r*sp.sin(v)
    h=sp.sin(alpha)*X+sp.cos(alpha)*Z
    hu,hv=sp.diff(h,u),sp.diff(h,v)
    return h,hu,hv
h0,hu0,hv0=crit(0)
check('L1a α=0: ∂h/∂u ≡ 0 (критическое множество — окружности cos v=0)', sp.simplify(hu0)==0)
alpha=sp.Rational(3,10)
h,hu,hv=crit(alpha)
cands=[(0,sp.pi/2-alpha),(0,3*sp.pi/2-alpha),(sp.pi,sp.pi/2+alpha),(sp.pi,3*sp.pi/2+alpha)]
H=sp.hessian(h,(u,v))
idx=[]
for cu,cv in cands:
    assert abs(float(hu.subs({u:cu,v:cv})))<1e-12 and abs(float(hv.subs({u:cu,v:cv})))<1e-12
    ev=[float(e) for e in H.subs({u:cu,v:cv}).evalf().eigenvals()]
    idx.append(sum(1 for e in ev if e<0))
check(f'L1b α=0.3: 4 критические точки, индексы {sorted(idx)} = [0,1,1,2]', sorted(idx)==[0,1,1,2])
check('L1c χ = Σ(−1)^индекс = 0 (тор); у сферы высота: min+max, χ=2', sum((-1)**k for k in idx)==0)
# при α≠0 других критических точек нет: ∂h/∂u = −sinα (R+r cos v) sin u = 0 ⇒ sin u = 0
check('L1d α≠0: ∂h/∂u=0 ⇔ sin u=0 (поэтому точек ровно 4)', sp.simplify(hu+sp.sin(alpha)*(R+r*sp.cos(v))*sp.sin(u))==0)

# L2. Ветвь МУ7 y=x² ∩ ветвь МУ8 x=y²: x⁴=x ⇒ {0,1,ω,ω²}; три точки на расстоянии 1 от 0 и |y|=1.
roots=sp.solve(x**4-x,x)
check(f'L2a корни x⁴−x: {roots}', len(roots)==4 and 0 in roots)
nz=[q for q in roots if q!=0]
check('L2b три точки: |x|=1 (расстояние до линзы 0) и |y|=|x²|=1 ⇒ лежат на торе |x|=|y|=1',
      all(sp.simplify(sp.Abs(q)-1)==0 and sp.simplify(sp.Abs(q**2)-1)==0 for q in nz))

# L3. Тор как склейка двух листов: w² = x⁴ − x (4 точки ветвления) — род 1;
#     переворот x=1/t (линза 0 → ∞): (w t²)² = 1 − t³ ⇒ j = 0 (шестиугольный тор).
check('L3a x⁴−x без кратных корней ⇒ род (4/2 − 1) = 1', sp.discriminant(x**4-x,x)!=0)
lhs=sp.expand(((x**4-x).subs(x,1/t))*t**8)
check('L3b x=1/t: (x⁴−x)·t⁸ = t⁴·(1−t³), т.е. (w t²)² = 1 − t³', sp.expand(lhs-t**4*(1-t**3))==0)
def cr(a,b,c,d):  # двойное отношение
    return sp.simplify((a-c)*(b-d)/((a-d)*(b-c)))
def jlam(L): return sp.nsimplify(sp.simplify(256*(L**2-L+1)**3/(L**2*(L-1)**2)))
l1=cr(0,1,om,om**2)
check(f'L3c двойное отношение (0,1,ω,ω²) = {sp.nsimplify(l1)}; j = {jlam(l1)} (= 0)', jlam(l1)==0)
l2=sp.limit((-1-0)*(1-t)/((-1-t)*(1-0)),t,sp.oo)   # (−1,1;0,∞)
check(f'L3d точки C-104 (−1,0,1,∞): λ = {l2}; j = {jlam(l2)} (= 1728, квадратный тор)', jlam(l2)==1728)

# L4. Три точки инварианта не несут (Мёбиус 3-транзитивен); четвёртая (линза) даёт двойное отношение = форму тора.
a,b,c=sp.Rational(2),sp.Rational(-3),I
M=lambda z:((z-a)*(b-c))/((z-c)*(b-a))   # a→0, b→1, c→∞
check('L4a любые три точки переводятся в 0,1,∞', [sp.simplify(M(a)),sp.simplify(M(b))]==[0,1])
d=sp.Rational(5)+2*I
N=lambda z:(2*z+1)/(z+7)   # произвольное дробно-линейное (полюс −7 не совпадает с точками)
check('L4b двойное отношение четырёх точек инвариантно при Мёбиусе', sp.simplify(cr(N(a),N(b),N(c),N(d))-cr(a,b,c,d))==0)
# L4c. Три точки, равноудалённые от линзы, НЕ дают квадратного тора (j=1728 ⇔ λ∈{−1,2,1/2}):
#      линза 0, точки 1, b, c на единичной окружности (поворот вокруг 0 — без ограничения общности).
check('L4c-0 j−1728 = 0 ⇔ λ ∈ {−1, 2, 1/2}', set(sp.solve(sp.numer(sp.together(256*(lam**2-lam+1)**3-1728*lam**2*(lam-1)**2)),lam))=={-1,2,sp.Rational(1,2)})
g=sp.symbols('g',real=True); c_=sp.cos(g)+I*sp.sin(g)
# λ = cr(0,1,b,c) = b(1−c)/(c(1−b)); λ=−1 ⇒ b̄+c̄=2 ⇒ b=c=1; λ=2 ⇒ |1+c|=2; λ=1/2 ⇒ |2−c|=1
check('L4c-1 λ=2: |1+c|²=4 при |c|=1 ⇒ cos g = 1 (c=1, вырождение)', sp.simplify(sp.expand(sp.Abs(1+c_)**2-4).rewrite(sp.cos))==2*sp.cos(g)-2)
check('L4c-2 λ=1/2: |2−c|²=1 при |c|=1 ⇒ cos g = 1 (c=1, вырождение)', sp.simplify(sp.expand(sp.Abs(2-c_)**2-1).rewrite(sp.cos))==4-4*sp.cos(g))
lens_sq=cr(0,1,I,-1)
check(f'L4c-3 пример: точки 1, i, −1 вокруг линзы 0 → j = {jlam(lens_sq)} (не 1728)', jlam(lens_sq)!=1728)

# L5. Инверсия с центром в линзе 0 и радиусом 1: z ↦ 1/z̄ — неподвижны 1,ω,ω²; 0 ↔ ∞.
#     На сфере Римана это отражение в плоскости экватора (X,Y,Z) ↦ (X,Y,−Z).
inv=lambda z: 1/sp.conjugate(z)
check('L5a 1, ω, ω² неподвижны', all(sp.simplify(inv(q)-q)==0 for q in nz))
def st(z):  # стереографическая проекция на единичную сферу
    z=sp.nsimplify(z); m=sp.Abs(z)**2
    return [sp.simplify(2*sp.re(z)/(1+m)),sp.simplify(2*sp.im(z)/(1+m)),sp.simplify((m-1)/(1+m))]
zz=sp.Rational(1,3)+sp.Rational(1,2)*I
A,B=st(zz),st(inv(zz))
check('L5b образ инверсии на сфере = отражение в экваторе', [sp.simplify(A[0]-B[0]),sp.simplify(A[1]-B[1]),sp.simplify(A[2]+B[2])]==[0,0,0])

# L6. Отражение — степень поворота на обоих особых торах:
#     j=1728: t4:(x,y)↦(−x,iy), t4² = (x,−y);  j=0: t6:(t,s)↦(ωt,−s) на s²=1−t³, t6³ = (t,−s).
check('L6a t6 сохраняет s²=1−t³', sp.simplify(((-s)**2-(1-(om*t)**3))-(s**2-(1-t**3)))==0)
p=(t,s)
for _ in range(3): p=(sp.expand(om*p[0]),-p[1])
check('L6b t6³ = (t,−s) — смена знака корня', sp.simplify(p[0]-t)==0 and p[1]==-s)
check('L6c фактор тора по w↦−w — сфера: 2g−2 = 2(2·0−2) + 4 при g=1', 2*1-2==2*(2*0-2)+4)

# L7. Тор Клиффорда |x|=|y|=1 лежит на S³ радиуса √2; стереографическая проекция (из N=(0,0,0,√2), не на торе)
#     даёт в R³ тор вращения: профиль a=0 — окружность.
rho=sp.sqrt(2); bb=sp.symbols('bb',real=True)
X=rho/(rho-sp.sin(bb)); Zc=rho*sp.cos(bb)/(rho-sp.sin(bb))
# профиль — окружность с центром (X0,0): найдём X0, rr по трём точкам и проверим тождественно
pts=[(X.subs(bb,q),Zc.subs(bb,q)) for q in (0,sp.pi/2,-sp.pi/2)]
X0,rr2=sp.symbols('X0 rr2')
sol=sp.solve([(pp[0]-X0)**2+pp[1]**2-rr2 for pp in pts[:2]],[X0,rr2],dict=True)[0]
circ=sp.simplify((X-sol[X0])**2+Zc**2-sol[rr2])
check(f'L7 профиль — окружность: центр {sp.nsimplify(sol[X0])}, радиус {sp.nsimplify(sp.sqrt(sol[rr2]))}; R/r = {sp.nsimplify(sol[X0]/sp.sqrt(sol[rr2]))}', circ==0)

print('ALL PASS' if ok_all else 'SOME FAIL')
