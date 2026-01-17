---
# Core Classification
protocol: f(x) v2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61793
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fx-v2-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Pool at Capacity Cannot Be Liquidated

### Overview


The `PoolManager` contract has a maximum capacity for each pool's collateral. The `_changePoolCollateral` function will reject any changes that exceed this capacity. When a pool has bad debt, the protocol uses funds from the `ReservePool` to cover it. However, when liquidating a pool, the funds from the reserve are added to the pool's collateral amount. This can cause the liquidation to fail if the total amount exceeds the pool's capacity. The suggestion is to subtract the liquidation collateral before adding the reserve's funds to the pool's collateral. The f(x) Protocol team has acknowledged the issue but has decided not to make any changes at this time due to the low likelihood of it occurring and minimal impact on users.

### Original Finding Content

Each pool in the `PoolManager` contract has a maximum capacity of collateral that it can hold. The `_changePoolCollateral` function [reverts if the change surpasses the capacity](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/PoolManager.sol#L688). When a tick has bad debt, the protocol uses funds from the `ReservePool` contract to cover the uncollateralized part of the debt to be able to facilitate the liquidation.

When a pool is liquidated through the [`liquidate` function](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/PoolManager.sol#L386) of the `PoolManager` contract, the funds pulled from the reserve are [added to the current pool's collateral amount](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/PoolManager.sol#L416). If the sum of the funds from the reserve and the current balance surpasses the capacity (i.e., capacity<bonusFromReserve+balancecapacity < bonusFromReserve + balancecapacity<bonusFromReserve+balance), the liquidation will fail.

Consider adding the reserve's funds to the pool collateral variables after the liquidation collateral has been subtracted.

***Update:** Acknowledged, not resolved. The f(x) Protocol team stated:*

> *The case is rare, and given the low likelihood of it occurring in practice, we have opted not to make any changes at this time. The current implementation maintains simpler and more predictable behavior, and modifying the reserve collateral logic could introduce unnecessary complexity for an edge case that has minimal user impact.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | f(x) v2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fx-v2-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

