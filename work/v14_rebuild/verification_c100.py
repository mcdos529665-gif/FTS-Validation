"""Проверки addendum_2026-10-08_rotation_projection.md (C-100…C-104).
Чистый Python. Запуск: python -X utf8 verification_c100.py
Проверяются только математические факты; смысл уровней (СУ) не проверяется."""
import cmath, itertools, math
from fractions import Fraction as Fr
from math import comb

res = []
def check(cid, desc, cond):
    res.append(bool(cond)); print("PASS" if cond else "FAIL", cid, desc)

grid = [Fr(a, 4) for a in range(-16, 17)]
close = lambda a, b, e=1e-9: abs(a - b) <= e * max(1, abs(a), abs(b))
R90 = lambda p: (-p[1], p[0]); R90m = lambda p: (p[1], -p[0]); SW = lambda p: (p[1], p[0])
R180 = lambda p: (-p[0], -p[1]); MIR = lambda p: (p[0], -p[1])

# C-100: склейка МУ6∪МУ7 = |y|=x² при повороте на ±90° и при x↔y переходит в пару МУ8 y²=|x| и обратно;
# крест |y|=|x| (= МУ2∪МУ3 = МУ4∪МУ5 как множества) переходит сам в себя;
# противоположность y=−f(x) даёт для всех форм только зеркало y↦−y, поворот — частично.
U67 = [(t, s * t * t) for t in grid for s in (1, -1)]
U8 = [(s * y * y, y) for y in grid for s in (1, -1)]
on67 = lambda p: abs(p[1]) == p[0] * p[0]
on8 = lambda p: p[1] * p[1] == abs(p[0])
cross = lambda p: abs(p[1]) == abs(p[0])
ok = all(on8(op(p)) for op in (R90, R90m, SW) for p in U67)
ok &= all(on67(op(p)) for op in (R90, R90m, SW) for p in U8)
ok &= {(x, y) for x, y in [(t, s * t) for t in grid for s in (1, -1)]} == \
      {(x, y) for x, y in [(t, s * abs(t)) for t in grid for s in (1, -1)]}
ok &= all(cross(R90(p)) for p in [(t, s * t) for t in grid for s in (1, -1)])
forms = {"x": lambda x: x, "|x|": abs, "x²": lambda x: x * x,
         "√|x|": lambda x: math.sqrt(abs(x)), "x³": lambda x: x ** 3}
def gives_opposite(op, f):
    return all(close(float(op((t, f(t)))[1]), -float(f(op((t, f(t)))[0]))) for t in grid)
table = {n: tuple(gives_opposite(op, f) for op in (MIR, R90, R180)) for n, f in forms.items()}
ok &= table == {"x": (True, True, False), "|x|": (True, False, True), "x²": (True, False, True),
                "√|x|": (True, False, True), "x³": (True, False, False)}
check("C100", "|y|=x² ↔ y²=|x| при повороте ±90° и x↔y; крест |y|=|x| неподвижен; "
      "противоположность всем формам даёт только y↦−y (90° — для x, 180° — для чётных, x³ — ни один)", ok)

# C-101: двойка — единственное ненулевое x с x+x=x·x; то же равенство даёт длину = площади
# окружности при r=2; при x=2 умножение на x есть удвоение, степени 2,4,8.
ok = [x for x in range(-50, 51) if x + x == x * x] == [0, 2]
ok &= [r for r in range(-50, 51) if 2 * r == r * r] == [0, 2]                     # 2πr = πr² ⟺ 2r = r²
ok &= close(2 * math.pi * 2, math.pi * 2 ** 2)
ok &= all(2 * F == F + F for F in (2, 2 ** 2, 2 ** 3)) and (2, 2 ** 2, 2 ** 3) == (2, 4, 8)
ok &= 2 ** 3 == 2 ** 2 + 2 ** 2 and 2 ** 2 == 2 + 2                             # МУ9(2)=МУ6+МУ6, МУ6(2)=МУ2+МУ2
check("C101", "x+x=x·x ⟺ x∈{0,2}; 2πr=πr² ⟺ r∈{0,2}; при x=2: x·F=F+F, МУ2,МУ6,МУ9 = 2,4,8", ok)

# C-102: О1 как подстановка x = n−1 в МУn; МУ8 в форме y⁴=x² (C-76) над C при x=7 даёт ±√7, ±√−7;
# 2 раскладывается в числах с √−7; −7≡1 (mod 8); |GL(3,2)| = 168 = |PSL(2,7)|;
# контроль: сдвиг n−1 по числу совпадений с окнами не выделяется.
mu = {2: lambda a: [a], 3: lambda a: [-a], 4: lambda a: [abs(a), -abs(a)], 5: lambda a: [-abs(a)],
      6: lambda a: [a * a], 7: lambda a: [a * a, -a * a], 9: lambda a: [a ** 3]}
vals = {n: mu[n](n - 1) for n in mu}
ok = vals == {2: [1], 3: [-2], 4: [3, -3], 5: [-4], 6: [25], 7: [36, -36], 9: [512]}
roots = [s * math.sqrt(7) * u for s in (1, -1) for u in (1, 1j)]
ok &= all(close(abs(r ** 4 - 49), 0) for r in roots) and len({(round(r.real, 9), round(r.imag, 9)) for r in roots}) == 4
ok &= close(abs(cmath.sqrt(-7) - 1j * math.sqrt(7)), 0)
w = (1 + cmath.sqrt(-7)) / 2
ok &= close(abs(w * w.conjugate() - 2), 0) and close(abs(w * w - w + 2), 0) and (-7) % 8 == 1
ok &= [d for d in range(-1, -40, -1) if all((-d) % (p * p) for p in range(2, 7)) and d % 8 == 1][0] == -7
gl = sum(1 for m in itertools.product((0, 1), repeat=9)
         if (m[0] * (m[4] * m[8] - m[5] * m[7]) - m[1] * (m[3] * m[8] - m[5] * m[6])
             + m[2] * (m[3] * m[7] - m[4] * m[6])) % 2)
ok &= gl == 168 == 7 * (7 * 7 - 1) // 2 and 2 ** 3 - 1 == 7
WIN = set(range(3, 26, 2))
def hits(n, a):
    if n == 8:                                       # ±√a, ±i√a: корень окна (√−1,√−2,√−3,√5,√−7) или целое окно
        return a in (1, 2, 3, 5, 7) or (a > 0 and math.isqrt(a) ** 2 == a and math.isqrt(a) in WIN)
    return any(isinstance(v, int) and abs(v) in WIN for v in mu[n](a)) if n in mu else False
counts = {k: sum(1 for n in range(2, 10) if n + k != 0 and hits(n, n + k)) for k in range(-3, 3)}
ok &= counts[-1] == 3 and max(counts.values()) == 3 and sum(1 for v in counts.values() if v == 3) >= 2
check("C102", "МУn(n−1): 1,−2,±3,−4,25,±36,512; y⁴=49 → ±√7,±i√7; 2=((1+√−7)/2)((1−√−7)/2), −7≡1 mod 8; "
      "|GL(3,2)|=168; контроль сдвигов: n−1 не единственный максимум совпадений", ok)

# C-103: треугольник Паскаля mod 2 = повторение a≠b из одной единицы (правило О1);
# число нечётных в строке n = 2^popcount(n); полные строки 2^k−1; строка 7 — 8 клеток, строка 8 — 2;
# узлы канона 3, 7, 15 — полные строки, узел 11 — нет (8 из 12).
rows = [[1]]
for n in range(1, 65):
    prev = rows[-1]
    rows.append([1] + [int(prev[k - 1] != prev[k]) for k in range(1, n)] + [1])
ok = all(rows[n] == [comb(n, k) % 2 for k in range(n + 1)] for n in range(65))
ok &= all(sum(rows[n]) == 2 ** bin(n).count("1") for n in range(65))
full = [n for n in range(65) if all(rows[n])]
ok &= full == [0, 1, 3, 7, 15, 31, 63] and sum(rows[7]) == 8 and sum(rows[8]) == 2
ok &= [n for n in (3, 7, 11, 15) if n in full] == [3, 7, 15] and (sum(rows[11]), len(rows[11])) == (8, 12)
check("C103", "Паскаль mod 2 = итерация a≠b; нечётных 2^popcount(n); полные строки 0,1,3,7,15,31,63; "
      "строка 7: 8 клеток, строка 8: 2; узлы 3,7,15 полные, 11 — нет (8/12)", ok)

# C-104: x²=x ⟺ x∈{0,1}; x³=x ⟺ x∈{−1,0,1}; t³=t ⟺ t=P−Q (P,Q — ортогональные проекции), t²=P+Q;
# sign³=sign; Фано: 7 точек F₂³∖0, прямые {a,b,a⊕b}, 7 прямых по 3 точки, любые две точки — ровно одна прямая.
ok = [x for x in grid if x * x == x] == [0, 1] and [x for x in grid if x ** 3 == x] == [-1, 0, 1]
mat = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
diag = lambda *d: [[d[i] if i == j else 0 for j in range(3)] for i in range(3)]
add = lambda A, B, s=1: [[A[i][j] + s * B[i][j] for j in range(3)] for i in range(3)]
T, P, Q = diag(1, -1, 0), diag(1, 0, 0), diag(0, 1, 0)
T2 = mat(T, T)
ok &= mat(T2, T) == T and T == add(P, Q, -1) and mat(P, Q) == diag(0, 0, 0) == mat(Q, P)
ok &= T2 == add(P, Q) and mat(T2, T2) == T2
sgn = lambda x: (x > 0) - (x < 0)
ok &= all(sgn(x) ** 3 == sgn(x) and sgn(x ** 3) == sgn(x) for x in grid)
pts = [v for v in itertools.product((0, 1), repeat=3) if any(v)]
xor = lambda a, b: tuple(i ^ j for i, j in zip(a, b))
lines = {frozenset((a, b, xor(a, b))) for a, b in itertools.combinations(pts, 2)}
ok &= len(pts) == 7 and len(lines) == 7 and all(len(l) == 3 for l in lines)
ok &= all(sum(1 for l in lines if a in l and b in l) == 1 for a, b in itertools.combinations(pts, 2))
check("C104", "x²=x → {0,1}; x³=x → {−1,0,1}; t=P−Q, t²=P+Q — проекция; sign³=sign; "
      "Фано: 7 прямых {a,b,a⊕b} по 3 точки, две точки — одна прямая", ok)

print(f"\nИТОГ: {sum(res)} PASS / {len(res) - sum(res)} FAIL")
raise SystemExit(0 if all(res) else 1)
