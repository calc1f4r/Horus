---
# Core Classification
protocol: UMA Audit – Phase 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11426
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-audit-phase-2/
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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M01] Sponsors can delay liquidations

### Overview


This bug report is about the UMA Protocol which is a financial platform. It states that any under-collateralized sponsor is able to delay liquidation attempts by transferring their position to another address that they control before the liquidation transaction is processed. This would cause the liquidation to fail. It also states that sponsors that recognize they are about to be liquidated would redeem their position. However, if they are able to delay liquidation for long enough, they could keep the global collateralization ratio artificially depressed, potentially below the collateralization requirement. This would allow them to create under-collateralized positions or withdraw excessive collateral. In the worst-case scenario, sponsors could delay liquidation until they are insolvent. 

To fix this bug, it was suggested to delay position transfers for a short time window, treating them similar to slow withdrawal requests. This was fixed in PR#1314, where transfers of positions are now delayed for the same duration as slow withdrawal requests.

### Original Finding Content

Any under-collateralized sponsor can delay liquidation attempts by [transferring their position](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/PricelessPositionManager.sol#L165) to another address that they control before the [liquidation transaction targeted at the old address](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/Liquidatable.sol#L188) is processed. This would cause the liquidation to fail.


In most cases, sponsors that recognize that are about to be liquidated would [redeem their position](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/PricelessPositionManager.sol#L336). However, were sponsors able to successfully delay liquidation for long enough, they could keep the [global collateralization ratio](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/PricelessPositionManager.sol#L621-L624) artificially depressed, potentially below the [collateralization requirement](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/Liquidatable.sol#L90). In this scenario, sponsors would be able to [create under-collateralized positions](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/PricelessPositionManager.sol#L303) or [withdraw excessive collateral](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/PricelessPositionManager.sol#L201). In the extreme case, sponsors could delay liquidation until they were insolvent.


Consider delaying position transfers for a short time window, thereby treating them similar to slow withdrawals.


**Update:** *Fixed in [PR#1314](https://github.com/UMAprotocol/protocol/pull/1314). Transfers of positions are now delayed for the same duration as slow withdrawal requests.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UMA Audit – Phase 2 |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uma-audit-phase-2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

