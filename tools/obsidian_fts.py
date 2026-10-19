"""Deterministic, source-grounded FTS Obsidian export; stdlib only.

Preview by default; --write applies a checked export; --check verifies a vault.
The canonical graph remains authoritative. No semantic promotion takes place.
"""
from __future__ import annotations

import argparse
import ast
import csv
from collections import defaultdict, deque
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote, unquote
from obsidian_fts_corpus import Corpus, CORPUS_INDEX, COVERAGE
from obsidian_fts_registry import INDEX as RESEARCH_INDEX, blocks

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VAULT = Path('E:/projects/Obsidian/FTS')
PACKAGE = 'work/v14_rebuild/obsidian_encyclopedia'
GRAPH = 'work/v14_rebuild/claim_graph/claim_graph.json'
MANIFEST = '90 — Служебное/manifest.json'
VERSION = '1.2'
FOLDERS = [
    '00 — Начало', '01 — ФТС в целом', '02 — Уровни',
    '03 — Сущности и свойства', '04 — Операции и связи',
    '05 — Окна и структуры', '06 — Модели и исследования',
    '07 — Основания и проверки', '08 — Мои заметки', '90 — Служебное',
]
HOME = FOLDERS[0] + '/Начать здесь.md'
RULES = FOLDERS[0] + '/Правила базы.md'
STATUS_PAGE = FOLDERS[9] + '/Оценки статусов.md'
LITERAL_PAGE = FOLDERS[9] + '/Значения и ссылки.md'
SOURCE_INDEX = FOLDERS[7] + '/Документы проекта.md'
TYPES = {
    'level': 'Семантический уровень', 'minimal_expression': 'Минимальное логическое выражение',
    'private_expression': 'Операциональное чтение', 'mathematical_expression': 'Математическое представление',
    'operator': 'Оператор', 'operator_candidate': 'Кандидат оператора',
    'connectivity_ground': 'Основание связности', 'axiom': 'Аксиоматическое положение',
    'definition': 'Определение', 'research_proposal': 'Исследовательское предложение',
    'complex_analog': 'Комплексный аналог', 'statistical_analog': 'Статистический аналог',
    'tensor_analog': 'Тензорный аналог', 'overlay': 'Оверлей', 'candidate_overlay': 'Кандидатный оверлей',
    'window_family': 'Семейство окон', 'window_grouping': 'Группировка окон',
    'window_family_statement': 'Положение о семействах окон',
    'card': 'Карточка авторского пакета', 'claim': 'Исследовательское утверждение',
    'open_question': 'Открытый или ранее поставленный вопрос', 'verification': 'Проверка',
    'source_document': 'Документ-источник', 'external_evidence': 'Внешнее свидетельство',
    'internal_evidence': 'Внутреннее свидетельство', 'finding': 'Результат исследования',
    'constraint': 'Ограничение', 'pattern': 'Закономерность', 'claim_group': 'Группа утверждений',
    'author_statement': 'Авторское положение', 'open_obligation': 'Незакрытое обязательство',
    'program': 'Исследовательская программа', 'scope': 'Область исследования',
    'project': 'Проект ФТС', 'meta_pattern': 'Группа закономерностей',
    'event': 'Исследовательское событие', 'unresolved_reference': 'Неразрешённая ссылка',
    'source_fragment': 'Фрагмент источника', 'source_reference': 'Ссылка на источник',
    'anti_mode': 'Антимода', 'boundary': 'Граница', 'rule': 'Правило',
    'status_promotion': 'Условие повышения статуса', 'failure_condition': 'Условие поражения',
    'test': 'Тест', 'logical_supplement': 'Логическое дополнение',
    'formalization_proposal': 'Предложение формализации', 'notation_rule': 'Правило обозначений',
    'guardrail': 'Ограничивающее правило', 'author_decision': 'Авторское решение',
    'alignment_note': 'Согласование представлений', 'research_index': 'Указатель исследований',
    'candidate_bundle': 'Пакет кандидатов', 'export_instruction': 'Инструкция экспорта',
    'boundary_candidate': 'Кандидат границы', 'topology_candidate': 'Топологический кандидат',
    'invariant_candidate': 'Кандидат инварианта', 'hypothesis_candidate': 'Кандидат гипотезы',
    'classification_candidate': 'Кандидат классификации', 'level_variant_candidate': 'Кандидат варианта уровня',
    'level_candidate': 'Кандидат уровня',
}
REL = {
    'depends_on': 'зависит от', 'contains': 'содержит', 'grounds_claim': 'обосновывает утверждение',
    'verified_by': 'проверяется посредством', 'supported_by': 'поддерживается свидетельством',
    'supports': 'поддерживает', 'limited_by': 'ограничивается', 'documented_in': 'описано в',
    'has_status': 'имеет оценку статуса', 'has_status_before': 'имело оценку статуса',
    'has_status_after': 'получило оценку статуса', 'has_next': 'имеет следующий уровень',
    'has_minimal_expression': 'имеет минимальное выражение', 'has_private_expression': 'имеет операциональное чтение',
    'has_math_expression': 'имеет математическое представление', 'has_window': 'имеет окно',
    'has_operator': 'связано с оператором', 'has_local_forbid': 'имеет локальный запрет',
    'has_antimode': 'имеет антимоду', 'has_family': 'имеет семейство',
    'uses_analogy': 'использует аналогию', 'projects_to': 'проецируется в',
    'curated_bridge_to': 'связано исследовательским мостом с', 'adopts': 'принимает',
    'opens_question': 'открывает вопрос', 'has_open_obligation': 'имеет незакрытое обязательство',
    'addresses_object': 'относится к объекту', 'maps_to': 'сопоставлено с',
    'references_evidence': 'ссылается на свидетельство', 'references_document': 'ссылается на документ',
    'has_complex_overlay': 'имеет комплексный оверлей', 'has_statistical_overlay': 'имеет статистический оверлей',
    'has_tensor_overlay': 'имеет тензорный оверлей', 'uses_carrier': 'использует носитель',
    'candidate_supports': 'предлагает кандидатную поддержку', 'tracks_question': 'отслеживает вопрос',
    'audits_claim': 'проверяет утверждение', 'contrasts_with': 'сопоставляется по различию с',
    'navigation_support_for': 'помогает навигации к', 'indexes_claim': 'индексирует утверждение',
    'has_research_scope': 'имеет область исследования', 'requires': 'требует',
    'applies_to': 'применяется к', 'refined_by': 'уточняется посредством',
}
LABELS = {
    'symbol': 'Обозначение', 'title': 'Название', 'type': 'Тип', 'register': 'Регистр',
    'scope': 'Область действия', 'domain': 'Область модели', 'statement': 'Формулировка',
    'question': 'Вопрос', 'conclusion': 'Вывод источника', 'limitation': 'Ограничение',
    'next_step': 'Следующий шаг', 'verdict': 'Оценка источника', 'text': 'Точная запись',
    'local_forbid': 'Локальный запрет', 'mathematical_scope': 'Математическая область',
    'levels': 'Адресованные уровни', 'window_length': 'Длина окна', 'windows': 'Окна',
    'canonical_membership': 'Каноническое включение', 'status': 'Статус записи',
    'St_FTS': 'Доказательный статус ФТС', 'evidence_status': 'Статус свидетельств',
    'author_status': 'Авторское принятие', 'status_axis': 'Ось статуса',
    'status_effect': 'Влияние на статус', 'status_text': 'Текст оценки статуса',
    'adoption_scope': 'Область принятия', 'revision_condition': 'Условие пересмотра',
    'oq_status': 'Состояние вопроса', 'evidence_kind': 'Тип свидетельства',
    'evidence_level': 'Уровень свидетельств', 'formulation_origin': 'Происхождение формулировки',
}


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def sha(value):
    if isinstance(value, str): value = value.encode('utf-8')
    return hashlib.sha256(value).hexdigest()


def slug(s):
    s = re.sub(r'[<>:"/\\|?*\[\]#^\x00-\x1f]', ' ', str(s))
    return re.sub(r'\s+', ' ', s).strip(' .')[:95] or 'Без названия'


def cell(v):
    if not isinstance(v, str): v = json.dumps(v, ensure_ascii=False)
    return v.replace('|', '&#124;').replace('[', '&#91;').replace(']', '&#93;').replace('\n', '<br>')


def fenced(s, language='text'):
    fence = '`' * max(3, max((len(m.group()) + 1 for m in re.finditer(r'`+', s)), default=3))
    return f'{fence}{language}\n{s}\n{fence}\n'


def link(target, label=None):
    target = target.replace('.md#', '#')
    if target.endswith('.md'): target = target[:-3]
    return f'[[{target}|{slug(label or target.split("/")[-1])}]]'


def frontmatter(id_, aliases, type_):
    return '\n'.join(['---', 'fts_id: ' + json.dumps(id_, ensure_ascii=False),
                      'type: ' + json.dumps(type_, ensure_ascii=False),
                      'aliases: ' + json.dumps(list(dict.fromkeys(a for a in aliases if a)), ensure_ascii=False),
                      'generated: true', '---', '']) + '\n'


class Encyclopedia:
    def __init__(self, root: Path, previous_mapping=None):
        self.root = root
        self.graph = json.loads((root / GRAPH).read_text(encoding='utf-8'))
        self.cards = [json.loads(x) for x in (root / 'source/fts_cards.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
        self.card_by_id = {c['id']: c for c in self.cards}
        self.nodes = {n['id']: n for n in self.graph['nodes']}
        self.outgoing = defaultdict(list)
        self.incoming = defaultdict(list)
        for e in self.graph['edges']:
            self.outgoing[e['source']].append(e)
            self.incoming[e['target']].append(e)
        self.editorial = json.loads((root / PACKAGE / 'editorial.json').read_text(encoding='utf-8'))
        self.manifest_source = json.loads((root / 'source/MANIFEST.json').read_text(encoding='utf-8'))
        self.paths = {}
        self.files = {}
        self.inputs = {}
        self.source_cache = {}
        self.missing_sources = set()
        self.stale_editorial = []
        self.sections = defaultdict(list)
        self.claim_records = {}
        registry_path = 'work/v14_rebuild/claim_graph/RESEARCH_CLAIMS.tsv'
        self.source(registry_path)
        for row in csv.DictReader(self.source_cache[(root/registry_path).resolve()].splitlines(), delimiter='\t'):
            self.claim_records[row['claim_id']] = row
        for n in self.nodes.values():
            if n['type'] == 'status_assessment':
                path = STATUS_PAGE + '#' + n['id']
            elif n['type'] in ('literal', 'source_reference', 'unresolved_reference'):
                path = LITERAL_PAGE + '#' + n['id']
            else:
                c = self.card_for(n)
                folder = self.folder_for(c.get('type', n['type']))
                id_ = c.get('id', n['id'])
                name = c.get('title') or TYPES.get(n['type'], 'Запись ФТС') + ' — ' + n.get('label', id_)
                safe_id = slug(id_)
                if len(id_)>60: safe_id=safe_id[:60]+'-'+sha(id_)[:10]
                path = f'{FOLDERS[folder]}/{safe_id} — {slug(name)[:80].rstrip(" .")}.md'
                self.sections[folder].append((path, name))
            # Keep published addresses stable even when a title or category changes.
            if previous_mapping and n['id'] in previous_mapping:
                previous_path = previous_mapping[n['id']]
                if bool('#' in previous_path) != bool('#' in path):
                    raise ValueError('Node representation changed; explicit migration required: '+n['id'])
                path = previous_path
                if '#' not in path:
                    self.sections[folder][-1] = (path, name)
            self.paths[n['id']] = path
        for c in self.cards:
            matches = [n for n in self.nodes.values() if n.get('card_id') == c['id'] and n.get('source_file') == 'source/fts_cards.jsonl']
            if len(matches) != 1: raise ValueError(f'Card mapping is not unique: {c["id"]}')
        if len(set(p.casefold() for p in self.paths.values() if '#' not in p)) != sum('#' not in p for p in self.paths.values()):
            raise ValueError('Duplicate page path')
        self.corpus = Corpus(self)

    def card_for(self, n):
        if n.get('source_file') == 'source/fts_cards.jsonl':
            return self.card_by_id.get(n.get('card_id'), {})
        return {}

    @staticmethod
    def folder_for(t):
        if t in ('level', 'minimal_expression', 'private_expression', 'mathematical_expression'): return 2
        if t in ('operator', 'operator_candidate'): return 4
        if t.startswith('window_'): return 5
        if t in ('axiom', 'connectivity_ground', 'project', 'scope', 'logical_supplement'): return 1
        if t in ('definition', 'anti_mode', 'boundary', 'rule', 'notation_rule', 'guardrail'): return 3
        if t in ('verification', 'internal_evidence', 'external_evidence', 'open_question', 'open_obligation', 'source_document', 'source_fragment', 'status_promotion', 'failure_condition', 'test'): return 7
        return 6

    def source(self, path, location=''):
        if not path: return 'нет в артефактах'
        p = (self.root / path).resolve()
        if not p.is_file():
            self.missing_sources.add(path)
            return f'Источник недоступен: `{cell(path)}`; место: `{cell(location)}`'
        if p not in self.source_cache:
            self.inputs[p.relative_to(self.root).as_posix()] = sha(p.read_bytes())
            try: self.source_cache[p] = p.read_text(encoding='utf-8-sig')
            except UnicodeError: self.source_cache[p] = ''
        return f'[Открыть источник]({p.as_uri()}) — `{cell(path)}`' + (f', `{cell(location)}`' if location else '')

    def excerpt(self, n):
        path = n.get('source_file', '')
        self.source(path, n.get('source_location', ''))
        p = (self.root / path).resolve()
        text = self.source_cache.get(p, '')
        if not text: return ''
        loc = n.get('source_location', '')
        lines = text.splitlines()
        m = re.fullmatch(r'L(\d+)(?:[-–]L?(\d+))?', loc)
        if m:
            start = max(0, int(m[1]) - 1)
            if p.suffix == '.py':
                try:
                    funcs = [x for x in ast.walk(ast.parse(text)) if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.lineno <= start+1 <= x.end_lineno]
                    if funcs:
                        f = min(funcs, key=lambda x: x.end_lineno - x.lineno)
                        return '\n'.join(lines[f.lineno-1:f.end_lineno])
                except SyntaxError: pass
            end = int(m[2]) if m[2] else min(len(lines), start+18)
            return '\n'.join(lines[start:end])
        if loc.startswith('row:') and p.suffix == '.tsv':
            row = int(loc.split(':')[1])
            return '\n'.join([lines[0]] + lines[max(1,row-1):row])
        anchor = n.get('anchor', '')
        if anchor:
            idx = next((i for i,l in enumerate(lines) if f'id="{anchor}"' in l or f"id='{anchor}'" in l), None)
            if idx is not None:
                end = next((j for j in range(idx+2,len(lines)) if lines[j].startswith('<a id=') or lines[j].startswith('## ')), min(len(lines),idx+60))
                return '\n'.join(lines[idx:end])
        for key in ('claim_id', 'pattern_id', 'finding_id', 'evidence_id'):
            term = n.get(key)
            if term and p.suffix == '.tsv':
                selected = [l for l in lines[1:] if term in l.split('\t')]
                if selected: return '\n'.join([lines[0]] + selected)
        if p.suffix=='.json' and loc:
            try:
                obj=json.loads(text)
                def find(value):
                    if isinstance(value,dict):
                        if loc in [v for v in value.values() if isinstance(v,str)]: return value
                        for v in value.values():
                            result=find(v)
                            if result is not None: return result
                    elif isinstance(value,list):
                        for v in value:
                            result=find(v)
                            if result is not None: return result
                found=find(obj)
                if found is not None: return dump(found)
            except json.JSONDecodeError: pass
        terms=re.findall(r'DN-\d{4}',loc)
        snippets=[]
        for term in terms:
            idx=next((i for i,l in enumerate(lines) if l.startswith('#') and term in l),None)
            if idx is not None:
                end=next((j for j in range(idx+1,len(lines)) if lines[j].startswith('#')),min(len(lines),idx+50))
                snippets.append('\n'.join(lines[idx:end]))
        if snippets: return '\n\n'.join(snippets)
        # Exact source opening; explicitly context, not an asserted definition.
        if n['type'] == 'source_document': return '\n'.join(lines[:30])
        return ''

    def nl(self, id_):
        n = self.nodes[id_]
        c = self.card_for(n)
        return link(self.paths[id_], c.get('title') or n.get('label') or id_)

    def status(self, record):
        fields = ['canonical_membership', 'status', 'author_status', 'St_FTS', 'evidence_status', 'status_axis', 'status_text', 'oq_status', 'evidence_kind', 'status_effect', 'adoption_scope', 'revision_condition']
        rows = ['| Ось / условие | Записанное значение |', '|---|---|']
        rows.extend(f'| {LABELS.get(k,k)} | {cell(record.get(k,"не указано"))} |' for k in fields)
        rows += ['| Математическое доказательство | Только по связанным свидетельствам; общий вывод не присваивается. |',
                 '| Эмпирическая поддержка | Только по связанным свидетельствам; при отсутствии — не указано. |']
        return '\n'.join(rows) + '\n'

    def relationships(self, id_):
        lines = ['| Откуда | Отношение | Куда | Область и происхождение | Основание |', '|---|---|---|---|---|']
        for e in self.outgoing[id_] + self.incoming[id_]:
            relation = REL.get(e['relation'], 'Связь источника') + f' (`{e["relation"]}`)'
            info = '; '.join(str(e[k]) for k in ('scope', 'confidence', 'layer', 'status_effect', 'rationale') if e.get(k))
            basis = self.source(e.get('source_file'), e.get('source_location', ''))
            lines.append(f'| {self.nl(e["source"])} | {relation} | {self.nl(e["target"])} | {cell(info) or "не указано"} | {basis} |')
        return '\n'.join(lines) + '\n' if len(lines)>2 else 'Связи в графе не зарегистрированы.\n'

    def page(self, n):
        c = self.card_for(n)
        record = c or {**self.claim_records.get(n.get('claim_id'),{}), **n}
        id_ = c.get('id', n['id'])
        title = c.get('title') or n.get('label', id_)
        type_ = c.get('type', n['type'])
        basis = self.source(n.get('source_file'), n.get('source_location', ''))
        ed = self.editorial.get(id_, {})
        valid_ed = ed.get('source_sha256') == sha(dump(record))
        if ed and not valid_ed: self.stale_editorial.append(id_)
        intro = ed.get('intro_ru') if valid_ed else None
        intro_facet = None
        entries = self.corpus.by_entity.get(id_,[])
        if not intro:
            intro_facet = next((f for f in entries if f['id'].startswith(('P_CARD_EXPLAIN_','P_CP_ROW_','P_CP_ACCEPTED_'))),None)
            if intro_facet:
                target=self.corpus.source_target(intro_facet)
                origin=link(target,'Основание пояснения') if target else self.source(intro_facet['source_file'])
                intro=intro_facet['summary_ru']+'\n\n**Область пояснения:** '+intro_facet['scope_ru']+'\n\n**Статус пояснения:** '+intro_facet['status_ru']+'\n\n'+origin
            else:
                intro = f'{TYPES.get(type_, "Сущность ФТС")}: {title}. Ниже приведены точная запись и зарегистрированные свойства; пояснение не расширяет их область действия.'
        example = ed.get('example_ru') if valid_ed else None
        if not example:
            item=next((f for f in entries if f['kind']=='example'),None)
            if item:
                target=self.corpus.source_target(item)
                origin=link(target,'Основание примера') if target else self.source(item['source_file'])
                example=item['summary_ru']+'\n\n**Область примера:** '+item['scope_ru']+'\n\n**Статус примера:** '+item['status_ru']+'\n\n'+origin
            else:
                example='Отдельный пример пока не подтверждён адресной записью проверенного слоя. Полнота разбора источников показана в разделе «Разбор материалов work»; связи и свойства доступны ниже.'
        exact = record.get('text') or record.get('statement') or record.get('question') or record.get('conclusion')
        if not exact and n['type'] not in ('verification', 'source_document'):
            exact = 'Самостоятельное определение: нет в артефактах. Название и характеристики сохранены из записи графа.'
        lines = [frontmatter(id_, [id_,n['id'],title,c.get('symbol','')], type_), f'# {title}',
                 link(HOME,'Главная') + ' · ' + link(FOLDERS[self.folder_for(type_)]+'/Обзор.md','Раздел'),
                 '## Что это', intro,
                 '## Место в ФТС', f'- Тип: **{TYPES.get(type_, type_)}** (`{type_}`).',
                 f'- Слой источника: `{n.get("layer", "не указано")}`.',
                 f'- Регистр: `{c.get("register", {"minimal_expression":"M / ЛУ", "private_expression":"Ch / операциональное чтение", "mathematical_expression":"A / МУ", "level":"СУ"}.get(type_,"не указано"))}`.',
                 '- Адресованные уровни: ' + cell(c.get('levels', n.get('scope', 'не указано; см. адресные связи ниже'))),
                 '## Определение и точная запись']
        if exact: lines += [fenced(exact)]
        excerpt = self.excerpt(n)
        if excerpt and not c:
            lines += ['### Фрагмент источника', 'Дословный контекст источника; границы фрагмента не заменяют область утверждения.', fenced(excerpt, 'python' if str(n.get('source_file','')).endswith('.py') else 'text')]
        if c.get('symbol'):
            lines += ['### Обозначение', fenced(c['symbol'])]
            # The raw original is preserved above. Only known math forms get a display copy.
            if id_ == 'A_07': lines += ['Отображение действующей математической формы:', '$$\n|y|=x*x\n$$', 'Логическая форма и операциональное чтение имеют собственные основания.']
        lines += ['## Свойства', '| Свойство | Формулировка | Область действия | Основание | Статус |', '|---|---|---|---|---|']
        omit = {'id','title','text','label','tags','path','depends_on','source_file','source_location'}
        props = [(k,v) for k,v in record.items() if k not in omit]
        # These properties are literal labelled fields embedded in level text.
        for pattern, label in [(r'Carrier=([^;\n]+)', 'Носитель из карточки'), (r'window=(\([^)]*\))', 'Окно из карточки')]:
            found = re.search(pattern, c.get('text',''))
            if found:
                lines.append(f'| {label} | {cell(found[1])} | Только область этой записи | {basis} | {cell(c.get("evidence_status",c.get("status","не указано")))} |')
        for k,v in props:
            lines.append(f'| {LABELS.get(k,k)} | {cell(v)} | {cell(record.get("mathematical_scope",record.get("scope",record.get("adoption_scope","не указано отдельно"))))} | {basis} | {cell(record.get("evidence_status",record.get("status_text",record.get("status","не указано"))))} |')
        lines += ['## Связи', self.relationships(n['id']), '## Пример и чтение',
                  example,
                  '## Ограничения и различия',
                  ed.get('caution_ru','Область определяется источником. Связь и соседство страниц сами по себе не доказывают тождество, наследование или повышение статуса.') if valid_ed else 'Область определяется источником. Соседство страниц не доказывает тождество, наследование или повышение статуса.']
        for k in ('limitation','revision_condition','open_obligations','open_questions','local_forbid','notes'):
            if record.get(k): lines += [f'**{LABELS.get(k,k)}:** {cell(record[k])}']
        if ed and not valid_ed: lines += ['> Пояснение требует пересмотра: источник изменился. Прежний редакторский текст не используется как действующее объяснение.']
        lines += ['## Основания и статус', basis, self.status(record),
                  'Отметка `canonical_adopted` не означает завершённого доказательства. Проверка математического предиката не повышает `St_FTS` автоматически.',
                  '## Связанные исследования и мои заметки',
                  'Исследования, вопросы и свидетельства перечислены в таблице направленных связей.',
                  link(FOLDERS[8]+'/Как вести мои заметки.md','Как добавить собственную заметку'),
                  f'Для комментария создайте файл в «08 — Мои заметки» и добавьте ссылку {link(self.paths[n["id"]],title)}. Он появится в обратных ссылках этой страницы.',
                  '## Происхождение', f'- ID графа: `{n["id"]}`.', f'- Редакторское пояснение: {"проверенный пересказ составителя, привязанный к хэшу источника" if (valid_ed or intro_facet) else "структурная справка; точный текст приведён выше"}.',
                  '### Полная исходная запись', fenced(dump(record).rstrip(),'json')]
        expansion = self.corpus.render_facets(id_, link, cell, fenced)
        if expansion:
            pos = lines.index('## Происхождение')
            lines.insert(pos, expansion)
        return blocks(lines)

    def add_documents(self):
        text = (self.root / 'work/DOCUMENT_MAP.md').read_text(encoding='utf-8')
        paths = set()
        for match in re.finditer(r'\]\(([^)]+)\)', text):
            rel = unquote(match[1]).split('#')[0]
            if not rel or '://' in rel: continue
            p = (self.root / 'work' / rel).resolve()
            if p.is_file() and p.is_relative_to(self.root): paths.add(p.relative_to(self.root).as_posix())
        known = {n.get('source_file'): n for n in self.nodes.values() if n['type']=='source_document'}
        lines = ['# Документы проекта', link(HOME,'Главная'), 'Документы из карты проекта, включая материалы вне графа. Исторические документы остаются адресными источниками и не объявляются действующим каноном.', '| Документ | Представление |', '|---|---|']
        for path in sorted(paths):
            source = self.source(path)
            if path in known: dest = self.nl(known[path]['id'])
            else:
                name = 'docmap_' + sha(path)[:12]
                page = FOLDERS[7] + '/' + name + ' — ' + slug(Path(path).stem) + '.md'
                dest = link(page, Path(path).stem)
                text_ = self.source_cache[(self.root/path).resolve()]
                self.files[page] = f'# Документ — {Path(path).stem}\n\n{link(SOURCE_INDEX,"Документы проекта")}\n\n{source}\n\nЗапись указателя; источник вне отдельного узла графа.\n\n## Начало документа\n\n' + fenced('\n'.join(text_.splitlines()[:35]))
            lines.append(f'| {source} | {dest} |')
        self.files[SOURCE_INDEX] = '\n\n'.join(lines[:3]) + '\n\n' + '\n'.join(lines[3:]) + '\n'

    def build(self):
        self.corpus_summary = self.corpus.build(link, cell, fenced, frontmatter)
        for n in self.nodes.values():
            dest = self.paths[n['id']]
            if '#' not in dest: self.files[dest] = self.page(n)
        for kind, page in [('status_assessment', STATUS_PAGE), ('literal', LITERAL_PAGE)]:
            lines = ['# ' + Path(page).stem, link(HOME,'Главная')]
            kinds = {kind} if kind=='status_assessment' else {'literal','source_reference','unresolved_reference'}
            for n in self.nodes.values():
                if n['type'] not in kinds: continue
                lines += [f'## {n["id"]}', n.get('label',''), self.source(n.get('source_file'),n.get('source_location','')),
                          self.status(n) if kind=='status_assessment' else fenced(dump(n).rstrip(),'json')]
                related = self.incoming[n['id']] + self.outgoing[n['id']]
                lines += ['Связанные записи: ' + ', '.join(self.nl(e['source'] if e['target']==n['id'] else e['target']) for e in related)]
            self.files[page] = '\n\n'.join(lines) + '\n'
        self.add_documents()
        self.level_pages()
        for idx, entries in self.sections.items():
            overview = FOLDERS[idx] + '/Обзор.md'
            intro = ['# ' + FOLDERS[idx].split(' — ',1)[1], link(HOME,'Главная'), 'Расположение в разделе служит навигации; типы связей и статусы указаны в самих карточках.']
            if idx==2: intro += [link(FOLDERS[2]+'/Лестница уровней.md','Обзор лестницы и уровней')]
            intro += ['- ' + link(p, name) for p,name in sorted(entries,key=lambda x:x[1].casefold())]
            self.files[overview] = '\n\n'.join(intro) + '\n'
        self.files[RULES] = (self.root / PACKAGE / 'RULES.md').read_text(encoding='utf-8')
        self.files[FOLDERS[0]+'/Обозначения.md'] = '# Обозначения ФТС\n\n' + link(HOME,'Главная') + '\n\n' + self.source('work/notation.md') + '\n\n' + (self.root/'work/notation.md').read_text(encoding='utf-8')
        # Rebase ordinary relative source links, so the copied glossary works in a separate vault.
        glossary = FOLDERS[0]+'/Обозначения.md'
        def rebase(m):
            target=m[2]
            if '://' in target or target.startswith('#'): return m[0]
            path, _, anchor=target.partition('#')
            p=(self.root/'work'/unquote(path)).resolve()
            if not p.is_file(): return m[0]
            return '['+m[1]+']('+p.as_uri()+')' + (' (раздел `'+anchor+'`)' if anchor else '')
        self.files[glossary]=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',rebase,self.files[glossary])
        unresolved = [n for n in self.nodes.values() if n.get('unresolved') or n['type']=='unresolved_reference' or n.get('resolution_state')=='unresolved']
        self.files[FOLDERS[9]+'/Известные пробелы.md'] = '\n\n'.join(['# Известные пробелы', link(HOME,'Главная'),
            'Неразрешённые узлы и ссылки исходного графа:', *['- '+self.nl(n['id']) for n in unresolved],
            'Отсутствующие локальные источники:', *['- `'+p+'`' for p in sorted(self.missing_sources)],
            'Пояснения, требующие пересмотра:', *['- '+x for x in self.stale_editorial],
            'Тематический указатель не означает исчерпывающего извлечения всех утверждений из всех документов проекта. Непредставленные свойства нельзя восстанавливать по аналогии.'])+'\n'
        self.files[FOLDERS[9]+'/Карта источников.md'] = '# Карта источников\n\n| ID графа | Страница или раздел |\n|---|---|\n' + '\n'.join(f'| `{id_}` | {self.nl(id_)} |' for id_ in sorted(self.nodes))+'\n'
        self.files[FOLDERS[9]+'/graph_snapshot.json'] = dump(self.graph)
        self.files[FOLDERS[9]+'/mapping.json'] = dump(self.paths)
        self.files[FOLDERS[9]+'/cards_snapshot.json'] = dump(self.cards)
        for p in [GRAPH,'source/fts_cards.jsonl','source/MANIFEST.json','work/DOCUMENT_MAP.md','work/notation.md',PACKAGE+'/editorial.json',PACKAGE+'/RULES.md','tools/obsidian_fts.py']:
            self.inputs[p] = sha((self.root/p).read_bytes())
        date = self.manifest_source.get('canonical_update_date','не указана')
        self.files[HOME] = '\n\n'.join(['# ФТС — энциклопедия сущностей',
            'Здесь можно найти сущность, прочитать её определение и свойства, затем перейти к основаниям, связям и открытым вопросам.',
            link(CORPUS_INDEX,'Полные материалы work')+' · '+link(COVERAGE,'Состояние раскрытия сущностей')+' · '+link(RESEARCH_INDEX,'Реестр исследовательских предложений'),
            f'**Исследовательские предложения:** {self.corpus_summary["research_proposals"]} отдельных страниц вне канона; принятые предложения адресованы существующим карточкам.',
            f'**Рабочий слой:** {self.corpus_summary["documents"]} полных текстов; разобрано {self.corpus_summary["reviewed"]} документов, включая {self.corpus_summary["derived_verified"]} производных, сверенных с первичными данными; {self.corpus_summary["facets"]} проверенных адресных раскрытий. Наличие полного текста и полнота его разбора различаются.',
            f'**Версия канона:** `{self.manifest_source.get("package")}`. Дата канона: {date}. Дата сборки и контроль источников — '+link(FOLDERS[9]+'/Состояние обновления.md','Состояние обновления')+'.',
            f'**Покрытие:** {len(self.cards)} карточек канона; {len(self.nodes)} узла и {len(self.graph["edges"])} направленная связь исходного графа.',
            '## С чего начать', link(FOLDERS[2]+'/Лестница уровней.md','Лестница и уровни −1…17')+' · '+link(FOLDERS[2]+'/LEVEL_07 — Уровень 7.md','Разобрать уровень 7')+' · '+link(RULES,'Правила чтения и обновления')+' · '+link(FOLDERS[0]+'/Обозначения.md','Словарь обозначений'),
            '## Разделы', *['- '+link(FOLDERS[i]+'/Обзор.md',FOLDERS[i].split(' — ',1)[1]) for i in range(1,8)],
            '## Источники, вопросы и свои заметки', link(SOURCE_INDEX,'Документы проекта')+' · '+link(FOLDERS[9]+'/Известные пробелы.md','Известные пробелы')+' · '+link(FOLDERS[8]+'/Как вести мои заметки.md','Мои заметки'),
            '## Как понимать связи', 'Иерархия папок — навигация. Основания, зависимости, проверки и ограничения показаны подписанными направленными связями. Каноническое принятие, авторское принятие и доказательный статус различаются.',
            'База подготовлена из артефактов ФТС; пояснения составителя не являются новыми положениями теории.'])+'\n'
        for module in ('tools/obsidian_fts_corpus.py','tools/obsidian_fts_registry.py'):
            self.inputs[module] = sha((self.root/module).read_bytes())
        return self.files

    def level_pages(self):
        overview = ['# Лестница уровней', link(HOME,'Главная'), 'ЛУ — логическая, СУ — семантическая, МУ — математическая лестница. Операциональное чтение показано отдельно. Номер без регистра не задаёт тождество представлений.']
        map_path='work/v14_rebuild/FTS_v14_register_map.md'
        map_source=self.source(map_path)
        map_lines=self.source_cache[(self.root/map_path).resolve()].splitlines()
        for level in range(-1,18):
            suffix = 'm1' if level==-1 else f'{level:02}'
            c = self.card_by_id['U_'+suffix]
            p = FOLDERS[2]+f'/LEVEL_{suffix} — Уровень {level}.md'
            lines = [f'# Уровень {level} — {c["title"]}',link(HOME,'Главная')+' · '+link(FOLDERS[2]+'/Лестница уровней.md','Лестница'),
                     'Обзор объединяет адреса представлений одного уровня. Их формулы, области и статусы читаются отдельно.']
            for label, prefix in [('Семантика — СУ','U_'),('Минимальное логическое выражение — ЛУ','M_'),('Математическое представление — МУ','A_'),('Операциональное чтение','CH_')]:
                cid=prefix+suffix
                found = [n for n in self.nodes.values() if n.get('card_id')==cid and self.card_for(n)]
                lines += ['## '+label]
                if found: lines += [self.nl(found[0]['id']), fenced(self.card_by_id[cid]['text'])]
                else:
                    lines += ['Отдельная карточка этого представления: нет в артефактах. '+map_source+'.']
                    if prefix=='A_':
                        row=next((line for line in map_lines if re.match(r'^\|\s*'+('−1' if level==-1 else str(level))+r'\s*\|',line)),None)
                        if row:
                            lines += ['Контекстная строка рабочей регистровой карты (все столбцы сохранены). Это сводка с собственными ограничениями, а не новая каноническая карточка. При расхождении действует адресная карточка текущего канона.',
                                      '| n | СУn | ЛУn | Ч-регистр | МУn | Чётность | Правая часть | Нуль |\n|---|---|---|---|---|---|---|---|\n'+row]
            lines += ['## Основания, операции и вопросы', 'Переходы и свидетельства доступны из таблиц связей соответствующих представлений. Отсутствие отдельной карточки не означает отсутствия чтения в других документах.']
            selected = []
            for prefix in ('U_','M_','A_','CH_'):
                selected += self.corpus.by_entity.get(prefix+suffix,[])
            selected = list({f['id']:f for f in selected}.values())
            if selected:
                lines += ['## Свойства, примеры и ограничения из work',
                          '| Положение | Пояснение | Область | Статус | Основание |\n|---|---|---|---|---|']
                for f in selected:
                    target=self.corpus.source_target(f)
                    basis=link(target, f['source_file']+':'+str(f['line_start'])) if target else self.source(f['source_file'])
                    lines[-1] += f'\n| {cell(f["title"])} | {cell(f["summary_ru"])} | {cell(f["scope_ru"])} | {cell(f["status_ru"])} | {basis} |'
            self.files[p] = blocks(lines)
            overview += ['- '+link(p,f'{level}: {c["title"]}')]
        self.files[FOLDERS[2]+'/Лестница уровней.md']='\n\n'.join(overview)+'\n'

    def verify(self, files=None):
        files = files or self.files
        errors=list(self.corpus.errors)+self.corpus.registry.verify(files)
        plain={p for p in files if p.endswith('.md')}
        adjacency=defaultdict(set)
        for path, text in files.items():
            if not path.endswith('.md'): continue
            # Ignore quoted source/code; links there are examples or exact source text.
            in_code=False
            cleaned=[]
            for line in text.splitlines():
                if line.startswith('```'): in_code=not in_code; continue
                if not in_code: cleaned.append(line)
            for target in re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', '\n'.join(cleaned)):
                dest,_,anchor=target.partition('#')
                dest=dest+'.md'
                if dest.startswith(FOLDERS[8]+'/'): continue
                if dest not in files: errors.append(f'Broken link {path}: {target}'); continue
                adjacency[path].add(dest)
                if anchor and f'## {anchor}\n' not in files[dest]: errors.append(f'Missing anchor: {target}')
        distances={HOME:0}; q=deque([HOME])
        while q:
            p=q.popleft()
            for target in adjacency[p]:
                if target not in distances: distances[target]=distances[p]+1; q.append(target)
        for id_, dest in self.paths.items():
            path,_,anchor=dest.partition('#')
            if path not in plain: errors.append(f'Missing mapping {id_}')
            if anchor and f'## {anchor}\n' not in files[path]: errors.append(f'Missing node anchor {id_}')
            if '#' not in dest and distances.get(path,999)>3: errors.append(f'Over 3 clicks: {id_}')
        for rid,path in self.corpus.registry.paths.items():
            if distances.get(path,999)>3: errors.append('Over 3 clicks: '+rid)
        for c in self.cards:
            n=next(n for n in self.nodes.values() if n.get('card_id')==c['id'] and self.card_for(n))
            text=files[self.paths[n['id']]]
            if fenced(c['text']) not in text: errors.append(f'Canonical text changed: {c["id"]}')
            if fenced(dump(c).rstrip(),'json') not in text: errors.append(f'Canonical record lost: {c["id"]}')
        for cid,facets in self.corpus.by_entity.items():
            nid=self.corpus.card_nodes.get(cid)
            path=self.paths[nid] if nid else self.corpus.registry.paths.get(cid)
            text=files.get(path,'')
            for facet in facets:
                if fenced(facet['exact_quote']) not in text:
                    errors.append('Facet quotation lost: '+facet['id']+' / '+cid)
                for field in ('summary_ru','scope_ru','status_ru'):
                    if facet[field] not in text:
                        errors.append('Facet explanation lost: '+facet['id']+' / '+cid+' / '+field)
        # Sample gate: exact U7 registers and retained proof/adoption axes.
        for cid in ['U_07','M_07','CH_07','A_07','OP_Lift','OP_pi','AC_20261003_WINDOWS_TRIPLES']:
            if cid not in self.card_by_id: errors.append(f'Sample card missing: {cid}')
        if 'canonical_adopted' not in self.card_by_id['A_07'].values(): errors.append('Unexpected U7 adoption source; revise sample gate')
        return errors


def checked_path(vault, rel):
    p=(vault/rel).resolve()
    if not p.is_relative_to(vault.resolve()): raise ValueError(f'Outside vault: {rel}')
    return p


def publish(vault, enc, write=False, date=None):
    files=enc.files.copy()
    manifest_path=vault/MANIFEST
    old=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    previous=old.get('files',{})
    conflict=[]
    updates=[]
    archived=[]
    for rel, text in files.items():
        p=checked_path(vault,rel)
        actual=sha(p.read_bytes()) if p.exists() else None
        if actual and actual!=previous.get(rel) and actual!=sha(text): conflict.append(rel)
        elif actual!=sha(text): updates.append(rel)
    for rel, expected in previous.items():
        if rel in files or rel.endswith('Состояние обновления.md') or rel.endswith('История обновлений.md'): continue
        p=checked_path(vault,rel)
        if p.exists():
            if sha(p.read_bytes())!=expected: conflict.append(rel)
            else:
                prior=p.read_text(encoding='utf-8')
                files[rel]=prior if prior.startswith('> Архивная страница.') else '> Архивная страница. Эта запись отсутствует в текущем экспорте; прежнее содержание сохранено для старых ссылок и комментариев.\n\n'+prior
                if files[rel]!=prior: archived.append(rel)
    status_rel=FOLDERS[9]+'/Состояние обновления.md'
    history_rel=FOLDERS[9]+'/История обновлений.md'
    # These are managed, too; never overwrite manual changes even during a no-op.
    for rel in [status_rel,history_rel]:
        p=vault/rel
        if p.exists() and sha(p.read_bytes())!=previous.get(rel): conflict.append(rel)
    changes=bool(updates or archived or enc.inputs!=old.get('input_digests'))
    summary={'create_or_update':len(updates),'archive':len(archived),'conflicts':sorted(set(conflict)), 'card_count':len(enc.cards),'graph_nodes':len(enc.nodes),'graph_edges':len(enc.graph['edges'])}
    if not write: return summary
    if conflict:
        # Preserve both current file bytes and proposed replacements for explicit review.
        for rel in set(conflict):
            p=checked_path(vault,rel)
            conflict_dir=vault/FOLDERS[9]/'Конфликты'/sha(rel)[:12]
            conflict_dir.mkdir(parents=True,exist_ok=True)
            if p.exists():
                current=p.read_bytes()
                (conflict_dir/('сохранённая-правка-'+sha(current)[:12]+'.md')).write_bytes(current)
            (conflict_dir/'предлагаемая-версия.md').write_text(files.get(rel,'Запись удалена из нового экспорта.'),encoding='utf-8')
            (conflict_dir/'адрес.txt').write_text(rel,encoding='utf-8')
        raise RuntimeError('Обнаружены ручные изменения; сборка не применена. Копии сохранены в «90 — Служебное/Конфликты».')
    date=date or datetime.now(timezone(timedelta(hours=3))).date().isoformat()
    if changes or not old:
        status=f'# Состояние обновления\n\nДата сборки: {date}.\n\nВерсия канона: `{enc.manifest_source.get("package")}`.\n\nКарточек канона: {len(enc.cards)}. Узлов графа: {len(enc.nodes)}. Связей: {len(enc.graph["edges"])}.\n\nХэши всех использованных источников записаны в manifest.json.\n\nПояснений, требующих пересмотра: {len(enc.stale_editorial)}. Отсутствующих источников: {len(enc.missing_sources)}.\n\n'+link(FOLDERS[9]+'/Известные пробелы.md','Известные пробелы')+'\n'
        files[status_rel]=status
        prev_history=(vault/history_rel).read_text(encoding='utf-8') if (vault/history_rel).exists() else '# История обновлений\n'
        files[history_rel]=prev_history+f'\n- {date}: создано/обновлено {len(updates)}, архивировано {len(archived)}; карточек {len(enc.cards)}, узлов {len(enc.nodes)}.\n'
    else:
        for rel in [status_rel,history_rel]:
            if (vault/rel).exists(): files[rel]=(vault/rel).read_text(encoding='utf-8')
    for rel,text in files.items():
        p=checked_path(vault,rel)
        if not p.exists() or p.read_bytes()!=text.encode('utf-8'):
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(text,encoding='utf-8',newline='\n')
    # User-owned files are seeded once, never managed by the manifest.
    personal=vault/FOLDERS[8]/'Как вести мои заметки.md'
    if not personal.exists():
        personal.parent.mkdir(parents=True,exist_ok=True)
        personal.write_text('# Мои заметки\n\nСоздавайте здесь собственные файлы. Добавляйте ссылку на сущность, затем свой вопрос или предложение. Эта папка не перезаписывается генератором.\n\nПример:\n\n'+link(enc.paths[next(n['id'] for n in enc.nodes.values() if n.get('card_id')=='OP_Lift' and enc.card_for(n))],'Lift')+'\n\nМой вопрос: …\n\nПредложение меняет проект только после отдельного переноса и проверки.\n',encoding='utf-8')
    config=vault/'.obsidian'
    config.mkdir(exist_ok=True)
    defaults={'app.json':{'alwaysUpdateLinks':True,'newFileLocation':'folder','newFileFolderPath':FOLDERS[8]},'core-plugins.json':['file-explorer','global-search','switcher','graph','backlink','outgoing-link','tag-pane','page-preview','properties','outline','bookmarks'],'community-plugins.json':[],'graph.json':{'search':'-path:"90 — Служебное"','showTags':False,'showAttachments':False,'hideUnresolved':False}}
    for name,obj in defaults.items():
        p=config/name
        if not p.exists(): p.write_text(dump(obj),encoding='utf-8')
    manifest={'schema':'fts-obsidian/v1','generator':VERSION,'source_root':str(enc.root.resolve()),'updated_on':date if changes else old.get('updated_on',date),'input_digests':enc.inputs,'files':{p:sha(t) for p,t in sorted(files.items())},'node_mapping':enc.paths,'cards':{c['id']: next(enc.paths[n['id']] for n in enc.nodes.values() if n.get('card_id')==c['id'] and enc.card_for(n)) for c in enc.cards}}
    output=dump(manifest)
    if not manifest_path.exists() or manifest_path.read_text(encoding='utf-8')!=output: manifest_path.write_text(output,encoding='utf-8')
    return summary


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,default=ROOT)
    p.add_argument('--vault',type=Path,default=DEFAULT_VAULT)
    mode=p.add_mutually_exclusive_group()
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    mode.add_argument('--preview',action='store_true')
    args=p.parse_args(argv)
    check=subprocess.run([sys.executable,'-X','utf8',str(args.source_root/'tools/claim_graph.py'),'validate'],cwd=args.source_root,capture_output=True,text=True,encoding='utf-8')
    if check.returncode: raise RuntimeError('Граф устарел или не прошёл проверку:\n'+check.stdout+check.stderr)
    existing_manifest=args.vault/MANIFEST
    previous_mapping=json.loads(existing_manifest.read_text(encoding='utf-8')).get('node_mapping') if existing_manifest.exists() else None
    enc=Encyclopedia(args.source_root, previous_mapping); enc.build()
    # References to runtime update status are supplied by publication.
    enc.files.setdefault(FOLDERS[9]+'/Состояние обновления.md','# Состояние обновления\n')
    errs=enc.verify()
    if errs: raise RuntimeError('\n'.join(errs[:30]))
    enc.files.pop(FOLDERS[9]+'/Состояние обновления.md')
    if args.check:
        m=json.loads((args.vault/MANIFEST).read_text(encoding='utf-8'))
        errs=[]
        for rel,h in m['files'].items():
            path=checked_path(args.vault,rel)
            if not path.exists() or sha(path.read_bytes())!=h: errs.append('Изменён или отсутствует: '+rel)
        if enc.inputs!=m['input_digests']: errs.append('Источники изменились: требуется обновление')
        files={rel:(args.vault/rel).read_text(encoding='utf-8') for rel in m['files'] if (args.vault/rel).exists()}
        errs+=enc.verify(files)
        if errs: raise RuntimeError('\n'.join(errs[:30]))
        print(dump({'result':'PASS','cards':len(enc.cards),'nodes':len(enc.nodes),'edges':len(enc.graph['edges']),'managed_files':len(m['files']),'stale_editorial':enc.stale_editorial,'stale_registry_editorial':enc.corpus.registry.stale,'research_proposals':enc.corpus_summary['research_proposals'],'missing_sources':sorted(enc.missing_sources)}))
    else:
        summary=publish(args.vault,enc,args.write)
        print(dump(summary))
        if summary['conflicts']: return 2
    return 0


if __name__=='__main__':
    try: sys.exit(main())
    except (ValueError, RuntimeError, OSError) as e:
        print(str(e),file=sys.stderr); sys.exit(1)
