---
# Core Classification
protocol: Lizardstarking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20470
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-02-01-LizardStarking.md
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
  - Pashov
---

## Vulnerability Title

[H-01] Users will forever lose their accrued rewards if they call `withdrawStake` before calling `claimReward` first

### Overview


This bug report is about a feature of a smart contract that allows users to stake and withdraw their rewards. The issue is that if a user calls the `withdrawStake` function without first calling `claimReward` for each reward pool, then they will lose all of their unclaimed rewards forever. This can lead to a monetary loss for users. The front-end will enforce the right sequence of calls, however, the Gitbook documentation falsely claims that re-staking will re-gain user's access to their rewards.

Two possible solutions are proposed: the first is to enforce zero unclaimed rewards when a call to `withdrawStake` is made by reverting if there are any such unclaimed rewards; the second is to call `claimReward` in `withdrawStake`. This bug has a medium likelihood of happening and resulting in a monetary value loss for users.

### Original Finding Content

**Impact:**
High, as this will lead to a monetary loss for users

**Likelihood:**
Medium, as even though the front-end will enforce the right sequence of calls, the Gitbook docs falsely claims re-staking will re-gain user's access to their rewards

**Description**

The contract is implemented so that if a user calls `withdrawStake` without first calling `claimReward` for each reward pool then the staker will lose all of his unclaimed rewards forever, they will be locked into the staking contract. While the front-end will enforce the right sequence of calls, the Gitbook docs state that `When un-staked, a user will lose access to all their pending rewards and lose access to future rewards (unless they re-stake)` which gives the impression that you can re-stake and then you will re-gain access to your unclaimed rewards, but this is not the case as the `withdrawStake` method removes the data needed for previous rewards calculation.

Since the docs give a misleading information about they way this mechanism works and also users can interact directly with the smart contract in a bad way for them (when they are not malicious) this has a higher likelihood of happening and resulting a monetary value loss for users.

**Recommendations**

One possible solution is to enforce zero unclaimed rewards when a call to `withdrawStake` is made by reverting if there are any such unclaimed rewards. Another one is to just call `claimReward` in `withdrawStake`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Lizardstarking |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-02-01-LizardStarking.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

