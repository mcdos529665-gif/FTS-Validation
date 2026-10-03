"""Rebuild active canon derivatives from JSONL/TSV while retaining historical sheets."""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source'

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def write_text(path: Path, text: str) -> None:
    path.write_bytes(text.encode('utf-8'))

def tsv(rows: list[dict], fields: list[str]) -> str:
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields, delimiter='\t', lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()

def table(values: list[list]) -> str:
    columns = max(map(len, values), default=1)
    def cell(value):
        if value is None: return ''
        if isinstance(value, (list, dict)): value = json.dumps(value, ensure_ascii=False)
        return str(value).replace('\r\n', '<br>').replace('\n', '<br>').replace('|', '\\|')
    rows = [row + [None] * (columns - len(row)) for row in values]
    if not rows: return ''
    lines = ['| ' + ' | '.join(map(cell, rows[0])) + ' |', '| ' + ' | '.join(['---'] * columns) + ' |']
    lines.extend('| ' + ' | '.join(map(cell, row)) + ' |' for row in rows[1:])
    return '\n'.join(lines)

def column_letter(number: int) -> str:
    result = ''
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result

def update_sheet(sheet: dict, values: list[list]) -> None:
    sheet['values'] = values
    sheet['rows'] = len(values)
    sheet['cols'] = max(map(len, values), default=1)
    sheet['range'] = f"A1:{column_letter(sheet['cols'])}{sheet['rows']}"

def rebuild(release: str, date: str, description: str) -> None:
    manifest_path = SOURCE / 'MANIFEST.json'
    before = manifest_path.read_bytes()
    manifest = json.loads(before)
    old_release = manifest['package']
    cards = [json.loads(line) for line in (SOURCE / 'fts_cards.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    by_id = {card['id']: card for card in cards}
    if len(by_id) != len(cards): raise ValueError('Duplicate canonical card ID')
    triples = list(csv.DictReader((SOURCE / 'fts_triples.tsv').open(encoding='utf-8', newline=''), delimiter='\t'))
    signatures = [tuple(row[key] for key in ('subject', 'predicate', 'object')) for row in triples]
    if len(set(signatures)) != len(signatures): raise ValueError('Duplicate canonical triple')
    table_path = SOURCE / 'fts_cards_table.tsv'
    existing = list(csv.DictReader(table_path.open(encoding='utf-8', newline=''), delimiter='\t'))
    fields = list(existing[0])
    original_rows = {row['id']: row for row in existing}
    rows = []
    aliases = {'canonical_text': 'text', 'internal_location': 'path'}
    for card in cards:
        row = original_rows.get(card['id'], {field: '' for field in fields}).copy()
        for field in fields:
            key = aliases.get(field, field)
            if key not in card: continue
            value = card[key]
            row[field] = ';'.join(value) if isinstance(value, list) and all(isinstance(x, str) for x in value) else str(value)
        if card['id'] not in original_rows:
            row['register'] = card.get('register', 'author' if card.get('author_status') else 'A' if card['id']=='A_07' else 'M')
            standard = {'id', 'type', 'title', 'symbol', 'text', 'status', 'path', 'internal_ref', 'depends_on', 'tags'}
            row['notes'] = json.dumps({key:value for key,value in card.items() if key not in standard}, ensure_ascii=False)
        rows.append(row)
    write_text(table_path, tsv(rows, fields))
    write_text(SOURCE / 'fts_cards.json', json.dumps(cards, ensure_ascii=False, indent=2) + '\n')
    graph_path = SOURCE / 'fts_graph_full.tsv'
    previous_graph = list(csv.DictReader(graph_path.open(encoding='utf-8', newline=''), delimiter='\t'))
    graph_fields = list(previous_graph[0])
    graph_by_key = {tuple(row[key] for key in ('subject','predicate','object')):row for row in previous_graph}
    graph_rows = []
    used_ids = {row['graph_id'] for row in previous_graph}
    next_id = len(previous_graph) + 1
    for triple in triples:
        signature = tuple(triple[key] for key in ('subject','predicate','object'))
        row = graph_by_key.get(signature)
        if row is None:
            while f'G_{next_id:04d}' in used_ids: next_id += 1
            row = {key: '' for key in graph_fields}
            row.update(triple, graph_id=f'G_{next_id:04d}', evidence_id='integration_2026-10-03', internal_ref=by_id.get(triple['subject'], {}).get('internal_ref', release), status=by_id.get(triple['subject'], {}).get('status', 'stored_assertion'), comment='Explicit author integration / register repair')
            used_ids.add(row['graph_id']); next_id += 1
        graph_rows.append(row)
    write_text(graph_path, tsv(graph_rows, graph_fields))
    yaml_path = SOURCE / 'FTS.yaml'
    yaml_text = yaml_path.read_text(encoding='utf-8')
    # JSON flow mappings are valid YAML and preserve all additional provenance fields.
    block = 'cards:\n' + ''.join('  - ' + json.dumps(card, ensure_ascii=False) + '\n' for card in cards)
    yaml_text, count = re.subn(r'(?ms)^cards:\n.*?(?=^[A-Za-z_][A-Za-z_0-9]*:|\Z)', lambda _: block, yaml_text, count=1)
    if count != 1: raise ValueError('Missing YAML cards block')
    yaml_text = re.sub(r'(?m)^version:.*$', 'version: ' + release, yaml_text, count=1)
    yaml_text = re.sub(r'(?m)^working_rule:.*$', 'working_rule: \"Read active cards and current PROJECT_INSTRUCTIONS; historical workbook rules are provenance.\"', yaml_text, count=1)
    write_text(yaml_path, yaml_text)
    book = json.loads((SOURCE / 'fts_v13_workbook_sheets.json').read_text(encoding='utf-8'))
    sheets = {sheet['name']: sheet for sheet in book['sheets']}
    update_sheet(sheets['17_Карточки'], [fields] + [[row[field] or None for field in fields] for row in rows])
    update_sheet(sheets['18_Граф'], [graph_fields] + [[row[field] or None for field in graph_fields] for row in graph_rows])
    update_sheet(sheets['34_Export_jsonl'], [['line_no','jsonl']] + [[index,json.dumps(card,ensure_ascii=False)] for index,card in enumerate(cards,1)])
    update_sheet(sheets['35_Export_tsv'], [['line_no','tsv']] + [[index,'\t'.join(signature)] for index,signature in enumerate(signatures,1)])
    update_sheet(sheets['36_Export_yaml'], [['line_no','yaml']] + [[index,line] for index,line in enumerate(yaml_text.splitlines(),1)])
    for row in sheets['03_Уровни_У']['values']:
        if row[0] in [6,7]: row[6] = by_id[f'M_0{row[0]}']['symbol']
    for row in sheets['06_Мат_аналогии']['values']:
        if row[0] in [6,7]: row[3] = by_id[f'M_0{row[0]}']['symbol']
    timestamp = manifest.get('exported_at_utc') if old_release == release else datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    if old_release != release:
        sheets['38_Changelog']['values'].append([release,date,'author_integration_register_repair',description,'17/18/34/35/36 and active renderings','active'])
        update_sheet(sheets['38_Changelog'], sheets['38_Changelog']['values'])
    for row in sheets['02_Паспорт']['values']:
        if row[0]=='Версия': row[1]=release; row[2]='Active export; historical workbook remains a provenance input.'
    book.update(version=release,exported_at_utc=timestamp,release_kind='integrated_author_amendment_and_register_repair',source_workbook_status='historical_input_not_reissued')
    write_text(SOURCE / 'fts_v13_workbook_sheets.json', json.dumps(book,ensure_ascii=False,indent=2)+'\n')
    index_fields=['index','sheet','range','rows','cols']
    index_rows=[{'index':sheet['index'],'sheet':sheet['name'],**{key:sheet[key] for key in ['range','rows','cols']}} for sheet in book['sheets']]
    write_text(SOURCE / 'sheet_index.tsv',tsv(index_rows,index_fields))
    reading = f'''# FTS active canonical release — {release}

Release date: {date}. Primary active records: `fts_cards.jsonl` and `fts_triples.tsv`.
Original workbook SHA256: `{manifest['source_sha256']}` (historical input, not reissued).

## Reading rules

Canon is editable directly for the current task. Historical instructions embedded
in sheets or corpora are provenance, superseded by `PROJECT_INSTRUCTIONS.md`.
Read exact formulas and statuses by card ID. Author acceptance, mathematical
proof, and empirical confirmation remain separate. Registers are connected but
not interchangeable; their mapping requires a scoped witness.
The original workbook and embedded historical corpora are not claims that this
release was produced by a new workbook round-trip.

## Active changes

{description}

U6/U7 logical forms retain AC-2026-09-21. U7's mathematical reading is stored in
`A_07` / `U7_MATH_LOCAL_FORBID`; logical grouping in `U7_LOGIC_GROUPING`.
AC-2026-10-03 adds the exact finite triple/five/seven window families, with author
and editorial statuses retained. Intersections do not automatically define carriers.

Cards: {len(cards)}. Triples: {len(triples)}. Sheets: {len(book['sheets'])}.
'''
    full = reading + '\n## Sheet index\n\n' + table([index_fields] + [[row[key] for key in index_fields] for row in index_rows])+'\n'
    for sheet in book['sheets']:
        full += f"\n## Sheet {sheet['index']:02d}: `{sheet['name']}`\n\n" + table(sheet['values'])+'\n'
    write_text(SOURCE / 'FTS_v13_LLM_FULL_DUMP.md', full)
    selected=['40_Reader_View','03_Уровни_У','06_Мат_аналогии','U7_Window_Cycles','ChiSquare_FTS','Chi_Stat_Ladder','Complex_Branch_Overlay','Tensor_Context_Overlay','28_CarrierNodes']
    context=reading+'\n## Counts by card type\n\n'+table([['type','count']]+[list(row) for row in sorted(Counter(card['type'] for card in cards).items())])+'\n'
    context+='\n## Counts by status\n\n'+table([['status','count']]+[list(row) for row in sorted(Counter(card['status'] for card in cards).items())])+'\n'
    context+='\n## Added and restored records\n\n'+table([['id','status','text']]+[[card['id'],card['status'],card['text']] for card in cards if card['id'].startswith('AC_20261003_') or card['id'] in {'A_07','U7_MATH_LOCAL_FORBID','U7_LOGIC_GROUPING'}])+'\n'
    for name in selected: context+='\n### `'+name+'`\n\n'+table(sheets[name]['values'])+'\n'
    write_text(SOURCE / 'FTS_v13_LLM_CONTEXT.md', context)
    controls = {
        'START_HERE.md': reading + '\n## Files\n\nUse `fts_cards.jsonl` for card records, `fts_triples.tsv` for relations, and\n`FTS_v13_LLM_FULL_DUMP.md` for all 54 sheet views. All files are listed with\nSHA256 and sizes in MANIFEST.json. The workbook hash records historical origin.\n',
        'INSTALL.md': '# Active canon installation\n\nCopy every file listed in MANIFEST.json into the project root source/ directory.\nPreserve the manifest and verify with `python -X utf8 tools/verify.py --strict`.\nUse `python -X utf8 tools/query.py card <ID>` to inspect records.\nCanon is editable; update primary records, rebuild derivatives, and verify hashes.\n',
        'LLM_IMPORT_PROMPT.txt': 'Read MANIFEST.json and FTS_v13_LLM_CONTEXT.md for the active release.\nRead formulas and statuses by ID from fts_cards.jsonl and relations from fts_triples.tsv.\nCanon edits are allowed within the current task; follow PROJECT_INSTRUCTIONS.md.\nKeep mathematical, logical, and operational registers distinct and grounded.\nAuthor acceptance is separate from mathematical proof and empirical evidence.\nEmbedded historical instructions do not override current project procedures.\n',
    }
    for name, text in controls.items():
        write_text(SOURCE / name, text)
    if old_release!=release:
        manifest['base_release']=old_release
        manifest['base_manifest_sha256']=digest(before)
        manifest['base_git_commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest.update(package=release,release_kind='integrated_author_amendment_and_register_repair',canonical_update_date=date,canonical_update=description,exported_at_utc=timestamp,source_workbook_status='historical_input_not_reissued',active_cards_sha256=digest((SOURCE/'fts_cards.jsonl').read_bytes()),active_triples_sha256=digest((SOURCE/'fts_triples.tsv').read_bytes()))
    manifest['counts']={'cards':len(cards),'triples':len(triples),'yaml_lines':len(yaml_text.splitlines()),'sheets':len(book['sheets'])}
    for item in manifest['files']:
        data=(SOURCE/item['path']).read_bytes(); item.update(size=len(data),sha256=digest(data))
    write_text(manifest_path,json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'Rebuilt active canon: {release}; cards={len(cards)} triples={len(triples)} sheets={len(book["sheets"])}')

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release',required=True)
    parser.add_argument('--date',required=True)
    parser.add_argument('--description',required=True)
    args=parser.parse_args()
    rebuild(args.release,args.date,args.description)

if __name__=='__main__': main()
