---
# Core Classification
protocol: Elfi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34792
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/329
source_link: none
github_link: https://github.com/sherlock-audit/2024-05-elfi-protocol-judging/issues/258

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
finders_count: 1
finders:
  - mstpr-brainbot
---

## Vulnerability Title

H-30: Mismatching funding fees can result in the protocol incurring a deficit or insolvency risk

### Overview


This bug report discusses a potential issue with the funding fees in the protocol. It was discovered by a user named mstpr-brainbot and the protocol has acknowledged the issue. The problem occurs when funding fees are calculated and one side is capped while the other side does not receive the adjusted fee. This can result in incorrect funding fees and even lead to insolvency. The report includes a detailed explanation of the calculations and how the discrepancy can occur. It also provides a proof of concept and code snippets for reference. The recommendation is to adjust the funding fees for both parties to be equal. There is also a discussion among users about the design choice and whether this is a valid issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-05-elfi-protocol-judging/issues/258 

The protocol has acknowledged this issue.

## Found by 
mstpr-brainbot
## Summary
When funding fees are calculated if it's high enough it can be capped for one side but the other side would not get the new adjusted funding fee. Result of it can end up for misplayed funding fees and even bad debt in some cases.  
## Vulnerability Detail
Assume there are:
$150 totalLongOpenInterest
$50 totalShortOpenInterest
10 seconds passed since the last interaction

Following the execution in `MarketQueryProcess::getUpdateMarketFundingFeeRate()` the following calculations will be done:

fundingRatePerSecond = 10^^-8

totalFundingFee = 150 * 10 * 10^^-8 =
= 1.5 * 10^^-5

currentLongFundingFeePerQty = 
1.5 * 10^^-5 / 150
= -10^^-7

shortFundingFeePerQtyDelta =  1.5 * 10^^-5 / 50 
3 * 10 ^^-7
Assume the max cap is 2 * 10 ^^-7:
We pick 2*10^-7
= 2*10^^-7

longFundingFeeRate = 
(-10^^-7 * 3600 / 10 )/ 10^^-5
= -3.6

shortFundingFeeRate =
(2*10^^-7 * 3600 / 10) / 10^^-5
= 7.2

For short position that holds 50:
realizedFundingFeeDelta =
50 * 2*10^^-7 =
= 10^^-5

For long position that holds 150:
realizedFundingFeeDelta = 
-150 * 10^^-7 =  
= -1.5 * 10^^-5

As we can observe, longs pay 1.5 and shorts receive 1. There is a discrepancy of 0.5 in funding fees that are not paid to short users.

This discrepancy can lead to insolvency because of how the pool accounts for its total holdings. The pool's total value is calculated as the amount plus `unsettledAmount`, where `unsettledAmount` is essentially the accrued funding fees. If the long's 1.5 fee is accounted for as unsettled, the contract assumes this 1.5 will be paid back to shorts, so the protocol is always counting correctly in the long run. However, this assumption is incorrect because shorts will not receive the 1.5 funding fee; they will only receive 1 in our case. Therefore, the excess "0.5" accounted in the pool's total value is incorrect because it will never be returned by the other party.

**Textual Proof of Concept:**
Assume the pool has 100 baseAmount and 10 unsettledFee, totaling 110 assets. Someone can open positions based on a value of 110, expecting that at the end of the day, when the unsettledFees are settled, 10 assets will be returned to the system. However, if the funding fee for the short party is capped, they will only receive 8 fees instead of 10. Consequently, the pool will incorrectly account for "2" assets.
## Impact
Miscounting of pools total value. Positions that are opened will think there is enough funds but actually these fees will never returned by the other party, resulting a position opened without proper collateral. Hence, high. 
## Code Snippet
https://github.com/sherlock-audit/2024-05-elfi-protocol/blob/8a1a01804a7de7f73a04d794bf6b8104528681ad/elfi-perp-contracts/contracts/process/MarketProcess.sol#L29-L52

https://github.com/sherlock-audit/2024-05-elfi-protocol/blob/8a1a01804a7de7f73a04d794bf6b8104528681ad/elfi-perp-contracts/contracts/process/MarketQueryProcess.sol#L110-L161

https://github.com/sherlock-audit/2024-05-elfi-protocol/blob/8a1a01804a7de7f73a04d794bf6b8104528681ad/elfi-perp-contracts/contracts/process/LpPoolQueryProcess.sol#L110-L145
## Tool used

Manual Review

## Recommendation
If the maximum is picked then adjust the counter party's funding fee accordingly. Always give out the same funding fees for both parties. If longs pays 10 then shorts should receive the 10 and vice versa
https://github.com/sherlock-audit/2024-05-elfi-protocol/blob/8a1a01804a7de7f73a04d794bf6b8104528681ad/elfi-perp-contracts/contracts/process/MarketQueryProcess.sol#L110-L161



## Discussion

**0xELFi02**

Not a issue:
Mechanically, it is neutral in the long term, and the mechanism balances the impact of funding fee imbalances.

**nevillehuang**

@0xELFi02 What exactly is the design choice here that makes it neutral in the long term to balance funding fee imbalance? Since it was not noted in the READ.ME, I believe this issue could be valid

Same comments applies for issue #33, #102, #258

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Elfi |
| Report Date | N/A |
| Finders | mstpr-brainbot |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-05-elfi-protocol-judging/issues/258
- **Contest**: https://app.sherlock.xyz/audits/contests/329

### Keywords for Search

`vulnerability`

