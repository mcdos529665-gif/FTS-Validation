#!/usr/bin/env python3
"""Конечные и символические пробы NC-01…NC-04; не C-NN и не статусный гейт.

Запуск: python -X utf8 work/v14_rebuild/check_new_connections.py [--write]
Ожидаемый контрпример проверяется как контрпример, а не скрытый FAIL теории.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import log2
from pathlib import Path
import platform

import sympy as sp


REPORT = Path(__file__).with_name("NEW_CONNECTIONS_REPORT.md")


def partitions(n: int) -> list[tuple[int, ...]]:
    """Все разбиения через канонические restricted-growth строки."""
    result = [(0,)]
    for _ in range(1, n):
        result = [p + (k,) for p in result for k in range(max(p) + 2)]
    return result


def factorable(through: tuple, target: tuple) -> bool:
    """target=h(through) на всем конечном носителе."""
    return all(
        through[i] != through[j] or target[i] == target[j]
        for i in range(len(through)) for j in range(len(through))
    )


def joint(*representations: tuple) -> tuple:
    return tuple(zip(*representations))


def equivalent(a: tuple, b: tuple) -> bool:
    return factorable(a, b) and factorable(b, a)


def conditional_entropy(target: tuple, observation: tuple) -> float:
    """Равномерная конечная модель; логарифмы по основанию 2."""
    pairs = Counter(zip(observation, target))
    totals = Counter(observation)
    n = len(target)
    return sum(
        float(Fraction(count, n)) * log2(Fraction(totals[obs], count))
        for (obs, _), count in pairs.items()
    )


def order_commutes() -> str:
    ps = partitions(4)
    assert len(ps) == len(set(ps)) == 15
    for q, r, s in product(ps, repeat=3):
        assert equivalent(joint(joint(q, r), s), joint(joint(q, s), r))
    return "15^3=3375 троек разбиений: оба порядка сохраняют одну различимость"


def order_not_unique() -> str:
    ps = partitions(4)
    # Проверка покрытия через отсутствие промежуточного разбиения,
    # независимо от формулы разности числа блоков.
    covers = {
        p: [q for q in ps if p != q and factorable(q, p) and not any(
            r not in (p, q) and factorable(q, r) and factorable(r, p)
            for r in ps
        )]
        for p in ps
    }

    def paths(p: tuple) -> list[tuple]:
        if p == (0, 1, 2, 3):
            return [(p,)]
        return [(p,) + tail for q in covers[p] for tail in paths(q)]

    chains = paths((0, 0, 0, 0))
    assert len(chains) == 18
    assert all([len(set(p)) for p in path] == [1, 2, 3, 4] for path in chains)
    assert ((0, 0, 0, 0), (0, 0, 1, 1), (0, 1, 2, 2), (0, 1, 2, 3)) in chains
    assert ((0, 0, 0, 0), (0, 1, 0, 1), (0, 1, 2, 1), (0, 1, 2, 3)) in chains
    return "18 насыщенных цепей 1→2→3→4 блока; невставляемость не выбирает порядок"


def contextual_redundancy() -> str:
    q, r, s = (0, 0, 0, 0), (0, 0, 1, 1), (1, 1, 0, 0)
    assert not factorable(q, r) and not factorable(q, s)
    assert factorable(joint(q, r), s)
    assert factorable(joint(q, s), r)
    return "r и 1-r по отдельности уточняют q, но второй вопрос уже восстановим"


Q0 = (0, 0, 0, 0)
R = (0, 0, 1, 1)
S = (0, 1, 0, 1)
XOR = tuple(a ^ b for a, b in zip(R, S))


def joint_gain() -> str:
    risks = [conditional_entropy(XOR, obs) for obs in (Q0, R, S, joint(R, S))]
    assert risks == [1.0, 1.0, 1.0, 0.0]
    # Прямой свидетель независимости каждого канала от цели.
    assert all(count == 1 for count in Counter(zip(R, XOR)).values())
    assert all(count == 1 for count in Counter(zip(S, XOR)).values())
    assert not factorable(R, XOR) and not factorable(S, XOR)
    assert factorable(joint(R, S), XOR)
    return "XOR: H(Θ), H(Θ|r), H(Θ|s), H(Θ|r,s) = 1,1,1,0 бит"


def deletion_and_addition() -> str:
    full = conditional_entropy(XOR, joint(R, S))
    assert conditional_entropy(XOR, R) - full == 1.0
    assert conditional_entropy(XOR, S) - full == 1.0
    assert conditional_entropy(XOR, Q0) - conditional_entropy(XOR, R) == 0.0
    assert conditional_entropy(XOR, Q0) - conditional_entropy(XOR, S) == 0.0
    return "удаление любого канала из полной пары стоит 1 бит; добавление к пустому — 0"


def gain_limits() -> str:
    assert conditional_entropy(R, R) == 0.0  # другая цель: первый канал уже достаточен
    # На диагональной поддержке {(0,0),(1,1)} прежняя XOR-цель константна.
    assert conditional_entropy((0, 0), (0, 0)) == 0.0
    assert not factorable(Q0, R) and not factorable(Q0, S)
    return "выигрыш зависит от цели/поддержки; ноль по цели не равен отсутствию уточнения Ω"


x, y, a, b, c, d, u, v = sp.symbols("x y a b c d u v", real=True)
z1, z2, g = a + sp.I*b, c + sp.I*d, u + sp.I*v


def square(z):
    return sp.expand(z * sp.conjugate(z))


def mixed_real() -> str:
    assert sp.expand(square(x+y) - square(x) - square(y) - 2*x*y) == 0
    assert (square(1), square(1)) == (square(1), square(-1)) == (1, 1)
    assert square(1+1) == 4 and square(1-1) == 0
    return "(x+y)^2-x^2-y^2=2xy; (1,1)/(1,-1): покомпонентные Q равны, совместные 4/0"


def complex_relative() -> str:
    cross = z1 * sp.conjugate(z2)
    real_readout = (square(z1+z2) - square(z1) - square(z2))/2
    imag_readout = (square(z1+sp.I*z2) - square(z1) - square(z2))/2
    assert sp.simplify(real_readout - sp.re(cross)) == 0
    assert sp.simplify(imag_readout - sp.im(cross)) == 0
    assert sp.simplify(square(cross) - square(z1)*square(z2)) == 0
    return "две смешанные Q-пробы восстанавливают z1*conj(z2); |cross|²=Q1*Q2"


def symmetry_scope() -> str:
    cross = z1 * sp.conjugate(z2)
    assert sp.expand((g*z1)*sp.conjugate(g*z2) - square(g)*cross) == 0
    assert 1*sp.conjugate(1) == 1
    assert 1*sp.conjugate(sp.I) == -sp.I
    return "при Q(g)=1 общий поворот сохраняет cross; независимый поворот меняет 1 на -i"


def phase_zero_boundary() -> str:
    assert sp.expand((0*z1)*sp.conjugate(z2)) == 0
    assert square(0) == 0
    # Общий фазовый поворот не восстанавливается даже всеми четырьмя считываниями.
    def readouts(p, q):
        return square(p), square(q), square(p+q), square(p+sp.I*q)
    assert readouts(1, sp.I) == readouts(sp.I, -1)
    return "при нулевом компоненте нормировка не определена; общая фаза не восстановлена"


def blind_readout() -> str:
    anti = (x*x - y*y)/2
    assert sp.expand(anti - (x-y)*(x+y)/2) == 0
    assert anti.subs({x: 1, y: -1}) == 0
    assert (x-y).subs({x: 1, y: -1}) == 2
    return "контрпример: f=x², (x,y)=(1,-1), f_anti=0 при x-y=2"


def historical_witness_zero() -> str:
    # Именно функционал действующей SHADOW-3, без подмены старого примера.
    f = x*x*y + 3*x
    anti = (f - f.subs({x:y, y:x}, simultaneous=True))/2
    assert sp.expand(anti - (x-y)*(x*y+3)/2) == 0
    assert anti.subs({x: 1, y: -3}) == 0
    assert (x-y).subs({x: 1, y: -3}) == 4
    return "сама SHADOW-3: (1,-3) даёт нуль множителя xy+3 вне диагонали"


def polynomial_boundary() -> str:
    checked = 0
    for i in range(5):
        for j in range(5-i):
            f = x**i*y**j
            anti = sp.expand((f-f.subs({x:y, y:x}, simultaneous=True))/2)
            h, remainder = sp.div(anti, x-y, x, y)
            assert remainder == 0
            assert sp.expand(h-h.subs({x:y, y:x}, simultaneous=True)) == 0
            checked += 1
    assert checked == 15
    # Отдельно проверяем базовый детектор и дополнительный нуль, не обобщая сетку.
    assert sp.solveset(sp.Eq(x-y, 0), x, domain=sp.S.Reals) == sp.FiniteSet(y)
    return "15 мономов степени ≤4: f_anti=(x-y)h, h симметричен; базовый детектор x-y"


def boolean_boundary() -> str:
    p = sp.Symbol("p")
    assert sp.simplify_logic(sp.And(p, sp.Not(p))) == sp.false
    assert sp.simplify_logic(sp.Or(p, sp.Not(p))) == sp.true
    # Модель двух каналов НЕ ограничена булевым дополнением f=1-t.
    channels = set(product((0, 1), repeat=2))
    boolean_shadow = {(0, 1), (1, 0)}
    assert channels - boolean_shadow == {(0, 0), (1, 1)}
    return "булево p∧¬p=False, p∨¬p=True; независимая пара каналов имеет ещё (0,0)/(1,1)"


def square_boundary() -> str:
    assert sp.simplify(sp.Abs(x)**2-x*x) == 0
    assert sp.simplify(sp.sqrt(x*x)-sp.Abs(x)) == 0
    return "x вещественный: |x|²=x² и sqrt(x²)=|x|; взаимная восстановимость одного чтения"


CHECKS = [
    ("NC-P01", "NC-01: перестановка уточнений", order_commutes),
    ("NC-P02", "NC-01: порядок не вынужден", order_not_unique),
    ("NC-P03", "NC-01: контекстная избыточность", contextual_redundancy),
    ("NC-P04", "NC-02: совместный выигрыш", joint_gain),
    ("NC-P05", "NC-02: RoleNec и одиночное добавление", deletion_and_addition),
    ("NC-P06", "NC-02: цель и поддержка", gain_limits),
    ("NC-P07", "NC-03: порядок Agg/Q", mixed_real),
    ("NC-P08", "NC-03: комплексные смешанные считывания", complex_relative),
    ("NC-P09", "NC-03: общая/независимая симметрия", symmetry_scope),
    ("NC-P10", "NC-03: нуль и общая фаза", phase_zero_boundary),
    ("NC-P11", "NC-04: контрпример общему iff", blind_readout),
    ("NC-P12", "NC-04: контрпример внутри SHADOW-3", historical_witness_zero),
    ("NC-P13", "NC-04: фактор и базовый детектор", polynomial_boundary),
    ("EC-P01", "EC-001: булева область", boolean_boundary),
    ("EC-P02", "EC-002: один вещественный скаляр", square_boundary),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="сохранить отчет рядом со скриптом")
    args = parser.parse_args()
    rows = []
    for check_id, label, fn in CHECKS:
        try:
            evidence = fn()
            status = "PASS"
        except Exception as exc:
            evidence = f"{type(exc).__name__}: {exc}"
            status = "FAIL"
        rows.append((check_id, label, status, evidence))
        print(f"{check_id} {status}: {evidence}")
    passed = sum(row[2] == "PASS" for row in rows)
    failed = len(rows)-passed
    print(f"summary: {passed} PASS / {failed} FAIL; candidate only")
    if args.write:
        text = [
            "# NEW CONNECTIONS — машинные свидетели", "",
            "Дата пакета: 2026-09-09. Связанные формулировки: NEW_CONNECTIONS_2026-09-09.md.",
            "Область: конечные модели Ω из четырёх состояний и указанные тождества над R/C.",
            "PASS у контрпримера подтверждает наличие контрпримера к снятой формулировке.",
            "Это самостоятельные candidate-пробы; C01–C62 и St_FTS не повышаются.", "",
            f"Python {platform.python_version()}, SymPy {sp.__version__}.",
            f"SHA256 check_new_connections.py: `{sha256(Path(__file__).read_bytes()).hexdigest()}`.",
            "Команда: `python -X utf8 work/v14_rebuild/check_new_connections.py --write`.", "",
            "| ID | Предикат | Результат | Свидетель |", "|---|---|---|---|",
        ]
        text.extend("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |" for row in rows)
        text.extend(["", f"**Итого: {passed} PASS / {failed} FAIL.**", ""])
        REPORT.write_text("\n".join(text), encoding="utf-8", newline="\n")
    return int(failed != 0)


if __name__ == "__main__":
    raise SystemExit(main())
