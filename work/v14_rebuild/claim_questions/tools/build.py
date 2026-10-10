# -*- coding: utf-8 -*-
"""Сборка слоя вопросов ФТС: входы (inputs/) + снимок источников (sources.py) -> производные файлы.

Инструмент проверки, не канон: source/ и work/ только читаются.
Производные (перезаписываются при каждом запуске, байт-в-байт детерминированы):
  QUESTION_CARDS.jsonl          — все карточки вопросов, поле layer: assertion | object;
  OBJECT_QUESTION_CARDS.jsonl   — производный вид: только layer=object;
  OBJECTS.md                    — реестр объектов и их вопросы;
  QUESTION_GROUPS.md/.tsv       — группы всех вопросов проекта (оба слоя, OPEN_QUESTIONS, журнал);
  QUESTION_CROSSREF.tsv         — ручные связи с OPEN_QUESTIONS (из inputs/crossref.tsv, проверенные);
  DUPLICATE_CANDIDATES.tsv      — почти-дубли для ручного решения (не исправляются автоматически).

Запуск: py -3.11 -X utf8 work/v14_rebuild/claim_questions/tools/build.py
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

CQ = HERE.parent
INP = CQ / 'inputs'
ROOT = S.ROOT

# ---------- решётки и словари ----------
LAT_ASSERT = ['answered', 'gap', 'bridge', 'obligation', 'test', 'limit', 'term', 'compare']
LAT_OBJECT = ['definition', 'identity', 'symmetry', 'image', 'preimage', 'neighbor', 'mirror',
              'uniqueness', 'role', 'external']
COVERAGE = ['covered', 'partial', 'open', 'answered_elsewhere', 'external']
LINK_RELATIONS = ['same', 'instance', 'related', 'answered_by_closed', 'premise_outdated']

GROUP_FALLBACK = {}  # заполняется из inputs/groups.tsv

# Отнесение карточек/утверждений к группам по семейству источника (первое совпадение побеждает).
SOURCE_GROUP_FIXED = {
    'O_09': 'G10', 'O_12': 'G10', 'O_13': 'G10', 'O_14': 'G10', 'O_15': 'G10', 'O_16': 'G10', 'O_17': 'G10',
    'O_18': 'G10', 'O_19': 'G10', 'O_20': 'G11', 'OP_kappa': 'G10', 'OP_WindowClose': 'G03', 'A0b': 'G07',
    'A5': 'G10', 'A5a': 'G10', 'ADDENDUM_V3': 'G13', 'ADD_NOTATION_ABS': 'G13', 'ADD_RESEARCH_FORMAT': 'G13',
    'ADD_U11_EPI': 'G04', 'ADD_U12_CIRCLE': 'G05', 'SP_U8': 'G04', 'SP_U9': 'G04', 'SP_U12': 'G05',
    'A_07': 'G03', 'U12_CHI_PI_COMPLEX_BOUNDARY': 'G08',
    'CM-001': 'G06', 'CM-002': 'G04', 'CM-003': 'G04', 'CM-004': 'G04', 'CM-005': 'G04', 'CM-006': 'G05',
    'CM-007': 'G05', 'CM-008': 'G05', 'CM-009': 'G07', 'CM-010': 'G06', 'CM-011': 'G08', 'CM-012': 'G05',
    'CM-013': 'G06', 'CM-014': 'G06', 'CM-015': 'G08', 'CM-016': 'G06', 'CM-017': 'G13', 'CM-018': 'G13',
    'CM-019': 'G13', 'CM-020': 'G11', 'CM-021': 'G11', 'CM-022': 'G11', 'CM-023': 'G09', 'CM-024': 'G09',
    'CM-025': 'G12',
    'PA-C01': 'G09', 'PA-C02': 'G09', 'PA-C03': 'G09', 'PA-C04': 'G09', 'PA-C05': 'G09', 'PA-C06': 'G08',
    'PA-C07': 'G01', 'PA-C08': 'G08', 'PA-C09': 'G12', 'PA-F01': 'G06', 'PA-F02': 'G06', 'PA-F03': 'G06',
    'PA-F04': 'G07', 'PA-F05': 'G08', 'PA-F06': 'G06', 'PA-F07': 'G06', 'PA-F08': 'G05', 'PA-F09': 'G05',
    'PA-F10': 'G08', 'PA-F11': 'G06', 'PA-G01': 'G13', 'PA-G02': 'G13', 'PA-G03': 'G13', 'PA-G04': 'G13',
    'PA-R01': 'G13', 'PA-R02': 'G13', 'PA-R03': 'G11', 'PA-R04': 'G11', 'PA-R05': 'G11', 'PA-R06': 'G13',
    'PA-R07': 'G12',
    'DR10_QG_WITNESS': 'G10', 'NEURAL_T2_SCAFFOLD': 'G11', 'NEURAL_T3_NOT_VERIFIED': 'G11',
    'OQ25_DEFINITION_OPTIONS': 'G13', 'OQ25_RELATION_PRODUCT': 'G03', 'OQ25_SECTION_NATURALITY': 'G01',
    'OQ25_U6_PROVENANCE': 'G03', 'OQ25_UNITS48': 'G07', 'U4_U7_TYPED_CANDIDATE': 'G03',
    'U6_Q_NOT_SUFFICIENT_FOR_U7': 'G03', 'U6_VSTAR_BRIDGE_UNDERDETERMINED': 'G03',
}


def source_group(sid):
    """Группа утверждения по семейству источника."""
    m = re.fullmatch(r'(U|M|CH)_(m1|\d\d)', sid)
    if m:
        n = -1 if m.group(2) == 'm1' else int(m.group(2))
        return 'G02' if n <= 6 else 'G03' if n == 7 else 'G04' if n <= 11 else 'G05'
    if sid in SOURCE_GROUP_FIXED:
        return SOURCE_GROUP_FIXED[sid]
    if re.fullmatch(r'AF-0(0[1-4]|09|1[0-3]|17|19|20)', sid):
        return 'G13'
    if re.fullmatch(r'AF-0(0[5-7]|1[4-6])', sid):
        return 'G11'
    if sid in ('AF-008', 'AF-018'):
        return 'G12'
    if sid.startswith('DN_'):
        return 'G14'
    if sid in ('WINDOW_ABSOLUTIZATION_AUTHOR', 'WINDOW_COUNTERWEIGHT_AUTHOR',
               'WINDOW_COUNTERWEIGHT_TRANSFER_CANDIDATE', 'WINDOW_COUNTING_AUTHOR',
               'WINDOW_FIRST_DISTINCTION_AUTHOR', 'WINDOW_JOINT_SCOPE_DIRECTION'):
        return 'G14'
    if sid.startswith(('WINDOW_', 'AC_2026')):
        return 'G07'
    if re.fullmatch(r'O_(0[1-8]|1[01])', sid):
        return 'G01'
    if sid.startswith('OP_Chi') or sid.startswith('OP_Complex') or sid.startswith('OP_Tensor'):
        return 'G08'
    if sid.startswith('OP_'):
        return 'G01'
    if re.fullmatch(r'A\d', sid):
        return 'G01'
    if re.fullmatch(r'F\d|T7[ABC]', sid):
        return 'G10'
    if sid in ('ADD_MIRROR_WINDOW', 'ADD_ZERO_BOUNDARY', 'ADD_PARITY_TOPOLOGY', 'ADD_TOPO_INVARIANTS',
               'SP_WINDOW', 'SP_ZERO', 'ADD_HALF_PHI', 'ADD_CONSTANTS'):
        return 'G06'
    if sid.startswith('U7_'):
        return 'G03'
    if sid.startswith(('CHI_', 'COMPLEX_', 'TENSOR_')):
        return 'G08'
    raise KeyError(f'нет правила группы для источника {sid}')


# ---------- регулярные выражения для явных ссылок (границы слов через (?<!\w)/(?!\w)) ----------
CARD_IDS = sorted(S.cards().keys(), key=len, reverse=True)
CARD_RE = re.compile(r'(?<![\w-])(' + '|'.join(re.escape(c) for c in CARD_IDS) + r')(?![\w-])')
LVL_RE = re.compile(r'(?<!\w)(?:МУ|ЛУ|СУ|У|U_?)\(?(−1|-1|m1|\d{1,2})\)?(?!\d|\.\d)')
LVL_RANGE_RE = re.compile(r'(?<!\w)(?:МУ|ЛУ|СУ|У)(\d{1,2})\s*[–…-]\s*(?:МУ|ЛУ|СУ|У)?(\d{1,2})(?!\w)')
CHECK_RE = re.compile(r'(?<![\w-])(?:C-?(\d{2,3})|G60-(\d{2}))(?![\w-])')
DICT_RE = re.compile(r'(?<!\w)Д(\d{1,2})(?!\d)')
CRIT_RE = re.compile(r'(?<!\w)(К[1-5]|О[1-9]\d?|F[1-6]|O_\d\d)(?!\d)')
OQ_RE = re.compile(r'(?<![\w-])(oq-[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(?![\w-])')
FILE_RE = re.compile(r'(?<![\w/.-])((?:work|source|tools)/[\w./-]+|[\w-]+\.(?:py|md|tsv|jsonl|json|txt|csv|html))(?![\w/-])')

EXT_DOMAINS = {
    'Blackwell/теория решений': r'Blackwell|Блэкуэлл|статистическ\w+ теори\w+ решени',
    'категории/HoTT': r'HoTT|категор|WFS|морфизм',
    'комплексные числа/фаза': r'комплекс|фаз|exp\(i|e\^\{?i|\bz/\|z\|',
    'кватернионы/октонионы/Фано': r'Фано|октонион|кватернион|\bH4\b|\bO8\b|\bS4\b|\bB8\b',
    'теория групп/Галуа/вычеты': r'Галуа|mod ?\d+|\(Z/|C4×|V4|группа обратимых|вычет',
    'эллиптические функции/Якоби/℘': r'Якоби|Вейерштрасс|℘|j-инвариант|эллиптич',
    'p-адические числа': r'адич',
    'топология/χ_E/сфера/тор': r'χ_E|Пуанкаре|(?<!\w)тор(?:а|у|ом|е|ы|ов)?(?!\w)|(?<!\w)тороид|(?<!\w)сфер|топологич',
    'вероятность/ЦПТ/Леви/Эджворт': r'ЦПТ|Леви|Lévy|Эджворт|кумулянт|тяж[её]л\w+ хвост',
    'Виета/многочлены': r'Виет|многочлен',
    'Фурье': r'Фурье',
    'гиперболические функции': r'гипербол|cosh',
    'фрактал/Серпинский': r'Серпинск|самоподоб|фрактал',
    'нейросети': r'нейр|neural|scaffold',
    'логика/диагональ': r'диагонал|самоприменен',
    'χ-статистика': r'χ(?!_E)|(?<!\w)chi(?!\w)|CHI_|p-value',
    'анализ и статистика (производная, гладкость, сходимость, дисперсия, мера)':
        r'(?<!\w)(производн\w*|гладк\w*|дифференцир\w*|сходимост\w*|дисперси\w*|мер[аыуе](?!\w)|интеграл\w*)',
}
# Какая группа отвечает за внешнюю область (для вторичных групп).
EXT_GROUP = {
    'Blackwell/теория решений': 'G12', 'категории/HoTT': 'G12', 'комплексные числа/фаза': 'G08',
    'кватернионы/октонионы/Фано': 'G07', 'теория групп/Галуа/вычеты': 'G07',
    'эллиптические функции/Якоби/℘': 'G05', 'p-адические числа': 'G07',
    'топология/χ_E/сфера/тор': 'G08', 'вероятность/ЦПТ/Леви/Эджворт': 'G08', 'Виета/многочлены': 'G05',
    'Фурье': 'G08', 'гиперболические функции': 'G05', 'фрактал/Серпинский': 'G07', 'нейросети': 'G11',
    'логика/диагональ': 'G09', 'χ-статистика': 'G08',
}
CLASS_RE = {
    'data': r'OpenML|RadioML|CFO|датасет|benchmark|предрегистр|pre-?registered|Wilcoxon|repeated CV|'
            r'train-fold|o20|d2_sign|d10|прогон',
    'infrastructure': r'workbook|MANIFEST|экспорт|export|граф|depends_on|TSV|JSONL|verification\.py|'
                      r'probes\.py|SymPy|CHECKSUMS',
    'author_decision': r'за автором|решение автора|авторск\w+ решени|выберет автор|Решение за автором|'
                       r'author_choice|автор\w* (?:не )?принял',
}
CLASS_GROUP = {'data': 'G11', 'infrastructure': 'G13', 'author_decision': 'G14'}


def levels_in(text):
    out = set()
    for m in LVL_RE.finditer(text):
        v = m.group(1)
        n = -1 if v in ('−1', '-1', 'm1') else int(v)
        if -1 <= n <= 17:
            out.add(n)
    for m in LVL_RANGE_RE.finditer(text):
        a, b = int(m.group(1)), int(m.group(2))
        if a < b <= 17:
            out.update(range(a, b + 1))
    return sorted(out)


def refs_of(text, own_id=None):
    """Явные ссылки из текста: уровни, карточки, проверки, словарь, критерии, якоря, файлы."""
    cards = sorted(set(CARD_RE.findall(text)) - {own_id})
    checks = sorted({('C-%02d' % int(a)) if a else ('G60-' + b) for a, b in CHECK_RE.findall(text)})
    dictionary = sorted({'Д' + d for d in DICT_RE.findall(text) if 1 <= int(d) <= 11})
    criteria = sorted(set(CRIT_RE.findall(text)))
    oq = sorted(set(OQ_RE.findall(text)))
    files = sorted(set(FILE_RE.findall(text)))
    return {'levels': levels_in(text), 'cards': cards, 'checks': checks, 'dict': dictionary,
            'criteria': criteria, 'oq': oq, 'files': files}


def external_of(text):
    return sorted(k for k, p in EXT_DOMAINS.items() if re.search(p, text))


def classes_of(text):
    return sorted(k for k, p in CLASS_RE.items() if re.search(p, text))


def theme_groups(externals, classes, primary):
    """Вторичные группы: тематические семейства, которых касается текст (кроме основной)."""
    gs = {EXT_GROUP[e] for e in externals if e in EXT_GROUP}
    gs |= {CLASS_GROUP[c] for c in classes if c in CLASS_GROUP}
    gs.discard(primary)
    return sorted(gs)


# ---------- чтение таблиц ----------
def read_table(path, header):
    with open(path, encoding='utf-8', newline='') as f:
        rows = list(csv.reader(f, delimiter='\t'))
    if rows[0] != header:
        raise ValueError(f'{path.name}: заголовок {rows[0]} != {header}')
    out = []
    for i, r in enumerate(rows[1:], 2):
        if not any(x.strip() for x in r):
            continue
        if len(r) != len(header):
            raise ValueError(f'{path.name}:{i}: полей {len(r)} вместо {len(header)}')
        d = dict(zip(header, r))
        d['_line'] = i
        out.append(d)
    return out


def split_ids(s):
    return [x for x in s.split() if x]


def norm_check(x):
    m = re.fullmatch(r'C-?(\d{2,3})', x)
    return ('C-%02d' % int(m.group(1))) if m else x


ASSERT_HEADER = ['question_id', 'source_kind', 'source_id', 'question_kind', 'parent_question_id', 'question',
                 'previous_question', 'revised', 'added', 'answer_status', 'answer_pointer', 'premise_note',
                 'checked', 'corpus_coverage', 'known_in_corpus']
OBJECT_HEADER = ['question_id', 'object_id', 'aspect', 'aspect_detail', 'parent_question_id', 'parent_relation',
                 'corpus_coverage', 'known_in_corpus', 'answer_status', 'answer_pointer', 'added', 'revised',
                 'previous_question', 'question']
OBJECTS_HEADER = ['object_id', 'label', 'role', 'kind', 'primary_group', 'aliases_regex', 'defining_cards',
                  'definition_note']
GROUPS_HEADER = ['group_id', 'name', 'criteria', 'asks', 'points_to']
OQ_GROUPS_HEADER = ['oq_id', 'primary_group', 'secondary_groups']
CROSSREF_HEADER = ['question_id', 'open_question', 'relation', 'note']


def load_inputs():
    groups = read_table(INP / 'groups.tsv', GROUPS_HEADER)
    group_ids = {g['group_id'] for g in groups}
    objects = read_table(INP / 'objects.tsv', OBJECTS_HEADER)
    oq_groups = read_table(INP / 'oq_groups.tsv', OQ_GROUPS_HEADER)
    return dict(groups=groups, group_ids=group_ids, objects=objects, oq_groups=oq_groups,
                assertion=read_table(INP / 'assertion_questions.txt', ASSERT_HEADER),
                object=read_table(INP / 'object_questions.txt', OBJECT_HEADER),
                crossref=read_table(INP / 'crossref.tsv', CROSSREF_HEADER))


def build_records(I):
    """Возвращает (assertion_records, object_records, oq_items, dn_items, crossref_rows, warnings)."""
    warnings = []
    src = {}
    for a in S.card_assertions() + S.graph_assertions():
        if a['source_id'] in src:
            raise ValueError(f'дубль источника {a["source_id"]}')
        src[a['source_id']] = a
    oq = S.open_questions()
    dn = S.journal_questions()
    group_ids = I['group_ids']

    # --- оверлей групп открытых вопросов
    oqg = {r['oq_id']: r for r in I['oq_groups']}
    missing_oq = set(oq) - set(oqg)
    extra_oq = set(oqg) - set(oq)
    if missing_oq or extra_oq:
        raise ValueError(f'oq_groups: нет групп для {sorted(missing_oq)}, лишние {sorted(extra_oq)}')
    for k, r in oqg.items():
        if r['primary_group'] not in group_ids:
            raise ValueError(f'oq_groups {k}: неизвестная группа {r["primary_group"]}')

    # --- утверждения
    assertion = []
    seen_q = set()
    for r in I['assertion']:
        qid = r['question_id']
        if qid in seen_q:
            raise ValueError(f'дубль question_id {qid}')
        seen_q.add(qid)
        s = src.get(r['source_id'])
        if s is None:
            raise ValueError(f'{qid}: нет источника {r["source_id"]}')
        if s['source_kind'] != r['source_kind']:
            raise ValueError(f'{qid}: kind {r["source_kind"]} != {s["source_kind"]}')
        text = r['question'] + ' ‖ ' + s['source_text']
        refs = refs_of(text, own_id=r['source_id'])
        ext = external_of(text)
        cls = classes_of(text)
        primary = source_group(r['source_id'])
        rec = {
            'question_id': qid,
            'layer': 'assertion',
            'parent_question_id': r['parent_question_id'] or None,
            'parent_relation': 'derived' if r['parent_question_id'] else None,
            'source_kind': s['source_kind'],
            'source_id': s['source_id'],
            'source_status': s['source_status'],
            'source_text': s['source_text'],
        }
        for k in ('source_verdict', 'source_resolution', 'source_unresolved'):
            if k in s:
                rec[k] = s[k]
        rec.update({
            'question_kind': r['question_kind'],
            'question': r['question'],
            'primary_group': primary,
            'secondary_groups': theme_groups(ext, cls, primary),
            'refs': refs,
            'classes': cls,
            'external_domains': ext,
            'known_in_corpus': split_ids(r['known_in_corpus']),
            'corpus_coverage': r['corpus_coverage'],
            'answer_status': r['answer_status'],
            'answer_pointer': r['answer_pointer'] or None,
            'premise_note': r['premise_note'] or None,
            'checked': r['checked'] or None,
            'question_origin': 'assistant_derived',
            'author_review': 'none',
            'added': r['added'] or None,
            'revised': r['revised'] or None,
            'previous_question': r['previous_question'] or None,
        })
        assertion.append(rec)

    # --- объекты
    objs = {o['object_id']: o for o in I['objects']}
    for o in objs.values():
        if o['primary_group'] not in group_ids:
            raise ValueError(f'объект {o["object_id"]}: неизвестная группа {o["primary_group"]}')
    obj_records = []
    for r in I['object']:
        qid = r['question_id']
        if qid in seen_q:
            raise ValueError(f'дубль question_id {qid}')
        seen_q.add(qid)
        o = objs.get(r['object_id'])
        if o is None:
            raise ValueError(f'{qid}: нет объекта {r["object_id"]}')
        text = r['question']
        refs = refs_of(text)
        ext = external_of(text)
        cls = classes_of(text)
        primary = o['primary_group']
        aspect = r['aspect']
        rec = {
            'question_id': qid,
            'layer': 'object',
            'parent_question_id': r['parent_question_id'] or None,
            'parent_relation': r['parent_relation'] or None,
            'object_id': o['object_id'],
            'object': o['label'],
            'object_role': o['role'],
            'object_kind': o['kind'],
            'aspect': aspect,
            'aspect_detail': r['aspect_detail'] or None,
            'question': text,
            'primary_group': primary,
            'secondary_groups': theme_groups(ext, cls, primary),
            'refs': refs,
            'classes': cls,
            'external_domains': ext,
            'known_in_corpus': split_ids(r['known_in_corpus']),
            'corpus_coverage': r['corpus_coverage'],
            'answer_status': r['answer_status'],
            'answer_pointer': r['answer_pointer'] or None,
            'question_origin': 'assistant_derived',
            'author_review': 'none',
            'added': r['added'] or None,
            'revised': r['revised'] or None,
            'previous_question': r['previous_question'] or None,
        }
        obj_records.append(rec)

    # --- ссылки на родителей должны существовать (проверяется и в check.py; здесь — для сборки)
    ids = {r['question_id'] for r in assertion} | {r['question_id'] for r in obj_records}
    for r in assertion + obj_records:
        if r['parent_question_id'] and r['parent_question_id'] not in ids:
            raise ValueError(f'{r["question_id"]}: нет родителя {r["parent_question_id"]}')

    # --- связи с OPEN_QUESTIONS
    xref = I['crossref']
    for r in xref:
        if r['relation'] not in LINK_RELATIONS:
            raise ValueError(f'crossref строка {r["_line"]}: связь {r["relation"]}')
        if r['open_question'] not in oq:
            raise ValueError(f'crossref строка {r["_line"]}: нет пункта {r["open_question"]}')
        if r['question_id'] not in ids:
            raise ValueError(f'crossref строка {r["_line"]}: нет вопроса {r["question_id"]}')
    xref_sorted = sorted(xref, key=lambda r: (r['question_id'], r['open_question']))

    # --- пункты OPEN_QUESTIONS и журнал как вопросы для групп
    oq_items = []
    for k, v in oq.items():
        text = v['text']
        refs = refs_of(text, own_id=None)
        ext = external_of(text)
        cls = classes_of(text)
        g = oqg[k]
        oq_items.append(dict(qid=k, origin='OPEN_QUESTIONS', kind=v['status'], text=text,
                             primary=g['primary_group'], secondary=sorted(set(split_ids(g['secondary_groups']))),
                             src=k, refs=refs, ext=ext, cls=cls, coverage='',
                             section=v['section']))
    dn_items = []
    for k, v in dn.items():
        text = v['title'] + ' ‖ ' + v['open_question']
        refs = refs_of(text)
        ext = external_of(text)
        cls = classes_of(text)
        dn_items.append(dict(qid=k, origin='DIALOGUE_JOURNAL', kind='pending', text=text,
                             primary='G14', secondary=theme_groups(ext, cls, 'G14'), src=k,
                             refs=refs, ext=ext, cls=cls, coverage='', section=''))

    # --- предупреждения (не ошибки): внешние понятия без метки external
    for r in assertion + obj_records:
        if r['external_domains'] and any(e.startswith('анализ') for e in r['external_domains']) \
                and r.get('aspect') != 'external':
            warnings.append(f'{r["question_id"]}: тема «анализ и статистика» без аспекта external — проверить')
    return assertion, obj_records, oq_items, dn_items, xref_sorted, warnings


STOP = {'что', 'как', 'для', 'это', 'при', 'или', 'чем', 'его', 'она', 'они', 'так', 'если', 'где', 'когда',
        'почему', 'какой', 'какая', 'какие', 'каков', 'каковы', 'есть', 'ли', 'все', 'него', 'нет', 'был',
        'the', 'and', 'что', 'который', 'которые', 'также', 'только', 'между', 'после', 'перед', 'одна',
        'один', 'того', 'этого', 'этот', 'эта', 'эти', 'тот', 'та', 'те', 'из', 'без', 'над', 'под'}


def near_duplicates(records):
    """Пары вопросов с совпадением слов >= 0.6 внутри источника и >= 0.8 во всём наборе.

    Совпадение = |A∩B| / min(|A|,|B|) по словам длиной от 3 букв без служебных слов (STOP).
    """
    def toks(t):
        return {w for w in re.findall(r'\w{3,}', t.lower()) if w not in STOP}
    rows = []
    texts = [(r['question_id'], r['question'], r.get('source_id') or r.get('object_id'), r['layer'],
              toks(r['question'])) for r in records]
    seen = set()
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = texts[i], texts[j]
            if a[1] == b[1]:
                raise ValueError(f'точный дубль текста: {a[0]} и {b[0]}')
            if not a[4] or not b[4]:
                continue
            ov = len(a[4] & b[4]) / min(len(a[4]), len(b[4]))
            same_src = a[2] == b[2]
            if (same_src and ov >= 0.6) or ov >= 0.8:
                key = (a[0], b[0])
                if key in seen:
                    continue
                seen.add(key)
                rows.append([a[0], b[0], 'same_source' if same_src else 'global', f'{ov:.2f}', a[1], b[1]])
    return rows


def write_jsonl(path, records):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')


def write_tsv(path, header, rows):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def fmt_list(items, n=8):
    return ', '.join(str(x) for x in items[:n]) or '—'


def write_objects_md(I, obj_records):
    L = ['# Вопросы к объектам: формулы лестницы, операторы и термины\n']
    L.append('Дата: 2026-10-10. Второй слой вопросов (`layer: object`). Первый слой задан к **утверждениям** '
             '(`QUESTION_CARDS.jsonl`, `layer: assertion`); здесь — к **объектам**, о которых утверждения говорят '
             'мимоходом: что это, какие свойства, откуда берётся, почему на этом уровне. Пробел обнаружился на '
             'вопросе «что такое x²?»: прямого вопроса об объекте не было нигде.\n')
    L.append(f'Карточки: [QUESTION_CARDS.jsonl](QUESTION_CARDS.jsonl) (фильтр `layer=object`) и производный файл '
             f'[OBJECT_QUESTION_CARDS.jsonl](OBJECT_QUESTION_CARDS.jsonl). Вопросов {len(obj_records)} к '
             f'{len(I["objects"])} объектам. Вопросы сформулированы ассистентом (`assistant_derived`), ответов нет, '
             'авторской проверки не было.\n')
    L.append('**Что значит покрытие** (`corpus_coverage`). `covered` — в корпусе есть проверка или карточка, отвечающая '
             'на вопрос (источники перечислены); `partial` — ответ есть частично; `open` — ответа нет; '
             '`answered_elsewhere` — ответ в закрытом пункте `OPEN_QUESTIONS.md` (`answer_pointer`); `external` — '
             'понятие вне канона ФТС, не считается пробелом ФТС. Это пометка наличия источника, а не проверка, что '
             'ответ верен и полон.\n')
    L.append('**Решётка аспектов:** ' + ', '.join(LAT_OBJECT) + '. Исходный тип вопроса сохранён в `aspect_detail`.\n')
    L.append('## Сводка\n')
    L.append('| Объект | Роль | Тип | Вопросов | covered | partial | open | answered_elsewhere | external |')
    L.append('|---|---|---|---:|---:|---:|---:|---:|---:|')
    for o in I['objects']:
        rs = [r for r in obj_records if r['object_id'] == o['object_id']]
        c = collections.Counter(r['corpus_coverage'] for r in rs)
        L.append(f"| `{o['label']}` ({o['object_id']}) | {o['role']} | {o['kind']} | {len(rs)} | {c['covered']} | "
                 f"{c['partial']} | {c['open']} | {c['answered_elsewhere']} | {c['external']} |")
    tot = collections.Counter(r['corpus_coverage'] for r in obj_records)
    L.append(f"| **Всего** | | | {len(obj_records)} | {tot['covered']} | {tot['partial']} | {tot['open']} | "
             f"{tot['answered_elsewhere']} | {tot['external']} |\n")
    L.append('## Объекты\n')
    for o in I['objects']:
        rs = [r for r in obj_records if r['object_id'] == o['object_id']]
        L.append(f"### {o['label']} — {o['role']}\n")
        L.append(f"Тип: {o['kind']}. Группа: {o['primary_group']}. Определение: "
                 f"{fmt_list(split_ids(o['defining_cards']), 12)}"
                 + (f" ({o['definition_note']})" if o['definition_note'] else '') + '.\n')
        if not rs:
            L.append('Вопросов пока нет.\n')
            continue
        for i, r in enumerate(rs, 1):
            mark = {'covered': '●', 'partial': '◐', 'open': '○', 'answered_elsewhere': '✓',
                    'external': '◇'}[r['corpus_coverage']]
            src = ', '.join(f'`{k}`' for k in r['known_in_corpus']) or '—'
            par = f" (ветвь {r['parent_question_id']})" if r['parent_question_id'] else ''
            L.append(f"{i}. {mark} **{r['question_id']} · {r['aspect']}.**{par} {r['question']}  \n   "
                     f"Источники: {src}.")
        L.append('')
    L.append('## Что не закрыто\n')
    L.append('- Набор объектов выбран ассистентом: формулы МУ2–МУ13, МУ15, термины и операторы '
             '(Δ, κ, Close, Refuse, Sever, π/ι, Lift, 0_A по уровням). Остальные объекты (p-адические носители, '
             'Window как отдельный оператор, Promote, Unpack, Compress₂/Expand₂) в реестр не входят.')
    L.append('- Аспекты назначены ассистентом по смыслу вопроса; единой процедуры проверки нет.')
    L.append('- Пометка `covered` не проверяет полноту ответа.')
    L.append('- Ответы не писались, статусы канона не менялись, `OPEN_QUESTIONS.md` и канон не изменялись.\n')
    return '\n'.join(L) + '\n'


def write_groups_md(I, assertion, obj_records, oq_items, dn_items, n_dup):
    groups = I['groups']
    all_q = [dict(layer=r['layer'], group=r['primary_group'], coverage=r['corpus_coverage'],
                  refs=r['refs'], secondary=r['secondary_groups'], classes=r['classes'],
                  external=r['external_domains'], qid=r['question_id'], kind=r.get('question_kind') or
                  r.get('aspect'), text=r['question']) for r in assertion + obj_records]
    all_q += [dict(layer=i['origin'], group=i['primary'], coverage='', refs=i['refs'], secondary=i['secondary'],
                   classes=i['cls'], external=i['ext'], qid=i['qid'], kind=i['kind'], text=i['text'])
              for i in oq_items + dn_items]
    L = ['# Группы вопросов проекта и то, на что они ссылаются\n']
    L.append('Дата: 2026-10-10. Источники: `work/OPEN_QUESTIONS.md` (103 пункта), `QUESTION_CARDS.jsonl` '
             f'(вопросы к утверждениям: {len(assertion)}, к объектам: {len(obj_records)}), '
             '`work/DIALOGUE_NUANCE_JOURNAL.md` (пункты с открытым вопросом: '
             f'{len(dn_items)}). Всего вопросов в группах: {len(all_q)}.\n')
    L.append('Основная группа назначена правилом (для утверждений — по семейству источника; для объектов — по '
             'объекту в `inputs/objects.tsv`; для открытых пунктов — вручную в `inputs/oq_groups.tsv`). '
             'Вторичные группы — тематические семейства, которых касается текст вопроса (внешние области, данные, '
             'инфраструктура, решение автора). Ссылки (уровни, карточки, проверки, словарь, критерии, якоря, файлы) '
             'извлечены из текста регулярными выражениями с границами слов; это навигация, а не решение и не '
             'изменение статусов.\n')
    L.append('Построчно: [QUESTION_GROUPS.tsv](QUESTION_GROUPS.tsv). Связи с открытыми пунктами: '
             '[QUESTION_CROSSREF.tsv](QUESTION_CROSSREF.tsv). Почти-дубли для ручного решения: '
             '[DUPLICATE_CANDIDATES.tsv](DUPLICATE_CANDIDATES.tsv).\n')
    L.append('## Сводка\n')
    L.append('| Группа | Всего | Вопросы к утверждениям | Вопросы к объектам | Открытые пункты (откр./част./закр.) | '
             'Вопросы журнала | На что ссылается прежде всего |')
    L.append('|---|---:|---:|---:|---|---:|---|')
    for g in groups:
        gid = g['group_id']
        qs = [q for q in all_q if q['group'] == gid]
        n_a = sum(1 for q in qs if q['layer'] == 'assertion')
        n_o = sum(1 for q in qs if q['layer'] == 'object')
        n_oq = [q for q in qs if q['layer'] == 'OPEN_QUESTIONS']
        st = collections.Counter(q['kind'] for q in n_oq)
        n_dn = sum(1 for q in qs if q['layer'] == 'DIALOGUE_JOURNAL')
        L.append(f"| {gid}. {g['name']} | {len(qs)} | {n_a} | {n_o} | "
                 f"{st.get(' ', 0)}/{st.get('~', 0)}/{st.get('x', 0)} | {n_dn} | {g['points_to'][:90]}… |")
    L.append('')
    for g in groups:
        gid = g['group_id']
        qs = [q for q in all_q if q['group'] == gid]
        sec = [q for q in all_q if gid in q['secondary']]
        L.append(f"## {gid}. {g['name']} — {len(qs)}\n")
        L.append(f"**Критерий включения.** {g['criteria']}\n")
        L.append(f"**О чём спрашивает.** {g['asks']}\n")
        L.append(f"**На что ссылается.** {g['points_to']}\n")
        levels = collections.Counter(x for q in qs for x in q['refs']['levels'])
        checks = collections.Counter(x for q in qs for x in q['refs']['checks'])
        cards = collections.Counter(x for q in qs for x in q['refs']['cards'])
        ext = collections.Counter(x for q in qs for x in q['external'])
        cov = collections.Counter(q['coverage'] for q in qs if q['coverage'])
        L.append('Счётчики: уровни ' + fmt_list([f'У{k} ({v})' for k, v in levels.most_common(8)]) +
                 '; карточки ' + fmt_list([f'{k} ({v})' for k, v in cards.most_common(6)]) +
                 '; проверки ' + fmt_list([f'{k} ({v})' for k, v in checks.most_common(6)]) +
                 '; внешние области ' + fmt_list([f'{k} ({v})' for k, v in ext.most_common(4)]) +
                 f'; покрытие ' + (', '.join(f'{k} {v}' for k, v in sorted(cov.items())) or '—') +
                 f'; вторичная принадлежность: {len(sec)}.\n')
        opn = [q for q in qs if q['layer'] == 'OPEN_QUESTIONS' and q['kind'] != 'x']
        clo = [q for q in qs if q['layer'] == 'OPEN_QUESTIONS' and q['kind'] == 'x']
        if opn:
            L.append('Незакрытые пункты `OPEN_QUESTIONS.md`: ' +
                     ', '.join(f'[`{q["qid"]}`](../../OPEN_QUESTIONS.md#{q["qid"]})' for q in opn) + '.\n')
        if clo:
            L.append('Закрытые: ' + ', '.join(f'`{q["qid"]}`' for q in clo) + '.\n')
        L.append('')
    # --- наблюдения: числа берутся из данных сборки
    by_g = collections.Counter(q['group'] for q in all_q)
    top = by_g.most_common(1)[0]
    low = min(by_g.items(), key=lambda kv: (kv[1], kv[0]))
    opn = collections.Counter(q['group'] for q in all_q if q['coverage'] == 'open')
    ext_n = sum(1 for q in all_q if q['coverage'] == 'external')
    role_children = sum(1 for r in obj_records if r['parent_question_id'] == 'QO-ROLE.1')
    sec_n = sum(1 for q in all_q if q['secondary'])
    L.append('## Наблюдения\n')
    L.append(f'1. **Вопросы распределены неравномерно.** Больше всего в группе {top[0]} ({top[1]}), меньше всего в '
             f'{low[0]} ({low[1]}). Всего вопросов {len(all_q)}: к утверждениям {len(assertion)}, к объектам '
             f'{len(obj_records)}, пунктов OPEN_QUESTIONS {len(oq_items)}, журнал {len(dn_items)}.')
    L.append('2. **Пробелы без ответа в корпусе** (`open`) сильнее всего в группах: ' +
             ', '.join(f'{g} ({n})' for g, n in opn.most_common(4)) + f'. Всего `open`: {sum(opn.values())}.')
    L.append(f'3. **Внешние понятия** (`external`) вынесены из пробелов: {ext_n} вопросов, в том числе гладкость, '
             'дисперсия и сходимость рядов. Они не считаются пробелом ФТС.')
    L.append(f'4. **Роль формы.** {role_children} вопросов о роли форм МУ2…МУ15 сведены к одному мосту '
             '`QO-ROLE.1` (связь `instance`); мост по К1–К5 сам открыт.')
    L.append(f'5. **Вторичные группы** назначены у {sec_n} вопросов из {len(all_q)}: они отражают внешние области, '
             'данные, инфраструктуру или решение автора; основная группа — по семейству источника, объекту или ручной записи.')
    L.append('6. **Почти-дубли** не исправлены: ' + str(n_dup) +
             ' пар в [DUPLICATE_CANDIDATES.tsv](DUPLICATE_CANDIDATES.tsv) ждут решения.\n')
    L.append('## Уже отвечены и устаревшие предпосылки\n')
    for r in assertion + obj_records:
        if r['answer_status'] != 'unanswered' or r.get('premise_note'):
            note = f"; предпосылка: {r['premise_note']}" if r.get('premise_note') else ''
            L.append(f"- `{r['question_id']}` — {r['answer_status']}: {r.get('answer_pointer') or '—'}{note}")
    L.append('')
    L.append('## Что не закрыто\n')
    L.append('- Группы назначены одной основной меткой; вторичные отражают только тематические семейства, '
             'а не полный смысл вопроса.')
    L.append('- Автоматическое извлечение ссылок пропускает упоминания без явного идентификатора и иногда ловит '
             'лишнее; счётчики — ориентир.')
    L.append('- Связи с открытыми пунктами (`QUESTION_CROSSREF.tsv`) собраны вручную по смыслу; полнота не гарантирована.')
    L.append('- Почти-дубли (`DUPLICATE_CANDIDATES.tsv`) не решены; решение о слиянии — за авторской проверкой.')
    L.append('- Ответы не писались, статусы не менялись, `OPEN_QUESTIONS.md` и канон не изменялись.\n')
    return '\n'.join(L) + '\n', all_q


def write_groups_tsv(path, I, assertion, obj_records, oq_items, dn_items):
    gname = {g['group_id']: g['name'] for g in I['groups']}
    header = ['question_id', 'layer_or_origin', 'kind', 'primary_group', 'primary_group_name', 'secondary_groups',
              'source_or_object', 'levels', 'cards', 'checks', 'dict_and_criteria', 'oq_anchors', 'files',
              'external_domains', 'classes', 'corpus_coverage', 'question']
    rows = []
    for r in assertion + obj_records:
        rows.append([r['question_id'], r['layer'], r.get('question_kind') or r.get('aspect'), r['primary_group'],
                     gname[r['primary_group']], ' '.join(r['secondary_groups']),
                     r.get('source_id') or r.get('object_id'), ' '.join(map(str, r['refs']['levels'])),
                     ' '.join(r['refs']['cards']), ' '.join(r['refs']['checks']),
                     ' '.join(r['refs']['dict'] + r['refs']['criteria']), ' '.join(r['refs']['oq']),
                     ' '.join(r['refs']['files']), '; '.join(r['external_domains']), '; '.join(r['classes']),
                     r['corpus_coverage'], r['question']])
    for i in oq_items + dn_items:
        rows.append([i['qid'], i['origin'], i['kind'], i['primary'], gname[i['primary']],
                     ' '.join(i['secondary']), i['src'], ' '.join(map(str, i['refs']['levels'])),
                     ' '.join(i['refs']['cards']), ' '.join(i['refs']['checks']),
                     ' '.join(i['refs']['dict'] + i['refs']['criteria']), ' '.join(i['refs']['oq']),
                     ' '.join(i['refs']['files']), '; '.join(i['ext']), '; '.join(i['cls']), '', i['text']])
    rows.sort(key=lambda x: (x[3], x[1], x[0]))
    write_tsv(path, header, rows)


def main():
    I = load_inputs()
    assertion, obj_records, oq_items, dn_items, xref, warnings = build_records(I)

    # QUESTION_CARDS.jsonl — единый файл; OBJECT_QUESTION_CARDS.jsonl — производный вид
    write_jsonl(CQ / 'QUESTION_CARDS.jsonl', assertion + obj_records)
    write_jsonl(CQ / 'OBJECT_QUESTION_CARDS.jsonl', obj_records)
    (CQ / 'OBJECTS.md').write_text(write_objects_md(I, obj_records), encoding='utf-8', newline='\n')
    dup = near_duplicates(assertion + obj_records)
    md, _ = write_groups_md(I, assertion, obj_records, oq_items, dn_items, len(dup))
    (CQ / 'QUESTION_GROUPS.md').write_text(md, encoding='utf-8', newline='\n')
    write_groups_tsv(CQ / 'QUESTION_GROUPS.tsv', I, assertion, obj_records, oq_items, dn_items)
    write_tsv(CQ / 'QUESTION_CROSSREF.tsv', CROSSREF_HEADER,
              [[r['question_id'], r['open_question'], r['relation'], r['note']] for r in xref])
    write_tsv(CQ / 'DUPLICATE_CANDIDATES.tsv',
              ['question_a', 'question_b', 'scope', 'overlap', 'text_a', 'text_b'], dup)

    print(f'утверждения: {len(assertion)}; объекты: {len(obj_records)}; пункты OQ: {len(oq_items)}; '
          f'журнал: {len(dn_items)}; связи: {len(xref)}; почти-дубли: {len(dup)}')
    for w in warnings:
        print('ПРЕДУПРЕЖДЕНИЕ:', w)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
