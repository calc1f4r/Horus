---
# Core Classification
protocol: Aave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19264
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/aave/aave-v3/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/aave/aave-v3/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

User’s Borrowing Status is not Updated When Their Entire Debt is Liquidated

### Overview

See description below for full details.

### Original Finding Content

## Description
When a user has a position that no longer satisfies the required ratio of collateral-to-debt, that user may be liquidated via the function `liquidationCall()`. If the user’s position breaches a certain threshold, the entire position may be liquidated in one transaction.

If the entire debt of a user is liquidated for an asset, the user should no longer be considered borrowing. However, the function `executeLiquidationCall()` will not change the borrowing status for a user. The impact is that a user may have no debt for an asset but still be marked as borrowing if their entire debt is liquidated.

## Recommendations
We recommend updating a user’s borrowing status to be false for the asset if their entire debt balance was liquidated.

## Resolution
The issue has been resolved in PR#556 by adding the following statement, which checks if the entire debt balance is liquidated.

```javascript
if ( vars.userTotalDebt == vars.actualDebtToLiquidate ) {
    userConfig.setBorrowing(debtReserve.id, false);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Aave |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/aave/aave-v3/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/aave/aave-v3/review.pdf

### Keywords for Search

`vulnerability`

