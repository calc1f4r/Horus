---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: pre/post_balance

# Attack Vector Details
attack_type: pre/post_balance
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4077
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-yield-contest
source_link: https://code4rena.com/reports/2021-05-yield
github_link: https://github.com/code-423n4/2021-05-yield-findings/issues/16

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - pre/post_balance
  - from=to

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-01] Duplication of Balance

### Overview


This bug report is about a vulnerability in the Cauldron smart contract, which allows users to duplicate the amount of ink or art held within the contract. This is done by exploiting the stir function of the Cauldron, which caches balances in memory before decrementing and incrementing. As a result, if a transfer to self is performed, the assignment balances[to] = balancesTo will contain the added-to balance instead of the neutral balance. This allows users to duplicate any number of ink or art units at will, which could have severe consequences on the integrity of the protocol. The code referenced in the bug report can be found at the given link. The recommended mitigation step is to impose a require check that prohibits the from and to variables to be equivalent.

### Original Finding Content


It is possible to duplicate currently held `ink` or `art` within a Cauldron, thereby breaking the contract's accounting system and minting units out of thin air.

The `stir` function of the `Cauldron`, which can be invoked via a `Ladle` operation, caches balances in memory before decrementing and incrementing. As a result, if a transfer to self is performed, the assignment `balances[to] = balancesTo` will contain the added-to balance instead of the neutral balance.

This allows one to duplicate any number of `ink` or `art` units at will, thereby severely affecting the protocol's integrity. A similar attack was exploited in the third bZx hack resulting in a roughly 8 million loss.

Recommend that a `require` check should be imposed prohibiting the `from` and `to` variables to be equivalent.

**[albertocuestacanada (Yield) confirmed](https://github.com/code-423n4/2021-05-yield-findings/issues/16#issuecomment-852044133):**
 > It is a good finding and a scary one. It will be fixed. Duplicated with #7.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-yield
- **GitHub**: https://github.com/code-423n4/2021-05-yield-findings/issues/16
- **Contest**: https://code4rena.com/contests/2021-05-yield-contest

### Keywords for Search

`Pre/Post Balance, from=to`

