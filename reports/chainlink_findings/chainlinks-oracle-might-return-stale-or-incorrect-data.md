---
# Core Classification
protocol: Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51602
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/anzen-finance/anzen-v2
source_link: https://www.halborn.com/audits/anzen-finance/anzen-v2
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

Chainlink's Oracle Might Return Stale or Incorrect Data

### Overview


The USDzPriceOracle and SPCTPriceOracle contracts use Chainlink as their price oracle. When requesting the price, the contracts may accept stale data which could cause problems in a volatile market. The getPrice() function does not check if the feed was updated at the most recent round or if the round has completed, and it also does not check if the value returned by priceFeed.decimals() is greater than 18. The Anzen team has solved this issue by implementing improvements to the code. The new code includes checks for stale data and ensures that the value returned by priceFeed.decimals() is not greater than 18. This issue has been resolved and the code has been updated.

### Original Finding Content

##### Description

The `USDzPriceOracle` and `SPCTPriceOracle` contracts use Chainlink as their price oracle. When requesting the price via the `getPrice()` function, the contracts query Chainlink for the underlying token price using the `latestRoundData()` function. This function returns `uint80 roundId`, `int256 answer`, `uint256 startedAt`, `uint256 updatedAt` and `uint80 answeredInRound`. `roundId` denotes the identifier of the most recent update round, `answer` is the price of the asset, `startedAt` is the timestamp at which the round started and `updatedAt` is the timestamp at which the feed was updated.

The `getPrice()` function does not check if the feed was updated at the most recent round nor does it verify that `startedAt` (timestamp at which the round started) is not 0, and this can result in accepting stale data which may threaten the stability of the protocol in a volatile market.

```
function getPrice() external view returns (uint256) {
    (, int256 price,, uint256 updatedAt,) = priceFeed.latestRoundData();
    require(price > 0, "invalid price");
    require(block.timestamp - updatedAt <= heartbeat, "stale price");

    return uint256(price) * 10 ** (18 - uint256(priceFeed.decimals()));
}
```

Finally, be aware that, in the unlikely event of `priceFeed.decimals()` returning a value greater than 18, the whole function would break due to the last operation underflowing (`18 - uint256(priceFeed.decimals())`).

##### BVSS

[AO:A/AC:L/AX:M/C:N/I:N/A:H/D:N/Y:N/R:N/S:U (5.0)](/bvss?q=AO:A/AC:L/AX:M/C:N/I:N/A:H/D:N/Y:N/R:N/S:U)

##### Recommendation

Consider improving checks for stale data. Specifically, make sure `startedAt` is not 0 (which would indicate that the round has not completed) and that `answeredInRound` is greater or equal to `roundId`.

Finally, consider adding a check for `priceFeed.decimals()` to make sure it is lower than or equal to 18.

```
function getPrice() external view returns (uint256) {
    (uint80 roundId, int256 price, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound) = priceFeed.latestRoundData();
    require(price > 0, "invalid price");
    require(block.timestamp - updatedAt <= heartbeat, "stale price");
    require(startedAt > 0, "Round not complete");
    require(answeredInRound >= roundId, "stale price");

    uint256 priceFeedDecimals = uint256(priceFeed.decimals();
    require(priceFeedDecimals <= 18, "Incorrect decimals");

    return uint256(price) * 10 ** (18 - uint256(priceFeed.decimals()));
}
```

  

### Remediation Plan

**SOLVED:** The **Anzen team** solved the issue by implementing the proposed improvement.

##### Remediation Hash

<https://github.com/Anzen-Finance/protocol-v2/commit/1b0203995bf643801a18ff39e4f2d69aec7b3400>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol V2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/anzen-finance/anzen-v2
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/anzen-finance/anzen-v2

### Keywords for Search

`vulnerability`

