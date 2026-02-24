---
# Core Classification
protocol: Numa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45279
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/554
source_link: none
github_link: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/38

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
  - juaan
---

## Vulnerability Title

M-2: OracleUtils.ethLeftSide() is not correct for some tokens, leading to incorrect nuAsset pricing

### Overview


The report discusses a bug found by user juaan in the OracleUtils.ethLeftSide() function. This function is used to determine whether ETH is in the numerator or denominator of a price feed, in order to correctly price paired assets. However, the function is implemented incorrectly and can lead to incorrect pricing of assets in some cases. The root cause is that the function checks the first 3 characters of the price feed's description string and assumes that if they are "ETH", then the numerator is ETH. This is not always true, as there are assets with "ETH" as the first 3 characters that are not actually ETH. This leads to incorrect pricing in the NumaPrinter. The protocol team has stated that this bug could potentially affect any asset with a chainlink and 18 decimals, including currencies, commodities, other cryptocurrencies, and stocks. The proposed solution is to check the first 4 bytes of the description string and only return true if they are the same as "ETH/". This will ensure that the function is always correct. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/38 

## Found by 
juaan

### Summary

[`OracleUtils::ethLeftSide()`](https://github.com/sherlock-audit/2024-12-numa-audit/blob/ae1d7781efb4cb2c3a40c642887ddadeecabb97d/Numa/contracts/libraries/OracleUtils.sol#L261-L270) is used to check whether ETH is in the numerator or the denominator of the price feed, in order to correctly price the paired asset.

The check is implemented incorrectly, causing incorrect pricing of assets in some cases.

### Root Cause

The function [`OracleUtils::ethLeftSide()`](https://github.com/sherlock-audit/2024-12-numa-audit/blob/ae1d7781efb4cb2c3a40c642887ddadeecabb97d/Numa/contracts/libraries/OracleUtils.sol#L261-L270) checks the first 3 characters of the pricefeed’s description string, and checks if they are “ETH”. If so, it assumes that the numerator is ETH. 

The issue is that there are assets which have “ETH” as the first 3 characters, but are not ETH. An example is the LST, Stader ETHx. 

It has a [price feed on Arbitrum Mainnet](https://data.chain.link/feeds/arbitrum/mainnet/ethx-eth-exchange-rate), denominated in ETH, with the description string “ETHx/ETH”.

Even though ETH is on the right side, the `ethLeftSide()` function will return `true`, which is incorrect.

This causes the asset to be priced incorrectly in the `NumaPrinter`, since it assumes that the asset is ETH.

Note: the protocol team has [stated](https://discord.com/channels/812037309376495636/1315694506754048023/1318110286372409415):
> This **should be able to theoretically mint any asset with a chainlink (18 decimals)**, including RWA assets.

> This could be assets like currencies (nuUSD, nuEUR, etc), commodities (nuGOLD, nuOIL, etc), **other cryptocurrencies** (nuETH, nuBTC), and stocks (nuTSLA, nuNVDA, etc)

### Internal pre-conditions

An asset like ETHx is used as a nuAsset

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

nuAssets can be priced incorrectly in some cases

### PoC

_No response_

### Mitigation

Check the first 4 bytes of the pricefeed's description string, and return true only if the first 4 bytes are the same as “ETH/”
This ensures that the function is always correct

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Numa |
| Report Date | N/A |
| Finders | juaan |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-12-numa-audit-judging/issues/38
- **Contest**: https://app.sherlock.xyz/audits/contests/554

### Keywords for Search

`vulnerability`

