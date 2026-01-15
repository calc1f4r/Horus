---
# Core Classification
protocol: Index
chain: everychain
category: oracle
vulnerability_type: stale_price

# Attack Vector Details
attack_type: stale_price
affected_component: oracle

# Source Information
source: solodit
solodit_id: 20220
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/81
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-Index-judging/issues/296

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
  - stale_price
  - chainlink

# Audit Details
report_date: unknown
finders_count: 30
finders:
  - 0xStalin
  - volodya
  - 0xGoodess
  - jasonxiale
  - warRoom
---

## Vulnerability Title

M-6: Chainlink price feed is `deprecated`, not sufficiently validated and can return `stale` prices.

### Overview


This bug report is about an issue found in the Index Coop's AaveLeverageStrategyExtension.sol contract. The issue is that the internal function `_createActionInfo()` uses the deprecated Chainlink latestAnswer function to get the latest price, and this function does not guarantee that the price returned is not stale. The lack of checks to ensure that the return values are valid could lead to wrong calculation of the collateral and borrow prices and other unexpected behavior.

The bug was found by the team of 0x007, 0x8chars, 0xGoodess, 0xStalin, Bauchibred, Bauer, Brenzee, BugBusters, Cryptor, Diana, Madalad, MohammedRizwan, Ocean\_Sky, Oxsadeeq, Phantasmagoria, Saeedalipoor01988, ShadowForce, erictee, jasonxiale, kn0t, kutugu, lil.eth, oxchryston, rvierdiiev, saidam017, sashik\_eth, shogoki, volodya, warRoom, whitehat.

The bug was fixed by switching to using the `latestRoundData` function and adding a configurable maxPriceAge that is compared against the `updatedAt` value. The source code for the fix can be found in the link https://github.com/IndexCoop/index-coop-smart-contracts/pull/142. The severity of the bug was first marked as high but was later changed to medium due to the fact that the bug does not seem to have any real adverse consequences.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-Index-judging/issues/296 

## Found by 
0x007, 0x8chars, 0xGoodess, 0xStalin, Bauchibred, Bauer, Brenzee, BugBusters, Cryptor, Diana, Madalad, MohammedRizwan, Ocean\_Sky, Oxsadeeq, Phantasmagoria, Saeedalipoor01988, ShadowForce, erictee, jasonxiale, kn0t, kutugu, lil.eth, oxchryston, rvierdiiev, saidam017, sashik\_eth, shogoki, volodya, warRoom, whitehat
## Summary
The function `_createActionInfo()` uses Chainlink's deprecated latestAnswer function, this function also does not guarantee that the price returned by the Chainlink price feed is not stale and there is no additional checks to ensure that the return values are valid.

## Vulnerability Detail

The internal function `_createActionInfo()` uses calls `strategy.collateralPriceOracle.latestAnswer()` and `strategy.borrowPriceOracle.latestAnswer()` that uses Chainlink's deprecated latestAnswer() to get the latest price. However, there is no check for if the return value is a stale data.
```solidity

function _createActionInfo() internal view returns(ActionInfo memory) {
        ActionInfo memory rebalanceInfo;

        // Calculate prices from chainlink. Chainlink returns prices with 8 decimal places, but we need 36 - underlyingDecimals decimal places.
        // This is so that when the underlying amount is multiplied by the received price, the collateral valuation is normalized to 36 decimals.
        // To perform this adjustment, we multiply by 10^(36 - 8 - underlyingDecimals)
        int256 rawCollateralPrice = strategy.collateralPriceOracle.latestAnswer();
        rebalanceInfo.collateralPrice = rawCollateralPrice.toUint256().mul(10 ** strategy.collateralDecimalAdjustment);
        int256 rawBorrowPrice = strategy.borrowPriceOracle.latestAnswer();
        rebalanceInfo.borrowPrice = rawBorrowPrice.toUint256().mul(10 ** strategy.borrowDecimalAdjustment);
// More Code....
}
   
```

## Impact
The function `_createActionInfo()` is used to return important values used throughout the contract, the staleness of the chainlinklink return values will lead to wrong calculation of the collateral and borrow prices and other unexpected behavior.

## Code Snippet
https://github.com/IndexCoop/index-coop-smart-contracts/blob/317dfb677e9738fc990cf69d198358065e8cb595/contracts/adapters/AaveLeverageStrategyExtension.sol#L889

## Tool used

Manual Review

## Recommendation
The `latestRoundData` function should be used instead of the deprecated `latestAnswer` function and add sufficient checks to ensure that the pricefeed is not stale.

```solidity
(uint80 roundId, int256 assetChainlinkPriceInt, , uint256 updatedAt, uint80 answeredInRound) = IPrice(_chainlinkFeed).latestRoundData();
            require(answeredInRound >= roundId, "price is stale");
            require(updatedAt > 0, "round is incomplete");
 ```          




## Discussion

**0xffff11**

Sponsor comments:
```
Good point to switch away from using the deprecated method, which we will look into.
However from this issue it is not clear how / if there is any actual vulnerability resulting from the use of this method.
--
Agree with @ckoopmann , the proposed fix of using latestRoundData() looks reasonable to me
--
I switched to confirmed / disagree with severity as this issue is factually correct and will result in us changing the code, but does not seem to have any real adverse consequences.
```

**0xffff11**

I do believe that this should remain as a medium. Not just for the impact stated by the watson, but also because Chainlink might simply not support it anymore in the future.

**ckoopmann**

Switched to using `latestRoundData` and adding a configurable maxPriceAge that is compared against the `updatedAt` value.
Fixed in:
https://github.com/IndexCoop/index-coop-smart-contracts/pull/142

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Index |
| Report Date | N/A |
| Finders | 0xStalin, volodya, 0xGoodess, jasonxiale, warRoom, Phantasmagoria, lil.eth, whitehat, Cryptor, MohammedRizwan, saidam017, BugBusters, Brenzee, 0x007, Bauer, erictee, Diana, Madalad, oxchryston, Bauchibred, 0x8chars, Ocean\_Sky, Oxsadeeq, kn0t, ShadowForce, kutugu, shogoki, sashik\_eth, rvierdiiev, Saeedalipoor01988 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-Index-judging/issues/296
- **Contest**: https://app.sherlock.xyz/audits/contests/81

### Keywords for Search

`Stale Price, Chainlink`

