---
# Core Classification
protocol: Hyperdrive February 2024
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35825
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Saw-Mon and Natalie
  - Christoph Michel
  - Deivitto
  - M4rio.eth
---

## Vulnerability Title

LPs are paying twice for governance fees when opening longs

### Overview


This bug report discusses a medium risk issue in the code for HyperdriveLong.sol, specifically in the _calculateOpenLong function. The problem is that governance fees are being removed twice from the bond and share reserves, meaning that LPs are paying for them twice. The recommendation is to only remove the fees from the share reserves and to update the bondReservesDelta variable accordingly. The issue has been fixed in PR 766 and has been verified by Spearbit, but it may be confusing to read the code without understanding this change.

### Original Finding Content

## Severity: Medium Risk

## Context
HyperdriveLong.sol#L435-L470

## Description
The `_calculateOpenLong` function first computes fees on the bond amount that is paid out to the trader. The governance fee measured in bonds is removed from the bond reserves, then converted to a vault shares amount, and again removed from the share reserves. The governance fees are essentially removed twice, once from the bond and once from the share reserves. This means the LPs are effectively paying twice for it.

## Recommendation
Consider only removing the governance fees from the share reserves. We can imagine this as governance swapping the fees that were taken as bonds to shares. For this, the governance fees need to be removed from the `bondReservesDelta` variable (because `y - dy` will mean that it is added back to the bond reserves).

```solidity
- bondReservesDelta = bondProceeds + governanceCurveFee;
+ bondReservesDelta = bondProceeds;
```

## DELV
Fixed in PR 766.

## Spearbit
Verified. The `_bondProceeds` are now the same as `_bondReservesDelta`, which simplifies some of the code (but also makes reading the code a little confusing if you don't have that insight).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Hyperdrive February 2024 |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Christoph Michel, Deivitto, M4rio.eth |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf

### Keywords for Search

`vulnerability`

