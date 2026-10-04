"""Сверка таблицы окон windows_table.tsv со счётом. Чистый Python.
Запуск из папки work/v14_rebuild: python verification_windows_table.py
Проверяет вычислимые столбцы (шаг, узлы, середины, группа, тип, неразличимые пары) и то,
что каждая проверка C-xx из столбца «проверка» есть в файлах verification_*.py рядом.
Смысловые столбцы (теория, статус, примечание) сверяются с addendum вручную."""
import glob, os
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "windows_table.tsv"), encoding="utf-8")]
head, rows = rows[0], rows[1:]
col = {h: i for i, h in enumerate(head)}
src = "".join(open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(HERE, "verification_*.py")))

def units(s): return [x for x in range(1, s) if gcd(x, s) == 1] if s > 2 else [1]
def order(a, s):
    if s <= 2: return 1
    k, y = 1, a % s
    while y != 1: y = y * a % s; k += 1
    return k
def inv(a, s): return 1 if s <= 2 else next(b for b in range(1, s) if a * b % s == 1)
def group(s):
    U = units(s); o = [order(a, s) for a in U]; N = len(U)
    if N == 1: return "{1}", "зеркальная"
    if max(o) == N: return f"C{N}", ("поворотная" if N > 2 else "зеркальная")
    if max(o) == 2: k = N.bit_length() - 1; return ("V4" if k == 2 else f"(Z/2)^{k}"), "зеркальная"
    if sorted(o) == [1, 2, 2, 2, 4, 4, 4, 4]: return "C2×C4", "смешанная"
    return "?", "?"
def pairs(s):
    return ";".join("{%d,%d}" % (a, inv(a, s)) for a in units(s) if a < inv(a, s)) or "нет"

bad = []
for r in rows:
    n, s = int(r[col["длина"]]), int(r[col["шаг"]]); m = (n - 1) // 2
    exp = {
        "шаг": str(n - 1),
        "узлы": ";".join(str(-1 + k * s) for k in range(5)),
        "середины": ";".join(str(m - 1 + k * s) for k in range(5)),
        "группа": group(s)[0], "тип": group(s)[1],
    }
    if r[col["неразличимые_пары"]] != "—": exp["неразличимые_пары"] = pairs(s)
    for k, v in exp.items():
        if r[col[k]] != v: bad.append((n, k, r[col[k]], v))
    for c in r[col["проверка"]].split(";"):
        if c != "—" and f'"{c.replace("-", "")}"' not in src: bad.append((n, "проверка", c, "нет в verification_*.py"))
ok = not bad and [int(r[0]) for r in rows] == list(range(3, 27, 2)) and all(len(r) == len(head) for r in rows)
for b in bad: print("расхождение:", *b)
print("PASS" if ok else "FAIL", f"таблица окон: {len(rows)} строк, {len(head)} столбцов, вычислимые столбцы совпадают со счётом")
