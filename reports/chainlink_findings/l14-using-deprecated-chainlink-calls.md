---
# Core Classification
protocol: 1inch Limit Order Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10697
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/1inch-limit-order-protocol-audit/
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
  - dexes
  - services
  - cross_chain
  - nft_lending
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L14] Using deprecated Chainlink calls

### Overview

See description below for full details.

### Original Finding Content

The [`ChainlinkCalculator`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/helpers/ChainlinkCalculator.sol) contract is intended to be used to query Chainlink oracles. It does so via making calls to their [`latestTimestamp`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/helpers/ChainlinkCalculator.sol#L23) and [`latestAnswer`](https://github.com/1inch/limit-order-protocol/blob/4d94eea25e4dac6271bfd703096a5c4a4d899b4a/contracts/helpers/ChainlinkCalculator.sol#L27) methods, [both of which have been deprecated](https://github.com/smartcontractkit/chainlink/blob/master/contracts/src/v0.6/FluxAggregator.sol#L335-L361). In fact, the methods are no longer present in the API of Chainlink aggregators [as of version three](https://github.com/smartcontractkit/chainlink/blob/master/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol).


To avoid potential future incompatibilities with Chainlink oracles, consider using the [`latestRoundData`](https://github.com/smartcontractkit/chainlink/blob/1adaebc7acedb3a133611ec5cbb61a852802ad33/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol#L43) method instead.


***Update:** Fixed in [pull request #67](https://github.com/1inch/limit-order-protocol/pull/67).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | 1inch Limit Order Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/1inch-limit-order-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

