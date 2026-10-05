"""The prose merge may select a representative but must retain every source ID."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from horus_review.core import check_lineage
from merge_shard_findings import parse_findings


class MergeLineageTests(unittest.TestCase):
    def test_inline_and_fenced_example_headers_do_not_create_inputs(self):
        content = "### F-001: Example\n\nReference: see ### F-002 above\n```markdown\n### F-003: Example quotation\n| Severity | HIGH |\n```\n| Severity | LOW |\n"
        findings = parse_findings(content, "example")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["severity"], "LOW")
        self.assertIn("F-003", findings[0]["body"])

    def test_unsupported_headers_preamble_fields_and_repeated_fields_fail(self):
        valid = "### F-001: Example\n| Severity | LOW |\n"
        for content in ("## F-002: Lost\n| Severity | HIGH |\n" + valid,
                        valid + "### Finding 4\n| Severity | HIGH |\n",
                        "| Root Cause | Unparsed claim |\n" + valid,
                        valid + "| Severity | HIGH |\n",
                        valid + "### F-001: Repeated ID\n",
                        valid + "```\nUnclosed example"):
            with self.subTest(content=content[:50]):
                with self.assertRaises(ValueError):
                    parse_findings(content, "example")

    def test_decorated_headers_fail_and_backtick_info_does_not_hide_inputs(self):
        for header in ("### [F-002] Title", "### **F-002**: Title"):
            with self.subTest(header=header):
                with self.assertRaises(ValueError):
                    parse_findings("### F-001: First\nBody\n" + header + "\nSeparate claim", "example")
        content = "```x```\n### F-001: Actual finding\n| Severity | LOW |\n```x```"
        self.assertEqual(len(parse_findings(content, "example")), 1)

    def test_malformed_header_has_clear_failure(self):
        with self.assertRaises(ValueError):
            parse_findings("### F-: Malformed\n\nExample body", "example")

    def test_representative_replacement_retains_all_members(self):
        template = "### F-001: Example\n\n| Affected Code | example:1 |\n| Root Cause | Counting policy |\n| Severity | {} |\n| Confidence | {} |\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "03-findings-shard-one.md").write_text(template.format("LOW", "LOW"))
            (root / "03-findings-shard-two.md").write_text(template.format("MEDIUM", "HIGH"))
            (root / "03-findings-shard-three.md").write_text(template.format("LOW", "LOW"))
            script = Path(__file__).resolve().parents[1] / "scripts/merge_shard_findings.py"
            result = subprocess.run([sys.executable, str(script), str(root)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            lineage = json.loads((root / "03-merge-lineage.json").read_text())
            self.assertEqual(len(lineage["inputs"]), 3)
            self.assertEqual({r["input_id"] for r in lineage["routes"]}, set(lineage["inputs"]))
            self.assertEqual({r["candidate_ids"][0] for r in lineage["routes"]}, {"M-001"})
            self.assertEqual(check_lineage(lineage, {"M-001"}), [])
            self.assertIn("LINEAGE_REMAP_REQUIRED", {i["code"] for i in check_lineage(lineage, {"M-001"}, final=True)})
            self.assertEqual({r["confidence"] for r in lineage["input_records"]}, {"HIGH", "LOW"})
            self.assertEqual({r["severity"] for r in lineage["input_records"]}, {"MEDIUM", "LOW"})
            self.assertTrue(all(r["original_id"] == "F-001" and len(r["block_sha256"]) == 64 for r in lineage["input_records"]))
            self.assertTrue(lineage["heuristic_only"])
            self.assertEqual(len(lineage["source_artifacts"]), 3)
            self.assertIn("| Confidence | HIGH |", (root / "03-findings-raw.md").read_text())
