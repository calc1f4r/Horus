---
# Core Classification
protocol: UMA Oval Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32583
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-oval-audit
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

Use of Deprecated Function From Chainlink API

### Overview


This bug report discusses the use of deprecated functions from the Chainlink interface in the `IAggregatorV3Source` and `UniswapAnchoredViewSourceAdapter` contracts. The report suggests replacing these functions with the appropriate up-to-date counterparts and not importing the `IAggregatorV3` interface into the `IAggregatorV3Source` interface to avoid future mistakes. The issue has been resolved in a recent pull request.

### Original Finding Content

The [`IAggregatorV3Source` interface](https://github.com/UMAprotocol/oev-contracts/blob/39fd6f90f952a9514df779562671cddaa5578e71/src/interfaces/chainlink/IAggregatorV3Source.sol) inherits from the [`IAggregatorV3` interface](https://github.com/UMAprotocol/oev-contracts/blob/39fd6f90f952a9514df779562671cddaa5578e71/src/interfaces/chainlink/IAggregatorV3.sol) which implements Chainlink's deprecated functions [`latestAnswer`](https://github.com/UMAprotocol/oev-contracts/blob/39fd6f90f952a9514df779562671cddaa5578e71/src/interfaces/chainlink/IAggregatorV3.sol#L5) and [`latestTimestamp`](https://github.com/UMAprotocol/oev-contracts/blob/39fd6f90f952a9514df779562671cddaa5578e71/src/interfaces/chainlink/IAggregatorV3.sol#L7). Moreover, the `IAggregatorV3Source` interface itself implements Chainlink's deprecated [`latestRound` function](https://github.com/UMAprotocol/oev-contracts/blob/39fd6f90f952a9514df779562671cddaa5578e71/src/interfaces/chainlink/IAggregatorV3Source.sol#L7).


Additionally, the [`UniswapAnchoredViewSourceAdapter` contract](https://github.com/UMAprotocol/oev-contracts/blob/0f2c18660fc342ced7c7177577432f7d06481684/src/adapters/compound/UniswapAnchoredViewSourceAdapter.sol) in `getLatestSourceData` is using Chainlink's deprecated [`latestTimestamp` function](https://github.com/UMAprotocol/oev-contracts/blob/0f2c18660fc342ced7c7177577432f7d06481684/src/adapters/compound/UniswapAnchoredViewSourceAdapter.sol#L53).


The usage of Chainlink's deprecated functions in `ChainlinkDestinationAdapter` contracts is justified to respect the interface of the protocols that already implement the deprecated Chainlink interface and to ease the switch to the newly developed `Oval`-based contract without introducing breaking changes to the destination protocol. However, the `ChainlinkSourceAdapter` contracts should follow the up-to-date interface from the [Chainlink docs](https://docs.chain.link/data-feeds/api-reference).


Consider replacing Chainlink's deprecated functions with the appropriate up-to-date counterparts. Moreover, consider not importing the `IAggregatorV3` interface into the `IAggregatorV3Source` interface to avoid future mistakes and separate both codebases for source and destination adapters.


***Update:** Resolved in [pull request #93](https://github.com/UMAprotocol/oev-contracts/pull/93) at commit [35d5f7c](https://github.com/UMAprotocol/oev-contracts/commit/35d5f7c0bb4c9dd7884d1a403c9d9b996b0f7fd4).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UMA Oval Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uma-oval-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

