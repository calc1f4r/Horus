---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42508
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-biconomy
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/52

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
finders_count: 0
finders:
---

## Vulnerability Title

[M-11] `LiquidityProviders`: Setting new liquidity pool will break contract

### Overview


The bug report is about a function in the LiquidityProviders contract that allows owners to change the liquidity pool. This can cause a problem for users who have added liquidity using the addTokenLiquidity function, as their tokens will be transferred to the old liquidity pool and cannot be retrieved if the liquidity pool is changed again. This can result in users losing their funds. The recommended mitigation steps include implementing a sophisticated migration mechanism and only allowing the liquidity pool to be set once. The severity of the bug has been decreased to medium as the funds are not lost forever and can be retrieved if the old liquidity pool is set again.

### Original Finding Content

_Submitted by cmichel, also found by gzeon_

[LiquidityProviders.sol#L171](https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/hyphen/LiquidityProviders.sol#L171)<br>

Owners can change the `liquidityPool` variable any time with the `setLiquidityPool` function.<br>
If a liquidity pool was already set and users added liquidity with `addTokenLiquidity`, the tokens are directly transferred to the liquidity pool and not kept in the `LiquidityProviders` contract.<br>
Changing the `liquidityPool` to a different contract will make it impossible for the users to withdraw their liquidity using `removeLiquidity` because the tokens are still in the old `liquidityPool` and cannot be retrieved.<br>

All users will lose their funds.

### Recommended Mitigation Steps

Changing the `liquidityPool` requires a sophisticated migration mechanism.<br>
Only allow setting the `liquidityPool` contract once.

**[ankurdubey521 (Biconomy) acknowledged](https://github.com/code-423n4/2022-03-biconomy-findings/issues/52)**

**[pauliax (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/52#issuecomment-1114560240):**
 > A valid concern, but I am downgrading this to Medium risk because the funds are not lost forever, the same old liquidityPool can be set again by the owner in such a case.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/52
- **Contest**: https://code4rena.com/reports/2022-03-biconomy

### Keywords for Search

`vulnerability`

