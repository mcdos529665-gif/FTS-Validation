# -*- coding: utf-8 -*-
"""Построить отчёт структуры канона и patch-план графа будущего v14.

Файл ``source/`` только читается. Выходы создаются в ``audit/``.
"""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "source"

# Эти отношения имеют буквальный объект или идентификатор области, а не ссылку
# на карточку. ``supports`` может также указывать карточку, поэтому его объект
# классифицируется по фактическому наличию ID.
LITERAL_PREDICATES = {
    "has_window",
    "has_antimode",
    "supports",
    "candidate_supports",
    "defeats_or_tests",
    "exports_to",
    "requires",
}
MIXED_PREDICATES = {"does_not_promote_above"}


def read_cards() -> list[dict]:
    return [
        json.loads(line)
        for line in (SOURCE / "fts_cards.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def read_triples() -> list[dict[str, str]]:
    with (SOURCE / "fts_triples.tsv").open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def strongly_connected(graph: dict[str, set[str]]) -> list[list[str]]:
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    components: list[list[str]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = low[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for neighbour in graph[node]:
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
                components.append(sorted(component))

    for node in sorted(graph):
        if node not in indices:
            visit(node)
    return sorted(components)


def main() -> None:
    cards = read_cards()
    triples = read_triples()
    ids = {card["id"] for card in cards}
    predicates = Counter(row["predicate"] for row in triples)
    entity_objects = Counter()
    literal_objects = Counter()
    for row in triples:
        if row["object"] in ids:
            entity_objects[row["predicate"]] += 1
        else:
            literal_objects[row["predicate"]] += 1

    card_deps = {
        (card["id"], dependency)
        for card in cards
        for dependency in card.get("depends_on", [])
        if dependency in ids
    }
    triple_deps = {
        (row["subject"], row["object"])
        for row in triples
        if row["predicate"] == "depends_on" and row["subject"] in ids and row["object"] in ids
    }
    card_only = sorted(card_deps - triple_deps)
    triple_only = sorted(triple_deps - card_deps)

    graph: dict[str, set[str]] = defaultdict(set)
    for source, target in card_deps:
        graph[source].add(target)
    for identifier in ids:
        graph[identifier]
    cycles = strongly_connected(graph)

    with (HERE / "GRAPH_RELATION_PATCH.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["operation", "subject", "predicate", "object", "reason", "target_release"])
        for subject, obj in card_only:
            writer.writerow([
                "ADD_TRIPLE",
                subject,
                "depends_on",
                obj,
                "card.depends_on exists but TSV edge is absent",
                "future_v14_export",
            ])
        for subject, obj in triple_only:
            writer.writerow([
                "REVIEW_TRIPLE",
                subject,
                "depends_on",
                obj,
                "TSV edge is absent from card.depends_on; reconcile against workbook",
                "future_v14_export",
            ])

    lines = [
        "# GRAPH AUDIT — v13 immutable export",
        "",
        "## Найдено → зависимости → вывод → что не закрыто",
        "",
        f"**Найдено.** Канон содержит {len(cards)} карточку и {len(triples)} триплетов; "
        f"уникальных предикатов — {len(predicates)}, дубликатов триплетов — "
        f"{len(triples) - len({(r['subject'], r['predicate'], r['object']) for r in triples})}.",
        "",
        "**Зависимости.** Ссылкой на сущность считается объект, совпадающий с ID карточки. "
        "Буквальные объекты (`has_window`, `has_antimode`, scope labels, имена файлов и "
        "формулировки требований) не объявляются битой ссылкой. Все неразрешённые entity-ссылки "
        "перечислены в `CANON_REFERENCE_PATCH.tsv`.",
        "",
        f"**Вывод.** JSONL `depends_on` содержит {len(card_deps)} разрешённых entity-рёбер, TSV — "
        f"{len(triple_deps)}. В TSV отсутствует {len(card_only)} карточных рёбер; {len(triple_only)} "
        "TSV-ребро отсутствует в карточке. Это P2-разрыв двух представлений, а не основание "
        "молча считать TSV полным графом. Механический patch-план записан в `GRAPH_RELATION_PATCH.tsv`.",
        "",
        "**Что не закрыто.** `source/` неизменяем. Применение patch-плана требует нового workbook "
        "round-trip и MANIFEST; циклы должны быть подтверждены автором как взаимные определения "
        "или разорваны направленным основанием.",
        "",
        "## Предикаты и тип объектов",
        "",
        "| Предикат | Всего | Entity-ID | Literal/неразрешённый | Правило |",
        "|---|---:|---:|---:|---|",
    ]
    for predicate in sorted(predicates):
        if predicate in LITERAL_PREDICATES:
            rule = "literal/mixed по фактическому ID"
        elif predicate in MIXED_PREDICATES:
            rule = "entity или literal scope"
        else:
            rule = "entity reference"
        lines.append(
            f"| `{predicate}` | {predicates[predicate]} | {entity_objects[predicate]} | "
            f"{literal_objects[predicate]} | {rule} |"
        )

    lines += [
        "",
        "## Циклы card.depends_on",
        "",
    ]
    for component in cycles:
        lines.append(f"- `{' ↔ '.join(component)}`")
    lines += [
        "",
        "Три SCC не являются вычислительной ошибкой, но опровергают предположение, что "
        "`depends_on` уже является DAG. До авторского решения они маркируются как P2 и не "
        "используются для доказательства порядка оснований.",
        "",
        "## Асимметрия depends_on",
        "",
        f"- Card-only edges: {len(card_only)} (`ADD_TRIPLE` в patch-плане).",
        f"- Triple-only edges: {len(triple_only)} (`REVIEW_TRIPLE` в patch-плане).",
    ]
    for subject, obj in triple_only:
        lines.append(f"- Конфликт: `{subject} →depends_on→ {obj}` есть только в TSV.")
    lines.append("")
    (HERE / "GRAPH_AUDIT.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
