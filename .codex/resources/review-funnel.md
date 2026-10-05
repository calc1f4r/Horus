# Offline case-level review evaluation

Use `scripts/review_funnel.py` to check an existing evaluation ledger against a
separately retained reference inventory. This is an offline bookkeeping tool.
It does not inspect target code, generate findings, schedule agents, fetch URLs,
or authenticate a person's review. Keep research labels away from producers.

```bash
python3 scripts/review_funnel.py case-ledger.json --inventory case-inventory.json --evidence-root <archived-record-root>
```

Output is JSON; 0 means the declared records are structurally consistent, not
that evaluation is complete. Inspect unknown counts and null metrics. The CLI
writes no files. Closed fields, duplicate-key rejection, source hashes, LF line
ranges and inventory reconciliation prevent accidental loss or reinterpretation.

Inventory schema: integer `schema_version: 1` and `cases`, with exact fields
`id`, `cohort`, `reference_severity`, boolean `included`, `exclusion_reason`
and `exclusion_basis_ids`. Exclusions require resolving basis IDs and a reason. Reference severities
are `critical`, `high`, `medium`, `low`, `informational`. Preserve excluded cases
in the inventory with `included: false`; they stay visible but do not enter the
included summary. Empty inventories fail. Retain the inventory outside the
working ledger and bind its exact file SHA256 in the ledger.

Ledger fields: `schema_version`, `inventory_sha256`, `observation_unit`,
`sources`, `cases`. Each source has `id`, relative `path`, lowercase `sha256`,
immutable archive `revision`, and inclusive integer `line_start`/`line_end`.
Paths must resolve inside the evidence root. Pin target/dependency identities
in the archived manifests supporting an assessment; an archive hash alone does
not authenticate the contents of that manifest.

Each case has exactly `id`, `owner_label`, `matched_candidate_ids`,
`label_basis_ids`, `claimed_severities`, `reported_annotation`,
`annotation_basis_ids`, `assessments`. Reported annotations need archived basis.
Owner labels are `matched`, `unmatched`, `unknown`; matched labels require
candidate IDs, other labels prohibit them. All labels need archived basis IDs.
Claimed severities retain their original spelling and do not change reference
severity. Original labels remain intact when reconciliation challenges a match. Generic
`severity-error` remains a reconciliation blocker; directional grading and venue
differences do not rewrite the reference-severity bucket.

Every case carries all five assessments:

| Field | Status values |
|---|---|
| eligibility | unknown, unresolved, eligible, ineligible |
| delivery | unknown, unresolved, delivered, missing |
| provisional_presence | unknown, unresolved, present, absent |
| closure | unknown, unresolved, bounded, unbounded, not-applicable |
| grading | unknown, unresolved, rubric-consistent, claim-understated, claim-overstated, venue-rule-difference, insufficient-match, severity-error |

An assessment has exactly `status`, `authority`, `reviewer_id`, `basis_ids`,
`reason`, `coverage`, `scope`, `limitations`. Unknown assessments have authority
`unknown`, reviewer `null`, and coverage `unknown`. A human `unresolved` assessment retains reviewer, basis, examined coverage and
limitations, but contributes unknown to settled metrics and stage attribution.
A substantive assessment
needs a reviewer ID, resolving basis IDs, nonempty reason/scope, and `partial`
or `complete` coverage. Partial coverage requires visible limitations.
Partial human assessments remain unknown for metrics/stage attribution; a
bounded closure can retain its explicit partial scope and limitations.

Authority `reported` preserves retrospective interpretations but contributes
only `unknown` to verified-stage calculations. Authority `human` means the file
declares an attributable human decision; the tool cannot verify identity,
independence, adequacy of evidence or correctness. Do not change authority to
human on behalf of an absent reviewer. Model criticism remains reported.

Negative conclusions are bounded by their declared scope. Human assertions of
missing delivery or absent provisional candidates require complete evidence
for that scope. Incomplete logs must stay unknown. A matched final output does
not prove an earlier provisional candidate existed. A reference absent from
the final output does not establish a generation failure.

Loss stages are deliberately coarse. Verified eligibility plus missing
delivery yields `delivery-missing`. Verified eligibility/delivery plus absent
provisional output yields `before-provisional`; present provisional output
yields `after-provisional-unlocalized`. Other misses stay `unknown`; delivery and provisional-presence status counters
remain independently visible even while the cause is unlocalized. Existing
owner matches remain visible as `owner-matched`. A substantive ineligibility
assessment preserves the historical label while classifying scope separately.

The eligible-recall field is null while eligibility is unknown, eligible owner
labels are unknown, or eligible matches await grading/equivalence reconciliation.
Missing delivery remains in the end-to-end denominator. No delivery-conditioned
recall is substituted. Summaries separate cohorts and reference severities, retain excluded-stratum
counts, identify eligible matched cases separately, and expose closure counters.
Reported and deferred assessments retain their full caveats and source basis.
The scope/coverage gate checks declarations, not evidence sufficiency; a person
can still misstate the applicable scope. Separate authentic provenance and
human assessment of scope are required.
Pooled observed waves are descriptive; recording the observation unit does not
make them comparable single-run or held-out estimates.

Human grading review must distinguish reference, claim and applicable venue
rubrics, cite their archived basis, and accept that an insufficient match may
challenge the original numerator. No tool here rewrites frozen adjudication
labels. Resolve disagreements through the study's separately recorded label
amendment process before making a revised performance claim.

Before attributing failures to reasoning, use saved delivery manifests and
handoff records to check which pinned inputs were available. Missing context,
context not consumed, interpretation errors and absent records are different
claims; incomplete evidence does not select between them. Keep source-version,
rubric and reviewer uncertainty visible.

This ledger implements record correctness and human review accounting. It
does not measure a recall uplift. Exposed historical cases are development
material; future efficacy claims require independent held-out evidence,
blinded outcome assessment, comparable budgets and target-level uncertainty.
