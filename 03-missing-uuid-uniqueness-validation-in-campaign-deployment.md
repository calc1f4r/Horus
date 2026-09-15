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
solodit_id: 55724
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

[03] Missing UUID uniqueness validation in campaign deployment

### Overview

See description below for full details.

### Original Finding Content


The NudgeCampaignFactory does not validate the uniqueness of campaign UUIDs during deployment, potentially allowing multiple campaigns with the same identifier.

### Vulnerability Details

When deploying campaigns through `deployCampaign` and `deployAndFundCampaign` functions, there is no check to ensure that the provided `uuid` parameter is unique across all campaigns. This could lead to multiple campaigns sharing the same identifier.

While the CREATE2 deployment pattern ensures unique contract addresses due to other parameters in the salt calculation, having unique UUID’s is important for off-chain tracking and integration systems that may rely on these identifiers.

### Impact

* Multiple campaigns could share the same UUID, causing confusion in off-chain systems.
* Could lead to errors in campaign tracking or analytics that rely on UUID uniqueness.
* May impact integrations with external systems that expect UUIDs to be unique identifiers.

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

    // No validation that uuid is unique
    // ...
}
```

### Recommended mitigation steps

Implement a mapping to track used UUIDs and add a validation check in campaign deployment functions:
```

// Add to contract state variables
mapping(uint256 => bool) public usedUUIDs;

// Add to deployCampaign function
if (usedUUIDs[uuid]) revert DuplicateUUID();
usedUUIDs[uuid] = true;
```

Also, add the corresponding error definition:
```

error DuplicateUUID();
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

