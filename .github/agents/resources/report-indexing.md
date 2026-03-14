# Report Indexing Framework

Shared framework for normalizing noisy `reports/<topic>_findings/` folders before database synthesis or cross-report analysis.

## Trust Hierarchy

Use the strongest signal available in this order:

1. **Source identifiers** — `solodit_id`, `source_link`, `contest_link`, `github_link`. These are authoritative for provenance and hard deduplication.
2. **Report body sections** — `Root Cause`, `Description`, `Summary`, `Attack Path`, `Internal/External Preconditions`, `Impact`, `Recommendation`, `PoC`, `Original Finding Content`. These are authoritative for classification.
3. **Title** — useful for quick triage, but often describes symptoms instead of the root cause.
4. **Frontmatter classification fields** — `category`, `vulnerability_type`, `tags`, `affected_component`. These are hints only and are often generic or stale.
5. **Folder name** — an acquisition bucket only. Never assume every file inside a topic folder belongs to one vulnerability class.

## Canonical Record

Normalize every raw report into the following record before clustering:

| Field | Purpose | Preferred evidence |
|-------|---------|--------------------|
| `path` | Stable source reference | Filesystem path |
| `sourceKey` | Hard dedupe / provenance | `solodit_id`, else canonical source URL |
| `protocol` | Project normalization | Body content, then frontmatter |
| `auditor` | Independence counting | `audit_firm`, report source |
| `severity` | Preserve source rating | Frontmatter and body severity label |
| `reportType` | Filter evidence vs context | Title + body structure |
| `rootCauseFamily` | Broad vulnerability family | `Root Cause` / `Description` |
| `missingControl` | Exact missing guard / validation | Body evidence |
| `affectedComponent` | Module / contract / function family | Code refs + body |
| `triggerPrimitive` | Attacker action or enabling condition | `Attack Path` / preconditions |
| `sinkOrInvariantBreak` | What concretely goes wrong | `Impact` + body |
| `impactSummary` | Short impact label | `Impact` section |
| `patternKey` | Fine-grained clustering key | Derived formula below |
| `duplicateGroup` | Hard / soft duplicate tracking | Source IDs + title/body similarity |

## Report Type Classification

Classify each file into exactly one report type:

- `finding`: concrete vulnerability with a clear bug, exploit path, or explicit impact
- `fix-review`: evaluates a remediation, patch set, or post-fix behavior
- `duplicate-summary`: mostly lists related findings, duplicates, or contest references
- `analysis/meta`: design discussion, economic analysis, or implementation commentary without a discrete exploitable finding
- `noise`: docs, style, gas, tests, process notes, or other non-security material

Only `finding` records count as primary evidence for a database entry. All other types are context-only.

## Extraction Order

1. Parse frontmatter and preserve all raw metadata.
2. Parse structured body headings and recover the vulnerability narrative.
3. Write a one-sentence root cause statement using the [root cause analysis framework](root-cause-analysis.md).
4. Normalize `missingControl`, `affectedComponent`, `triggerPrimitive`, and `sinkOrInvariantBreak`.
5. Derive `patternKey`.
6. Assign `reportType` and `duplicateGroup`.

## Pattern Key Formula

Use the smallest key that still separates materially different bugs:

`patternKey = missingControl | affectedComponent | triggerPrimitive | sinkOrInvariantBreak`

Examples:

- `missing-share-price-protection | ERC4626 deposit/mint path | donation / manipulated totalAssets | victim share dilution`
- `missing-array-length-validation | reinvest batch loop | mismatched user-supplied arrays | out-of-bounds revert / inconsistent execution`

This key is intentionally finer than a root-cause keyword. Two reports that both say "missing validation" should still split when the component, attacker primitive, or sink differs.

## Merge And Split Rules

- Merge reports only when the same `patternKey` is supported by the body evidence.
- Split reports when they share only a surface term such as `ERC4626`, `missing validation`, `price manipulation`, or `rounding`.
- Split reports when the affected component changes from one function family to another, even if the missing control is similar.
- Split reports when the sink changes from griefing, to DoS, to accounting corruption, to direct loss.
- Use the [pattern abstraction ladder](pattern-abstraction-ladder.md) only after the fine-grained grouping is correct.

## Duplicate Handling

- **Hard duplicate**: same `solodit_id`, same source URL, same GitHub issue, or obviously the same underlying finding number.
- **Soft duplicate**: normalized title, protocol, root cause, and key code excerpts match strongly, but stable IDs differ or are missing.
- Keep the highest-quality representative file for the evidence table.
- Track duplicates as supporting context, but do **not** count them as independent support for frequency, severity consensus, or auditor diversity.

## Counting Rules

- Evidence counts use deduplicated `finding` records only.
- Validation strength counts distinct auditors / contests after deduplication.
- Severity consensus uses the **lowest** severity among unique supporting findings.
- `fix-review`, `analysis/meta`, `duplicate-summary`, and `noise` records may inform narrative context, but never satisfy the minimum-support threshold.
- If a file cannot be classified confidently, mark it as context-only instead of forcing it into a pattern bucket.

## Common Failure Modes

- Topic folders often contain tangential findings that merely mention the same standard or protocol family.
- Frontmatter frequently leaves `category` or `vulnerability_type` as `uncategorized` or `unknown`.
- Titles often name the symptom, not the missing control.
- Fix reviews and analysis memos can look relevant while failing to provide a standalone vulnerability instance.
- Contest duplicate roundups can inflate evidence counts if not collapsed first.