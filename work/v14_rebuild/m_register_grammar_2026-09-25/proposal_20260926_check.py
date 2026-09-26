"""Check the revised author trees and explicit interpretations of equality.

Evidence applies to syntax and declared readouts only, not FTS canon status.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from syntax_check import ROOT, parse, swap_root, atoms, leaf_count, boolean_shadow
from cycle_readout import outcomes

HERE = Path(__file__).resolve().parent


def count_subtree(tree, target):
    return int(tree == target) + (0 if isinstance(tree, str) else sum(count_subtree(c, target) for c in tree[1:]))


def label(tree):
    if isinstance(tree, str):
        return tree
    return f"({label(tree[1])} {tree[0]} {label(tree[2])})"


def same_root_components(first, second):
    """Candidate equality of ordered child pairs, ignoring only the root mode.

    Domain: binary composition trees. Inner operations are kept verbatim.
    This is a comparison rule proposed by the assistant, not canonical Eq_7.
    """
    if isinstance(first, str) or isinstance(second, str):
        raise ValueError("The relation is defined here only on binary compositions")
    return first[1:] == second[1:]


def main():
    source = HERE / "PROPOSAL_2026-09-26.md"
    forms = {line.split(" := ", 1)[0]: line.split(" := ", 1)[1]
             for line in source.read_text(encoding="utf-8").splitlines()
             if line.startswith(("T5 := ", "T6 := ", "T7 := "))}
    t5, t6, t7 = (parse(forms[k]) for k in ("T5", "T6", "T7"))
    b, d = parse("(a=b) ∧ (a≠b)"), parse("(a=b) ∨ (a≠b)")
    x, y = ("∨", d, b), ("∧", d, b)
    canonical7 = next(parse(c["symbol"]) for c in (
        json.loads(line) for line in (ROOT / "source/fts_cards.jsonl").read_text(encoding="utf-8").splitlines()
    ) if c["id"] == "M_07")
    compact7 = ("∨", b, d)
    boolean_rows = []
    for p, q in ((False, False), (False, True), (True, False), (True, True)):
        left, right = (boolean_shadow(t, p, q) for t in t7[1:])
        boolean_rows.append({"p": p, "q": q,
                             "T7_outer_OR": boolean_shadow(t7, p, q),
                             "outer_OR_replaced_by_equality_of_boolean_results": left == right,
                             "left_result": left, "right_result": right})
    result = {
        "scope": "literal ordered syntax and separately declared observation criteria; ordinary Boolean equality is only a counterfactual control",
        "author_formula_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "syntax": {
            "T5_is_D_AND_B": t5 == y,
            "T6_is_flip_T5_AND_T5": t6 == ("∧", swap_root(t5), t5),
            "T7_is_T6_OR_flip_T6": t7 == ("∨", t6, swap_root(t6)),
            "previous_duplicate_copy_defect_is_absent": t7[1] != t7[2],
            "T7_has_pattern_X_AND_Y_OR_X_OR_Y": t7 == ("∨", ("∧", x, y), ("∨", x, y)),
            "T7_left_is_T6": t7[1] == t6,
            "T6_right_is_T5": t6[2] == t5,
            "T5_right_is_M4_B": t5[2] == b,
            "B_occurrences_in_T5_T6_T7": [count_subtree(t, b) for t in (t5, t6, t7)],
            "atomic_occurrences_in_T5_T6_T7": [leaf_count(t) for t in (t5, t6, t7)],
            "new_T7_is_active_M07_tree": t7 == canonical7,
        },
        "literal_equality_of_T7_left_and_right": t7[1] == t7[2],
        "candidate_special_equality_of_root_components": {
            "T7_branches_equal_by_this_rule": same_root_components(*t7[1:]),
            "same_test_on_branches_of_T5_and_T6": [same_root_components(*t[1:]) for t in (t5, t6)],
            "changing_one_component_is_detected": not same_root_components(t6, ("∧", x, b)),
            "reordering_different_components_is_detected": not same_root_components(t6, ("∧", y, x)),
            "substitution_in_arbitrary_lower_context_is_not_preserved": not same_root_components(("∧", t7[1], b), ("∧", t7[2], b)),
            "interpretation": "same ordered composition basis, different root mode; this does not imply the same action or establish first availability at U7",
        },
        "equality_under_atom_inventory_only": {
            "all_B_D_T5_T6_T7_are_equal_by_this_observation": all(atoms(t) == atoms(b) for t in (b, d, t5, t6, t7)),
            "limitation": "this coarse reading also erases the AND/OR distinction already between B and D; it does not establish a U7-specific ability",
        },
        "previous_Out_reading": {
            "T7_outcomes": sorted(label(t) for t in outcomes(t7)),
            "T7_outcome_count": len(outcomes(t7)),
            "short_B_OR_D_outcome_count": len(outcomes(compact7)),
            "same_outcome_sets": outcomes(t7) == outcomes(compact7),
            "limitation": "candidate Out retains entire AND subtrees; it is not accepted FTS semantics",
        },
        "ordinary_boolean_equality_counterfactual_only_not_authors_special_equality": boolean_rows,
        "status_effect": "none; no probability operation, equivalence relation on FTS carriers, or level assignment is established",
    }
    (HERE / "PROPOSAL_20260926_RESULTS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
