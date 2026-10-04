---
# Core Classification
protocol: Origin OETH Integration Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33094
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/origin-oeth-integration-audit
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

Minting is still possible even if redemptions are not

### Overview

See description below for full details.

### Original Finding Content

When redeeming OUSD or OETH, the corresponding amount of each collateral token is [calculated](https://github.com/OriginProtocol/origin-dollar/blob/508921bd39f988fa61b60cea372b910725ff7bd0/contracts/contracts/vault/VaultCore.sol#L165). The operation will fail if any of the tokens [drift too far](https://github.com/OriginProtocol/origin-dollar/blob/508921bd39f988fa61b60cea372b910725ff7bd0/contracts/contracts/vault/VaultCore.sol#L695) from the expected price. However, when minting new OUSD or OETH, [only the deposited collateral](https://github.com/OriginProtocol/origin-dollar/blob/508921bd39f988fa61b60cea372b910725ff7bd0/contracts/contracts/vault/VaultCore.sol#L74) needs to be within the acceptable range. This introduces the possibility that users can deposit funds but will be unable to withdraw them.


In the interest of predictability, consider preventing deposits unless all collateral tokens are redeemable. This would help ensure that deposits and withdrawals are enabled and disabled together during unexpected market conditions.


***Update:** Acknowledged, not resolved. The Origin team stated:*



> *For code simplicity, OUSD/OETH prioritizes protecting the protcool over protecting interacting users. If a user mints with a non-depegged coin when another coin is depegged, this is a benefit for the protocol.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Origin OETH Integration Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/origin-oeth-integration-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

