#!/usr/bin/env python3
"""Точные кандидатные проверки типизированного отсутствия и проекта Lift."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Hashable, Iterable


F = Fraction
REPORT_PATH = Path(__file__).with_name("ABSENCE_LIFT_REPORT.md")


@dataclass(frozen=True)
class ProvenanceStep:
    source: str
    operation: str
    target: str


@dataclass(frozen=True)
class AbsenceRecord:
    expected_type: str
    locus: str
    mechanism: str
    provenance: tuple[ProvenanceStep, ...]
    witness: str


def event_projection(record: AbsenceRecord) -> tuple[str, str, str]:
    """Каноническая булева тень: тип и локус сохранены, структура стёрта."""

    return (record.expected_type, record.locus, "absent")


def provenance_continuous(
    steps: tuple[ProvenanceStep, ...], origin: str, locus: str
) -> bool:
    current = origin
    for step in steps:
        if step.source != current:
            return False
        current = step.target
    return current == locus


def sever(
    steps: tuple[ProvenanceStep, ...], operation: str
) -> tuple[ProvenanceStep, ...]:
    return tuple(step for step in steps if step.operation != operation)


def minimum_zero_one_risk(
    observations: tuple[Hashable, ...],
    correct_actions: tuple[str, ...],
) -> Fraction:
    if len(observations) != len(correct_actions) or not observations:
        raise ValueError("наблюдения и правильные действия должны быть согласованы")
    unique_observations = tuple(dict.fromkeys(observations))
    actions = tuple(dict.fromkeys(correct_actions))
    best = F(1)
    for choices in product(actions, repeat=len(unique_observations)):
        policy = dict(zip(unique_observations, choices, strict=True))
        errors = sum(
            policy[observation] != correct
            for observation, correct in zip(
                observations, correct_actions, strict=True
            )
        )
        best = min(best, F(errors, len(observations)))
    return best


def lifted_product(
    old_layer: tuple[str, ...], residual: tuple[str, ...]
) -> tuple[tuple[str, str], ...]:
    return tuple((old, remainder) for old in old_layer for remainder in residual)


def projection(pair: tuple[str, str]) -> str:
    return pair[0]


def residual_readout(pair: tuple[str, str]) -> str:
    return pair[1]


def factors_through_projection(
    old_layer: tuple[str, ...], residual: tuple[str, ...]
) -> bool:
    lifted = lifted_product(old_layer, residual)
    if not residual:
        return True
    for choices in product(residual, repeat=len(old_layer)):
        candidate = dict(zip(old_layer, choices, strict=True))
        if all(
            residual_readout(pair) == candidate[projection(pair)]
            for pair in lifted
        ):
            return True
    return False


def has_projection_section(
    old_layer: tuple[str, ...], residual: tuple[str, ...]
) -> bool:
    lifted = lifted_product(old_layer, residual)
    if not old_layer:
        return True
    if not lifted:
        return False
    fibers = {
        old: tuple(pair for pair in lifted if projection(pair) == old)
        for old in old_layer
    }
    return all(fibers[old] for old in old_layer)


Check = tuple[str, str, bool, str]


def run_checks() -> list[Check]:
    checks: list[Check] = []

    def add(check_id: str, title: str, passed: bool, detail: str) -> None:
        checks.append((check_id, title, passed, detail))

    chain = (
        ProvenanceStep("sensor", "capture", "ingest"),
        ProvenanceStep("ingest", "filter", "model_input"),
    )
    not_produced = AbsenceRecord(
        "temperature",
        "model_input",
        "not_produced",
        (
            ProvenanceStep("sensor", "no_capture", "ingest"),
            ProvenanceStep("ingest", "forward_absence", "model_input"),
        ),
        "log:no_capture",
    )
    filtered = AbsenceRecord(
        "temperature",
        "model_input",
        "filtered",
        chain,
        "log:filter_rule_7",
    )

    add(
        "TA-01",
        "Одна булева тень допускает разные механизмы и provenance",
        event_projection(not_produced) == event_projection(filtered)
        and not_produced != filtered,
        "Две различные записи отображаются в одно событие absent(A@ℓ).",
    )

    records = (not_produced, filtered)
    add(
        "TA-02",
        "Проекция event/Tot необратима на выбранном волокне",
        len(set(records)) == 2
        and len({event_projection(record) for record in records}) == 1,
        "Мощность волокна 2, мощность булевого образа 1; декодера нет.",
    )

    severed = sever(chain, "capture")
    add(
        "TA-03",
        "Sever разрывает непрерывность provenance",
        provenance_continuous(chain, "sensor", "model_input")
        and not provenance_continuous(severed, "sensor", "model_input"),
        "До удаления путь sensor→model_input непрерывен, после удаления ребра — нет.",
    )

    mechanisms = ("not_produced", "withheld")
    actions = ("recreate", "request_access")
    boolean_risk = minimum_zero_one_risk(("absent", "absent"), actions)
    typed_risk = minimum_zero_one_risk(mechanisms, actions)
    add(
        "TA-04",
        "Проверенный механизм может дать операциональный выигрыш",
        boolean_risk == F(1, 2) and typed_risk == 0,
        f"Риск булевой тени={boolean_risk}; риск типизированного механизма={typed_risk}.",
    )

    unknown_risk = minimum_zero_one_risk(("unknown", "unknown"), actions)
    add(
        "TA-05",
        "Неинформативная метка не подтверждает AbsDataGain",
        unknown_risk == boolean_risk == F(1, 2),
        f"Постоянный unknown сохраняет риск {unknown_risk}; прироста нет.",
    )

    old_layer = ("x0", "x1")
    residual = ("r0", "r1")
    basepoint = "r0"
    embedded = tuple((old, basepoint) for old in old_layer)
    add(
        "LT-01",
        "Set-кандидат сохраняет старый слой",
        tuple(projection(pair) for pair in embedded) == old_layer,
        "Для ι(x)=(x,r₀) точно выполнено π∘ι=id_X.",
    )

    add(
        "LT-02",
        "Остаточное чтение не факторизуется через старый слой",
        not factors_through_projection(old_layer, residual),
        "ρ различает r₀ и r₁ в одном π-волокне.",
    )

    singleton_residual = ("r0",)
    add(
        "LT-03",
        "Одноточечный остаток не даёт definability gain",
        factors_through_projection(old_layer, singleton_residual),
        "При |R|=1 residual readout факторизуется через π.",
    )

    add(
        "LT-04",
        "Пустой остаток блокирует требуемую секцию",
        not has_projection_section(old_layer, ()),
        "При непустом X и R=∅ объект X×R пуст, поэтому ι:X→X×R не существует.",
    )

    wfs_passport = {
        "sample_square_has_filler": True,
        "category_laws_defined": False,
        "factorization_for_every_morphism": False,
        "fillers_for_every_required_square": False,
        "substitution_stability": False,
    }
    required_wfs_fields: Iterable[str] = (
        "category_laws_defined",
        "factorization_for_every_morphism",
        "fillers_for_every_required_square",
        "substitution_stability",
    )
    add(
        "LT-05",
        "Один заполнитель не устанавливает WFS",
        wfs_passport["sample_square_has_filler"]
        and not all(wfs_passport[field] for field in required_wfs_fields),
        "Локальный filler есть, но глобальные категориальные обязательства не закрыты.",
    )

    return checks


def render_report(checks: list[Check]) -> str:
    passed = sum(result for _, _, result, _ in checks)
    failed = len(checks) - passed
    output = []
    for check_id, title, result, detail in checks:
        status = "PASS" if result else "FAIL"
        output.append(f"{status} {check_id} — {title}: {detail}")
    output.append(f"Итог: {passed} PASS / {failed} FAIL из {len(checks)}")

    return (
        "# Отчёт проверок типизированного отсутствия и проекта Lift\n\n"
        "- Статус проверок: `candidate_probe`, не C-NN.\n"
        "- Арифметика риска: точные рациональные числа `Fraction`.\n"
        "- Область: конечные записи, множества и паспортные условия.\n"
        "- Влияние на `St_FTS`: отсутствует.\n\n"
        "Команда:\n\n"
        "```powershell\n"
        "python -X utf8 "
        "work/v14_rebuild/e5_literature_review/"
        "check_absence_lift_projects.py --write-report\n"
        "```\n\n"
        "Результат:\n\n"
        "```text\n"
        + "\n".join(output)
        + "\n```\n\n"
        "TA-01…TA-05 подтверждают необратимость булевой проекции, локальный "
        "эффект provenance и ограниченный пример выигрыша. LT-01…LT-05 "
        "подтверждают только конечную Set-модель и выявленные предпосылки. "
        "Проверки не канонизируют запись `0_A`, не доказывают общий Lift и "
        "не устанавливают WFS.\n"
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
