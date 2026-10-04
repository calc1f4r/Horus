---
# Core Classification
protocol: Roots_2025-02-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55116
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

[H-06] BGT stake rewards are locked

### Overview


This bug report is about a medium severity issue in the Staker contract. When staking our collateral token to get BGT reward tokens, the BGT contract helps us stake the BGT token into the BGTStaker contract. However, there is a missing interface in the Staker contract to claim the HONEY rewards from staking BGT tokens in the BGTStaker contract. The report recommends adding this interface to the Staker contract to fix the issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** High

## Description

In Staker contract, we will stake our collateral token to get some BGT reward tokens. BGT reward tokens can be boosted. When we boost our BGT token in the staker contract, BGT contract will help us stake our BGT token into BGTStaker contract(https://berascan.com/address/0x44F07Ce5AfeCbCC406e6beFD40cc2998eEb8c7C6).

```solidity
    function _tryToBoost() internal {
            if (queued > 0 && blockDelta > 8191) {
            rewardCache.activateBoost(validator);
        }
```

```solidity
    function activateBoost(address user, bytes calldata pubkey) external returns (bool) {
        IBGTStaker(staker).stake(user, amount);
        return true;
    }
```

When we check BGTStaker's implementation, we stake BGT token into BGT Staker, we can get some HONEY rewards. We can get these rewards via interface `getReward`. But we miss one interface in Staker contract to get this part of rewards.

```solidity
    function getReward() external returns (uint256) {
        return _getReward(msg.sender, msg.sender);
    }
```

## Recommendations

Add one interface in Staker contract to claim this boost rewards.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Roots_2025-02-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Roots-security-review_2025-02-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

