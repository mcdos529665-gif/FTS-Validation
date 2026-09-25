"""Candidate structured-outcome readout; not an implementation of FTS semantics."""
from __future__ import annotations

import json
from pathlib import Path

from syntax_check import ROOT, parse, leaf_count

HERE = Path(__file__).resolve().parent
B = parse("(a=b) ∧ (a≠b)")


def outcomes(tree):
    if isinstance(tree, str) or tree[0] == "∧":
        return frozenset({tree})
    return outcomes(tree[1]) | outcomes(tree[2])


def expand(tree):
    return ("∨", B, tree)


def compress_once(tree):
    if not isinstance(tree, tuple) or tree[:2] != ("∨", B):
        raise ValueError("Expected the explicitly specified B OR wrapper")
    return tree[2]


def main():
    lines = (HERE / "CYCLE_CLARIFICATION.md").read_text(encoding="utf-8").splitlines()
    forms = {line.split(" := ", 1)[0]: line.split(" := ", 1)[1]
             for line in lines if line.startswith(("R := ", "R_expanded := "))}
    short = parse(forms["R"])
    longer = parse(forms["R_expanded"])
    current7 = next(parse(c["symbol"]) for c in (
        json.loads(line) for line in (ROOT / "source/fts_cards.jsonl").read_text(encoding="utf-8").splitlines()
    ) if c["id"] == "M_07")
    expected = frozenset({"a=b", "a≠b", B})
    samples = []
    t = short
    for n in range(9):
        samples.append({"expansions": n, "atomic_occurrences": leaf_count(t),
                        "same_three_outcomes": outcomes(t) == expected,
                        "one_step_roundtrip": compress_once(expand(t)) == t})
        t = expand(t)
    result = {
        "scope": "assistant-proposed outcome projection; AND keeps an entire tree, OR takes set union; original trees retained",
        "given_longer_is_expand_of_shorter": longer == expand(short),
        "trees_differ": longer != short,
        "both_read_as_three_author_outcomes": outcomes(short) == outcomes(longer) == expected,
        "outcome_projection_is_not_injective": short != longer and outcomes(short) == outcomes(longer),
        "roundtrip_also_works_on_B": compress_once(expand(B)) == B,
        "B_expansion_also_preserves_its_outcomes": outcomes(expand(B)) == outcomes(B),
        "arbitrary_formula_need_not_have_three_outcomes": outcomes(expand(B)) != expected,
        "active_M7_differs_from_given_expansion": current7 != longer,
        "active_M7_outcomes_count_under_this_candidate_only": len(outcomes(current7)),
        "finite_samples": samples,
        "status_effect": "none; no FTS level assignment or correspondence with Close is established",
    }
    (HERE / "CYCLE_RESULTS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in result.items() if k != "finite_samples"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
