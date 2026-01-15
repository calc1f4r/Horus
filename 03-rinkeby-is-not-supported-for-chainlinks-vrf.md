---
# Core Classification
protocol: Art Gobblers
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25404
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-artgobblers
source_link: https://code4rena.com/reports/2022-09-artgobblers
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
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[03]  Rinkeby is not supported for Chainlink's VRF

### Overview

See description below for full details.

### Original Finding Content

Rinkeby is deprecated and not listed as supported for [Chainlink](https://docs.chain.link/docs/vrf/v1/supported-networks/). The documentation states `Once the Ethereum mainnet transitions to proof-of-stake, Rinkeby will no longer be an accurate staging environment for mainnet. ... Developers who currently use Rinkeby as a staging/testing environment should prioritize migrating to Goerli or Sepolia` [link](https://blog.ethereum.org/2022/06/21/testnet-deprecation)

*There is 1 instance of this issue:*
```solidity
File: /script/deploy/DeployRinkeby.s.sol

6:   contract DeployRinkeby is DeployBase {

```
https://github.com/code-423n4/2022-09-artgobblers/blob/d2087c5a8a6a4f1b9784520e7fe75afa3a9cbdbe/script/deploy/DeployRinkeby.s.sol#L6



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Art Gobblers |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-artgobblers
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-09-artgobblers

### Keywords for Search

`vulnerability`

