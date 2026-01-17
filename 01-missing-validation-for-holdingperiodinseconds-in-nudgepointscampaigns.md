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
solodit_id: 55722
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

[01] Missing validation for `holdingPeriodInSeconds` in `NudgePointsCampaigns`

### Overview

See description below for full details.

### Original Finding Content


The `holdingPeriodInSeconds` parameter lacks validation in both `createPointsCampaign` and `createPointsCampaigns` functions within the `NudgePointsCampaigns` contract, allowing privileged users to create campaigns with a zero holding period. This contradicts the core design principle of the protocol’s token holding incentive mechanism.

### Vulnerability Details

In the `NudgePointsCampaigns` contract, the protocol validates the `targetToken` parameter but fails to validate whether the `holdingPeriodInSeconds` is greater than zero. This oversight allows administrators to create campaigns that don’t enforce any actual holding period.

The `holdingPeriodInSeconds` parameter represents the duration users must hold tokens to qualify for rewards, which is a fundamental mechanic of the protocol’s incentive system. A holding period of 0 seconds essentially bypasses this core requirement.

Affected functions:

* `createPointsCampaign`
* `createPointsCampaigns`

### Impact

If `holdingPeriodInSeconds` is set to 0:

1. Users would immediately qualify for rewards without actually holding tokens for any meaningful duration.
2. This undermines the stated design goal of incentivizing token retention.
3. Creates inconsistent behavior compared to other campaigns where holding periods are enforced.
4. Violates user expectations and the protocol’s documentation which specifically mentions holding periods as a requirement.

While this wouldn’t directly lead to financial loss, it could be exploited to distribute rewards in a manner inconsistent with the protocol’s stated objectives and potentially allow for gaming of the reward mechanism.

### Proof of Concept

In NudgePointsCampaigns.sol, the validation for the `createPointsCampaign` function:
```

function createPointsCampaign(
    uint256 campaignId,
    uint32 holdingPeriodInSeconds,
    address targetToken
) external onlyRole(NUDGE_ADMIN_ROLE) returns (Campaign memory) {
    // Validates target token but not holding period
    if (targetToken == address(0)) {
        revert InvalidTargetToken();
    }

    // No validation for holdingPeriodInSeconds == 0

    if (campaigns[campaignId].targetToken != address(0)) {
        revert CampaignAlreadyExists();
    }

    // Creates the campaign regardless of holdingPeriodInSeconds value
    campaigns[campaignId] = Campaign({
        targetToken: targetToken,
        totalReallocatedAmount: 0,
        holdingPeriodInSeconds: holdingPeriodInSeconds,
        pID: 0
    });

    emit PointsCampaignCreated(campaignId, holdingPeriodInSeconds, targetToken);
    return campaigns[campaignId];
}
```

Similarly, in the `createPointsCampaigns` function (lines 86-105), batch campaign creation has the same validation gap.

### Recommended mitigation steps

Add validation for `holdingPeriodInSeconds` in both functions to ensure it’s greater than zero:

For `createPointsCampaign`:
```

function createPointsCampaign(
    uint256 campaignId,
    uint32 holdingPeriodInSeconds,
    address targetToken
) external onlyRole(NUDGE_ADMIN_ROLE) returns (Campaign memory) {
    if (targetToken == address(0)) {
        revert InvalidTargetToken();
    }

    // Add validation for holding period
    if (holdingPeriodInSeconds == 0) {
        revert InvalidHoldingPeriod();
    }

    if (campaigns[campaignId].targetToken != address(0)) {
        revert CampaignAlreadyExists();
    }

    campaigns[campaignId] = Campaign({
        targetToken: targetToken,
        totalReallocatedAmount: 0,
        holdingPeriodInSeconds: holdingPeriodInSeconds,
        pID: 0
    });

    emit PointsCampaignCreated(campaignId, holdingPeriodInSeconds, targetToken);
    return campaigns[campaignId];
}
```

For `createPointsCampaigns`:
```

function createPointsCampaigns(
    uint256[] calldata campaignIds,
    uint32[] calldata holdingPeriodsInSeconds,
    address[] calldata targetTokens
) external onlyRole(NUDGE_ADMIN_ROLE) returns (Campaign[] memory) {
    for (uint256 i = 0; i < campaignIds.length; i++) {
        if (targetTokens[i] == address(0)) {
            revert InvalidTargetToken();
        }

        // Add validation for holding period
        if (holdingPeriodsInSeconds[i] == 0) {
            revert InvalidHoldingPeriod();
        }

        if (campaigns[campaignIds[i]].targetToken != address(0)) {
            revert CampaignAlreadyExists();
        }

        campaigns[campaignIds[i]] = Campaign({
            targetToken: targetTokens[i],
            totalReallocatedAmount: 0,
            holdingPeriodInSeconds: holdingPeriodsInSeconds[i],
            pID: 0
        });

        emit PointsCampaignCreated(campaignIds[i], holdingPeriodsInSeconds[i], targetTokens[i]);
    }

    return campaigns;
}
```

Also, add the custom error definition at the contract level:
```

error InvalidHoldingPeriod();
```

### References

* NudgeCampaignFactory.sol implements similar validation in line 80: `if (holdingPeriodInSeconds == 0) revert InvalidParameter();`
* [`createPointsCampaign`](https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgePointsCampaigns.sol# L58)
* [`createPointsCampaigns`](https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgePointsCampaigns.sol# L98)



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

