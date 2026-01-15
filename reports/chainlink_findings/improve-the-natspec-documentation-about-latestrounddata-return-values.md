---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40747
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c32cfcdb-e602-44bf-a16c-ca6dd217673e
source_link: https://cdn.cantina.xyz/reports/cantina_morpho_blue_oracles_adapters_feb2024.pdf
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

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Jonah Wu
  - StErMi
---

## Vulnerability Title

Improve the NatSpec documentation about latestRoundData return values 

### Overview

See description below for full details.

### Original Finding Content

## Context
WstEthEthExchangeRateChainlinkAdapter.sol#L26-L30

## Description
The `latestRoundData()` function in the `WstEthEthExchangeRateChainlinkAdapter` returns the following values to be compliant with the Chainlink interface signature as explained in their documentation:

- `uint80 roundId`
- `int256 answer`
- `uint256 startedAt`
- `uint256 updatedAt`
- `uint80 answeredInRound`

The current implementation of `WstEthEthExchangeRateChainlinkAdapter.latestRoundData` only returns non-empty values for the `answer` returned variable, leaving all the others "empty" (using the Solidity default compiler value). 

While this could be seen as valid behavior for a custom Chainlink-like oracle, such behavior should be documented and explained.

## Recommendation
Morpho should improve the natspec documentation about values returned by `latestRoundData`, documenting that only the `answer` return parameter will have a valid value, while the other parameters will be "empty". 

An additional change that should be considered is to clarify that this is a "Chainlink-compliant" contract that does not fully follow the normal behavior of a Chainlink oracle that would always return non-empty values for all the returned parameters.

## Morpho
Addressed in PR 83.

## Cantina Managed
PR 83 correctly documents and clarifies the value (always 0) returned by the named parameters:

- `uint80 roundId`
- `int256 answer`
- `uint256 startedAt`
- `uint256 updatedAt`
- `uint80 answeredInRound`

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Jonah Wu, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_morpho_blue_oracles_adapters_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c32cfcdb-e602-44bf-a16c-ca6dd217673e

### Keywords for Search

`vulnerability`

