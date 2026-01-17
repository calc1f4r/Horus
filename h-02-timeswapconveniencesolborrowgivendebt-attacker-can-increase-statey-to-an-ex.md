---
# Core Classification
protocol: Timeswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25632
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-timeswap
source_link: https://code4rena.com/reports/2022-01-timeswap
github_link: https://github.com/code-423n4/2022-01-timeswap-findings/issues/169

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
  - yield
  - services
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-02] `TimeswapConvenience.sol#borrowGivenDebt()` Attacker can increase `state.y` to an extremely large value with a dust amount of `assetOut`

### Overview


This bug report is about an issue related to the manipulation of the `state.y` variable in the Timeswap protocol. It is located in the `TimeswapConvenience.sol` file and cannot be solved by adding the `onlyConvenience` modifier. The bug report recommends removing the function as it does not make sense for the caller to specify the interest they want to pay. 

The impact of this bug is twofold. Firstly, when `pool.state.y` is extremely large, many core features of the protocol will malfunction as the arithmetic related to `state.y` can overflow. This is demonstrated in the LendMath.check() and BorrowMath.check() functions. Secondly, an attacker can set `state.y` to a near overflow value, then use the `lend()` function to get a large amount of extra interest with a small amount of asset tokens, thus stealing funds from other lenders and liquidity providers. This bug was confirmed by Mathepreneur (Timeswap).

### Original Finding Content

_Submitted by WatchPug_

<https://github.com/code-423n4/2022-01-timeswap/blob/bf50d2a8bb93a5571f35f96bd74af54d9c92a210/Timeswap/Timeswap-V1-Convenience/contracts/libraries/BorrowMath.sol#L19-L53>

This issue is similar to the two previous issues related to `state.y` manipulation. Unlike the other two issues, this function is not on `TimeswapPair.sol` but on `TimeswapConvenience.sol`, therefore this can not be solved by adding `onlyConvenience` modifier.

Actually, we believe that it does not make sense for the caller to specify the interest they want to pay, we recommend removing this function.

#### Impact

*   When `pool.state.y` is extremely large, many core features of the protocol will malfunction, as the arithmetic related to `state.y` can overflow. For example:

LendMath.check(): <https://github.com/code-423n4/2022-01-timeswap/blob/bf50d2a8bb93a5571f35f96bd74af54d9c92a210/Timeswap/Timeswap-V1-Core/contracts/libraries/LendMath.sol#L28-L28>

BorrowMath.check(): <https://github.com/code-423n4/2022-01-timeswap/blob/bf50d2a8bb93a5571f35f96bd74af54d9c92a210/Timeswap/Timeswap-V1-Core/contracts/libraries/BorrowMath.sol#L31-L31>

*   An attacker can set `state.y` to a near overflow value, then `lend()` to get a large amount of extra interest (as Bond tokens) with a small amount of asset tokens. This way, the attacker can steal funds from other lenders and liquidity providers.

**[Mathepreneur (Timeswap) confirmed](https://github.com/code-423n4/2022-01-timeswap-findings/issues/169)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Timeswap |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-timeswap
- **GitHub**: https://github.com/code-423n4/2022-01-timeswap-findings/issues/169
- **Contest**: https://code4rena.com/reports/2022-01-timeswap

### Keywords for Search

`vulnerability`

