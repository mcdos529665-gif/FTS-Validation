"""Exact finite witnesses for signed window candidates; no FTS status decisions."""
from __future__ import annotations

import argparse
import itertools
import json
from math import gcd
from pathlib import Path

import sympy as sp


def bit(g: int, i: int) -> int:
    return (g >> i) & 1


def parity_sign(n: int) -> int:
    return -1 if n % 2 else 1


def eps_h(g: int, h: int) -> int:
    return parity_sign(bit(g, 0) * bit(h, 0)
                       + bit(g, 1) * bit(h, 1)
                       + bit(g, 1) * bit(h, 0))


def eps_split(g: int, h: int) -> int:
    # I^2=-1, J^2=+1, JI=-IJ; basis (1,I,J,IJ).
    return parity_sign(bit(g, 0) * bit(h, 0)
                       + bit(g, 1) * bit(h, 0))


def eps_comm(g: int, h: int) -> int:
    return parity_sign(sum(bit(g, i) * bit(h, i) for i in range(2)))


def eps_diag(g: int, h: int) -> int:
    return -1 if g == h and g != 0 else 1


def eps_oct(g: int, h: int) -> int:
    # Baez convention: (x,y)(u,v)=(xu-v*y*, x* v+u y).
    # e_(p,0)=(h_p,0), e_(p,1)=(0,h_p), pair means x+ell*y.
    p, q, t, u = g & 3, h & 3, bit(g, 2), bit(h, 2)
    star_p = 1 if p == 0 else -1
    if t == 0 and u == 0:
        return eps_h(p, q)
    if t == 0 and u == 1:
        return star_p * eps_h(p, q)
    if t == 1 and u == 0:
        return eps_h(q, p)
    return -star_p * eps_h(q, p)


MODELS = {
    "T4": (2, lambda g, h: 1),
    "C4": (2, eps_comm),
    "H4": (2, eps_h),
    "S4": (2, eps_split),
    "N4": (2, eps_diag),
    "T8": (3, lambda g, h: 1),
    "B8": (3, lambda g, h: eps_h(g & 3, h & 3)),
    "O8": (3, eps_oct),
}


def mul(eps, a, b):
    s, g = a
    t, h = b
    return s * t * eps(g, h), g ^ h


def associator(eps, g, h, k):
    return eps(g, h) * eps(g ^ h, k) * eps(h, k) * eps(g, h ^ k)


def vector_mul(eps, x, y):
    n = len(x)
    out = [0] * n
    for g, h in itertools.product(range(n), repeat=2):
        out[g ^ h] += eps(g, h) * x[g] * y[h]
    return [sp.expand(v) for v in out]


def coordinates(modulus, roots):
    units = [r for r in range(modulus) if gcd(r, modulus) == 1]
    # Missing-root bits, not raw presence bits: identity has degree zero.
    labels = {r: tuple((1 - int(sp.jacobi_symbol(root, r))) // 2
                       for root in roots) for r in units}
    assert len(set(labels.values())) == len(units)
    for r, s in itertools.product(units, repeat=2):
        assert labels[(r * s) % modulus] == tuple(
            a ^ b for a, b in zip(labels[r], labels[s]))
    return labels


def model_results(name, d, eps):
    n = 1 << d
    assert all(eps(0, g) == eps(g, 0) == 1 for g in range(n))
    assert all(eps(g, h) in (-1, 1)
               for g, h in itertools.product(range(n), repeat=2))
    comm_fail = [(g, h) for g, h in itertools.product(range(n), repeat=2)
                 if eps(g, h) != eps(h, g)]
    assoc_fail = [(g, h, k) for g, h, k in
                  itertools.product(range(n), repeat=3)
                  if associator(eps, g, h, k) != 1]
    # Full signed domain, not a prime sample or just selected examples.
    signed = list(itertools.product((-1, 1), range(n)))
    for a, b in itertools.product(signed, repeat=2):
        assert mul(eps, a, b)[1] == mul(eps, b, a)[1]
    for a, b, c in itertools.product(signed, repeat=3):
        left = mul(eps, mul(eps, a, b), c)
        right = mul(eps, a, mul(eps, b, c))
        assert left[1] == right[1] == (a[1] ^ b[1] ^ c[1])
    a, b, c = (1, 1), (1, 2), (1, 3)
    result = {
        "dimension": n,
        "negative_basis_squares": sum(eps(g, g) == -1 for g in range(1, n)),
        "commutative": not comm_fail,
        "associative": not assoc_fail,
        "noncommuting_basis_pairs": len(comm_fail),
        "nonassociative_basis_triples": len(assoc_fail),
        "first_associativity_counterexample": assoc_fail[:1],
        "ab_ba": [mul(eps, a, b), mul(eps, b, a)],
        "abc": [mul(eps, mul(eps, a, b), c),
                mul(eps, a, mul(eps, b, c))],
        "aab": [mul(eps, mul(eps, a, a), b),
                mul(eps, a, mul(eps, a, b))],
        "epsilon_table": [[eps(g, h) for h in range(n)] for g in range(n)],
        "signed_pairs_checked": len(signed) ** 2,
        "signed_triples_checked": len(signed) ** 3,
    }
    if d == 3:
        ell = (1, 4)
        result["ab_ell"] = [mul(eps, mul(eps, a, b), ell),
                            mul(eps, a, mul(eps, b, ell))]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("RESULTS.json"))
    args = parser.parse_args()
    labels12 = coordinates(12, (-1, -3))
    labels24 = coordinates(24, (-1, -3, -2))
    results = {name: model_results(name, *model) for name, model in MODELS.items()}
    expected = {
        "T4": (0, True, True), "C4": (2, True, True),
        "H4": (3, False, True), "S4": (1, False, True),
        "N4": (3, True, False), "T8": (0, True, True),
        "B8": (6, False, True), "O8": (7, False, False),
    }
    for name, values in expected.items():
        r = results[name]
        assert (r["negative_basis_squares"], r["commutative"], r["associative"]) == values
    assert results["O8"]["ab_ell"] == [(-1, 7), (1, 7)]
    assert results["B8"]["ab_ell"] == [(1, 7), (1, 7)]
    # The three residues with exactly one available root are dependent.
    assert 5 * 7 % 24 == 11
    indices = [sum(x << i for i, x in enumerate(labels24[r])) for r in (5, 7, 11)]
    assert indices[0] ^ indices[1] == indices[2]
    assert associator(eps_oct, *indices) == 1
    # Independent matrix realization of S4.
    unit = sp.eye(2)
    imag = sp.Matrix([[0, -1], [1, 0]])
    invol = sp.diag(1, -1)
    mats = [unit, imag, invol, imag * invol]
    for g, h in itertools.product(range(4), repeat=2):
        assert mats[g] * mats[h] == eps_split(g, h) * mats[g ^ h]
    x, y = sp.symbols("x y", real=True)
    inner = {}
    for name, eps in (("H4", eps_h), ("S4", eps_split)):
        # c has the fixed arithmetic degree of node -1 in mod 12.
        z, j = [x, y, 0, 0], [0, 0, 0, 1]
        j_inv = [0, 0, 0, eps(3, 3)]
        adj = vector_mul(eps, vector_mul(eps, j, z), j_inv)
        assert adj == [x, -y, 0, 0]
        inner[name] = {"J_square": eps(3, 3),
                       "JzJ_inverse": [str(v) for v in adj]}
    # Gauge invariant diagonal; equivalence cannot join differing counts.
    for name in ("T4", "C4", "H4", "S4", "N4"):
        _, eps = MODELS[name]
        for signs in itertools.product((-1, 1), repeat=3):
            t = (1,) + signs
            assert all(t[g] * t[g] * t[0] * eps(g, g) == eps(g, g)
                       for g in range(4))
    payload = {"claim_ids": ["WINDOW_SIGN_SHADOW_INVARIANT",
                              "WINDOW_SIGN_MODELS_INEQUIVALENT",
                              "WINDOW_NODE_INNER_NONUNIQUE"],
               "domain": "signed basis B_d; bilinear extension only where stated",
               "coordinates12": labels12, "coordinates24": labels24,
               "models": results, "inner_conjugation": inner,
               "dependent_single_root_residues": {"residues": [5, 7, 11],
                   "indices": indices, "O8_associator": 1},
               "status": "PASS", "fts_status_effect": "none"}
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8", newline="\n")
    print("PASS: 8 models; exact finite signed domains; 12/24 character maps; "
          "matrix split model; symbolic inner conjugation. No St_FTS conclusion.")
    print(json.dumps({name: {k: r[k] for k in ("negative_basis_squares", "commutative", "associative", "nonassociative_basis_triples")} for name, r in results.items()}))


if __name__ == "__main__":
    main()
