"""Finite counterchecks for the submitted recursive-distinction note, not C-NN."""
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def factors(q, r):
    return all(q[i] != q[j] or r[i] == r[j]
               for i in range(len(q)) for j in range(len(q)))


def source_integrity():
    m = json.loads((HERE/'INPUT_MANIFEST.json').read_text(encoding='utf-8'))
    data = (HERE/m['file']).read_bytes()
    assert len(data) == m['bytes'] and sha256(data).hexdigest() == m['sha256']
    return {'bytes': len(data), 'source_sha256': m['sha256']}


def capacity_vs_activity():
    states = tuple(product((0, 1), repeat=2))
    active = tuple(a for a, b in states)
    answer = tuple(b for a, b in states)
    assert not factors(active, answer)
    assert factors(states, answer)
    # Both systems receive the same tuple and may read either coordinate at unit cost.
    return {'from_active_readout': False, 'from_available_state': True,
            'same_decoder_cost': 1}


def operator_without_data():
    states = (-1, 1)
    magnitude = tuple(abs(x) for x in states)
    sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)
    answer = tuple(sign(x) for x in states)
    assert not factors(magnitude, answer)
    assert tuple(sign(v) for v in magnitude) != answer
    return {'sign_operation_available': True, 'original_sign_recoverable': False}


def kernel_reflexivity():
    count = 0
    for q in product((0, 1), repeat=4):
        eq = lambda a, b: q[a] == q[b]
        assert all(eq(a, a) for a in range(4))
        assert all(not (eq(a, b) and eq(b, c)) or eq(a, c)
                   for a, b, c in product(range(4), repeat=3))
        count += 1
    return {'total_observers_checked': count, 'can_have_Eq_a_a_false': False}


def tolerance_not_equality():
    adm = lambda a, b: abs(a-b) <= 1
    assert adm(0, 1) and adm(1, 2) and not adm(0, 2)
    return {'witness': [0, 1, 2], 'tolerance': 1, 'transitive': False}


def excluded_middle_not_knowledge():
    models = (False, True)
    known = lambda predicate: all(predicate(a) for a in models)
    assert known(lambda a: a or not a)
    assert not (known(lambda a: a) or known(lambda a: not a))
    return {'known_excluded_middle': True, 'known_either_answer': False}


def evidence_channels():
    values = tuple(product((0, 1), repeat=2))
    neg = lambda v: (v[1], v[0])
    designated = lambda v: v[0] == 1
    info_le = lambda a, b: all(x <= y for x, y in zip(a, b))
    assert all(info_le((0, 0), v) and info_le(v, (1, 1)) for v in values)
    assert not info_le((0, 1), (1, 0)) and not info_le((1, 0), (0, 1))
    p, q = (1, 1), (0, 0)
    assert designated(p) and designated(neg(p)) and not designated(q)
    assert [v for v in values if (v[0] or v[1]) and not (v[0] and v[1])] == [(0, 1), (1, 0)]
    return {'values': 4, 'information_order_total': False,
            'explosion_under_positive_designation': False,
            'FTS_absence_semantics_proved': False}


def triple_overlap():
    triples = [(2*k-1, 2*k, 2*k+1) for k in range(4)]
    assert triples == [(-1, 0, 1), (1, 2, 3), (3, 4, 5), (5, 6, 7)]
    assert all(set(a) & set(b) == {a[-1]} for a, b in zip(triples, triples[1:]))
    assert len(triples[0]) != len((-1, 0, 1, 2, 3))
    return {'triples': triples, 'shared_boundary_levels': [1, 3, 5],
            'semantic_recursion_proved': False}


CASES = [
    ('RN-01', 'Байты исходной записки', source_integrity),
    ('RN-02', 'Активный вывод и доступный аппарат', capacity_vs_activity),
    ('RN-03', 'Операция без сохранённых исходных данных', operator_without_data),
    ('RN-04', 'Рефлексивность ядра полного наблюдателя', kernel_reflexivity),
    ('RN-05', 'Допустимая погрешность не обязана быть транзитивной', tolerance_not_equality),
    ('RN-06', 'Исключённое третье не даёт известного ответа', excluded_middle_not_knowledge),
    ('RN-07', 'Модель двух каналов без explosion', evidence_channels),
    ('RN-08', 'Индексное перекрытие четырёх троек', triple_overlap),
]


def main():
    rows = []
    for ident, label, run in CASES:
        try:
            evidence, status = run(), 'PASS'
        except Exception as error:
            evidence, status = {'error': f'{type(error).__name__}: {error}'}, 'FAIL'
        rows.append({'id': ident, 'predicate': label, 'status': status, 'evidence': evidence})
        print(f'{ident} {status}: {label}')
    passed = sum(r['status'] == 'PASS' for r in rows)
    result = {'scope': 'finite_external_models_not_FTS_status',
              'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'passed': passed, 'failed': len(rows)-passed, 'checks': rows}
    (HERE/'CHECK_RESULTS.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n',
                                         encoding='utf-8', newline='\n')
    report = ['# Проверки записки о рекурсивном различении', '',
              '2026-09-12. Конечные внешние модели; не C-NN, не доказательство статусов ФТС.',
              'PASS контрпримера подтверждает ограничение проверяемой внешней формулировки.', '',
              f'**{passed} PASS / {len(rows)-passed} FAIL.**', '',
              '| ID | Предикат | Результат | Свидетель |', '|---|---|---|---|']
    for row in rows:
        detail = json.dumps(row['evidence'], ensure_ascii=False).replace('|', '\\|')
        report.append(f"| {row['id']} | {row['predicate']} | {row['status']} | {detail} |")
    (HERE/'CHECK_REPORT.md').write_text('\n'.join(report)+'\n', encoding='utf-8', newline='\n')
    return int(passed != len(rows))


if __name__ == '__main__':
    raise SystemExit(main())
