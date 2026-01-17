---
# Core Classification
protocol: Radiant V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32855
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant
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
  - OpenZeppelin
---

## Vulnerability Title

Missing PriceProvider Oracle Updates

### Overview


The `PriceProvider` contract is used to provide pricing data to other contracts in the protocol. It can use different oracles to get this data, but when using the `UniV2TwapOracle`, the `update` function needs to be triggered frequently to keep the data up to date. However, some contracts that use `PriceProvider` are not triggering this function, which means their price data may be stale. This bug has been fixed in a recent pull request, so it is recommended to always trigger the `update` function before using `PriceProvider` to get accurate pricing data.

### Original Finding Content

The [`PriceProvider`](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/oracles/PriceProvider.sol) contract is responsible for providing pricing data to multiple contracts of the protocol. It uses either pool data or one of the following oracles: `ChainlinkV3Adapter`, `UniV3TwapOracle`, `UniV2TwapOracle`.


In the case where [`UniV2TwapOracle`](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/oracles/UniV2TwapOracle.sol#L119-L161) is used, the `update` function must be frequently triggered to correctly track TWAP data, otherwise the returned price will be stale. This is done in the [`LockZap`](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/zap/LockZap.sol#L270) contract and in multiple functions of the [`MultiFeeDistribution`](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/staking/MultiFeeDistribution.sol) contract.


The following contracts are using `PriceProvider` but are missing oracle updates:


* [`RadiantOFT`](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/token/RadiantOFT.sol)
* [`Compounder`](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/accessories/Compounder.sol)
* [`EligibilityDataProvider`](https://github.com/radiant-capital/v2-core/blob/e8f21f103e17736907b62809d1ad902febc53714/contracts/radiant/eligibility/EligibilityDataProvider.sol)


It is recommended to always trigger the `update` function before using `PriceProvider` to query price data.


***Update:** Resolved in [pull request #235](https://github.com/radiant-capital/v2-core/pull/235) at commits [6d1516f](https://github.com/radiant-capital/v2-core/commit/6d1516ffe8eab7e2b6383296e39c057f5a9b0c74), [c654e43](https://github.com/radiant-capital/v2-core/commit/c654e4341506bf8718de4e2d0206feaf081de3d8) and [4467c8d](https://github.com/radiant-capital/v2-core/commit/4467c8df331e563f0daa10df311ceb0334c6e6bd).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

