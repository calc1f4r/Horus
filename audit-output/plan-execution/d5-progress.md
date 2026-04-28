# D5 Progress — Self-Improving Hunt Cards

Status: partial.

## Completed

- Added `--gap-analysis <audit-output-dir>` mode specification to
  `.claude/agents/db-quality-monitor.md`.
- Created `DB/_drafts/README.md`.
- Created `DB/_telemetry/README.md`.
- Added draft/telemetry conventions to `.claude/rules/db-entries.md`.
- Updated `scripts/generate_manifests.py` to ignore `_drafts`, `_telemetry`,
  `graphify-out`, and generated manifest dirs.
- Updated `scripts/db_quality_check.py` to ignore graph/draft/telemetry
  artifacts as DB entries.

## Remaining

- Run gap analysis against a real past audit with `CONFIRMED-REPORT.md`.
- Produce and inspect a `db-gap-analysis.md` report.
- Create at least one sample telemetry sidecar or draft from a confirmed finding.
- Validate draft quality against `TEMPLATE.md`.

