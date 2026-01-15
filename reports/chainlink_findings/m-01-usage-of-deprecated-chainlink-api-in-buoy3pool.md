---
# Core Classification
protocol: Gro Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42239
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-06-gro
source_link: https://code4rena.com/reports/2021-06-gro
github_link: https://github.com/code-423n4/2021-06-gro-findings/issues/106

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

protocol_categories:
  - dexes
  - cdp
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] Usage of deprecated ChainLink API in `Buoy3Pool`

### Overview


The Chainlink API used in the Buoy3Pool oracle wrappers is outdated and can return incorrect data. This could lead to inaccurate prices being used. The Chainlink documentation recommends adding checks to ensure the data is not stale, similar to those used in the new API. A fix has been implemented in the release version.

### Original Finding Content

_Submitted by cmichel, also found by 0xRajeev and a_delamo_

The Chainlink API (`latestAnswer`) used in the `Buoy3Pool` oracle wrappers is deprecated:

> This API is deprecated. Please see API Reference for the latest Price Feed API. [Chainlink Docs](https://docs.chain.link/docs/deprecated-aggregatorinterface-api-reference/#latestanswer)

It seems like the old API can return stale data. Checks similar to that of the new API using `latestTimestamp` and `latestRoundare` are needed, as this could lead to stale prices according to the Chainlink documentation:
* [under current notifications: "if answeredInRound < roundId could indicate stale data."](https://docs.chain.link/docs/developer-communications#current-notifications)
* [under historical price data: "A timestamp with zero value means the round is not complete and should not be used."](https://docs.chain.link/docs/historical-price-data#solidity)

Recommend adding checks similar to `latestTimestamp` and `latestRoundare`

```solidity
(
    uint80 roundID,
    int256 price,
    ,
    uint256 timeStamp,
    uint80 answeredInRound
) = chainlink.latestRoundData();
require(
    timeStamp != 0,
    “ChainlinkOracle::getLatestAnswer: round is not complete”
);
require(
    answeredInRound >= roundID,
    “ChainlinkOracle::getLatestAnswer: stale data”
);
require(price != 0, "Chainlink Malfunction”);
```

**[kristian-gro (Gro) confirmed](https://github.com/code-423n4/2021-06-gro-findings/issues/106)**
> Confirmed and Fix has been implemented in release version.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gro Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-gro
- **GitHub**: https://github.com/code-423n4/2021-06-gro-findings/issues/106
- **Contest**: https://code4rena.com/reports/2021-06-gro

### Keywords for Search

`vulnerability`

