"""Candidate outcome projection and guided syntax reading; not FTS semantics."""
from __future__ import annotations

import json
from pathlib import Path

from syntax_check import ROOT, parse, leaf_count, boolean_shadow, swap_root

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


def and_reading_witness():
    """Separate candidate reading rule for the user's later AND-fold example."""
    d = swap_root(B)
    long_form = ("∧", B, d)
    second_unfolding = ("∧", long_form, d)

    def fold_fixed_d_family(tree):
        steps = 0
        while tree != B:
            if isinstance(tree, str) or tree[0] != "∧" or tree[2] != d:
                raise ValueError("Outside the explicitly generated fixed-D family")
            tree = tree[1]
            steps += 1
        return tree, steps

    paired = [B, d]
    for _ in range(2):
        x, y = paired[-2:]
        paired.extend((("∧", x, y), ("∨", x, y)))
    valuations = [
        {"p": p, "q": q,
         "paired_U4_to_U9_boolean_shadow": [int(boolean_shadow(t, p, q)) for t in paired],
         "long_AND_and_short_B_agree": boolean_shadow(long_form, p, q) == boolean_shadow(B, p, q)}
        for p, q in ((False, False), (False, True), (True, False), (True, True))
    ]
    return {
        "scope": "new stipulated syntax reading: unfold base B as B AND swap_root(B); repeated right-D wrappers form a separate illustrative family",
        "one_step_reconstructed_from_B_and_rule": long_form == ("∧", B, swap_root(B)),
        "one_step_compresses_to_B": fold_fixed_d_family(long_form) == (B, 1),
        "different_depths_have_same_short_reading": long_form != second_unfolding and fold_fixed_d_family(long_form)[0] == fold_fixed_d_family(second_unfolding)[0] == B,
        "depths_require_distinct_trace_if_exact_history_is_requested": [fold_fixed_d_family(t)[1] for t in (long_form, second_unfolding)],
        "previous_Out_does_not_preserve_this_AND_fold": outcomes(long_form) != outcomes(B),
        "boolean_shadow_valuations": valuations,
        "status_effect": "no FTS equality, speed measurement or proof of speed-fundamentality discrimination",
    }


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
        "scope": "assistant-proposed Out projection keeps AND trees and unions OR outcomes; later_AND_fold_example uses a separate stated reading rule",
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
        "later_AND_fold_example": and_reading_witness(),
        "status_effect": "none; no FTS level assignment or correspondence with Close is established",
    }
    (HERE / "CYCLE_RESULTS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in result.items() if k != "finite_samples"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
