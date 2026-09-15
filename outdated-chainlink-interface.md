---
# Core Classification
protocol: Venus Protocol Oracles Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33089
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/venus-protocol-oracles-audit
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

Outdated Chainlink Interface

### Overview

See description below for full details.

### Original Finding Content

In [line 201 of `ChainlinkOracle`](https://github.com/VenusProtocol/oracle/blob/78b1a411c42e5c103e688e4e76bc69c476206833/contracts/oracles/ChainlinkOracle.sol#L201), the interface `AggregatorV2V3Interface` is used, which inherits from both the `AggregatorInterface` and the `AggregatorV3Interface`. Chainlink recommends using the `AggregatorV3Interface`, as shown in [its documentation](https://docs.chain.link/data-feeds/api-reference). This prevents the usage of deprecated functions in the `AggregatorInterface`, which do not throw errors if no answer has been reached, but instead return 0. The dependence on this unexpected behavior increases the attack surface for the calling contract.


Consider updating the interface used in the `ChainlinkOracle` from `AggregatorV2V3Interface` to `AggregatorV3Interface`.


***Update:** Resolved in [pull request #84](https://github.com/VenusProtocol/oracle/pull/84) at commit [ddd4b02](https://github.com/VenusProtocol/oracle/pull/84/commits/ddd4b0222e40f1b6accf4f003face5206e947489).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Venus Protocol Oracles Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/venus-protocol-oracles-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

