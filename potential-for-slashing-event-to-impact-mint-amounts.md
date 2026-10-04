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
solodit_id: 35988
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/kelp/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Potential For Slashing Event To Impact Mint Amounts

### Overview

See description below for full details.

### Original Finding Content

## Description

The accuracy of the `rsETHPrice` calculated by `lrtOracle.rsETHPrice` in the `LRTDepositPool` contract is dependent on frequent updates via `LRTOracle.updateRSETHPrice()`. There are two instances where a change in price can occur:

1. EigenLayer or staking rewards distribution
2. A mass slashing event

Currently, there is no incentive for third parties to call `LRTOracle.updateRSETHPrice()` due to gas costs. The Kelp team’s intended approach of updating the `rsETH` price once or twice per day, in practice, is adequate for accounting for price increases from staking and EigenLayer rewards, assuming EigenLayer rewards are distributed in a linear fashion similar to staking rewards throughout the year. However, it may not be timely enough to account for any mass slashing event. If such an event occurs, minters will receive less than their fair share of `rsETH` until such time that `LRTOracle.updateRSETHPrice()` is called.

## Recommendations

- Consider automatically calling `updateRSETHPrice()` within the `getRsETHAmountToMint()` function to ensure the `rsETH` price is always current before minting.
- Alternatively, monitor EigenLayer rewards distribution to ensure they follow similar distribution patterns as ETH staking rewards so that, in practice, there is no profitable incentive to frontrun any reward distribution.
- If the gas trade-off is deemed to be not worthwhile for minting, consider calling `updateRSETHPrice()` automatically when implementing future withdraw functionality to prevent any frontrunning and potential insolvency.

## Resolution

The issue was acknowledged by the project team providing the following comment as to why the issue does not need to be fixed:

"The reason we do not update exchange rate on an asset deposit is because it increases gas cost to end user. With the slow change of LST/LRT exchange rate, we believe it is practical to rely on exchange rate update twice a day."

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

