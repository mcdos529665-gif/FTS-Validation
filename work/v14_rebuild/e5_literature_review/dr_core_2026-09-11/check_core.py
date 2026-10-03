"""Independent finite checks for the returned DR core; NOT the C-NN suite.

Report code is never imported or executed. Each case states a bounded predicate.
Run from any directory with Python -X utf8. No third-party dependencies.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent


def partitions(n):
    def extend(labels):
        if len(labels) == n:
            yield tuple(labels)
        else:
            for label in range(max(labels, default=-1) + 2):
                yield from extend(labels + [label])
    yield from extend([])


def factors(q, r):
    return all(q[i] != q[j] or r[i] == r[j]
               for i in range(len(q)) for j in range(len(q)))


def powerset(n):
    return set(range(1 << n))


def moore(family, n):
    return (1 << n) - 1 in family and all(a & b in family for a in family for b in family)


def closure(family, value, n):
    result = (1 << n) - 1
    for member in family:
        if value & member == value:
            result &= member
    return result


def denotations(n, transitions, atoms):
    full = (1 << n) - 1
    result = {0, full, *atoms}
    while True:
        before = set(result)
        result.update(full ^ x for x in before)
        result.update(a & b for a in before for b in before)
        result.update(sum(1 << i for i, targets in enumerate(transitions)
                          if any(x & (1 << t) for t in targets)) for x in before)
        if result == before:
            return result


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, column))
             for column in zip(*b)] for row in a]


def brier_risk(e):
    # Equal prior on two hypotheses; squared loss for posterior P(theta=1).
    return sum((a * b / (2 * (a + b)) if a + b else F(0)) for a, b in zip(*e))


def input_integrity():
    manifest = json.loads((HERE / 'INPUT_MANIFEST.json').read_text(encoding='utf-8'))
    assert len(manifest['files']) == 7
    for entry in manifest['files']:
        data = (HERE / entry['file']).read_bytes()
        assert len(data) == entry['bytes']
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
    return {'reports': 7, 'hashes_match': True}


def fibre_criterion():
    tested = 0
    for q, r in product(product(range(2), repeat=4), repeat=2):
        decoder_exists = any(all(h[q[i]] == r[i] for i in range(4))
                             for h in product(range(2), repeat=2))
        assert decoder_exists == factors(q, r)
        qr = tuple(zip(q, r))
        for t in partitions(4):
            if factors(t, q) and factors(t, r):
                assert factors(t, qr)
        tested += 1
    return {'q_r_pairs': tested, 'carrier_size': 4, 'partitions_per_pair': 15}


def minimum_not_cover():
    q, r = (0, 0, 1, 1), (0, 1, 0, 1)
    qr, middle = tuple(zip(q, r)), (0, 1, 2, 2)
    assert factors(qr, middle) and factors(middle, q)
    assert not factors(q, middle) and not factors(middle, qr)
    assert not factors(q, r) and not factors(r, q)
    return {'blocks': [2, 3, 4], 'incomparable_first_queries': True}


def partition_moore_gap():
    low, mid, high = {0, 3}, {0, 1, 3}, powerset(2)
    assert low < mid < high and all(moore(a, 2) for a in (low, mid, high))
    assert 3 ^ 1 not in mid
    return {'domain_sizes': [2, 3, 4], 'middle_closed_under_complement': False}


def subset_question_gain():
    low = {0, 1, 2, 4, 7}
    mid, high = low | {3}, powerset(3)
    assert all(moore(a, 3) for a in (low, mid, high))
    assert all(closure(a, i, 3) == i for a in (low, mid, high) for i in (1, 2, 4))
    assert closure(low, 3, 3) == closure(low, 5, 3) == 7
    assert closure(mid, 3, 3) != closure(mid, 5, 3)
    assert closure(mid, 5, 3) == closure(mid, 6, 3) == 7
    assert closure(high, 5, 3) != closure(high, 6, 3)
    return {'domain_sizes': [5, 6, 8], 'singleton_observations_equal': True}


def one_question_not_language():
    q = (0, 0, 1)
    ex_r = (1, 0, 1)
    assert not factors(q, ex_r)
    ds = denotations(3, [(2,), (1,), (2,)], [4])
    assert ds == powerset(3)
    return {'one_question_blocks': 2, 'language_blocks': 3, 'denotations': 8}


def independent_quotient():
    transitions = [(2,), (3,), (4,), (3,), (4,), (5,)]
    labels = (False, False, False, False, True, True)
    candidates = list(partitions(6))
    valid = [q for q in candidates if factors(q, labels) and
             all(q[i] != q[j] or {q[t] for t in transitions[i]} ==
                 {q[t] for t in transitions[j]} for i in range(6) for j in range(6))]
    minimum = min(len(set(q)) for q in valid)
    minimizers = [q for q in valid if len(set(q)) == minimum]
    assert len(candidates) == 203 and len(valid) == 4
    assert minimizers == [(0, 1, 2, 1, 3, 3)]
    q = minimizers[0]
    ds = denotations(6, transitions, [48])
    expected = {sum(1 << i for i in range(6) if mask & (1 << q[i]))
                for mask in powerset(4)}
    assert ds == expected and len(ds) == 16
    # An additional allowed question separates 4 and 5 and invalidates this quotient.
    assert not factors(q, (0, 0, 0, 0, 1, 0))
    return {'partitions': 203, 'stable': 4, 'minimum_blocks': 4,
            'minimizers': 1, 'all_language_denotations': 16}


def scalar_readouts():
    xs = tuple(range(-4, 5))
    forms = [tuple(f(x) for x in xs) for f in (abs, lambda x: -abs(x),
             lambda x: x*x, lambda x: -x*x)]
    assert all(factors(a, b) for a in forms for b in forms)
    assert not factors(forms[0], xs)
    assert factors(xs, tuple(-x for x in xs)) and factors(tuple(-x for x in xs), xs)
    assert all(x*x == abs(x)*abs(x) for x in xs)
    return {'sample': list(xs), 'four_scalar_kernels_equal': True,
            'sign_recovery_from_modulus': False}


def projection_coherence():
    states = list(product(range(2), repeat=3))
    failures = [s for s in states if s[0] != (s[0] ^ s[2])]
    assert len(failures) == 4
    assert all((a ^ 0) == a for a in range(2))  # section for direct map
    f, g = lambda x: x, lambda x: x + x*(x-1)
    assert all(f(x) == g(x) for x in (0, 1)) and f(2) != g(2)
    return {'route_mismatches': 4, 'states': 8, 'two_anchors_not_function_identity': True}


def two_completenesses():
    rho, f, g = (0, 2, 2), (0, 0, 2), (1, 2, 2)
    forward = lambda h: all(h[rho[x]] == rho[h[rho[x]]] for x in range(3))
    backward = lambda h: all(rho[h[x]] == rho[h[rho[x]]] for x in range(3))
    assert forward(f) and not backward(f)
    assert backward(g) and not forward(g)
    return {'F_forward_backward': [True, False], 'G_forward_backward': [False, True]}


def dynamic_section():
    f, q = (1, 0), (0, 0)
    assert all(q[f[x]] == q[x] for x in range(2))
    assert all(f[s] != s for s in range(2))
    return {'set_sections': 2, 'transition_preserving_sections': 0}


def sufficiency_not_history():
    e = [[F(x,16) for x in row] for row in ([9,3,3,1],[1,3,3,9])]
    count = [[1,0,0],[0,1,0],[0,1,0],[0,0,1]]
    recover_law = [[1,0,0,0],[0,F(1,2),F(1,2),0],[0,0,0,1]]
    t = matmul(e, count)
    assert matmul(t, recover_law) == e
    assert not factors((0,1,1,2), (0,0,1,1))
    # Equal prior. Only count=1 is ambiguous, with mass 6/16.
    first_bit_risk = F(6,16) * F(1,2)
    assert first_bit_risk == F(3,16)
    return {'channel_law_reconstructed': True, 'first_bit_error_from_count': str(first_bit_risk)}


def fresh_vs_copy():
    single = [[F(3,4),F(1,4)],[F(1,4),F(3,4)]]
    copied = matmul(single, [[1,0,0,0],[0,0,0,1]])
    fresh = [[a*b for a,b in product(row, repeat=2)] for row in single]
    assert brier_risk(single) == brier_risk(copied) == F(3,16)
    assert brier_risk(fresh) == F(3,20) < brier_risk(copied)
    return {'single_and_copy_brier': '3/16', 'two_fresh_brier': '3/20'}


def partial_history():
    states = list(product(range(2), repeat=3))
    low = tuple(c for a,b,c in states)
    mid = tuple((c, a | b) for a,b,c in states)
    high = tuple((c, a+b) for a,b,c in states)
    assert [len(set(v)) for v in (low,mid,high)] == [2,4,6]
    assert factors(high,mid) and factors(mid,low)
    assert not factors(low,mid) and not factors(mid,high)
    return {'outputs': [2,4,6], 'FTS_early_form_excluded': False}


def decoder_budget():
    xs = list(product(range(2), repeat=4))
    parity = tuple(sum(x) % 2 for x in xs)
    tested = 0
    for k in range(4):
        for indices in combinations(range(4), k):
            observation = tuple(tuple(x[i] for i in indices) for x in xs)
            assert not factors(observation, parity)
            tested += 1
    assert factors(tuple(xs), parity)
    return {'proper_coordinate_subsets': tested, 'full_input_contains_answer': True,
            'adaptive_lower_bound': 'see REVIEW proof; not inferred from fixed subsets'}


def exact_vs_as():
    q, r, mass = (0,0), (1,0), (F(0),F(1))
    assert not factors(q,r)
    assert sum(p for p,answer in zip(mass,r) if answer != 0) == 0
    return {'exact_decoder': False, 'zero_error_almost_sure_decoder': True}


def primary_square_checks():
    p = HERE.parent / 'arxiv/cs_0401016v3/source/main.tex'
    data = p.read_bytes()
    assert hashlib.sha256(data).hexdigest() == '1dc82beddef12f71bde268f27303ea3ba37fc9e72516785e9824e23a99ac8eb7'
    assert data[:2] == b'\x1f\x8b'
    source = gzip.decompress(data).decode('utf-8')
    assert r'\bZ_{<0}^2=\bZ_{>0}^2 =\bZ^2' in source
    # 0 is a square of an integer, but not of a strictly positive integer.
    assert 0**2 == 0 and all(z*z != 0 for z in range(1,100))
    witnesses = []
    for n in range(1,5):
        m, next_power = 2**(2**n), 2**(n+1)
        assert 1 < m < 2**next_power
        witnesses.append(m)
    return {'compressed_source_bytes': len(data), 'decoded_bytes': len(source.encode()),
            'strict_sign_zero_counterexample': 0, 'successive_power_witnesses': witnesses,
            'infinite_intersection': 'analytical proof in SOURCE_AUDIT; not a finite test'}


def intermediate_channels():
    bsc = lambda p: [[1-p,p],[p,1-p]]
    e0, e1, e2 = bsc(F(0)), bsc(F(1,4)), bsc(F(1,2))
    assert matmul(e0,bsc(F(1,4))) == e1
    assert matmul(e1,bsc(F(1,2))) == e2
    risk = lambda e: sum(min(a,b)/2 for a,b in zip(*e))
    assert [risk(e) for e in (e0,e1,e2)] == [F(0),F(1,4),F(1,2)]
    return {'optimal_01_risks': ['0','1/4','1/2'], 'strict_intermediate_experiment': True}


CASES = [
    ('DRC-01','Byte integrity of seven submitted reports',input_integrity),
    ('DRC-02','Fibre criterion and fixed-pair minimality on four states',fibre_criterion),
    ('DRC-03','A minimum may skip covers; first queries may be incomparable',minimum_not_cover),
    ('DRC-04','Partition cover has an intermediate Moore domain',partition_moore_gap),
    ('DRC-05','Set questions can grow at unchanged singleton distinguishability',subset_question_gain),
    ('DRC-06','One extra answer does not preserve the temporal language',one_question_not_language),
    ('DRC-07','Independent six-state quotient, all partitions and denotations',independent_quotient),
    ('DRC-08','Scalar reversible recoding and missing sign',scalar_readouts),
    ('DRC-09','Local sections and two anchors do not ensure coherence',projection_coherence),
    ('DRC-10','Forward and backward completeness are independent',two_completenesses),
    ('DRC-11','A dynamic quotient need not have a dynamic section',dynamic_section),
    ('DRC-12','Statistical sufficiency does not recover an actual history',sufficiency_not_history),
    ('DRC-13','Copying and a fresh observation differ in decision value',fresh_vs_copy),
    ('DRC-14','An intermediate history record has two strict information gains',partial_history),
    ('DRC-15','Full information and a restricted decoding budget differ',decoder_budget),
    ('DRC-16','Exact nonfactorization may disappear almost surely',exact_vs_as),
    ('DRC-17','Primary source compression and bounded square counterchecks',primary_square_checks),
    ('DRC-18','Strictly intermediate binary statistical experiment',intermediate_channels),
]


def main():
    rows = []
    for ident, label, case in CASES:
        try:
            detail, status = case(), 'PASS'
        except Exception as error:
            detail, status = {'error': f'{type(error).__name__}: {error}'}, 'FAIL'
        rows.append({'id': ident, 'predicate': label, 'status': status, 'detail': detail})
        print(f'{ident}: {status} — {label}')
    passed = sum(r['status'] == 'PASS' for r in rows)
    result = {'scope': 'finite_external_candidate_checks_not_C_NN',
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'passed': passed, 'failed': len(rows)-passed, 'checks': rows}
    (HERE/'CHECK_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    report = ['# Проверки основного DR-блока', '',
              'Самостоятельный код; вложенный код отчётов не исполняется. Дата пакета: 2026-09-11.',
              'PASS относится к предикату указанного конечного примера, не к ФТС и не к C-NN.', '',
              f'**{passed} PASS / {len(rows)-passed} FAIL.**', '',
              '| ID | Предикат | Итог | Свидетель |', '|---|---|---|---|']
    for r in rows:
        detail = json.dumps(r['detail'],ensure_ascii=False).replace('|','\\|')
        report.append(f"| {r['id']} | {r['predicate']} | {r['status']} | {detail} |")
    (HERE/'CHECK_REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8',newline='\n')
    return int(passed != len(rows))


if __name__ == '__main__':
    raise SystemExit(main())
