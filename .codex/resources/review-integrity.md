# Review decision integrity (schema version 1)

Use `scripts/review_integrity.py` for offline decision, lineage and publication
checks. This contract applies to post-review records, not discovery planning.
It does not execute reviewed code, follow URLs, call models or certify truth.

## Commands and failure behavior

```bash
python3 scripts/review_integrity.py check audit-output/review-records.json --evidence-root <snapshot-root>
python3 scripts/review_integrity.py tally audit-output/review-records.json
python3 scripts/review_integrity.py ledger audit-output/review-records.json --evidence-root <snapshot-root>
python3 scripts/review_integrity.py gate audit-output/review-records.json --evidence-root <snapshot-root>
```

Commands print JSON. Exit 0 means the requested structural check passed; exit 1
means repair is required. `check` may pass with unresolved candidates: consult
both `ok` and `blocked`; structural errors empty `publishable_ids`. `gate` also verifies final report dispositions
and refuses publishing a blocked candidate. Keep `review-check.json`,
`review-tally.json`, `review-ledger.json` and `review-gate.json` beside the report.
Capture output even on failure; never fabricate a passing result.

`tally` is policy replay only, without source validation. It is not a publication
gate or an adjudication. If `recorded_supported_ids` is supplied, an omitted or
extra ID produces `TALLY_MISMATCH`/a failing reconciliation, not a changed vote.
Missing/duplicate/unknown panel voters cannot silently shrink the denominator.

## Bundle structure

### Strict fields, identifiers and current digest behavior

Duplicate JSON keys, nonfinite numbers, excessive nesting and boolean/float
version numbers fail as malformed input. Structural object fields are closed;
misspelled fields cannot silently drop contrary evidence. Optional display data
belongs in an explicit `metadata` object, with no voting/eligibility semantics.
Metadata can still affect digests/copy equality; editing it may require fresh
reviews. IDs use
ASCII letters/digits plus `.`, `_`, `:`, `/` and `-`, beginning with a letter or
digit. Whitespace and lookalike Unicode are rejected; `bundle` is reserved.
Diagnostic identity is `(scope, id)`; source/candidate name collisions cannot
exchange errors. Input-route errors name the affected candidates and prevent
their support transitions.

Line ranges count LF-delimited physical lines, including CRLF. Unicode/control
separators do not create extra citation lines. Digest version 2 binds the values
of all declared material dependency pins, even without cited source rows, plus
the target pin. This changes old digests: obtain fresh substantive reviews;
do not stamp new hashes onto saved approvals. Unrelated pins remain independent.

The shard merger accepts anchored `### F-ID: Title` headings and rejects
recognizable unsupported finding headings, pre-header finding fields, repeated
IDs/fields and unclosed fences. Inline/fenced examples are not headings. Source
artifacts retain parsed counts and preamble hash/byte length. This guards
recognizable omissions, not arbitrary unlabelled prose or incomplete authorship.
Final candidates cannot use the intermediate namespace (default `M` for merger
inventory); surviving remap/artifact markers also imply that namespace.
Identity mappings fail independently of the namespace marker. Retained shard
`parsed_count` values must be nonnegative integers and sum to the merge-input
count; empty-shard declarations require that sum to be zero. Counts and hashes
are declared provenance, not independently authenticated parser executions.
Empty shard remaps require an explicit `no_shard_inputs` reason.

Incomplete panels have tally decision `incomplete`, not an invented dispute.
Use `deferred` for unreviewed or unanimously unresolved records. `contested`
requires an explicit recorded contest, differing votes or linked dispute.
Unpublished dispositions cannot contain `severity`, `venue` or
`decision_reviewer`; keep tentative/dissenting ratings in attributed reviews.

Flag fingerprints are recomputed and their stored source hashes must match the
declared archived artifact. Preserve the old artifact under its stable source
ID; do not retarget a settled flag to replacement evidence. Record/ledger roles
are explicit, independent of whether a damaged record retains `components`.

### Fields

The input object contains:

| Field | Contract |
|---|---|
| `schema_version` | `1` |
| `revisions` | Map of immutable snapshot identities; `target` is required; material dependencies get their own keys |
| `sources` | Array of source snapshots described below; unique IDs |
| `policy` | `{version: 1, axis: "technical_support", reviewers: [unique IDs], threshold: strict-majority}`; predeclare `venue_adjudicators` for publication venues |
| `records` | Candidate records; unique, stable IDs |
| `lineage` | Declared input inventory and one explicit route per input |
| `ledger` | Existing review-item dispositions, including pre-candidate items |
| `recorded_supported_ids` | Optional saved technical-support result for exact reconciliation |
| `report_dispositions` | Required by `gate`; exactly one disposition for every candidate |

Use the pinned target/dependency snapshots in one evidence root. A source has
`id`, `kind` (`source`, `spec`, `execution`, `external`), relative `path`,
`revision_key`, `revision`, lowercase `sha256`, and 1-based inclusive
`line_start`/`line_end`. Paths must resolve inside the evidence root, including
symlinks. Hashes and ranges must resolve; changed snapshots are stale. External
sources also record their primary-source HTTPS `url` and an archived local text
snapshot. No URL is fetched by the checker. The reviewer must verify that the
source is primary and applicable; a URL or digest is not evidence of that alone.

Revision identities are caller-supplied provenance, not automatically authenticated
Git history. Use full commits, locked dependency versions or immutable snapshot
IDs. Never use a moving branch or floating version as a pin. Conservation is
relative to the declared inventory; check that it includes every source artifact.

## Candidate and review records

Each record has `id`, `author_id`, `target_revision`, `kind` (`finding` or
`advisory`), `state`, `dependency_keys`, `components`, `assumptions`, and `reviews`.
Do not use a confidence label as a lifecycle state.

- States: `candidate`, `unresolved`, `supported`, `rejected`, `contested`.
- Components: `mechanism`, `contract`, `impact`. Each has a `statement`, `status`
  (`supported` or `unresolved`), `mode` (`static`, `executed`, `external`,
  `unresolved`) and `evidence_ids`. Unresolved components name `missing_evidence`.
- Evidence is per component. An execution log may support a mechanism while the
  contract/impact interpretation remains unresolved. Static derivations are
  allowed; tests are not mandatory. Executed/external modes require a source
  of the corresponding kind. A declared execution artifact is not an authenticated
  proof that an agent ran a tool; reviewers must check the log's provenance.
- `assumptions.actors` and `assumptions.impact` each have a `statement`,
  `evidence_ids` and `contradicting_ids` (empty when none were found). Contrary
  evidence requires `contradiction_resolution`; record uncertainty honestly.
  Cite absence of specification as a limitation, not an automatic rejection.
- Declare material `dependency_keys`; unknown or cited-but-undeclared dependency
  revisions block publication. Unrelated dependencies need not be inventoried.

Each review has `reviewer_id`, `kind` (`human` or `model`), `technical_verdict`
(`supported`, `rejected`, `unresolved`), `component_ids` covering all three
components, `input_ids`, `evidence_digest` and optional `venues`.
The reviewer ID must differ from the author. Inputs must include supporting and
contradicting material. Record which inputs were seen; shared inputs imply
correlation and a different ID does not prove independent reasoning.

Compute the claim/source digest with:

```bash
python3 scripts/review_integrity.py digest audit-output/review-records.json
```

The substantive reviewer records this digest with its decision. Never stamp
approvals on behalf of absent reviewers. Digests bind declared decisions to the
claim, declared decision policy and referenced snapshots; unrelated sources do
not invalidate approvals. Declare broader relied-on context and all venue-rule
basis IDs in `context_ids`, with material revision keys in `dependency_keys`.
Policy/adjudicator or referenced rule-snapshot changes require fresh approvals.
These are not signatures or
authenticated identities; editable verdicts and venue decisions are not bound
or authenticated by this digest.
Claim/source/contradiction changes require new reviews. Keep externally authentic
review logs where available. A fully populated form does not prove semantic truth.

`venues` is a map from venue name to `{eligibility, severity, basis_ids}`.
Eligibility is `eligible`, `ineligible` or `unresolved`; severity is
`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO` or `QA`. Preserve each reviewer’s
decision. Technical-support votes do not vote on contest eligibility or produce a
universal cross-venue severity. Ineligible technical findings remain traceable.

## Lineage and report dispositions

`lineage.inputs` lists unique raw input IDs. Each `lineage.routes` object has
`input_id` and either `candidate_ids` or a `disposition` with state
`deferred`/`rejected` and a concrete `reason`. Merges retain all input memberships;
splits list each resulting candidate on one route. Missing, repeated, unknown or
orphaned IDs fail reconciliation.

The shard merger emits `03-merge-lineage.json` with deterministic input IDs,
source/block hashes, original IDs, every member's confidence/severity and routes
to intermediate `M-NNN` IDs. Its text-based grouping is a heuristic, not verified
root-cause equivalence. Triage assigns stable final IDs and supplies a map such
as `{"M-001": ["F-003"], "M-002": ["F-001", "F-002"]}`. Run
`review_integrity.py remap <lineage.json> --mapping <map.json>` and import its
result with `merge_routes`, `candidate_remap` and raw provenance. Add every other
stream before final conservation; additional stream routes need not enter the
shard-specific map. Unmapped intermediate routes and inconsistent
maps fail. Final candidate IDs remain stable after triage.
When the merger's `input_records` inventory survives, it must agree with every
shard route and remain included in the combined input inventory. Removing a
route while leaving its inventory record fails; complete artifact rewriting
cannot be authenticated by this checker.
In this initial schema, `input_records` identifies merger inventory and requires
an explicit final remap even if the namespace marker was accidentally omitted.

Each final `report_dispositions` object has `id` and state `published`, `deferred`,
`rejected` or `contested`. Unpublished items need a concrete `reason`. Published
items preserve the record's `kind`. If reporting severity, identify `venue`,
`decision_reviewer` and the unchanged `severity` of that review's eligible,
technically supported decision by the reviewer predeclared in
`policy.venue_adjudicators`. Do not choose a reviewer after seeing severity.
Retain the full venue vector and dissent from the tally in the report.
With no venue, omit severity. A supported
advisory can publish its own claim; uncertainty cannot become QA by relabeling.

Only supported records with supported policy results, resolving evidence and
review provenance, and no open/stale linked contradiction are publishable.
Unresolved items and queue overflow remain in the sidecar and limitations.
Do not silently discard them. A final report must reflect these dispositions;
the JSON gate does not parse or attest arbitrary Markdown, enforce pipeline run
mode or verify both pre-judge and deep-review stages. Existing execution and
remediation checks remain separate confirmation requirements. Saved-result
reconciliation compares declared artifact IDs, not independently authenticated
truth. It is required when a previous consensus artifact exists.

## Disposition visibility and manual corrections

Ledger entries have `id`, `revision_key`, `revision`, state `open`, `deferred`,
`closed` or `contested`, `basis_ids`, `limitations`, optional `candidate_ids`,
and a `reason` for deferral. Closures without resolving references are reported
as unsupported. Revision changes mark keyed closures stale. Linked stale,
unsupported closures or contested conclusions block their candidate's publication.
Open items and unsupported deferrals remain visible limitations; a material
unresolved premise must also be recorded in the candidate components.
`closed_with_reference` means a reference exists, not verified correctness.
Report counts and limitations; never call read counts correctness coverage.

For a specific correction backed by an artifact already in the bundle:

```bash
python3 scripts/review_integrity.py contradict audit-output/review-records.json --evidence-root <snapshot-root> --entry-id <ledger-id> --source-id <source-id> --premise '<specific corrected premise>' --actor-id <reviewer-id>
```

This returns a **new bundle on stdout**. Save it separately, review the diff,
then replace the working record. It marks the entry and linked candidates
contested and invalidates their prior approvals. Identical artifact/premise
fingerprints do not create duplicate flags. It does not invoke another agent.
Release 0 provides manual corrections only; automated re-review is deferred.

Resolve without deleting the flag using `resolve <bundle> --evidence-root <root>
--fingerprint <fingerprint> --basis-id <source-id> --actor-id <reviewer-id>
--reason '<specific resolution>'`. Repeat `--basis-id` for multiple artifacts.
This retains the flag and attributable resolution, restores the ledger's
pre-flag state (without turning open work into a closure), preserves and adds
basis references, and leaves the candidate contested. Fresh reviews must include the
contrary artifact and resolution basis and bind the new digest before support.
Authentication remains external: editable JSON cannot detect malicious flag or
history deletion. Partial deletion or disagreement between surviving ledger,
candidate and history copies does fail consistency checks. A duplicate already
resolved flag returns a clear error rather than silently discarding dissent;
use new evidence/a corrected premise for a new flag. New linked candidates
inherit the existing resolved artifact and still require fresh review. Mixed
open/resolved copies can be reconciled with an attributed resolution while
retaining previous resolution information in history.
Flags retain `affected_candidate_ids`; silently unlinking a previously affected
candidate fails. Keep an out-of-scope candidate in the lineage with a visible
disposition rather than erasing its correction history. Multiple simultaneous
flags retain the ledger's `pre_contradiction_state` until all are resolved;
an earlier manual contested state is never cleared by settling one new premise.
Expanding a flag's affected membership conservatively invalidates approvals for
all candidates sharing that flag. This initial release does not import interim
development bundles whose flags lack `affected_candidate_ids`; reconstruct
their provenance as unresolved rather than inventing missing metadata.

Use `transition <bundle> --evidence-root <root> --id <id> --state <state>
--actor-id <reviewer-id> --reason '<concrete reason>'` for guarded state changes. It also returns a copy
on stdout and records history. Support requires resolving evidence and policy;
final rejection requires the declared policy. Demotions to unresolved/contested
remain possible when evidence breaks, without requiring renewed approvals first.
Support transitions check the candidate, its relied-on sources and bundle-level
invariants; an unrelated candidate awaiting review does not prevent a clean
candidate's state update. The complete publication gate still requires the
whole bundle to pass.
Copy-returning commands exit 0 on successful mutation, not publication approval.
Rejected records cannot jump
directly to supported. Human review queues are bounded: overflow stays deferred.
For legacy prose, retain original IDs and sources, mark unresolved information,
and collect new reviews; never invent missing approvals during migration.

## Separate evaluation ledger

For case-level retrospective accounting, use `review-funnel.md` and
`scripts/review_funnel.py`. Keep unknown eligibility and missing historical
records explicit; publication support does not establish benchmark recall.
This separate offline ledger preserves reference/claim grading and reported
interpretations without treating them as human-verified loss stages.
