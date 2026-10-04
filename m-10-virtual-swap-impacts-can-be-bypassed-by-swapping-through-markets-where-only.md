---
# Core Classification
protocol: GMX Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18805
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/74
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-gmx-judging/issues/257

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
  - IllIllI
---

## Vulnerability Title

M-10: Virtual swap impacts can be bypassed by swapping through markets where only one of the collateral tokens has virtual inventory

### Overview


This bug report deals with virtual swap impacts being bypassed by swapping through markets where only one of the collateral tokens has virtual inventory. This vulnerability was found by IllIllI and the impact of it is that if the virtual swap amount for a particular token is very large, a user can split their large order into multiple smaller orders, and route them through other markets where there is no virtual token for one of the pools, and avoid the fees. The code snippet shows that virtual impacts are completely skipped if one of the tokens doesn't have a virtual version. The tool used to find this vulnerability was manual review. The recommendation to fix this issue is to use the non-virtual token's inventory as the standin for the missing virtual inventory token.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-gmx-judging/issues/257 

## Found by 
IllIllI
## Summary

Virtual swap impacts can be bypassed by swapping through markets where only one of the collateral tokens has virtual inventory


## Vulnerability Detail

The code that calculates price impacts related to swapping, skips the application of virtual impacts if one of the tokens doesn't have a virtual token set


## Impact

If the virtual swap amount for a particular token is very large, and a large swap through that market would cause the balance to drop a lot, causing the trade to have a large negative impact, a user can split their large order into multiple smaller orders, and route them through other markets where there is no virtual token for one of the pools, and avoid the fees (assuming those pools have non-virtual imbalances that favor such a trade).


## Code Snippet

Virtual impacts are completely skipped if one of the tokens doesn't have a virtual version:
```solidity
// File: gmx-synthetics/contracts/pricing/SwapPricingUtils.sol : SwapPricingUtils.getPriceImpactUsd()   #1

113            (bool hasVirtualInventoryTokenB, uint256 virtualPoolAmountForTokenB) = MarketUtils.getVirtualInventoryForSwaps(
114                params.dataStore,
115                params.market.marketToken,
116                params.tokenB
117            );
118    
119            if (!hasVirtualInventoryTokenA || !hasVirtualInventoryTokenB) {
120 @>             return priceImpactUsd;
121:           }
```
https://github.com/sherlock-audit/2023-04-gmx/blob/main/gmx-synthetics/contracts/pricing/SwapPricingUtils.sol#L113-L121


## Tool used

Manual Review


## Recommendation

Use the non-virtual token's inventory as the standin for the missing virtual inventory token

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | GMX Update |
| Report Date | N/A |
| Finders | IllIllI |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-gmx-judging/issues/257
- **Contest**: https://app.sherlock.xyz/audits/contests/74

### Keywords for Search

`vulnerability`

