---
# Core Classification
protocol: Yieldy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2897
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-yieldy-contest
source_link: https://code4rena.com/reports/2022-06-yieldy
github_link: https://github.com/code-423n4/2022-06-yieldy-findings/issues/48

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - csanuragjain
---

## Vulnerability Title

[M-22] MINIMUM_LIQUIDITY checks missing - Bringing Liquidity below required min

### Overview


This bug report is about a vulnerability in the code of a contract called LiquidityReserve.sol. This vulnerability allows a whale (someone who provides a large amount of liquidity) to use the removeLiquidity function to remove all of their liquidity, leaving the residual liquidity below the minimum liquidity. This is incorrect and can be exploited. 

The proof of concept for this vulnerability is as follows: the whale provides initial liquidity plus more using the enableLiquidityReserve and addLiquidity functions. There are also other small liquidity providers. Then, the whale decides to remove all the liquidity provided, resulting in the balance liquidity dropping below the minimum liquidity. 

The recommended mitigation step is to add a check to the code that requires the balance of the staking token to be greater than or equal to the minimum liquidity, plus the amount to withdraw. This will prevent the whale from removing all of their liquidity.

### Original Finding Content

_Submitted by csanuragjain_

Whale who provided most liquidity to the contract can simply use removeLiquidity function and can remove all of his liquidity. This can leave the residual liquidity to be less than MINIMUM_LIQUIDITY which is incorrect.

### Proof of Concept

1.  Whale A provided initial liquidity plus more liquidity using enableLiquidityReserve and addLiquidity function

2.  There are other small liquidity providers as well

3.  Now Whale A decides to remove all the liquidity provided

4.  This means after liquidity removal the balance liquidity will even drop below MINIMUM_LIQUIDITY which is incorrect

### Recommended Mitigation Steps

Add below check

    require(
                IERC20Upgradeable(stakingToken).balanceOf(address(this)) - MINIMUM_LIQUIDITY >=
                    amountToWithdraw,
                "Not enough funds"
            );

**[toshiSat (Yieldy) confirmed and resolved](https://github.com/code-423n4/2022-06-yieldy-findings/issues/48)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yieldy |
| Report Date | N/A |
| Finders | csanuragjain |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-yieldy
- **GitHub**: https://github.com/code-423n4/2022-06-yieldy-findings/issues/48
- **Contest**: https://code4rena.com/contests/2022-06-yieldy-contest

### Keywords for Search

`vulnerability`

