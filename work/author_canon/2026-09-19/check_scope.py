"""Конечные свидетели границ внешнего чтения AC-2026-09-19, не тест ФТС."""

from itertools import product


def main():
    print("Boolean reading with independent p,q; no FTS status conclusion")
    print("p q | U6 U7 | p&q p|q")
    rows = []
    for p, q in product((False, True), repeat=2):
        u6 = (p or q) and (p and q)
        u7 = (p or q) or (p and q)
        rows.append((p, q, u6, u7))
        print(*(int(x) for x in (p, q)), "|", int(u6), int(u7), "|", int(p and q), int(p or q))
    assert all(u6 == (p and q) and u7 == (p or q) for p, q, u6, u7 in rows)
    assert all(not u6 and u7 for p, q, u6, u7 in rows if q == (not p))
    print("PASS: absorption on 4/4 valuations; q=not p gives False/True")

    def qnorm(z):
        return z.real * z.real + z.imag * z.imag

    z1, z2 = 1+0j, -1+0j
    assert z1 != z2 and qnorm(z1) == qnorm(z2) and -qnorm(z1) == -qnorm(z2)
    print("PASS: z=+1 and z=-1 have equal Q=1 and -Q=-1")
    coherent = qnorm(z1+z2)
    componentwise = qnorm(z1)+qnorm(z2)
    assert coherent == 0 and componentwise == 2
    print(f"PASS: Q(1+(-1))={coherent:g}; Q(1)+Q(-1)={componentwise:g}")
    print("Scope only: these checks do not prove or refute FTS AND/OR or U7 phase visibility")


if __name__ == "__main__":
    main()
