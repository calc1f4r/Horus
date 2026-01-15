---
# Core Classification
protocol: Fungify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31815
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
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
  - Zach Obront
---

## Vulnerability Title

[M-02] NFT oracle missing Chainlink liveness checks

### Overview


The bug report discusses an issue with the `getUnderlyingPrice()` function in the Chainlink oracle. It states that when this function is called, it performs recommended liveness checks to ensure the price is not stale. However, in the `FloorPriceFeedAdaptor`, which calculates the NFT's USD value, these checks are not performed. As a result, the adaptor returns a value of `0` for the price, which will not pass the stale price check and lead to inaccurate liquidations. The report recommends adding the same liveness checks to the `FloorPriceFeedAdaptor` as used in the Chainlink oracle. This issue has been fixed in a recent commit.

### Original Finding Content

When `getUnderlyingPrice()` is called on the Chainlink oracle, the recommended liveness checks are performed:
```solidity
(
    /*uint80 roundID*/,
    int rate,
    /*uint startedAt*/,
    uint updatedAt,
    /*uint80 answeredInRound*/
) = feed.latestRoundData();

...

// check if price is stale
uint stalePriceDelay = stalePriceDelays[asset];
if (stalePriceDelay != 0 && block.timestamp > updatedAt + stalePriceDelay) {
    revert StalePrice();
}
```
However, in the `FloorPriceFeedAdaptor`, we calculate the NFT's USD value by pulling from two separate oracles and combining the values. When these values are pulled, no liveness checks are performed:
```solidity
function latestAnswer() public view returns (int256) {
    (
        ,
        int floorRate,
        ,
        ,

    ) = floorPriceFeed.latestRoundData();

    (
        ,
        int ethRate,
        ,
        ,

    ) = ethPriceFeed.latestRoundData();

    return floorRate * ethRate / 1e18; // scale to 8 decimals places like Chainlink
}
```

When the adaptor returns the `latestRoundData()` to the oracle, it fills in all values except the price with 0s.

```solidity
function latestRoundData()
    public
    view
    returns (
        uint80 roundId,
        int256 answer,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) {
    return (0, latestAnswer(), 0, 0, 0);
}
```

However, a return value of `0` will not pass the stale price check. Instead, `0` will lead any updated time that isn't at the exact current timestamp to fail the check.

As a result, any NFT oracle that has a `stalePriceDelay` added will be unusable and revert whenever it is called.

The result is that we will need to skip stale price checks, allowing outdated prices that can lead to inaccurate liquidations. This is especially important because Chainlink's NFT Floor Price Feeds are considered "Specialized Feeds" (less secure, see [I-01]), so need to be carefully monitored.

**Recommendation**

It is recommended to add the same liveness checks to the `FloorPriceFeedAdaptor` as are used in the Chainlink oracle.

**Review**

Fixed as recommended in [d603c6636266cee9d62434c839f58821de5ee193](https://github.com/fungify-dao/taki-contracts/pull/9/commits/d603c6636266cee9d62434c839f58821de5ee193).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Fungify |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

