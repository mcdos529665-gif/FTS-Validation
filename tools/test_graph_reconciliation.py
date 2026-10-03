"""Regression guards for opaque prerequisites and witnessed graph references."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from reference_resolution import dependency_cycles, dependency_sets, fragment_witness, validate_resolutions
import claim_graph


class DependencyTests(unittest.TestCase):
    def test_missing_noncard_prerequisite_is_visible(self):
        card, triple = dependency_sets([{'id': 'X', 'depends_on': ['Missing_map']}], [])
        self.assertEqual(card - triple, {('X', 'Missing_map')})

    def test_unknown_subject_in_triples_is_visible(self):
        card, triple = dependency_sets([], [{'subject': 'Missing_claim', 'predicate': 'depends_on', 'object': 'X'}])
        self.assertEqual(triple - card, {('Missing_claim', 'X')})

    def test_any_new_cycle_and_self_loop_are_detected(self):
        edges = {('A', 'B'), ('B', 'C'), ('C', 'A'), ('Other', 'Other'), ('D', 'E')}
        self.assertEqual(dependency_cycles(edges), [('A', 'B', 'C'), ('Other',)])

    def test_typed_operator_backlink_is_not_a_prerequisite(self):
        cards = [{'id': 'Operator', 'depends_on': ['Core']}, {'id': 'Core', 'depends_on': []}]
        triples = [{'subject': 'Operator', 'predicate': 'depends_on', 'object': 'Core'},
                   {'subject': 'Core', 'predicate': 'has_operator', 'object': 'Operator'}]
        card, triple = dependency_sets(cards, triples)
        self.assertEqual(card, triple)
        self.assertEqual(dependency_cycles(card | triple), [])


class WitnessTests(unittest.TestCase):
    def test_fragment_uses_exact_key_not_similar_name(self):
        with tempfile.TemporaryDirectory(prefix='fts-reference-', dir='E:/Codex/work/fts-graph-reconcile-20261003') as temporary:
            root = Path(temporary)
            (root / 'book.json').write_text(json.dumps({'sheets': [{'name': 'Operators', 'values': [['OP_A_old', 'old'], ['OP_A', 'exact']]}]}), encoding='utf-8')
            row = {'raw_reference': 'OP_A', 'resolution': 'sheet_record', 'target': 'book.json',
                   'locator': json.dumps({'sheet': 'Operators', 'key': 'OP_A'})}
            location, witness = fragment_witness(root, row)
            self.assertEqual(witness, ['OP_A', 'exact'])
            self.assertIn('row:2:key:OP_A', location)

    def test_duplicate_key_is_inconclusive(self):
        with tempfile.TemporaryDirectory(prefix='fts-reference-', dir='E:/Codex/work/fts-graph-reconcile-20261003') as temporary:
            root = Path(temporary)
            (root / 'book.json').write_text(json.dumps({'sheets': [{'name': 'Operators', 'values': [['OP_A', 'one'], ['OP_A', 'two']]}]}), encoding='utf-8')
            row = {'raw_reference': 'OP_A', 'resolution': 'sheet_record', 'target': 'book.json',
                   'locator': json.dumps({'sheet': 'Operators', 'key': 'OP_A'})}
            with self.assertRaises(ValueError): fragment_witness(root, row)

    def test_unknown_scope_member_is_rejected(self):
        rows = {'Scope': {'resolution': 'scope', 'target': '["Existing", "Missing"]'}}
        with self.assertRaises(ValueError): validate_resolutions(Path('.'), rows, {'Existing'})

    def test_tampered_graph_fragment_is_rejected(self):
        graph = copy.deepcopy(claim_graph.load_graph())
        node = next(node for node in graph['nodes'] if node.get('resolution_state') == 'resolved_fragment')
        node['fragment_record'] = ['invented definition']
        with self.assertRaisesRegex(AssertionError, 'Fragment witness drift'):
            claim_graph.validate_graph(graph)

    def test_new_unclassified_reference_is_rejected(self):
        graph = copy.deepcopy(claim_graph.load_graph())
        node = next(node for node in graph['nodes'] if node.get('resolution_state') == 'unresolved_reference')
        node['raw_reference'] = 'unreviewed_new_reference'
        with self.assertRaisesRegex(AssertionError, 'Unclassified unresolved reference'):
            claim_graph.validate_graph(graph)


if __name__ == '__main__':
    unittest.main()
