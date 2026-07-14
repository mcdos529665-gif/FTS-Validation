# -*- coding: utf-8 -*-
"""Единый поиск крупных внешних входов аудита.

RadioML не является частью git-репозитория. Порядок поиска:
1) ``FTS_RADIOML_PATH`` (путь к файлу либо каталогу);
2) историческое расположение внутри worktree;
3) общий Windows-кэш на ``E:``.
"""
from __future__ import annotations

import os
from pathlib import Path


RADIOML_FILENAME = "RML2016.10a_dict.pkl"
RADIOML_EXPECTED_SIZE = 640_919_653
RADIOML_EXPECTED_SHA256 = "b29ccc25b00d0718cd3b70ffa9158662ec83f6d9b63ffd845c7bcbe3b3096e8c"
RADIOML_ENV = "FTS_RADIOML_PATH"

AUDIT_DIR = Path(__file__).resolve().parent
REBUILD_DIR = AUDIT_DIR.parent
RADIOML_LOCAL = REBUILD_DIR / "d10_phase" / "radioml" / RADIOML_FILENAME
RADIOML_E_DRIVE = Path("E:/FTS-data/RadioML") / RADIOML_FILENAME


def _environment_path() -> Path | None:
    raw = os.environ.get(RADIOML_ENV, "").strip().strip('"')
    if not raw:
        return None
    path = Path(os.path.expandvars(raw)).expanduser()
    if path.is_file() or path.name.casefold() == RADIOML_FILENAME.casefold():
        return path
    if path.is_dir() or not path.suffix:
        return path / RADIOML_FILENAME
    return path


def radioml_candidates() -> tuple[Path, ...]:
    candidates = [_environment_path(), RADIOML_LOCAL]
    if os.name == "nt":
        candidates.append(RADIOML_E_DRIVE)

    unique: list[Path] = []
    seen: set[str] = set()
    for path in candidates:
        if path is None:
            continue
        key = str(path).casefold()
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return tuple(unique)


def resolve_radioml_path() -> Path:
    """Вернуть заданный env-путь либо первый существующий fallback.

    Явно заданный, но ошибочный ``FTS_RADIOML_PATH`` не маскируется fallback-ом.
    """
    environment = _environment_path()
    if environment is not None:
        return environment
    for path in radioml_candidates():
        if path.is_file():
            return path
    return RADIOML_LOCAL


def radioml_search_summary() -> str:
    return "; ".join(str(path) for path in radioml_candidates())
