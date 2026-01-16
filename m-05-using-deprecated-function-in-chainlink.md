---
# Core Classification
protocol: Astrolab
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58109
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-05] Using deprecated function in Chainlink

### Overview


This bug report discusses a problem with the `StrategyV5Chainlink` function, which is used to convert from USD to input token amount. The function currently uses a deprecated function, `IChainlinkAggregatorV3.latestAnswer`, which can lead to inaccurate calculations of total asset values and share prices. The report recommends updating the function to use `IChainlinkAggregatorV3.latestRoundData` instead, which provides more comprehensive data and ensures the freshness and relevance of the price. Additionally, when deploying on Arbitrum, a check should be included to verify the status of the Arbitrum Sequencer, as this can impact the reliability of the price feeds.

### Original Finding Content

## Severity

**Impact:** High - Using stale prices leads to inaccurate calculations of total asset values and share prices.

**Likelihood:** Low - The return price can be wrong or stale without validating

## Description

To convert from USD to input token amount, `StrategyV5Chainlink` uses `IChainlinkAggregatorV3.latestAnswer`. However the function `latestAnswer` is deprecated by Chainlink. This deprecated function usage is also observed in other libraries, such as `ChainlinkUtils`.

    function _usdToInput(uint256 _amount, uint8 _index) internal view returns (uint256) {
        return _amount.mulDiv(10**uint256(inputFeedDecimals[_index]) * inputDecimals[_index],
            uint256(inputPriceFeeds[_index].latestAnswer()) * 1e6); // eg. (1e6+1e8+1e6)-(1e8+1e6) = 1e6
    }

For reference: https://docs.chain.link/data-feeds/api-reference#latestanswer

`IChainlinkAggregatorV3.latestRoundData` should be used instead.

## Recommendations

Update the function to use `latestRoundData` from Chainlink. This method provides comprehensive data about the latest price round, including the timestamp, ensuring the price's freshness and relevance.

Example implementation:

    uint256 private constant GRACE_PERIOD_TIME = 3600; // how long till we consider the price as stale

    function getChainlinkPrice (AggregatorV2V3Interface feed) internal {
        (uint80 roundId, int256 price, uint startedAt, uint updatedAt, uint80 answeredInRound) = feed.latestRoundData();
        require(price > 0, "invalid price");
        require(block.timestamp <= updatedAt + GRACE_PERIOD_TIME, "Stale price");
        return price;
    }

When deploying on Arbitrum, include a check to verify the status of the Arbitrum Sequencer, as this can impact the reliability of the price feeds.

Example: https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Astrolab |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

