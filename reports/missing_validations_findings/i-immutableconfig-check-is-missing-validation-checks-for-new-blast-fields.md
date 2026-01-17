---
# Core Classification
protocol: DRAFT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29890
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-node-review-draft.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-node-review-draft.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Mattsse
  - Dtheo
  - Sujith Somraaj
  - Blockdev
  - The-lichking
---

## Vulnerability Title

(i ImmutableConfig) Check() is missing validation checks for new Blast fields

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
`optimism/op-chain-ops/immutables/immutables.go#L31`, PR 29

## Description
The method `(i ImmutableConfig) Check()` contains checks for nearly every field in `Immutable`. Checks have been added for the following additional fields introduced by Blast: 
- `i["Shares"]["price"]`
- `i["Gas"]["baseClaimRate"]`
- `i["L2BlastBridge"]["otherBridge"]`

However, the following new Blast fields still do not have a check:
- `immutable["Shares"]["reporter"]`
- `immutable["Gas"]["admin"]`
- `immutable["Gas"]["zeroClaimRate"]`
- `immutable["Gas"]["baseGasSeconds"]`
- `immutable["Gas"]["ceilGasSeconds"]`
- `immutable["Gas"]["ceilClaimRate"]`
- `immutable["Blast"]["yieldContract"]`
- `immutable["USDB"]["bridge"]`
- `immutable["USDB"]["remoteToken"]`

Adding these checks will help the `BuildOptimism()` functionality error gracefully if these fields are not included or malformed in the target JSON file. This will prevent unexpected behavior.

## Recommendation
Add checks for the new fields that do not have any.

---

## Severity: Low Risk

## Context
`optimism/op-chain-ops/immutables/immutables.go#L198-L206`

## Description
USDB predeployment is skipped as highlighted above. The Blast team states that the USDB-related code was commented out due to issues with USDB's constructor, which has since been fixed outside of the review scope.

## Recommendation
Fix the USDB deployment.

> **Note:** This appears to be an artifact of the development process that the developers are aware of, so the severity is set to low. If this is not addressed before launch, the impact will be critical. It is strongly advised that this issue be addressed with care. The code, as it stands at the review commit hash, could prompt a large loss of funds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | DRAFT |
| Report Date | N/A |
| Finders | Mattsse, Dtheo, Sujith Somraaj, Blockdev, The-lichking |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-node-review-draft.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/report-blast-node-review-draft.pdf

### Keywords for Search

`vulnerability`

