#!/usr/bin/env python3
"""Unit tests for retrieval category taxonomy."""

import os
import sys
import unittest


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from horus_retrieval.taxonomy import CATEGORY_MAP, GENERAL_SUBCATEGORIES  # noqa: E402


class TestTaxonomy(unittest.TestCase):

    def test_category_map_has_general_and_core_manifests(self):
        for category in ("oracle", "amm", "bridge", "tokens", "general", "sui-move"):
            with self.subTest(category=category):
                self.assertIn(category, CATEGORY_MAP)
                self.assertTrue(CATEGORY_MAP[category])

    def test_general_subcategories_are_disjoint(self):
        seen = {}
        for subcategory, config in GENERAL_SUBCATEGORIES.items():
            self.assertTrue(config["description"])
            self.assertTrue(config["folders"])
            for folder in config["folders"]:
                self.assertNotIn(folder, seen, f"{folder} appears in {subcategory} and {seen.get(folder)}")
                seen[folder] = subcategory


if __name__ == "__main__":
    unittest.main(verbosity=2)
