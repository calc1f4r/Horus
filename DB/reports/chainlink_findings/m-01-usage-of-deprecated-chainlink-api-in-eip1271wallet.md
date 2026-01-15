---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24658
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-notional
source_link: https://code4rena.com/reports/2022-01-notional
github_link: https://github.com/code-423n4/2022-01-notional-findings/issues/197

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] Usage of deprecated ChainLink API in `EIP1271Wallet`

### Overview


This bug report focuses on the Chainlink API (`latestAnswer`) being used in the `EIP1271Wallet` contract. This API has been deprecated and does not return an error if no answer has been reached, but instead returns 0. Additionally, the `latestAnswer` is reported with 18 decimals for crypto quotes, but 8 decimals for FX quotes.

The recommended mitigation steps are to use the `latestRoundData` function to get the price instead and to add checks on the return data with proper revert messages if the price is stale or the round is uncomplete.

Overall, this bug report highlights the importance of using the correct API and the potential issues that could arise from using deprecated APIs. It is important to ensure that the API used is up to date and that the correct decimals are used for the appropriate quotes. Additionally, it is important to add checks on the return data to ensure that the data is valid and up to date.

### Original Finding Content

_Submitted by cmichel, also found by 0x1f8b, defsec, leastwood, pauliax, sirhashalot, TomFrenchBlockchain, UncleGrandpa925, and WatchPug_

The Chainlink API (`latestAnswer`) used in the `EIP1271Wallet` contract is deprecated:

> This API is deprecated. Please see API Reference for the latest Price Feed API. [Chainlink Docs](https://web.archive.org/web/20210304160150/https://docs.chain.link/docs/deprecated-aggregatorinterface-api-reference)

This function does not error if no answer has been reached but returns 0. Besides, the `latestAnswer` is reported with 18 decimals for crypto quotes but 8 decimals for FX quotes (See Chainlink FAQ for more details). A best practice is to get the decimals from the oracles instead of hard-coding them in the contract.

#### Recommended Mitigation Steps

Use the `latestRoundData` function to get the price instead. Add checks on the return data with proper revert messages if the price is stale or the round is uncomplete, for example:

```solidity
(uint80 roundID, int256 price, , uint256 timeStamp, uint80 answeredInRound) = priceOracle.latestRoundData();
require(answeredInRound >= roundID, "...");
require(timeStamp != 0, "...");
```

**[pauliax (judge) commented](https://github.com/code-423n4/2022-01-notional-findings/issues/197#issuecomment-1037191042):**
 > Valid finding. I am hesitating whether this should be low or medium but decided to leave it as a medium because the likeliness is low but the impact would be huge, and all the wardens submitted this with a medium severity. Also: "Assets not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements."



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Notional |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-notional
- **GitHub**: https://github.com/code-423n4/2022-01-notional-findings/issues/197
- **Contest**: https://code4rena.com/reports/2022-01-notional

### Keywords for Search

`vulnerability`

