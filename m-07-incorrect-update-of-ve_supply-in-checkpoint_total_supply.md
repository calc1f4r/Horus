---
# Core Classification
protocol: Hyperstable_2025-02-26
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57798
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-02-26.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-07] Incorrect update of `ve_supply` in `checkpoint_total_supply()`

### Overview


The report describes a bug in the `RewardsDistributor.sol` contract where the `ve_supply[t]` value is not being properly updated. This can be exploited by a malicious user to manipulate reward calculations and steal future distribution rewards. To fix this, the report recommends ensuring that `ve_supply[t]` is only updated when the corresponding week has fully elapsed. The suggested solution involves changing the code in the contract.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

In the `RewardsDistributor.sol` contract, the `checkpoint_total_supply()` function is responsible for storing the total supply at a given time `t` in the `ve_supply[t]` mapping. This value is used for future reward distribution calculations. The relevant code is as follows:

```solidity

File: RewardsDistributor.sol
158:                 ve_supply[t] = FixedPointMathLib.max(uint256(int256(pt.bias - pt.slope * dt)), 0);
```

The `ve_supply[t]` value should only be updated when the week corresponding to time `t` has ended, when `t + 1 weeks <= block.timestamp`. However, the current implementation allows `ve_supply[t]` to be updated incorrectly when `block.timestamp % 1` weeks is zero.

This creates a vulnerability where the balance of a newly created `vePeg` NFT (created immediately after `checkpoint_total_supply()` is called) is not accounted for in `ve_supply[t]`.
A malicious user could exploit this flaw to manipulate reward calculations and steal future distribution rewards.

This will lead to reward manipulation. A malicious actor could create a `vePeg` NFT at a specific time to exclude its balance from `ve_supply[t]`, leading to incorrect reward distributions.

## Recommendations

To mitigate this issue, ensure that `ve_supply[t]` is only updated when the week corresponding to time `t` has fully elapsed. This can be achieved by:

```diff
File: RewardsDistributor.sol

         for (uint256 i = 0; i < 20; i++) {
-             if (t > rounded_timestamp) {
+             if (t >= rounded_timestamp)
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperstable_2025-02-26 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperstable-security-review_2025-02-26.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

