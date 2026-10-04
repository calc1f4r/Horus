---
# Core Classification
protocol: Beanstalk: The Finale
chain: everychain
category: oracle
vulnerability_type: oracle

# Attack Vector Details
attack_type: oracle
affected_component: oracle

# Source Information
source: solodit
solodit_id: 36221
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n
source_link: none
github_link: https://github.com/Cyfrin/2024-05-beanstalk-the-finale

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
  - oracle

protocol_categories:
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - sohrabhind
  - bladesec
  - joicygiore
  - Draiakoo
  - holydevoti0n
---

## Vulnerability Title

`LibChainlinkOracle::getTokenPrice` will always return instantaneuous prices

### Overview


Summary:

The function `LibChainlinkOracle::getTokenPrice` is supposed to return a price based on a certain time period called `lookback`. However, due to a mistake in the code, the function always returns the instantaneous price, regardless of the `lookback` value. This can lead to unexpected results and needs to be fixed. The recommended solution is to change the conditional statement in the code to correctly return the twap price when `lookback` is greater than 0 and the instantaneous price when `lookback` is equal to 0. Manual review was used to identify this issue. 

### Original Finding Content

## Summary

The `LibChainlinkOracle::getTokenPrice` function has a parameter of `lookback` in order to determine how many seconds ago do we want to obtain the twap of a chainlink price feed. However, this is implemented in a wrong way

## Relevant GitHub Links:
https://github.com/Cyfrin/2024-05-beanstalk-the-finale/blob/main/protocol/contracts/libraries/Oracle/LibChainlinkOracle.sol#L39-L48

## Vulnerability Details

When `LibChainlinkOracle::getTokenPrice` is called, it returns a different price calculation depending on the `lookback` parameter passed to the function:

```Solidity
    function getTokenPrice(
        address priceAggregatorAddress,
        uint256 maxTimeout,
        uint256 lookback
    ) internal view returns (uint256 price) {
        return
            lookback > 0
                ? getPrice(priceAggregatorAddress, maxTimeout)
                : getTwap(priceAggregatorAddress, maxTimeout, lookback);
    }
```

In this case the ternary operator returns the function `getPrice` (instantaneous price) when lookback > 0 and `getTwap` when lookback == 0. As we can see, the conditional for returning the different price computation is wrong because it returns the twap price when lookback = 0, which is basically the instantaneous price and it returns the current price when the lookback parameter is greater than 0, when it should return the twap according to the amount of lookback passed.

The correct behaviour should be that when `lookback` is set to 0, it should return the instantaneous price "`getPrice`" and when it is greater than 0 it should return the "`getTwap`" function passing it the lookback parameter.

## Impact

Medium, no matter what `lookback` will be, the instantaneous price from the chainlink oracle will be returned.

Chainlink is not manipulable but the functionality clearly does not work as intended and can return unexpected results.

## Tools Used

Manual review

## Recommendations

```diff
    function getTokenPrice(
        address priceAggregatorAddress,
        uint256 maxTimeout,
        uint256 lookback
    ) internal view returns (uint256 price) {
        return
-            lookback > 0
+            lookback == 0
                ? getPrice(priceAggregatorAddress, maxTimeout)
                : getTwap(priceAggregatorAddress, maxTimeout, lookback);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beanstalk: The Finale |
| Report Date | N/A |
| Finders | sohrabhind, bladesec, joicygiore, Draiakoo, holydevoti0n, bareli, T1MOH, emmac002, KalyanSingh2, tlaloc |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-05-beanstalk-the-finale
- **Contest**: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n

### Keywords for Search

`Oracle`

