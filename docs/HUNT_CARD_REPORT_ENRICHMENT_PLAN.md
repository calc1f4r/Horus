# Hunt Card Report Enrichment Plan

**Status**: Draft  
**Date**: 2026-04-28  
**Scope**: Enrich every generated Horus hunt card using evidence from `reports/`, while preserving the new graph-aware Horus architecture.  
**Related architecture**: `docs/HORUS_GRAPH_EVOLUTION_PLAN.md`, `docs/codex-architecture.md`

## 0. Purpose

Horus hunt cards are the primary low-context runtime interface for DB-powered audits. They currently compress DB entries into grep patterns, detection statements, verification steps, and triage hints. The goal of this plan is to make every hunt card more correct, more actionable, and better connected to real audit evidence by reading the raw report corpus behind each DB entry.

This plan is intentionally written for future execution. An agent should be able to return to this document later, understand the intended workflow, and execute the work without re-deriving the architecture.

## 1. Core Rule

Do **not** hand-edit generated hunt-card JSON.

The correct enrichment path is:

```text
reports/ evidence
  -> canonical DB/**/*.md entries and frontmatter
  -> scripts/generate_manifests.py extraction
  -> scripts/generate_micro_directives.py enrichment
  -> DB/manifests/**/*.json generated outputs
  -> scripts/build_db_graph.py graph artifacts
  -> benchmark validation
```

Generated files include:

- `DB/index.json`
- `DB/manifests/*.json`
- `DB/manifests/huntcards/*.json`
- `DB/graphify-out/**`

If hunt-card behavior is wrong, fix either:

- the source DB Markdown in `DB/**/*.md`, or
- the generator/enricher scripts in `scripts/`.

Then regenerate.

## 2. Definition Of Done

The enrichment project is complete when:

- Every existing hunt card has been scored for quality.
- Every hunt card is mapped to explicit or inferred supporting reports where possible.
- DB entries have been updated with report-backed root causes, attack scenarios, valid bug signals, false-positive guards, impact notes, and source references.
- `scripts/generate_manifests.py` and `scripts/generate_micro_directives.py` extract the richer DB structure into hunt cards.
- `DB/manifests/huntcards/all-huntcards.json` is regenerated from source.
- `DB/graphify-out/graph.json` is rebuilt from canonical generated artifacts.
- A benchmark shows recall improvement without unacceptable precision loss.

Target metrics:

- At least 20% recall lift over the current hunt-card baseline.
- False-positive rate no more than 1.5x the baseline.
- Audit runtime no more than 1.5x the baseline.

## 3. Required Outputs

Create these durable DB-local working artifacts during execution:

```text
DB/_telemetry/huntcard-enrichment/
├── baseline-quality.json
├── card-report-map.json
├── unresolved-report-map.json
├── evidence-packs/
│   └── <hunt-card-id>.json
├── before-after/
│   └── <hunt-card-id>.json
├── benchmark-results.json
└── ENRICHMENT-REPORT.md
```

Create the cross-DB progress tracker at:

```text
DB/_telemetry/huntcard-enrichment/CHECKLIST.md
```

Create or update these source/runtime files as needed:

```text
DB/**/*.md
scripts/generate_manifests.py
scripts/generate_micro_directives.py
tests/benchmark/findings.jsonl
DB/_drafts/README.md
DB/_telemetry/README.md
```

Regenerate these outputs after source changes:

```text
DB/index.json
DB/manifests/*.json
DB/manifests/huntcards/*.json
DB/graphify-out/**
```

## 4. Current Hunt Card Shape

Current generated hunt cards include fields like:

```json
{
  "id": "tokens-example-001",
  "title": "First Depositor Inflation Attack",
  "severity": "HIGH",
  "grep": "previewDeposit|previewMint|totalAssets|totalSupply",
  "detect": "Empty vault share accounting can be inflated before a victim deposit.",
  "cat": ["tokens", "erc4626", "vault"],
  "ref": "DB/tokens/example.md",
  "lines": [100, 180],
  "check": [
    "VERIFY: share minting depends on externally manipulable totalAssets.",
    "PROVE: attacker can donate or inflate assets before victim deposit.",
    "FALSIFY: vault mints dead shares or enforces minimum initial liquidity."
  ],
  "antipattern": "Initial depositor can set share price with dust liquidity.",
  "securePattern": "Mint dead shares or enforce a minimum first deposit.",
  "validWhen": "An attacker can cheaply skew the first depositor exchange rate.",
  "invalidWhen": "The vault neutralizes empty-vault exchange-rate manipulation.",
  "impact": "Victim deposit receives too few shares and loses redeemable assets."
}
```

The enrichment should preserve this compact shape, but make each field report-backed and executable.

Optional additional generated fields may be introduced if they remain compact:

```json
{
  "preconditions": ["empty or near-empty vault", "attacker can donate or compound assets"],
  "proofShape": "attacker seeds dust, inflates accounting denominator, victim receives too few shares",
  "falsePositiveSignals": ["dead shares exist", "minimum initial deposit prevents profitable setup"],
  "reportEvidence": {
    "count": 7,
    "severityConsensus": "HIGH",
    "sampleReports": ["reports/erc4626_findings/..."]
  },
  "graphHints": {
    "variants": ["donation attack", "rounding loss", "share inflation"],
    "commonlyComposesWith": ["oracle exchange-rate manipulation", "fee-on-transfer accounting"]
  }
}
```

## 5. Phase 0: Baseline Inventory

Read:

- `DB/manifests/huntcards/all-huntcards.json`
- `DB/index.json`
- `DB/manifests/*.json`

For every card, record:

- `id`
- `title`
- `severity`
- `grep`
- `detect`
- `check`
- `antipattern`
- `securePattern`
- `validWhen`
- `invalidWhen`
- `impact`
- `ref`
- `lines`
- `cat`
- `neverPrune`

Write:

```text
DB/_telemetry/huntcard-enrichment/baseline-quality.json
```

Score every card on:

- `grep_specificity`: grep terms are code-like, distinctive, and not overly generic.
- `detect_correctness`: detect text states the actual root cause.
- `check_actionability`: checks can be executed against target code.
- `false_positive_guard`: `invalidWhen` clearly rejects safe implementations.
- `impact_clarity`: impact explains the security consequence.
- `report_support`: number and quality of supporting raw reports.
- `graph_connectivity`: card has meaningful relationships in the DB graph.

Recommended score scale:

```json
{
  "score": 0,
  "meaning": "missing or unusable"
}
```

```json
{
  "score": 1,
  "meaning": "weak, vague, or mostly structural"
}
```

```json
{
  "score": 2,
  "meaning": "usable but incomplete"
}
```

```json
{
  "score": 3,
  "meaning": "strong and directly executable"
}
```

## 6. Phase 1: Map Hunt Cards To Reports

For every hunt card:

1. Use `card.ref` and `card.lines` to read only the relevant DB section.
2. Parse the DB section and frontmatter for:
   - local `reports/<category>/<file>.md` references
   - Solodit IDs
   - source links
   - GitHub issue links
   - audit firm names
   - protocol names
   - source report tables
3. If explicit report references are missing, infer candidate reports by:
   - matching `title`
   - matching `searchKeywords`
   - matching `codeKeywords`
   - matching `vulnerability_type`
   - matching report category folder
   - matching protocol category
4. Save confidence for each mapping:
   - `explicit`: direct path or ID in DB entry
   - `strong_semantic`: multiple title/root-cause/code terms match
   - `weak_keyword`: only broad terms match
   - `unresolved`: no credible report mapping

Write:

```text
DB/_telemetry/huntcard-enrichment/card-report-map.json
DB/_telemetry/huntcard-enrichment/unresolved-report-map.json
```

Suggested schema:

```json
{
  "card_id": "tokens-example-001",
  "db_ref": "DB/tokens/example.md",
  "lines": [100, 180],
  "report_refs": [
    {
      "path": "reports/erc4626_findings/example.md",
      "confidence": "explicit",
      "matched_terms": ["previewDeposit", "inflation", "first depositor"],
      "solodit_id": "32092",
      "severity": "MEDIUM",
      "audit_firm": "Code4rena",
      "protocol": "Wise Lending"
    }
  ],
  "unresolved": false
}
```

## 7. Phase 2: Extract Evidence Packs

For each mapped report, extract only the content needed to improve hunt-card precision and recall.

Evidence fields:

- `root_cause`: why the bug exists.
- `attack_preconditions`: what must be true before exploitation.
- `attacker_capabilities`: permissions, capital, roles, timing, or state required.
- `vulnerable_identifiers`: function names, variable names, modifiers, events, modules.
- `exploit_sequence`: ordered exploit or failure sequence.
- `broken_invariant`: accounting, access control, oracle, cross-chain, or state invariant violated.
- `impact`: concrete consequence.
- `mitigation`: fix or safe implementation signal.
- `false_positive_guards`: conditions that make a grep hit non-reportable.
- `severity`: report severity.
- `source_metadata`: protocol, firm, source URL, Solodit ID, finders if available.

Write one evidence pack per card:

```text
DB/_telemetry/huntcard-enrichment/evidence-packs/<card-id>.json
```

Suggested schema:

```json
{
  "card_id": "tokens-example-001",
  "db_ref": "DB/tokens/example.md",
  "reports": [
    {
      "path": "reports/erc4626_findings/example.md",
      "root_cause": "Share minting uses a denominator that an attacker can inflate before the victim deposit.",
      "attack_preconditions": ["vault has little or no supply", "attacker can affect totalAssets before victim deposit"],
      "attacker_capabilities": ["front-run deposit", "donate assets or trigger compounding"],
      "vulnerable_identifiers": ["previewMintShares", "totalSupply", "underlyingLpAssetsCurrent"],
      "exploit_sequence": [
        "attacker seeds dust liquidity",
        "attacker inflates accounting assets",
        "victim deposits against skewed exchange rate",
        "victim receives too few shares"
      ],
      "broken_invariant": "Depositor shares should fairly represent contributed assets.",
      "impact": "Victim loses redeemable assets to exchange-rate manipulation.",
      "mitigation": "minimum first deposit, dead shares, or correct initialization",
      "false_positive_guards": ["admin performs safe initial seeding before public deposits"],
      "severity": "MEDIUM"
    }
  ],
  "consensus": {
    "report_count": 4,
    "severity_consensus": "HIGH",
    "common_root_cause": "attacker-controlled exchange-rate denominator"
  }
}
```

## 8. Phase 3: Enrich Canonical DB Markdown

For each DB entry, update the source Markdown with report-backed structure.

Prefer adding or normalizing these sections:

```markdown
### Root Cause

### Attack Scenario

### Code Patterns to Look For

### Valid Bug Signals

### False Positive Guards

### Impact

### Secure Implementation

### References & Source Reports
```

Also enrich YAML frontmatter when applicable:

```yaml
code_keywords:
  - previewDeposit
  - totalAssets
  - totalSupply
primitives:
  - ERC4626
  - vault shares
affected_component:
  - share accounting
vulnerability_type: share inflation
root_cause_family: attacker-controlled accounting denominator
attack_type: first depositor inflation
impact: asset loss
protocol_categories:
  - vault
  - yield
```

DB Markdown must remain concise. Do not paste entire reports. Summarize the report evidence and keep source links or local report paths in references.

## 9. Phase 4: Improve Manifest And Hunt-Card Extraction

Update `scripts/generate_manifests.py` so richer source fields become manifest fields.

Potential additions:

- `preconditions`
- `proofShape`
- `falsePositiveSignals`
- `reportEvidence`
- `graphHints`

Improve extraction of:

- `codeKeywords`
- `searchKeywords`
- `rootCause`
- severity consensus
- report references
- protocol categories

Update `scripts/generate_micro_directives.py` so generated `check` entries are proof-oriented:

- `VERIFY`: confirm the code contains the unsafe root cause.
- `PROVE`: show attacker-controlled reachability or state manipulation.
- `FALSIFY`: identify safe implementation conditions.
- `IMPACT`: connect the bug to concrete loss, DoS, or invariant violation.
- `COMPOSE`: note multi-step or cross-contract compositions when reports show them.

Generated checks should be compact and directly executable against grep hit locations.

## 10. Phase 5: Graph-Aware Enrichment

After DB and generator updates, rebuild the graph:

```bash
python3 scripts/generate_manifests.py
python3 scripts/build_db_graph.py
python3 scripts/db_quality_check.py
```

Use `DB/graphify-out/graph.json` to verify that enriched cards connect to related vulnerability concepts.

Useful relationship types:

- `variant_of`
- `same_root_cause_as`
- `requires_precondition`
- `commonly_composes_with`
- `leads_to`
- `mitigated_by`

Example relationship cluster for ERC4626/vault inflation:

- first depositor inflation
- donation attack
- exchange-rate manipulation
- rounding loss
- empty vault share inflation
- minimum liquidity mitigation
- dead-share mitigation

The graph layer should expand candidate cards. It should not prune away baseline cards.

## 11. Phase 6: Execution Order

Process manifests in this order:

1. `oracle`
2. `tokens`
3. `general-defi`
4. `amm`
5. `bridge`
6. `sui-move`
7. `solana`
8. `cosmos`
9. `account-abstraction`
10. `zk-rollup`
11. `general-security`
12. `general-infrastructure`
13. `general-governance`
14. `unique`

Reasoning:

- Start with high-impact, high-report-density categories.
- Validate the workflow on categories where report evidence is abundant.
- Move to ecosystem-specific categories after extraction rules stabilize.
- Leave `unique` last because it is heterogeneous and likely needs manual review.

For each manifest:

1. Score current cards.
2. Map reports.
3. Extract evidence packs.
4. Patch DB Markdown.
5. Regenerate manifests and hunt cards.
6. Save before/after card diffs.
7. Run quality checks.
8. Rebuild graph after each major category batch.

## 12. Phase 7: Benchmark

Build:

```text
tests/benchmark/findings.jsonl
```

Each benchmark row:

```json
{
  "finding_id": "wise-lending-m-03",
  "report_path": "reports/erc4626_findings/m-03-first-depositor-inflation-attack-in-pendlepowerfarmtoken.md",
  "expected_card_ids": ["tokens-..."],
  "category": "erc4626",
  "severity": "MEDIUM",
  "multi_step": true,
  "keywords": ["previewMintShares", "totalSupply", "underlyingLpAssetsCurrent", "first depositor"]
}
```

Measure:

- `baseline_recall`: current hunt cards surface expected card.
- `enriched_recall`: enriched hunt cards surface expected card.
- `graph_expanded_recall`: graph expansion surfaces expected adjacent card.
- `precision`: grep hits that survive card checks.
- `triage_quality`: checks lead to correct valid/invalid conclusion.
- `context_efficiency`: fewer full DB reads required.

Write:

```text
DB/_telemetry/huntcard-enrichment/benchmark-results.json
```

## 13. Phase 8: Telemetry And Draft Loop

Use the self-improving hunt-card architecture from the graph evolution plan.

If a confirmed finding has no matching card:

- draft a TEMPLATE-compliant entry in `DB/_drafts/`
- do not auto-promote it into live DB categories
- list it in `DB/_telemetry/huntcard-enrichment/<audit-id>-db-gap-analysis.md`

If an existing card has weak performance:

- write telemetry in `DB/_telemetry/`
- suggest grep refinements, false-positive guards, or source DB edits

The generator must continue ignoring:

- `DB/_drafts/`
- `DB/_telemetry/`

## 14. Validation Commands

After each DB or generator batch:

```bash
python3 scripts/generate_manifests.py
python3 scripts/db_quality_check.py
```

After graph-relevant enrichment:

```bash
python3 scripts/build_db_graph.py
```

When changing Codex-facing or Claude playbooks:

```bash
python3 scripts/sync_codex_compat.py
python3 scripts/sync_codex_compat.py --check
```

If generator output changes, inspect:

```text
DB/manifests/huntcards/all-huntcards.json
DB/manifests/keywords.json
DB/graphify-out/GRAPH_REPORT.md
```

## 15. Quality Gates

A card is considered enriched only if:

- `grep` contains distinctive code identifiers or protocol-specific terms.
- `detect` describes the bug root cause, not just the category.
- `check` includes proof and falsification steps.
- `validWhen` states the reportability condition.
- `invalidWhen` states at least one concrete safe condition when known.
- `impact` is concrete.
- Supporting reports are listed or the lack of report support is explicitly marked.
- Related graph concepts are discoverable after graph rebuild.

## 16. Pilot Recommendation

Start with `tokens` / ERC4626-style vault cards.

Reasons:

- `reports/erc4626_findings/` is dense.
- There are many real variants of the same root causes.
- Existing cards can be tested against concrete report examples.
- Useful graph relationships are obvious:
  - first depositor inflation
  - donation attack
  - rounding loss
  - fee-on-transfer accounting
  - preview function mismatch
  - totalAssets manipulation

Pilot deliverables:

- enriched ERC4626/vault DB sections
- improved extraction rules for proof shapes and false-positive guards
- benchmark examples from `reports/erc4626_findings/`
- before/after comparison for affected hunt cards

Only scale to all manifests after the pilot proves that the enrichment format improves recall and triage quality.

## 17. Non-Goals

This plan does not:

- replace the graph evolution plan
- replace `scripts/generate_manifests.py`
- replace `scripts/build_db_graph.py`
- hand-edit generated JSON
- read all reports into agent context at once
- auto-promote draft DB entries into live manifests
- remove grep-based fallback

The goal is to make the existing architecture stronger, not to bypass it.

## 18. Quick Start For Future Agents

1. Read this file.
2. Read `docs/HORUS_GRAPH_EVOLUTION_PLAN.md`.
3. Read `docs/codex-architecture.md`.
4. Load `DB/manifests/huntcards/all-huntcards.json`.
5. Start with the pilot category:

```text
reports/erc4626_findings/
DB/tokens/
DB/manifests/tokens.json
DB/manifests/huntcards/tokens-huntcards.json
```

6. Produce baseline scoring before editing anything.
7. Patch canonical DB Markdown and generator logic.
8. Regenerate and validate.
9. Document the result in:

```text
DB/_telemetry/huntcard-enrichment/ENRICHMENT-REPORT.md
```
