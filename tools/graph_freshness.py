"""Свежесть производного графа graphify относительно его входов.

Сравнивает SHA256 входов сборки из graphify-out/build_manifest.json (поле
inputs) с текущим содержимым файлов. Изменённый или отсутствующий вход
означает, что граф собран по другой версии файла: ответ из graph.json по
такому файлу сначала сверяется с каноном (query.py card / context).

Ограничение: новые файлы, которых не было среди входов сборки, здесь не видны
(состав входов задаёт детектор graphify с .graphifyignore и .git/info/exclude).
FRESH означает «записанные входы не изменились», а не «граф покрывает весь проект».

Выход: 0 — все входы совпадают; 1 — есть расхождения; 2 — манифест не прочитан.
Только чтение: ничего не пересобирает и не записывает.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "graphify-out" / "build_manifest.json"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classify(root: Path, inputs: dict[str, dict]) -> tuple[list[str], list[str], int]:
    changed: list[str] = []
    missing: list[str] = []
    for relative, record in sorted(inputs.items()):
        path = root / relative
        if not path.is_file():
            missing.append(relative)
        elif sha256_of(path) != record["sha256"]:
            changed.append(relative)
    return changed, missing, len(inputs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="корень проекта (по умолчанию этот репозиторий)")
    parser.add_argument("--manifest", type=Path, default=MANIFEST, help="путь к build_manifest.json")
    parser.add_argument("--verbose", action="store_true", help="перечислить все расхождения, а не первые 20")
    args = parser.parse_args()

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        inputs = manifest["inputs"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR манифест не прочитан: {exc}")
        return 2

    changed, missing, total = classify(args.root.resolve(), inputs)
    status = "FRESH" if not changed and not missing else "STALE"
    print(
        f"{status} graph inputs: {total} проверено; изменено={len(changed)}; "
        f"отсутствует={len(missing)}; source_commit={manifest.get('source_commit', 'нет')}"
    )
    limit = None if args.verbose else 20
    for label, items in (("CHANGED", changed), ("MISSING", missing)):
        for relative in items[:limit]:
            print(f"  {label} {relative}")
        if limit is not None and len(items) > limit:
            print(f"  {label} ... ещё {len(items) - limit} (запусти с --verbose)")
    return 0 if status == "FRESH" else 1


if __name__ == "__main__":
    sys.exit(main())
