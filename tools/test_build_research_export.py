#!/usr/bin/env python3
"""Автоматические проверки единой исследовательской выгрузки ФТС."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "build_research_export",
    HERE / "build_research_export.py",
)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
sys.modules["build_research_export"] = builder
SPEC.loader.exec_module(builder)


class ResearchExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.first = builder.build_bytes()
        cls.second = builder.build_bytes()
        cls.text = cls.first.decode("utf-8")

    def test_deterministic(self) -> None:
        self.assertEqual(self.first, self.second)

    def test_expected_size(self) -> None:
        self.assertGreaterEqual(len(self.first), 750_000)
        self.assertLessEqual(len(self.first), 900_000)

    def test_required_sections_are_ordered(self) -> None:
        positions = [self.text.index(heading) for heading in builder.REQUIRED_HEADINGS]
        self.assertEqual(positions, sorted(positions))

    def test_external_fulltexts_are_not_inputs(self) -> None:
        for relative in builder.INPUT_PATHS:
            parts = {part.lower() for part in relative.parts}
            self.assertNotIn("papers", parts)
            self.assertNotIn("dossier.ru.md", parts)
            self.assertNotIn("source.en.md", parts)

    def test_forbidden_markers_are_absent(self) -> None:
        lowered = self.text.lower()
        for marker in builder.FORBIDDEN_MARKERS:
            self.assertNotIn(marker.lower(), lowered)

    def test_only_current_state_is_included(self) -> None:
        state_section = self.text.split(
            "## 2. Текущее состояние проекта", 1
        )[1].split("## 3. Основной исследовательский текст v14", 1)[0]
        self.assertNotIn("## Лог сессий", state_section)

    def test_canon_counts_and_verification_are_current(self) -> None:
        cards, triples, sheets, _ = builder.source_counts()
        passed, failed, total = builder.verification_counts()
        self.assertEqual((cards, triples, sheets), (161, 238, 54))
        self.assertEqual(failed, 0)
        self.assertIn(f"{passed} PASS / {failed} FAIL из {total}", self.text)

    def test_all_seed_dois_are_preserved(self) -> None:
        for entry in builder.bib_entries():
            self.assertIn(entry["doi_normalized"], self.text.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
