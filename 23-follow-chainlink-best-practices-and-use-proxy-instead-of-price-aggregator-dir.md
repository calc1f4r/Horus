---
# Core Classification
protocol: LoopFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49099
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-loopfi
source_link: https://code4rena.com/reports/2024-07-loopfi
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
finders_count: 0
finders:
---

## Vulnerability Title

[23] Follow chainlink best practices and use proxy instead of price aggregator directly

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-07-loopfi/blob/57871f64bdea450c1f04c9a53dc1a78223719164/src/oracle/ChainlinkOracle.sol#L91-L111

```solidity
function _fetchAndValidate(address token) internal view returns (bool isValid, uint256 price) {
  Oracle memory oracle = oracles[token];
  try AggregatorV3Interface(oracle.aggregator).latestRoundData() returns (
    uint80, /*roundId*/
    int256 answer,
    uint256, /*startedAt*/
    uint256 updatedAt,
    uint80 /*answeredInRound*/
  ) {
    isValid = (answer > 0 && block.timestamp - updatedAt <= oracle.stalePeriod);
    return (isValid, wdiv(uint256(answer), oracle.aggregatorScale));
  } catch {
    // return the default values (false, 0) on failure
  }
}
```

This function fetches and validates the latest price from Chainlink; however, Chainlink recommends using the proxy and not the priceAggregator directly as a best practice.

### Impact

QA, best practice.

### Recommended Mitigation Steps

Follow the mentioned [best practices from Chainlink](https://docs.chain.link/data-feeds). You can call the `latestRoundData()` function directly on the aggregator, but it is a best practice to use the proxy instead so that changes to the aggregator do not affect your application. Similar to the proxy contract, the aggregator contract has a `latestAnswer` variable, owner address, `latestTimestamp` variable, and several others.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-loopfi
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-07-loopfi

### Keywords for Search

`vulnerability`

