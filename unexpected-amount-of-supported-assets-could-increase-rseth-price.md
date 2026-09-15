---
# Core Classification
protocol: Kelp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35987
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Unexpected Amount of Supported Assets Could Increase rsETH price

### Overview


The bug report discusses a potential issue with the LRTDepositPool and NodeDelegator contracts that could result in an increase in the price of rsETH. This could happen if these contracts receive an unexpected amount of supported assets without the proper function being called. This could be intentional or accidental. The report also describes an attack scenario where a malicious user could manipulate the share price of rsETH by depositing a small amount and then transferring a large amount of assets to the contract. The report recommends implementing a system of internal accounting to track the amount of each supported asset and using an initial mint to mitigate the risk of this issue. The Kelp DAO has resolved this issue by implementing an initial mint after deployment. 

### Original Finding Content

## Description

If, for any reason, the `LRTDepositPool` contract or the `NodeDelegator` contract received an unexpected amount of supported assets, the `rsETH` price would increase. 

The `LRTDepositPool` contract could receive intentionally (from a malicious user) or unintentionally (accidentally) an amount of supported assets without the function `depositAsset()`. Also, the `NodeDelegator` contract could receive an amount of supported assets without calling the function `transferAssetToNodeDelegator()`. 

According to the function `LRTOracle.updateRSETHPrice()`, `rsETHPrice = totalETHInPool / rsEthSupply`. So, if one of the `LRTDepositPool` contracts or the `NodeDelegator` contract receives an unexpected amount of supported assets, the `rsETH` price would increase. This is because when receiving an unexpected amount of supported assets, no new `rsETH` tokens are minted, so the `rsEthSupply` would not increase. However, the total amount of supported assets would increase, and consequently, the `totalETHInPool` would increase.

An attack scenario that can occur is that the first minter can maliciously manipulate the share price to take a profit from future user deposits. This can be done by first depositing the lowest possible amount of supported assets (1 wei) to the deposit pool, and then transferring a large amount of assets to the pool contract directly. This will artificially inflate the share price of `rsETH` for future depositors.

## Recommendations

- Consider using a system of internal accounting to track the amount of each supported asset within the project, so that any excess could be withdrawn.
- A potential solution to the share inflation attack is implementing a decimal offset for virtual shares and assets in the pool. See this link for more details: [Inflation Attacks With Virtual Shares And Assets](<insert-link-here>).
- Alternatively, an initial mint could also be used to mitigate the risk of this issue.

## Resolution

Kelp DAO has elected to resolve this issue using an initial mint immediately after deployment.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Kelp |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf

### Keywords for Search

`vulnerability`

