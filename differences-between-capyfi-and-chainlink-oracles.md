---
# Core Classification
protocol: CapyFi Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61616
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/capyfi-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Differences Between CapyFi And Chainlink Oracles

### Overview

See description below for full details.

### Original Finding Content

There are some implementation differences between Chainlink's and Capyfi's aggregators:

* In Chainlink price feeds, the [`roundId` is composed of `phaseId` and `originalId`](https://docs.chain.link/data-feeds/historical-data#roundid-in-proxy). The `phaseId` is a counter that gets incremented each time a new aggregator is referenced and the `originalId` is a counter to track each submitted price in the data feed. These two IDs are packed into the same `uint80` shifted by `uint80((phaseId << 64) + originalId)`. Both counters start at 1, hence, the first valid `roundId` should be `18446744073709551617`. However, in Capyfi's implementation, it [starts at 1](https://github.com/LaChain/capyfi-sc/blob/cf47234ecffe0747f894dc73c4df15b78469b0bf/src/contracts/PriceOracle/CapyfiAggregatorV3.sol#L61) and gets [incremented](https://github.com/LaChain/capyfi-sc/blob/cf47234ecffe0747f894dc73c4df15b78469b0bf/src/contracts/PriceOracle/CapyfiAggregatorV3.sol#L116) each time a new price is submitted. If an external integrator wants to fetch historical data from the very beginning and they try to fetch the first valid round from a Chainlink aggregator into Capyfi's implementation, it will revert.
* When someone wants to fetch data from a round that has not yet been filled, Chainlink's implementation returns empty data. For `getAnswer(uint256 roundId)` and `getTimestamp(uint256 roundId)`, it returns 0 and for `getRoundData(uint80 roundId)`, it returns 0 for `answer`, `startedAt`, and `updatedAt`. However, in Capyfi's implementation, it reverts the execution. This can also break external integrations.
* There are no minimum and maximum price bound checks in the CapyFi oracle.
* For the CapyFi oracle, `startedAt` is always the same value as `updatedAt`. This is because when `updateAnswer` is called, that price is immediately the price of the oracle, whereas Chainlink aggregates multiple oracle sources which requires a time delay.

Consider documenting the above-listed differences in the codebase so that integrators can be aware of them.

***Update:** Resolved in [pull request #7](https://github.com/LaChain/capyfi-sc/pull/7) at [commit fb173f](https://github.com/LaChain/capyfi-sc/pull/7/commits/fb173f1fe2b0b994d5329613ad8b380f8f902e63).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | CapyFi Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/capyfi-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

