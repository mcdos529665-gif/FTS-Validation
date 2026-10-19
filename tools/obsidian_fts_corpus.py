"""Source corpus and reviewed, source-bound facets for the FTS encyclopedia.

Routing by a literal identifier is navigation only. Only reviewed facets become
properties of an entity. Full source context remains available in the vault.
"""
from collections import defaultdict
from obsidian_fts_registry import Registry, blocks
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

PACKAGE = 'work/v14_rebuild/obsidian_encyclopedia'
CORPUS_INDEX = '07 — Основания и проверки/Материалы work.md'
COVERAGE = '90 — Служебное/Разбор материалов work.md'
FACETS = PACKAGE + '/facets.jsonl'
REVIEWS = PACKAGE + '/document_reviews.json'
KINDS = {'property': 'Свойство', 'example': 'Пример', 'limitation': 'Ограничение',
         'definition': 'Определение', 'research': 'Исследовательское чтение',
         'author_clarification': 'Авторское уточнение'}


def digest(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def classify(path):
    """Explicit exclusions are retained in the census with their reason."""
    parts = Path(path).parts
    if 'obsidian_encyclopedia' in parts:
        return 'служебное', 'Правила и данные самой энциклопедии; исключены из рекурсивного импорта.'
    if any(x in parts for x in ('canon_history', 'state_history', 'notation_history', 'instruction_history')):
        return 'история', 'Исторический архив; переносится только по адресному основанию.'
    if 'export' in parts:
        return 'дубликат', 'Сводный производный экспорт; первичные документы учитываются отдельно.'
    if 'paper_plan' in parts and Path(path).name.startswith('habr_draft_'):
        return 'история', 'Промежуточный вариант статьи; итоговый текст учитывается отдельно.'
    if Path(path).name in ('REGISTER_head.md', 'REGISTER_tail.md'):
        return 'дубликат', 'Части сборки реестра; полный реестр учитывается отдельно.'
    if Path(path).name == 'source.en.md' or '/inputs/DR-' in path:
        return 'внешний текст', 'Внешний полный текст; в энциклопедии используются локальные обзоры и досье с их ограничениями.'
    if Path(path).name in ('STATE.md', 'DOCUMENT_MAP.md'):
        return 'указатель', 'Навигация и состояние; содержательные первоисточники перечислены в корпусе.'
    if any(x in parts for x in ('project_consistency',)):
        return 'процедура', 'Согласование проекта; сохраняется как контекст проверок, не определение сущности.'
    if any(t in Path(path).name.upper() for t in ('PROTOCOL', 'PREREGISTRATION', 'RUNBOOK', 'SEARCH_LOG', 'TOOLCHAIN', 'PROVIDER_STATUS', 'PIPELINE', 'STYLE_PROFILE')):
        return 'протокол', 'Область, метод или план; не свидетельство завершённого результата.'
    return 'содержание', 'Материал теории, исследования, авторского уточнения или результата.'


def sections(text):
    """Partition all lines exactly once; headings inside code are not boundaries."""
    lines = text.splitlines()
    starts = [(0, 'Начало документа')]
    fence = None
    for i, line in enumerate(lines):
        f = re.match(r'^\s*(`{3,}|~{3,})', line)
        if f:
            char = f[1][0]
            if fence is None: fence = char
            elif fence == char: fence = None
            continue
        if fence is None and re.match(r'^#{1,6}\s+', line):
            title = re.sub(r'^#+\s+', '', line).strip()
            if i == 0: starts[0] = (0, title)
            else: starts.append((i, title))
    return [{'start': start+1, 'end': starts[i+1][0] if i+1<len(starts) else len(lines),
             'title': title, 'text': '\n'.join(lines[start:starts[i+1][0] if i+1<len(starts) else len(lines)])}
            for i, (start,title) in enumerate(starts) if start < len(lines)]


class Corpus:
    def __init__(self, enc):
        self.enc = enc
        self.root = enc.root
        self.documents = []
        self.by_entity = defaultdict(list)
        self.facets = []
        self.errors = []
        self.stale_facets = []
        self.reviews = {}
        self.mentions = defaultdict(list)
        self.by_path = {}
        self.assets = []
        self.questions = []
        self.entity_questions = defaultdict(list)
        for rel in (FACETS, REVIEWS):
            p = self.root/rel
            if p.exists():
                enc.inputs[rel] = digest(p.read_bytes())
                if rel == REVIEWS: self.reviews = json.loads(p.read_text(encoding='utf-8'))
                else: self.facets = [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
        self.card_nodes = {n['card_id']: nid for nid,n in enc.nodes.items() if enc.card_for(n)}
        self.scan()
        self.scan_assets()
        self.registry = Registry(self)
        self.validate_facets()
        self.load_questions()

    def load_questions(self):
        rel='work/v14_rebuild/claim_questions/QUESTION_CARDS.jsonl'
        p=self.root/rel
        if not p.exists(): return
        self.enc.inputs[rel]=digest(p.read_bytes())
        self.questions=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
        for q in self.questions:
            refs=q.get('refs',{})
            ids=set(q.get('known_in_corpus',[])+refs.get('cards',[])+[q.get('source_id','')])
            # An explicit level reference is a navigation address, not inheritance.
            ids.update('U_'+('m1' if n==-1 else f'{n:02}') for n in refs.get('levels',[]) if isinstance(n,int))
            for cid in ids & self.card_nodes.keys(): self.entity_questions[cid].append(q)

    def scan_assets(self):
        """Census of non-Markdown evidence; inventory is not semantic acceptance."""
        for p in sorted((self.root/'work').rglob('*')):
            if not p.is_file() or p.suffix.lower()=='.md': continue
            rel=p.relative_to(self.root).as_posix()
            excluded=None
            if '__pycache__' in p.parts or p.suffix=='.pyc': excluded='Кеш исполнения, не источник утверждения.'
            elif any(x in p.parts for x in ('obsidian_encyclopedia','export','canon_history','state_history','notation_history','instruction_history')):
                excluded='Данные энциклопедии, производный экспорт или исторический архив; первоисточники учитываются отдельно.'
            kind={'.py':'исполняемый свидетель / инструмент','.lean':'формальное доказательство','.wl':'CAS-свидетель',
                  '.tsv':'структурированный реестр','.json':'структурированные данные / результат','.jsonl':'адресные записи',
                  '.bib':'библиографические записи','.txt':'текстовый материал','.pdf':'бинарный документ',
                  '.tex':'исходник документа'}.get(p.suffix.lower(),'конфигурация / иной материал')
            record={'path':rel,'kind':kind,'size':p.stat().st_size,'excluded_reason':excluded}
            if not excluded:
                h=hashlib.sha256()
                with p.open('rb') as stream:
                    for block in iter(lambda:stream.read(1024*1024),b''): h.update(block)
                record['sha256']=h.hexdigest()
                self.enc.inputs[rel]=record['sha256']
                review=self.reviews.get(rel,{})
                record['review']=review if review.get('sha256')==record['sha256'] else {}
                record['review_stale']=bool(review and not record['review'])
                record['content_review']=(record['review'].get('review_note','подтверждён') if record['review'] else
                    'требует пересмотра после изменения источника' if record['review_stale'] else
                    'не завершён; адресные результаты могут быть представлены через граф или раскрытия')
            self.assets.append(record)
        self.enc.inputs['__work_asset_census__']=digest(json.dumps(self.assets,ensure_ascii=False,sort_keys=True))

    def scan(self):
        # Full Markdown census includes files not reachable from a graph or map.
        ids = sorted(self.card_nodes, key=len, reverse=True)
        id_pattern = re.compile(r'(?<![\w])('+'|'.join(re.escape(x) for x in ids)+r')(?![\w])')
        for p in sorted((self.root/'work').rglob('*.md')):
            rel = p.relative_to(self.root).as_posix()
            category, reason = classify(rel)
            raw = p.read_bytes()
            doc = {'path':rel, 'sha256':digest(raw), 'category':category, 'reason':reason}
            review = self.reviews.get(rel,{})
            doc['review'] = review if review.get('sha256') == doc['sha256'] else {}
            doc['review_stale'] = bool(review and not doc['review'])
            doc['included'] = category in ('содержание','протокол','процедура')
            if doc['included']:
                text = raw.decode('utf-8-sig')
                doc['sections'] = sections(text)
                doc['page'] = '07 — Основания и проверки/WORK_'+digest(rel)[:16]+' — '+re.sub(r'[<>:"/\\|?*\[\]#^]', ' ', p.stem)[:65].rstrip(' .')+'.md'
                self.enc.inputs[rel] = doc['sha256']
                for section in doc['sections']:
                    section['anchor'] = 'W_'+digest(rel+'\n'+str(section['start']))[:16]
                    # Literal membership provides a route to evidence; it asserts no property.
                    section['entity_ids'] = sorted(set(id_pattern.findall(section['text'])))
                    for cid in section['entity_ids']:
                        self.mentions[cid].append((doc, section))
            self.documents.append(doc)
            self.by_path[rel] = doc
        # Census membership is part of freshness: a new file changes the digest.
        self.enc.inputs['__work_markdown_census__'] = digest(json.dumps([(d['path'],d['sha256']) for d in self.documents],ensure_ascii=False))

    def validate_facets(self):
        seen = set()
        for f in self.facets:
            fid = f.get('id')
            if not fid or fid in seen: self.errors.append('Дублирующийся/отсутствующий ID раскрытия: '+str(fid))
            seen.add(fid)
            path = f.get('source_file','')
            p = (self.root/path).resolve()
            if not p.is_relative_to(self.root.resolve()) or not p.is_file():
                self.errors.append('Источник раскрытия отсутствует: '+str(fid)); continue
            raw = p.read_bytes()
            self.enc.inputs[path] = digest(raw)
            if f.get('source_sha256') != digest(raw):
                self.stale_facets.append(f); continue
            lines = raw.decode('utf-8-sig').splitlines()
            a,b = f.get('line_start',0),f.get('line_end',0)
            if not (1<=a<=b<=len(lines)) or '\n'.join(lines[a-1:b]) != f.get('exact_quote'):
                self.errors.append('Неточный фрагмент раскрытия: '+str(fid)); continue
            if f.get('kind') not in KINDS or not f.get('summary_ru') or not f.get('scope_ru') or not f.get('status_ru'):
                self.errors.append('Неполное раскрытие: '+str(fid))
            for cid in f.get('entity_ids',[]):
                if cid not in self.card_nodes and cid not in self.registry.research_ids: self.errors.append('Неизвестная сущность раскрытия: '+str(cid))
                else: self.by_entity[cid].append(f)

    def source_target(self, f):
        doc = self.by_path.get(f['source_file'])
        if doc and doc['included']:
            section = next(s for s in doc['sections'] if s['start'] <= f['line_start'] <= s['end'])
            return doc['page']+'#'+section['anchor']
        return None

    def render_facets(self, cid, link, cell, fenced):
        entries = self.by_entity.get(cid,[])
        lines = []
        stale=[f for f in self.stale_facets if cid in f.get('entity_ids',[])]
        if stale:
            lines += ['> Требуют пересмотра '+str(len(stale))+' раскрытий: изменились исходные документы. Прежние пересказы не выдаются за действующие свойства. Сохранённые записи доступны в служебном work_coverage.json.']
        if entries:
            lines += ['## Раскрытие по материалам проекта',
                     'Далее — адресные пояснения и свойства из рабочих материалов. Каждая запись сохраняет собственную область, происхождение и статус; принятие карточки не повышает статус связанного исследования.',
                     '| Свойство / различие | Формулировка | Область действия | Основание | Статус |', '|---|---|---|---|---|']
            for f in entries:
                target = self.source_target(f)
                basis = link(target, f['source_file']+':'+str(f['line_start'])) if target else self.enc.source(f['source_file'],f'L{f["line_start"]}–L{f["line_end"]}')
                lines.append(f'| {cell(KINDS[f["kind"]]+": "+f["title"])} | {cell(f["summary_ru"])} | {cell(f["scope_ru"])} | {basis} | {cell(f["status_ru"])} |')
            for f in entries:
                lines += ['### '+f['title'],f['summary_ru'], '**Область:** '+f['scope_ru'], '**Статус:** '+f['status_ru'],
                          self.enc.source(f['source_file'],f'L{f["line_start"]}–L{f["line_end"]}'),
                          'Дословное основание:',fenced(f['exact_quote'])]
        mentions = self.mentions.get(cid,[])
        primary=self.enc.card_by_id.get(cid,{}).get('source_document','').partition('#')[0]
        doc=self.by_path.get(primary)
        if doc and doc['included']:
            lines += ['## Полный документ происхождения',
                      link(doc['page'],'Читать '+primary),
                      'Документ указан в самой карточке как source_document. Его остальные положения не приписываются этой карточке автоматически.']
        lines += self.registry.reference_lines(cid,link)
        questions=self.entity_questions.get(cid,[])
        if questions:
            lines += ['## Вопросы к сущности и её адресованным утверждениям',
                      'Сохранены вопросы исследовательского слоя. `unanswered` и наличие источника ответа — разные поля; отметка covered сама по себе не доказывает, что ответ верен и полон. Происхождение и авторская проверка показаны отдельно.',
                      '| Вопрос | Состояние ответа | Покрытие корпусом | Происхождение / проверка |', '|---|---|---|---|']
            for q in questions:
                lines.append('| '+cell(q['question_id']+': '+q['question'])+' | '+cell(q.get('answer_status','не указано'))+' | '+cell(q.get('corpus_coverage','не указано'))+' | '+cell(str(q.get('question_origin','не указано'))+' / '+str(q.get('author_review','не указано')))+' |')
            lines += [self.enc.source('work/v14_rebuild/claim_questions/QUESTION_CARDS.jsonl','question_id; исходные записи в служебном снимке')]
        if mentions:
            lines += ['## Дополнительный контекст work',
                      'Ниже разделы, буквально упоминающие ID этой сущности. Это поисковый контекст, а не утверждение зависимости или наследования. Полные тексты сохранены внутри хранилища.']
            lines += ['- '+link(d['page']+'#'+s['anchor'],d['path']+' — '+s['title']) for d,s in mentions]
        return blocks(lines) if lines else ''

    def rebase(self, text, source_path):
        def replace(m):
            target = m[2]
            if '://' in target or target.startswith(('mailto:','data:')): return m[0]
            path,_,anchor = target.partition('#')
            p = (self.root/source_path).parent/unquote(path) if path else self.root/source_path
            uri = p.resolve().as_uri()
            return '['+m[1]+']('+uri+')'+(' (раздел `'+anchor.replace('`','')+'`)' if anchor else '')
        # Original links remain source links rather than accidental vault paths.
        text = re.sub(r'(?<!!)\[([^\]\n]+)\]\(([^\n)]+)\)',replace,text)
        text = text.replace('[[',r'\[\[').replace(']]',r'\]\]')
        return text

    def build(self, link, cell, fenced, frontmatter):
        research_count = self.registry.build(link,cell,fenced,frontmatter)
        canonical_entities = len(self.by_entity.keys() & self.card_nodes.keys())
        research_entities = len(self.by_entity.keys() & self.registry.research_ids)
        for d in self.documents:
            if not d['included']: continue
            title = d['sections'][0]['title'] if d['sections'] else Path(d['path']).stem
            lines = ['# '+title, link(CORPUS_INDEX,'Материалы work'), self.enc.source(d['path']),
                     '**Роль:** '+d['category']+'. '+d['reason'],
                     'Полный локальный контекст. Формулировки документа сохраняют своё время и область. Противоречия с действующим каноном читаются как различия версий или незакрытые обязательства, а не исправляются при экспорте.']
            if d['review']: lines += ['**Разбор:** '+d['review'].get('review_note','')]
            else: lines += ['**Разбор:** полный текст включён; содержательный разбор ещё не подтверждён.']
            for s in d['sections']:
                body = re.sub(r'^#{1,6}\s+.*(?:\n|$)','',s['text'],count=1)
                lines += ['## '+s['anchor'], '### '+s['title'], f'Исходные строки {s["start"]}–{s["end"]}.', self.rebase(body,d['path'])]
            self.enc.files[d['page']] = '\n\n'.join(lines)+'\n'
        included = [d for d in self.documents if d['included']]
        reviewed = [d for d in included if d['review']]
        lines = ['# Материалы work',link('00 — Начало/Начать здесь.md','Главная'),
                 'Полные рабочие тексты, в том числе вне графа. Авторские уточнения, модели, протоколы, отрицательные результаты и вопросы имеют разные роли. '+link(COVERAGE,'Границы и состояние содержательного разбора'),
                 '| Документ | Роль | Содержательный разбор |', '|---|---|---|']
        lines += [f'| {link(d["page"], d["path"])} | {d["category"]} | {"подтверждён" if d["review"] else "не завершён"} |' for d in included]
        self.enc.files[CORPUS_INDEX] = '\n\n'.join(lines[:3])+'\n\n'+'\n'.join(lines[3:])+'\n'
        report = ['# Разбор материалов work',link('00 — Начало/Начать здесь.md','Главная'),
                  f'Перепись: {len(self.documents)} Markdown-документов. Полных текстов включено: {len(included)}. Подтверждённых содержательных разборов: {len(reviewed)}. Проверенных адресных раскрытий: {len(self.facets)-len(self.stale_facets)}. Требуют пересмотра: {len(self.stale_facets)}. Сущностей с такими раскрытиями: {canonical_entities} из {len(self.card_nodes)}; дополнительных исследовательских страниц с раскрытиями: {research_entities}.',
                  'Точное включение текста, поиск упоминания и проверенное содержательное раскрытие учитываются раздельно. Наличие полного текста не закрывает обязательство его разбора.',
                  '| Источник | Роль / решение | Разбор |', '|---|---|---|']
        for d in self.documents:
            state = 'подтверждён' if d['review'] else ('требует пересмотра' if d['review_stale'] else ('ожидает разбора' if d['included'] else 'исключён с основанием'))
            report.append(f'| `{d["path"]}` | {cell(d["category"]+": "+d["reason"])} | {state} |')
        self.enc.files[COVERAGE] = '\n\n'.join(report[:4])+'\n\n'+'\n'.join(report[4:])+'\n'
        other='90 — Служебное/Материалы кроме Markdown.md'
        self.enc.files[COVERAGE]+='\n'+link(other,'Перепись таблиц, данных, свидетелей и других форматов')+'\n'
        asset_lines=['# Материалы кроме Markdown',link(COVERAGE,'Состояние содержательного разбора'),
                     'Фиксируется весь состав work. Эта перепись не означает, что содержательные результаты каждого файла уже извлечены в статьи.',
                     '| Файл | Роль | Решение / состояние |','|---|---|---|']
        asset_lines += ['| '+self.enc.source(a['path'])+' | '+a['kind']+' | '+cell(a.get('excluded_reason') or a.get('content_review'))+' |' for a in self.assets]
        self.enc.files[other]='\n\n'.join(asset_lines[:3])+'\n\n'+'\n'.join(asset_lines[3:])+'\n'
        serial = [{k:v for k,v in d.items() if k!='sections'} | {'sections':[{k:v for k,v in s.items() if k!='text'} for s in d.get('sections',[])]} for d in self.documents]
        self.enc.files['90 — Служебное/work_coverage.json'] = json.dumps({'documents':serial,'assets':self.assets,'facets':self.facets,'stale_facets':[f['id'] for f in self.stale_facets],'errors':self.errors},ensure_ascii=False,sort_keys=True,indent=2)+'\n'
        self.enc.files['90 — Служебное/entity_questions_snapshot.json'] = json.dumps(self.questions,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
        return {'documents':len(included),'reviewed':len(reviewed),'facets':len(self.facets)-len(self.stale_facets),'stale_facets':len(self.stale_facets),'entities':canonical_entities,'research_entities':research_entities,'pending':len(included)-len(reviewed),'research_proposals':research_count}
