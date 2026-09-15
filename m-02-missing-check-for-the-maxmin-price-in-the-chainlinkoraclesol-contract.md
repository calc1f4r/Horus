---
# Core Classification
protocol: Moonwell
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26838
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-moonwell
source_link: https://code4rena.com/reports/2023-07-moonwell
github_link: https://github.com/code-423n4/2023-07-moonwell-findings/issues/340

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
finders_count: 12
finders:
  - okolicodes
  - dacian
  - R-Nemes
  - markus\_ether
  - kodyvim
---

## Vulnerability Title

[M-02] Missing check for the max/min price in the `chainlinkOracle.sol` contract

### Overview


This bug report is about a `chainlinkOracle.sol` contract and the `getChainlinkPrice` function which is used to get/call the `latestRoundData` from the aggregator v2 and v3. It was found that the function does not check for the min and max amount return to prevent some cases from happening. This could mean that, if a case like LUNA happens, then the oracle will return the minimum price and not the crashed price.

Recommended mitigation steps include adding checks like `require(answer < _maxPrice, "Upper price bound breached");` and `require(answer > _minPrice, "Lower price bound breached");` to avoid returning the min price or the max price in case of the price crashes. The Chainlink Aggregator has minPrice and maxPrice circuit breakers built into it, but a circuit breaker should be implemented on the Moonwell oracle so that when the price edges close to `minAnswer` or `maxAnswer` it starts reverting, to avoid consuming stale prices when Chainlink freezes. The bug report was acknowledged by Moonwell.

### Original Finding Content


The `chainlinkOracle.sol` contract specially the `getChainlinkPrice` function using the aggregator v2 and v3 to get/call the `latestRoundData`. the function should check for the min and max amount return to prevent some case happen, something like this:

<https://solodit.xyz/issues/missing-checks-for-chainlink-oracle-spearbit-connext-pdf> 

<https://solodit.xyz/issues/m-16-chainlinkadapteroracle-will-return-the-wrong-price-for-asset-if-underlying-aggregator-hits-minanswer-sherlock-blueberry-blueberry-git>

If a case like LUNA happens then the oracle will return the minimum price and not the crashed price.

### Proof of Concept

The function `getChainlinkPrice`:

```soliditiy
function getChainlinkPrice(
        AggregatorV3Interface feed
    ) internal view returns (uint256) {
        (, int256 answer, , uint256 updatedAt, ) = AggregatorV3Interface(feed)
            .latestRoundData();
        require(answer > 0, "Chainlink price cannot be lower than 0");
        require(updatedAt != 0, "Round is in incompleted state");

        // Chainlink USD-denominated feeds store answers at 8 decimals
        uint256 decimalDelta = uint256(18).sub(feed.decimals());
        // Ensure that we don't multiply the result by 0
        if (decimalDelta > 0) {
            return uint256(answer).mul(10 ** decimalDelta);
        } else {
            return uint256(answer);
        }
    }
```

The function did not check for the min and max price.

### Recommended Mitigation Steps

Some check like this can be added to avoid returning of the min price or the max price in case of the price crashes.

```solidity
          require(answer < _maxPrice, "Upper price bound breached");
          require(answer > _minPrice, "Lower price bound breached");
```

**[sorrynotsorry (Lookout) commented](https://github.com/code-423n4/2023-07-moonwell-findings/issues/340#issuecomment-1660090896):**
  >The implementation does not set a min/max value by design. Also Chainlink does not return min/max price as per the AggregatorV3 docs [HERE](https://docs.chain.link/data-feeds/api-reference#latestrounddata)  contrary to the reported below;

 >ChainlinkAggregators have minPrice and maxPrice circuit breakers built into them.
 
 >Further proof required as per the context.

**[alcueca (Judge) commented](https://github.com/code-423n4/2023-07-moonwell-findings/issues/340#issuecomment-1676380695):**
 > The warden is actually right. [It is a bit difficult to find](https://docs.chain.link/data-feeds#check-the-latest-answer-against-reasonable-limits), but the `minAnswer` and `maxAnswer` can be retrieved from the Chainlink Aggregator, one step through the proxy. A circuit breaker should be implemented on the Moonwell oracle so that when the price edges close to `minAnswer` or `maxAnswer` it starts reverting, to avoid consuming stale prices when Chainlink freezes.

 **[ElliotFriedman (Moonwell) acknowledged](https://github.com/code-423n4/2023-07-moonwell-findings/issues/340)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Moonwell |
| Report Date | N/A |
| Finders | okolicodes, dacian, R-Nemes, markus\_ether, kodyvim, 0xkazim, MohammedRizwan, Auditwolf, nadin, BRONZEDISC, niki, Hama |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-moonwell
- **GitHub**: https://github.com/code-423n4/2023-07-moonwell-findings/issues/340
- **Contest**: https://code4rena.com/reports/2023-07-moonwell

### Keywords for Search

`vulnerability`

