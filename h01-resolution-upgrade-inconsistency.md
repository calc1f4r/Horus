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
solodit_id: 10774
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

[H01] Resolution upgrade inconsistency

### Overview


A bug report was submitted for the OUSD token, a digital currency that achieves its rebasing functionality by tracking credit balances and scaling them by a conversion factor. The `OUSDResolutionUpgrade` contract was designed as a temporary logic contract to increase the precision of the conversion factors. This contract has two functions, one to update the global parameters and one to upgrade individual user accounts in batches.

The bug reported was that there was no access control on either of these functions, meaning an attacker could include the zero address in a batch of account upgrades, which would set its flag and prevent anyone from upgrading the global state. This could produce an inconsistent state where a subset of the accounts use the new resolution, while the global parameters remain unchanged. The suggested solution was to restrict the `upgradeAccounts` function to non-zero accounts.

The bug was fixed in commit 95e8c90.

### Original Finding Content

The OUSD token achieves its rebasing functionality by tracking credit balances and scaling them by a conversion factor to retrieve the corresponding OUSD token balances. The `OUSDResolutionUpgrade` contract is designed as a temporary logic contract that replaces the token functionality with mechanisms to increase the precision of the conversion factors. In particular, there is [a function](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/token/OUSDResolutionUpgrade.sol#L8) to update the global parameters and [a separate function](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/token/OUSDResolutionUpgrade.sol#L17) to upgrade the individual user accounts in batches.


To avoid upgrading the same account multiple times, [an upgrade flag is set](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/token/OUSDResolutionUpgrade.sol#L21) for each account. Similarly, [the upgrade flag is set](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/token/OUSDResolutionUpgrade.sol#L10) for the zero address to indicate that the global parameters have been updated. There is no access control on either of these functions. This means that an attacker can include the zero address in a batch of account upgrades, which will set its flag and prevent anyone from upgrading the global state. This could produce an inconsistent state where a subset of the accounts use the new resolution, while the global parameters remain unchanged.


Consider restricting the `upgradeAccounts` function to non-zero account.


**Update:** *Fixed in [commit 95e8c90](https://github.com/OriginProtocol/origin-dollar/commit/95e8c90afbe9103d14e2dfba875acce08f108d3c).*

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

