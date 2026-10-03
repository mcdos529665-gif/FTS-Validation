# Active canon installation

Copy every file listed in MANIFEST.json into the project root source/ directory.
Preserve the manifest and verify with `python -X utf8 tools/verify.py --strict`.
Use `python -X utf8 tools/query.py card <ID>` to inspect records.
Canon is editable; update primary records, rebuild derivatives, and verify hashes.
