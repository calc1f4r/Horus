---
# Core Classification
protocol: Goat Tech
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54278
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/404911dd-3a50-4b63-90d4-e0b9164a34a5
source_link: https://cdn.cantina.xyz/reports/cantina_competition_goat_mar2024.pdf
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
  - ethan
---

## Vulnerability Title

Users can lock funds for less time than the minimum staking duration 

### Overview


This bug report discusses an issue with the staking duration feature. Despite having a minimum staking duration, users are able to lock funds for a shorter period of time than intended. This is due to a flaw in the code that checks for expired locks. The recommended solution is to change the function to check for the minimum staking duration instead of just checking if the remaining duration is greater than zero. The team has confirmed the issue and will fix it soon.

### Original Finding Content

## Analysis of Staking Duration Issue

## Context
(No context files were provided by the reviewer)

## Description
Despite enforcing an explicit minimum staking duration, it is possible for users to lock funds for less time than intended. 

If a user locks funds in an existing position without adding to its duration, the `Controller` checks (in `calMintStakingPower`) that the lock has not expired:

```solidity
// LHelper.sol L34
uint rd = LLocker.restDuration(oldLockData);
// ...
if (lockTime_ == 0) {
    require(rd > 0, "already unlocked");
}
```

It then allows staking to continue without additional checks on the duration. But if `rd` is less than the minimum staking duration, the new funds will only be locked for that arbitrarily short period of time. In contrast, the minimum staking amount is enforced in all cases.

## Recommendation
Rather than requiring that the remaining duration of the position is greater than zero, the function should check that it is greater than the minimum staking duration:

```solidity
// LHelper.sol L23
function calMintStakingPower(
    LLocker.SLock memory oldLockData,
    uint lockAmount_,
    uint lockTime_,
    bool isSelfStake_,
    uint selfStakeAdvantage_,
    uint minDuration_
)
internal
view
returns(uint)
{
    uint rd = LLocker.restDuration(oldLockData);
    // ...
    if (lockTime_ == 0) {
        require(rd > minDuration_, "too little time remaining"); // minDuration_ = 30 days
    }
    // ...
}
```

## Goat
Confirmed. Will fix soon.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Goat Tech |
| Report Date | N/A |
| Finders | ethan |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_goat_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/404911dd-3a50-4b63-90d4-e0b9164a34a5

### Keywords for Search

`vulnerability`

