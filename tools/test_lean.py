"""Regressions for the proof runner's trust boundary; no network or installation."""
import unittest
from lean import audit_axioms


class AxiomAuditTests(unittest.TestCase):
    def test_standard_axioms_and_axiom_free_result(self):
        output = "'FTS.a' depends on axioms: [propext,\n Classical.choice, Quot.sound]\n'FTS.b' does not depend on any axioms"
        result = audit_axioms(output, ['FTS.a', 'FTS.b'])
        self.assertEqual(result['FTS.b'], [])
        self.assertEqual(set(result['FTS.a']), {'propext', 'Classical.choice', 'Quot.sound'})

    def test_placeholders_custom_axioms_and_native_escape_rejected(self):
        for axiom in ['sorryAx', 'FTS.assume_result', 'Lean.ofReduceBool']:
            with self.subTest(axiom=axiom), self.assertRaises(RuntimeError):
                audit_axioms(f"'FTS.a' depends on axioms: [{axiom}]", ['FTS.a'])

    def test_incomplete_or_unrecognized_audit_rejected(self):
        for output in ["'FTS.a' depends on axioms: []", 'new unrecognized output format']:
            with self.subTest(output=output), self.assertRaises(RuntimeError):
                audit_axioms(output, ['FTS.a', 'FTS.b'])


if __name__ == '__main__':
    unittest.main()
