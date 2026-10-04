---
# Core Classification
protocol: Harmonixfinance Vesting Hyperliquid
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63986
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarmonixFinance-Vesting-Hyperliquid-Security-Review.md
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
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[M-01] Overflow Risk During Vesting Math with Extremely Large Amount (Owner/Merkle-Builder Data Issue)

### Overview


The report highlights a bug in the `getVestedAmount()` function which has a medium level of severity. The function multiplies the `totalGrantAmount` with two other values, which can lead to an overflow when extreme `amount` values are used. This can cause the function to fail and the user will not be able to claim their vested amount until the root of the problem is fixed. The affected code is located in the `MultiVestingDistributor.sol` file. The team recommends bounding the inputs or using safe scaling methods to avoid the overflow. They have also fixed the issue.

### Original Finding Content


## Severity

Medium Risk

## Description

The `getVestedAmount()` multiplies `totalGrantAmount` by BPS and by elapsed values. With Solidity 0.8 checked math, extreme `amount` values (from the Merkle leaf) can overflow and revert. That bricks `getVestedAmount()` and `claim` for that user until the root is fixed.

## Location of Affected Code

File: [contracts/merkle-distributor/distribution/MultiVestingDistributor.sol](https://github.com/harmonixfi/harmonix-tge/blob/75f7fc4f0126e98dbb772949ee1ac48ecf2e8f23/apps/contracts/contracts/merkle-distributor/distribution/MultiVestingDistributor.sol)

```solidity
function getVestedAmount( uint256 distributionId, uint256 totalGrantAmount ) public view returns (uint256) {
  // code
  tgeAmount = (totalGrantAmount * config.cliffBps) / config.maxBps;
  // code
  linearVested = (totalLinearAmount * elapsedTime) / duration;           // continuous
  linearVested = (totalLinearAmount * periodsPassed) / totalPeriods;     // stepped
  // code
}
```

## Impact

DoS for any user whose leaf encodes an oversized `amount`, they cannot claim or even query vested without revert.

## Recommendation

Bound inputs or use safe scaling:

- Validate `amount` upper-bounds off-chain when building the tree and/or on-chain during creation (e.g., enforce `amount <= MAX_GRANT`).
- Or switch to 512-bit mul/div helpers (e.g., `Math.mulDiv` in OZ) where appropriate to avoid intermediate overflow.

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Harmonixfinance Vesting Hyperliquid |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarmonixFinance-Vesting-Hyperliquid-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

