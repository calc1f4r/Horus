---
# Core Classification
protocol: DittoETH
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27486
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc
source_link: none
github_link: https://github.com/Cyfrin/2023-09-ditto

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

protocol_categories:
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - serialcoder
---

## Vulnerability Title

Use of hardcoded price deviation in baseOracleCircuitBreaker()

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibOracle.sol#L77-L78">https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibOracle.sol#L77-L78</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibOracle.sol#L81">https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibOracle.sol#L81</a>


## Summary

The `LibOracle::baseOracleCircuitBreaker()` uses the hardcoded value of 50% price deviation, which might be too large when using the ETH as a base price reference. Moreover, the fixed % deviation is considered too risky because the protocol's DAO or admin will not be able to update it in production.

## Vulnerability Details

> **This report raises an issue regarding the `priceDeviation` variable only**, as the `invalidFetchData` (2-hour stale check) was flagged as a known issue.

The `baseOracleCircuitBreaker()` is used for verifying the price reported by Chainlink. If the reported price is invalid or its [price deviation when compared to the protocol's cached oracle price is more than 50%](https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibOracle.sol#L77-L78), the function will fall back to get Uniswap's TWAP price instead.

However, the `baseOracleCircuitBreaker()` uses a [hardcoded value of 50% price deviation](https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibOracle.sol#L78) (`0.5 ether`), which might be too large when using the ETH as a base price reference. Moreover, the fixed % deviation is considered too risky because the protocol's DAO or admin will not be able to update it in production.

```solidity
    //@audit -- this report raises an issue regarding the priceDeviation variable only, as the invalidFetchData (2-hour stale check) was flagged as a known issue
    function baseOracleCircuitBreaker(
        uint256 protocolPrice,
        uint80 roundId,
        int256 chainlinkPrice,
        uint256 timeStamp,
        uint256 chainlinkPriceInEth
    ) private view returns (uint256 _protocolPrice) {
        bool invalidFetchData = roundId == 0 || timeStamp == 0
            || timeStamp > block.timestamp || chainlinkPrice <= 0
            || block.timestamp > 2 hours + timeStamp;
        uint256 chainlinkDiff = chainlinkPriceInEth > protocolPrice
            ? chainlinkPriceInEth - protocolPrice
            : protocolPrice - chainlinkPriceInEth;
@>      bool priceDeviation =
@>          protocolPrice > 0 && chainlinkDiff.div(protocolPrice) > 0.5 ether;

        //@dev if there is issue with chainlink, get twap price. Compare twap and chainlink
@>      if (invalidFetchData || priceDeviation) { //@audit -- this report raises an issue regarding the priceDeviation variable only, as the invalidFetchData (2-hour stale check) was flagged as a known issue
            ...
        } else {
            return chainlinkPriceInEth;
        }
    }
```

- https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibOracle.sol#L77-L78

- https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibOracle.sol#L81

## Impact

> **This report raises an issue regarding the `priceDeviation` variable only**, as the `invalidFetchData` (2-hour stale check) was flagged as a known issue.

The use of the hardcoded value of 50% price deviation (`0.5 ether`) might be too large when using the ETH as a base price reference. Moreover, the fixed % deviation is considered too risky because the protocol's DAO or admin will not be able to update it in production.

Consequently, the [check for price deviation](https://github.com/Cyfrin/2023-09-ditto/blob/a93b4276420a092913f43169a353a6198d3c21b9/contracts/libraries/LibOracle.sol#L81) in the `baseOracleCircuitBreaker()` might not be effective enough for filtering out the stale price in production, directly affecting the quality of the oracle price that will be consumed by the core functions of the `Ditto` protocol (HIGH impact).

## Tools Used

Manual Review

## Recommendations

The % price deviation should be a variable updatable by the protocol's DAO or admin in production.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | DittoETH |
| Report Date | N/A |
| Finders | serialcoder |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-09-ditto
- **Contest**: https://www.codehawks.com/contests/clm871gl00001mp081mzjdlwc

### Keywords for Search

`vulnerability`

