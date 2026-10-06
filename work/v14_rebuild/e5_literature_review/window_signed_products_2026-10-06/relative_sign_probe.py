"""Candidate paired readout, using the previously verified signed tables."""
import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).parent


def observe(u, v, n):
    x, y = [0] * n, [0] * n
    x[u[1]], y[v[1]] = u[0], v[0]
    plus = sum((a + b) ** 2 for a, b in zip(x, y))
    minus = sum((a - b) ** 2 for a, b in zip(x, y))
    assert (plus - minus) % 4 == 0
    return {"plus": plus, "minus": minus, "relative": (plus - minus) // 4}


def main():
    sign_rows = []
    for s, t in product((-1, 1), repeat=2):
        got = observe((s, 1), (t, 1), 4)
        assert got["relative"] == s * t
        assert got == observe((-s, 1), (-t, 1), 4)
        sign_rows.append({"s": s, "t": t, **got})
    source = json.loads((ROOT / "RESULTS.json").read_text(encoding="utf-8"))
    rows = {}
    for name, model in source["models"].items():
        n, eps = model["dimension"], model["epsilon_table"]
        def mul(u, v):
            return u[0] * v[0] * eps[u[1]][v[1]], u[1] ^ v[1]
        a, b, c, one = (1, 1), (1, 2), (1, 3), (1, 0)
        row = {
            "square_a": observe(mul(a, a), one, n),
            "square_node_c": observe(mul(c, c), one, n),
            "order_ab": observe(mul(a, b), mul(b, a), n),
            "grouping_aab": observe(mul(mul(a, a), b), mul(a, mul(a, b)), n),
        }
        if n == 8:
            ell = (1, 4)
            row["grouping_ab_ell"] = observe(mul(mul(a, b), ell), mul(a, mul(b, ell)), n)
        rows[name] = row
    assert rows["H4"]["square_node_c"] == {"plus": 0, "minus": 4, "relative": -1}
    assert rows["S4"]["square_node_c"] == {"plus": 4, "minus": 0, "relative": 1}
    assert rows["B8"]["grouping_ab_ell"]["relative"] == 1
    assert rows["O8"]["grouping_ab_ell"]["relative"] == -1
    # The prescribed probe vectors distinguish the five 4D and three 8D examples.
    for dimension in (4, 8):
        signatures = [tuple(v["relative"] for v in row.values())
                      for name, row in rows.items()
                      if source["models"][name]["dimension"] == dimension]
        assert len(set(signatures)) == len(signatures)
    result = {"status": "PASS", "sign_rows": sign_rows, "models": rows,
              "assumptions": "common real vector carrier; paired addition before projection; orthonormal basis",
              "limitation": "candidate readout, no executable FTS operation identified; not a multiplicative norm assumption"}
    (ROOT / "RELATIVE_SIGN_RESULTS.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("PASS: four sign pairs; all 8 model readouts; H/S square and B/O grouping distinguished.")


if __name__ == "__main__":
    main()
