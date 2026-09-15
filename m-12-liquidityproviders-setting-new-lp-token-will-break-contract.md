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
solodit_id: 42509
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-biconomy
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/51

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

[M-12] `LiquidityProviders`: Setting new LP token will break contract

### Overview


This bug report highlights an issue with the `setLpToken` function in the LiquidityProviders.sol contract. The function allows owners to change the `lpToken` variable at any time, but if this is done after users have added liquidity and received a `lpToken` NFT, they will not be able to withdraw their funds using `removeLiquidity`. This could result in users losing their funds. The recommended mitigation steps include implementing a sophisticated migration mechanism and only allowing the `lpToken` contract to be set once. The severity of this bug has been decreased to Medium, as the funds are not lost forever and can be recovered by setting the old `lpToken` again. 

### Original Finding Content

_Submitted by cmichel, also found by gzeon_

[LiquidityProviders.sol#L116](https://github.com/code-423n4/2022-03-biconomy/blob/db8a1fdddd02e8cc209a4c73ffbb3de210e4a81a/contracts/hyphen/LiquidityProviders.sol#L116)<br>

Owners can change the `lpToken` variable at any time with the `setLpToken` function.<br>
If an LP token was already set and users added liquidity with `addTokenLiquidity` and were minted a `lpToken` NFT, changing the `lpToken` to a different contract will make it impossible for the users to withdraw their liquidity using `removeLiquidity`.<br>

All users will lose their funds.

### Recommended Mitigation Steps

Changing the `lpToken` requires a sophisticated migration mechanism.<br>
Only allow setting the `lpToken` contract once.

**[ankurdubey521 (Biconomy) acknowledged](https://github.com/code-423n4/2022-03-biconomy-findings/issues/51)**

**[pauliax (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/51#issuecomment-1114560361):**
 > A valid concern, but I am downgrading this to Medium risk because the funds are not lost forever, the same old lpToken can be set again by the owner in such a case.



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
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/51
- **Contest**: https://code4rena.com/reports/2022-03-biconomy

### Keywords for Search

`vulnerability`

