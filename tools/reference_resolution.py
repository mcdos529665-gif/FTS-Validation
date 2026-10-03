"""Explicit, witnessed resolution of FTS references; no inferred definitions."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'work/v14_rebuild/audit/REFERENCE_RESOLUTIONS.tsv'
KINDS = {'card_alias', 'sheet_record', 'document_fragment', 'document_set', 'scope', 'literal', 'missing', 'ambiguous'}


def load_resolutions(path: Path = REGISTRY) -> dict[str, dict[str, str]]:
    with path.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    result = {}
    for row in rows:
        raw = row['raw_reference']
        if not raw or raw in result:
            raise ValueError(f'Duplicate/empty reference resolution: {raw!r}')
        if row['resolution'] not in KINDS:
            raise ValueError(f'Unknown resolution kind for {raw}: {row["resolution"]}')
        if not all(row.get(key) for key in ('evidence', 'scope', 'status_effect')):
            raise ValueError(f'Unwitnessed reference resolution: {raw}')
        if row['resolution'] in {'missing', 'ambiguous'} and not row.get('next_step'):
            raise ValueError(f'Missing next step: {raw}')
        result[raw] = row
    return result


def fragment_witness(root: Path, row: dict[str, str]) -> tuple[str, object]:
    """Resolve an exact sheet key or unique document excerpt, never fuzzy text."""
    target = (root / row['target']).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        raise ValueError(f'Missing/outside reference target: {row["target"]}')
    locator = json.loads(row['locator'])
    if row['resolution'] == 'sheet_record':
        book = json.loads(target.read_text(encoding='utf-8'))
        sheets = [sheet for sheet in book['sheets'] if sheet['name'] == locator['sheet']]
        if len(sheets) != 1:
            raise ValueError(f'Nonunique sheet: {locator}')
        matches = [(number, values) for number, values in enumerate(sheets[0]['values'], 1)
                   if str(values[0]) == locator['key']]
        if len(matches) != 1:
            raise ValueError(f'Nonunique/missing sheet key: {row["raw_reference"]}: {locator}')
        number, values = matches[0]
        return f'sheet:{locator["sheet"]}:row:{number}:key:{locator["key"]}', values
    if row['resolution'] == 'document_fragment':
        lines = target.read_text(encoding='utf-8').splitlines()
        matches = [(number, text) for number, text in enumerate(lines, 1)
                   if locator['excerpt'] in text]
        if len(matches) != 1:
            raise ValueError(f'Nonunique/missing excerpt: {row["raw_reference"]}: {locator}')
        number, text = matches[0]
        return f'L{number}', text
    raise ValueError(f'Not a fragment resolution: {row["resolution"]}')


def validate_resolutions(root: Path, resolutions: dict[str, dict[str, str]], card_ids: set[str]) -> None:
    for raw, row in resolutions.items():
        kind = row['resolution']
        if kind == 'card_alias' and row['target'] not in card_ids:
            raise ValueError(f'Missing alias card: {raw} -> {row["target"]}')
        if kind in {'sheet_record', 'document_fragment'}:
            fragment_witness(root, row)
        if kind in {'scope', 'document_set'}:
            members = json.loads(row['target'])
            if not isinstance(members, list) or not members or len(members) != len(set(members)):
                raise ValueError(f'Invalid/nonunique reference collection: {raw}')
            for member in members:
                if kind == 'scope' and member not in card_ids:
                    raise ValueError(f'Missing scope card: {raw} -> {member}')
                if kind == 'document_set':
                    path = (root / member).resolve()
                    if not path.is_relative_to(root.resolve()) or not path.is_file():
                        raise ValueError(f'Missing/outside collection document: {raw} -> {member}')


def dependency_sets(cards: list[dict], triples: list[dict]) -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    """Compare all explicit prerequisites, including unresolved and fragment refs."""
    return (
        {(card['id'], dependency) for card in cards for dependency in card['depends_on']},
        {(row['subject'], row['object']) for row in triples if row['predicate'] == 'depends_on'},
    )


def dependency_cycles(edges: set[tuple[str, str]]) -> list[tuple[str, ...]]:
    """Tarjan SCCs over every stored prerequisite; relation back-links are excluded."""
    graph: dict[str, set[str]] = {}
    for source, target in edges:
        graph.setdefault(source, set()).add(target)
        graph.setdefault(target, set())
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    cycles: list[tuple[str, ...]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = low[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for neighbour in sorted(graph[node]):
            if neighbour not in indices:
                visit(neighbour)
                low[node] = min(low[node], low[neighbour])
            elif neighbour in on_stack:
                low[node] = min(low[node], indices[neighbour])
        if low[node] == indices[node]:
            component = []
            while True:
                item = stack.pop()
                on_stack.remove(item)
                component.append(item)
                if item == node:
                    break
            if len(component) > 1 or node in graph[node]:
                cycles.append(tuple(sorted(component)))

    for node in sorted(graph):
        if node not in indices:
            visit(node)
    return sorted(cycles)
