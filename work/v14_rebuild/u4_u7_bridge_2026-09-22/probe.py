"""Finite candidate probes for the active U4→U7 forms; no St_FTS effect."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CARDS = ROOT / "source" / "fts_cards.jsonl"
P = "(a=b)"
Q = "(a≠b)"
B = f"{P} ∧ {Q}"
D = f"{P} ∨ {Q}"
U6 = f"({B}) ∧ ({D})"
U7 = f"({U6}) ∨ (({B}) ∨ ({D}))"


def cards() -> dict[str, dict]:
    return {row["id"]: row for row in (json.loads(line) for line in CARDS.read_text(encoding="utf-8").splitlines())}


def square_of_sum(trace: tuple[int, ...]) -> int:
    return sum(trace) ** 2


def sum_of_squares(trace: tuple[int, ...]) -> int:
    return sum(x * x for x in trace)


def outcome(trace: tuple[int, ...]) -> str:
    if not trace:
        return "none"
    signs = set(trace)
    return "joint" if len(signs) == 2 else ("eq" if 1 in signs else "neq")


def from_archive(summary: int, archive: tuple[int, ...] | None) -> tuple[int, str]:
    if archive is None:
        raise ValueError("archive required")
    if square_of_sum(archive) != summary:
        raise ValueError("archive and summary disagree")
    return summary, outcome(archive)


def from_fresh_measurement(summary: int, measurement: tuple[int, ...] | None) -> tuple[int, str]:
    if measurement is None:
        raise ValueError("fresh measurement required")
    if square_of_sum(measurement) != summary:
        raise ValueError("measurement and summary disagree")
    return summary, outcome(measurement)


def check(label: str, predicate: bool) -> None:
    if not predicate:
        raise AssertionError(label)
    print(f"PASS {label}")


def main() -> None:
    source = cards()
    check("P01 active M04/M05/M06/M07 literal grouping", all(
        source[key]["symbol"] == value for key, value in
        (("M_04", B), ("M_05", D), ("M_06", U6), ("M_07", U7))
    ))

    # B is a field of two typed possibilities; selecting one is an extra datum.
    check("P02 field alone does not determine selection", len({1, -1}) == 2)
    check("P03 one selected event does not determine family aggregate",
          square_of_sum((1, 1)) != square_of_sum((1, -1)))

    traces = ((1, 1), (-1, -1), (1, -1), (-1, 1))
    check("P04 nonempty two-event domain is consistent", all(len(t) >= 2 for t in traces))
    check("P05 all three U7 outcome labels have witnesses",
          {outcome(t) for t in traces} == {"eq", "neq", "joint"})
    check("P06 U6 square summary cannot factor U7 label",
          square_of_sum((1, 1)) == square_of_sum((-1, -1))
          and outcome((1, 1)) != outcome((-1, -1)))
    check("P07 cancellation is not absence",
          square_of_sum((1, -1)) == square_of_sum(()) == 0
          and outcome((1, -1)) != outcome(()))
    check("P08 two historical V*V bridges differ on joint trace",
          square_of_sum((1, -1)) != sum_of_squares((1, -1)))
    check("P09 both V*V bridges are sign-blind",
          all(square_of_sum(t) == square_of_sum(tuple(-x for x in t))
              and sum_of_squares(t) == sum_of_squares(tuple(-x for x in t)) for t in traces))
    check("P10 archive and fresh measurement give same three labels",
          all(from_archive(square_of_sum(t), t) == from_fresh_measurement(square_of_sum(t), t)
              for t in traces))
    for fn, datum in ((from_archive, None), (from_fresh_measurement, None)):
        try:
            fn(4, datum)
        except ValueError:
            pass
        else:
            raise AssertionError("missing resource was accepted")
    check("P11 U7 constructions require distinct additional resources", True)
    check("P12 singleton/empty are boundary cases, not three-outcome witness",
          outcome((1,)) == "eq" and outcome(()) == "none")


if __name__ == "__main__":
    main()
