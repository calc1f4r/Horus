---
# Core Classification
protocol: Buck Labs: Smart Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64672
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Strong-DAO-Spearbit-Security-Review-December-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Strong-DAO-Spearbit-Security-Review-December-2025.pdf
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
finders_count: 2
finders:
  - R0bert
  - ChinmayFarkya
---

## Vulnerability Title

CAP price uses maximum of oracle and collateral ratio instead of minimum

### Overview

See description below for full details.

### Original Finding Content

## Severity: Medium Risk

## Context
(No context files were provided by the reviewer)

## Description
The `getCAPPrice()` function in `PolicyManager.sol` determines the collateral-aware peg (CAP) price by using `Math.max(oraclePrice, cr)` during undercollateralized conditions (CR < 1.0). 

In situations where the protocol is undercollateralized (CR < 1.0), the current code chooses the greater of the oracle price and the collateral ratio:

```solidity
if (oracleHealthy) {
    // Oracle is healthy, use max(oracle, CR) per architecture
    (uint256 oraclePrice,) = IOracleAdapter(oracleAdapter).latestPrice();
    rawCAP = Math.max(oraclePrice, cr);
}
```

This leads the protocol to always present users with the "best" price rather than a conservative estimate, potentially enabling value extraction if either data source becomes compromised or corrupted.

## Recommendation
Replace `Math.max` with `Math.min` to use the more conservative price source:

```solidity
if (oracleHealthy) {
    // Oracle is healthy, use min(oracle, CR) for conservative pricing
    (uint256 oraclePrice,) = IOracleAdapter(oracleAdapter).latestPrice();
    rawCAP = Math.min(oraclePrice, cr);
}
```

This ensures that even if one data source is compromised or erroneous, the protocol uses the lower (more conservative) price to protect reserves. The min-of-sources approach is a standard safety pattern in DeFi pricing oracles, as it prevents exploitation when any single price feed becomes unreliable.

## Buck Labs
Acknowledged. There is a very good chance we switch to min instead of max with v2, but for this contract set and our initial launch, we're going to go with max. If oracle shows 0.95 but CR is 0.60, using 0.95 penalizes users beyond what the market believes the backing is worth. Or vice versa.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Buck Labs: Smart Contracts |
| Report Date | N/A |
| Finders | R0bert, ChinmayFarkya |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Strong-DAO-Spearbit-Security-Review-December-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Strong-DAO-Spearbit-Security-Review-December-2025.pdf

### Keywords for Search

`vulnerability`

