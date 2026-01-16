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
solodit_id: 11425
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-audit-phase-2/
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

[H02] Sponsors can force liquidation of insolvent positions

### Overview


UMA protocol is a financial contracts platform that allows users to create and trade synthetic tokens. Liquidators are responsible for liquidating positions that are under-collateralized. However, they cannot specify a minimum collateral-to-token ratio, which can lead to liquidators accidentally liquidating an insolvent position. This can result in liquidators burning their tokens with insufficient compensation. 

There are two attack vectors that can be used to exploit this vulnerability. The first attack vector is when the position about to be liquidated is the only open position, the sponsor can redeem their tokens, reducing the global collateralization ratio to zero and then creating an insolvent position. The second attack vector is if the liquidation is processed late enough, the sponsor might simply complete a slow withdrawal before being liquidated.

To prevent liquidators from accidentally liquidating an insolvent position, it is suggested to include a minimum collateral-to-token ratio. This bug has since been fixed in PR#1351.

### Original Finding Content

Liquidators specify a maximum [collateral-to-token ratio](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/Liquidatable.sol#L190) to ensure they do not accidentally liquidate a position that is collateralized. However, they cannot indicate a minimum collateral-to-token ratio. If the liquidation is front-run in such a way that the target position becomes insolvent (not just under-collateralized), the liquidator will end up [burning their tokens](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/Liquidatable.sol#L267-L268) with insufficient compensation. We have identified two possible attack vectors:


* A) If the position about to be liquidated is the only open position, the sponsor can [redeem their tokens](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/PricelessPositionManager.sol#L336) (which reduces the [global collateralization ratio](https://docs.umaproject.org/uma/synthetic_tokens/glossary.html#_global_collateralization_ratio_gcr) to zero) and then [create an insolvent position](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/PricelessPositionManager.sol#L303).
* B) If the liquidation is processed late enough, the sponsor might simply complete a slow withdrawal before being liquidated.


Consider including a minimum collateral-to-token ratio to prevent liquidators from accidentally liquidating an insolvent position.


**Update:** *Fixed in [PR#1351](https://github.com/UMAprotocol/protocol/pull/1351).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

