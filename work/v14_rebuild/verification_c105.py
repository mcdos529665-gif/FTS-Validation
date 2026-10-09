"""Проверки МУ7 как множества |y|=x² (C-105…C-108).
Основание: решение автора 2026-10-08 (A_07 = |y|=x*x, запрет y≠x² снят); решение 04 группы 4–10
(принято по поручению автора через консультацию, 2026-10-09). Продолжают G60-19, G60-41, G60-50.
Чистый Python. Запуск: py -3.11 -X utf8 verification_c105.py
Проверяются только математические факты; смысл уровней (СУ) не проверяется.

Предсказания, записанные до первого запуска:
  C-105  МУ7 = МУ6 ∪ ветвь (y=−x²); МУ6 ⊂ МУ7; над x≠0 два значения y, над x=0 одно.
  C-106  Как функции x² и −x² совпадают только в нуле; МУ7 замкнута относительно x↦−x и y↦−y;
         отношение y/x² на МУ7 (x≠0) пробегает {+1,−1}, на ветви — {−1}.
  C-107  Tot(МУ7) — коллапс отношения {+1,−1}→{1} — оставляет ровно МУ6; Var{x²,−x²}=(x²)², Var{x²,x²}=0
         (форма C-61 для пары {6,7}).
  C-108  При x=1: МУ7(1)={1,−1}=МУ2(1)∪МУ3(1), ветвь даёт МУ3(1) (равенство C-52 — для ветви);
         зеркальные пары {2,3} и {4,5} совпадают с отражением точно, у {6,7} отражение МУ6 лежит в МУ7,
         но не равно ей; МУ7 переходит сама в себя (C-60 — для ветви)."""
from fractions import Fraction as Fr

res = []


def check(cid, desc, cond):
    res.append(bool(cond))
    print("PASS" if cond else "FAIL", cid, desc)


grid = [Fr(a, 4) for a in range(-16, 17)]
ygrid = [Fr(b, 16) for b in range(-256, 257)]
MU6 = {(t, t * t) for t in grid}
BRANCH = {(t, -t * t) for t in grid}                       # ветвь МУ7: y = −x²
MU7 = {(t, s * t * t) for t in grid for s in (1, -1)}       # множество |y| = x²
on_mu7 = lambda x, y: abs(y) == x * x

# C-105: МУ7 = МУ6 ∪ ветвь, МУ6 ⊂ МУ7, лишних точек нет; над x≠0 два значения, над 0 одно.
ok = MU6 <= MU7 and BRANCH <= MU7 and MU7 == MU6 | BRANCH
ok &= {(x, y) for x in grid for y in ygrid if on_mu7(x, y)} == MU7
ok &= all(len({y for (xx, y) in MU7 if xx == t}) == (1 if t == 0 else 2) for t in grid)
check("C105", "МУ7 (|y|=x²) = МУ6 ∪ ветвь y=−x²; МУ6 ⊂ МУ7; над x≠0 два значения y — не график функции", ok)

# C-106: как функции x² и −x² совпадают только в нуле; МУ7 замкнута по x↦−x и y↦−y;
# отношение y/x² на МУ7 пробегает {+1,−1}, на ветви — только {−1}.
ok = [t for t in grid if t * t == -t * t] == [0]
ok &= all(((-x), y) in MU7 and (x, -y) in MU7 for (x, y) in MU7)
ok &= {y / (x * x) for (x, y) in MU7 if x != 0} == {1, -1}
ok &= {y / (x * x) for (x, y) in BRANCH if x != 0} == {-1}
check("C106", "x² и −x² как функции совпадают только в x=0; МУ7 чётна по x и по y; y/x² на МУ7 ∈ {+1,−1}, на ветви ∈ {−1}", ok)


# C-107: Tot(МУ7) = МУ6 — коллапс Z/2 → {1} отношения y/x² оставляет ровно МУ6;
# форма C-61 для пары {6,7}: Var{c,−c}=c², Var{c,c}=0 при c=x².
def var(vals):
    m = sum(vals) / len(vals)
    return sum((v - m) ** 2 for v in vals) / len(vals)


tot = {(x, y) for (x, y) in MU7 if x == 0 or y == x * x}
ok = tot == MU6
ok &= all(var([x * x, -x * x]) == (x * x) ** 2 and var([x * x, x * x]) == 0 for x in grid if x != 0)
check("C107", "Tot(МУ7) (коллапс {+1,−1}→{1} для y/x²) = МУ6; Var{x²,−x²}=(x²)², Var{x²,x²}=0", ok)

# C-108: значения при x=1 и зеркальные пары.
mu2 = lambda x: {x}
mu3 = lambda x: {-x}
mu4 = lambda x: {abs(x)}
mu5 = lambda x: {-abs(x)}
mu6 = lambda x: {x * x}
mu7 = lambda x: {x * x, -x * x}
one = Fr(1)
ok = mu7(one) == {1, -1} == mu2(one) | mu3(one)
ok &= mu3(one) <= mu7(one) and mu6(one) <= mu7(one)
ok &= {-x * x for x in [one]} == mu3(one)                                  # ветвь при x=1 = МУ3(1) (C-52)
ok &= all({-v for v in mu2(x)} == mu3(x) for x in grid)                    # отражение МУ2 = МУ3
ok &= all({-v for v in mu4(x)} == mu5(x) for x in grid)                    # отражение МУ4 = МУ5
ok &= not all({-v for v in mu6(x)} == mu7(x) for x in grid)                # отражение МУ6 ≠ МУ7
ok &= all({-v for v in mu6(x)} <= mu7(x) for x in grid)                    # но лежит в МУ7
ok &= all({-v for v in mu7(x)} == mu7(x) for x in grid)                    # МУ7 переходит сама в себя
check("C108", "x=1: МУ7(1)={1,−1}=МУ2(1)∪МУ3(1); отражение МУ2=МУ3 и МУ4=МУ5 точно, отражение МУ6 ⊂ МУ7, не равно; "
      "МУ7 переходит сама в себя", ok)

print(f"\nИТОГ: {sum(res)} PASS / {len(res) - sum(res)} FAIL")
raise SystemExit(0 if all(res) else 1)
