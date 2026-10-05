"""Versioned review records, policy replay, lineage and disposition checks.

These checks establish structural integrity, not truth or reviewer independence.
Revision identities and reviewer identities are supplied by the caller. Evidence
content is checked against hashes in the record; no code or URLs are executed.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlparse
from .schema import is_identifier, validate_shape, validate_lineage_shape

COMPONENTS = {"mechanism", "contract", "impact"}
STATES = {"candidate", "unresolved", "supported", "rejected", "contested"}
MODES = {"static", "executed", "external", "unresolved"}
SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "QA"}


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _objects(value, name):
    if not isinstance(value, list) or any(not isinstance(v, dict) for v in value):
        raise ValueError(f"{name} must be an array of objects")
    return value


def _strings(value, name, nonempty=False):
    if not isinstance(value, list) or any(not is_identifier(v) for v in value):
        raise ValueError(f"{name} must be an array of canonical identifiers")
    if len(set(value)) != len(value) or (nonempty and not value):
        raise ValueError(f"{name} must contain unique values and meet its minimum size")
    return value


def _index(rows, name):
    result = {}
    for row in _objects(rows, name):
        key = row.get("id")
        if not is_identifier(key) or key in result:
            raise ValueError(f"{name} requires unique, nonempty IDs")
        result[key] = row
    return result


def _issue(code, item, detail, scope="record", candidate_ids=None):
    result = {"code": code, "scope": "bundle" if item == "bundle" else scope, "id": item, "detail": detail}
    if candidate_ids is not None:
        result["candidate_ids"] = sorted(set(candidate_ids))
    return result


def _flags(obj):
    return _objects(obj.get("contradictions", []), "contradictions")


def _open_flags(obj):
    return any(flag.get("status", "open") != "resolved" for flag in _flags(obj))


def _reference_ids(record):
    ids = set(record.get("context_ids", []))
    for name, obj in record.get("components", {}).items():
        if name != "metadata" and isinstance(obj, dict):
            ids.update(obj.get("evidence_ids", []))
    for name, obj in record.get("assumptions", {}).items():
        if name != "metadata" and isinstance(obj, dict):
            ids.update(obj.get("evidence_ids", []))
            ids.update(obj.get("contradicting_ids", []))
    for flag in _flags(record):
        if flag.get("source_id"):
            ids.add(flag["source_id"])
        resolution = flag.get("resolution", {})
        if isinstance(resolution, dict):
            ids.update(resolution.get("basis_ids", []))
    return ids


def evidence_digest(record, sources, policy, revisions):
    """Bind review approvals to the claim and source snapshots, not prose labels."""
    claim = {k: v for k, v in record.items() if k not in {"reviews", "state", "history"}}
    relied = _reference_ids(record)
    pins = {key: revisions.get(key) for key in {"target", *record.get("dependency_keys", [])}}
    payload = {"digest_version": 2, "record": claim, "policy": policy, "revisions": pins,
               "sources": sorted((s for s in sources if s["id"] in relied), key=lambda s: s["id"])}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def bundle_digests(bundle):
    """Compute digests without silently collapsing duplicate declared IDs."""
    validate_shape(bundle)
    records = _index(bundle.get("records"), "records")
    sources = list(_index(bundle.get("sources"), "sources").values())
    return {key: evidence_digest(record, sources, bundle["policy"], bundle["revisions"]) for key, record in records.items()}


def _flag_fingerprint(flag):
    payload = {key: flag.get(key) for key in ("entry_id", "source_id", "source_sha256", "premise")}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, allow_nan=False).encode()).hexdigest()


def _check_flag_provenance(obj, source_map, item, ledger=False):
    issues = []
    scope = "ledger" if ledger else "record"
    fingerprints = []
    for flag in _flags(obj):
        fingerprints.append(flag.get("fingerprint"))
        if any(not _text(flag.get(key)) for key in ("entry_id", "source_id", "premise", "actor_id")):
            issues.append(_issue("CONTRADICTION_PROVENANCE", item, "Flag requires an entry, source, specific premise and actor", scope))
        source = source_map.get(flag.get("source_id"), {})
        if flag.get("source_sha256") != source.get("sha256") or not isinstance(flag.get("source_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", flag["source_sha256"]):
            issues.append(_issue("CONTRADICTION_SOURCE", item, "Flag hash must identify its declared source snapshot", scope))
        if flag.get("fingerprint") != _flag_fingerprint(flag):
            issues.append(_issue("CONTRADICTION_FINGERPRINT", item, "Fingerprint disagrees with the retained artifact/premise", scope))
        if ledger and flag.get("entry_id") != item:
            issues.append(_issue("CONTRADICTION_LINK", item, "Ledger flag names a different ledger entry", scope))
    if any(not _text(fp) for fp in fingerprints) or len(set(fingerprints)) != len(fingerprints):
        issues.append(_issue("CONTRADICTION_FINGERPRINT", item, "Flag fingerprints must be unique and nonempty", scope))
    return issues


def tally(policy, records):
    """Strict-majority technical support; preserve venue decisions as a vector."""
    validate_shape({"policy": policy, "records": records})
    if not isinstance(policy, dict) or type(policy.get("version")) is not int or policy.get("version") != 1 or policy.get("axis") != "technical_support":
        raise ValueError("policy must declare version 1 and axis technical_support")
    panel = _strings(policy.get("reviewers"), "policy.reviewers", nonempty=True)
    threshold = policy.get("threshold")
    if type(threshold) is not int or threshold != len(panel) // 2 + 1:
        raise ValueError("policy.threshold must be a strict majority of the declared panel")
    adjudicators = policy.get("venue_adjudicators", {})
    if not isinstance(adjudicators, dict) or any(not _text(k) or v not in panel for k, v in adjudicators.items()):
        raise ValueError("policy.venue_adjudicators must predeclare a panel reviewer per selected venue")
    output = []
    for record in _index(records, "records").values():
        votes = {}
        venues = {}
        for review in _objects(record.get("reviews", []), "reviews"):
            who = review.get("reviewer_id")
            verdict = review.get("technical_verdict")
            if who not in panel or who in votes or verdict not in {"supported", "rejected", "unresolved"}:
                raise ValueError(f"{record['id']}: duplicate, unknown or malformed reviewer vote")
            votes[who] = verdict
            declared = review.get("venues", {})
            if not isinstance(declared, dict):
                raise ValueError("review.venues must be an object")
            for venue, decision in declared.items():
                if not _text(venue) or not isinstance(decision, dict):
                    raise ValueError("malformed venue decision")
                if decision.get("eligibility") not in {"eligible", "ineligible", "unresolved"} or decision.get("severity") not in SEVERITIES:
                    raise ValueError("venue decision needs eligibility and a recognized severity")
                venues.setdefault(venue, {})[who] = deepcopy(decision)
        counts = Counter(votes.values())
        if set(votes) != set(panel):
            decision = "incomplete"
        elif counts["supported"] >= threshold:
            decision = "supported"
        elif counts["rejected"] >= threshold:
            decision = "rejected"
        elif counts["unresolved"] >= threshold:
            decision = "unresolved"
        else:
            decision = "contested"
        output.append({"id": record["id"], "decision": decision, "counts": dict(counts),
                       "missing_reviewers": sorted(set(panel) - set(votes)), "venues": venues})
    return {"policy": deepcopy(policy), "results": output}


def reconcile_tally(computed, recorded_ids):
    """Compare saved consensus IDs with policy replay, without changing verdicts."""
    recorded = set(_strings(recorded_ids, "recorded_supported_ids"))
    expected = {r["id"] for r in computed["results"] if r["decision"] == "supported"}
    return {"ok": expected == recorded, "computed_count": len(expected), "recorded_count": len(recorded),
            "omitted_ids": sorted(expected - recorded), "extra_ids": sorted(recorded - expected)}


def _merge_namespace(lineage):
    return lineage.get("intermediate_namespace") or ("M" if any(key in lineage for key in ("input_records", "merge_routes", "candidate_remap", "source_artifacts")) else None)


def check_lineage(lineage, record_ids, final=False):
    """Every declared input has one route, with explicit merge/split membership."""
    issues = []
    if not isinstance(lineage, dict):
        return [_issue("LINEAGE_MISSING", "bundle", "Provide input inventory and routes")]
    validate_lineage_shape(lineage)
    namespace = _merge_namespace(lineage)
    if namespace is not None and not is_identifier(namespace):
        raise ValueError("intermediate_namespace must be a canonical identifier")
    if final and namespace:
        if any(key.startswith(namespace + "-") for key in record_ids):
            issues.append(_issue("LINEAGE_FINAL_NAMESPACE", "bundle", "Final candidates cannot retain intermediate merge IDs"))
        if not lineage.get("merge_routes") and not _text(lineage.get("no_shard_inputs")):
            issues.append(_issue("LINEAGE_EMPTY_REMAP", "bundle", "An empty merge map needs an explicit no-shard-input reason"))
    if final and namespace and "candidate_remap" not in lineage:
        issues.append(_issue("LINEAGE_REMAP_REQUIRED", "bundle", "Map intermediate merge IDs explicitly to final candidate IDs"))
    merge_inputs = {r.get("input_id") for r in _objects(lineage.get("routes"), "lineage.routes")}
    if "candidate_remap" in lineage:
        expected = remap_lineage({k: v for k, v in lineage.items() if k not in {"candidate_remap", "merge_routes", "routes"}} | {"routes": lineage.get("merge_routes", [])}, lineage["candidate_remap"])
        merge_inputs = {r["input_id"] for r in expected["routes"]}
        actual_merge_routes = [r for r in _objects(lineage.get("routes"), "lineage.routes") if r.get("input_id") in merge_inputs]
        if sorted(expected["routes"], key=lambda r: r["input_id"]) != sorted(actual_merge_routes, key=lambda r: r["input_id"]):
            issues.append(_issue("LINEAGE_REMAP_MISMATCH", "bundle", "Final routes differ from the explicit intermediate-ID map"))
    if "input_records" in lineage:
        inventory = set(_index(lineage["input_records"], "input_records"))
        if inventory != merge_inputs or not inventory.issubset(set(lineage.get("inputs", []))):
            issues.append(_issue("LINEAGE_INVENTORY", "bundle", "Surviving input inventory disagrees with routes"))
    if "source_artifacts" in lineage:
        artifacts = _objects(lineage["source_artifacts"], "source_artifacts")
        counts = [artifact.get("parsed_count") for artifact in artifacts]
        if any(type(count) is not int or count < 0 for count in counts):
            issues.append(_issue("LINEAGE_ARTIFACT_COUNT", "bundle", "Every retained shard artifact needs a nonnegative integer parsed_count"))
        elif sum(counts) != len(merge_inputs) or (lineage.get("no_shard_inputs") and sum(counts) != 0):
            issues.append(_issue("LINEAGE_ARTIFACT_COUNT", "bundle", "Retained shard counts disagree with merge inputs or empty-shard declaration"))
    inputs = _strings(lineage.get("inputs"), "lineage.inputs")
    routes = _objects(lineage.get("routes"), "lineage.routes")
    routed_candidates = {}
    for route in routes:
        routed_candidates.setdefault(route.get("input_id"), set()).update(_strings(route.get("candidate_ids", []), "route.candidate_ids"))
    seen = set()
    reached = set()
    for route in routes:
        key = route.get("input_id")
        if key not in inputs or key in seen:
            issues.append(_issue("LINEAGE_ROUTE", str(key), "Unknown or repeated input route", "input", routed_candidates.get(key, [])))
        seen.add(key)
        members = _strings(route.get("candidate_ids", []), "route.candidate_ids")
        disposition = route.get("disposition")
        if bool(members) == bool(disposition):
            issues.append(_issue("LINEAGE_DISPOSITION", str(key), "Use candidate membership OR explicit disposition", "input", routed_candidates.get(key, [])))
        if disposition and (not isinstance(disposition, dict) or disposition.get("state") not in {"deferred", "rejected"} or not _text(disposition.get("reason"))):
            issues.append(_issue("LINEAGE_REASON", str(key), "Excluded inputs need a state and reason", "input", routed_candidates.get(key, [])))
        reached.update(members)
    for key in sorted(set(inputs) - seen):
        issues.append(_issue("LINEAGE_LOSS", key, "Input has no disposition", "input"))
    for key in sorted(reached - set(record_ids)):
        for route in routes:
            if key in route.get("candidate_ids", []):
                issues.append(_issue("LINEAGE_DANGLING", str(route.get("input_id")), f"Route names missing candidate {key}", "input", route["candidate_ids"]))
    for key in sorted(set(record_ids) - reached):
        issues.append(_issue("LINEAGE_ORPHAN", key, "Candidate has no input provenance"))
    return issues


def remap_lineage(lineage, mapping):
    """Explicit intermediate-to-final ID mapping; preserve raw provenance."""
    validate_lineage_shape(lineage)
    if not isinstance(mapping, dict):
        raise ValueError("candidate remap must be an object")
    routes = _objects(lineage.get("routes"), "lineage.routes")
    intermediate = {key for route in routes for key in _strings(route.get("candidate_ids", []), "candidate_ids")}
    if set(mapping) != intermediate:
        raise ValueError("Remap must account for every intermediate merge ID exactly once")
    for value in mapping.values():
        _strings(value, "remap final IDs", nonempty=True)
        if set(value).intersection(mapping):
            raise ValueError("Final IDs must be distinct from every intermediate mapping key")
        namespace = _merge_namespace(lineage)
        if namespace and any(key.startswith(namespace + "-") for key in value):
            raise ValueError("Final IDs cannot remain in the intermediate namespace")
    result = deepcopy(lineage)
    result["merge_routes"] = deepcopy(routes)
    result["candidate_remap"] = deepcopy(mapping)
    result["routes"] = []
    for route in routes:
        updated = deepcopy(route)
        if route.get("candidate_ids"):
            updated["candidate_ids"] = sorted({key for raw in route["candidate_ids"] for key in mapping[raw]})
        result["routes"].append(updated)
    return result


def check_sources(sources, revisions, evidence_root):
    issues = []
    verified = set()
    root = Path(evidence_root).resolve()
    for source in _index(sources, "sources").values():
        key = source["id"]
        if source.get("kind") not in {"source", "spec", "execution", "external"}:
            issues.append(_issue("SOURCE_KIND", key, "Declare source, spec, execution or external evidence", "source"))
            continue
        if source.get("kind") == "external":
            url = urlparse(source.get("url", ""))
            if url.scheme != "https" or not url.netloc:
                issues.append(_issue("EXTERNAL_PROVENANCE", key, "External snapshot needs its primary-source HTTPS URL", "source"))
                continue
        revision_key = source.get("revision_key")
        if revision_key not in revisions or source.get("revision") != revisions.get(revision_key):
            issues.append(_issue("SOURCE_STALE", key, "Evidence revision does not match the declared snapshot", "source"))
            continue
        try:
            relative = source.get("path")
            if not _text(relative) or Path(relative).is_absolute():
                raise ValueError("Evidence path must be relative")
            path = (root / relative).resolve()
            if not path.is_relative_to(root):
                raise ValueError("Evidence path leaves the evidence root")
            data = path.read_bytes()
            expected = source.get("sha256")
            if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected) or hashlib.sha256(data).hexdigest() != expected:
                raise ValueError("Evidence hash does not match")
            start, end = source.get("line_start"), source.get("line_end")
            lines = data.decode("utf-8").split("\n")
            if lines[-1] == "":
                lines.pop()
            if type(start) is not int or type(end) is not int or not (1 <= start <= end <= len(lines)):
                raise ValueError("Evidence line range does not resolve")
        except (OSError, ValueError, UnicodeError) as exc:
            issues.append(_issue("SOURCE_UNRESOLVED", key, str(exc), "source"))
        else:
            verified.add(key)
    return issues, verified


def summarize_ledger(entries, revisions, verified_sources):
    """Visibility only: referenced closure is not a correctness verdict."""
    summary = Counter()
    output = []
    for entry in _index(entries, "ledger").values():
        state = entry.get("state")
        if state not in {"open", "deferred", "closed", "contested"}:
            raise ValueError("ledger.state must be open, deferred, closed or contested")
        revision_key = entry.get("revision_key")
        basis = _strings(entry.get("basis_ids", []), "ledger.basis_ids")
        if _open_flags(entry):
            status = "contested"
        elif revision_key not in revisions or entry.get("revision") != revisions.get(revision_key):
            status = "stale"
        elif state == "closed" and (not basis or not set(basis).issubset(verified_sources)):
            status = "unsupported_closure"
        elif state == "deferred" and not _text(entry.get("reason")):
            status = "unsupported_deferral"
        else:
            status = "closed_with_reference" if state == "closed" else state
        summary[status] += 1
        output.append({"id": entry["id"], "status": status, "basis_ids": basis,
                       "limitations": entry.get("limitations", ""), "reason": entry.get("reason", "")})
    return {"counts": dict(summary), "entries": output,
            "limitation": "References and dispositions do not establish correctness or complete coverage."}


def check_bundle(bundle, evidence_root, publication=False):
    """Validate snapshots, approvals, dispositions and (optionally) publication."""
    validate_shape(bundle)
    if not isinstance(bundle, dict) or type(bundle.get("schema_version")) is not int or bundle.get("schema_version") != 1:
        raise ValueError("bundle.schema_version must be 1")
    revisions = bundle.get("revisions")
    if not isinstance(revisions, dict) or not _text(revisions.get("target")) or any(not _text(k) or not _text(v) for k, v in revisions.items()):
        raise ValueError("revisions must contain nonempty immutable snapshot identities including target")
    records = _index(bundle.get("records"), "records")
    sources = _objects(bundle.get("sources"), "sources")
    issues, verified = check_sources(sources, revisions, evidence_root)
    source_map = _index(sources, "sources")
    issues.extend(check_lineage(bundle.get("lineage"), records, final=True))
    computed = tally(bundle.get("policy"), list(records.values()))
    decisions = {r["id"]: r for r in computed["results"]}
    blocked = {}

    def refs(value, item, scope="record"):
        try:
            ids = _strings(value, "evidence_ids", nonempty=True)
        except ValueError as exc:
            issues.append(_issue("EVIDENCE_REQUIRED", item, str(exc), scope))
            return []
        if not set(ids).issubset(verified):
            issues.append(_issue("EVIDENCE_UNRESOLVED", item, "Referenced evidence is missing, stale or does not resolve", scope))
        return ids

    for key, record in records.items():
        start = len(issues)
        issues.extend(_check_flag_provenance(record, source_map, key))
        if record.get("state") not in STATES:
            issues.append(_issue("STATE_INVALID", key, "Unknown lifecycle state"))
        if record.get("target_revision") != revisions["target"]:
            issues.append(_issue("RECORD_STALE", key, "Candidate targets a different revision"))
        if not _text(record.get("author_id")) or record.get("kind") not in {"finding", "advisory"}:
            issues.append(_issue("IDENTITY_REQUIRED", key, "Author and claim kind are required"))
        dependencies = _strings(record.get("dependency_keys", []), "dependency_keys")
        if any(k not in revisions for k in dependencies):
            issues.append(_issue("DEPENDENCY_UNPINNED", key, "A material dependency lacks a snapshot identity"))
        components = record.get("components", {})
        if not isinstance(components, dict):
            raise ValueError("components must be an object")
        unresolved = False
        used_sources = set()
        context_ids = _strings(record.get("context_ids", []), "context_ids")
        if context_ids:
            used_sources.update(refs(context_ids, key))
        for flag in _flags(record):
            used_sources.update(refs([flag.get("source_id")], key))
            if flag.get("status", "open") not in {"open", "resolved"}:
                issues.append(_issue("CONTRADICTION_STATUS", key, "Unknown contradiction status"))
            if flag.get("status") == "resolved":
                resolution = flag.get("resolution")
                if not isinstance(resolution, dict) or not _text(resolution.get("actor_id")) or not _text(resolution.get("reason")):
                    issues.append(_issue("CONTRADICTION_RESOLUTION", key, "Resolution requires attribution and a concrete reason"))
                else:
                    used_sources.update(refs(resolution.get("basis_ids"), key))
        for name in sorted(COMPONENTS):
            component = components.get(name)
            if not isinstance(component, dict) or not _text(component.get("statement")):
                issues.append(_issue("COMPONENT_REQUIRED", key, f"Missing {name} claim"))
                continue
            if component.get("mode") not in MODES or component.get("status") not in {"supported", "unresolved"}:
                issues.append(_issue("EVIDENCE_MODE", key, f"Invalid {name} evidence mode/status"))
            if component.get("status") == "unresolved" or component.get("mode") == "unresolved":
                unresolved = True
                if not _text(component.get("missing_evidence")):
                    issues.append(_issue("UNRESOLVED_REASON", key, f"Name missing {name} evidence"))
            else:
                evidence_ids = refs(component.get("evidence_ids"), key)
                used_sources.update(evidence_ids)
                required_kind = {"executed": "execution", "external": "external"}.get(component.get("mode"))
                if required_kind and not any(source_map.get(i, {}).get("kind") == required_kind for i in evidence_ids):
                    issues.append(_issue("EVIDENCE_MODE_SOURCE", key, f"{name} needs an attributable {required_kind} artifact"))
        assumptions = record.get("assumptions", {})
        if not isinstance(assumptions, dict):
            raise ValueError("assumptions must be an object")
        for name in ("actors", "impact"):
            assumption = assumptions.get(name)
            if not isinstance(assumption, dict) or not _text(assumption.get("statement")):
                issues.append(_issue("ASSUMPTION_REQUIRED", key, f"Missing {name} assumptions"))
                continue
            used_sources.update(refs(assumption.get("evidence_ids"), key))
            contrary = _strings(assumption.get("contradicting_ids", []), "contradicting_ids")
            if not set(contrary).issubset(verified):
                issues.append(_issue("CONTRADICTION_UNRESOLVED", key, "Contradicting source cannot be resolved"))
            used_sources.update(contrary)
            if contrary and not _text(assumption.get("contradiction_resolution")):
                issues.append(_issue("CONTRADICTION_REASON", key, "Explain how contrary evidence affects the claim"))
        relied_keys = {source_map[i]["revision_key"] for i in used_sources if i in source_map}
        if not (relied_keys - {"target"}).issubset(dependencies):
            issues.append(_issue("DEPENDENCY_UNDECLARED", key, "Cited material dependency is not declared"))
        digest = evidence_digest(record, sources, bundle["policy"], revisions)
        for review in _objects(record.get("reviews", []), "reviews"):
            if review.get("reviewer_id") == record.get("author_id") or review.get("kind") not in {"human", "model"}:
                issues.append(_issue("REVIEW_PROVENANCE", key, "Reviewer must differ from author; declare human or model"))
            if review.get("evidence_digest") != digest:
                issues.append(_issue("REVIEW_STALE", key, "Approval is not bound to this claim/source snapshot"))
            if set(_strings(review.get("component_ids"), "review.component_ids")) != COMPONENTS:
                issues.append(_issue("REVIEW_INCOMPLETE", key, "Review must explicitly cover mechanism, contract and impact"))
            inputs = set(refs(review.get("input_ids"), key))
            if not used_sources.issubset(inputs):
                issues.append(_issue("REVIEW_INPUTS", key, "Review provenance omits relied-on evidence"))
            for venue_decision in review.get("venues", {}).values():
                basis = set(refs(venue_decision.get("basis_ids"), key))
                if not basis.issubset(inputs):
                    issues.append(_issue("REVIEW_INPUTS", key, "Venue policy evidence was not included in reviewer inputs"))
                if not basis.issubset(context_ids):
                    issues.append(_issue("VENUE_CONTEXT", key, "Venue rule sources must be declared in digest-bound context_ids"))
        reasons = [issue["code"] for issue in issues[start:]]
        if unresolved:
            reasons.append("UNRESOLVED_COMPONENT")
        if record.get("state") != "supported":
            reasons.append("STATE_NOT_SUPPORTED")
        if decisions[key]["decision"] != "supported":
            reasons.append("POLICY_NOT_SUPPORTED")
        if _open_flags(record):
            reasons.append("OPEN_CONTRADICTION")
        blocked[key] = sorted(set(reasons))

    ledger = summarize_ledger(bundle.get("ledger", []), revisions, verified)
    ledger_status = {entry["id"]: entry["status"] for entry in ledger["entries"]}
    for entry in _objects(bundle.get("ledger", []), "ledger"):
        issues.extend(_check_flag_provenance(entry, source_map, entry["id"], ledger=True))
        affected = _strings(entry.get("candidate_ids", []), "ledger.candidate_ids")
        if not set(affected).issubset(records):
            issues.append(_issue("LEDGER_DANGLING", entry["id"], "Ledger names a missing candidate", "ledger"))
        fingerprints = [f.get("fingerprint") for f in _flags(entry)]
        for event in _objects(entry.get("history", []), "history"):
            if event.get("fingerprint") and event["fingerprint"] not in fingerprints:
                issues.append(_issue("CONTRADICTION_HISTORY", entry["id"], "Ledger history references a deleted flag", "ledger"))
        for flag in _flags(entry):
            if flag.get("status", "open") not in {"open", "resolved"}:
                issues.append(_issue("CONTRADICTION_STATUS", entry["id"], "Unknown ledger flag status", "ledger"))
            refs([flag.get("source_id")], entry["id"], "ledger")
            original_affected = _strings(flag.get("affected_candidate_ids"), "flag.affected_candidate_ids")
            for missing in set(original_affected) - set(affected):
                issues.append(_issue("CONTRADICTION_AFFECTED", missing, f"Previously affected candidate was silently unlinked from {entry['id']}"))
            if flag.get("status") == "resolved":
                resolution = flag.get("resolution")
                if not isinstance(resolution, dict) or not _text(resolution.get("actor_id")) or not _text(resolution.get("reason")):
                    issues.append(_issue("CONTRADICTION_RESOLUTION", entry["id"], "Ledger resolution requires attribution and a concrete reason", "ledger"))
                else:
                    refs(resolution.get("basis_ids"), entry["id"], "ledger")
            for key in set(affected).intersection(records):
                copies = [f for f in _flags(records[key]) if f.get("fingerprint") == flag.get("fingerprint")]
                if len(copies) != 1 or copies[0] != flag:
                    issues.append(_issue("CONTRADICTION_COPIES", key, "Ledger and candidate flag copies disagree"))
        if ledger_status[entry["id"]] in {"contested", "stale", "unsupported_closure"}:
            for key in set(affected).intersection(records):
                blocked[key].append("LEDGER_" + ledger_status[entry["id"]].upper())
    ledger_map = _index(bundle.get("ledger", []), "ledger")
    for key, record in records.items():
        flags = _flags(record)
        fingerprints = [f.get("fingerprint") for f in flags]
        if any(not _text(fp) for fp in fingerprints) or len(set(fingerprints)) != len(fingerprints):
            issues.append(_issue("CONTRADICTION_FINGERPRINT", key, "Flag fingerprints must be unique and nonempty"))
        for history in _objects(record.get("history", []), "history"):
            if history.get("fingerprint") and history["fingerprint"] not in fingerprints:
                issues.append(_issue("CONTRADICTION_HISTORY", key, "History references a deleted contradiction flag"))
        for flag in flags:
            entry = ledger_map.get(flag.get("entry_id"), {})
            if key not in flag.get("affected_candidate_ids", []) or key not in entry.get("candidate_ids", []) or not any(f == flag for f in _flags(entry)):
                issues.append(_issue("CONTRADICTION_LINK", key, "Candidate flag has no matching linked ledger copy"))
    reconciliation = None
    if "recorded_supported_ids" in bundle:
        reconciliation = reconcile_tally(computed, bundle["recorded_supported_ids"])
        if not reconciliation["ok"]:
            issues.append(_issue("TALLY_MISMATCH", "bundle", "Saved supported IDs differ from declared policy replay"))
    if publication:
        dispositions = _index(bundle.get("report_dispositions"), "report_dispositions")
        if set(dispositions) != set(records):
            issues.append(_issue("REPORT_CONSERVATION", "bundle", "Every candidate needs exactly one final report disposition"))
        for key, disposition in dispositions.items():
            state = disposition.get("state")
            if key not in records:
                continue
            if state != "published" and any(field in disposition for field in ("severity", "venue", "decision_reviewer")):
                issues.append(_issue("UNPUBLISHED_RATING", key, "Unpublished dispositions cannot carry a publication rating"))
            if state not in {"published", "deferred", "rejected", "contested"}:
                issues.append(_issue("REPORT_STATE", key, "Invalid report disposition"))
            elif state != "published" and not _text(disposition.get("reason")):
                issues.append(_issue("REPORT_REASON", key, "Unpublished items need a visible reason"))
            elif state == "rejected" and (records[key].get("state") != "rejected" or decisions[key]["decision"] != "rejected"):
                issues.append(_issue("REPORT_REJECTION", key, "Final candidate rejection requires the declared technical-support policy"))
            elif state == "contested" and not (records[key].get("state") == "contested" or len(decisions[key]["counts"]) > 1 or _open_flags(records[key]) or "LEDGER_CONTESTED" in blocked[key]):
                issues.append(_issue("REPORT_CONTESTED", key, "Contested disposition needs a recorded dispute"))
            elif state == "published":
                if blocked[key]:
                    issues.append(_issue("PUBLICATION_BLOCKED", key, ", ".join(blocked[key])))
                if disposition.get("kind") != records[key].get("kind"):
                    issues.append(_issue("REPORT_KIND", key, "Report cannot convert uncertainty into an advisory"))
                venue = disposition.get("venue")
                if venue:
                    review = disposition.get("decision_reviewer")
                    decision = decisions[key]["venues"].get(venue, {}).get(review)
                    support = next((r for r in records[key]["reviews"] if r["reviewer_id"] == review), {})
                    authority = bundle["policy"].get("venue_adjudicators", {}).get(venue)
                    if not authority or review != authority or not decision or support.get("technical_verdict") != "supported" or decision["eligibility"] != "eligible" or disposition.get("severity") != decision["severity"]:
                        issues.append(_issue("VENUE_DECISION", key, "Use an attributable eligible venue decision without changing severity"))
                elif "severity" in disposition:
                    issues.append(_issue("UNSCOPED_SEVERITY", key, "No universal cross-venue severity is manufactured"))
    for issue in issues:
        scope, item = issue["scope"], issue["id"]
        if scope == "record":
            affected = [item]
        elif scope == "source":
            affected = [key for key, record in records.items() if item in _reference_ids(record)]
        elif scope == "ledger":
            affected = ledger_map.get(item, {}).get("candidate_ids", [])
        elif scope == "input":
            affected = issue.get("candidate_ids", [])
        else:
            affected = list(records)
        for key in set(affected).intersection(blocked):
            blocked[key].append(issue["code"])
    blocked = {key: sorted(set(value)) for key, value in blocked.items()}
    return {"ok": not issues, "issues": issues, "tally": computed,
            "publishable_ids": [] if issues else sorted(k for k, reasons in blocked.items() if not reasons),
            "blocked": blocked, "ledger": ledger, "reconciliation": reconciliation,
            "limitation": "Structural checks cannot establish semantic truth or authenticate reviewer identity."}


def flag_contradiction(bundle, entry_id, source_id, premise, actor):
    """Return a copy with an attributable contradiction; never re-run reviewers."""
    validate_shape(bundle)
    if not _text(premise) or not is_identifier(actor):
        raise ValueError("A specific premise correction and actor identity are required")
    sources = _index(bundle.get("sources"), "sources")
    if source_id not in sources:
        raise ValueError("Contradiction must reference a declared evidence artifact")
    result = deepcopy(bundle)
    entries = _index(result.get("ledger", []), "ledger")
    records = _index(result.get("records"), "records")
    if entry_id not in entries:
        raise ValueError("Unknown ledger entry")
    entry = entries[entry_id]
    affected = _strings(entry.get("candidate_ids", []), "ledger.candidate_ids")
    if not set(affected).issubset(records):
        raise ValueError("Ledger references a missing candidate")
    payload = {"entry_id": entry_id, "source_id": source_id, "source_sha256": sources[source_id].get("sha256"),
               "premise": premise, "actor_id": actor}
    fingerprint = _flag_fingerprint(payload)
    flag = {**payload, "fingerprint": fingerprint, "status": "open", "affected_candidate_ids": sorted(affected)}
    prior = next((f for f in _flags(entry) if f.get("fingerprint") == fingerprint), None)
    if prior:
        original = set(_strings(prior.get("affected_candidate_ids", []), "affected_candidate_ids"))
        if not original.issubset(affected):
            raise ValueError("Restore affected candidate links before modifying the flag")
        missing = [records[k] for k in affected if not any(f.get("fingerprint") == fingerprint for f in _flags(records[k]))]
        if prior.get("status") == "resolved" and not missing:
            raise ValueError("Flag already resolved; provide new artifact/premise rather than silently re-raising it")
        if not missing and original == set(affected):
            return result
        inherited = deepcopy(prior)
        inherited["affected_candidate_ids"] = sorted(affected)
        for obj, is_record in [(entry, False), *((records[k], True) for k in affected)]:
            flags = obj.setdefault("contradictions", [])
            found = next((i for i, f in enumerate(flags) if f.get("fingerprint") == fingerprint), None)
            if found is None:
                flags.append(deepcopy(inherited))
            else:
                flags[found] = deepcopy(inherited)
            old = obj.get("state")
            if is_record:
                obj["state"] = "contested"
            obj.setdefault("history", []).append({"from": old, "to": obj["state"], "actor_id": actor, "reason": "Affected membership expanded; fresh candidate reviews required", "fingerprint": fingerprint})
        return result
    for obj, is_record in [(entry, False), *((records[k], True) for k in affected)]:
        existing = _objects(obj.setdefault("contradictions", []), "contradictions")
        if any(f.get("fingerprint") == fingerprint for f in existing):
            continue
        old = obj.get("state")
        if not is_record and not _open_flags(obj):
            obj["pre_contradiction_state"] = old
        existing.append(deepcopy(flag))
        obj.setdefault("history", []).append({"from": old, "to": "contested", "reason": premise, "actor_id": actor, "fingerprint": fingerprint})
        obj["state"] = "contested"
    return result


def resolve_contradiction(bundle, fingerprint, actor, reason, basis_ids):
    """Retain a resolved flag; new snapshot-bound approvals are still required."""
    validate_shape(bundle)
    if not is_identifier(actor) or not _text(reason):
        raise ValueError("Resolution requires an actor and concrete reason")
    basis = _strings(basis_ids, "resolution.basis_ids", nonempty=True)
    if not set(basis).issubset(_index(bundle.get("sources"), "sources")):
        raise ValueError("Resolution basis must reference declared artifacts")
    result = deepcopy(bundle)
    matching = [flag for obj in [*_objects(result.get("records"), "records"), *_objects(result.get("ledger", []), "ledger")] for flag in _flags(obj) if flag.get("fingerprint") == fingerprint]
    if not matching:
        raise ValueError("Unknown contradiction fingerprint")
    if not any(flag.get("status", "open") != "resolved" for flag in matching):
        raise ValueError("This flag is already resolved; use new evidence for another correction")
    for obj, is_record in [*((r, True) for r in _objects(result.get("records"), "records")), *((e, False) for e in _objects(result.get("ledger", []), "ledger"))]:
        for flag in _flags(obj):
            if flag.get("fingerprint") != fingerprint:
                continue
            previous_resolution = deepcopy(flag.get("resolution"))
            flag["status"] = "resolved"
            flag["resolution"] = {"actor_id": actor, "reason": reason, "basis_ids": basis}
            old = obj.get("state")
            if is_record:
                obj["state"] = "contested"
            else:
                original = obj.get("pre_contradiction_state", old)
                obj["state"] = "contested" if _open_flags(obj) else original
                obj["basis_ids"] = sorted(set(_strings(obj.get("basis_ids", []), "basis_ids")) | set(basis))
            event = {"from": old, "to": obj["state"], "reason": reason, "actor_id": actor, "fingerprint": fingerprint}
            if previous_resolution:
                event["previous_resolution"] = previous_resolution
            obj.setdefault("history", []).append(event)
    return result


def transition(bundle, record_id, state, reason, evidence_root, actor):
    """Apply a guarded state transition to a copy and keep a visible reason."""
    validate_shape(bundle)
    if state not in STATES or not _text(reason) or not is_identifier(actor):
        raise ValueError("Transition needs a recognized state, actor and concrete reason")
    result = deepcopy(bundle)
    records = _index(result.get("records"), "records")
    if record_id not in records:
        raise ValueError("Unknown candidate")
    record = records[record_id]
    old = record.get("state")
    allowed = {"candidate": {"unresolved", "supported", "rejected", "contested"},
               "unresolved": {"supported", "rejected", "contested"},
               "supported": {"unresolved", "contested"},
               "rejected": {"contested"}, "contested": {"unresolved", "supported", "rejected"}}
    if state not in allowed.get(old, set()):
        raise ValueError(f"Invalid lifecycle transition {old} -> {state}")
    if state == "supported":
        checked = check_bundle(result, evidence_root)
        relevant = {("record", record_id), ("bundle", "bundle")} | {("source", key) for key in _reference_ids(record)}
        relevant.update(("ledger", e["id"]) for e in _objects(result.get("ledger", []), "ledger") if record_id in e.get("candidate_ids", []))
        if any((i["scope"], i["id"]) in relevant for i in checked["issues"]) or set(checked["blocked"][record_id]) - {"STATE_NOT_SUPPORTED"}:
            raise ValueError("Unresolved evidence, review or contradiction prevents support")
    if state == "rejected":
        decision = tally(result.get("policy"), [record])["results"][0]
        if decision["decision"] != "rejected":
            raise ValueError("Final rejection requires the declared review policy")
    record.setdefault("history", []).append({"from": old, "to": state, "reason": reason, "actor_id": actor})
    record["state"] = state
    return result
