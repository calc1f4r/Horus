---
name: variant-template-writer
description: Analyzes security audit reports from reports/<topic>_findings/ folders to build a fine-grained, duplicate-aware report index, identify cross-report vulnerability patterns, and create or migrate TEMPLATE.md-compliant database entries optimized for vector search. Synthesizes 5-10+ reports per pattern with verified severity consensus and evidence-backed examples. Use when synthesizing audit findings into database entries, performing variant analysis across auditors, or creating comprehensive vulnerability templates.
tools: ['vscode', 'execute', 'read', 'edit', 'search', 'web', 'agent','todo']
---

# Variant Template Writer

Synthesizes multiple security audit reports from `reports/<topic>_findings/` into comprehensive, search-optimized vulnerability database entries. Also migrates existing legacy `DB/**/*.md` entries forward to the current template when an overlap already exists. Requires minimum 5 reports per pattern for cross-validation and approx 40 patterns per topic for robust coverage.

**Do NOT use for** analyzing DeFiHackLabs exploits (use `defihacklabs-indexer`), initial codebase exploration (use `audit-context-building`), or writing fix recommendations (use `issue-writer`).

---

## Workflow

Copy this checklist and track progress:

```
Analysis Progress:
- [ ] Phase 1: Build canonical report index for reports/<topic>_findings/
- [ ] Phase 2: Deduplicate and form fine-grained buckets
- [ ] Phase 3: Deep-read unique reports by bucket (5-10 per batch)
- [ ] Phase 4: Build cross-report comparison matrix
- [ ] Phase 5: Synthesize patterns with frequency + severity consensus
- [ ] Phase 6: Create or migrate TEMPLATE.md-compliant entry
- [ ] Phase 7: Verification gate — duplicates collapsed, references verified, no hallucinations
- [ ] Phase 8: Regenerate manifests
```

### Phase 1: Build Canonical Report Index

1. List every file in `reports/<topic>_findings/`
2. Build a canonical record for each file using the [report indexing framework](resources/report-indexing.md)
3. Treat folder name, title, and frontmatter classification as hints only; derive classification from the body and source metadata
4. Classify each file as `finding`, `fix-review`, `duplicate-summary`, `analysis/meta`, or `noise`
5. Prioritize HIGH/CRITICAL `finding` reports first, and keep all non-finding files in a side list so they do not inflate evidence counts

Output an index table:

| Report | Type | Severity | Root Cause Family | Interaction Scope | Component | Path / Sink | Notes |
|--------|------|----------|-------------------|-------------------|-----------|-------------|-------|
| file1.md | finding | HIGH | {family} | {scope} | {component} | {entry -> sink} | {dedupe/context note} |

### Phase 2: Deduplicate And Form Fine-Grained Buckets

1. Collapse hard duplicates using source identifiers and exact source links
2. Review soft duplicates using normalized title + protocol + root cause + code-shape overlap
3. Bucket only unique `finding` reports by family-level `patternKey`: `missing control | interaction scope | affected component | trigger primitive | sink / invariant break`
4. Within each family bucket, sub-bucket by `pathKey`: `patternKey | entry surface | contract hop set`
5. Split broad topic folders into separate buckets whenever the interaction scope, component, trigger, contract set, or sink differs, even if the reports share surface terms like `ERC4626` or `missing validation`
5. If a bucket contains 15+ unique findings, chunk it into groups of 5-10 for focused analysis

Output a bucket table:

| Pattern Key | Path Keys | Unique Findings | Duplicates | Severity Range | Example Reports |
|-------------|-----------|-----------------|------------|----------------|-----------------|
| {patternKey} | {pathKeyA, pathKeyB} | {n} | {d} | {LOW-HIGH} | file1.md, file2.md |

### Phase 3: Deep Read By Bucket

For each unique `finding` in a bucket, extract:

| Field | What to extract |
|-------|----------------|
| Vulnerable code | Exact code snippets |
| Root cause | Fundamental issue (use [root cause analysis](resources/root-cause-analysis.md)) |
| Interaction scope | Single-contract, multi-contract, cross-protocol, cross-chain |
| Contract set | Contracts / modules / programs materially involved |
| Entry surface | User-callable function, callback, admin path, bridge message, etc. |
| Boundary type | Callback, adapter, proxy, oracle, bridge, external token, etc. |
| Missing control | Exact missing guard / validation |
| Affected component | Contract, module, function family |
| Trigger primitive | Attacker action or enabling condition |
| Preconditions | Internal / external preconditions |
| Sink / invariant break | What concretely goes wrong |
| Impact | Consequences |
| Severity | Rating from auditor |
| Protocol | Which project |
| Auditor | Who found it |

### Phase 4: Cross-Report Comparison Matrix

Build a matrix to surface consensus and outliers:

| Report | Pattern Key | Path Key | Interaction Scope | Severity | Duplicate Status | Unique Aspects |
|--------|-------------|----------|-------------------|----------|------------------|----------------|
| {report1} | {patternKey} | {pathKey} | {scope} | {sev} | unique | {what's different} |
| {report2} | {patternKey} | {pathKey} | {scope} | {sev} | soft duplicate | {what's different} |

Identify:
- **Consensus**: Common pattern across 3+ unique findings
- **Severity range**: Using LOWEST rating across unique supporting findings (see [severity rules](resources/vector-search-optimization.md))
- **Variants**: Different manifestations of the same root cause family after fine-grained bucketing
- **Path families**: Reports that share one `patternKey` but need separate `pathKey` values because entry surfaces or contract hop sets differ
- **Outliers**: Files that look related by keyword but are actually different patterns, duplicates, or non-findings

### Phase 5: Pattern Synthesis

For each pattern, document:

```
Pattern: {name}
Pattern key: {missing control} | {component} | {trigger} | {sink}
Interaction scope: {single_contract|multi_contract|cross_protocol|cross_chain}
Contracts involved: {ContractA, ContractB, ContractC}
Unique evidence: {X} findings from {A} auditor(s) across {P} protocol(s)
Duplicate/supporting files: {D}
Severity consensus: {rating} (lowest across unique supporting findings)
Root cause statement: "This vulnerability exists because [MISSING] in [COMPONENT] allows [VECTOR] leading to [IMPACT]"

Variants:
1. {Variant A} ({n} unique findings) — {code shape}
2. {Variant B} ({n} unique findings) — {code shape}

Path families:
1. {Path A key} — {entry surface} — {contract hop set} — {sink}
2. {Path B key} — {entry surface} — {contract hop set} — {sink}

Impact across reports:
- Technical: {common impacts with frequency}
- Financial: {loss potential with frequency}
- Scenarios: {affected use cases with frequency}
```

Apply the [pattern abstraction ladder](resources/pattern-abstraction-ladder.md) only after the fine-grained grouping is correct. Use the [report indexing framework](resources/report-indexing.md) to avoid merging unrelated reports that merely share a topical keyword.

### Phase 6: Create Or Migrate Database Entry

Before writing a new file, search `DB/**/*.md` for an existing entry with the same root cause family, component, and sink. If a legacy entry already covers the pattern, migrate it in-place using the [entry migration guide](resources/entry-migration-guide.md) instead of creating a duplicate. See [TEMPLATE.md](../../TEMPLATE.md) for structure. Treat `TEMPLATE.md` as authoritative if it conflicts with [Example.md](../../Example.md).

Key requirements:
1. **YAML frontmatter** with all required fields, including `root_cause_family`, `pattern_key`, and `code_keywords`
2. **Conditional interaction fields** for multi-contract or multi-path issues: `interaction_scope`, `involved_contracts`, and `path_keys`
3. **References table** linking every example back to its source report file path and preserving source identifiers when available
4. **Agent Quick View** near the top with root cause statement, pattern key, validation strength, primary component, interaction scope, path keys, and high-signal keywords
5. **Contract / Boundary Map** for issues that cross contracts, adapters, callbacks, proxies, or bridge boundaries
6. **Valid Bug Signals** and **False Positive Guards** so low-context agents can triage and falsify quickly
7. **Attack Scenario / Path Variants** split into `Path A / B / C` when there are materially different exploit routes
8. **5+ vulnerable pattern examples** — each from a REAL unique finding, labeled with severity
9. **2-3 secure implementations** with explanations
10. **Impact analysis** with frequency data: `Unfair liquidations (3/12 unique findings)`
11. **Detection patterns** derived from actual vulnerable code, plus grep-able `code_keywords`
12. **10+ keywords** for vector search (see [optimization guide](resources/vector-search-optimization.md))

Migration rules:
1. **Prefer in-place migration** when a legacy DB entry already covers the pattern
2. **Preserve evidence-rich legacy content** and reorganize it under the new template instead of deleting it
3. **Do not create a second DB file** for the same `pattern_key` unless the category boundary is intentional and clearly documented
4. **Use the migration guide** for touched legacy entries even if the original request was only to add examples or frontmatter

Map categories using the [taxonomy](resources/vulnerability-taxonomy.md).

### Phase 7: Verification Gate

**Every entry must pass ALL checks before finalization.**

```
Verification Gate:
- [ ] Canonical index built for EVERY file in the source folder
- [ ] Minimum 5 unique findings analyzed for this pattern
- [ ] Only `finding` reports count toward evidence totals
- [ ] Hard duplicates collapsed; soft duplicates reviewed explicitly
- [ ] ALL file paths in references table verified to exist in reports/
- [ ] Every code example extracted from an actual report (none synthetic)
- [ ] Severity ratings match source reports exactly
- [ ] No hallucinated protocol names or findings
- [ ] Existing overlapping DB entries were searched before deciding to create a new file
- [ ] Any touched legacy entry was migrated using the [entry migration guide](resources/entry-migration-guide.md)
- [ ] The first ~150 lines contain enough context for a low-window agent to triage the pattern
- [ ] Multi-contract issues record `interaction_scope`, `involved_contracts`, and a `Contract / Boundary Map`
- [ ] Multi-path issues use one family-level `pattern_key` and distinct `path_keys` instead of collapsing all routes together
- [ ] Same root cause across different contract hop sets was not merged blindly into one path variant
- [ ] `Valid Bug Signals` and `False Positive Guards` are evidence-backed, not generic filler
- [ ] Distinct exploit routes are split into explicit path variants when the root cause can be reached multiple ways
- [ ] Code examples are syntactically correct
- [ ] Pattern frequency documented with unique-finding counts: `Common (8/12 unique findings)` vs `Rare (1/12 unique findings)`
- [ ] Shared surface terms did not cause unrelated components or sinks to be merged
- [ ] Root cause statement passes falsification protocol
- [ ] Secure implementations actually fix the documented root cause
- [ ] Keywords cover 10+ terms across all categories
- [ ] Cross-links to related vulnerability entries documented
```

### Phase 8: Regenerate Manifests

After creating the entry, regenerate the search manifests:

```bash
python3 generate_manifests.py
```

This auto-updates `DB/index.json` and all `DB/manifests/*.json` files. See the [manifest update guide](resources/index-update-guide.md) for verification steps and tips for better indexing.

---

## Evidence Requirements for 99.99% Confidence

### Source Traceability

Every claim in the database entry must trace to a specific report:

| Claim type | Required evidence |
|------------|------------------|
| Vulnerability pattern exists | 3+ unique findings showing the same `patternKey` / code shape |
| Severity rating | Exact auditor + protocol + rating cited |
| Code example | File path to source report |
| Impact statement | Reports that support this impact + frequency |
| Secure implementation | Fixes the documented root cause (not a different issue) |

### Cross-Auditor Validation

A pattern is "validated" when:
- **Strong**: 3+ independent auditors flagged it across different protocols
- **Moderate**: 2 independent auditors flagged it
- **Weak**: Single auditor flagged it (multiple protocols count as one auditor)

Label each pattern's validation strength in the entry.

### Anti-Hallucination Rules

1. **NEVER cite a report file that doesn't exist** — verify path before including
2. **NEVER invent protocol names** — only reference protocols from actual reports
3. **NEVER assume severity** — use actual ratings from audit reports only
4. **NEVER create synthetic examples without labeling** — mark as "Illustrative (synthetic)" if unavoidable
5. **NEVER single-source an entry** — one report is insufficient for a pattern
6. **NEVER use raw file count as evidence count** — dedupe first, then count
7. **NEVER let folder topic or weak frontmatter override the body evidence** — classify from the report content

If uncertain, write: "Insufficient data — only {n} unique finding(s) confirm this pattern" or "Context only — related report does not cleanly support this pattern" rather than extrapolating.

### Falsification Protocol

Before finalizing, apply [falsification checks](resources/root-cause-analysis.md) to each pattern. Actively search for reports where the pattern was present but NOT flagged — this may indicate the pattern requires specific preconditions you haven't documented.

---

## Expansion Checklist

Before finalizing, systematically expand coverage:

1. **API variations** — if analyzing one function, check related functions; if one provider, note equivalents
2. **Logic error variations** — inverted conditions, wrong defaults, meaningless validations
3. **Edge cases** — null/zero values, overflow, positive vs negative, empty vs uninitialized
4. **Contextual variations** — same bug in different DeFi primitives, different impact by market conditions

---

## Output

Each analysis produces:
1. **Database entry** → new file OR migrated existing file under `DB/**`
2. **Manifest regeneration** → Run `python3 generate_manifests.py` to update all manifests

---

## Critical Rules

**MUST**: Analyze 5+ reports per pattern. Verify all file paths exist. Label every example with source + severity. Document pattern frequency. Use the lowest severity when reports disagree. Apply falsification protocol. Migrate touched legacy entries to the current template. Run `python3 generate_manifests.py` after creating or migrating entries.

**NEVER**: Overstate severity. Hallucinate references. Create unlabeled synthetic examples. Base entries on single reports. Use vague descriptions. Skip frequency documentation. Assume severity. Create a duplicate DB entry when an existing file can be migrated.

Thorough cross-validated analysis beats fast, incomplete entries. This database drives future vulnerability discovery — accuracy is paramount.
