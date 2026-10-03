#!/usr/bin/env python3
"""Детерминированные конечные пробы пакета явных дополнений 2026-09-05."""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from math import isclose, log2, sqrt
from pathlib import Path
from typing import Hashable, Iterable


REPORT_PATH = Path(__file__).with_name("EXPLICIT_ADDITIONS_REPORT.md")
Check = tuple[str, str, bool, str]
Partition = tuple[frozenset[str], ...]


def factor_table(
    target: dict[str, Hashable], through: dict[str, Hashable]
) -> dict[Hashable, Hashable] | None:
    """Возвращает u, когда target=u∘through; иначе None."""
    table: dict[Hashable, Hashable] = {}
    for omega, through_value in through.items():
        target_value = target[omega]
        previous = table.get(through_value)
        if previous is not None and previous != target_value:
            return None
        table[through_value] = target_value
    return table


def all_partitions(items: tuple[str, ...]) -> Iterable[Partition]:
    """Все разбиения малого конечного множества без дубликатов."""
    if not items:
        yield ()
        return
    first, *tail = items
    for partition in all_partitions(tuple(tail)):
        yield (frozenset({first}), *partition)
        for index, block in enumerate(partition):
            yield (
                *partition[:index],
                frozenset(set(block) | {first}),
                *partition[index + 1 :],
            )


def refines(fine: Partition, coarse: Partition) -> bool:
    return all(any(block <= outer for outer in coarse) for block in fine)


def strict_refines(fine: Partition, coarse: Partition) -> bool:
    return fine != coarse and refines(fine, coarse)


def partition_map(partition: Partition) -> dict[str, int]:
    return {
        item: index
        for index, block in enumerate(partition)
        for item in block
    }


def entropy(probabilities: Iterable[float]) -> float:
    return -sum(
        probability * log2(probability)
        for probability in probabilities
        if probability > 0.0
    )


def conditional_entropy(
    distribution: dict[tuple[Hashable, ...], Fraction],
    target_index: int,
    condition_indices: tuple[int, ...],
) -> float:
    grouped: dict[tuple[Hashable, ...], dict[Hashable, Fraction]] = defaultdict(
        lambda: defaultdict(Fraction)
    )
    totals: dict[tuple[Hashable, ...], Fraction] = defaultdict(Fraction)
    for outcome, probability in distribution.items():
        condition = tuple(outcome[index] for index in condition_indices)
        grouped[condition][outcome[target_index]] += probability
        totals[condition] += probability

    result = 0.0
    for condition, outcomes in grouped.items():
        total = totals[condition]
        result += float(total) * entropy(
            float(probability / total) for probability in outcomes.values()
        )
    return result


def run_checks() -> list[Check]:
    checks: list[Check] = []

    def add(check_id: str, title: str, passed: bool, detail: str) -> None:
        checks.append((check_id, title, passed, detail))

    omega = ("a", "b", "c", "d")
    q = {"a": "x", "b": "x", "c": "y", "d": "y"}
    r = {"a": 0, "b": 0, "c": 1, "d": 0}
    q_plus = {item: (q[item], r[item]) for item in omega}

    all_refinements_preserve_pair = True
    minimum_counts_hold = True
    for partition in all_partitions(omega):
        t = partition_map(partition)
        if factor_table(q, t) is not None and factor_table(r, t) is not None:
            all_refinements_preserve_pair &= factor_table(q_plus, t) is not None
            minimum_counts_hold &= len(set(t.values())) >= len(set(q_plus.values()))
    add(
        "EA-01",
        "REFINE-MIN: пара (q,r) факторизуется через любой сохраняющий её конкурент",
        all_refinements_preserve_pair and minimum_counts_hold,
        "На всех 15 разбиениях Ω из 4 состояний q⁺ не грубее представления t, "
        "через которое факторизуются и q, и r.",
    )

    q_collision = {"a": "x", "b": "x"}
    r_collision = {"a": 0, "b": 1}
    q_plus_collision = {
        item: (q_collision[item], r_collision[item])
        for item in q_collision
    }
    add(
        "EA-02",
        "QuestionGain-свидетель требует строгого уточнения",
        factor_table(r_collision, q_collision) is None
        and len(set(q_plus_collision.values())) > len(set(q_collision.values())),
        "При одинаковом q и разных r ответ не факторизуется через старую запись; "
        "q⁺ разделяет её коллизию.",
    )

    partition_universe = ("0", "1", "2", "3")
    partitions = tuple(all_partitions(partition_universe))
    dense_ok = True
    pair_count = 0
    for coarse in partitions:
        for fine in partitions:
            if not strict_refines(fine, coarse):
                continue
            pair_count += 1
            intermediate_exists = any(
                strict_refines(middle, coarse) and strict_refines(fine, middle)
                for middle in partitions
            )
            cover = not intermediate_exists
            pieces_per_coarse_block = [
                sum(block <= outer for block in fine)
                for outer in coarse
            ]
            one_binary_split = (
                pieces_per_coarse_block.count(2) == 1
                and all(count in {1, 2} for count in pieces_per_coarse_block)
            )
            dense_ok &= (
                cover
                == (len(fine) == len(coarse) + 1)
                == one_binary_split
            )
    add(
        "EA-03",
        "DENSE-PARTITION: покрытие равно одному двоичному расщеплению блока",
        dense_ok and pair_count > 0,
        f"Проверены все {pair_count} строгих пар разбиений множества из 4 элементов.",
    )

    symmetric_fibers = {radius: {-radius, radius} for radius in range(1, 5)}
    no_equivariant_selector = all(
        all(selected != -selected for selected in fiber)
        for fiber in symmetric_fibers.values()
    )
    add(
        "EA-04",
        "SELECT-SYMMETRY: отражение не имеет неподвижного представителя в ненулевом слое",
        no_equivariant_selector,
        "Для r=1…4 ни один из ±r не равен своему отражению; эквивариантная секция "
        "над неподвижной базовой меткой невозможна.",
    )

    informative_distribution = {
        (0, "a", "m0"): Fraction(1, 4),
        (1, "a", "m1"): Fraction(1, 4),
        (0, "b", "m0"): Fraction(1, 4),
        (1, "b", "m1"): Fraction(1, 4),
    }
    h_theta_given_y = conditional_entropy(informative_distribution, 0, (1,))
    h_theta_given_y_m = conditional_entropy(informative_distribution, 0, (1, 2))
    cmi = h_theta_given_y - h_theta_given_y_m
    redundant_distribution = {
        (0, "a", "m_a"): Fraction(1, 4),
        (1, "a", "m_a"): Fraction(1, 4),
        (0, "b", "m_b"): Fraction(1, 4),
        (1, "b", "m_b"): Fraction(1, 4),
    }
    redundant_gain = conditional_entropy(
        redundant_distribution, 0, (1,)
    ) - conditional_entropy(redundant_distribution, 0, (1, 2))
    add(
        "EA-05",
        "ABS-GAIN: разность оптимального log-risk равна условному информационному выигрышу",
        isclose(cmi, 1.0, abs_tol=1e-12)
        and isclose(redundant_gain, 0.0, abs_tol=1e-12),
        f"Информативный M даёт {cmi:.1f} bit, перекодировка M=f(Y) даёт "
        f"{redundant_gain:.1f} bit.",
    )

    q_old = {"u": "c", "v": "c"}
    residual = {"u": "d0", "v": "d1"}
    lifted = {item: (q_old[item], residual[item]) for item in q_old}
    base_residual = "d0"
    section = lambda old: (old, base_residual)
    projection = lambda pair: pair[0]
    add(
        "EA-06",
        "LIFT-PROJECTION: секция сохраняет старый слой, но не фактический остаток",
        all(projection(lifted[item]) == q_old[item] for item in q_old)
        and projection(section("c")) == "c"
        and lifted["v"] != section(q_old["v"]),
        "π∘q⁺=q и π∘ι=id, но при остатке d1 фактическая запись не равна "
        "выбранной секции с d0.",
    )

    real_samples = (-3.0, -1.5, 0.0, 2.0, 5.0)
    square_guard = all(
        isclose(sqrt(value * value), abs(value), abs_tol=1e-12)
        and isclose(abs(value) ** 2, value * value, abs_tol=1e-12)
        for value in real_samples
    )
    add(
        "EA-07",
        "SQUARE-GUARD: |x| и x² взаимно восстанавливаются на одном вещественном x",
        square_guard,
        "На контрольной сетке выполнены |x|=√(x²) и x²=|x|²; это не создаёт "
        "нового наблюдения.",
    )

    diagonal_contradiction = all(value != 1 - value for value in (0, 1))
    add(
        "EA-08",
        "DIAGONAL-ANTITOTALITY: булево диагональное равенство невозможно",
        diagonal_contradiction,
        "Ни 0, ни 1 не удовлетворяет v=1−v; применимость к ФТС требует отдельного "
        "кодирования и самоприменения.",
    )

    return checks


def render_report(checks: list[Check]) -> str:
    passed = sum(result for _, _, result, _ in checks)
    failed = len(checks) - passed
    lines = [
        "# Отчёт конечных проверок явных дополнений 2026-09-05",
        "",
        "- Статус: candidate_probe для внешнего исследовательского пакета.",
        "- Область: конечные разбиения, конечные вероятностные модели и Set-примеры.",
        "- Влияние на St_FTS: отсутствует; это не C-NN статьи.",
        "",
        "Команда:",
        "",
        "    python -X utf8 work/v14_rebuild/e5_literature_review/check_explicit_additions.py --write-report",
        "",
        "Результат:",
        "",
    ]
    for check_id, title, result, detail in checks:
        status = "PASS" if result else "FAIL"
        lines.append(f"{status} {check_id} — {title}: {detail}")
    lines.extend(
        [
            f"Итог: {passed} PASS / {failed} FAIL из {len(checks)}",
            "",
            "EA-01…EA-08 проверяют точные конечные инстансы REFINE-MIN, "
            "DENSE-PARTITION, SELECT-SYMMETRY, ABS-GAIN, Lift, квадратный "
            "гардрейл и диагональную схему. Они не выбирают семантику уровня, "
            "не доказывают единственность лестницы и не канонизируют её.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="перезаписать детерминированный Markdown-отчёт",
    )
    args = parser.parse_args()
    checks = run_checks()
    for check_id, title, result, detail in checks:
        status = "PASS" if result else "FAIL"
        print(f"{status} {check_id} — {title}: {detail}")
    passed = sum(result for _, _, result, _ in checks)
    failed = len(checks) - passed
    print(f"Итог: {passed} PASS / {failed} FAIL из {len(checks)}")

    if args.write_report:
        REPORT_PATH.write_text(render_report(checks), encoding="utf-8", newline="\n")
        print(f"Отчёт: {REPORT_PATH}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
