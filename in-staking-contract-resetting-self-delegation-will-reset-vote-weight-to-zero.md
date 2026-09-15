---
# Core Classification
protocol: Templedao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33580
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
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
  - Hans
---

## Vulnerability Title

In staking contract, resetting self delegation will reset vote weight to zero

### Overview


This bug report is about a problem in the `TempleGoldStaking` contract. When a delegate resets their self delegation, the vote weights delegated to them are removed, causing their voting power to start accumulating from zero. This can result in the delegate losing all their voting power if the reset happens right before an epoch ends. To fix this, the stakeTime should not be decreased when resetting self delegation. This issue has been fixed in a recent update by the TempleDAO team and has been verified by Cyfrin.

### Original Finding Content

**Description:** In `TempleGoldStaking` contract, when a delegate resets self delegation, the vote weights delegated to the delegate will be removed by calling `_updateAccountWeight`.
Since zero is passed as new balance parameter, the `stakingTime` of vote weight is reset to zero:
```solidity
// TempleGoldStaking.sol:L580
if (_newBalance == 0) {
    t = 0;
    _lastShares = 0;
}
```

This means that the delegate's vote weight starts accumulating from zero even though the delegate has their own balance, which should not be decreased.

**Impact:** The delegate loses voting power, even becoming zero if resetting self delegation happens right before an epoch ends.

**Recommended Mitigation:** When resetting self delegation, it should not decrease stakeTime so that delegate's voting power remains based on their own balance

**TempleDAO:** Fixed in [PR 1043](https://github.com/TempleDAO/temple/pull/1043)

**Cyfrin:** Verified

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Templedao |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

