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
solodit_id: 1639
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest
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
finders_count: 2
finders:
  - cmichel
  - gzeon
---

## Vulnerability Title

[M-11] LiquidityProviders: Setting new liquidity pool will break contract

### Overview


A bug has been identified in the code of the LiquidityProviders.sol contract, which is part of the 2022-03-biconomy GitHub repository. This bug allows the owners of the contract to change the liquidityPool variable at any time using the setLiquidityPool function. This could lead to users losing their funds if they have already added liquidity with the addTokenLiquidity function, as the tokens are transferred directly to the liquidityPool and not kept in the LiquidityProviders contract. If the liquidityPool is changed, users will not be able to withdraw their funds using the removeLiquidity function. 

The recommended mitigation step to prevent this bug is to only allow the liquidityPool to be set once. This will require a sophisticated migration mechanism to be implemented.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/hyphen/LiquidityProviders.sol#L171


## Vulnerability details

## Impact
Owners can change the `liquidityPool` variable any time with the `setLiquidityPool` function.
If a liquidity pool was already set and users added liquidity with `addTokenLiquidity`, the tokens are directly transferred to the liquidity pool and not kept in the `LiquidityProviders` contract.
Changing the `liquidityPool` to a different contract will make it impossible for the users to withdraw their liquidity using `removeLiquidity` because the tokens are still in the old `liquidityPool` and cannot be retrieved.

All users will lose their funds.

## Recommended Mitigation Steps
Changing the `liquidityPool` requires a sophisticated migration mechanism.
Only allow setting the `liquidityPool` contract once.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | cmichel, gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/52
- **Contest**: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest

### Keywords for Search

`vulnerability`

