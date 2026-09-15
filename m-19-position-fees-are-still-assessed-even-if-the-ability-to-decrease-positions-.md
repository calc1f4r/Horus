---
# Core Classification
protocol: GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18666
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/6
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-gmx-judging/issues/157

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

M-19: Position fees are still assessed even if the ability to decrease positions is disabled

### Overview


This bug report is regarding an issue with position fees still being assessed even if the ability to decrease positions is disabled. This was found by IllIllI and manually reviewed. The impact of this bug is that users will be assessed position fees even if they wished to close their positions, and can be liquidated through no fault of their own. The code snippet shows that order creation and execution may be disabled, but position fees are tracked based on time and do not account for pauses. The recommendation is to track and account for disabling, and adjust position fees based on whether things were paused or not. However, it was decided that the additional complexity is not worth adding for this case.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-gmx-judging/issues/157 

## Found by 
IllIllI

## Summary

Position fees (borrowing and funding) are still assessed even if the ability to decrease positions is disabled


## Vulnerability Detail

Config keepers have the ability to disable order placement and order execution, and them doing so does not pause the state of position fees.


## Impact

Users will be assessed position fees even if they wished to close their positions, and can be liquidated through no fault of their own.


## Code Snippet

Order creation (to close a position) may be disabled:
```solidity
// File: gmx-synthetics/contracts/exchange/OrderHandler.sol : OrderHandler.createOrder()   #1

43:           FeatureUtils.validateFeature(dataStore, Keys.createOrderFeatureDisabledKey(address(this), uint256(params.orderType)));
```
https://github.com/sherlock-audit/2023-02-gmx/blob/main/gmx-synthetics/contracts/exchange/OrderHandler.sol#L43


As may execution of orders prior to the disabling of creation:

```solidity
// File: gmx-synthetics/contracts/exchange/OrderHandler.sol : OrderHandler._executeOrder()   #2

207:           FeatureUtils.validateFeature(params.contracts.dataStore, Keys.executeOrderFeatureDisabledKey(address(this), uint256(params.order.orderType())));
```
https://github.com/sherlock-audit/2023-02-gmx/blob/main/gmx-synthetics/contracts/exchange/OrderHandler.sol#L197-L210

But position fees are tracked based on time and do not account for pauses:
```solidity
// File: gmx-synthetics/contracts/market/MarketUtils.sol : MarketUtils.updatedAt   #3

1759        function getSecondsSinceCumulativeBorrowingFactorUpdated(DataStore dataStore, address market, bool isLong) internal view returns (uint256) {
1760            uint256 updatedAt = getCumulativeBorrowingFactorUpdatedAt(dataStore, market, isLong);
1761            if (updatedAt == 0) { return 0; }
1762 @>         return block.timestamp - updatedAt;
1763:       }
```
https://github.com/sherlock-audit/2023-02-gmx/blob/main/gmx-synthetics/contracts/market/MarketUtils.sol#L1759-L1763

```solidity
// File: gmx-synthetics/contracts/market/MarketUtils.sol : MarketUtils.getSecondsSinceFundingUpdated()   #4

1658        function getSecondsSinceFundingUpdated(DataStore dataStore, address market) internal view returns (uint256) {
1659            uint256 updatedAt = dataStore.getUint(Keys.fundingUpdatedAtKey(market));
1660            if (updatedAt == 0) { return 0; }
1661 @>         return block.timestamp - updatedAt;
1662:       }
```
https://github.com/sherlock-audit/2023-02-gmx/blob/main/gmx-synthetics/contracts/market/MarketUtils.sol#L1658-L1662


## Tool used

Manual Review


## Recommendation

Track and account for disabling, and adjust position fees based on whether things were paused or not.




## Discussion

**xvi10**

this is a valid concern, but we do not think this logic should be added

orders should only be disabled if there is an emergency issue, we do not think the additional complexity is worth adding for this case

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | GMX |
| Report Date | N/A |
| Finders | IllIllI |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-gmx-judging/issues/157
- **Contest**: https://app.sherlock.xyz/audits/contests/6

### Keywords for Search

`vulnerability`

