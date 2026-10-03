"""Внешний булевый предел AC-2026-09-21; не тест семантики ФТС."""

from itertools import product


def main():
    print("Boolean shadow of the exact nested grouping; no FTS status conclusion")
    print("p q | C=p&q D=p|q | U6=(C&D) U7=(C&D)|(C|D)")
    rows = []
    for p, q in product((False, True), repeat=2):
        c = p and q
        d = p or q
        u6 = c and d
        u7 = (c and d) or (c or d)
        rows.append((p, q, c, d, u6, u7))
        print(*(int(x) for x in (p, q, c, d, u6, u7)))
    assert all(u6 == (p and q) for p, q, c, d, u6, u7 in rows)
    assert all(u7 == (p or q) for p, q, c, d, u6, u7 in rows)
    assert all(not u6 and u7 for p, q, c, d, u6, u7 in rows if q == (not p))
    print("PASS: exact grouping evaluated on 4/4 ordinary Boolean valuations")
    print("Scope only: this does not define or refute the FTS operator")


if __name__ == "__main__":
    main()
