"""Exact local witnesses for OQ proposals, 2026-10-05.
These checks concern stated mathematical models, not FTS level semantics.
Run with Python -X utf8 and SymPy. No canon or report mutation.
"""
import itertools
import json
import math
import sympy as s

checks = []
def check(name, ok, evidence):
    checks.append({"id": name, "pass": bool(ok), "evidence": evidence})

x, a, b, q, t = s.symbols("x a b q t", real=True)
units = [v for v in range(1,48) if math.gcd(v,48)==1]
generated = sorted({pow(5,i,48)*pow(47,j,48)*pow(17,k,48)%48
                    for i in range(4) for j in range(2) for k in range(2)})
check("OC01_units48", generated==units and pow(5,2,48)==25
      and pow(5,4,48)==1 and pow(47,2,48)==1 and pow(17,2,48)==1,
      {"group":"C4 x C2 x C2","generators":[5,47,17],"units":units,"5_squared_mod48":25})
def subgroup(v,m):
    result={1}; z=v%m
    while z not in result:
        result.add(z); z=z*v%m
    return frozenset(result)
cyclic = subgroup(5,96)
same = [v for v in range(1,96) if math.gcd(v,96)==1 and subgroup(v,96)==cyclic]
check("OC02_cyclic_subgroup_not_just_inverse",len(cyclic)==8 and len(same)==4,
      {"modulus":96,"same_generated_subgroup":same,"order_of_5":len(cyclic)})
values=[s.Rational(k,2) for k in range(-6,7)]
section=lambda v: 1 if v<=0 else -1
check("OC03_cross_section",all(section(v)*v==-abs(v) for v in values),
      "epsilon(0)=+1 chosen explicitly; sign(0)=0 is not a branch label")
cross={2,-2}; chosen=-2
check("OC04_relation_product", {v*chosen for v in cross}=={-4,4},
      {"x":2,"retained_times_selected":sorted(v*chosen for v in cross),
       "limitation":"a relation times a section does not select -x^2"})
check("OC05_polarization", s.expand((a+b)**4-(a-b)**4-8*a*b*(a*a+b*b))==0
      and s.expand((a+b)**3-(a-b)**3-2*b*(3*a*a+b*b))==0,
      "Even N gives exchange symmetry; cubic N has D(0,1)=2 and D(1,0)=0")
check("OC06_branch_bit", 1**2==(-1)**2 and s.sign(1)!=s.sign(-1),
      "No single-valued sign readout factors through x^2 on R excluding 0")
P=s.Matrix([[s.Rational(3,4),s.Rational(1,4)],[s.Rational(1,4),s.Rational(3,4)]])
Q=P*P; reverse=Q.inv()*P
risk=lambda matrix: sum(min(matrix[0,j],matrix[1,j]) for j in range(2))/2
check("OC07_blackwell", Q==s.Matrix([[s.Rational(5,8),s.Rational(3,8)],[s.Rational(3,8),s.Rational(5,8)]])
      and reverse[0,1]<0 and risk(P)==s.Rational(1,4) and risk(Q)==s.Rational(3,8),
      {"P4":str(Q),"reverse_channel":str(reverse),"risks":["1/4","3/8"]})
X=(1,4); L=tuple(itertools.product(X,(-1,1)))
pi=lambda z:z[0]; rho=lambda z:z[1]; flip=lambda z:(z[0],-z[1])
sections=[dict(zip(X,signs)) for signs in itertools.product((-1,1),repeat=2)]
check("OC08_lift_section",all(pi((v,1))==v for v in X)
      and rho((1,1))!=rho((1,-1))
      and all(any((v,h[v])!=flip((v,h[v])) for v in X) for h in sections),
      "Set section exists; none is equivariant under branch swap with trivial action on X")
roots=[2-s.sqrt(4-q),2+s.sqrt(4-q)]
check("OC09_real_complex_boundary",all(s.simplify(q+(y-2)**2-4)==0 for y in roots)
      and [s.simplify(y.subs(q,4)) for y in roots]==[2,2]
      and set(s.solve(5+(x-2)**2-4,x))==set(),
      "For q>=0 real roots exist iff q<=4; for q=5 complex roots are 2+-i")
A=s.Matrix([[1,1],[0,1]]); B=s.diag(2,1); K=s.kronecker_product(A,B)
v=s.Matrix([1,2,3,4]); G=s.eye(4); Gp=K.inv().T*G*K.inv()
T=s.Matrix([[1,2,0,0],[0,1,0,0],[0,0,2,1],[0,0,0,2]])
check("OC10_tensor_covariance",(v.T*K.T*Gp*K*v)[0]==(v.T*G*v)[0]
      and (K*T*K.inv())*(K*v)==K*(T*v),
      "K=A tensor B; metric transforms by K^-T G K^-1; operator by K T K^-1")
R=s.Matrix([[s.cos(t),-s.sin(t)],[s.sin(t),s.cos(t)]])
H=s.Matrix([[s.cosh(t),s.sinh(t)],[s.sinh(t),s.cosh(t)]])
eta=s.diag(1,-1)
check("OC11_dynamic_forms",s.simplify(R.T*R)==s.eye(2) and s.simplify(H.T*eta*H)==eta,
      "Circular and hyperbolic dynamics preserve different quadratic forms")
check("OC12_hyperbola_not_negation",(0**2+1**2-1)==0 and (0**2-1**2-1)!=0,
      "Negating an equation preserves its zero set; switching its quadratic signature does not")
p,n=s.symbols("p n")
u6=p*n*(p+n);u7=u6+p*n+p+n
check("OC13_provenance_polynomials",s.expand(u6)==p*p*n+p*n*n
      and s.expand(u7-u6)==p*n+p+n,
      {"u6":str(s.expand(u6)),"u7":str(s.expand(u7)),
       "limit":"commutative semiring forgets original grouping; AST still needed"})
# Disjoint versus overlapping windows do not force an injective or invertible projection.
f={7:5,8:6,9:7};g={9:7,10:8,11:9}
check("OC14_window_projection_candidate",g[9]==7 and f[7]==5,
      "Shift by -2 is an available map on listed triples; adjacency alone does not select it")
# Candidate 15 is unit complex orbit, not an odd single-valued real function.
check("OC15_parity_type_limit",s.simplify(s.exp(s.I*0)+s.exp(-s.I*0))==2,
      "exp(i theta) is not odd in theta (at theta=0 it equals 1); a locus has no function parity")

print(json.dumps({"checks":checks,"passed":sum(c["pass"] for c in checks),
                  "total":len(checks)},ensure_ascii=False,indent=2))
raise SystemExit(0 if all(c["pass"] for c in checks) else 1)
