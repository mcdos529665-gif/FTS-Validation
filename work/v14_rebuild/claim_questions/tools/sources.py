"""Снимок источников для слоя вопросов (только чтение; канон не меняется).

Что читается:
- source/fts_cards.jsonl — карточки канона (172);
- work/v14_rebuild/claim_graph/claim_graph.json — узлы claim, claim_group, finding, pattern
  (37 + 25 + 20 + 31 = 113 утверждений исследовательского и аудитного слоя) и полные тексты
  из RESEARCH_CLAIMS.tsv;
- проверки C-NN и G60-NN: разбор AST вызовов check(...) во всех verification*.py под work/v14_rebuild;
- пункты work/OPEN_QUESTIONS.md (строки «- [s] текст {#oq-…}», s ∈ {' ', 'x', '~'});
- DN-пункты work/DIALOGUE_NUANCE_JOURNAL.md с полем open_question.

Запуск: py -3.11 -X utf8 sources.py  — печатает сводку счётчиков.
"""
import ast
import json
import pathlib
import re
import sys

TOOLS = pathlib.Path(__file__).resolve().parent
CQ = TOOLS.parent                      # claim_questions/
ROOT = pathlib.Path(__file__).resolve().parents[4]   # корень репозитория
GRAPH = ROOT / 'work/v14_rebuild/claim_graph/claim_graph.json'
RESEARCH = ROOT / 'work/v14_rebuild/claim_graph/RESEARCH_CLAIMS.tsv'
CARDS = ROOT / 'source/fts_cards.jsonl'
OQ_FILE = ROOT / 'work/OPEN_QUESTIONS.md'
JOURNAL = ROOT / 'work/DIALOGUE_NUANCE_JOURNAL.md'
VERIF_DIR = ROOT / 'work/v14_rebuild'


def cards():
    """id -> dict(status, text) для карточек канона."""
    out = {}
    for line in CARDS.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        c = json.loads(line)
        out[c['id']] = dict(status=c.get('status', ''), text=c.get('text', ''))
    return out


def graph_assertions():
    """Утверждения исследовательского и аудитного слоя из claim_graph.json.

    Возвращает список dict: source_kind, source_id, source_status, source_text,
    и по возможности source_verdict, source_resolution, source_unresolved.
    """
    g = json.load(open(GRAPH, encoding='utf-8'))
    research = {}
    for row in RESEARCH.read_text(encoding='utf-8').splitlines()[1:]:
        if row.strip():
            parts = row.split('\t')
            research[parts[0]] = parts[1]
    out = []
    for n in g['nodes']:
        t = n.get('type')
        if t == 'claim':
            cid = n['claim_id']
            out.append(dict(source_kind='claim', source_id=cid, source_status=n['status_text'],
                            source_text=research[cid]))
        elif t == 'claim_group':
            out.append(dict(source_kind='claim_group', source_id=n['claim_id'],
                            source_status=n['verdict'], source_text=n['label'],
                            source_verdict=n['verdict'], source_resolution=n['resolution']))
        elif t == 'finding':
            out.append(dict(source_kind='finding', source_id=n['finding_id'],
                            source_status=n['finding_status'], source_text=n['conclusion'],
                            source_verdict=n['conclusion'], source_unresolved=n['unresolved']))
        elif t == 'pattern':
            out.append(dict(source_kind='pattern', source_id=n['pattern_id'],
                            source_status=n['verdict'], source_text=n['statement'],
                            source_verdict=n['verdict']))
    return out


def card_assertions():
    """Карточки канона как утверждения (172)."""
    return [dict(source_kind='card', source_id=k, source_status=v['status'], source_text=v['text'])
            for k, v in cards().items()]


def normalize_check_id(raw):
    m = re.fullmatch(r'C(\d+)', raw)
    if m:
        return 'C-' + m.group(1)
    return raw


def checks():
    """Проверки C-NN и G60-NN: id -> dict(file, text). Разбор AST вызовов check(...)."""
    out = {}
    files = sorted(p for p in VERIF_DIR.rglob('verification*.py') if '__pycache__' not in p.parts)
    for path in files:
        tree = ast.parse(path.read_text(encoding='utf-8'))
        rel = path.relative_to(ROOT).as_posix()

        def visit(node, func_doc):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    visit(child, ast.get_docstring(child))
                    continue
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) \
                        and child.func.id == 'check' and child.args \
                        and isinstance(child.args[0], ast.Constant) \
                        and isinstance(child.args[0].value, str) \
                        and re.fullmatch(r'C\d+|G60-\d+', child.args[0].value):
                    cid = normalize_check_id(child.args[0].value)
                    desc = None
                    if len(child.args) >= 2 and isinstance(child.args[1], ast.Constant) \
                            and isinstance(child.args[1].value, str):
                        desc = child.args[1].value
                    elif func_doc:
                        desc = func_doc.strip().splitlines()[0]
                    if cid in out:
                        raise ValueError(f'дубль проверки {cid}: {out[cid]["file"]} и {rel}')
                    out[cid] = dict(file=rel, text=(desc or '').strip())
                visit(child, func_doc)

        visit(tree, None)
    return out


def open_questions():
    """Пункты OPEN_QUESTIONS.md: id -> dict(status, text, section)."""
    out = {}
    section = '(начало)'
    pat = re.compile(r'^- \[([ x~])\] (.*?)\s*\{#(oq-[\w-]+)\}\s*$')
    for line in OQ_FILE.read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            section = line[3:].strip()
            continue
        m = pat.match(line)
        if m:
            if m.group(3) in out:
                raise ValueError(f'дубль якоря {m.group(3)}')
            out[m.group(3)] = dict(status=m.group(1), text=m.group(2).strip(), section=section)
    return out


def journal_questions():
    """DN-пункты журнала с непустым open_question: id -> dict(title, open_question)."""
    txt = JOURNAL.read_text(encoding='utf-8')
    out = {}
    for m in re.finditer(r'## (DN-\d+) · (.+?)\n(.*?)(?=\n## DN-|\Z)', txt, re.S):
        oq = re.search(r'open_question: (.+)', m.group(3))
        if oq and oq.group(1).strip() != 'none':
            out[m.group(1)] = dict(title=m.group(2).strip(), open_question=oq.group(1).strip())
    return out


def all_registry():
    """Все реестры в одном словаре (для проверки ссылок)."""
    cs = cards()
    oq = open_questions()
    ck = checks()
    return dict(cards=cs, open_questions=oq, checks=ck, journal=journal_questions())


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    ga = graph_assertions()
    ca = card_assertions()
    ck = checks()
    oq = open_questions()
    jq = journal_questions()
    print('карточки канона:', len(ca))
    print('утверждения графа (claim/claim_group/finding/pattern):', len(ga))
    print('проверки (C-NN и G60-NN):', len(ck), 'из файлов:', len({v['file'] for v in ck.values()}))
    print('пункты OPEN_QUESTIONS:', len(oq))
    print('DN с открытым вопросом:', len(jq))
