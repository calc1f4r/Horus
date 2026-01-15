---
# Core Classification
protocol: Zaros
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38005
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clyg8slke0001bvhpwszwjr7z
source_link: none
github_link: https://github.com/Cyfrin/2024-07-zaros

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
  - 0xe4669da
---

## Vulnerability Title

In `ChainlinkUtil::getPrice` function, skipping `roundId` check at all can be disastrous

### Overview

See description below for full details.

### Original Finding Content

## Summary

In `ChainlinkUtil::getPrice` function, the `roundId` is not checked or validated at all. Stale prices could result in mass liquidations and huge bad debts that could even challenge the going concern of the protocol.

## Vulnerability Details

Zaros protocol is solely relying on Chainlink for most of the critical functionalities of the protocol. This actually introduces the chances of single point of failure. For off-chain price feeds, Zaros is using Chainlink's aggregator only.

While getting the off-chain price of an asset using `ChainlinkUtil::getPrice` function, the `roundId` is not checked or validated at all. However, `updatedAt` is compared with the `priceFeedHeartbeatSeconds`, but this sole check is not enough. As we can see in [this report](https://solodit.xyz/issues/m-02-should-check-return-data-from-chainlink-aggregators-code4rena-yeti-finance-yeti-finance-contest-git) how important the validation of `roundId` is.

[This another report](https://solodit.xyz/issues/m-05-chainlinks-latestrounddata-might-return-stale-or-incorrect-results-code4rena-backd-backd-contest-git) is also suitable for our case because the protocol has used the `updatedAt` and some sort of `stalePriceDelay` in order to accept only the fresh prices and avoid any stale prices. The reason that this report is valid because `roundId` is not validated at all, that makes this logic vulnerable to disastrous exploits.

The Chainlink [docs](https://docs.chain.link/data-feeds/historical-data) also emphasize the validation of `roundId`. Using the `roundId` we can ensure the data freshness, sequential data integrity, stale data detection and round completion.

Among others, a devastating example and lesson as a result of Chainlink price oracle malfunction we have [TERRA LUNA](https://cointelegraph.com/news/defi-protocols-declare-losses-as-attackers-exploit-luna-price-feed-discrepancy). We have to implement as many controls as we can to avoid such mishaps.

Source: [ChainlinkUtil.sol#L59C1-L76C6](https://github.com/Cyfrin/2024-07-zaros/blob/d687fe96bb7ace8652778797052a38763fbcbb1b/src/external/chainlink/ChainlinkUtil.sol#L59C1-L76C6)

```solidity
    ...
    try priceFeed.latestRoundData() returns (uint80, int256 answer, uint256, uint256 updatedAt, uint80) {
        // no roundId validation <= FOUND
@>      if (block.timestamp - updatedAt > priceFeedHeartbeatSeconds) {
            revert Errors.OraclePriceFeedHeartbeat(address(priceFeed));
        }
        
        IOffchainAggregator aggregator = IOffchainAggregator(priceFeed.aggregator());
        int192 minAnswer = aggregator.minAnswer();
        int192 maxAnswer = aggregator.maxAnswer();

        if (answer <= minAnswer || answer >= maxAnswer) {
            revert Errors.OraclePriceFeedOutOfRange(address(priceFeed));
        }

        price = ud60x18(answer.toUint256() * 10 ** (Constants.SYSTEM_DECIMALS - priceDecimals));
    } catch {
        revert Errors.InvalidOracleReturn();
    }
    ...
    
```

## Impact

As an impact of wrong price feeds, positions may be liquidated prematurely or fail to liquidate when they should and eventually resulting bad debts. Positions open on wrong collateral prices which may cost major financial losses to the protocol. Incorrect collateral valuation can cause under-collateralization.

## Tools Used

Manual review

## Recommendations

To mitigate the risk, `latestRoundData` function returns the `answeredInRound` value among other returned values. Although this value is depreacated as mentioned in the docs but still this can be used to validate the `roundId`. If Zaros don't want to validate the `roundId` using `answeredInRound` (deprecated) then atleast it must check the `startedAt` timestamp because each roundData has this prop. The implication should be like, `startedAt` should be greater than last `startedAt` this will ensure that price does not pertain to previous round and the price is fresh and udpated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Zaros |
| Report Date | N/A |
| Finders | 0xe4669da |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-07-zaros
- **Contest**: https://codehawks.cyfrin.io/c/clyg8slke0001bvhpwszwjr7z

### Keywords for Search

`vulnerability`

