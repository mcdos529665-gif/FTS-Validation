# Зафиксированные версии исследовательского контура

- Academic Research Skills plugin: `academic-research-skills@academic-research-skills-codex`
- plugin ref/version: `v0.1.18` / `0.1.18`
- vendored upstream ARS: `v3.16.0`
- vendored upstream commit: `73c898c842afae3f163ac571dfa098c72d7c82af`
- marketplace source: `https://github.com/Imbad0202/academic-research-skills-codex.git`
- ARS mode: inline only
- disabled by policy: full-runtime, automatic agent commands, hooks
- Consensus: existing installed connector; no duplicate MCP registration
- Semantic Scholar: Graph API wrapper, initial rate `1 RPS`, `429`/`Retry-After`
- ResearchRabbit: manual BibTeX/RIS/CSV round-trip
- Wolfram: separate `$fts-wolfram-audit`, explicit invocation only
- citation cache: `E:\FTS-data\academic-research\verification.db`
- environment variable: `ARS_VERIFICATION_CACHE_PATH`

Порядок обновления: изменить зафиксированный ref, повторить quality gates ARS,
тесты маршрутизации, smoke-тесты провайдеров, валидатор E5 и проектные проверки.
Обновлять lock-запись только после прохождения всех проверок.
