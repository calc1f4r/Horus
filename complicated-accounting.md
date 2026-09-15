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
solodit_id: 10483
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/origin-dollar-audit-2/
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

Complicated accounting

### Overview

See description below for full details.

### Original Finding Content

The `withdraw` function of the `BaseCurveStrategy` determines the number of 3CRV tokens to burn by using the price to [slightly overestimate](https://github.com/OriginProtocol/origin-dollar/blob/bfe0ac8e5d7c05b9bf1021fafb25e0aed8a6ed45/contracts/contracts/strategies/BaseCurveStrategy.sol#L134-L137) the desired value, [determining the corresponding amount](https://github.com/OriginProtocol/origin-dollar/blob/53448a5801e81208cf36fbcba908862c7a21a6ca/contracts/contracts/strategies/BaseCurveStrategy.sol#L141-L144) of stablecoin, and then [scaling down the LP amount](https://github.com/OriginProtocol/origin-dollar/blob/53448a5801e81208cf36fbcba908862c7a21a6ca/contracts/contracts/strategies/BaseCurveStrategy.sol#L146) linearly to match the required stablecoin value. Instead, consider directly querying the amount of LP tokens to burn with the [`calc_token_amount` function](https://curve.readthedocs.io/exchange-pools.html#StableSwap.calc_token_amount), and then adjusting for fees. If desired, the amount could be validated with the [`calc_withdraw_one_coin` function](https://curve.readthedocs.io/exchange-pools.html#StableSwap.calc_withdraw_one_coin).


**Update:** *Acknowledged, not resolved. The Origin team stated:*



> *calc\_token\_amount does not account for curve fees. Correctly accounting for way curve fees are calculated ends up being more code than the current method.*
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Origin Dollar Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/origin-dollar-audit-2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

