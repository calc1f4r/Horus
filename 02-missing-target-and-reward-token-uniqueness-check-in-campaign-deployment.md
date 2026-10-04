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
solodit_id: 55723
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

[02] Missing target and reward token uniqueness check in campaign deployment

### Overview

See description below for full details.

### Original Finding Content


The NudgeCampaignFactory contract lacks validation to prevent using the same token address for both the target token and the reward token when deploying campaigns. This could lead to unexpected behavior and confusion for users.

### Vulnerability Details

When deploying a campaign through `deployCampaign` and `deployAndFundCampaign` functions, there is no check to ensure that the `targetToken` and `rewardToken` parameters are different addresses. While both addresses are validated to be non-zero, the contract allows them to be identical.

This could result in a campaign where users are required to hold a token and are rewarded with the same token, potentially creating circular dependency issues or unexpected incentive structures.

### Impact

* Creates confusing incentive mechanisms where the same token is both required for eligibility and given as a reward.
* May result in logical inconsistencies in campaign operations.
* Could lead to unexpected behavior during reward calculations and distributions.
* Diverges from the intended separation of target and reward tokens in the protocol design.

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

    // No check that targetToken != rewardToken
    // ...
}
```

### Recommended mitigation steps

Add a validation check in both `deployCampaign` and `deployAndFundCampaign` functions to ensure the target and reward tokens are different:
```

// Add to deployCampaign function
if (targetToken == rewardToken) revert SameTokenForTargetAndReward();
```

Also, add the corresponding error definition:
```

error SameTokenForTargetAndReward();
```

### References

* [`deployCampaign`](https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgeCampaignFactory.sol# L75-L108)
* [`deployAndFundCampaign`](https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgeCampaignFactory.sol# L118-L164)



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

