"""Negative controls for scope provenance and the persistent project projection."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import claim_graph as cg
from tools.audit_research_scope import address_routes


class AddressControls(unittest.TestCase):
    def route(self, nodes, edges):
        entity = {"scope_categories": [{"id": "grounds", "anchor_card_ids": ["O_14"]}]}
        return {row["node_id"]: row for row in address_routes({"nodes": nodes, "edges": edges}, entity)}

    def node(self, node_id, node_type, **fields):
        return {"id": node_id, "type": node_type, "label": node_id, "layer": "research", **fields}

    def edge(self, edge_id, source, target, relation, layer="research"):
        return {"id": edge_id, "source": source, "target": target, "relation": relation,
                "layer": layer, "source_file": "fixture.tsv", "source_location": "row:2"}

    def base(self):
        return [self.node("ground", "card", card_id="O_14"), self.node("claim", "claim", claim_id="X")]

    def test_one_of_four_addresses_is_sufficient(self):
        rows = self.route(self.base(), [self.edge("g", "claim", "ground", "grounds_claim")])
        self.assertEqual(rows["claim"]["address_state"], "recorded_route")
        self.assertEqual(rows["claim"]["scope_categories"], "grounds")

    def test_shared_verification_cannot_assign_subject(self):
        nodes = self.base() + [self.node("other", "claim"), self.node("check", "verification")]
        edges = [self.edge("v1", "claim", "check", "verified_by"),
                 self.edge("v2", "other", "check", "verified_by"),
                 self.edge("g", "other", "ground", "grounds_claim")]
        self.assertEqual(self.route(nodes, edges)["claim"]["address_state"], "no_recorded_route")

    def test_common_document_cannot_assign_subject(self):
        nodes = self.base() + [self.node("doc", "source_document")]
        edges = [self.edge("a", "doc", "claim", "contains"), self.edge("b", "doc", "ground", "contains"),
                 self.edge("g", "claim", "doc", "grounds_claim")]
        self.assertEqual(self.route(nodes, edges)["claim"]["address_state"], "no_recorded_route")

    def test_unadopted_formalization_is_not_an_unanswered_author_claim(self):
        nodes = self.base() + [self.node("proposal", "card", card_id="A5",
                                        status="assistant_formalization_not_adopted")]
        edges = [self.edge("candidate", "proposal", "ground", "candidate_supports")]
        self.assertEqual(self.route(nodes, edges)["proposal"]["address_state"], "unadopted_formalization")

    def test_project_scope_edges_do_not_repair_claims(self):
        nodes = self.base() + [self.node("scope", "scope", layer="project_definition")]
        edges = [self.edge("a", "claim", "scope", "addresses_object", "project_definition"),
                 self.edge("b", "scope", "ground", "addresses_object", "project_definition")]
        self.assertEqual(self.route(nodes, edges)["claim"]["address_state"], "no_recorded_route")

    def test_owned_expression_has_explicit_subject(self):
        nodes = self.base() + [self.node("expression", "card", card_id="M")]
        edges = [self.edge("owns", "ground", "expression", "has_minimal_expression")]
        row = self.route(nodes, edges)["expression"]
        self.assertEqual(row["address_state"], "recorded_route")
        self.assertEqual(json.loads(row["route"])[0]["direction"], "owner")

    def test_prerequisite_is_addressed_by_its_declared_dependent(self):
        nodes = self.base() + [self.node("premise", "card", card_id="A")]
        edges = [self.edge("dep", "ground", "premise", "depends_on")]
        row = self.route(nodes, edges)["premise"]
        self.assertEqual(row["address_state"], "recorded_route")
        self.assertEqual(json.loads(row["route"])[0]["direction"], "prerequisite_of")

    def test_evidence_bridge_preserves_limited_scope(self):
        nodes = self.base() + [self.node("evidence", "external_evidence")]
        edges = [self.edge("support", "claim", "evidence", "supported_by"),
                 self.edge("map", "evidence", "ground", "maps_to")]
        edges[0]["scope"] = "component-level only"
        row = self.route(nodes, edges)["claim"]
        self.assertEqual(row["address_state"], "recorded_route")
        self.assertEqual(json.loads(row["route"])[0]["scope"], "component-level only")
        self.assertIn("no status promotion", row["interpretation"])


class ProjectProjectionControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = cg.build_graph()
        cls.data = json.loads(cg.PROJECT_ENTITY.read_text(encoding="utf-8"))
        cls.cards = {node["card_id"]: node["id"] for node in cls.graph["nodes"]
                     if node["type"] == "card"}

    def test_project_is_queryable_and_has_four_scopes(self):
        self.assertEqual(cg.alias_map(self.graph)["FTS"], "project_fts")
        scopes = [edge for edge in self.graph["edges"] if edge["source"] == "project_fts"
                  and edge["relation"] == "has_research_scope"]
        self.assertEqual(len(scopes), 4)
        self.assertTrue(all(edge.get("assertion_kind") is None for edge in scopes))

    def test_removed_scope_edge_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph["edges"] = [edge for edge in graph["edges"] if edge["id"] != "project_scope_grounds"]
        with self.assertRaisesRegex(AssertionError, "Project entity/scope projection"):
            cg.validate_graph(graph)

    def test_changed_objective_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        next(node for node in graph["nodes"] if node["id"] == "project_fts")["objective"] = "Unrelated objective"
        with self.assertRaisesRegex(AssertionError, "Project entity/scope projection"):
            cg.validate_graph(graph)

    def test_unknown_anchor_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["scope_categories"][0]["anchor_card_ids"].append("MISSING_SCOPE_TARGET")
        builder = cg.GraphBuilder()
        with mock.patch.object(cg.json, "loads", return_value=data):
            with self.assertRaisesRegex(ValueError, "Invalid project anchors"):
                cg.add_project_entity(builder, self.cards)

    def test_duplicate_requirement_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["assertion_requirements"][1]["id"] = "R1"
        builder = cg.GraphBuilder()
        with mock.patch.object(cg.json, "loads", return_value=data):
            with self.assertRaisesRegex(ValueError, "R1-R6"):
                cg.add_project_entity(builder, self.cards)


if __name__ == "__main__":
    unittest.main()
