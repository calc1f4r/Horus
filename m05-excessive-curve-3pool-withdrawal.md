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
solodit_id: 10783
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/origin-dollar-audit/
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

[M05] Excessive Curve 3Pool withdrawal

### Overview


A bug has been identified in the ThreePoolStrategy contract, which is used to withdraw funds. The issue is that the number of LP tokens to burn is determined by retrieving the asset value of all LP tokens, and then scaling down linearly to the desired withdrawal amount. This means that the withdrawal will retrieve too many tokens, and any excess tokens are sent to the vault. This could be significant, as it increases as the fraction of assets invested decreases. 

To avoid this issue, the calc_token_amount function should be used to determine the number of LP tokens to burn, or the remove_liquidity_imbalance function to withdraw a specific amount of asset tokens. This issue has been partially fixed in PR#718, although the strategy contract still withdraws the maximum amount needed from the Gauge. In addition, the strict inequality in the require statement makes it impossible to withdraw the max amount of pTokens.

### Original Finding Content

When withdrawing funds from the `ThreePoolStrategy`, the number of LP tokens to burn is determined by [retrieving the asset value of all LP tokens](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/ThreePoolStrategy.sol#L178-L181), and then [scaling down linearly](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/ThreePoolStrategy.sol#L184) to the desired withdrawal amount. However, not all LP tokens are valued equally: as the size of the withdrawal increases, the value of each LP token should decrease. This means [the withdrawal](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/ThreePoolStrategy.sol#L201-L206) will retrieve too many tokens.


To account for this, any excess tokens are [sent to the vault](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/ThreePoolStrategy.sol#L209-L212). The comments and variables names suggest that the excess amount would be negligible. However, since most use cases involve withdrawing a small fraction of all the assets invested by this strategy, and the discrepancy increases as the fraction decreases, it could be significant. It is worth noting that excess funds that are sent to the vault do not automatically trigger a reallocation if they exceed the internal liquidity buffer.


To avoid excess withdrawals, consider using [the `calc_token_amount` function](https://curve.readthedocs.io/exchange-pools.html#StableSwap.calc_token_amount) to determine the number of LP tokens to burn or [the `remove_liquidity_imbalance` function](https://curve.readthedocs.io/exchange-pools.html#StableSwap.remove_liquidity_imbalance) to withdraw a specific amount of asset tokens.


**Update:** *Partially fixed in [PR#718](https://github.com/OriginProtocol/origin-dollar/pull/718). Although `remove_liquidity_imbalance` is now used to avoid excess withdrawal from Curve’s 3Pool, the strategy contract [still withdraws, at most, the maximum amount needed from the Gauge](https://github.com/OriginProtocol/origin-dollar/blob/685771c2ea2e20d73440382eb1353e67bb2f7c8e/contracts/contracts/strategies/ThreePoolStrategy.sol#L184-L191). In addition, the strict in inequality in [this require statement](https://github.com/OriginProtocol/origin-dollar/blob/685771c2ea2e20d73440382eb1353e67bb2f7c8e/contracts/contracts/strategies/ThreePoolStrategy.sol#L183) makes it impossible to withdraw the max amount of `pTokens`.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

