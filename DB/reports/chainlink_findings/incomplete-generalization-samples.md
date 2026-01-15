---
# Core Classification
protocol: ERC-4337 Account Abstraction Incremental Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32542
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/erc-4337-account-abstraction-incremental-audit
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

Incomplete Generalization [samples]

### Overview

See description below for full details.

### Original Finding Content

The `TokenPaymaster` refers to the [native asset](https://github.com/eth-infinitism/account-abstraction/blob/9879c931ce92f0bee1bca1d1b1352eeb98b9a120/contracts/samples/TokenPaymaster.sol#L56) and a [bridging asset](https://github.com/eth-infinitism/account-abstraction/blob/9879c931ce92f0bee1bca1d1b1352eeb98b9a120/contracts/samples/utils/OracleHelper.sol#L122), but also explicitly mentions [Ether and dollars](https://github.com/eth-infinitism/account-abstraction/blob/9879c931ce92f0bee1bca1d1b1352eeb98b9a120/contracts/samples/utils/OracleHelper.sol#L36-L40). This is not purely descriptive. It also assumes that the Chainlink price [is updated every 24 hours](https://github.com/eth-infinitism/account-abstraction/blob/9879c931ce92f0bee1bca1d1b1352eeb98b9a120/contracts/samples/utils/OracleHelper.sol#L161), even though different Chainlink oracles can have [wildly different heartbeats](https://docs.chain.link/data-feeds/price-feeds/addresses?network=ethereum&page=1), ranging from 1 hour to 48 hours.


Consider choosing a specific configuration, or making all parameters and comments generic.


***Update:** Resolved in [pull request #425](https://github.com/eth-infinitism/account-abstraction/pull/425).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | ERC-4337 Account Abstraction Incremental Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/erc-4337-account-abstraction-incremental-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

