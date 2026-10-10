# -*- coding: utf-8 -*-
"""Самопроверки слоя вопросов ФТС (только чтение; канон не меняется).

Проверяет производные файлы, собранные build.py, и входы inputs/ относительно живых реестров
(карточки канона, утверждения графа, проверки C-NN/G60-NN, пункты OPEN_QUESTIONS.md, DN-журнала).
Выход: строки PASS/FAIL, код возврата 1 при любом FAIL.

Запуск: py -3.11 -X utf8 work/v14_rebuild/claim_questions/tools/check.py
"""
import collections
import csv
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sources as S  # noqa: E402
import build as B  # noqa: E402

CQ = HERE.parent
# Решётка аспектов объектов проверяется только после нормализации аспектов (см. README).
LATTICE_ENFORCED = True
NEW_OBJECTS = ['O-DELTA', 'O-KAPPA', 'O-CLOSE', 'O-REFUSE', 'O-SEVER', 'O-PI', 'O-LIFT', 'O-ABSLVL']
ASSERTION_SOURCE_KINDS = ('card', 'claim', 'claim_group', 'finding', 'pattern')
DEFINING_RE = re.compile(r'C-\d{2,3}|G60-\d{2}')


def main():
    fails = []

    def ok(name, cond, detail=''):
        print(('PASS ' if cond else 'FAIL ') + name + ('' if cond or not detail else f' — {detail}'))
        if not cond:
            fails.append(name)

    I = B.load_inputs()
    recs = [json.loads(l) for l in open(CQ / 'QUESTION_CARDS.jsonl', encoding='utf-8')]
    objrecs = [json.loads(l) for l in open(CQ / 'OBJECT_QUESTION_CARDS.jsonl', encoding='utf-8')]
    assertion = [r for r in recs if r['layer'] == 'assertion']
    obj = [r for r in recs if r['layer'] == 'object']

    # --- живые реестры
    src = {a['source_id']: a for a in S.card_assertions() + S.graph_assertions()}
    cards = S.cards()
    checks = S.checks()
    oq = S.open_questions()
    dn = S.journal_questions()
    registry = set(cards) | set(src) | set(checks) | set(oq) | set(dn)
    group_ids = I['group_ids']
    objs = {o['object_id'] for o in I['objects']}

    # --- 1. утверждения
    n_src = len(src)
    ok('источников утверждений 285', n_src == 285, f'источников {n_src}')
    base = [r for r in assertion if not r['parent_question_id']]
    by_src = collections.Counter(r['source_id'] for r in base)
    ok('каждое утверждение имеет ровно один базовый вопрос',
       all(by_src[s] == 1 for s in src) and len(base) == n_src,
       f'базовых {len(base)}; без вопроса {[s for s in src if by_src[s] != 1][:5]}')
    ok('базовый вопрос называется Q-<source_id>',
       all(r['question_id'] == 'Q-' + r['source_id'] for r in base))
    ok('тип источника вопроса совпадает с реестром',
       all(src[r['source_id']]['source_kind'] == r['source_kind'] for r in assertion if r['source_id'] in src))

    # --- 2. уникальность
    all_ids = [r['question_id'] for r in recs]
    ok('question_id уникальны (оба слоя)', len(all_ids) == len(set(all_ids)))
    texts = [r['question'] for r in recs]
    ok('точных дублей текста нет', len(texts) == len(set(texts)))
    ids = set(all_ids)

    # --- 3. родители
    bad_parent = [r['question_id'] for r in recs if r['parent_question_id'] and r['parent_question_id'] not in ids]
    ok('каждый parent_question_id существует', not bad_parent, str(bad_parent[:5]))
    bad_parent_src = [r['question_id'] for r in assertion if r['parent_question_id']
                      and r['parent_question_id'] != 'Q-' + r['source_id']]
    ok('производный вопрос ссылается на базовый вопрос того же источника', not bad_parent_src,
       str(bad_parent_src[:5]))

    # --- 4. ссылки существуют в реестрах
    bad = []
    for r in recs:
        for k in r['known_in_corpus']:
            if k not in registry:
                bad.append(f"{r['question_id']}:known:{k}")
        for c in r['refs']['cards']:
            if c not in cards:
                bad.append(f"{r['question_id']}:card:{c}")
        for c in r['refs']['checks']:
            if c not in checks:
                bad.append(f"{r['question_id']}:check:{c}")
        for c in r['refs']['oq']:
            if c not in oq:
                bad.append(f"{r['question_id']}:oq:{c}")
        for f in r['refs']['files']:
            if f.startswith(('work/', 'source/', 'tools/')) and not (S.ROOT / f).exists():
                bad.append(f"{r['question_id']}:file:{f}")
    ok('каждый ID в known_in_corpus и refs существует (карточки, проверки, якоря, файлы)', not bad,
       '; '.join(bad[:6]))
    ok('ответ в корпусе (known_in_corpus) не пуст у covered и partial',
       not [r['question_id'] for r in recs
            if r['corpus_coverage'] in ('covered', 'partial') and not r['known_in_corpus']])

    # --- 5. ответы и покрытие
    ae = []
    for r in recs:
        if r['answer_status'] == 'answered_elsewhere' or r['corpus_coverage'] == 'answered_elsewhere':
            anchors = re.findall(r'oq-[\w-]+', r['answer_pointer'] or '')
            if not any(a in oq and oq[a]['status'] == 'x' for a in anchors) \
                    or not (r['answer_status'] == 'answered_elsewhere' and r['corpus_coverage'] == 'answered_elsewhere'):
                ae.append(r['question_id'])
    ok('answered_elsewhere: answer_pointer указывает на закрытый [x] пункт OPEN_QUESTIONS', not ae, str(ae[:5]))
    coverage_bad = [r['question_id'] for r in recs if r['corpus_coverage'] not in B.COVERAGE]
    ok('покрытие из словаря covered|partial|open|answered_elsewhere|external', not coverage_bad, str(coverage_bad[:5]))
    ext =[r for r in obj if r['aspect'] == 'external' or r['corpus_coverage'] == 'external']
    ok('аспект external ⇔ покрытие external (объекты)',
       all((r['aspect'] == 'external') == (r['corpus_coverage'] == 'external') for r in obj),
       str([r['question_id'] for r in ext if (r['aspect'] == 'external') != (r['corpus_coverage'] == 'external')][:5]))
    ok('вопросы с аспектом external помечены тегом [внешнее]',
       all('[внешнее]' in r['question'] for r in ext if r['aspect'] == 'external'),
       str([r['question_id'] for r in ext if r['aspect'] == 'external' and '[внешнее]' not in r['question']][:5]))
    open_n = sum(1 for r in recs if r['corpus_coverage'] == 'open')
    ext_n = sum(1 for r in recs if r['corpus_coverage'] == 'external')
    ok('external не входит в число open (раздельные категории)',
       open_n + ext_n + sum(1 for r in recs if r['corpus_coverage'] in ('covered', 'partial', 'answered_elsewhere'))
       == len(recs))

    # --- 6. группы
    ok('у каждого вопроса есть допустимая primary_group',
       all(r['primary_group'] in group_ids for r in recs))
    ok('secondary_groups допустимы и не совпадают с primary',
       all(g in group_ids and g != r['primary_group'] for r in recs for g in r['secondary_groups']))

    # --- 7. объекты
    ok('каждый вопрос к объекту ссылается на объект из реестра', all(r['object_id'] in objs for r in obj))
    ok('у объектов нет дублей', len(objs) == len(I['objects']))
    bad_def = []
    for o in I['objects']:
        for d in o['defining_cards'].split():
            if not (d in cards or d in src or d in checks or DEFINING_RE.fullmatch(d)):
                bad_def.append(f"{o['object_id']}:{d}")
            elif DEFINING_RE.fullmatch(d) and d not in checks:
                bad_def.append(f"{o['object_id']}:{d}")
    ok('карточки-определения объектов существуют (канон, утверждения или проверки)', not bad_def,
       '; '.join(bad_def[:6]))
    ok('аспекты объектов из решётки', all(r['aspect'] in B.LAT_OBJECT for r in obj),
       str([r['question_id'] for r in obj if r['aspect'] not in B.LAT_OBJECT][:6]))

    ok('у каждого объекта есть карточка-определение или пометка «определения в каноне нет»',
       all(o['defining_cards'].strip() or o['definition_note'].strip() for o in I['objects']))
    per_obj = collections.Counter(r['object_id'] for r in obj)
    ok('новые объекты (Δ, κ, Close, Refuse, Sever, π/ι, Lift, 0_A по уровням): 2–4 вопроса каждому',
       all(2 <= per_obj[o] <= 4 for o in NEW_OBJECTS), str({o: per_obj[o] for o in NEW_OBJECTS}))
    form_ids = {o['object_id'] for o in I['objects'] if o['kind'] == 'formula'}
    role_forms = [r for r in obj if r['aspect'] == 'role' and r['object_id'] in form_ids]
    ok('роль формы: все вопросы role по формам ссылаются на родителя QO-ROLE.1 (instance)',
       role_forms and all(r['parent_question_id'] == 'QO-ROLE.1' and r['parent_relation'] == 'instance'
                          for r in role_forms), str(len(role_forms)))
    ok('QO-ROLE.1 существует и не имеет родителя', any(r['question_id'] == 'QO-ROLE.1' and not r['parent_question_id']
                                                       for r in obj))
    ok('у проверяемых объектов есть смысловой аспект из решётки (без «прочего»)',
       all(r['aspect'] in B.LAT_OBJECT for r in obj))

    # --- 8. производные файлы
    ok('OBJECT_QUESTION_CARDS.jsonl — срез слоя object',
       [json.dumps(r, sort_keys=True, ensure_ascii=False) for r in objrecs] ==
       [json.dumps(r, sort_keys=True, ensure_ascii=False) for r in obj])
    groups_rows = list(csv.reader(open(CQ / 'QUESTION_GROUPS.tsv', encoding='utf-8', newline=''), delimiter='\t'))
    expected = len(recs) + len(oq) + len(dn)
    ok('QUESTION_GROUPS.tsv покрывает все вопросы (карточки, объекты, пункты OQ, журнал)',
       len(groups_rows) - 1 == expected, f'строк {len(groups_rows) - 1}, ожидалось {expected}')
    xref = list(csv.reader(open(CQ / 'QUESTION_CROSSREF.tsv', encoding='utf-8', newline=''), delimiter='\t'))[1:]
    ok('QUESTION_CROSSREF.tsv: вопросы и пункты существуют, связь из словаря',
       all(r[0] in ids and r[1] in oq and r[2] in B.LINK_RELATIONS for r in xref))
    print(f'INFO вопросов {len(recs)} (утверждения {len(assertion)}, объекты {len(obj)}); '
          f'связей с OPEN_QUESTIONS {len(xref)}; покрытие: ' +
          ', '.join(f'{k} {v}' for k, v in sorted(collections.Counter(r['corpus_coverage'] for r in recs).items())))
    print(f'ИТОГ: FAIL {len(fails)}')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
