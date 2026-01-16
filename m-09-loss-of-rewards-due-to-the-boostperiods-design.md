---
# Core Classification
protocol: Fyde May
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36414
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review-May.md
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

protocol_categories:
  - yield

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-09] Loss of rewards due to the boostPeriods design

### Overview


This report highlights a bug in the reward calculation process of the Fyde Treasury Liquid Vault. The severity of the bug is high and it has a low likelihood of occurring. The bug affects the calculation of boosted rewards for users who did not claim during the boost periods. This results in users losing out on boosted rewards and only earning based on the normal rate. The report recommends tracking boosted rewards separately from normal rewards per user to ensure fair distribution of rewards.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

`rewardRate()` calculated based on boostPeriods as follows:

```solidity
    for (uint256 i; i < boostPeriods.length; ++i) {
      currTime = currTime - timeInPeriod;
      uint256 nextTimeStamp = // if boostPeriods[i].timeStamp in the past, take the current time
        currTime > boostPeriods[i].timeStamp ? currTime : boostPeriods[i].timeStamp;
      uint256 lastUpdate =
        boostPeriods[i].timeStamp > lastUpdateTime ? boostPeriods[i].timeStamp : lastUpdateTime;
      timeInPeriod = nextTimeStamp - lastUpdate;
      totalTime += timeInPeriod;

      rateMultiplier += timeInPeriod * boostPeriods[i].multiplier;
      if (lastUpdateTime > boostPeriods[i].timeStamp) break;
    }
```

[fRewardsDistributor.sol:L178](https://github.com/FydeTreasury/liquid-vault/blob/6bf1be3dec4b6c9e33929a51bf07539a4ced74f2/src/yield/RewardsDistributor.sol#L178)

If the boostPeriod is in the past, it means expired, therefore, take the current time instead. However, if a user didn't claim during the boost periods, the user would lose the boosted rewards and will earn only based on the normal rate (currentTime - lastUpdateTime).

Please note that, even if the user claims rewards during the boost periods, there will be always some loss. This is because the user can't guarantee to claim the rewards exactly right before the **boostPeriods[i].timeStamp** expires. This issue brings unfairness in terms of reward distribution to the users.

**Recommendations**

Boosted rewards calculation should be tracked independently from normal rewards per user.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Fyde May |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review-May.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

