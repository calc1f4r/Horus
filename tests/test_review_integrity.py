"""Decision integrity fixtures; no target vulnerabilities or exploit execution."""
from copy import deepcopy
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from horus_review.core import check_bundle, check_lineage, evidence_digest, flag_contradiction, reconcile_tally, remap_lineage, resolve_contradiction, summarize_ledger, tally, transition


class ReviewIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        data = b"Example review material.\nDocumented counting policy.\n"
        (self.root / "example.txt").write_bytes(data)
        source = {"id": "S1", "kind": "source", "path": "example.txt", "revision_key": "target",
                  "revision": "snapshot-1", "sha256": hashlib.sha256(data).hexdigest(), "line_start": 1, "line_end": 2}
        record = {"id": "F-001", "author_id": "author", "state": "supported", "kind": "finding",
                  "target_revision": "snapshot-1", "dependency_keys": [], "context_ids": ["S1"],
                  "components": {name: {"statement": f"Example {name} claim.", "status": "supported",
                                        "mode": "static", "evidence_ids": ["S1"]} for name in ("mechanism", "contract", "impact")},
                  "assumptions": {name: {"statement": "Explicit fixture assumption.", "evidence_ids": ["S1"],
                                         "contradicting_ids": []} for name in ("actors", "impact")}, "reviews": []}
        self.bundle = {"schema_version": 1, "revisions": {"target": "snapshot-1"}, "sources": [source],
                       "policy": {"version": 1, "axis": "technical_support", "reviewers": ["a", "b", "c"], "threshold": 2},
                       "records": [record], "lineage": {"inputs": ["raw-1"], "routes": [{"input_id": "raw-1", "candidate_ids": ["F-001"]}]},
                       "ledger": [{"id": "L1", "state": "closed", "revision_key": "target", "revision": "snapshot-1",
                                   "basis_ids": ["S1"], "candidate_ids": ["F-001"], "limitations": "Fixture, not a correctness proof."}],
                       "report_dispositions": [{"id": "F-001", "state": "published", "kind": "finding"}]}
        for who in ("a", "b", "c"):
            record["reviews"].append({"reviewer_id": who, "kind": "model", "technical_verdict": "supported",
                                      "component_ids": ["mechanism", "contract", "impact"], "input_ids": ["S1"], "venues": {}})
        self.sign()

    def sign(self, bundle=None):
        bundle = bundle or self.bundle
        for record in bundle["records"]:
            for review in record["reviews"]:
                review["evidence_digest"] = evidence_digest(record, bundle["sources"], bundle["policy"], bundle["revisions"])

    def codes(self, result):
        return {i["code"] for i in result["issues"]}

    def gate(self):
        return check_bundle(self.bundle, self.root, publication=True)

    def test_valid_static_record_passes_without_execution(self):
        result = self.gate()
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["publishable_ids"], ["F-001"])

    def test_component_omissions_preserve_id_and_block_publication(self):
        for component in ("mechanism", "contract", "impact"):
            with self.subTest(component=component):
                bundle = deepcopy(self.bundle)
                del bundle["records"][0]["components"][component]
                self.sign(bundle)
                result = check_bundle(bundle, self.root, publication=True)
                self.assertIn("COMPONENT_REQUIRED", self.codes(result))
                self.assertEqual(result["tally"]["results"][0]["id"], "F-001")
                self.assertIn("PUBLICATION_BLOCKED", self.codes(result))

    def test_unresolved_does_not_become_advisory(self):
        record = self.bundle["records"][0]
        record["state"] = "unresolved"
        record["components"]["impact"].update(status="unresolved", mode="unresolved", missing_evidence="No agreed impact interpretation")
        self.sign()
        self.bundle["report_dispositions"][0]["kind"] = "advisory"
        result = self.gate()
        self.assertIn("PUBLICATION_BLOCKED", self.codes(result))
        self.assertIn("REPORT_KIND", self.codes(result))
        self.assertEqual(len(result["blocked"]), 1)

    def test_supported_advisory_can_publish_its_own_supported_claim(self):
        self.bundle["records"][0]["kind"] = "advisory"
        self.bundle["report_dispositions"][0]["kind"] = "advisory"
        self.sign()
        self.assertTrue(self.gate()["ok"])

    def test_changed_claim_requires_new_approvals(self):
        self.bundle["records"][0]["components"]["impact"]["statement"] = "Changed claim"
        self.assertIn("REVIEW_STALE", self.codes(self.gate()))

    def test_changed_file_and_missing_range_do_not_resolve(self):
        (self.root / "example.txt").write_text("Changed snapshot")
        self.assertIn("SOURCE_UNRESOLVED", self.codes(self.gate()))

    def test_range_and_path_traversal_fail(self):
        self.bundle["sources"][0]["line_end"] = 200
        self.sign()
        self.assertIn("SOURCE_UNRESOLVED", self.codes(self.gate()))
        self.bundle["sources"][0]["line_end"] = 2
        self.bundle["sources"][0]["path"] = "../outside.txt"
        self.sign()
        result = self.gate()
        self.assertTrue(any("leaves the evidence root" in i["detail"] for i in result["issues"]))

    def test_declared_material_dependency_needs_revision(self):
        self.bundle["records"][0]["dependency_keys"] = ["missing-dependency"]
        self.sign()
        self.assertIn("DEPENDENCY_UNPINNED", self.codes(self.gate()))

    def test_self_review_cannot_satisfy_publication(self):
        self.bundle["records"][0]["author_id"] = "a"
        self.sign()
        self.assertIn("REVIEW_PROVENANCE", self.codes(self.gate()))

    def test_all_eight_binary_majority_combinations(self):
        record = self.bundle["records"][0]
        for votes in itertools.product(("supported", "rejected"), repeat=3):
            for review, vote in zip(record["reviews"], votes):
                review["technical_verdict"] = vote
            result = tally(self.bundle["policy"], [record])["results"][0]
            expected = "supported" if votes.count("supported") >= 2 else "rejected"
            self.assertEqual(result["decision"], expected)

    def test_incomplete_panel_is_incomplete_and_retained(self):
        self.bundle["records"][0]["reviews"].pop()
        result = self.gate()
        self.assertEqual(result["tally"]["results"][0]["decision"], "incomplete")
        self.assertIn("PUBLICATION_BLOCKED", self.codes(result))

    def test_duplicate_vote_is_not_counted(self):
        record = self.bundle["records"][0]
        record["reviews"].append(deepcopy(record["reviews"][0]))
        with self.assertRaises(ValueError):
            tally(self.bundle["policy"], [record])

    def test_venue_severity_is_preserved_not_fused(self):
        record = self.bundle["records"][0]
        for who, severity in zip(record["reviews"], ("HIGH", "MEDIUM", "LOW")):
            who["venues"] = {"example-venue": {"eligibility": "eligible", "severity": severity, "basis_ids": ["S1"]}}
        self.bundle["report_dispositions"][0].update(venue="example-venue", decision_reviewer="b", severity="MEDIUM")
        self.bundle["policy"]["venue_adjudicators"] = {"example-venue": "b"}
        self.sign()
        self.assertTrue(self.gate()["ok"])
        self.bundle["report_dispositions"][0]["severity"] = "HIGH"
        self.assertIn("VENUE_DECISION", self.codes(self.gate()))

    def test_unscoped_severity_is_blocked(self):
        self.bundle["report_dispositions"][0]["severity"] = "HIGH"
        self.assertIn("UNSCOPED_SEVERITY", self.codes(self.gate()))

    def test_three_way_disagreement_and_two_reviewer_tie_are_contested(self):
        record = self.bundle["records"][0]
        for review, vote in zip(record["reviews"], ("supported", "rejected", "unresolved")):
            review["technical_verdict"] = vote
        self.assertEqual(tally(self.bundle["policy"], [record])["results"][0]["decision"], "contested")
        self.bundle["policy"].update(reviewers=["a", "b"], threshold=2)
        record["reviews"].pop()
        self.assertEqual(tally(self.bundle["policy"], [record])["results"][0]["decision"], "contested")

    def test_execution_mode_requires_an_execution_artifact(self):
        self.bundle["records"][0]["components"]["mechanism"]["mode"] = "executed"
        self.sign()
        self.assertIn("EVIDENCE_MODE_SOURCE", self.codes(self.gate()))

    def test_external_mode_requires_source_provenance(self):
        self.bundle["sources"][0]["kind"] = "external"
        self.sign()
        self.assertIn("EXTERNAL_PROVENANCE", self.codes(self.gate()))

    def test_contrary_evidence_needs_a_recorded_resolution(self):
        self.bundle["records"][0]["assumptions"]["actors"]["contradicting_ids"] = ["S1"]
        self.sign()
        self.assertIn("CONTRADICTION_REASON", self.codes(self.gate()))

    def test_venue_decision_requires_a_basis(self):
        self.bundle["records"][0]["reviews"][0]["venues"] = {"example": {"eligibility": "eligible", "severity": "HIGH"}}
        self.assertIn("EVIDENCE_REQUIRED", self.codes(self.gate()))

    def test_lifecycle_support_is_guarded_and_history_retained(self):
        record = self.bundle["records"][0]
        record["state"] = "candidate"
        changed = transition(self.bundle, "F-001", "supported", "Fresh component review", self.root, "owner")
        self.assertEqual(record["state"], "candidate")
        self.assertEqual(changed["records"][0]["history"][0]["from"], "candidate")
        self.assertTrue(check_bundle(changed, self.root, publication=True)["ok"])
        record["state"] = "rejected"
        with self.assertRaises(ValueError):
            transition(self.bundle, "F-001", "supported", "Unattributed reversal", self.root, "owner")

    def test_unresolved_component_cannot_transition_to_supported(self):
        record = self.bundle["records"][0]
        record["state"] = "unresolved"
        record["components"]["impact"].update(status="unresolved", mode="unresolved", missing_evidence="Missing specification")
        self.sign()
        with self.assertRaises(ValueError):
            transition(self.bundle, "F-001", "supported", "A label is not evidence", self.root, "owner")

    def test_reconciliation_detects_omission_and_extra_id(self):
        computed = tally(self.bundle["policy"], self.bundle["records"])
        result = reconcile_tally(computed, ["unknown"])
        self.assertFalse(result["ok"])
        self.assertEqual(result["omitted_ids"], ["F-001"])
        self.assertEqual(result["extra_ids"], ["unknown"])

    def test_linked_ledger_contradiction_cannot_be_hidden_from_report(self):
        self.bundle["ledger"][0]["state"] = "contested"
        self.assertIn("PUBLICATION_BLOCKED", self.codes(self.gate()))
        self.assertIn("LEDGER_CONTESTED", self.gate()["blocked"]["F-001"])

    def test_linked_stale_closure_blocks_publication(self):
        self.bundle["ledger"][0]["revision"] = "old"
        self.assertIn("LEDGER_STALE", self.gate()["blocked"]["F-001"])

    def test_demotion_allowed_with_broken_evidence_and_attribution(self):
        (self.root / "example.txt").write_text("Changed source")
        changed = transition(self.bundle, "F-001", "unresolved", "Evidence snapshot changed", self.root, "owner")
        self.assertEqual(changed["records"][0]["state"], "unresolved")
        self.assertEqual(changed["records"][0]["history"][-1]["actor_id"], "owner")

    def test_contradiction_resolution_retains_flag_and_requires_fresh_review(self):
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Policy premise contradicted", "owner")
        fp = flagged["records"][0]["contradictions"][0]["fingerprint"]
        resolved = resolve_contradiction(flagged, fp, "owner", "Documented interpretation resolved", ["S1"])
        self.assertEqual(resolved["records"][0]["contradictions"][0]["status"], "resolved")
        self.assertIn("REVIEW_STALE", self.codes(check_bundle(resolved, self.root)))
        with self.assertRaises(ValueError):
            flag_contradiction(resolved, "L1", "S1", "Policy premise contradicted", "another-reviewer")
        self.sign(resolved)
        supported = transition(resolved, "F-001", "supported", "Fresh review accepted resolution", self.root, "owner")
        self.assertTrue(check_bundle(supported, self.root, publication=True)["ok"])

    def test_resolution_artifact_must_be_in_reviewer_inputs(self):
        source = deepcopy(self.bundle["sources"][0]); source["id"] = "S2"
        self.bundle["sources"].append(source)
        flagged = flag_contradiction(self.bundle, "L1", "S2", "New premise evidence", "owner")
        fp = flagged["records"][0]["contradictions"][0]["fingerprint"]
        resolved = resolve_contradiction(flagged, fp, "owner", "Specific resolution", ["S2"])
        self.sign(resolved)
        self.assertIn("REVIEW_INPUTS", self.codes(check_bundle(resolved, self.root)))

    def test_unrelated_sources_do_not_invalidate_other_records(self):
        second = deepcopy(self.bundle["records"][0]); second["id"] = "F-002"
        self.bundle["records"].append(second)
        self.bundle["lineage"]["routes"][0]["candidate_ids"].append("F-002")
        self.sign()
        prior = [evidence_digest(r, self.bundle["sources"], self.bundle["policy"], self.bundle["revisions"]) for r in self.bundle["records"]]
        unrelated = deepcopy(self.bundle["sources"][0]); unrelated["id"] = "S2"
        self.bundle["sources"].append(unrelated)
        self.assertEqual(prior, [evidence_digest(r, self.bundle["sources"], self.bundle["policy"], self.bundle["revisions"]) for r in self.bundle["records"]])
        self.assertTrue(check_bundle(self.bundle, self.root)["ok"])

    def test_orphan_and_bundle_errors_never_claim_publishability(self):
        self.bundle["lineage"]["routes"] = [{"input_id": "raw-1", "disposition": {"state": "deferred", "reason": "Awaiting review"}}]
        result = check_bundle(self.bundle, self.root)
        self.assertIn("LINEAGE_ORPHAN", result["blocked"]["F-001"])
        self.assertEqual(result["publishable_ids"], [])

    def test_venue_authority_cannot_be_cherry_picked(self):
        record = self.bundle["records"][0]
        for index, review in enumerate(record["reviews"]):
            review["venues"] = {"example": {"eligibility": "eligible" if index == 0 else "ineligible", "severity": "HIGH" if index == 0 else "LOW", "basis_ids": ["S1"]}}
        self.bundle["policy"]["venue_adjudicators"] = {"example": "b"}
        self.sign()
        self.bundle["report_dispositions"][0].update(venue="example", decision_reviewer="a", severity="HIGH")
        self.assertIn("VENUE_DECISION", self.codes(self.gate()))

    def test_intermediate_ids_require_explicit_final_mapping(self):
        intermediate = {"intermediate_namespace": "M", "inputs": ["raw-1"], "routes": [{"input_id": "raw-1", "candidate_ids": ["M-001"]}]}
        remapped = remap_lineage(intermediate, {"M-001": ["F-001"]})
        self.assertEqual(check_lineage(remapped, {"F-001"}, final=True), [])
        remapped["routes"][0]["candidate_ids"] = ["F-002"]
        self.assertIn("LINEAGE_REMAP_MISMATCH", {i["code"] for i in check_lineage(remapped, {"F-002"}, final=True)})

    def test_symlink_outside_evidence_root_fails(self):
        with tempfile.TemporaryDirectory() as outside:
            path = Path(outside) / "outside.txt"
            path.write_text("Outside artifact")
            (self.root / "link.txt").symlink_to(path)
            self.bundle["sources"][0]["path"] = "link.txt"
            self.sign()
            self.assertTrue(any("leaves the evidence root" in i["detail"] for i in self.gate()["issues"]))

    def test_supported_candidate_cannot_be_hidden_as_rejected(self):
        self.bundle["report_dispositions"][0].update(state="rejected", reason="Unsupported label change")
        self.assertIn("REPORT_REJECTION", self.codes(self.gate()))

    def test_malformed_review_reference_retains_other_candidate_dispositions(self):
        second = deepcopy(self.bundle["records"][0]); second["id"] = "F-002"
        self.bundle["records"].append(second)
        self.bundle["lineage"]["routes"][0]["candidate_ids"].append("F-002")
        self.sign()
        del self.bundle["records"][0]["reviews"][0]["input_ids"]
        result = check_bundle(self.bundle, self.root)
        self.assertEqual(set(result["blocked"]), {"F-001", "F-002"})
        self.assertIn("EVIDENCE_REQUIRED", result["blocked"]["F-001"])
        self.assertEqual(result["publishable_ids"], [])

    def test_cli_demotion_with_broken_evidence_returns_copy(self):
        path = self.root / "bundle.json"; path.write_text(json.dumps(self.bundle))
        (self.root / "example.txt").write_text("Changed snapshot")
        cli = Path(__file__).resolve().parents[1] / "scripts/review_integrity.py"
        run = subprocess.run([sys.executable, str(cli), "transition", str(path), "--evidence-root", str(self.root),
                              "--id", "F-001", "--state", "unresolved", "--reason", "Snapshot changed", "--actor-id", "owner"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(json.loads(run.stdout)["records"][0]["state"], "unresolved")
        self.assertEqual(json.loads(path.read_text())["records"][0]["state"], "supported")

    def test_cli_resolution_keeps_flag_and_does_not_approve(self):
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Policy corrected", "owner")
        fp = flagged["records"][0]["contradictions"][0]["fingerprint"]
        path = self.root / "bundle.json"; path.write_text(json.dumps(flagged))
        cli = Path(__file__).resolve().parents[1] / "scripts/review_integrity.py"
        run = subprocess.run([sys.executable, str(cli), "resolve", str(path), "--evidence-root", str(self.root),
                              "--fingerprint", fp, "--basis-id", "S1", "--reason", "Specific interpretation resolved", "--actor-id", "owner"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result["records"][0]["contradictions"][0]["status"], "resolved")
        self.assertEqual(result["records"][0]["state"], "contested")
        self.assertIn("REVIEW_STALE", self.codes(check_bundle(result, self.root)))

    def test_deleted_record_flag_cannot_revive_old_approvals(self):
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Policy corrected", "owner")
        fp = flagged["records"][0]["contradictions"][0]["fingerprint"]
        resolved = resolve_contradiction(flagged, fp, "owner", "Interpretation settled", ["S1"])
        del resolved["records"][0]["contradictions"]
        resolved["records"][0]["state"] = "supported"
        result = check_bundle(resolved, self.root, publication=True)
        self.assertIn("CONTRADICTION_COPIES", self.codes(result))
        self.assertIn("CONTRADICTION_HISTORY", self.codes(result))
        self.assertEqual(result["publishable_ids"], [])

    def test_ledger_resolution_is_validated_too(self):
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Policy corrected", "owner")
        fp = flagged["records"][0]["contradictions"][0]["fingerprint"]
        resolved = resolve_contradiction(flagged, fp, "owner", "Interpretation settled", ["S1"])
        del resolved["ledger"][0]["contradictions"][0]["resolution"]
        self.assertIn("CONTRADICTION_RESOLUTION", self.codes(check_bundle(resolved, self.root)))

    def test_resolution_does_not_close_an_open_obligation(self):
        self.bundle["ledger"][0].update(state="open", basis_ids=[])
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Policy corrected", "owner")
        fp = flagged["records"][0]["contradictions"][0]["fingerprint"]
        resolved = resolve_contradiction(flagged, fp, "owner", "One premise resolved", ["S1"])
        self.assertEqual(resolved["ledger"][0]["state"], "open")
        self.assertEqual(check_bundle(resolved, self.root)["ledger"]["counts"], {"open": 1})

    def test_new_link_inherits_resolution_and_mixed_copies_can_be_repaired(self):
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Policy corrected", "owner")
        fp = flagged["records"][0]["contradictions"][0]["fingerprint"]
        resolved = resolve_contradiction(flagged, fp, "owner", "First interpretation", ["S1"])
        second = deepcopy(self.bundle["records"][0]); second["id"] = "F-002"
        resolved["records"].append(second)
        resolved["ledger"][0]["candidate_ids"].append("F-002")
        resolved["lineage"]["routes"][0]["candidate_ids"].append("F-002")
        inherited = flag_contradiction(resolved, "L1", "S1", "Policy corrected", "owner")
        self.assertEqual(inherited["records"][1]["contradictions"][0]["status"], "resolved")
        self.assertEqual(inherited["records"][1]["state"], "contested")
        inherited["records"][1]["contradictions"][0]["status"] = "open"
        del inherited["records"][1]["contradictions"][0]["resolution"]
        repaired = resolve_contradiction(inherited, fp, "owner", "Consistent resolution for both", ["S1"])
        self.sign(repaired)
        result = check_bundle(repaired, self.root)
        self.assertNotIn("CONTRADICTION_COPIES", self.codes(result))
        self.assertTrue(result["ok"], result)

    def test_policy_change_invalidates_claim_approvals(self):
        self.bundle["policy"]["venue_adjudicators"] = {"example": "a"}
        self.assertIn("REVIEW_STALE", self.codes(self.gate()))

    def test_venue_rule_snapshot_is_digest_bound_and_dependency_declared(self):
        data = b"Example venue policy.\n"; (self.root / "rules.txt").write_bytes(data)
        source = {"id": "RULES", "kind": "spec", "path": "rules.txt", "revision_key": "rules", "revision": "rules-1",
                  "sha256": hashlib.sha256(data).hexdigest(), "line_start": 1, "line_end": 1}
        self.bundle["sources"].append(source); self.bundle["revisions"]["rules"] = "rules-1"
        record = self.bundle["records"][0]; record["context_ids"].append("RULES"); record["dependency_keys"].append("rules")
        for review in record["reviews"]:
            review["input_ids"].append("RULES")
            review["venues"] = {"example": {"eligibility": "eligible", "severity": "LOW", "basis_ids": ["RULES"]}}
        self.sign(); self.assertTrue(self.gate()["ok"])
        data = b"Changed venue policy.\n"; (self.root / "rules.txt").write_bytes(data)
        source["sha256"] = hashlib.sha256(data).hexdigest(); source["revision"] = "rules-2"; self.bundle["revisions"]["rules"] = "rules-2"
        self.assertIn("REVIEW_STALE", self.codes(self.gate()))
        record["dependency_keys"] = []; self.sign()
        self.assertIn("DEPENDENCY_UNDECLARED", self.codes(self.gate()))

    def test_multistream_lineage_can_extend_remapped_shard_inputs(self):
        intermediate = {"intermediate_namespace": "M", "inputs": ["raw-1"], "routes": [{"input_id": "raw-1", "candidate_ids": ["M-001"]}]}
        lineage = remap_lineage(intermediate, {"M-001": ["F-001"]})
        lineage["inputs"].append("other-stream:1")
        lineage["routes"].append({"input_id": "other-stream:1", "candidate_ids": ["F-002"]})
        self.assertEqual(check_lineage(lineage, {"F-001", "F-002"}, final=True), [])

    def test_clean_record_can_be_supported_while_another_is_pending_review(self):
        second = deepcopy(self.bundle["records"][0]); second["id"] = "F-002"
        self.bundle["records"].append(second); self.bundle["lineage"]["routes"][0]["candidate_ids"].append("F-002")
        entry = deepcopy(self.bundle["ledger"][0]); entry["id"] = "L2"; entry["candidate_ids"] = ["F-002"]
        self.bundle["ledger"].append(entry); self.bundle["records"][0]["state"] = "candidate"; self.sign()
        flagged = flag_contradiction(self.bundle, "L2", "S1", "Second claim needs review", "owner")
        result = transition(flagged, "F-001", "supported", "First claim independently supported", self.root, "owner")
        self.assertEqual(result["records"][0]["state"], "supported")
        self.assertEqual(result["records"][1]["state"], "contested")

    def test_contested_report_requires_an_actual_recorded_dispute(self):
        self.bundle["report_dispositions"][0].update(state="contested", reason="No actual dispute")
        self.assertIn("REPORT_CONTESTED", self.codes(self.gate()))

    def test_preexisting_manual_contest_survives_specific_flag_resolution(self):
        self.bundle["ledger"][0]["state"] = "contested"
        flagged = flag_contradiction(self.bundle, "L1", "S1", "One separate premise", "owner")
        fp = flagged["records"][0]["contradictions"][0]["fingerprint"]
        resolved = resolve_contradiction(flagged, fp, "owner", "Only that premise resolved", ["S1"])
        self.assertEqual(resolved["ledger"][0]["state"], "contested")
        self.sign(resolved)
        with self.assertRaises(ValueError):
            transition(resolved, "F-001", "supported", "Unrelated dispute remains", self.root, "owner")
        self.assertIn("LEDGER_CONTESTED", check_bundle(resolved, self.root)["blocked"]["F-001"])

    def test_multiple_flag_resolution_order_preserves_original_ledger_state(self):
        first = flag_contradiction(self.bundle, "L1", "S1", "First premise", "owner")
        second = flag_contradiction(first, "L1", "S1", "Second premise", "owner")
        fingerprints = [f["fingerprint"] for f in second["ledger"][0]["contradictions"]]
        for order in (fingerprints, list(reversed(fingerprints))):
            result = deepcopy(second)
            result = resolve_contradiction(result, order[0], "owner", "First resolution", ["S1"])
            self.assertEqual(result["ledger"][0]["state"], "contested")
            result = resolve_contradiction(result, order[1], "owner", "Second resolution", ["S1"])
            self.assertEqual(result["ledger"][0]["state"], "closed")

    def test_surviving_merge_inventory_detects_a_deleted_member(self):
        raw = {"intermediate_namespace": "M", "inputs": ["one", "two", "three"],
               "input_records": [{"id": name} for name in ("one", "two", "three")],
               "routes": [{"input_id": name, "candidate_ids": ["M-001"]} for name in ("one", "two", "three")]}
        lineage = remap_lineage(raw, {"M-001": ["F-001"]})
        lineage["inputs"].remove("two")
        lineage["routes"] = [r for r in lineage["routes"] if r["input_id"] != "two"]
        lineage["merge_routes"] = [r for r in lineage["merge_routes"] if r["input_id"] != "two"]
        self.assertIn("LINEAGE_INVENTORY", {i["code"] for i in check_lineage(lineage, {"F-001"}, final=True)})

    def test_ledger_history_detects_deleted_flag_copies(self):
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Corrected premise", "owner")
        del flagged["ledger"][0]["contradictions"]
        del flagged["records"][0]["contradictions"]
        flagged["records"][0]["history"] = []
        flagged["records"][0]["state"] = "supported"
        self.assertIn("CONTRADICTION_HISTORY", self.codes(check_bundle(flagged, self.root)))

    def test_original_affected_candidate_cannot_be_silently_unlinked(self):
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Corrected premise", "owner")
        fp = flagged["records"][0]["contradictions"][0]["fingerprint"]
        resolved = resolve_contradiction(flagged, fp, "owner", "One resolution", ["S1"])
        resolved["ledger"][0]["candidate_ids"] = []
        del resolved["records"][0]["contradictions"]; resolved["records"][0]["history"] = []
        resolved["records"][0]["state"] = "supported"
        result = check_bundle(resolved, self.root, publication=True)
        self.assertIn("CONTRADICTION_AFFECTED", self.codes(result))
        self.assertFalse(result["ok"])

    def test_unrelated_precandidate_flag_does_not_block_clean_support_transition(self):
        data = b"Separate pre-candidate review material.\n"; (self.root / "unrelated.txt").write_bytes(data)
        source = deepcopy(self.bundle["sources"][0]); source.update(id="S9", path="unrelated.txt", sha256=hashlib.sha256(data).hexdigest(), line_end=1)
        self.bundle["sources"].append(source)
        self.bundle["ledger"].append({"id": "L9", "state": "open", "revision_key": "target", "revision": "snapshot-1", "basis_ids": [], "candidate_ids": []})
        self.bundle["records"][0]["state"] = "candidate"
        flagged = flag_contradiction(self.bundle, "L9", "S9", "Unrelated premise", "owner")
        (self.root / "unrelated.txt").write_text("Changed unrelated material")
        updated = transition(flagged, "F-001", "supported", "Independent claim supported", self.root, "owner")
        self.assertEqual(updated["records"][0]["state"], "supported")

    def test_inventory_is_checked_when_importer_drops_remap_metadata(self):
        lineage = {"inputs": ["one", "three"], "input_records": [{"id": k} for k in ("one", "two", "three")],
                   "routes": [{"input_id": k, "candidate_ids": ["F-001"]} for k in ("one", "three")]}
        codes = {i["code"] for i in check_lineage(lineage, {"F-001"}, final=True)}
        self.assertIn("LINEAGE_INVENTORY", codes)
        self.assertIn("LINEAGE_REMAP_REQUIRED", codes)

    def test_unlinked_candidate_is_blocked_from_support_transition(self):
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Corrected premise", "owner")
        fp = flagged["records"][0]["contradictions"][0]["fingerprint"]
        resolved = resolve_contradiction(flagged, fp, "owner", "One resolution", ["S1"])
        resolved["ledger"][0]["candidate_ids"] = []
        del resolved["records"][0]["contradictions"]; resolved["records"][0]["history"] = []
        resolved["records"][0]["state"] = "candidate"
        result = check_bundle(resolved, self.root)
        self.assertIn("CONTRADICTION_AFFECTED", result["blocked"]["F-001"])
        with self.assertRaises(ValueError):
            transition(resolved, "F-001", "supported", "Unlinked metadata is inconsistent", self.root, "owner")

    def test_lineage_merges_splits_and_exclusions(self):
        lineage = {"inputs": ["one", "two", "three"], "routes": [
            {"input_id": "one", "candidate_ids": ["F1", "F2"]},
            {"input_id": "two", "candidate_ids": ["F1"]},
            {"input_id": "three", "disposition": {"state": "deferred", "reason": "Awaiting context"}}]}
        self.assertEqual(check_lineage(lineage, {"F1", "F2"}), [])
        lineage["routes"].pop()
        self.assertIn("LINEAGE_LOSS", {i["code"] for i in check_lineage(lineage, {"F1", "F2"})})

    def test_report_omission_fails_conservation(self):
        self.bundle["report_dispositions"] = []
        self.assertIn("REPORT_CONSERVATION", self.codes(self.gate()))

    def test_ledger_unsupported_and_stale_are_visible(self):
        entry = self.bundle["ledger"][0]
        entry["basis_ids"] = []
        result = summarize_ledger([entry], self.bundle["revisions"], {"S1"})
        self.assertEqual(result["counts"], {"unsupported_closure": 1})
        entry["revision"] = "old"
        self.assertEqual(summarize_ledger([entry], self.bundle["revisions"], {"S1"})["counts"], {"stale": 1})

    def test_manual_contradiction_is_attributable_idempotent_and_blocks(self):
        original = deepcopy(self.bundle)
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Corrected policy premise", "owner")
        again = flag_contradiction(flagged, "L1", "S1", "Corrected policy premise", "owner")
        self.assertEqual(self.bundle, original)
        self.assertEqual(len(again["records"][0]["contradictions"]), 1)
        self.assertEqual(again["records"][0]["state"], "contested")
        result = check_bundle(again, self.root, publication=True)
        self.assertIn("OPEN_CONTRADICTION", result["blocked"]["F-001"])
        self.assertIn("PUBLICATION_BLOCKED", self.codes(result))

    def test_contradiction_cannot_reference_missing_candidate(self):
        self.bundle["ledger"][0]["candidate_ids"] = ["missing"]
        with self.assertRaises(ValueError):
            flag_contradiction(self.bundle, "L1", "S1", "Specific premise", "owner")

    def test_new_artifact_can_flag_without_refreshing_stale_approvals(self):
        source = deepcopy(self.bundle["sources"][0])
        source["id"] = "S2"
        self.bundle["sources"].append(source)
        self.assertNotIn("REVIEW_STALE", self.codes(self.gate()))
        path = self.root / "bundle.json"
        path.write_text(json.dumps(self.bundle))
        cli = Path(__file__).resolve().parents[1] / "scripts/review_integrity.py"
        run = subprocess.run([sys.executable, str(cli), "contradict", str(path), "--evidence-root", str(self.root),
                              "--entry-id", "L1", "--source-id", "S2", "--premise", "New specification contradicts a premise",
                              "--actor-id", "owner"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        flagged = json.loads(run.stdout)
        self.assertEqual(flagged["records"][0]["state"], "contested")
        self.assertEqual(flagged["records"][0]["contradictions"][0]["source_id"], "S2")

    def test_cli_gate_and_malformed_input_return_clear_exit_codes(self):
        path = self.root / "bundle.json"
        path.write_text(json.dumps(self.bundle))
        cli = Path(__file__).resolve().parents[1] / "scripts/review_integrity.py"
        run = subprocess.run([sys.executable, str(cli), "gate", str(path), "--evidence-root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        path.write_text("{invalid")
        run = subprocess.run([sys.executable, str(cli), "gate", str(path), "--evidence-root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertEqual(json.loads(run.stdout)["issues"][0]["code"], "MALFORMED_INPUT")

    def test_declared_dependency_pin_change_requires_fresh_reviews(self):
        self.bundle["revisions"]["material-dep"] = "dep-1"
        self.bundle["records"][0]["dependency_keys"] = ["material-dep"]
        self.sign()
        self.assertTrue(self.gate()["ok"])
        self.bundle["revisions"]["material-dep"] = "dep-2"
        self.assertIn("REVIEW_STALE", self.codes(self.gate()))
        self.sign()
        self.assertTrue(self.gate()["ok"])

    def test_unrelated_revision_pin_change_does_not_stale_reviews(self):
        self.bundle["revisions"]["unrelated"] = "unrelated-1"
        self.sign()
        self.bundle["revisions"]["unrelated"] = "unrelated-2"
        self.assertTrue(self.gate()["ok"])

    def test_version_fields_require_integer_one(self):
        for field in ("schema_version", "policy"):
            for value in (True, 1.0, "1", None):
                with self.subTest(field=field, value=value):
                    bundle = deepcopy(self.bundle)
                    if field == "policy":
                        bundle[field]["version"] = value
                    else:
                        bundle[field] = value
                    self.sign(bundle)
                    with self.assertRaises(ValueError):
                        check_bundle(bundle, self.root, publication=True)

    def test_cli_rejects_duplicate_json_members_at_every_depth(self):
        data = json.dumps(self.bundle)
        variants = [data.replace('"schema_version": 1', '"schema_version": 999, "schema_version": 1', 1),
                    data.replace('"status": "supported"', '"status": "unresolved", "status": "supported"', 1)]
        cli = Path(__file__).resolve().parents[1] / "scripts/review_integrity.py"
        path = self.root / "bundle.json"
        for text in variants:
            with self.subTest(text=text[:80]):
                path.write_text(text)
                run = subprocess.run([sys.executable, str(cli), "gate", str(path), "--evidence-root", str(self.root)], capture_output=True, text=True)
                self.assertEqual(run.returncode, 1)
                self.assertEqual(json.loads(run.stdout)["issues"][0]["code"], "MALFORMED_INPUT")
                self.assertIn("Duplicate JSON member", json.loads(run.stdout)["issues"][0]["detail"])

    def test_cli_rejects_nonfinite_numbers_in_ignored_metadata(self):
        cli = Path(__file__).resolve().parents[1] / "scripts/review_integrity.py"
        path = self.root / "bundle.json"
        for token in ("NaN", "Infinity", "-Infinity", "1e999"):
            with self.subTest(token=token):
                data = json.dumps(self.bundle)
                path.write_text('{"metadata": ' + token + ', ' + data[1:])
                run = subprocess.run([sys.executable, str(cli), "gate", str(path), "--evidence-root", str(self.root)], capture_output=True, text=True)
                self.assertEqual(run.returncode, 1)
                self.assertEqual(json.loads(run.stdout)["issues"][0]["code"], "MALFORMED_INPUT")

    def test_remap_rejects_duplicate_mapping_keys(self):
        cli = Path(__file__).resolve().parents[1] / "scripts/review_integrity.py"
        lineage = self.root / "lineage.json"
        lineage.write_text(json.dumps({"inputs": ["raw-1"], "routes": [{"input_id": "raw-1", "candidate_ids": ["M-001"]}]}))
        mapping = self.root / "mapping.json"
        mapping.write_text('{"M-001": ["F-999"], "M-001": ["F-001"]}')
        run = subprocess.run([sys.executable, str(cli), "remap", str(lineage), "--mapping", str(mapping)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertIn("Duplicate JSON member", json.loads(run.stdout)["issues"][0]["detail"])

    def test_flag_source_hash_and_fingerprint_must_match_retained_artifact(self):
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Generic correction", "owner")
        fp = flagged["ledger"][0]["contradictions"][0]["fingerprint"]
        resolved = resolve_contradiction(flagged, fp, "owner", "Generic resolution", ["S1"])
        resolved["records"][0]["state"] = "supported"
        self.sign(resolved)
        self.assertTrue(check_bundle(resolved, self.root, publication=True)["ok"])
        for field, value, code in (("source_sha256", "f" * 64, "CONTRADICTION_SOURCE"),
                                   ("fingerprint", "f" * 64, "CONTRADICTION_FINGERPRINT"),
                                   ("premise", "Changed retained premise", "CONTRADICTION_FINGERPRINT"),
                                   ):
            with self.subTest(field=field):
                bundle = deepcopy(resolved)
                for obj in [bundle["ledger"][0], bundle["records"][0]]:
                    obj["contradictions"][0][field] = value
                self.sign(bundle)
                self.assertIn(code, self.codes(check_bundle(bundle, self.root, publication=True)))

    def test_precandidate_flags_require_correct_entry_and_unique_fingerprint(self):
        self.bundle["ledger"][0]["candidate_ids"] = []
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Generic pending correction", "owner")
        entry = flagged["ledger"][0]
        entry["contradictions"][0]["entry_id"] = "OTHER"
        self.assertIn("CONTRADICTION_LINK", self.codes(check_bundle(flagged, self.root)))
        entry["contradictions"].append(deepcopy(entry["contradictions"][0]))
        self.assertIn("CONTRADICTION_FINGERPRINT", self.codes(check_bundle(flagged, self.root)))

    def test_identifier_aliases_and_reserved_id_are_rejected(self):
        for value in ("F-001 ", " F-001", "F-001\u00a0", "F-00\u0411", "bundle"):
            with self.subTest(value=value):
                bundle = deepcopy(self.bundle)
                bundle["records"][0]["id"] = value
                with self.assertRaises(ValueError):
                    check_bundle(bundle, self.root)
        self.bundle["records"][0]["author_id"] = "a "
        with self.assertRaises(ValueError):
            check_bundle(self.bundle, self.root)

    def test_source_record_id_collision_does_not_misattribute_source_error(self):
        second = deepcopy(self.bundle["records"][0]); second["id"] = "F-002"
        self.bundle["records"].append(second); self.bundle["lineage"]["routes"][0]["candidate_ids"].append("F-002")
        source = deepcopy(self.bundle["sources"][0]); source.update(id="F-002", sha256="f" * 64)
        self.bundle["sources"].append(source); self.sign()
        result = check_bundle(self.bundle, self.root)
        issue = next(i for i in result["issues"] if i["code"] == "SOURCE_UNRESOLVED")
        self.assertEqual(issue["scope"], "source")
        self.assertEqual(result["blocked"]["F-002"], [])

    def test_record_error_does_not_block_another_record_citing_same_named_source(self):
        second = deepcopy(self.bundle["records"][0]); second["id"] = "F-002"
        self.bundle["records"].append(second); self.bundle["lineage"]["routes"][0]["candidate_ids"].append("F-002")
        source = deepcopy(self.bundle["sources"][0]); source["id"] = "F-002"
        self.bundle["sources"].append(source)
        first = self.bundle["records"][0]; first["state"] = "candidate"; first["context_ids"].append("F-002")
        for review in first["reviews"]:
            review["input_ids"].append("F-002")
        self.sign(); second["components"]["impact"]["statement"] = "Unrelated changed claim"
        result = transition(self.bundle, "F-001", "supported", "Relevant evidence remains fresh", self.root, "owner")
        self.assertEqual(result["records"][0]["state"], "supported")

    def test_duplicate_input_route_blocks_its_candidate_transition(self):
        self.bundle["lineage"]["routes"].append(deepcopy(self.bundle["lineage"]["routes"][0]))
        self.bundle["records"][0]["state"] = "candidate"
        result = check_bundle(self.bundle, self.root)
        self.assertIn("LINEAGE_ROUTE", result["blocked"]["F-001"])
        self.assertEqual(next(i for i in result["issues"] if i["code"] == "LINEAGE_ROUTE")["scope"], "input")
        with self.assertRaises(ValueError):
            transition(self.bundle, "F-001", "supported", "Cannot ignore duplicate lineage", self.root, "owner")

    def test_unreviewed_or_unanimously_unresolved_disposition_is_deferred(self):
        for votes in ([], ["unresolved"] * 3):
            with self.subTest(votes=votes):
                bundle = deepcopy(self.bundle); record = bundle["records"][0]
                record["state"] = "unresolved"
                record["reviews"] = record["reviews"][:len(votes)]
                for review, vote in zip(record["reviews"], votes):
                    review["technical_verdict"] = vote
                bundle["report_dispositions"][0] = {"id": "F-001", "state": "contested", "reason": "No actual disagreement"}
                self.assertIn("REPORT_CONTESTED", self.codes(check_bundle(bundle, self.root, publication=True)))
                bundle["report_dispositions"][0].update(state="deferred", reason="Awaiting substantive review")
                self.assertTrue(check_bundle(bundle, self.root, publication=True)["ok"])

    def test_actual_partial_panel_disagreement_can_be_contested(self):
        record = self.bundle["records"][0]; record["state"] = "unresolved"
        record["reviews"].pop(); record["reviews"][0]["technical_verdict"] = "rejected"
        self.bundle["report_dispositions"][0] = {"id": "F-001", "state": "contested", "reason": "Recorded support/rejection disagreement"}
        result = self.gate()
        self.assertEqual(result["tally"]["results"][0]["decision"], "incomplete")
        self.assertTrue(result["ok"], result)

    def test_unpublished_dispositions_cannot_invent_a_severity(self):
        self.bundle["report_dispositions"][0].update(state="deferred", reason="Scheduling deferral")
        for field, value in (("severity", "CRITICAL"), ("venue", "example"), ("decision_reviewer", "a")):
            with self.subTest(field=field):
                bundle = deepcopy(self.bundle); bundle["report_dispositions"][0][field] = value
                self.assertIn("UNPUBLISHED_RATING", self.codes(check_bundle(bundle, self.root, publication=True)))

    def test_identity_and_stub_remaps_cannot_keep_intermediate_ids(self):
        raw = {"intermediate_namespace": "M", "inputs": ["raw-1"], "routes": [{"input_id": "raw-1", "candidate_ids": ["M-001"]}]}
        with self.assertRaises(ValueError):
            remap_lineage(raw, {"M-001": ["M-001"]})
        stub = deepcopy(raw); stub.update(candidate_remap={}, merge_routes=[])
        codes = {i["code"] for i in check_lineage(stub, {"M-001"}, final=True)}
        self.assertIn("LINEAGE_FINAL_NAMESPACE", codes)
        self.assertIn("LINEAGE_EMPTY_REMAP", codes)
        without_marker = deepcopy(raw); without_marker.pop("intermediate_namespace"); without_marker["input_records"] = [{"id": "raw-1"}]
        with self.assertRaises(ValueError):
            remap_lineage(without_marker, {"M-001": ["M-001"]})

    def test_empty_shard_inventory_needs_an_explicit_reason(self):
        empty = {"intermediate_namespace": "M", "inputs": [], "input_records": [], "routes": []}
        lineage = remap_lineage(empty, {})
        self.assertIn("LINEAGE_EMPTY_REMAP", {i["code"] for i in check_lineage(lineage, set(), final=True)})
        lineage["no_shard_inputs"] = "Reviewed shard contains no finding headers"
        self.assertEqual(check_lineage(lineage, set(), final=True), [])

    def test_structural_typos_are_errors_and_metadata_has_no_decision_semantics(self):
        for section, typo, value in (("assumption", "contradicting_id", ["S2"]), ("record", "contradiction", []), ("ledger", "components", {}), ("bundle", "ok", False)):
            with self.subTest(section=section):
                bundle = deepcopy(self.bundle)
                obj = {"assumption": bundle["records"][0]["assumptions"]["actors"], "record": bundle["records"][0], "ledger": bundle["ledger"][0], "bundle": bundle}[section]
                obj[typo] = value
                with self.assertRaises(ValueError):
                    check_bundle(bundle, self.root)
        self.bundle["metadata"] = {"ok": False, "note": "Display only"}
        self.assertTrue(self.gate()["ok"])

    def test_missing_component_object_does_not_convert_record_to_ledger_on_resolution(self):
        flagged = flag_contradiction(self.bundle, "L1", "S1", "Generic correction", "owner")
        fp = flagged["ledger"][0]["contradictions"][0]["fingerprint"]
        del flagged["records"][0]["components"]
        resolved = resolve_contradiction(flagged, fp, "owner", "Generic resolution", ["S1"])
        self.assertEqual(resolved["records"][0]["state"], "contested")
        self.assertNotIn("basis_ids", resolved["records"][0])

    def test_line_ranges_follow_lf_not_unicode_control_separators(self):
        for separator in ("\x0c", "\x0b", "\u2028", "\u0085", "\r"):
            with self.subTest(separator=repr(separator)):
                data = ("one" + separator + "two\n").encode()
                (self.root / "example.txt").write_bytes(data)
                self.bundle["sources"][0]["sha256"] = hashlib.sha256(data).hexdigest()
                self.sign()
                self.assertIn("SOURCE_UNRESOLVED", self.codes(self.gate()))
        data = b"one\r\ntwo\r\n"; (self.root / "example.txt").write_bytes(data)
        self.bundle["sources"][0]["sha256"] = hashlib.sha256(data).hexdigest(); self.sign()
        self.assertTrue(self.gate()["ok"])

    def test_cli_deep_nesting_and_duplicate_digest_ids_fail_clearly(self):
        cli = Path(__file__).resolve().parents[1] / "scripts/review_integrity.py"; path = self.root / "bundle.json"
        path.write_text('[' * 1200 + '0' + ']' * 1200)
        run = subprocess.run([sys.executable, str(cli), "digest", str(path)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1); self.assertEqual(json.loads(run.stdout)["issues"][0]["code"], "MALFORMED_INPUT")
        self.bundle["records"].append(deepcopy(self.bundle["records"][0])); path.write_text(json.dumps(self.bundle))
        run = subprocess.run([sys.executable, str(cli), "digest", str(path)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1); self.assertEqual(json.loads(run.stdout)["issues"][0]["code"], "MALFORMED_INPUT")

    def test_surviving_artifact_counts_detect_dropped_inventory_and_inputs(self):
        raw = {"intermediate_namespace": "M", "inputs": ["one", "two", "three"],
               "source_artifacts": [{"path": "example.md", "parsed_count": 3}],
               "routes": [{"input_id": key, "candidate_ids": ["M-001"]} for key in ("one", "two", "three")]}
        lineage = remap_lineage(raw, {"M-001": ["F-001"]})
        lineage["inputs"].remove("two")
        for field in ("routes", "merge_routes"):
            lineage[field] = [r for r in lineage[field] if r["input_id"] != "two"]
        self.assertIn("LINEAGE_ARTIFACT_COUNT", {i["code"] for i in check_lineage(lineage, {"F-001"}, final=True)})
        lineage.update(merge_routes=[], candidate_remap={}, no_shard_inputs="No inputs")
        self.assertIn("LINEAGE_ARTIFACT_COUNT", {i["code"] for i in check_lineage(lineage, {"F-001"}, final=True)})

    def test_artifact_counts_require_nonnegative_integers(self):
        lineage = {"inputs": [], "routes": [], "source_artifacts": [{"path": "example.md", "parsed_count": 0}]}
        for value in (True, -1, 1.0, "0", None):
            with self.subTest(value=value):
                lineage["source_artifacts"][0]["parsed_count"] = value
                self.assertIn("LINEAGE_ARTIFACT_COUNT", {i["code"] for i in check_lineage(lineage, set())})

    def test_marker_stripping_cannot_allow_identity_remapping(self):
        raw = {"inputs": ["one"], "routes": [{"input_id": "one", "candidate_ids": ["R-001"]}]}
        with self.assertRaises(ValueError):
            remap_lineage(raw, {"R-001": ["R-001"]})
        final = {"inputs": ["one"], "routes": [{"input_id": "one", "candidate_ids": ["M-001"]}],
                 "merge_routes": [{"input_id": "one", "candidate_ids": ["X-001"]}], "candidate_remap": {"X-001": ["M-001"]}}
        self.assertIn("LINEAGE_FINAL_NAMESPACE", {i["code"] for i in check_lineage(final, {"M-001"}, final=True)})

    def test_dangling_sibling_on_input_blocks_clean_candidate(self):
        self.bundle["lineage"]["routes"][0]["candidate_ids"].append("F-999")
        self.bundle["records"][0]["state"] = "candidate"
        result = check_bundle(self.bundle, self.root)
        self.assertIn("LINEAGE_DANGLING", result["blocked"]["F-001"])
        with self.assertRaises(ValueError):
            transition(self.bundle, "F-001", "supported", "Missing sibling must be retained", self.root, "owner")

    def test_missing_route_input_is_diagnostic_not_key_error(self):
        lineage = {"inputs": [], "routes": [{"candidate_ids": ["F-999"]}]}
        issues = check_lineage(lineage, set())
        self.assertIn("LINEAGE_DANGLING", {i["code"] for i in issues})
        self.assertIn("LINEAGE_ROUTE", {i["code"] for i in issues})



if __name__ == "__main__":
    unittest.main()
