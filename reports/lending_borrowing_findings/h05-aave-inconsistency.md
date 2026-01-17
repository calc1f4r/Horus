---
# Core Classification
protocol: Origin Dollar Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10778
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/origin-dollar-audit/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H05] AAVE inconsistency

### Overview


A bug was reported in the `AaveStrategy` contract which uses the version 2 interface. The bug was identified in two inconsistencies: the strategy attempted to grant an allowance to the non-existent Lending Pool Core instead of the Lending Pool, and the strategy used the outdated `redeem` function in the `withdrawAll` function. The Origin team had already identified and addressed the first inconsistency in a subsequent commit. The bug has been fixed in the commit 650913e.

### Original Finding Content

The `AaveStrategy` contract uses the [version 2 interface](https://docs.aave.com/developers/v/2.0/) in anticipation of a future reconfiguration of the investment strategies. However, we identified two inconsistencies:


* the strategy [attempts to grant an allowance](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/AaveStrategy.sol#L186) to the non-existent Lending Pool Core, instead of the Lending Pool, which would make the strategy unusable and prevent OUSD token mints whenever the strategy is in use.
* the strategy uses the [outdated `redeem` function](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/AaveStrategy.sol#L129) in the `withdrawAll` function, which is called when [the strategy is removed](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/vault/VaultAdmin.sol#L189).


When this was raised with the Origin team they indicated that they had already identified and addressed the first inconsistency in a subsequent commit. Consider using the new interface when withdrawing all tokens.


**Update:** *Fixed in [commit 650913e](https://github.com/OriginProtocol/origin-dollar/commit/650913e027900a3ecbb85c14ac269b043c2a7239).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Origin Dollar Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/origin-dollar-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

