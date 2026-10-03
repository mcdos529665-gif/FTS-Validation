import sympy as s
w,v=s.symbols('w v',real=True)
losses=[(w-1)**2/2,(w+1)**2/2]
L=s.expand(sum(losses))
g=[s.diff(x,w).subs(w,0) for x in losses]
assert L==w*w+1 and g==[-1,1] and s.diff(L,w).subs(w,0)==0
joint=s.expand(((w+v-1)**2+(w-v+1)**2)/2)
assert joint==w*w+(v-1)**2 or s.expand(joint-w*w-(v-1)**2)==0
assert joint.subs({w:0,v:1})==0
assert s.diff(joint,v).subs({w:0,v:0})==-2
x=s.symbols('x')
f0=s.Integer(0); fit=1-x*x
train=(-1,1); test=(0,)
tr0=sum((f0.subs(x,t))**2 for t in train)
tr1=sum((fit.subs(x,t))**2 for t in train)
te0=sum((f0.subs(x,t))**2 for t in test)
te1=sum((fit.subs(x,t))**2 for t in test)
assert (tr0,tr1,te0,te1)==(0,0,0,1)
print("L_shared =",L,"; at w=0 gradients =",g,"; total=0; loss=1")
print("L_with_context =",joint,"; at (w,v)=(0,0) dL/dv=-2; at (0,1) loss=0")
print("Same exact train fit, different held-out error:",(tr0,tr1,te0,te1))
print("PASS: three limited mathematical witnesses; not a neural experiment or FTS status test")

classes={"hammer":"tool","saw":"tool"}
actions={"hammer":"strike","saw":"cut"}
assert classes["hammer"]==classes["saw"]
assert actions["hammer"]!=actions["saw"]
print("PASS: common class does not answer the operation question")
