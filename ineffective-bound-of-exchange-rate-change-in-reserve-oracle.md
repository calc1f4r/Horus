---
# Core Classification
protocol: Ion Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32703
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ion-protocol-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Ineffective Bound of Exchange Rate Change in Reserve Oracle

### Overview


The ReserveOracle contract has a restriction on how much the current exchange rate can change when the updateExchangeRate function is called. However, this restriction only applies each time the function is called and can be easily bypassed by calling the function multiple times in a single transaction. This can be exploited by an attacker to manipulate the price and liquidate users. To prevent this, it is suggested to implement a time or block-based restriction on large price changes. This issue has been resolved in a recent pull request.

### Original Finding Content

In the [`ReserveOracle` contract](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/reserve/ReserveOracle.sol), a `MAX_CHANGE` percentage bound is enforced that determines the maximum amount the `currentExchangeRate` can change when the `updateExchangeRate` function is called. This restriction only applies each time the function is called and there is no restriction on how much the exchange rate can change within a single block or transaction. The `MAX_CHANGE` bound can be easily bypassed by calling `updateExchangeRate` multiple times in a single transaction.


The reserve oracle is used within the `Liquidation` contract to determine the [value of collateral](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/Liquidation.sol#L168) when determining if a vault is liquidatable. Since the reserve oracle [computes the exchange rate](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/reserve/ReserveOracle.sol#L95-L105) as the minimum of the protocol exchange rate and an averaged price from external price feeds, if an attacker were to have sufficient control over any of the [price feeds](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/reserve/ReserveOracle.sol#L20-L22), or was able to manipulate the [protocol exchange rate](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/oracles/reserve/ReserveOracle.sol#L35), they would be able to move the price enough within a single transaction to liquidate users by undervauling their collateral.


Consider either using a time or block-based maximum change percentage to limit large price changes to longer periods of time and prevent single transaction attack scenarios.


***Update:** Resolved in [pull request #32](https://github.com/Ion-Protocol/ion-protocol/pull/32).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ion Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ion-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

