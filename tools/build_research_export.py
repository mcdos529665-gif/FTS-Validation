#!/usr/bin/env python3
"""Детерминированная сборка единой исследовательской выгрузки ФТС для ИИ."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "work" / "v14_rebuild" / "export" / "FTS_research_project_for_AI.md"

PROJECT_INSTRUCTIONS = Path("PROJECT_INSTRUCTIONS.md")
STATE = Path("work/STATE.md")
NOTATION = Path("work/notation.md")
DECISIONS = Path("work/DECISIONS.md")
OPEN_QUESTIONS = Path("work/OPEN_QUESTIONS.md")
EXTERNAL_CONFLICTS = Path("work/EXTERNAL_CONFLICTS.md")

V14_PAPER = Path("work/v14_rebuild/FTS_v14_paper.md")
REGISTER_MAP = Path("work/v14_rebuild/FTS_v14_register_map.md")
STATUS_PATCH = Path("work/v14_rebuild/status_patch_v14.md")
RED_TEAM = Path("work/v14_rebuild/red_team_F3.md")
VERIFICATION_REPORT = Path("work/v14_rebuild/verification_report.md")
VERIFICATION_CODE = Path("work/v14_rebuild/verification.py")
EXTERNAL_BRIDGE_U1_U5 = Path("work/v14_rebuild/external_bridge_u1_u5.md")
CODE_INFORMATION_RECODE = Path("work/v14_rebuild/code_information_recode_note.md")
NEW_CONNECTIONS_REPORT = Path("work/v14_rebuild/NEW_CONNECTIONS_REPORT.md")
NEW_CONNECTIONS_CHECK = Path("work/v14_rebuild/check_new_connections.py")

E5_ROOT = Path("work/v14_rebuild/e5_literature_review")
E5_PROTOCOL = E5_ROOT / "PROTOCOL.md"
E5_STATUS = E5_ROOT / "WAVE_0_STATUS.md"
E5_AUTHOR_CYCLE_AMENDMENT = E5_ROOT / "PROTOCOL_AMENDMENT_005_AUTHOR_CYCLE.md"
E5_SYNTHESIS = E5_ROOT / "SYNTHESIS.md"
E5_NOVELTY_BOUNDARY = E5_ROOT / "NOVELTY_BOUNDARY.md"
E5_COUPLING = E5_ROOT / "COUPLING_MAP.md"
E5_SEEDS = E5_ROOT / "seed_set.bib"
E5_CANDIDATES = E5_ROOT / "CANDIDATES.tsv"
E5_BLACKWELL_AMENDMENT = E5_ROOT / "PROTOCOL_AMENDMENT_003.md"
E5_BLACKWELL_BRIDGE = E5_ROOT / "BLACKWELL_BRIDGE.md"
E5_BLACKWELL_REPORT = E5_ROOT / "BLACKWELL_BRIDGE_REPORT.md"
E5_BLACKWELL_CHECK = E5_ROOT / "check_blackwell_bridge.py"
E5_ABSENCE_LIFT_AMENDMENT = E5_ROOT / "PROTOCOL_AMENDMENT_004.md"
E5_TYPED_ABSENCE = E5_ROOT / "TYPED_ABSENCE_BRIDGE.md"
E5_LIFT_TYPING = E5_ROOT / "LIFT_TYPING_PROJECT.md"
E5_ABSENCE_LIFT_REPORT = E5_ROOT / "ABSENCE_LIFT_REPORT.md"
E5_ABSENCE_LIFT_CHECK = E5_ROOT / "check_absence_lift_projects.py"
E5_EXPLICIT_ADDITIONS = E5_ROOT / "EXPLICIT_ADDITIONS_2026-09-05.md"
E5_EXPLICIT_ADDITIONS_REPORT = E5_ROOT / "EXPLICIT_ADDITIONS_REPORT.md"
E5_EXPLICIT_ADDITIONS_CHECK = E5_ROOT / "check_explicit_additions.py"
E5_DEEP_RESEARCH_REQUESTS = E5_ROOT / "DEEP_RESEARCH_REQUESTS_CONNECTIVITY.md"
DR_CORE = E5_ROOT / "dr_core_2026-09-11"
DR_CORE_REVIEW = DR_CORE / "REVIEW.md"
DR_CORE_SOURCES = DR_CORE / "SOURCE_AUDIT.md"
DR_CORE_ROUTING = DR_CORE / "CONFLICT_ROUTING.md"
DR_CORE_REPORT = DR_CORE / "CHECK_REPORT.md"
DR_CORE_CHECK = DR_CORE / "check_core.py"
DR_CORE_MANIFEST = DR_CORE / "INPUT_MANIFEST.json"
RD_ROOT = Path("work/v14_rebuild/recursive_distinction_2026-09-12")
RD_REVIEW = RD_ROOT / "REVIEW.md"
RD_QUESTIONS = RD_ROOT / "AUTHOR_QUESTIONS.md"
RD_REPORT = RD_ROOT / "CHECK_REPORT.md"
RD_CHECK = RD_ROOT / "check_note.py"
RD_MANIFEST = RD_ROOT / "INPUT_MANIFEST.json"
RD_ORIGINAL = RD_ROOT / "SOURCE_ORIGINAL.txt"
INTERPRETATION_ROOT = Path("work/v14_rebuild/interpretation_descent_undermind_2026-09-12")
INTERPRETATION_REVIEW = INTERPRETATION_ROOT / "REVIEW.md"
INTERPRETATION_MATRIX = INTERPRETATION_ROOT / "EVIDENCE_MATRIX.md"
INTERPRETATION_AUDIT = INTERPRETATION_ROOT / "SOURCE_AUDIT.md"
INTERPRETATION_PROTOCOL = INTERPRETATION_ROOT / "PROTOCOL.md"
NONARBITRARY_ROOT = Path("work/v14_rebuild/nonarbitrariness_dialogue_2026-09-13")
NONARBITRARY_REVIEW = NONARBITRARY_ROOT / "REVIEW.md"
NONARBITRARY_CLAIMS = NONARBITRARY_ROOT / "CLAIM_MAP.md"
NONARBITRARY_MANIFEST = NONARBITRARY_ROOT / "INPUT_MANIFEST.json"
NONARBITRARY_ORIGINAL = NONARBITRARY_ROOT / "SOURCE_ORIGINAL.txt"
U6_RANDOM_REGULARITY = Path("work/v14_rebuild/U6_RANDOM_REGULARITY_2026-09-13.md")
AUTHOR_CYCLE_CHARTER = Path("work/v14_rebuild/AUTHOR_CYCLE_CHARTER_2026-09-13.md")
TRAIN_REFLECTION_DRAFT = Path("work/v14_rebuild/TRAIN_REFLECTION_TEST_DRAFT_2026-09-14.md")
TRAIN_REFLECTION_ROOT = Path("work/v14_rebuild/train_reflection")
TRAIN_REFLECTION_PROTOCOL = TRAIN_REFLECTION_ROOT / "PROTOCOL.md"
TRAIN_REFLECTION_PROTOCOL_V2_DRAFT = TRAIN_REFLECTION_ROOT / "PROTOCOL_V2_DRAFT_2026-09-15.md"
TRAIN_REFLECTION_PROGRAM = TRAIN_REFLECTION_ROOT / "run_reflection.py"
TRAIN_REFLECTION_RESULTS_MD = TRAIN_REFLECTION_ROOT / "RESULTS.md"
TRAIN_REFLECTION_RESULTS_JSON = TRAIN_REFLECTION_ROOT / "results.json"
DIALOGUE_SEMANTICS_NOTE = Path("work/v14_rebuild/dialogue_semantics_2026-09-15.md")
AUTHOR_CANON_INDEX = Path("work/AUTHOR_CANON.md")
AUTHOR_CANON_ROOT = Path("work/author_canon/2026-09-21")
AUTHOR_CANON_INPUTS = tuple(AUTHOR_CANON_ROOT / name for name in (
    "AMENDMENT.md", "AUTHOR_MESSAGE.txt", "INHERITED_AUTHOR_MESSAGE.txt",
    "INHERITED_AUTHOR_CLARIFICATION.txt",
    "cards.jsonl", "triples.tsv", "MANIFEST.json", "check_scope.py",
))
NEURAL_ANALOGY_ROOT = Path("work/v14_rebuild/neural_analogy_2026-09-19")
NEURAL_ANALOGY_REVIEW = NEURAL_ANALOGY_ROOT / "REVIEW.md"
NEURAL_ANALOGY_AUTHOR_MESSAGE = NEURAL_ANALOGY_ROOT / "AUTHOR_MESSAGE.txt"
NEURAL_ANALOGY_CHECK = NEURAL_ANALOGY_ROOT / "check_examples.py"

SOURCE_MANIFEST = Path("source/MANIFEST.json")
CANON_CONTEXT = Path("source/FTS_v13_LLM_CONTEXT.md")
CANON_FULL_DUMP = Path("source/FTS_v13_LLM_FULL_DUMP.md")
CANON_CARDS = Path("source/fts_cards.jsonl")
CANON_TRIPLES = Path("source/fts_triples.tsv")

INPUT_PATHS = (
    Path("tools/build_research_export.py"),
    PROJECT_INSTRUCTIONS,
    STATE,
    NOTATION,
    DECISIONS,
    OPEN_QUESTIONS,
    EXTERNAL_CONFLICTS,
    V14_PAPER,
    REGISTER_MAP,
    STATUS_PATCH,
    RED_TEAM,
    VERIFICATION_REPORT,
    VERIFICATION_CODE,
    EXTERNAL_BRIDGE_U1_U5,
    CODE_INFORMATION_RECODE,
    NEW_CONNECTIONS_REPORT,
    NEW_CONNECTIONS_CHECK,
    E5_PROTOCOL,
    E5_STATUS,
    E5_AUTHOR_CYCLE_AMENDMENT,
    E5_SYNTHESIS,
    E5_NOVELTY_BOUNDARY,
    E5_COUPLING,
    E5_SEEDS,
    E5_CANDIDATES,
    E5_BLACKWELL_AMENDMENT,
    E5_BLACKWELL_BRIDGE,
    E5_BLACKWELL_REPORT,
    E5_BLACKWELL_CHECK,
    E5_ABSENCE_LIFT_AMENDMENT,
    E5_TYPED_ABSENCE,
    E5_LIFT_TYPING,
    E5_ABSENCE_LIFT_REPORT,
    E5_ABSENCE_LIFT_CHECK,
    E5_EXPLICIT_ADDITIONS,
    E5_EXPLICIT_ADDITIONS_REPORT,
    E5_EXPLICIT_ADDITIONS_CHECK,
    E5_DEEP_RESEARCH_REQUESTS,
    DR_CORE_REVIEW,
    DR_CORE_SOURCES,
    DR_CORE_ROUTING,
    DR_CORE_REPORT,
    DR_CORE_CHECK,
    DR_CORE_MANIFEST,
    RD_REVIEW,
    RD_QUESTIONS,
    RD_REPORT,
    RD_CHECK,
    RD_MANIFEST,
    RD_ORIGINAL,
    INTERPRETATION_REVIEW,
    INTERPRETATION_MATRIX,
    INTERPRETATION_AUDIT,
    INTERPRETATION_PROTOCOL,
    NONARBITRARY_REVIEW,
    NONARBITRARY_CLAIMS,
    NONARBITRARY_MANIFEST,
    NONARBITRARY_ORIGINAL,
    U6_RANDOM_REGULARITY,
    AUTHOR_CYCLE_CHARTER,
    TRAIN_REFLECTION_DRAFT,
    TRAIN_REFLECTION_PROTOCOL,
    TRAIN_REFLECTION_PROTOCOL_V2_DRAFT,
    TRAIN_REFLECTION_PROGRAM,
    TRAIN_REFLECTION_RESULTS_MD,
    TRAIN_REFLECTION_RESULTS_JSON,
    DIALOGUE_SEMANTICS_NOTE,
    AUTHOR_CANON_INDEX,
    *AUTHOR_CANON_INPUTS,
    NEURAL_ANALOGY_REVIEW,
    NEURAL_ANALOGY_AUTHOR_MESSAGE,
    NEURAL_ANALOGY_CHECK,
    SOURCE_MANIFEST,
    CANON_CONTEXT,
    CANON_FULL_DUMP,
    CANON_CARDS,
    CANON_TRIPLES,
)

FORBIDDEN_MARKERS = (
    "E:/torrent",
    "E:\\torrent",
    "source.en.md",
    "DOSSIER.ru.md",
    "cdn-mineru",
    "papers/E5-H",
)

REQUIRED_HEADINGS = (
    "## 1. Паспорт выгрузки и правила чтения",
    "## 2. Текущее состояние проекта",
    "## 3. Основной исследовательский текст v14",
    "## 4. Нотация, карты и статусный патч",
    "## 5. Критика и машинная верификация",
    "## 6. Решения и открытые вопросы",
    "## 7. Внешний исследовательский контур E5",
    "## 8. Компактный контекст канона v13",
    "## 9. Полный 54-листовый дамп канона v13",
    "## 10. Машиночитаемые приложения",
)

RELATION_ROLES = {
    "direct": "прямой методологический контроль или основание проверки",
    "limiting": "ограничивает сильный перенос внешнего результата в ФТС",
    "alternative": "задаёт альтернативный формализм или baseline",
    "analogy": "допускается только как аналогия",
}


class ExportError(RuntimeError):
    """Ошибка состава или проверки исследовательской выгрузки."""


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")


def read_text(relative: Path) -> str:
    path = ROOT / relative
    if not path.is_file():
        raise ExportError(f"отсутствует обязательный вход: {relative.as_posix()}")
    return normalize_text(path.read_text(encoding="utf-8"))


def file_sha256(relative: Path) -> str:
    digest = hashlib.sha256()
    with (ROOT / relative).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def demote_headings(text: str, levels: int) -> str:
    """Понизить Markdown-заголовки, не меняя fenced code blocks."""

    lines: list[str] = []
    fence: str | None = None
    for line in normalize_text(text).split("\n"):
        stripped = line.lstrip()
        fence_match = re.match(r"(`{3,}|~{3,})", stripped)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            lines.append(line)
            continue
        if fence is None:
            match = re.match(r"^(#{1,6})(\s+.*)$", line)
            if match:
                count = min(6, len(match.group(1)) + levels)
                line = "#" * count + match.group(2)
        lines.append(line)
    return "\n".join(lines)


def markdown_source(title: str, relative: Path, *, heading_levels: int = 3) -> str:
    body = demote_headings(read_text(relative), heading_levels)
    return (
        f"### {title}\n\n"
        f"*Источник сборки: `{relative.as_posix()}`.*\n\n"
        f"{body}"
    )


def current_state() -> str:
    text = read_text(STATE)
    return text.split("\n## Лог сессий", 1)[0].rstrip()


def verification_counts() -> tuple[int, int, int]:
    report = read_text(VERIFICATION_REPORT)
    match = re.search(r"\*\*Итог:\s*(\d+)\s+PASS\s*/\s*(\d+)\s+FAIL\s+из\s+(\d+)\*\*", report)
    if not match:
        raise ExportError("не удалось извлечь итог машинной верификации")
    return tuple(int(value) for value in match.groups())


def source_counts() -> tuple[int, int, int, str]:
    data = json.loads(read_text(SOURCE_MANIFEST))
    counts = data["counts"]
    return (
        int(counts["cards"]),
        int(counts["triples"]),
        int(counts["sheets"]),
        str(data["source_sha256"]),
    )


def input_manifest_table() -> str:
    rows = [
        "| Входной артефакт | SHA256 |",
        "|---|---|",
    ]
    for relative in INPUT_PATHS:
        rows.append(f"| `{relative.as_posix()}` | `{file_sha256(relative)}` |")
    return "\n".join(rows)


def bib_entries() -> list[dict[str, str]]:
    text = read_text(E5_SEEDS)
    blocks = re.findall(r"(?ms)^@(\w+)\{([^,]+),(.*?)(?=^@\w+\{|\Z)", text)
    entries: list[dict[str, str]] = []
    for entry_type, key, body in blocks:
        fields: dict[str, str] = {"entry_type": entry_type, "key": key.strip()}
        for name in ("author", "title", "journal", "year", "doi"):
            match = re.search(
                rf"(?mi)^\s*{name}\s*=\s*(?:\{{([^}}]*)\}}|\"([^\"]*)\")\s*,?\s*$",
                body,
            )
            if match:
                fields[name] = normalize_text(match.group(1) or match.group(2)).strip()
        if "doi" not in fields:
            raise ExportError(f"BibTeX-запись {key.strip()} не содержит DOI")
        fields["doi_normalized"] = fields["doi"].lower().removeprefix("https://doi.org/")
        entries.append(fields)
    if not entries:
        raise ExportError("seed_set.bib не содержит записей")
    return entries


def candidate_records() -> dict[str, dict[str, str]]:
    path = ROOT / E5_CANDIDATES
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    by_doi: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        doi = row["doi"].lower().removeprefix("https://doi.org/").strip()
        if doi:
            by_doi.setdefault(doi, []).append(row)
    selected: dict[str, dict[str, str]] = {}
    for doi, candidates in by_doi.items():
        selected[doi] = sorted(
            candidates,
            key=lambda row: (
                not row["record_id"].startswith("E5-H"),
                row["screening_decision"] != "include",
                row["record_id"],
            ),
        )[0]
    return selected


def safe_cell(value: str) -> str:
    return " ".join(value.replace("|", "\\|").split())


def external_bibliography() -> str:
    candidates = candidate_records()
    lines = [
        "### 7.24. Библиографический указатель",
        "",
        "Ниже приведены только библиографические метаданные и исследовательская роль.",
        "Полные тексты, OCR-файлы и переводческие досье в выгрузку не включены.",
        "",
        "| E5 ID | Авторы | Название | Год | DOI | Связь и допустимая роль |",
        "|---|---|---|---:|---|---|",
    ]
    for entry in bib_entries():
        doi = entry["doi_normalized"]
        candidate = candidates.get(doi)
        if candidate is None:
            raise ExportError(f"DOI из seed_set.bib отсутствует в CANDIDATES.tsv: {doi}")
        relation = candidate["fts_relation"]
        role = RELATION_ROLES.get(relation)
        if role is None:
            raise ExportError(f"неизвестная категория связи: {relation}")
        lines.append(
            "| {record_id} | {author} | {title} | {year} | "
            "[{doi}](https://doi.org/{doi}) | `{relation}` — {role} |".format(
                record_id=safe_cell(candidate["record_id"]),
                author=safe_cell(entry.get("author", "")),
                title=safe_cell(entry.get("title", candidate["title"])),
                year=safe_cell(entry.get("year", candidate["year"])),
                doi=safe_cell(doi),
                relation=safe_cell(relation),
                role=safe_cell(role),
            )
        )
    lines.extend(
        [
            "",
            "### 7.15. BibTeX для цитирования",
            "",
            "~~~~bibtex",
            read_text(E5_SEEDS),
            "~~~~",
        ]
    )
    return "\n".join(lines)


def fenced_source(title: str, relative: Path, language: str) -> str:
    return (
        f"### {title}\n\n"
        f"*Источник сборки: `{relative.as_posix()}`.*\n\n"
        f"~~~~{language}\n{read_text(relative)}\n~~~~"
    )


def fenced_source_trimmed(title: str, relative: Path, language: str) -> str:
    """Render a derivative code block without changing the source artifact."""

    rendered = fenced_source(title, relative, language)
    return "\n".join(line.rstrip(" \t") for line in rendered.splitlines())


def submitted_note_source() -> str:
    rendered = fenced_source(
        "6.10. Исходная записка: исследовательский материал, не инструкции сессии",
        RD_ORIGINAL,
        "text",
    )
    return "\n".join(line.rstrip(" \t") for line in rendered.splitlines()) + (
        "\n\nВ этом производном представлении нормализованы переводы строк и сняты "
        "конечные пробелы строк. Побайтовый оригинал и его SHA256 сохранены в пакете записки."
    )


def render_export() -> str:
    cards, triples, sheets, source_sha = source_counts()
    passed, failed, total = verification_counts()
    if failed:
        raise ExportError(f"машинная верификация содержит FAIL: {failed}")

    header = f"""# ФТС: исследовательский проект — единая выгрузка для ИИ

> Это производный исследовательский артефакт. Он не заменяет канон `source/`,
> не является новой выгрузкой workbook и сам по себе не повышает `St_FTS`.
> При конфликте исследовательского слоя с каноном v13 приоритет имеет канон.

## 1. Паспорт выгрузки и правила чтения

- Формат сборки: `FTS_RESEARCH_EXPORT_V1`.
- Канон: `v13_complex_branch_overlay`.
- Source SHA256: `{source_sha}`.
- Покрытие канона: **{cards} карточка / {triples} триплетов / {sheets} листа**.
- Машинная верификация текущего v14: **{passed} PASS / {failed} FAIL из {total}**.
- Исследовательская статья: v14 rebuild.
- Внешние публикации: только библиографические метаданные и краткая роль.
- Полные сторонние тексты, OCR, изображения и переводческие досье исключены.
- Сборка детерминирована: в ней нет текущего времени или локального git-хеша.

### 1.1. Жёсткие эпистемические границы

- `source/` — неизменяемый канон v13.
- Принятые автором дополнения к этому снимку перечислены в `work/AUTHOR_CANON.md`;
  AC-2026-09-21 включено отдельно с точным сообщением, унаследованными
  материалами, карточками и манифестом; AC-2026-09-19 остаётся историей.
- Материалы `work/` — развитие, проверки, решения и кандидаты.
- Внешний результат всегда остаётся `[внешнее]`.
- `candidate`/`overlay` не равны `canonical_strict`.
- `¬A ≠ 0_A ≠ −A`; `phase ≠ −A`; `branch access ≠ Lift`;
  `array ≠ tensor` без закона преобразования.
- При отсутствии локального основания следует писать `нет в артефактах`.

### 1.2. Манифест входных артефактов

{input_manifest_table()}

{markdown_source("1.3. Полные проектные инструкции", PROJECT_INSTRUCTIONS)}
"""

    parts = [
        header,
        "## 2. Текущее состояние проекта\n\n"
        "*Включена текущая часть `work/STATE.md`; длинный журнал сессий исключён.*\n\n"
        + demote_headings(current_state(), 2),
        "## 3. Основной исследовательский текст v14\n\n"
        + demote_headings(read_text(V14_PAPER), 2),
        "## 4. Нотация, карты и статусный патч\n\n"
        + "\n\n".join(
            [
                markdown_source("4.1. Словарь нотации", NOTATION),
                markdown_source("4.2. Регистровая карта", REGISTER_MAP),
                markdown_source("4.3. Патч-таблица статусов", STATUS_PATCH),
            ]
        ),
        "## 5. Критика и машинная верификация\n\n"
        + "\n\n".join(
            [
                markdown_source("5.1. Красная команда F3", RED_TEAM),
                markdown_source("5.2. Отчёт машинной верификации", VERIFICATION_REPORT),
                fenced_source("5.3. Исполняемый код проверок", VERIFICATION_CODE, "python"),
                markdown_source("5.4. Отчёт кандидатных проверок новых связей", NEW_CONNECTIONS_REPORT),
                fenced_source("5.5. Исполняемый код кандидатных проверок", NEW_CONNECTIONS_CHECK, "python"),
            ]
        ),
        "## 6. Решения и открытые вопросы\n\n"
        + "\n\n".join(
            [
                markdown_source("6.1. Журнал значимых решений", DECISIONS),
                markdown_source("6.2. Открытые вопросы", OPEN_QUESTIONS),
                markdown_source("6.3. Журнал внешних коллизий", EXTERNAL_CONFLICTS),
                markdown_source("6.4. Код, предел кода и повторное кодирование", CODE_INFORMATION_RECODE),
                markdown_source("6.5. Рекурсивное различение: разбор новой записки", RD_REVIEW),
                markdown_source("6.6. Незакрытые уточнения автора", RD_QUESTIONS),
                markdown_source("6.7. Проверки рекурсивной записки", RD_REPORT),
                fenced_source("6.8. Код проверок записки", RD_CHECK, "python"),
                fenced_source("6.9. Манифест происхождения записки", RD_MANIFEST, "json"),
                submitted_note_source(),
                markdown_source("6.11. Авторский мандат ближайшего цикла", AUTHOR_CYCLE_CHARTER),
                markdown_source("6.12. Рабочая интеграция диалога: траектория и внутренняя регуляция", DIALOGUE_SEMANTICS_NOTE),
                markdown_source("6.13. Реестр принятых авторских дополнений", AUTHOR_CANON_INDEX),
                markdown_source("6.14. Авторское дополнение AC-2026-09-21", AUTHOR_CANON_ROOT / "AMENDMENT.md"),
                fenced_source("6.15. Новое авторское сообщение", AUTHOR_CANON_ROOT / "AUTHOR_MESSAGE.txt", "text"),
                fenced_source("6.16. Унаследованное авторское сообщение", AUTHOR_CANON_ROOT / "INHERITED_AUTHOR_MESSAGE.txt", "text"),
                fenced_source("6.17. Унаследованное уточнение трёх исходов У7", AUTHOR_CANON_ROOT / "INHERITED_AUTHOR_CLARIFICATION.txt", "text"),
                fenced_source("6.18. Карточки авторского дополнения", AUTHOR_CANON_ROOT / "cards.jsonl", "jsonl"),
                fenced_source("6.19. Связи авторского дополнения", AUTHOR_CANON_ROOT / "triples.tsv", "tsv"),
                fenced_source("6.20. Манифест авторского дополнения", AUTHOR_CANON_ROOT / "MANIFEST.json", "json"),
                fenced_source("6.21. Проверка границ внешних прочтений", AUTHOR_CANON_ROOT / "check_scope.py", "python"),
                markdown_source("6.22. Нейросетевой аналог ФТС: гашение и обобщение", NEURAL_ANALOGY_REVIEW),
                fenced_source_trimmed("6.23. Исходное сообщение об аналоге", NEURAL_ANALOGY_AUTHOR_MESSAGE, "text"),
                fenced_source("6.24. Воспроизводимые свидетели аналога", NEURAL_ANALOGY_CHECK, "python"),
            ]
        ),
        "## 7. Внешний исследовательский контур E5\n\n"
        + "\n\n".join(
            [
                markdown_source("7.1. Протокол систематического обзора", E5_PROTOCOL),
                markdown_source("7.2. Текущий статус волны 0", E5_STATUS),
                markdown_source(
                    "7.2a. Авторская поправка к текущему применению E5",
                    E5_AUTHOR_CYCLE_AMENDMENT,
                ),
                markdown_source("7.2b. Предварительный синтез E5", E5_SYNTHESIS),
                markdown_source("7.2c. Граница новизны E5", E5_NOVELTY_BOUNDARY),
                markdown_source("7.3. Предварительная карта сопряжений", E5_COUPLING),
                markdown_source(
                    "7.4. Поправка протокола для ограниченного Blackwell-моста",
                    E5_BLACKWELL_AMENDMENT,
                ),
                markdown_source(
                    "7.5. Типизированный Blackwell-мост У4–У6",
                    E5_BLACKWELL_BRIDGE,
                ),
                markdown_source(
                    "7.6. Отчёт точных кандидатных проверок",
                    E5_BLACKWELL_REPORT,
                ),
                fenced_source(
                    "7.7. Исполняемый код проверок Blackwell-моста",
                    E5_BLACKWELL_CHECK,
                    "python",
                ),
                markdown_source(
                    "7.8. Поправка протокола для 0_A и Lift",
                    E5_ABSENCE_LIFT_AMENDMENT,
                ),
                markdown_source(
                    "7.9. Механизм и provenance структурированного отсутствия",
                    E5_TYPED_ABSENCE,
                ),
                markdown_source(
                    "7.10. Категориальный проект типизации Lift",
                    E5_LIFT_TYPING,
                ),
                markdown_source(
                    "7.11. Отчёт проверок 0_A и Lift",
                    E5_ABSENCE_LIFT_REPORT,
                ),
                fenced_source(
                    "7.12. Исполняемый код проверок 0_A и Lift",
                    E5_ABSENCE_LIFT_CHECK,
                    "python",
                ),
                markdown_source(
                    "7.13. Внешний типизированный мост У1–У5",
                    EXTERNAL_BRIDGE_U1_U5,
                ),
                markdown_source(
                    "7.14. Явные дополнения Deep Research 2026-09-05",
                    E5_EXPLICIT_ADDITIONS,
                ),
                markdown_source(
                    "7.15. Отчёт конечных проверок явных дополнений",
                    E5_EXPLICIT_ADDITIONS_REPORT,
                ),
                fenced_source(
                    "7.16. Исполняемый код проверок явных дополнений",
                    E5_EXPLICIT_ADDITIONS_CHECK,
                    "python",
                ),
                markdown_source(
                    "7.17. Запросы Deep Research по основаниям связности",
                    E5_DEEP_RESEARCH_REQUESTS,
                ),
                markdown_source("7.18. Приёмка основного блока Deep Research", DR_CORE_REVIEW),
                markdown_source("7.19. Первичные источники и ограничения приёмки", DR_CORE_SOURCES),
                markdown_source("7.20. Маршрутизация предложенных коллизий", DR_CORE_ROUTING),
                markdown_source("7.21. Проверки основного DR-блока", DR_CORE_REPORT),
                fenced_source("7.22. Код независимых конечных проверок", DR_CORE_CHECK, "python"),
                fenced_source("7.23. Манифест семи входных отчётов", DR_CORE_MANIFEST, "json"),
                external_bibliography(),
                markdown_source("7.25. Интерпретация при понижении: Undermind", INTERPRETATION_REVIEW),
                markdown_source("7.26. Матрица внешних оснований интерпретации", INTERPRETATION_MATRIX),
                markdown_source("7.27. Аудит источников Undermind", INTERPRETATION_AUDIT),
                markdown_source("7.28. Протокол исследования интерпретации", INTERPRETATION_PROTOCOL),
                markdown_source("7.29. Непроизвольность лестницы: приём диалога", NONARBITRARY_REVIEW),
                markdown_source("7.33. У6: случайная закономерность и потеря знака", U6_RANDOM_REGULARITY),
                markdown_source("7.30. Карта тезисов о непроизвольности", NONARBITRARY_CLAIMS),
                fenced_source("7.31. Манифест диалога о непроизвольности", NONARBITRARY_MANIFEST, "json"),
                fenced_source("7.32. Исходный диалог о непроизвольности", NONARBITRARY_ORIGINAL, "text"),
                markdown_source("7.34. Черновик проверки рефлексии: пример поезда", TRAIN_REFLECTION_DRAFT),
                markdown_source("7.35. Протокол условной проверки внутренней регуляции", TRAIN_REFLECTION_PROTOCOL),
                markdown_source("7.36. Исправленный протокол v2 (черновик)", TRAIN_REFLECTION_PROTOCOL_V2_DRAFT),
                fenced_source("7.37. Скрипт проверки рефлексии", TRAIN_REFLECTION_PROGRAM, "python"),
                markdown_source("7.38. Результаты проверки рефлексии", TRAIN_REFLECTION_RESULTS_MD),
                fenced_source("7.39. Машинные результаты проверки рефлексии", TRAIN_REFLECTION_RESULTS_JSON, "json"),
            ]
        ),
        "## 8. Компактный контекст канона v13\n\n"
        + demote_headings(read_text(CANON_CONTEXT), 2),
        "## 9. Полный 54-листовый дамп канона v13\n\n"
        + demote_headings(read_text(CANON_FULL_DUMP), 2),
        "## 10. Машиночитаемые приложения\n\n"
        + "\n\n".join(
            [
                fenced_source("10.1. Канонические карточки JSONL", CANON_CARDS, "jsonl"),
                fenced_source("10.2. Канонические триплеты TSV", CANON_TRIPLES, "tsv"),
            ]
        ),
    ]
    rendered = "\n\n".join(part.rstrip() for part in parts) + "\n"
    validate_export(rendered)
    return rendered


def validate_export(text: str) -> None:
    lower = text.lower()
    for marker in FORBIDDEN_MARKERS:
        if marker.lower() in lower:
            raise ExportError(f"обнаружен запрещённый маркер: {marker}")
    if re.search(r"!\[[^\]]*\]\(https?://", text, flags=re.IGNORECASE):
        raise ExportError("обнаружено внешнее изображение")

    positions: list[int] = []
    for heading in REQUIRED_HEADINGS:
        position = text.find(heading)
        if position < 0:
            raise ExportError(f"отсутствует обязательный раздел: {heading}")
        positions.append(position)
    if positions != sorted(positions):
        raise ExportError("нарушен порядок обязательных разделов")

    cards, triples, sheets, _ = source_counts()
    expected_counts = (
        f"{cards} карточка",
        f"{triples} триплетов",
        f"{sheets} листа",
    )
    for value in expected_counts:
        if value not in text:
            raise ExportError(f"в паспорте отсутствует показатель: {value}")

    passed, failed, total = verification_counts()
    if f"{passed} PASS / {failed} FAIL из {total}" not in text:
        raise ExportError("итог верификации не совпадает с текущим отчётом")

    for entry in bib_entries():
        if entry["doi_normalized"] not in lower:
            raise ExportError(f"в выгрузке потерян DOI: {entry['doi_normalized']}")

    for marker in (
        "candidate_external_bridge",
        "BW-06",
        "6 PASS / 0 FAIL",
    ):
        if marker not in text:
            raise ExportError(f"в выгрузке потерян Blackwell-маркер: {marker}")

    for marker in (
        "candidate_typed_absence",
        "categorical_typing_project",
        "TA-05",
        "LT-05",
        "10 PASS / 0 FAIL",
    ):
        if marker not in text:
            raise ExportError(f"в выгрузке потерян маркер 0_A/Lift: {marker}")

    for marker in (
        "external_bridge_candidate",
        "Sem(U_n) ⇒ M_n",
        "EXT15-3",
    ):
        if marker not in text:
            raise ExportError(f"в выгрузке потерян маркер внешнего моста У1–У5: {marker}")


def build_bytes() -> bytes:
    return render_export().encode("utf-8")


def check_output(expected: bytes) -> int:
    if not OUTPUT_PATH.is_file():
        print(f"FAIL отсутствует выгрузка: {OUTPUT_PATH}")
        return 1
    actual = OUTPUT_PATH.read_bytes()
    if actual != expected:
        print(
            "FAIL выгрузка устарела: "
            f"expected={bytes_sha256(expected)} actual={bytes_sha256(actual)}"
        )
        return 1
    print(
        "PASS выгрузка актуальна: "
        f"bytes={len(actual)} sha256={bytes_sha256(actual)}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="проверить существующую выгрузку без перезаписи",
    )
    args = parser.parse_args()
    try:
        expected = build_bytes()
        if args.check:
            return check_output(expected)
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_bytes(expected)
        print(
            "PASS выгрузка собрана: "
            f"path={OUTPUT_PATH} bytes={len(expected)} sha256={bytes_sha256(expected)}"
        )
        return 0
    except (ExportError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
