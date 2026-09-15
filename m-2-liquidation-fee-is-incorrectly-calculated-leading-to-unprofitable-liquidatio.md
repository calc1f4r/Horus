---
# Core Classification
protocol: Sentiment V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41296
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/349
source_link: none
github_link: https://github.com/sherlock-audit/2024-08-sentiment-v2-judging/issues/91

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
finders_count: 16
finders:
  - Ryonen
  - X12
  - HHK
  - S3v3ru5
  - ravikiran.web3
---

## Vulnerability Title

M-2: Liquidation fee is incorrectly calculated, leading to unprofitable liquidations

### Overview


This bug report discusses an issue with the calculation of liquidation fees, which is causing liquidations to be unprofitable. The incorrect calculation method is leading to insolvency and bad debt. The root cause is identified as the liquidation fee being taken from the entire amount of collateral instead of from the profit of the liquidator. This results in a majority of liquidations being unprofitable. The correct approach to calculating the fee is proposed, and it is suggested that the profit of the liquidation should be calculated first before applying the fee. This bug has a high severity and is being discussed among multiple individuals.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-08-sentiment-v2-judging/issues/91 

## Found by 
0xKartikgiri00, A2-security, Bigsam, EgisSecurity, HHK, Oblivionis, Obsidian, Ryonen, S3v3ru5, ThePharmacist, X12, ZeroTrust, cryptomoon, hash, nfmelendez, ravikiran.web3
### Summary

Incorrect liquidation fee calculation makes liquidations unprofitable, leading to insolvency.

### Root Cause

During `PositionManager.liquidate()` , two things happen:

1. An amount `x` of the position’s collateral is paid to the liquidator ([link](https://github.com/sherlock-audit/2024-08-sentiment-v2/blob/25a0c8aeaddec273c5318540059165696591ecfb/protocol-v2/src/PositionManager.sol#L438))
2. The liquidator pays off the debt of the position ([link](https://github.com/sherlock-audit/2024-08-sentiment-v2/blob/25a0c8aeaddec273c5318540059165696591ecfb/protocol-v2/src/PositionManager.sol#L439))

During step 1, the liquidation fee is effectively calculated as `liquidationFee.mulDiv(x, 1e18)`

This is incorrect- the correct way would be to take the liquidation fee from the profit of the liquidator, rather than from the entire amount `x`

Due to this inaccuracy, a large majority of liquidations will be unprofitable:

### Example scenario

Consider a situation where liquidation fee is 30% (as stated in the contest README)

Say LTV = 90%, Debt value = $90, Collateral value drops from $100 to $98

Now, since the position LTV (90/98) is greater than the set LTV (90/100), the position is liquidatable

A liquidator aims to pay off the debt and receive the $98 worth of collateral, effectively buying the collateral at a discount of ~8%

However, They will only receive 70% of the $98 (due to the 30% liquidation fee), so they can only receive $68.6

This is extremely unprofitable since they have to pay off $90 worth of debt, and only receive $68.6 as a reward.

### The correct approach to calculating fee would be the following:

1. Calculate liquidator profit = Reward - Cost = $98 - $90 = $8
2. Calculate liquidator fee = feePercentage*profit = 30% of $8  = $2.4

This ensures that liquidations are still incentivised

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

Liquidations are unprofitable due to liquidation fee being calculated incorrectly.

This leads to bad debt and insolvency since there is no incentive to liquidate.

### PoC

_No response_

### Mitigation

Consider calculating the profit of the liquidation first, and take the fee based on that



## Discussion

**0xjuaan**

Hi @cvetanovv I forgot to escalate this (hard to keep track of so many), but I think everyone would agree this is high severity

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Sentiment V2 |
| Report Date | N/A |
| Finders | Ryonen, X12, HHK, S3v3ru5, ravikiran.web3, ZeroTrust, 0xKartikgiri00, hash, Oblivionis, EgisSecurity, Obsidian, ThePharmacist, cryptomoon, A2-security, nfmelendez, Bigsam |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-08-sentiment-v2-judging/issues/91
- **Contest**: https://app.sherlock.xyz/audits/contests/349

### Keywords for Search

`vulnerability`

