---
name: arxiv-source-import
description: Download a requested arXiv paper into the FTS project with its immutable TeX source package, official versioned PDF, and a source-backed Markdown workspace. Use when the user asks to locally obtain or archive a specific arXiv article; do not use for literature discovery, citation analysis, or PDF-to-Markdown conversion.
---

# Import an arXiv Primary Source

Preserve each paper as a reproducible local package instead of treating PDF extraction as the source. Each paper produces:

```text
<papers-directory>/<arxiv-id>/
├── source/                 # exact files supplied by arXiv; do not edit
├── original.pdf            # PDF of the same version
├── article.md              # working Markdown version or explicit source-backed scaffold
├── provenance.json         # version, URLs, download times, and SHA-256 hashes
└── source_manifest.sha256   # checksum of each file in source/
```

The project's root `source/` is the FTS canon, not a location for papers. External sources remain `[внешнее]`: importing a paper creates no link to canon cards and changes no FTS status.

## Version and request boundaries

- Require a versioned identifier by default, such as `2301.12345v2`. A versioned URL such as `https://arxiv.org/abs/2301.12345v2` is also accepted. This binds the source package and PDF to one fixed revision.
- If the user explicitly requests the latest version, `--allow-latest` is permitted. The script records the resolved version in `provenance.json`; report that version to the user. Do not describe an unversioned identifier as a reproducible version.
- The default paper directory is `work/v14_rebuild/e5_literature_review/arxiv/`. Pass `--dest` for another location. Do not overwrite an existing paper package.
- Do not use this skill for literature search, assessing the paper's credibility, or OCR. Use the separate `$fts-academic-research` workflow for discovery and external grounds.

## Import and verify

Run the script from the project root. It downloads only official arXiv URLs, safely extracts the archive into a staging directory, checks the PDF, and moves the finished package into place with one rename. Archives containing unsafe paths or links are rejected.

```text
python -X utf8 .agents/skills/arxiv-source-import/scripts/fetch_arxiv.py import 2301.12345v2
python -X utf8 .agents/skills/arxiv-source-import/scripts/fetch_arxiv.py import 2301.12345v2 --dest work/references/arxiv
python -X utf8 .agents/skills/arxiv-source-import/scripts/fetch_arxiv.py import 2301.12345 --allow-latest
python -X utf8 .agents/skills/arxiv-source-import/scripts/fetch_arxiv.py verify work/v14_rebuild/e5_literature_review/arxiv/2301.12345v2
```

After a successful import, run `verify` and check `git diff --check`. If the package belongs in project history, stage all its files as one snapshot. Do not edit the nested `source/` afterward.

## Markdown

Unless the user separately requests LaTeX conversion, the script creates `article.md` with `pending` status. This file is intentionally a scaffold: it does not pretend to be the paper and is not derived from PDF extraction. When Markdown is explicitly requested, create or correct it using only the files in the nested `source/`, keeping a reference to the originating `.tex`. Use `original.pdf` only to visually check formulas, tables, figures, and page structure.

For discrepancies, follow this order: nested `source/` (LaTeX) → `original.pdf` for visual checking → correct `article.md` against the source. Never rewrite LaTeX based on Markdown.

Report the result in Russian.
