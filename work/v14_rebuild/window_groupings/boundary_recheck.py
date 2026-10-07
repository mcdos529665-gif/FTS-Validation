"""Exact finite recheck of window boundaries; no FTS status inference."""
import json
from collections import defaultdict
from itertools import combinations, product
from math import gcd, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent


def units(modulus):
    return [a for a in range(1, modulus) if gcd(a, modulus) == 1]


def generated(a, modulus):
    values = {1}
    value = a % modulus
    while value not in values:
        values.add(value)
        value = value*a % modulus
    return tuple(sorted(values))


def power_classes(modulus):
    buckets = defaultdict(list)
    for a in units(modulus):
        buckets[generated(a, modulus)].append(a)
    return sorted(buckets.values(), key=lambda row: row[0])


def all_subgroups(modulus):
    values = units(modulus)
    found = []
    for size in range(len(values)+1):
        for subset in combinations(values, size):
            subgroup = set(subset)
            if 1 in subgroup and all(a*b % modulus in subgroup for a in subgroup for b in subgroup):
                found.append(tuple(subset))
    return found


def main():
    u22 = units(22)
    subgroups = all_subgroups(22)  # All 1024 subsets, not just inverse pairs.
    signatures = {a: tuple(int(a in subgroup) for subgroup in subgroups) for a in u22}
    buckets = defaultdict(list)
    for a in u22:
        buckets[signatures[a]].append(a)
    classes22 = sorted(buckets.values(), key=lambda row: row[0])
    expected = [[1], [3,5,9,15], [7,13,17,19], [21]]
    assert len(subgroups) == 4 and classes22 == expected
    assert classes22 == power_classes(22)
    for a,b in product(u22, repeat=2):
        assert (signatures[a] == signatures[b]) == (generated(a,22) == generated(b,22))
    assert len(generated(7,22)) == 10  # Explicit cyclic generator of U22.
    assert signatures[3] == signatures[9] and 3 != 9 and 3*9 % 22 == 5
    bad_pairs = [(a,b) for a,b in product(u22,repeat=2)
                 if signatures[a] == signatures[b] and a != b and a*b % 22 != 1]
    assert len(bad_pairs) == 16
    maxima = [[m,max(map(len,power_classes(m)))] for m in range(2,25,2)]
    assert [size for _,size in maxima] == [1,1,1,1,2,1,2,2,2,2,4,1]
    first = next(m for m,size in maxima if size>2)
    assert first == 22

    representations = {n: [[x,y] for x in range(isqrt(n)+1) for y in range(isqrt(n)+1)
                           if x*x+y*y == n] for n in (1,5,9,13,17,21)}
    assert all(representations[n] for n in (1,5,9,13,17)) and not representations[21]
    assert gcd(5,48) == 1 and 5*5 % 48 == 25
    generators96 = next(row for row in power_classes(96) if 5 in row)
    assert generators96 == [5,29,53,77] and len(generated(5,96)) == 8
    results = {
        'status':'PASS', 'scope':'finite subgroup-membership observation only; no FTS role proved',
        'WB22':{'units':u22,'subsets_checked':1024,'all_subgroups':subgroups,
                'classes':classes22,'all_pairs_checked':100,'non_inverse_equal_profile_pairs':len(bad_pairs),
                'witness':{'a':3,'b':9,'same_signature':True,'product_mod22':5},
                'cyclic_generator':7,'generator_order':10},
        'WB_FIRST_EVEN':{'max_class_sizes':maxima,'first_even_step':first,'window_length':first+1},
        'WB_EXISTING':{'two_square_representations':representations,'5_squared_mod48':25,
                       'generators_same_subgroup_mod96':generators96,'subgroup_order96':8},
    }
    (HERE/'BOUNDARY_RECHECK_RESULTS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('PASS boundary recheck: 1024 subsets, 100 pairs, all 12 even steps; first class larger than 2 at step22/window23; examples21/48/96 retained.')


if __name__ == '__main__':
    main()
