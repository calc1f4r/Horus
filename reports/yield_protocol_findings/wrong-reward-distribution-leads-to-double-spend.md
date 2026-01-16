---
# Core Classification
protocol: Staking-Module
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51959
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/bonzo/staking-module
source_link: https://www.halborn.com/audits/bonzo/staking-module
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
  - Halborn
---

## Vulnerability Title

Wrong Reward Distribution Leads to Double Spend

### Overview


The `AaveIncentivesController` contract has a bug where rewards are being transferred twice, causing financial loss to the rewards vault and doubling the rewards for the claimant. To fix this, the rewards should be transferred to the contract's address first and then to the recipient. Additionally, proper approvals should be set up for the `IWHBAR` contract. This has been solved by the Bonzo team and the issue can be found in the AaveIncentivesController.sol file.

### Original Finding Content

##### Description

The `AaveIncentivesController` contract has a vulnerability that results in double spending of rewards. The issue occurs in the `claimRewards` function, where the contract transfers rewards both as `REWARD_TOKEN` and as `IWHBAR`. Specifically, the contract transfers the reward amount to the recipient twice, once via `REWARD_TOKEN.transferFrom(REWARDS_VAULT, to, amountToClaim)` and again via `IWHBAR(_whbarContract).withdraw(REWARDS_VAULT, to, amountToClaim)`.

This leads to the recipient receiving the reward amount twice, causing financial loss to the rewards vault and effectively doubling the rewards for the claimant.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:C/D:C/Y:C/R:P/S:C (9.4)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:C/D:C/Y:C/R:P/S:C)

##### Recommendation

To fix this issue, the rewards should first be transferred to the contract's address and then transferred to the recipient. Additionally, proper approvals should be set up for the `IWHBAR` contract to transfer the reward amounts.

By implementing this change, the rewards will be correctly transferred to the recipient only once, and the risk of double spending will be mitigated. Additionally, ensure that the `REWARD_TOKEN` has been approved for spending by the `IWHBAR` contract to facilitate the withdrawal. This approach prevents financial loss and maintains the integrity of the rewards' distribution.

### Remediation Plan

**SOLVED:** The **Bonzo team** solved this issue as recommended. The `REWARDS_VAULT` will require to approve `AaveIncentivesController` to spend the `_whbarContract` tokens.

##### Remediation Hash

b1b269852a55fd7a2456b5d802054ba61ddffd8f

##### References

AaveIncentivesController.sol#169-170

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Staking-Module |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/bonzo/staking-module
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/bonzo/staking-module

### Keywords for Search

`vulnerability`

