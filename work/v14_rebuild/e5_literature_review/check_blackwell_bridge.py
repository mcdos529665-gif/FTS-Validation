#!/usr/bin/env python3
"""Точные кандидатные проверки конечного Blackwell-моста У4–У6."""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
from pathlib import Path


F = Fraction
Matrix = tuple[tuple[Fraction, ...], ...]
Vector = tuple[Fraction, ...]
REPORT_PATH = Path(__file__).with_name("BLACKWELL_BRIDGE_REPORT.md")


def matrix(rows: list[list[int | Fraction]]) -> Matrix:
    result = tuple(tuple(F(value) for value in row) for row in rows)
    if not result or not result[0]:
        raise ValueError("матрица должна быть непустой")
    width = len(result[0])
    if any(len(row) != width for row in result):
        raise ValueError("матрица должна быть прямоугольной")
    return result


def matmul(left: Matrix, right: Matrix) -> Matrix:
    if len(left[0]) != len(right):
        raise ValueError("несогласованные размеры матриц")
    return tuple(
        tuple(
            sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def is_row_stochastic(value: Matrix) -> bool:
    return all(
        all(entry >= 0 for entry in row) and sum(row, F(0)) == 1
        for row in value
    )


def deterministic_rules(observations: int, actions: int) -> tuple[Matrix, ...]:
    rules: list[Matrix] = []
    for selected in product(range(actions), repeat=observations):
        rules.append(
            tuple(
                tuple(F(int(action == chosen)) for action in range(actions))
                for chosen in selected
            )
        )
    return tuple(rules)


def risk_vector(experiment: Matrix, rule: Matrix, loss: Matrix) -> Vector:
    states = len(experiment)
    observations = len(experiment[0])
    if len(rule) != observations:
        raise ValueError("правило не согласовано с пространством наблюдений")
    actions = len(rule[0])
    if len(loss) != states or any(len(row) != actions for row in loss):
        raise ValueError("потери не согласованы с состояниями и действиями")
    return tuple(
        sum(
            (
                experiment[state][observation]
                * rule[observation][action]
                * loss[state][action]
                for observation in range(observations)
                for action in range(actions)
            ),
            F(0),
        )
        for state in range(states)
    )


def bayes_value(experiment: Matrix, loss: Matrix, prior: Vector) -> Fraction:
    if len(experiment) != len(prior):
        raise ValueError("априорное распределение не согласовано с состояниями")
    actions = len(loss[0])
    values = []
    for rule in deterministic_rules(len(experiment[0]), actions):
        risk = risk_vector(experiment, rule, loss)
        values.append(sum((prior[i] * risk[i] for i in range(len(prior))), F(0)))
    # В конечной линейной задаче минимум по рандомизированным правилам
    # достигается в детерминированной крайней точке.
    return min(values)


def equal_row_obstruction(source: Matrix, target: Matrix, first: int, second: int) -> bool:
    """Равные строки source не могут стать разными после правого умножения."""
    return source[first] == source[second] and target[first] != target[second]


def run_checks() -> list[tuple[str, str, bool, str]]:
    checks: list[tuple[str, str, bool, str]] = []

    def add(check_id: str, title: str, passed: bool, detail: str) -> None:
        checks.append((check_id, title, passed, detail))

    perfect = matrix([[1, 0], [0, 1]])
    forget = matrix([[1], [1]])
    constant = matmul(perfect, forget)
    zero_one_loss = matrix([[0, 1], [1, 0]])
    uniform_two: Vector = (F(1, 2), F(1, 2))

    add(
        "BW-01",
        "Типы и стохастичность бинарного огрубления",
        is_row_stochastic(perfect)
        and is_row_stochastic(forget)
        and is_row_stochastic(constant)
        and constant == matrix([[1], [1]]),
        "P, K, Q строко-стохастичны и Q=PK.",
    )

    replication_ok = True
    for low_rule in deterministic_rules(1, 2):
        lifted_rule = matmul(forget, low_rule)
        if risk_vector(perfect, lifted_rule, zero_one_loss) != risk_vector(
            constant, low_rule, zero_one_loss
        ):
            replication_ok = False
    add(
        "BW-02",
        "Репликация процедур после огрубления",
        replication_ok,
        "Проверены детерминированные крайние точки; общий случай следует линейно.",
    )

    perfect_value = bayes_value(perfect, zero_one_loss, uniform_two)
    constant_value = bayes_value(constant, zero_one_loss, uniform_two)
    add(
        "BW-03",
        "Непустой Blackwell-остаток",
        perfect_value == 0 and constant_value == F(1, 2),
        f"V(P)={perfect_value}, V(Q)={constant_value}, разрыв={constant_value-perfect_value}.",
    )

    add(
        "BW-04",
        "Обратное огрубление невозможно",
        equal_row_obstruction(constant, perfect, 0, 1),
        "Равные строки QH не могут совпасть с различными строками P.",
    )

    swap = matrix([[0, 1], [1, 0]])
    renamed = matmul(perfect, swap)
    add(
        "BW-05",
        "Переименование не создаёт прироста",
        matmul(renamed, swap) == perfect
        and bayes_value(renamed, zero_one_loss, uniform_two) == perfect_value,
        "Перестановка обратима: P и PK Blackwell-эквивалентны.",
    )

    first_bit = matrix([[1, 0], [1, 0], [0, 1], [0, 1]])
    second_bit = matrix([[1, 0], [0, 1], [1, 0], [0, 1]])
    first_loss = matrix([[0, 1], [0, 1], [1, 0], [1, 0]])
    second_loss = matrix([[0, 1], [1, 0], [0, 1], [1, 0]])
    uniform_four: Vector = (F(1, 4), F(1, 4), F(1, 4), F(1, 4))
    first_on_first = bayes_value(first_bit, first_loss, uniform_four)
    first_on_second = bayes_value(second_bit, first_loss, uniform_four)
    second_on_first = bayes_value(first_bit, second_loss, uniform_four)
    second_on_second = bayes_value(second_bit, second_loss, uniform_four)
    incomparable = (
        first_on_first == 0
        and first_on_second == F(1, 2)
        and second_on_first == F(1, 2)
        and second_on_second == 0
        and equal_row_obstruction(first_bit, second_bit, 0, 1)
        and equal_row_obstruction(second_bit, first_bit, 0, 2)
    )
    add(
        "BW-06",
        "Одна метрика не задаёт порядок Блэквелла",
        incomparable,
        "Первый и второй бит выигрывают на разных задачах; каналов нет в обе стороны.",
    )

    return checks


def render_report(checks: list[tuple[str, str, bool, str]]) -> str:
    passed = sum(result for _, _, result, _ in checks)
    failed = len(checks) - passed
    output = []
    for check_id, title, result, detail in checks:
        status = "PASS" if result else "FAIL"
        output.append(f"{status} {check_id} — {title}: {detail}")
    output.append(f"Итог: {passed} PASS / {failed} FAIL из {len(checks)}")

    return (
        "# Отчёт проверок Blackwell-моста\n\n"
        "- Статус проверок: `candidate_probe`, не C-NN.\n"
        "- Арифметика: точные рациональные числа `Fraction`.\n"
        "- Область: конечные эксперименты и заявленные примеры.\n"
        "- Влияние на `St_FTS`: отсутствует.\n\n"
        "Команда:\n\n"
        "```powershell\n"
        "python -X utf8 "
        "work/v14_rebuild/e5_literature_review/check_blackwell_bridge.py "
        "--write-report\n"
        "```\n\n"
        "Результат:\n\n"
        "```text\n"
        + "\n".join(output)
        + "\n```\n\n"
        "Проверки подтверждают матричную механику примера и контрпримеров. "
        "Они не доказывают отображение уровней ФТС на эксперименты и не "
        "проверяют канонический `projects_to`.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="перезаписать детерминированный Markdown-отчёт",
    )
    args = parser.parse_args()

    checks = run_checks()
    for check_id, title, passed, detail in checks:
        status = "PASS" if passed else "FAIL"
        print(f"{status} {check_id} — {title}: {detail}")
    passed_count = sum(result for _, _, result, _ in checks)
    failed_count = len(checks) - passed_count
    print(f"Итог: {passed_count} PASS / {failed_count} FAIL из {len(checks)}")

    if args.write_report:
        REPORT_PATH.write_text(render_report(checks), encoding="utf-8", newline="\n")
        print(f"Отчёт: {REPORT_PATH}")
    return 1 if failed_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
