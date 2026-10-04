---
# Core Classification
protocol: Nudge.xyz
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55726
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-03-nudgexyz
source_link: https://code4rena.com/reports/2025-03-nudgexyz
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
finders_count: 0
finders:
---

## Vulnerability Title

[05] Missing `rewardPPQ` validation in campaign deployment functions

### Overview

See description below for full details.

### Original Finding Content


The `deployCampaign` and `deployAndFundCampaign` functions in the NudgeCampaignFactory contract do not validate that the `rewardPPQ` parameter is greater than zero and less than `PPQ_DENOMINATOR`; potentially allowing campaigns to be created with zero or excessive rewards.

### Vulnerability Details

The `rewardPPQ` parameter represents the reward factor in parts per quadrillion (PPQ) used to calculate campaign rewards. This critical parameter lacks validation in both deployment functions.

When `rewardPPQ` is zero, the campaign would function normally but would never distribute any rewards to participants, as the reward calculation would always result in zero. This creates a dysfunctional campaign that contradicts the core purpose of the protocol.

Additionally, if `rewardPPQ` is equal to or greater than `PPQ_DENOMINATOR` (`1e15`), rewards would be equal to or greater than the original amount allocated, which could lead to excessive and potentially unsustainable reward distributions.

### Impact

* Campaigns could be deployed with zero reward rates, resulting in users participating but receiving no rewards.
* Campaigns could be deployed with excessively high reward rates (`≥100%`), leading to potentially unsustainable economic models.
* Creates potential for misleading campaigns where users participate expecting reasonable rewards but receive none or excessive amounts.
* Could damage user trust in the protocol if users don’t understand why they aren’t receiving expected rewards.
* Wastes gas and resources on campaigns that don’t fulfill their intended purpose.

### Proof of Concept

In NudgeCampaignFactory.sol:
```

function deployCampaign(
    uint32 holdingPeriodInSeconds,
    address targetToken,
    address rewardToken,
    uint256 rewardPPQ,
    address campaignAdmin,
    uint256 startTimestamp,
    address alternativeWithdrawalAddress,
    uint256 uuid
) public returns (address campaign) {
    if (campaignAdmin == address(0)) revert ZeroAddress();
    if (targetToken == address(0) || rewardToken == address(0)) revert ZeroAddress();
    if (holdingPeriodInSeconds == 0) revert InvalidParameter();

    // No validation that rewardPPQ > 0 and rewardPPQ < PPQ_DENOMINATOR
    // ...
}
```

The impact can be seen in NudgeCampaign.sol where rewards are calculated:
```

function getRewardAmountIncludingFees(uint256 toAmount) public view returns (uint256) {
    // If rewardPPQ is 0, this will always return 0 rewards
    // If rewardPPQ >= PPQ_DENOMINATOR (1e15), rewards will be >= 100% of toAmount
    return toAmount.mulDiv(rewardPPQ, PPQ_DENOMINATOR);
}
```

### Recommended mitigation steps

Add validation checks in both campaign deployment functions to ensure the reward rate is within valid bounds:
```

// Add to deployCampaign function
if (rewardPPQ == 0) revert ZeroRewardRate();
if (rewardPPQ >= PPQ_DENOMINATOR) revert ExcessiveRewardRate();
```

Also, add the corresponding error definitions:
```

error ZeroRewardRate();
error ExcessiveRewardRate();
```

### References

* [`deployCampaign`](https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgeCampaignFactory.sol# L75-L108)
* [`deployAndFundCampaign`](https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgeCampaignFactory.sol# L118-L164)
* [`getRewardAmountIncludingFees`](https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgeCampaign.sol# L162-L175)
* [`PPQ_DENOMINATOR` definition](https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgeCampaign.sol# L26)



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Nudge.xyz |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-03-nudgexyz
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-03-nudgexyz

### Keywords for Search

`vulnerability`

