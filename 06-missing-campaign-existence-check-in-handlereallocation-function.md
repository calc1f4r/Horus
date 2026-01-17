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
solodit_id: 55727
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

[06] Missing campaign existence check in `handleReallocation` function

### Overview

See description below for full details.

### Original Finding Content


The `handleReallocation` function in the NudgePointsCampaigns contract does not validate whether the specified campaign exists before proceeding with operations. This oversight allows interaction with non-existent campaigns, potentially leading to silent failures.

### Vulnerability Details

In the NudgePointsCampaigns contract, when the `handleReallocation` function is called with a non-existent campaign ID, it retrieves a default empty Campaign struct with zero values. The function then proceeds with operations on this empty struct instead of reverting.

The absence of an existence check means:

* The function continues execution with default values for campaign parameters.
* This will result in a silent failure while transferring tokens.

### Proof of Concept

In NudgePointsCampaigns.sol, the `handleReallocation` function loads the campaign without verifying its existence:
```

function handleReallocation(
    uint256 campaignId,
    address userAddress,
    address toToken,
    uint256 toAmount,
    bytes calldata data
) external payable whenNotPaused(campaignId) onlyRole(SWAP_CALLER_ROLE) {
    Campaign storage campaign = campaigns[campaignId];

    // No validation that campaign exists!

    if (toToken != campaign.targetToken) {
        revert InvalidToTokenReceived(toToken);
    }

    // If campaign doesn't exist, campaign.targetToken will be address(0)
    // Further operations would use default zero values
    // ...
}
```

### Recommended mitigation steps

Add a validation check at the beginning of the function to ensure the campaign exists:
```

function handleReallocation(
    uint256 campaignId,
    address userAddress,
    address toToken,
    uint256 toAmount,
    bytes calldata data
) external payable whenNotPaused(campaignId) onlyRole(SWAP_CALLER_ROLE) {
    Campaign storage campaign = campaigns[campaignId];

    // Verify the campaign exists before proceeding
    if (campaign.targetToken == address(0)) {
        revert CampaignDoesNotExist();
    }

    if (toToken != campaign.targetToken) {
        revert InvalidToTokenReceived(toToken);
    }

    // Continue with existing implementation
    // ...
}
```

This check uses the same pattern established in other parts of the codebase, where a campaign’s existence is determined by its targetToken being non-zero.

### References

[`handleReallocation`](https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgePointsCampaigns.sol# L127-L155)



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

