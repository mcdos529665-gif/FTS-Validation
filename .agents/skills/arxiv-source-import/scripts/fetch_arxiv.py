#!/usr/bin/env python3
"""Import a versioned arXiv source package without treating a PDF as source text."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tarfile
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Iterable


DEFAULT_DEST = Path("work/v14_rebuild/e5_literature_review/arxiv")
MAX_DOWNLOAD_BYTES = 1_073_741_824  # 1 GiB: prevents accidental archive bombs.
ALLOWED_HOSTS = {"arxiv.org", "www.arxiv.org", "export.arxiv.org"}
MODERN_ID = re.compile(r"^\d{4}\.\d{4,5}(?:v\d+)?$", re.IGNORECASE)
LEGACY_ID = re.compile(r"^[A-Za-z][A-Za-z.-]*/\d{7}(?:v\d+)?$", re.IGNORECASE)
VERSION_SUFFIX = re.compile(r"v\d+$", re.IGNORECASE)


class ImportFailure(RuntimeError):
    """A user-actionable import failure."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalise_identifier(value: str) -> str:
    """Accept an arXiv ID or official arXiv URL and return a bare ID."""
    raw = value.strip()
    if raw.lower().startswith("arxiv:"):
        raw = raw[6:].strip()

    parsed = urllib.parse.urlparse(raw)
    if parsed.scheme:
        host = parsed.hostname.lower() if parsed.hostname else ""
        if parsed.scheme != "https" or host not in ALLOWED_HOSTS:
            raise ImportFailure("Нужен идентификатор arXiv или официальный HTTPS URL arxiv.org.")
        parts = [urllib.parse.unquote(item) for item in parsed.path.split("/") if item]
        if len(parts) < 2 or parts[0] not in {"abs", "pdf", "e-print"}:
            raise ImportFailure("URL должен вести на /abs/, /pdf/ или /e-print/ arXiv.")
        raw = "/".join(parts[1:])

    raw = raw.removesuffix(".pdf")
    if not (MODERN_ID.fullmatch(raw) or LEGACY_ID.fullmatch(raw)):
        raise ImportFailure(f"Нераспознанный идентификатор arXiv: {value!r}")
    return raw


def has_version(identifier: str) -> bool:
    return VERSION_SUFFIX.search(identifier) is not None


def source_url(identifier: str) -> str:
    return f"https://arxiv.org/e-print/{identifier}"


def pdf_url(identifier: str) -> str:
    return f"https://arxiv.org/pdf/{identifier}"


def abs_url(identifier: str) -> str:
    return f"https://arxiv.org/abs/{identifier}"


def safe_article_dir_name(identifier: str) -> str:
    return identifier.replace("/", "_")


def require_official_response(response: object) -> None:
    final_url = getattr(response, "geturl")()
    parsed = urllib.parse.urlparse(final_url)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if parsed.scheme != "https" or host not in ALLOWED_HOSTS:
        raise ImportFailure(f"arXiv перенаправил загрузку на непредусмотренный адрес: {final_url}")


def request(url: str):
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": "FTS-arXiv-source-import/1.0 (local archival workflow)",
            "Accept": "*/*",
        },
    )


def read_text(url: str) -> str:
    try:
        with urllib.request.urlopen(request(url), timeout=60) as response:
            require_official_response(response)
            return response.read(MAX_DOWNLOAD_BYTES + 1).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        raise ImportFailure(f"arXiv вернул HTTP {error.code} для {url}") from error
    except urllib.error.URLError as error:
        raise ImportFailure(f"Не удалось обратиться к arXiv: {error.reason}") from error


def resolve_latest(identifier: str) -> str:
    page = read_text(abs_url(identifier))
    match = re.search(
        rf"arXiv:\s*({re.escape(identifier)}v\d+)\b", page, flags=re.IGNORECASE
    )
    if not match:
        raise ImportFailure(
            "Не удалось зафиксировать номер актуальной версии на странице arXiv; "
            "укажите идентификатор с vN вручную."
        )
    return match.group(1)


def download(url: str, destination: Path, max_bytes: int) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(request(url), timeout=60) as response:
            require_official_response(response)
            advertised_length = response.headers.get("Content-Length")
            if advertised_length and int(advertised_length) > max_bytes:
                raise ImportFailure(f"Загрузка больше разрешённого лимита {max_bytes} байт: {url}")
            total = 0
            digest = hashlib.sha256()
            with destination.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    total += len(chunk)
                    if total > max_bytes:
                        raise ImportFailure(f"Загрузка превысила лимит {max_bytes} байт: {url}")
                    output.write(chunk)
                    digest.update(chunk)
            return total, digest.hexdigest()
    except urllib.error.HTTPError as error:
        raise ImportFailure(f"arXiv вернул HTTP {error.code} для {url}") from error
    except urllib.error.URLError as error:
        raise ImportFailure(f"Не удалось скачать {url}: {error.reason}") from error


def safe_member_path(name: str) -> PurePosixPath:
    if "\\" in name or "\x00" in name:
        raise ImportFailure(f"Небезопасное имя в архиве: {name!r}")
    relative = PurePosixPath(name)
    if relative.is_absolute() or any(part in {"", ".."} for part in relative.parts):
        raise ImportFailure(f"Небезопасный путь в архиве: {name!r}")
    if relative.parts and relative.parts[0].endswith(":"):
        raise ImportFailure(f"Небезопасный путь в архиве: {name!r}")
    return relative


def extract_source(archive: Path, source_dir: Path) -> tuple[str, int]:
    """Extract a tar safely, or retain a single raw TeX source response."""
    with archive.open("rb") as stream:
        prefix = stream.read(5)
    if prefix == b"%PDF-":
        raise ImportFailure("arXiv не выдал пакет исходников (получен PDF). Импорт остановлен.")

    if not tarfile.is_tarfile(archive):
        if not prefix or prefix.startswith(b"<html") or prefix.startswith(b"<!DOC"):
            raise ImportFailure("arXiv не выдал распознаваемый архив исходников.")
        raw_source = source_dir / "main.tex"
        shutil.copyfile(archive, raw_source)
        return "single_tex", 1

    total_files = 0
    seen: set[PurePosixPath] = set()
    with tarfile.open(archive, mode="r:*") as tar:
        for member in tar.getmembers():
            relative = safe_member_path(member.name)
            if member.isdir():
                (source_dir.joinpath(*relative.parts)).mkdir(parents=True, exist_ok=True)
                continue
            if not member.isfile():
                raise ImportFailure(
                    f"Архив содержит ссылку или специальный объект {member.name!r}; "
                    "небезопасное извлечение отменено."
                )
            if relative in seen:
                raise ImportFailure(f"Архив содержит повторяющийся путь: {member.name!r}")
            seen.add(relative)
            target = source_dir.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            source = tar.extractfile(member)
            if source is None:
                raise ImportFailure(f"Не удалось прочесть файл из архива: {member.name!r}")
            with source, target.open("wb") as output:
                shutil.copyfileobj(source, output, length=1024 * 1024)
            total_files += 1
    if total_files == 0:
        raise ImportFailure("Архив исходников пуст.")
    return "tar", total_files


def iter_source_files(source_dir: Path) -> Iterable[Path]:
    yield from sorted(path for path in source_dir.rglob("*") if path.is_file())


def write_source_manifest(source_dir: Path, manifest_path: Path) -> int:
    rows: list[str] = []
    for path in iter_source_files(source_dir):
        relative = path.relative_to(source_dir).as_posix()
        if "\n" in relative or "\r" in relative:
            raise ImportFailure(f"Имя файла с переводом строки не поддержано: {relative!r}")
        rows.append(f"{sha256_file(path)}  {relative}")
    manifest_path.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    return len(rows)


def write_article_markdown(path: Path, identifier: str, source_url_value: str, pdf_url_value: str) -> None:
    text = f"""---
arxiv_id: {identifier}
source_of_truth: source/
official_pdf: original.pdf
markdown_status: pending
---

# arXiv:{identifier}

`article.md` пока не содержит конвертированного текста: этот scaffold создан вместе
с исходниками, чтобы не выдавать PDF-распознавание за первичный текст.

## Первоисточники

- LaTeX и все приложенные файлы: [`source/`](source/)
- Официальный PDF той же версии: [`original.pdf`](original.pdf)
- Метаданные и SHA-256: [`provenance.json`](provenance.json),
  [`source_manifest.sha256`](source_manifest.sha256)

Исходник для будущего Markdown: `{source_url_value}`

PDF для визуальной сверки: `{pdf_url_value}`

При расхождении Markdown и LaTeX приоритет имеет `source/`; PDF используется только
для визуальной структуры. Исправлять Markdown по исходникам, а не наоборот.
"""
    path.write_text(text, encoding="utf-8", newline="\n")


def import_article(args: argparse.Namespace) -> int:
    requested = normalise_identifier(args.identifier)
    if has_version(requested):
        resolved = requested
    elif args.allow_latest:
        resolved = resolve_latest(requested)
    else:
        raise ImportFailure(
            "Для воспроизводимого импорта укажите версию, например 2301.12345v2. "
            "Если пользователь прямо разрешил актуальную версию, повторите с --allow-latest."
        )

    destination_root = Path(args.dest).resolve()
    article_name = args.article_dir or safe_article_dir_name(resolved)
    if Path(article_name).name != article_name or article_name in {"", ".", ".."}:
        raise ImportFailure("--article-dir должен быть одним именем каталога.")
    final_dir = destination_root / article_name
    if final_dir.exists():
        raise ImportFailure(f"Каталог уже существует и не будет перезаписан: {final_dir}")

    destination_root.mkdir(parents=True, exist_ok=True)
    staging = destination_root / f".{article_name}.staging-{uuid.uuid4().hex}"
    staging.mkdir()
    download_dir = staging / "_download"
    download_dir.mkdir()
    source_archive = download_dir / "source.download"
    pdf_path = staging / "original.pdf"
    source_endpoint = source_url(resolved)
    pdf_endpoint = pdf_url(resolved)

    try:
        source_size, source_sha = download(source_endpoint, source_archive, args.max_download_bytes)
        source_dir = staging / "source"
        source_dir.mkdir()
        source_kind, unpacked_count = extract_source(source_archive, source_dir)
        pdf_size, pdf_sha = download(pdf_endpoint, pdf_path, args.max_download_bytes)
        with pdf_path.open("rb") as stream:
            if stream.read(5) != b"%PDF-":
                raise ImportFailure("Файл official PDF не начинается с сигнатуры %PDF-.")

        manifest_path = staging / "source_manifest.sha256"
        source_files = write_source_manifest(source_dir, manifest_path)
        fetched_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        provenance = {
            "schema": "arxiv-source-import/v1",
            "requested_identifier": requested,
            "arxiv_identifier": resolved,
            "fetched_at_utc": fetched_at,
            "urls": {"abstract": abs_url(resolved), "source": source_endpoint, "pdf": pdf_endpoint},
            "source_download": {
                "format": source_kind,
                "sha256": source_sha,
                "size_bytes": source_size,
                "unpacked_file_count": unpacked_count,
            },
            "original_pdf": {"sha256": pdf_sha, "size_bytes": pdf_size},
            "source_manifest": {"file_count": source_files, "algorithm": "sha256"},
        }
        (staging / "provenance.json").write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        write_article_markdown(staging / "article.md", resolved, source_endpoint, pdf_endpoint)
        shutil.rmtree(download_dir)
        staging.replace(final_dir)
    except Exception:
        raise

    print(f"IMPORTED {resolved} -> {final_dir}")
    return verify_article(argparse.Namespace(article_dir=final_dir))


def verify_article(args: argparse.Namespace) -> int:
    article_dir = Path(args.article_dir).resolve()
    source_dir = article_dir / "source"
    manifest_path = article_dir / "source_manifest.sha256"
    provenance_path = article_dir / "provenance.json"
    for required in (source_dir, manifest_path, provenance_path, article_dir / "original.pdf", article_dir / "article.md"):
        if not required.exists():
            raise ImportFailure(f"Не найден обязательный файл или каталог: {required}")

    expected: dict[str, str] = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        try:
            digest, relative = line.split("  ", 1)
        except ValueError as error:
            raise ImportFailure(f"Некорректная строка source_manifest.sha256: {line!r}") from error
        if not re.fullmatch(r"[0-9a-f]{64}", digest) or not relative or "\\" in relative:
            raise ImportFailure(f"Некорректная строка source_manifest.sha256: {line!r}")
        candidate = safe_member_path(relative)
        key = candidate.as_posix()
        if key in expected:
            raise ImportFailure(f"Повтор пути в source_manifest.sha256: {key}")
        expected[key] = digest

    actual = {path.relative_to(source_dir).as_posix(): sha256_file(path) for path in iter_source_files(source_dir)}
    if expected != actual:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        changed = sorted(key for key in set(expected) & set(actual) if expected[key] != actual[key])
        details = []
        if missing:
            details.append(f"missing={missing[:3]}")
        if extra:
            details.append(f"extra={extra[:3]}")
        if changed:
            details.append(f"changed={changed[:3]}")
        raise ImportFailure("source/ не совпадает с контрольной суммой: " + "; ".join(details))

    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    if provenance.get("schema") != "arxiv-source-import/v1":
        raise ImportFailure("Неподдерживаемая схема provenance.json.")
    if provenance.get("original_pdf", {}).get("sha256") != sha256_file(article_dir / "original.pdf"):
        raise ImportFailure("original.pdf не совпадает с SHA-256 в provenance.json.")
    with (article_dir / "original.pdf").open("rb") as stream:
        if stream.read(5) != b"%PDF-":
            raise ImportFailure("original.pdf не имеет сигнатуры %PDF-.")

    print(f"OK {provenance['arxiv_identifier']}: {len(actual)} source files; original.pdf verified")
    return 0


def positive_bytes(value: str) -> int:
    result = int(value)
    if result <= 0:
        raise argparse.ArgumentTypeError("лимит должен быть положительным числом байт")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    importer = commands.add_parser("import", help="download a versioned arXiv article")
    importer.add_argument("identifier", help="arXiv ID (for example 2301.12345v2) or official arXiv URL")
    importer.add_argument("--dest", default=DEFAULT_DEST, help=f"article-root directory (default: {DEFAULT_DEST})")
    importer.add_argument("--article-dir", help="single directory name below --dest")
    importer.add_argument("--allow-latest", action="store_true", help="resolve an unversioned ID to the current arXiv version")
    importer.add_argument("--max-download-bytes", type=positive_bytes, default=MAX_DOWNLOAD_BYTES)
    importer.set_defaults(handler=import_article)
    verifier = commands.add_parser("verify", help="verify an imported article against its manifests")
    verifier.add_argument("article_dir", help="article directory that contains source_manifest.sha256")
    verifier.set_defaults(handler=verify_article)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except ImportFailure as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    except (OSError, tarfile.TarError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
