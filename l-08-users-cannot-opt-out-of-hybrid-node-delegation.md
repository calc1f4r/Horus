---
# Core Classification
protocol: BOB-Staking_2025-10-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63731
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/BOB-Staking-security-review_2025-10-18.md
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

[L-08] Users cannot opt out of hybrid node delegation

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

The `BobStaking::alterHybridNodeDelegatee` function prevents users from opting out of hybrid node delegation by enforcing whitelist validation on all new delegatee addresses, including `address(0)`:

```solidity
function alterHybridNodeDelegatee(address newDelegatee) external nonReentrant {
    Staker storage staker = stakers[_stakeMsgSender()];
    if (staker.hybridNodeDelegatee == newDelegatee) revert DelegateeUnchanged();
    if (staker.amountStaked == 0) revert ZeroTokenStake();

    StakingCondition storage condition = stakingConditions[nextConditionId - 1];
    if (!condition.whitelistedHybridNodeDelegatees.contains(newDelegatee)) revert DelegateeNotWhitelisted();

    _updateUnclaimedRewardsForStaker(_stakeMsgSender());

    staker.hybridNodeDelegatee = newDelegatee;

    emit HybridNodeDelegateeAltered(_stakeMsgSender(), newDelegatee);
}
```

Since `address(0)` will never be included in the whitelist, users who have set a hybrid node delegatee cannot reset it to receive only base staking rewards. Once a user opts into hybrid node delegation, they are permanently forced to delegate to one of the whitelisted nodes, even if they prefer to stop participating in this reward mechanism.

**Recommendations**

In `alterHybridNodeDelegatee`, consider allowing `address(0)` as a valid parameter to enable users to opt out.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | BOB-Staking_2025-10-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/BOB-Staking-security-review_2025-10-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

