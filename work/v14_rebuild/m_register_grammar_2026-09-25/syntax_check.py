"""Literal tree comparison of an author proposal; no FTS semantic evaluation.

Run with python -X utf8. Results are evidence about the submitted strings and
explicit syntactic constructions, not new C-NN tests or status promotions.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TOKEN = re.compile(r"a≠a|a=a|a≠b|a=b|[()∧∨]")


def parse(text):
    compact = "".join(text.split())
    tokens = TOKEN.findall(compact)
    if "".join(tokens) != compact:
        raise ValueError(f"Unsupported token: {text}")
    pos = 0

    def factor():
        nonlocal pos
        token = tokens[pos]
        pos += 1
        if token == "(":
            result = expression()
            if pos >= len(tokens) or tokens[pos] != ")":
                raise ValueError(f"Missing closing parenthesis: {text}")
            pos += 1
            return result
        if token not in {"a≠a", "a=a", "a≠b", "a=b"}:
            raise ValueError(f"Expected atom: {text}")
        return token

    def expression():
        nonlocal pos
        left = factor()
        if pos < len(tokens) and tokens[pos] in {"∧", "∨"}:
            op = tokens[pos]
            pos += 1
            return (op, left, factor())
        return left

    result = expression()
    if pos != len(tokens):
        raise ValueError(f"Ambiguous grouping or trailing tokens: {text}")
    return result


def swap_root(tree):
    if isinstance(tree, str):
        raise ValueError("Root connective required")
    return ("∨" if tree[0] == "∧" else "∧", tree[1], tree[2])


def leaf_count(tree):
    return 1 if isinstance(tree, str) else leaf_count(tree[1]) + leaf_count(tree[2])


def atoms(tree):
    return {tree} if isinstance(tree, str) else atoms(tree[1]) | atoms(tree[2])


def boolean_shadow(tree, p, q):
    # Independent Boolean values for the two displayed roles. This is an
    # explicitly limited diagnostic translation, never the semantics of FTS.
    if isinstance(tree, str):
        return {"a=b": p, "a≠b": q}[tree]
    x, y = (boolean_shadow(child, p, q) for child in tree[1:])
    return (x and y) if tree[0] == "∧" else (x or y)


def main():
    raw = (HERE / "AUTHOR_TABLE.md").read_text(encoding="utf-8")
    rows = []
    for line in raw.splitlines():
        if not re.match(r"\| [0-8] \|", line):
            continue
        fields = [x.strip() for x in line.split("|")[1:-1]]
        rows.append(fields)
    simple = {int(n): parse(s) for n, s, _, _ in rows}
    complex_ = {int(n): parse(c) for n, _, _, c in rows if c}
    cards = {
        c["id"]: c
        for c in (
            json.loads(line)
            for line in (ROOT / "source/fts_cards.jsonl").read_text(encoding="utf-8").splitlines()
        )
        if c["id"] in {f"M_{n:02d}" for n in range(9)}
    }
    current6, current7 = (parse(cards[k]["symbol"]) for k in ("M_06", "M_07"))
    simple9 = ("∨", simple[6], simple[7])  # Continuation of the proposed paired rule.
    paired = {k: simple[k] for k in (2, 3)}
    for k in (2, 3, 4):
        previous = paired[2*k - 2], paired[2*k - 1]
        paired[2*k] = ("∧", *previous)
        paired[2*k + 1] = ("∨", *previous)
    comparisons = {
        "simple_0_1_2_4_5_6_match_current_trees": all(
            simple[n] == parse(cards[f"M_{n:02d}"]["symbol"]) for n in (0, 1, 2, 4, 5, 6)
        ),
        "simple_4_to_8_follow_paired_rule": all(simple[n] == paired[n] for n in range(4, 9)),
        "simple7_equals_current7_right_child": simple[7] == current7[2],
        "simple7_equals_current7": simple[7] == current7,
        "simple8_equals_swap_root_current7": simple[8] == swap_root(current7),
        "implied_simple9_equals_current7": simple9 == current7,
        "complex5_equals_simple6_with_only_root_children_swapped": complex_[5] == (simple[6][0], simple[6][2], simple[6][1]),
        "complex6_equals_swap_root_complex5_AND_complex5": complex_[6] == ("∧", swap_root(complex_[5]), complex_[5]),
        "complex7_equals_complex6_OR_identical_complex6": complex_[7] == ("∨", complex_[6], complex_[6]),
        "complex7_has_root_swapped_copy_of_complex6": swap_root(complex_[6]) in complex_[7][1:],
        "bootstrap2_is_literal_simple1_AND_simple0": simple[2] == ("∧", simple[1], simple[0]),
        "bootstrap3_is_literal_simple1_OR_simple0": simple[3] == ("∨", simple[1], simple[0]),
    }
    result = {
        "scope": "ordered binary syntax trees; redundant parentheses ignored; no associativity, commutativity, idempotence, or FTS semantics assumed",
        "source_sha256": hashlib.sha256((HERE / "AUTHOR_TABLE.md").read_bytes()).hexdigest(),
        "canon_sha256": hashlib.sha256((ROOT / "source/fts_cards.jsonl").read_bytes()).hexdigest(),
        "parsed_formulas": len(simple) + len(complex_),
        "comparisons": comparisons,
        "atom_sets": {"bootstrap_inputs": sorted(atoms(simple[0]) | atoms(simple[1])), "M2": sorted(atoms(simple[2])), "M3_proposal": sorted(atoms(simple[3]))},
        "leaf_counts": {"simple": {n: leaf_count(t) for n, t in simple.items()}, "complex": {n: leaf_count(t) for n, t in complex_.items()}, "current_M6": leaf_count(current6), "current_M7": leaf_count(current7)},
        "boolean_shadow_only": [
            {"p": p, "q": q, "simple": {n: boolean_shadow(simple[n], p, q) for n in range(4, 9)}, "complex": {n: boolean_shadow(complex_[n], p, q) for n in range(4, 8)}, "current_M7": boolean_shadow(current7, p, q)}
            for p, q in ((False, False), (False, True), (True, False), (True, True))
        ],
        "status_effect": "none; false comparisons report mismatches, not failures of canonical C-NN claims",
    }
    (HERE / "RESULTS.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"parsed_formulas": result["parsed_formulas"], "comparisons": comparisons}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
