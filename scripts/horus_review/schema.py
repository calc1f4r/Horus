"""Closed structural field sets and canonical identifiers for review records."""
import re


def is_identifier(value):
    return isinstance(value, str) and value != "bundle" and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]*", value) is not None


def _keys(obj, allowed, label):
    if not isinstance(obj, dict):
        raise ValueError(f"{label} must be an object")
    unknown = set(obj) - set(allowed) - {"metadata"}
    if unknown:
        raise ValueError(f"{label} contains unknown structural fields: {sorted(map(str, unknown))}")
    if "metadata" in obj and not isinstance(obj["metadata"], dict):
        raise ValueError(f"{label}.metadata must be a metadata object")


def _rows(obj, key, allowed, label):
    rows = obj.get(key, [])
    if not isinstance(rows, list):
        raise ValueError(f"{label}.{key} must be an array")
    for row in rows:
        _keys(row, allowed, f"{label}.{key}")
    return rows


FLAG = {"entry_id", "source_id", "source_sha256", "premise", "actor_id", "fingerprint", "status", "affected_candidate_ids", "resolution"}
RESOLUTION = {"actor_id", "reason", "basis_ids"}
HISTORY = {"from", "to", "actor_id", "reason", "fingerprint", "previous_resolution"}
ROUTE = {"input_id", "candidate_ids", "disposition"}
LINEAGE = {"schema_version", "heuristic_only", "intermediate_namespace", "source_artifacts", "input_records", "inputs", "routes", "merge_routes", "candidate_remap", "no_shard_inputs"}


def _corrections(obj, label):
    for flag in _rows(obj, "contradictions", FLAG, label):
        for key in ("entry_id", "source_id", "actor_id"):
            if key in flag and not is_identifier(flag[key]):
                raise ValueError(f"flag.{key} must be a canonical identifier")
        if "resolution" in flag:
            _keys(flag["resolution"], RESOLUTION, f"{label}.resolution")
            if "actor_id" in flag["resolution"] and not is_identifier(flag["resolution"]["actor_id"]):
                raise ValueError("resolution.actor_id must be a canonical identifier")
    for event in _rows(obj, "history", HISTORY, label):
        if "previous_resolution" in event:
            _keys(event["previous_resolution"], RESOLUTION, f"{label}.previous_resolution")


def validate_lineage_shape(lineage):
    _keys(lineage, LINEAGE, "lineage")
    for name in ("routes", "merge_routes"):
        for route in _rows(lineage, name, ROUTE, "lineage"):
            if "disposition" in route:
                _keys(route["disposition"], {"state", "reason"}, "route.disposition")
    _rows(lineage, "input_records", {"id", "original_id", "block_sha256", "severity", "confidence", "shard"}, "lineage")
    _rows(lineage, "source_artifacts", {"path", "sha256", "preamble_sha256", "preamble_bytes", "parsed_count"}, "lineage")


def validate_shape(bundle):
    """Reject typos rather than silently treating omitted evidence as empty."""
    _keys(bundle, {"schema_version", "revisions", "sources", "policy", "records", "lineage", "ledger", "recorded_supported_ids", "report_dispositions"}, "bundle")
    if "policy" in bundle:
        _keys(bundle["policy"], {"version", "axis", "reviewers", "threshold", "venue_adjudicators"}, "policy")
    _rows(bundle, "sources", {"id", "kind", "path", "revision_key", "revision", "sha256", "line_start", "line_end", "url"}, "bundle")
    for record in _rows(bundle, "records", {"id", "author_id", "target_revision", "kind", "state", "dependency_keys", "context_ids", "components", "assumptions", "reviews", "contradictions", "history"}, "bundle"):
        for key in ("id", "author_id"):
            if key in record and not is_identifier(record[key]):
                raise ValueError(f"record.{key} must be a canonical identifier")
        if "components" in record:
            _keys(record["components"], {"mechanism", "contract", "impact"}, "record.components")
            for name, component in record["components"].items():
                if name != "metadata":
                    _keys(component, {"statement", "status", "mode", "evidence_ids", "missing_evidence"}, "component")
        if "assumptions" in record:
            _keys(record["assumptions"], {"actors", "impact"}, "record.assumptions")
            for name, assumption in record["assumptions"].items():
                if name != "metadata":
                    _keys(assumption, {"statement", "evidence_ids", "contradicting_ids", "contradiction_resolution"}, "assumption")
        for review in _rows(record, "reviews", {"reviewer_id", "kind", "technical_verdict", "component_ids", "input_ids", "evidence_digest", "venues"}, "record"):
            if not is_identifier(review.get("reviewer_id")):
                raise ValueError("review.reviewer_id must be a canonical identifier")
            if "venues" in review:
                if not isinstance(review["venues"], dict):
                    raise ValueError("review.venues must be an object")
                for decision in review["venues"].values():
                    _keys(decision, {"eligibility", "severity", "basis_ids"}, "venue decision")
        _corrections(record, "record")
    for entry in _rows(bundle, "ledger", {"id", "revision_key", "revision", "state", "basis_ids", "limitations", "candidate_ids", "reason", "contradictions", "history", "pre_contradiction_state"}, "bundle"):
        _corrections(entry, "ledger")
    if "lineage" in bundle and bundle["lineage"] is not None:
        validate_lineage_shape(bundle["lineage"])
    _rows(bundle, "report_dispositions", {"id", "state", "reason", "kind", "venue", "decision_reviewer", "severity"}, "bundle")
