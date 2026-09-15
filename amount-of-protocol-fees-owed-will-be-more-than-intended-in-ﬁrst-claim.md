---
# Core Classification
protocol: Royco
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46676
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b99b673a-6790-4364-b76b-e8e3202464d2
source_link: https://cdn.cantina.xyz/reports/cantina_royco_august2024.pdf
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
finders_count: 4
finders:
  - Kurt Barry
  - Yorke Rhodes
  - kankodu
  - 0x4non
---

## Vulnerability Title

Amount of protocol fees owed will be more than intended in ﬁrst claim 

### Overview


The bug report mentions an issue with the ERC4626i claimProtocolFees function. The problem occurs when the function is called for the first time for a specific campaignId. The storage value for feeRewardsLastClaimed is set to 0, which causes the time elapsed variable to be assigned to the campaignData.end timestamp. This results in a significantly larger amount owed than intended by the campaign's protocolFeeRate. The recommendation is to assign lastUpdated to campaignData.start when feeRewardsLastClaimed is equal to 0. However, the developers have acknowledged the issue and stated that it will not be fixed as the ERC4626i is being rewritten entirely. 

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
The `ERC4626i` `claimProtocolFees` has the following snippet:

```solidity
CampaignData storage _campaignData = campaignIdToData[campaignId];
uint256 lastUpdated = feeRewardsLastClaimed[campaignId];
uint256 elapsed = (_campaignData.end - lastUpdated);
uint256 amountOwed = (elapsed * _campaignData.protocolFeeRate);
```

The first time this function is called for a given `campaignId`, `feeRewardsLastClaimed[campaignId]` will be `0` (the default value) in storage. This will lead to the `elapsed` variable being assigned to the `_campaignData.end`'s timestamp. As a consequence, the `amountOwed` will be many orders of magnitude larger than the campaign's `protocolFeeRate` intends. This will impact every campaign created upon the first claim.

## Recommendation
When `feeRewardsLastClaimed[campaignId] == 0`, assign `lastUpdated` to `_campaignData.start`, which will set the appropriate floor on time elapsed.

## Responses
**Royco:** Acknowledged. Won't fix: `ERC4626i` is being rewritten entirely.

**Cantina Managed:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Royco |
| Report Date | N/A |
| Finders | Kurt Barry, Yorke Rhodes, kankodu, 0x4non |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_royco_august2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b99b673a-6790-4364-b76b-e8e3202464d2

### Keywords for Search

`vulnerability`

