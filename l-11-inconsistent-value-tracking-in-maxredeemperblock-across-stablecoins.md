---
# Core Classification
protocol: Level_2025-04-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63753
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Level-security-review_2025-04-09.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-11] Inconsistent value tracking in `maxRedeemPerBlock` across stablecoins

### Overview

See description below for full details.

### Original Finding Content


The `maxRedeemPerBlock` limit tracks collateral amounts (USDC/USDT) rather than the actual `lvlUSD` value being redeemed. Since stablecoins can deviate from their peg (e.g., USDC at $0.99 and USDT at $1.01), this creates inconsistencies in the actual `lvlUSD` value being limited. A user redeeming through USDT when it's above peg could redeem 1-2% more `lvlUSD` value compared to someone using USDC when it's below peg, while both would be counted the same against the `maxRedeemPerBlock` limit.

```solidity
        uint256 collateralAmount = computeRedeem(asset, lvlUsdAmount);
        if (collateralAmount < expectedAmount) revert MinimumCollateralAmountNotMet();

@>        pendingRedemption[msg.sender][asset] += collateralAmount;
```

Consider tracking and limiting the `lvlUSD` value being redeemed instead of the raw collateral amount to ensure consistent value limits across different collateral types.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Level_2025-04-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Level-security-review_2025-04-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

