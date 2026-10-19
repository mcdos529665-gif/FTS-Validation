"""Address both accepted CP cards and proposals remaining outside the canon.

Registry links state reference, never inheritance. Curated explanations are
withheld when either their primary row file or disposition file changes.
"""
import csv
import hashlib
import json
from pathlib import Path
import re

BASE = 'work/v14_rebuild/candidates_register_2026-10-15/'
EDITORIAL = 'work/v14_rebuild/obsidian_encyclopedia/registry_editorial.json'
INDEX = '06 — Модели и исследования/Реестр исследовательских предложений.md'
DECISIONS = {'canonical':'принято в канон','alternative':'открытый выбор',
             'conflict':'зафиксированное противоречие','superseded':'заменённая формулировка',
             'historical':'историческая оценка','empty':'нет содержательного предложения'}


def sha(raw): return hashlib.sha256(raw).hexdigest()


def blocks(parts):
    """Keep generated table rows contiguous; preserve each source block verbatim."""
    out=''
    for part in parts:
        separator='\n' if out.rstrip().endswith('|') and part.startswith('|') else '\n\n'
        out += (separator if out else '')+part
    return out+'\n'


class Registry:
    def __init__(self, corpus):
        self.corpus=corpus
        self.enc=corpus.enc
        self.root=corpus.root
        self.rows={}; self.dispositions={}; self.paths={}; self.editorial={}
        self.related={}; self.errors=[]; self.stale=[]; self.primary={}
        self.inputs={}
        def read(rel):
            raw=(self.root/rel).read_bytes()
            self.inputs[rel]=sha(raw)
            self.enc.inputs[rel]=sha(raw)
            return raw
        for p in sorted((self.root/(BASE+'src')).glob('G*.tsv')):
            rel=p.relative_to(self.root).as_posix()
            lines=read(rel).decode('utf-8-sig').splitlines()
            reader=csv.DictReader(lines,delimiter='\t')
            start=1
            for row in reader:
                rid=row['id']
                if rid in self.rows: self.errors.append('Повтор CP: '+rid)
                self.rows[rid]=row
                self.primary[rid]={'source_file':rel,'source_sha256':self.inputs[rel],
                    'line_start':start+1,'line_end':reader.line_num,
                    'exact_quote':'\n'.join(lines[start:reader.line_num])}
                start=reader.line_num
        rel=BASE+'dispositions_2026-10-18.tsv'
        lines=read(rel).decode('utf-8-sig').splitlines()
        reader=csv.DictReader(lines,delimiter='\t'); start=1
        for row in reader:
            if row['layer']=='research':
                rid=row['id']
                if rid in self.dispositions: self.errors.append('Повтор решения CP: '+rid)
                self.dispositions[rid]=row|{'line_start':start+1,'line_end':reader.line_num,
                    'exact_quote':'\n'.join(lines[start:reader.line_num])}
            start=reader.line_num
        if set(self.rows)!=set(self.dispositions): self.errors.append('Состав CP и решений различается')
        self.editorial=json.loads(read(EDITORIAL).decode('utf-8'))
        for rid,row in self.rows.items():
            d=self.dispositions.get(rid,{})
            card=d.get('card')
            if d.get('decision')=='canonical':
                if card not in corpus.card_nodes: self.errors.append('Нет принятой CP-карточки: '+rid)
                else: self.paths[rid]=self.enc.paths[corpus.card_nodes[card]]
            else:
                # Immutable ID address survives editorial title changes.
                self.paths[rid]='06 — Модели и исследования/'+rid+' — Исследование.md'
                for cid in (row.get('cards') or '').split(','):
                    if cid in corpus.card_nodes: self.related.setdefault(cid,[]).append(rid)
                e=self.editorial.get(rid,{})
                if not e: self.errors.append('Нет проверенного пояснения CP: '+rid)
                elif (e.get('source_sha256')!=self.primary[rid]['source_sha256'] or
                      e.get('disposition_sha256')!=self.inputs[rel]): self.stale.append(rid)
                elif not all(e.get(k) for k in ('title','summary_ru','scope_ru')):
                    self.errors.append('Неполное пояснение CP: '+rid)
        self.research_ids={rid for rid,d in self.dispositions.items() if d['decision']!='canonical'}
        for rid in self.editorial:
            if rid not in self.rows: self.errors.append('Неизвестное пояснение CP: '+rid)

    def fresh(self, rid): return rid in self.editorial and rid not in self.stale

    def reference_lines(self, cid, link):
        ids=self.related.get(cid,[])
        if not ids: return []
        return ['## Предложения реестра вне канона',
                'Эти строки реестра ссылаются на карточку. Это адресная связь исследования; она не приписывает карточке все свойства предложения и не означает его принятия.',
                *['- '+link(self.paths[rid],rid+' — '+(self.editorial[rid]['title'] if self.fresh(rid) else 'пояснение требует пересмотра')) for rid in ids]]

    def document_link(self, location, link):
        path,_,anchor=location.partition('#')
        rel='work/'+path
        if not (self.root/rel).is_file(): rel=path
        doc=self.corpus.by_path.get(rel)
        if doc and doc['included']:
            return link(doc['page'],rel)+(' (исходный раздел `'+anchor+'`)' if anchor else '')
        return self.enc.source(rel,anchor or None)

    def question_link(self, qid, link):
        doc=self.corpus.by_path.get('work/OPEN_QUESTIONS.md')
        if doc and doc['included']:
            sec=next((s for s in doc['sections'] if qid in s['text']),None)
            return link(doc['page']+('#'+sec['anchor'] if sec else ''),qid)
        return qid

    def build(self, link, cell, fenced, frontmatter):
        index=['# Реестр исследовательских предложений',link('00 — Начало/Начать здесь.md','Главная'),
            'Каждая строка имеет один основной адрес: принятой CP-карточки либо отдельного исследования. Каноническое включение, происхождение формулировки, принятие текста ответа и доказательность различаются.',
            '| Предложение | Решение | Причина / область |','|---|---|---|']
        count=0
        for rid,row in self.rows.items():
            d=self.dispositions[rid]; e=self.editorial.get(rid,{})
            name=e['title'] if self.fresh(rid) else (row['claim'][:100] if d['decision']=='canonical' else 'пояснение требует пересмотра')
            index.append('| '+link(self.paths[rid],rid+' — '+name)+' | '+cell(DECISIONS.get(d['decision'],d['decision']))+' | '+cell(d['reason'])+' |')
            if d['decision']=='canonical': continue
            count+=1
            title=e['title'] if self.fresh(rid) else rid
            p=self.primary[rid]
            lines=[frontmatter(rid,[rid,rid.replace('-','_'),title],'research_proposal'),
                '# '+rid+' — '+title,link(INDEX,'Реестр предложений'),
                '## Что это',e['summary_ru'] if self.fresh(rid) else '> Пояснение требует пересмотра: изменился источник или решение. Ниже сохранены текущие исходные записи.',
                '## Место в ФТС',
                '| Поле | Запись источника |','|---|---|',
                '| Тип | '+cell(row['kind'])+' |',
                '| Происхождение | '+cell(row['origin'])+' |',
                '| Лестницы / уровни | '+cell(row['ladder']+' / '+row['levels'])+' |',
                '| Каноническое включение | Вне действующего набора CP-карточек source |',
                '## Точная формулировка',fenced(row['claim']),
                self.enc.source(p['source_file'],f'L{p["line_start"]}–L{p["line_end"]}'),
                '## Свойства и область',
                '| Положение | Область | Основание | Состояние |','|---|---|---|---|',
                '| '+cell(e['summary_ru'] if self.fresh(rid) else 'Пересказ временно отключён')+' | '+cell(e['scope_ru'] if self.fresh(rid) else 'см. текущие точные записи')+' | '+self.enc.source(p['source_file'])+' | '+cell(d['decision'])+' |',
                '## Связи',
                'Карточки, на которые ссылается реестр; смысл отношений не повышается до зависимости или тождества:']
            targets=[link(self.enc.paths[self.corpus.card_nodes[cid]],cid) for cid in (row.get('cards') or '').split(',') if cid in self.corpus.card_nodes]
            lines+=[' · '.join(targets) if targets else 'Прямая ссылка на карточку в этой строке не указана.']
            refs=sorted(set(re.findall(r'CP-\d{3}',d['reason']))-{rid})
            if refs: lines+=['Упомянуты в причине решения: '+' · '.join(link(self.paths[x],x) for x in refs if x in self.paths)]
            lines+=['Первичный документ: '+self.document_link(row['source'],link)]
            also=[x for x in (row.get('also') or '').split(';') if x]
            if also: lines+=['Дополнительный контекст: '+' · '.join(self.document_link(x,link) for x in also)]
            lines+=['## Пример',e.get('example_ru','Отдельный пример в этой записи реестра не приведён; дополнительные примеры следует читать в первичном документе.') if self.fresh(rid) else 'Редакторский пример временно отключён до пересмотра.',
                '## Ограничения и различия',e['scope_ru'] if self.fresh(rid) else 'Пояснение временно отключено.',
                '**Решение:** '+DECISIONS.get(d['decision'],d['decision'])+'. '+d['reason'],
                '## Основания и статус',
                '| Ось статуса | Состояние |','|---|---|',
                '| Каноническое включение | Вне действующего набора CP-карточек |',
                '| Авторское принятие | Не указано отдельным полем; исходный статус сохранён ниже |',
                '| St_FTS | не указано |',
                '| Математическая проверка | Список идентификаторов ниже; общий результат для всего предложения не указан |',
                '| Эмпирическая поддержка | не указано |',
                '**Статус в первичной строке реестра:** '+row['status'],
                '**Область решения 2026-10-18:** '+d['scope'],
                self.enc.source(BASE+'dispositions_2026-10-18.tsv',f'L{d["line_start"]}–L{d["line_end"]}'),
                'Перечисленные проверки относятся к собственным предикатам. Наличие идентификатора проверки не сообщает её результата и не является доказательством смыслового моста.',
                '**Проверки по реестру:** '+(row.get('checks') or 'не указано'),
                '### Дословные основания',fenced(p['exact_quote']),fenced(d['exact_quote']),
                '## Вопросы и мои заметки']
            qs=[q for q in (row.get('oq') or '').split(',') if q]
            lines+=[' · '.join(self.question_link(q,link) for q in qs) if qs else 'Открытый вопрос в этой строке не указан.',
                'DN: '+(row.get('dn') or 'не указано')+'. Личные комментарии храните в «08 — Мои заметки» со ссылкой на эту страницу.',
                '### Полная запись реестра',fenced(json.dumps(row,ensure_ascii=False,sort_keys=True,indent=2),'json')]
            expansion=self.corpus.render_facets(rid,link,cell,fenced)
            if expansion: lines.append(expansion)
            self.enc.files[self.paths[rid]]=blocks(lines)
            entry=(self.paths[rid],rid+' — '+title)
            if entry not in self.enc.sections[6]: self.enc.sections[6].append(entry)
        self.enc.files[INDEX]='\n\n'.join(index[:3])+'\n\n'+'\n'.join(index[3:])+'\n'
        self.enc.files['90 — Служебное/registry_mapping.json']=json.dumps({'mapping':self.paths,'outside_canon':count,
            'stale_editorial':self.stale,'primary':self.primary,'decisions':self.dispositions},ensure_ascii=False,sort_keys=True,indent=2)+'\n'
        return count

    def verify(self, files):
        errors=list(self.errors)
        for rid,d in self.dispositions.items():
            dest=self.paths.get(rid)
            if dest not in files: errors.append('Нет адреса CP: '+rid); continue
            if d['decision']!='canonical':
                if 'fts_id: '+json.dumps(rid,ensure_ascii=False) not in files[dest]: errors.append('Нет ID CP: '+rid)
                for quote in (self.rows[rid]['claim'],self.primary[rid]['exact_quote'],d['exact_quote']):
                    if quote not in files[dest]: errors.append('Потеряно точное основание CP: '+rid)
        return errors
