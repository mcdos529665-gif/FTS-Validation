"""Render current dependency consistency without replacing reviewed decisions."""
from __future__ import annotations
import csv
import io
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from reference_resolution import dependency_sets, dependency_cycles, load_resolutions

def main():
    source = ROOT / 'source'
    cards = [json.loads(line) for line in (source/'fts_cards.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    with (source/'fts_triples.tsv').open(encoding='utf-8', newline='') as stream:
        triples = list(csv.DictReader(stream, delimiter='\t'))
    left, right = dependency_sets(cards, triples)
    cycles = dependency_cycles(left | right)
    resolutions = load_resolutions()
    predicates = Counter(row['predicate'] for row in triples)
    manifest = json.loads((source/'MANIFEST.json').read_text(encoding='utf-8'))
    lines = [
        '# GRAPH AUDIT — active canonical release', '',
        'Релиз: `'+manifest['package']+'`. Полное сравнение включает адресаты-карточки, фрагменты и неразрешённые определения.', '',
        f'**Найдено.** {len(cards)} карточек, {len(triples)} триплетов; предикатов — {len(predicates)}.', '',
        f'**Зависимости.** JSONL: {len(left)}; TSV: {len(right)}; card-only={len(left-right)}, triple-only={len(right-left)}.', '',
        f'**Вывод.** Циклов предпосылок — {len(cycles)}. Обратные отношения applies_to/has_operator и принадлежность источнику сохраняются отдельно от depends_on.', '',
        '**Что не закрыто.** Lambda_link, TA1, U12_CHI_PI_BOUNDARY и NODE_SIGNATURES; определения и область должны быть восстановлены. Модели для двух causal/counterfactual требований также остаются обязательствами.', '',
        'Решения: [GRAPH_RELATION_PATCH.tsv](GRAPH_RELATION_PATCH.tsv), [DEPENDENCY_CYCLE_REVIEW.tsv](DEPENDENCY_CYCLE_REVIEW.tsv), [REFERENCE_RESOLUTIONS.tsv](REFERENCE_RESOLUTIONS.tsv).',
        'Полный разбор: [GRAPH_RECONCILIATION_2026-10-03](../../project_consistency/GRAPH_RECONCILIATION_2026-10-03.md).', '',
        '## Предикаты', '', '| Предикат | Число |', '|---|---:|',
    ]
    lines.extend(f'| `{predicate}` | {count} |' for predicate,count in sorted(predicates.items()))
    lines += ['', '## Циклы depends_on', '']
    lines.extend('- `'+ ' ↔ '.join(component)+'`' for component in cycles)
    if not cycles: lines.append('Не обнаружены.')
    lines += ['', '## Реестр исходных 34 ссылок', '', '| Решение | Число |', '|---|---:|']
    lines.extend(f'| `{kind}` | {count} |' for kind,count in sorted(Counter(row['resolution'] for row in resolutions.values()).items()))
    (HERE/'GRAPH_AUDIT.md').write_text('\n'.join(lines)+'\n', encoding='utf-8', newline='\n')
    pending = []
    for operation,edges in [('ADD_TRIPLE',left-right),('REVIEW_TRIPLE',right-left)]:
        pending.extend({'operation':operation,'subject':a,'predicate':'depends_on','object':b} for a,b in sorted(edges))
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream,fieldnames=['operation','subject','predicate','object'],delimiter='\t',lineterminator='\n')
    writer.writeheader(); writer.writerows(pending)
    (HERE/'PENDING_GRAPH_RELATION_PATCH.tsv').write_bytes(stream.getvalue().encode('utf-8'))
    print(f'Graph audit: drift={len(left-right)}/{len(right-left)}, cycles={len(cycles)}; reviewed ledger preserved')

if __name__ == '__main__': main()
