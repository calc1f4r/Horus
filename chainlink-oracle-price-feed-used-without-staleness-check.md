---
# Core Classification
protocol: Brt Dci Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52276
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/prodigy/brt-dci-contracts
source_link: https://www.halborn.com/audits/prodigy/brt-dci-contracts
github_link: none

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
  - Halborn
---

## Vulnerability Title

Chainlink Oracle Price Feed Used Without Staleness Check

### Overview


The report highlights an issue in the `getPrice` function in the AggregatorHelper.sol file, where the price data fetched from a Chainlink oracle is not checked for freshness. This means that outdated or incorrect price information can be used in important calculations. The report recommends implementing a check using the `updatedAt` value returned by `latestRoundData()` and comparing it to the current block timestamp. The issue has been solved by implementing these checks. The relevant code and references can be found in the report.

### Original Finding Content

##### Description

The `getPrice` function in AggregatorHelper.sol fetches price data from a Chainlink oracle without validating the freshness of the returned data:

```
function getPrice(address _aggregator, bytes32 _pythPriceFeed, bytes[] calldata _priceUpdateData)
    internal
    returns (int256 price)
{
    if (_pythPriceFeed == bytes32(0)) {
// latestRoundData() returns int256 answer
        (, price,,,) = IChainlinkOracle(_aggregator).latestRoundData();
    } else {
// PythStructs.Price.price is int64
        price =
            IPythAggregator(_aggregator).getLatestEmaPrice{value: msg.value}(_pythPriceFeed, _priceUpdateData).price;
    }
}
```

The function calls `latestRoundData()` on the Chainlink oracle but does not check the `updatedAt` timestamp to ensure the price data is current. This allows stale or outdated price information to be used in critical calculations.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:M/R:N/S:C (6.3)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:M/R:N/S:C)

##### Recommendation

It is recommended to implement a staleness check using the `updatedAt` value returned by `latestRoundData()`. Compare it against the current block timestamp and a predefined threshold:

```
if (_pythPriceFeed == bytes32(0)) {
        (, price,,uint256 updatedAt,) = IChainlinkOracle(_aggregator).latestRoundData();
        require(block.timestamp - updatedAt <= PRICE_FRESHNESS_THRESHOLD, "Stale price data");
    }
```

##### Remediation

**SOLVED:** Checks have been implemented to ensure price returned by chainlink is correct and not stale.

##### Remediation Hash

<https://github.com/prodigyfi/brt-dci-contracts/commit/d422f6cefa174580ce3afe6c03570cff8551149b>

##### References

[prodigyfi/brt-dci-contracts/src/AggregatorHelper.sol#L30](https://github.com/prodigyfi/brt-dci-contracts/blob/master/src/AggregatorHelper.sol#L30)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Brt Dci Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/prodigy/brt-dci-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/prodigy/brt-dci-contracts

### Keywords for Search

`vulnerability`

