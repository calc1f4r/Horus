---
# Core Classification
protocol: Frax Solidity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17920
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
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
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

Return values of the Chainlink oracle are not validated

### Overview

See description below for full details.

### Original Finding Content

## Security Assessment Summary

**Difficulty:** Low  

**Type:** Undefined Behavior  

**Target:**  
- FraxPoolV3.sol  
- ComboOracle.sol  
- FRAXOracleWrapper.sol  
- FXSOracleWrapper.sol  

## Description

The `latestRoundData` function returns a signed integer that is coerced to an unsigned integer without checking that the value is a positive integer. An overflow (e.g., `uint(-1)`) would drastically misrepresent the price and cause unexpected behavior. In addition, `FraxPoolV3` does not validate the completion and recency of the round data, permitting stale price data that does not reflect recent changes.

```solidity
function getFRAXPrice() public view returns (uint256) {
    (, int price, , , ) = priceFeedFRAXUSD.latestRoundData();
    return uint256(price).mul(PRICE_PRECISION).div(10 ** chainlink_frax_usd_decimals);
}

function getFXSPrice() public view returns (uint256) {
    (, int price, , , ) = priceFeedFXSUSD.latestRoundData();
    return uint256(price).mul(PRICE_PRECISION).div(10 ** chainlink_fxs_usd_decimals);
}
```
*Source: contracts/Frax/Pools/FraxPoolV3.sol#231–239*

An older version of Chainlink’s oracle interface has a similar function, `latestAnswer`. When this function is used, the return value should be checked to ensure that it is a positive integer. However, round information does not need to be checked because `latestAnswer` returns only price data.

## Recommendations

**Short-term:**  
Add a check to `latestRoundData` and similar functions to verify that values are non-negative before converting them to unsigned integers. Also, add an invariant that checks that the round has finished and that the price data is from the current round:

```solidity
require(updatedAt != 0 && answeredInRound == roundID);
```

**Long-term:**  
Define a minimum update threshold and add the following check:

```solidity
require((block.timestamp - updatedAt <= minThreshold) && (answeredInRound == roundID));
```

Furthermore, use consistent interfaces instead of mixing different versions.

## References

- Chainlink AggregatorV3Interface

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Solidity |
| Report Date | N/A |
| Finders | Samuel Moelius Maximilian Krüger Troy Sargent |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf

### Keywords for Search

`vulnerability`

