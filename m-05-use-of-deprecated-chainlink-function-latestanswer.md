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
solodit_id: 414
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-gro-protocol-contest
source_link: https://code4rena.com/reports/2021-06-gro
github_link: https://github.com/code-423n4/2021-06-gro-findings/issues/126

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
finders_count: 1
finders:
  - shw
---

## Vulnerability Title

[M-05] Use of deprecated Chainlink function latestAnswer

### Overview


This bug report is about a vulnerability related to Chainlink's `latestAnswer` function. This function does not error if no answer has been reached but returns 0, causing an incorrect price fed to the `Buoy3Pool`. This vulnerability was discovered by referencing Chainlink's documentation, as well as the code in the `Buoy3Pool.sol` file. The recommended mitigation step is to use the `latestRoundData` function to get the price instead, and add checks on the return data with proper revert messages if the price is stale or the round is uncomplete. This will help ensure that the data returned is accurate and up to date.

### Original Finding Content

## Handle

shw


## Vulnerability details

## Impact

According to Chainlink's documentation, the `latestAnswer` function is deprecated. This function does not error if no answer has been reached but returns 0, causing an incorrect price fed to the `Buoy3Pool`.

## Proof of Concept

Referenced code:
[Buoy3Pool.sol#L207](https://github.com/code-423n4/2021-06-gro/blob/main/contracts/pools/oracle/Buoy3Pool.sol#L207)
[Buoy3Pool.sol#L214-L216](https://github.com/code-423n4/2021-06-gro/blob/main/contracts/pools/oracle/Buoy3Pool.sol#L214-L216)

Referenced documentation:
[Chainlink - Deprecated API Reference](https://docs.chain.link/docs/deprecated-aggregatorinterface-api-reference/)
[Chainlink - Migration Instructions](https://docs.chain.link/docs/migrating-to-flux-aggregator/#3-use-the-new-functions)
[Chainlink - API Reference](https://docs.chain.link/docs/price-feeds-api-reference/)

## Recommended Mitigation Steps

Use the `latestRoundData` function to get the price instead. Add checks on the return data with proper revert messages if the price is stale or the round is uncomplete, for example:

```solidity
(uint80 roundID, int256 price, , uint256 timeStamp, uint80 answeredInRound) = oracle.latestRoundData();
require(answeredInRound >= roundID, "...");
require(timeStamp != 0, "...");

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gro Protocol |
| Report Date | N/A |
| Finders | shw |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-gro
- **GitHub**: https://github.com/code-423n4/2021-06-gro-findings/issues/126
- **Contest**: https://code4rena.com/contests/2021-07-gro-protocol-contest

### Keywords for Search

`vulnerability`

