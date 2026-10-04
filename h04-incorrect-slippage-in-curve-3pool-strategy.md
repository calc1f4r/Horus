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
solodit_id: 10777
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

[H04] Incorrect slippage in Curve 3Pool strategy

### Overview


This bug report concerns the `ThreePoolStrategy` contract used for withdrawing funds. The parameter used to control slippage is incorrectly calculated as a fraction of the burned LP tokens, which is not a meaningful value and may cause the withdrawal to fail unexpectedly. To avoid this, the parameter should be set to `_amount`, which would match the current behavior while avoiding the failure. This suggestion does not protect against a front-running attack or sandwich attack, however, and the `ThreePoolStrategy` contract would need the fair market rate of LP tokens denominated in the asset to withdraw. The bug has been partially fixed by a pull request, but the `withdraw` function still does not protect against front-running or sandwich attacks.

### Original Finding Content

When withdrawing funds from the `ThreePoolStrategy`, LP tokens [are exchanged](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/ThreePoolStrategy.sol#L201-L205) for the underlying asset. To control slippage, a [minimum asset amount](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/ThreePoolStrategy.sol#L204) to receive is specified.


However, the actual parameter does not match the intended usage. Instead, it is calculated as a fraction of the burned LP tokens, scaled so it has the same precision as the asset to withdraw. This is not a meaningful value, and when interpreted as an asset quantity, it may be more than the burned LP tokens are worth. In this scenario, the liquidity removal will fail unexpectedly.


To avoid this scenario, consider setting this parameter to `_amount`. Given the way the number of tokens to burn [was calculated](https://github.com/OriginProtocol/origin-dollar/blob/bf4ff28d5944ecc277e66294fd2c702fee5cd58b/contracts/contracts/strategies/ThreePoolStrategy.sol#L184), they will always exchange for `_amount` of assets at least. This would match the current behavior while avoiding the possibility of an unnecessary failure to withdraw.


Unfortunately, this suggestion does not protect against a front-running attack or sandwich attack, where the instantaneous state of the Curve protocol differs significantly from market equilibrium. To mitigate this, the `ThreePoolStrategy` contract would need the fair market rate of LP tokens denominated in the asset to withdraw.


**Update:** *Partially fixed by [PR#716](https://github.com/OriginProtocol/origin-dollar/pull/716). The `withdraw` function will now remove at least `_amount` from Curve’s 3Pool. Note, however, that the `withdraw` function still does not protect against front-running or sandwich attacks.*

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

