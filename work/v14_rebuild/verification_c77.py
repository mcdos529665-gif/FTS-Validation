"""verification_c77.py — проверки C-77…C-84: минимальные окна, номера уровней, модуль 12.

См. addendum_2026-10-04_windows_numbers.md. Минимальные окна — авторская фиксация;
всё про модуль 12 и чётность форм — кандидат/наблюдение (К2, К4, К5 не проводились).
Чистый Python, без внешних библиотек. Запуск: python verification_c77.py
"""
import io
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TRIPLES = os.path.join(ROOT, "source", "fts_triples.tsv")

results = []


def check(cid, desc, cond, note=""):
    results.append((cid, desc, bool(cond)))
    print(("PASS" if cond else "FAIL"), cid, desc, ("| " + note) if note else "")


def num(u):
    s = u.replace("U_", "")
    return -1 if s == "m1" else int(s)


triples = []
with io.open(TRIPLES, encoding="utf-8") as fh:
    for line in fh:
        p = line.rstrip("\n").split("\t")
        if len(p) == 3:
            triples.append(tuple(p))

# Авторская фиксация 2026-10-04
MIN_WINDOWS = [(-1, 0, 1), (1, 2, 3), (3, 4, 5), (5, 6, 7), (7, 8, 9), (9, 10, 11)]
COUPLING = [-1, 1, 3, 5, 7, 9, 11]

# C-77: форма минимальных окон и перекрытия
ok = all(w == (2 * k - 1, 2 * k, 2 * k + 1) for k, w in enumerate(MIN_WINDOWS))
ok &= all(set(MIN_WINDOWS[i]) & set(MIN_WINDOWS[i + 1]) == {MIN_WINDOWS[i][2]}
          for i in range(len(MIN_WINDOWS) - 1))
ok &= sorted({w[0] for w in MIN_WINDOWS} | {w[2] for w in MIN_WINDOWS}) == COUPLING
check("C77", "Минимальные окна = (2k−1,2k,2k+1), k=0..5; соседние перекрываются ровно в одном "
      "нечётном уровне; точки сцепки −1,1,3,5,7,9,11", ok)

# C-78: обе системы окон начинаются с −1 и являются разными вариантами (шаг 2 и шаг 4)
canon_w = sorted({tuple(int(t) for t in o.strip("()").split(","))
                  for s, r, o in triples if r == "has_window" and "..." not in o})
ok = MIN_WINDOWS[0][0] == -1 and canon_w[0][0] == -1
ok &= all(MIN_WINDOWS[i + 1][0] - MIN_WINDOWS[i][0] == 2 for i in range(len(MIN_WINDOWS) - 1))
ok &= all(canon_w[i + 1][0] - canon_w[i][0] == 4 for i in range(len(canon_w) - 1))
ok &= all(len(w) == 5 for w in canon_w) and all(len(w) == 3 for w in MIN_WINDOWS)
check("C78", "Обе системы окон начинаются с −1: минимальные (шаг 2, по 3 уровня) и канонические "
      "(has_window, шаг 4, по 5 уровней) — разные варианты, не части друг друга",
      ok, "; ".join(map(str, canon_w)))

# C-79: концы минимального окна связаны каноническим projects_to (+2); выше 7 рёбер нет
proj = {(num(s), num(o)) for s, r, o in triples if r == "projects_to"}
have = [w for w in MIN_WINDOWS if (w[2], w[0]) in proj]
miss = [w for w in MIN_WINDOWS if (w[2], w[0]) not in proj]
check("C79", "Концы минимальных окон (−1,0,1)…(5,6,7) связаны рёбрами projects_to (2k+1→2k−1) [C-33]; "
      "для (7,8,9), (9,10,11) рёбер в каноне нет (проекция 8+ открыта, §13)",
      have == MIN_WINDOWS[:4] and miss == MIN_WINDOWS[4:])

# C-80: точки сцепки чередуют узлы канона (≡3 mod 4) и позицию «выбор» П1 (≡1 mod 4)
nodes = {3, 7, 11, 15}
ok = all((x % 4 == 3) == (x in nodes or x == -1) for x in COUPLING)
ok &= [x for x in COUPLING if x % 4 == 1] == [1, 5, 9]
check("C80", "Точки сцепки: ≡3 (mod 4) — граница/узел окна (−1,3,7,11), ≡1 (mod 4) — середина окна, "
      "позиция «выбор» П1 (1,5,9)", ok)

# C-81: модуль 12 — группа Клейна и выпадение 3, 9
n = 12
U = [x for x in range(n) if math.gcd(x, n) == 1]
fib = {}
for x in range(n):
    fib.setdefault(x * x % n, []).append(x)
ok = U == [1, 5, 7, 11] and all(x * x % n == 1 for x in U)
ok &= sorted({x % n for x in COUPLING} - set(U)) == [3, 9]
ok &= (3 * 3 % n, 9 * 9 % n, 3 * 9 % n) == (9, 9, 3)
ok &= sorted({3 * u % n for u in U}) == [3, 9]
ok &= fib == {0: [0, 6], 1: [1, 5, 7, 11], 4: [2, 4, 8, 10], 9: [3, 9]}
ok &= (3 % 3, 9 % 3, 3 % 4, 9 % 4) == (0, 0, 3, 1)
ok &= all(pow(x, 3, n) == x for x in range(1, n, 2))
check("C81", "mod 12: единицы {1,5,7,11} ≅ V4 (все в квадрате 1); из точек сцепки вне V4 только 3, 9; "
      "3²≡9²≡9, 3·9≡3; 3,9 ≡ 0 mod 3, остаётся бит mod 4 (3≡−1, 9≡+1); слои квадрата {0,6},{1,5,7,11},"
      "{2,4,8,10},{3,9}; для нечётных x³≡x", ok)

# C-82: 12 — наибольший модуль, где квадрат — проекция (x⁴≡x² для всех x), и единственный такой с V4
N = 2000
projm = [m for m in range(2, N + 1) if all((pow(x, 4, m) - pow(x, 2, m)) % m == 0 for x in range(m))]


def v4(m):
    u = [x for x in range(1, m) if math.gcd(x, m) == 1]
    return len(u) == 4 and all(x * x % m == 1 for x in u)


g = 0
for x in range(2, 60):
    g = math.gcd(g, x * x * (x * x - 1))
ok = projm == [2, 3, 4, 6, 12] and [m for m in projm if v4(m)] == [12] and g == 12
ok &= [m for m in range(2, N + 1) if v4(m)] == [8, 12] and (2 * 2 % 8, 4 * 4 % 8) == (4, 0)
check("C82", "n≤2000 с x⁴≡x² для всех x: ровно делители 12 (gcd x²(x²−1) = 12); V4-единицы среди них только у 12; "
      "V4-единицы вообще у 8 и 12, но у 8 квадрат не проекция (2→4→0)", ok)


# C-83: наблюдение — на нечётных уровнях 3..11 форма нечётна ⟺ номер ≡ 0 (mod 3)
FORMS = {3: lambda x: -x, 5: lambda x: -abs(x), 7: lambda x: -x * x, 9: lambda x: x ** 3,
         11: math.exp, 2: lambda x: x, 4: abs, 6: lambda x: x * x, 8: lambda x: abs(x) ** 0.5,
         10: math.cos}
PTS = [0.5, 1.0, 1.7, 2.3]


def is_odd(f):
    return all(abs(f(-x) + f(x)) < 1e-12 for x in PTS)


odd_lv = [k for k in (3, 5, 7, 9, 11) if is_odd(FORMS[k])]
even_lv = [k for k in (2, 4, 6, 8, 10) if is_odd(FORMS[k])]
check("C83", "Наблюдение: среди нечётных уровней 3..11 нечётная форма ровно у 3 (−x) и 9 (x³), т.е. у ≡0 mod 3; "
      "на чётных уровнях правило не работает (У2 y=x нечётна, У6 x² чётна при 6≡0 mod 3)",
      odd_lv == [3, 9] and even_lv == [2])

# C-84: умножение номеров ≠ умножение форм: (форма У3)² = форма У6, а 3² = 9
check("C84", "Оговорка: (−x)² = x² — форма У6, хотя 3²=9; (−x)³ = −x³ — анти-форма У9",
      all((-x) ** 2 == x * x and (-x) ** 3 == -(x ** 3) for x in PTS))

n_pass = sum(r[2] for r in results)
print(f"\nИТОГ: {n_pass} PASS / {len(results) - n_pass} FAIL")

if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(results) else 1)
