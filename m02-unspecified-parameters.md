---
# Core Classification
protocol: MCDEX Mai Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11404
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/mcdex-mai-protocol-audit/
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
  - services
  - derivatives
  - rwa
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M02] Unspecified parameters

### Overview


This bug report is about the maximum position amount to liquidate when a user liquidates another position and the liquidation price and position side that is inferred contextually from the current mark price and the state of the target account. It also discusses the price that is inferred contextually when creating an AMM pool, adding liquidity, or removing liquidity. The bug report suggests that the user should be allowed to specify an acceptable price range and a deadline for when the action expires. This would make the liquidation and other actions more predictable. However, the Monte Carlo team have decided not to address this issue.

### Original Finding Content

When a user liquidates another position, they [specify the maximum position amount to liquidate](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/perpetual/Perpetual.sol#L291). However, the [liquidation price](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/perpetual/Perpetual.sol#L274) and [position side](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/perpetual/Position.sol#L267) is inferred contextually from the current mark price and the state of the target account. These values could change before the liquidation is confirmed, particularly during periods of high Ethereum congestion. In many cases the liquidator would accept any successful liquidation, but for the sake of predictability, consider allowing the liquidator to specify an acceptable price range, the side of the positions to liquidate and a deadline for when the liquidation attempt expires.


Similarly, when [creating the AMM pool](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/liquidity/AMM.sol#L162), [adding liquidity](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/liquidity/AMM.sol#L267) or [removing liquidity](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/liquidity/AMM.sol#L288), the price is inferred contextually. In the case of adding or removing liquidity, it could even change based on the actions of other users in the same block. Consider allowing the user to specify an acceptable price range and a deadline for when the action expires.


**Update:** *Acknowledged. The Monte Carlo team have decided not to address this issue.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | MCDEX Mai Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/mcdex-mai-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

