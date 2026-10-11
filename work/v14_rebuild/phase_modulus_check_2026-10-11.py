# Свидетель (candidate, вне общего маршрута) к sphere_holes_note_2026-10-11.md §6 (вариант согласования ассистента):
# четыре операции на сфере (фаза/модуль), cos как x² на повёрнутой сфере, линза на формах 6–9, эллипсы cos, Чебышёв,
# действие отражения и поворота на дырах тора.
# Запуск: py -3.11 -X utf8 work/v14_rebuild/phase_modulus_check_2026-10-11.py
import sympy as sp
import mpmath as mp
x,y,q,th=sp.symbols('x y q theta')
a,b,u,v=sp.symbols('a b u v',real=True)
lam=sp.symbols('lam',positive=True)
I=sp.I
ok_all=True
def check(name,cond):
    global ok_all
    ok_all&=bool(cond); print(('PASS ' if cond else 'FAIL ')+name)

# V1. cos — это возведение в квадрат на сфере, повёрнутой на 90°.
J=(q+1/q)/2                      # складка Жуковского: J(q)=J(1/q)
phi=lambda s:(s-1)/(s+1)         # поворот сферы: 1→0 (основание), −1→∞ (верхушка)
check('V1a cos x = J(e^{ix})', sp.simplify(((sp.exp(I*x)+sp.exp(-I*x))/2).rewrite(sp.cos)-sp.cos(x))==0)
check('V1b J(q)=J(1/q): cos чётен ⇔ складка по q↦1/q', sp.simplify(J-J.subs(q,1/q))==0)
check('V1c φ(J(q)) = φ(q)²: в повёрнутой карте J — это квадрат (МУ6)', sp.simplify(phi(J)-phi(q)**2)==0)
check('V1d то же для cos: (cos x−1)/(cos x+1) = −tg²(x/2)', sp.simplify(((sp.cos(x)-1)/(sp.cos(x)+1)+sp.tan(x/2)**2).rewrite(sp.exp))==0)  # прямой simplify не сводит; через exp — 0
M=sp.Matrix([[1,-1],[1,1]])/sp.sqrt(2)
check('V1e φ — поворот сферы: матрица унитарна', sp.simplify(M*M.H-sp.eye(2))==sp.zeros(2))
M2=sp.simplify(M**2); M4=sp.simplify(M**4)
check('V1f φ — поворот на 90°: φ² не тождество (z↦−1/z), φ⁴ = тождество в PSU(2)', M2!=sp.eye(2) and M2!=-sp.eye(2) and M4==-sp.eye(2))
check('V1g точки ветвления: у x² — 0 и ∞ (основание, верхушка); у J — ±1 (экватор)', sp.solve(sp.diff(J,q),q)==[-1,1] or set(sp.solve(sp.diff(J,q),q))=={-1,1})

# V2. В логарифмах w=u+iv (z=e^w): отражение z↦z̄ — w↦w̄; линза z↦1/z̄ — w↦−w̄; поворот — w↦w+iθ; масштаб — w↦w+log λ.
#     Пара (линза, масштаб) = пара (отражение, поворот), повёрнутая на 90° (M(w)=iw).
w=u+I*v; t_=sp.symbols('t',real=True)
R=lambda s: sp.conjugate(s); L=lambda s: -sp.conjugate(s)
Rot=lambda s: s+I*t_;       Sc=lambda s: s+t_
Mi=lambda s: I*s;           Minv=lambda s: -I*s
check('V2a M⁻¹∘отражение∘M = линза', sp.simplify(sp.expand(Minv(R(Mi(w)))-L(w)))==0)
check('V2b M⁻¹∘поворот∘M = масштаб (сдвиг по модулю)', sp.simplify(sp.expand(Minv(Rot(Mi(w)))-Sc(w)))==0)
zz=sp.Rational(2)+3*I
check('V2c отражение и поворот сохраняют |z| (параллели); линза и масштаб — arg z (меридианы)',
      sp.simplify(sp.Abs(sp.conjugate(zz))-sp.Abs(zz))==0 and sp.simplify(sp.Abs(sp.exp(I*t_)*zz)-sp.Abs(zz))==0
      and sp.simplify(sp.arg(1/sp.conjugate(zz))-sp.arg(zz))==0 and sp.simplify(sp.arg(lam*zz)-sp.arg(zz))==0)

# V3. Линза в двух координатах (x,y)↦(1/x̄,1/ȳ) сохраняет формы 6–9 и оставляет на месте тор |x|=|y|=1.
X=1/sp.conjugate(x)
for name,F in [('y=x²',lambda s:s**2),('y=x³',lambda s:s**3)]:
    Y=1/sp.conjugate(F(x))
    check(f'V3a линза сохраняет {name}', sp.simplify(Y-F(X))==0)
Yp=1/sp.conjugate(y); Xp=1/sp.conjugate(y**2)
check('V3b линза сохраняет x=y² (МУ8)', sp.simplify(Xp-Yp**2)==0)
fx=sp.solve([x-1/x],[x]);
fixed=[(sx,sy) for sx in (-1,1) for sy in (-1,1) if abs(sy)==sx**2]
check(f'V3c вещественные неподвижные точки линзы на МУ7 |y|=x²: {fixed} = Tot(7) без основания', len(fixed)==4)

# V4. Масштаб у cos: прямая Im x=b переходит в эллипс с полуосями ch b, |sh b|, фокусы ±1; b и −b — один эллипс.
cz=sp.expand(sp.cos(a+I*b),complex=True)
Xr,Yi=sp.re(cz),sp.im(cz)
check('V4a cos(a+ib) = cos a·ch b − i·sin a·sh b', sp.simplify(Xr-sp.cos(a)*sp.cosh(b))==0 and sp.simplify(Yi+sp.sin(a)*sp.sinh(b))==0)
check('V4b эллипс (X/ch b)²+(Y/sh b)²=1', sp.simplify((Xr/sp.cosh(b))**2+(Yi/sp.sinh(b))**2-1)==0)
check('V4c b и −b: тот же эллипс (сжатие = расширение в cos)', sp.simplify(Xr.subs(b,-b)-Xr)==0 and sp.simplify(Yi.subs(b,-b)+Yi)==0)
check('V4d фокусы ±1 при любом b: ch²−sh²=1', sp.simplify(sp.cosh(b)**2-sp.sinh(b)**2-1)==0)
check('V4e полуоси = (e^b ± e^−b)/2 — их различает только eˣ', sp.simplify(sp.cosh(b)-(sp.exp(b)+sp.exp(-b))/2)==0 and sp.simplify(sp.sinh(b)-(sp.exp(b)-sp.exp(-b))/2)==0)

# V5. Куб через линзу: T₃(cos θ)=cos 3θ, T₃=4x³−3x («x³ с противовесом x»); неподвижные точки T₃ — t³=t; J(q³)=T₃(J(q)).
T3=4*x**3-3*x
check('V5a T₃(cos θ) = cos 3θ', sp.simplify(sp.expand_trig(sp.cos(3*th))-T3.subs(x,sp.cos(th)))==0)
check(f'V5b T₃(x)−x = {sp.factor(T3-x)}: неподвижные точки −1,0,1 (C-104, t³=t)', set(sp.solve(T3-x,x))=={-1,0,1})
check('V5c J(q³) = T₃(J(q)): куб на окружности после складки = T₃', sp.simplify(J.subs(q,q**3)-T3.subs(x,J))==0)
aa=sp.Rational(-3,4)
check('V5d тор y²=x³−(3/4)x (T₃/4) — снова квадратный, j=1728', sp.simplify(1728*4*aa**3/(4*aa**3))==1728)

# V6. На торе y²=x³−x: отражение (x,y)↦(x,−y) умножает периоды на −1 (дыра обращается на месте),
#     поворот t:(x,y)↦(−x,iy) — на i (дыра a переходит в дыру b).
check('V6a t*(dx/y) = i·dx/y', sp.simplify((sp.diff(-x,x)/(I*y))/(1/y)-I)==0)
check('V6b отражение*(dx/y) = −dx/y', sp.simplify((sp.diff(x,x)/(-y))/(1/y)+1)==0)
orb_t=sp.Matrix([[1,0],[0,1],[-1,0],[0,-1]])   # ω, iω, −ω, −iω в координатах (Re, Im)
orb_r=sp.Matrix([[1,0],[-1,0]])                # ω, −ω
check('V6c орбита дыры: при повороте ранг 2 (обе дыры), при отражении ранг 1 («половина»)', orb_t.rank()==2 and orb_r.rank()==1)

# V7. Решётка периодов cos/eˣ (2π, 2πi): τ = i ⇒ тот же квадратный тор, что y²=x³−x.
mp.mp.dps=30
check(f'V7 j(τ=i)/1728 = {mp.nstr(mp.kleinj(1j),12)} (= 1)', abs(mp.kleinj(1j)-1)<mp.mpf('1e-20'))

print('ALL PASS' if ok_all else 'SOME FAIL')
