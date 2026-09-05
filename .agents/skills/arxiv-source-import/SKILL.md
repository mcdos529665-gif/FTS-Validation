---
name: arxiv-source-import
description: Download a requested arXiv paper into the FTS project with its immutable TeX source package, official versioned PDF, and a source-backed Markdown workspace. Use when the user asks to locally obtain or archive a specific arXiv article; do not use for literature discovery, citation analysis, or PDF-to-Markdown conversion.
---

# Импорт первоисточника arXiv

Сохраняй статью как воспроизводимый локальный пакет, а не как распознанный PDF.
Результат для каждой статьи имеет вид:

```text
<каталог-статей>/<arxiv-id>/
├── source/                 # точные файлы, выданные arXiv; не редактировать
├── original.pdf            # PDF той же версии
├── article.md              # рабочая Markdown-версия или её явный source-backed scaffold
├── provenance.json          # версия, URL, время и SHA-256 загрузок
└── source_manifest.sha256   # контрольная сумма каждого файла source/
```

Корневой `source/` проекта — канон ФТС v13 и не является местом для статей.
Внешние источники остаются `[внешнее]`: импорт не создаёт связи с карточками и не
меняет статусы ФТС.

## Версия и границы запроса

- По умолчанию требуй идентификатор с версией: `2301.12345v2` (принимаются также
  URL вида `https://arxiv.org/abs/2301.12345v2`). Это связывает исходники и PDF с
  одной фиксированной ревизией.
- Если пользователь осознанно просит актуальную версию, разрешён
  `--allow-latest`: скрипт сначала фиксирует найденную версию в `provenance.json` и
  в ответе. Не выдавай неверсированный идентификатор за воспроизводимую версию.
- По умолчанию каталог статей —
  `work/v14_rebuild/e5_literature_review/arxiv/`. Для другого расположения передай
  `--dest`; не создавай пакет поверх уже существующей статьи.
- Не подменяй этот навык литературным поиском, оценкой достоверности статьи или
  OCR. Для поиска и внешних оснований действует отдельный `$fts-academic-research`.

## Импорт и проверка

Запускай скрипт из корня проекта. Он скачивает только официальные URL arXiv,
безопасно извлекает архив в staging-каталог, проверяет PDF и переносит готовый
пакет одним переименованием. Архив с опасными путями или ссылками не извлекается.

```text
python -X utf8 .agents/skills/arxiv-source-import/scripts/fetch_arxiv.py import 2301.12345v2
python -X utf8 .agents/skills/arxiv-source-import/scripts/fetch_arxiv.py import 2301.12345v2 --dest work/references/arxiv
python -X utf8 .agents/skills/arxiv-source-import/scripts/fetch_arxiv.py import 2301.12345 --allow-latest
python -X utf8 .agents/skills/arxiv-source-import/scripts/fetch_arxiv.py verify work/v14_rebuild/e5_literature_review/arxiv/2301.12345v2
```

После успешного импорта выполни `verify` и проверь `git diff --check`. Если пакет
должен войти в историю проекта, добавь все его файлы как единый снимок; `source/`
внутри пакета больше не редактируй.

## Markdown

Скрипт создаёт `article.md` со статусом `pending`, когда пользователь не просил
отдельно конвертировать LaTeX. Это намеренно: он не притворяется статьёй и не
получается из PDF. При явном запросе на Markdown создавай или исправляй его только
по файлам `source/`, сохраняя ссылку на исходный `.tex`; `original.pdf` служит лишь
визуальной сверкой формул, таблиц, рисунков и структуры страниц.

При любом расхождении приоритет такой: `source/` (LaTeX) → `original.pdf` для
визуальной проверки → исправление `article.md` по исходникам. Никогда не
переписывай LaTeX по Markdown.
