"""Machine-readable scope parsing for 00-scope.md.

`recon-specialist` emits `audit-output/00-scope.md` with a fenced JSON block
under `## Machine-Readable Scope`. `scripts/grep_prune.py` and
`scripts/partition_shards.py` consume it via this module to restrict their
target set to in-scope files — the block is a contract, not documentation.
"""

import fnmatch
import json
import re


_JSON_FENCE_RE = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL)


def load_scope_block(scope_path):
    """Extract the machine-readable JSON block from a 00-scope.md file.

    Prefers the fenced JSON block that follows the `## Machine-Readable
    Scope` heading — a fence there that fails to parse raises (the block is
    a contract). Falls back to the first parseable fenced JSON object
    anywhere in the file. Returns None when no block is found.
    """
    with open(scope_path, "r", encoding="utf-8") as f:
        text = f.read()

    section = re.split(r"^##\s+Machine-Readable Scope\s*$", text, flags=re.MULTILINE)
    if len(section) >= 2:
        for match in _JSON_FENCE_RE.finditer(section[1]):
            return _parse_scope_json(match.group(1), scope_path)

    for match in _JSON_FENCE_RE.finditer(text):
        try:
            return _parse_scope_json(match.group(1), scope_path)
        except ValueError:
            continue
    return None


def _parse_scope_json(raw, scope_path):
    try:
        scope = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Scope block in {scope_path} is not valid JSON: {exc}") from exc
    if not isinstance(scope, dict):
        raise ValueError(f"Scope block in {scope_path} is not a JSON object")
    return scope


def _norm(path):
    return str(path).replace("\\", "/").rstrip("/")


def build_matcher(scope):
    """Build a predicate relpath -> bool from a scope block.

    A relative path is in scope when it matches any entry of `in_scope`,
    `diff_set`, or `blast_set`. Entries may be exact file paths, directory
    paths, or shell globs (fnmatch). When the scope declares none of the
    three lists non-empty, the matcher fails open (everything matches) so a
    skeleton scope block never silently empties a scan.
    """
    if not isinstance(scope, dict):
        raise ValueError("scope must be a dict")

    rules = []
    for key in ("in_scope", "diff_set", "blast_set"):
        for entry in scope.get(key) or []:
            if isinstance(entry, dict):  # out_of_scope-style entries
                continue
            rules.append(_norm(entry))
    rules = [r for r in rules if r]

    def matches(relpath):
        if not rules:
            return True
        rel = _norm(relpath)
        for rule in rules:
            if rel == rule or rel.startswith(rule + "/"):
                return True
            if any(ch in rule for ch in "*?[") and fnmatch.fnmatch(rel, rule):
                return True
        return False

    return matches


def filter_file_scope(file_path, target_path, matches):
    """Return True when `file_path` (absolute or target-relative) is in scope.

    Paths are normalized relative to `target_path` before matching; paths
    outside `target_path` never match (unless the matcher fails open with
    empty rules, in which case everything does).
    """
    rel = _norm(file_path)
    base = _norm(target_path)
    if rel.startswith(base + "/"):
        rel = rel[len(base) + 1:]
    elif rel.startswith("/"):
        # Absolute path outside the target root — strip leading components
        # heuristically via the tail of base.
        base_parts = base.split("/")
        file_parts = rel.split("/")
        if file_parts[: len(base_parts)] == base_parts:
            rel = "/".join(file_parts[len(base_parts):])
    return matches(rel)
