#!/usr/bin/env python3
"""Unit tests for hunt-card enrichment integration."""

import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from horus_retrieval.enrichment import enrich_huntcards  # noqa: E402
from horus_retrieval.writers import write_json  # noqa: E402


class TestEnrichment(unittest.TestCase):

    def test_enrich_huntcards_rewrites_combined_file_from_per_manifest_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            huntcards_dir = Path(tmp) / "huntcards"
            huntcards_dir.mkdir()
            write_json(
                huntcards_dir / "oracle-huntcards.json",
                {
                    "meta": {"totalCards": 1},
                    "cards": [{"id": "oracle-1", "title": "Oracle"}],
                },
            )
            write_json(
                huntcards_dir / "tokens-huntcards.json",
                {
                    "meta": {"totalCards": 1},
                    "cards": [{"id": "token-1", "title": "Token"}],
                },
            )
            write_json(
                huntcards_dir / "all-huntcards.json",
                {"meta": {"totalCards": 999}, "cards": []},
            )

            fake_module = types.ModuleType("generate_micro_directives")

            def fake_enrich_huntcard_file(input_path, output_path):
                with Path(input_path).open(encoding="utf-8") as f:
                    data = json.load(f)
                for card in data["cards"]:
                    card["check"] = ["verify exact condition"]
                with Path(output_path).open("w", encoding="utf-8") as f:
                    json.dump(data, f)
                return {"total": len(data["cards"]), "enriched": len(data["cards"])}

            fake_module.enrich_huntcard_file = fake_enrich_huntcard_file
            previous_module = sys.modules.get("generate_micro_directives")
            sys.modules["generate_micro_directives"] = fake_module
            emitted = []
            try:
                enrich_huntcards(
                    huntcards_dir,
                    {"oracle": {}, "tokens": {}},
                    emitted.append,
                )
            finally:
                if previous_module is None:
                    sys.modules.pop("generate_micro_directives", None)
                else:
                    sys.modules["generate_micro_directives"] = previous_module

            with (huntcards_dir / "all-huntcards.json").open(encoding="utf-8") as f:
                combined = json.load(f)

        self.assertEqual(combined["meta"]["totalCards"], 2)
        self.assertEqual(combined["meta"]["enriched"], 2)
        self.assertEqual(combined["meta"]["manifests"], ["oracle", "tokens"])
        self.assertEqual(
            [card["check"] for card in combined["cards"]],
            [["verify exact condition"], ["verify exact condition"]],
        )
        self.assertTrue(any("oracle-huntcards.json" in line for line in emitted))
        self.assertTrue(any("all-huntcards.json" in line for line in emitted))


if __name__ == "__main__":
    unittest.main(verbosity=2)
