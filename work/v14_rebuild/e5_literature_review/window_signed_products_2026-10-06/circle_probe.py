"""Exact circle candidate checks; no FTS semantic or status inference."""
import json
import math
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    x1, y1, x2, y2, theta, phi = sp.symbols("x1 y1 x2 y2 theta phi", real=True)
    dot, det = x1*x2 + y1*y2, x1*y2 - y1*x2
    assert sp.expand(dot**2 + det**2 - (x1**2+y1**2)*(x2**2+y2**2)) == 0
    assert sp.trigsimp(sp.cos(theta)*sp.cos(phi)+sp.sin(theta)*sp.sin(phi)-sp.cos(phi-theta)) == 0
    assert sp.trigsimp(sp.cos(theta)*sp.sin(phi)-sp.sin(theta)*sp.cos(phi)-sp.sin(phi-theta)) == 0
    assert sp.expand(((x1+x2)**2+(y1+y2)**2-(x1-x2)**2-(y1-y2)**2)/4-dot) == 0
    assert (-y1)*x2+x1*y2 == det  # Bcal(iu,v).
    u12 = [k for k in range(12) if math.gcd(k, 12) == 1]
    u24 = [k for k in range(24) if math.gcd(k, 24) == 1]
    fibers = [[k for k in u24 if k % 12 == j] for j in u12]
    assert fibers == [[1, 13], [5, 17], [7, 19], [11, 23]]
    assert all((r*s % 24) % 12 == (r % 12)*(s % 12) % 12 for r in u24 for s in u24)
    assert all(r*r % 24 == 1 for r in u24)
    R = lambda k: (k+6) % 24
    K = lambda k: -k % 24
    D = lambda k: (k+12) % 24
    for k in u24:
        assert R(k) in u24 and K(k) in u24
        assert R(R(k)) == D(k) and K(K(k)) == k
        assert K(R(k)) == D(R(K(k)))
        assert R(k) % 12 == 7*k % 12 and K(k) % 12 == 11*k % 12
        assert 13*k % 24 == D(k)
    perms = {tuple(((-1)**j*k+6*m) % 24 for k in u24) for m in range(4) for j in range(2)}
    assert len(perms) == 8
    assert all(tuple(f[u24.index(gk)] for gk in g) in perms for f in perms for g in perms)
    assert tuple(K(R(k)) for k in u24) != tuple(R(K(k)) for k in u24)
    traces = [[1, R(1), R(R(1))], [1, 7 % 24, 49 % 24]]
    assert traces == [[1, 7, 13], [1, 7, 1]]
    order_traces = [[1, R(1), K(R(1))], [1, K(1), R(K(1))]]
    assert order_traces == [[1, 7, 17], [1, 23, 5]]
    left, right = (row[-1] for row in order_traces)
    assert (left-right) % 24 == 12 and left % 12 == right % 12 == 5
    rot = sp.Matrix([[0, -1], [1, 0]])
    mirror = sp.diag(1, -1)
    identity = sp.eye(2)
    assert rot*rot == -identity and mirror*mirror == identity
    assert mirror*rot == -rot*mirror
    basis = [identity, rot, -rot*mirror, mirror]
    assert sp.Matrix.hstack(*(m.reshape(4, 1) for m in basis)).rank() == 4
    table = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))["models"]["S4"]["epsilon_table"]
    for g in range(4):
        for h in range(4):
            assert basis[g]*basis[h] == table[g][h]*basis[g ^ h]
    output = {
        "status": "PASS", "scope": "explicit circle candidate only; no FTS bridge proved",
        "phase_identities": True, "units12": u12, "units24": u24,
        "fibers": fibers, "kernel": fibers[0], "reduction_homomorphism": True,
        "all_arithmetic_squares_identity": True, "geometric_permutations": len(perms),
        "geometric_relations": True, "projected_actions_7_11": True,
        "index_traces_rotation_arithmetic": traces,
        "degree_traces_rotation_arithmetic": [[15*k for k in row] for row in traces],
        "degree_traces_rotation_mirror_orders": [[15*k for k in row] for row in order_traces],
        "order_results_antipodal": True, "order_results_squared_degrees": [150, 150],
        "matrix_span_rank": 4, "S4_products_matched": 16,
    }
    (ROOT / "CIRCLE_RESULTS.json").write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
