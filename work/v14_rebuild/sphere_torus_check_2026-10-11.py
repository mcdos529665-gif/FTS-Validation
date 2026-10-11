# Свидетель (candidate, вне общего маршрута) к sphere_holes_note_2026-10-11.md:
# пересечение МУ7∩МУ8, тор y^2=x^3-x, вырождение в остриё, род по степени, периоды cos/exp.
# Запуск: py -3.11 -X utf8 work/v14_rebuild/sphere_torus_check_2026-10-11.py
import sympy as sp
x,y,z,eps,t=sp.symbols('x y z eps t')
I=sp.I
# 1. MU7 (y=+-x^2) ∩ MU8 (y^2=+-x): all affine intersection points
pts=set()
for a in (1,-1):
    for b in (1,-1):
        for s in sp.solve([y-a*x**2, y**2-b*x],[x,y],dict=True):
            pts.add((sp.nsimplify(s[x]),sp.nsimplify(s[y])))
pts=sorted(pts,key=str)
print('7∩8 points:',len(pts))
nonbase=[p for p in pts if p!=(0,0)]
print(' all |x|=|y|=1 except base:',all(sp.simplify(sp.Abs(p[0])-1)==0 and sp.simplify(sp.Abs(p[1])-1)==0 for p in nonbase))
print(' x^6=1 for all nonbase:',all(sp.simplify(p[0]**6-1)==0 for p in nonbase), ' count',len(nonbase))
print(' real points:',[p for p in pts if p[0].is_real and p[1].is_real])
# per-pair: y=x^2, y^2=x -> x^4=x
print(' pair (y=x^2,y^2=x):',sp.factor(x**4-x))
# 2. projective: y=x^2 and y=-x^2 meet at [0:0:1],[0:1:0]
X,Y,Z=sp.symbols('X Y Z')
print('MU7 pair projective common pts:',sp.solve([Y*Z-X**2,Y*Z+X**2],[X,Y,Z],dict=True))
# 3. E: y^2=x^3-x
f=x**3-x
print('roots of x^3-x:',sp.solve(f,x))
a,b=-1,0
print('j-invariant:',sp.Rational(1728)*4*a**3/(4*a**3+27*b**2))
print('automorphism (x,y)->(-x,iy) preserves:',sp.expand((I*y)**2-((-x)**3-(-x)) + (y**2-f))==0)
for xv in [sp.Rational(-3,2),sp.Rational(-1,2),sp.Rational(1,2),2]:
    print('  x=',xv,' x^3-x =',f.subs(x,xv),'(hole)' if f.subs(x,xv)<0 else '(filled)')
# 4. degeneration eps->0
print('y^2=x^3-eps*x branch pts:',sp.solve(x**3-eps*x,x),' -> eps=0:',sp.factor((x**3-eps*x).subs(eps,0)))
# 5. degree-genus
print('genus by degree:',{d:(d-1)*(d-2)//2 for d in (1,2,3,4)})
# 6. Riemann-Hurwitz for double cover branched at n points: g = n/2 - 1
print('RH: 2 pts ->',2//2-1,' 4 pts ->',4//2-1)
# 7. y=x^3 is rational (parametrized by x) ; cusp y^2=x^3 parametrized by (t^2,t^3)
print('cusp param ok:',sp.simplify((t**3)**2-(t**2)**3)==0)
# 8. periods: cos period 2pi, exp period 2pi*i (= i * 2pi)
print('cos(x+2pi)=cos x:',sp.simplify(sp.cos(x+2*sp.pi)-sp.cos(x))==0,' exp(x+2pi i)=exp x:',sp.simplify(sp.exp(x+2*sp.pi*I)-sp.exp(x))==0,' cos(ix)=cosh x:',sp.simplify(sp.cos(I*x)-sp.cosh(x))==0)
