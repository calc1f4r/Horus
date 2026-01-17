---
# Core Classification
protocol: Liquorice
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49455
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#15-repositorysetliquidationthreshold-can-unexpectedly-change-the-global-defaultconfigliquidationthreshold-when-setting-an-isolated-threshold-for-a-specific-asset
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
  - MixBytes
---

## Vulnerability Title

`Repository.setLiquidationThreshold()` can unexpectedly change the global `defaultConfig.liquidationThreshold` when setting an isolated threshold for a specific asset.

### Overview


The report discusses a bug in a protocol where changing the threshold for a specific asset can also change the threshold for all default tokens, which can lead to bad debt if volatile tokens are assigned a high threshold. This can happen because the higher the liquidation threshold for an asset, the later users will be liquidated. The report recommends modifying the default liquidation threshold only through a dedicated function and setting a minimum threshold to prevent centralization risks.

### Original Finding Content

##### Description

When changing the threshold for a specific asset, the threshold for all default tokens may also change in a way that is unfavorable for the protocol:
- https://github.com/Liquorice-HQ/contracts/blob/6100e3f6406b1f8a4cadd222870e6ed370f1f8c5/src/contracts/Repository.sol#L288-L290

This can lead to bad debt if volatile tokens are assigned a high threshold.

The higher the liquidation threshold for an asset, the later users will be liquidated. As a result, if there are two assets—one low-volatility and one high-volatility—and the high-volatility asset uses the default config, then a reasonable increase in the threshold for the low-volatility asset will also increase the threshold for the high-volatility asset. This may be unexpected for the manager and could lead to the accumulation of bad debt.

##### Recommendation

We recommend modifying the default liquidation threshold only via a dedicated function.

Additionally, to prevent centralization risks, we also recommend setting a constant minimum liquidation threshold so that the admin cannot set it to 0 and liquidate all participants.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Liquorice |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#15-repositorysetliquidationthreshold-can-unexpectedly-change-the-global-defaultconfigliquidationthreshold-when-setting-an-isolated-threshold-for-a-specific-asset
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

