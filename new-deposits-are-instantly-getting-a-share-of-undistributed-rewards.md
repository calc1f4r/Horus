---
# Core Classification
protocol: GrowthDeFi WHEAT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13360
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/06/growthdefi-wheat/
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
  - dexes
  - cdp
  - yield
  - services
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Sergii Kravchenko
  - David Oz Kashi
  -  Dominik Muhs
---

## Vulnerability Title

New deposits are instantly getting a share of undistributed rewards

### Overview


A bug report was submitted regarding an issue with deposits and withdrawals in a system. When a new deposit is made, the current pending rewards are not withdrawn and reinvested, and are not taken into account when calculating the number of shares the depositor receives. Furthermore, all withdrawals are also happening without considering the pending rewards. This creates an attack vector where an attacker can make a deposit right before the `gulp` function is called, and then withdraw, receiving guaranteed profit. This can be done with a flash loan or a regular loan, and the risk is not very high as no price manipulation is required.

The recommended solution is to include the `gulp` call at the beginning of the `deposit` and `withdraw`, with an option to avoid calling `gulp` in the case of withdrawing. The issue was addressed in commit 34c6b355795027d27ae6add7360e61eb6b01b91b.

### Original Finding Content

#### Resolution



The client communicated this issue was addressed in commit 34c6b355795027d27ae6add7360e61eb6b01b91b.


#### Description


When a new deposit is happening, the current pending rewards are not withdrawn and re-invested yet. And they are not taken into account when calculating the number of shares that the depositor receives. The number of shares is calculated as if there were no pending rewards.
The other side of this issue is that all the withdrawals are also happening without considering the pending rewards. So currently, it makes more sense to withdraw right after `gulp` to gather the rewards.
In addition to the general “unfairness” of the reward distribution during the deposit/withdrawal, there is also an attack vector created by this issue.


**The Attack**


If the deposit is made right before the `gulp` function is called, the rewards from the `gulp` are distributed evenly across all the current deposits, including the ones that were just recently made. So if the deposit-gulp-withdraw sequence is executed, the caller receives guaranteed profit. If the attacker also can execute these functions briefly (in one block or transaction) and take a huge loan to deposit a lot of tokens, almost all the rewards from the gulp will be stolen by the attacker.
The easy 1-transaction attack with a flashloan can be done by the owner, miner, whitelisted contracts, or any contract if the `onlyEOAorWhitelist` modifier is disabled or stops working (<https://github.com/ConsenSys/growthdefi-audit-2021-06/issues/3)>. Even if `onlyEOAorWhitelist` is working properly, anyone can take a regular loan to make the attack. The risk is not that big because no price manipulation is required. The price will likely remain the same during the attack (few blocks maximum).


#### Recommendation


If issue [issue 6.3](#proactive-sandwiching-of-the-gulp-calls) is fixed while allowing anyone call the gulp contract, the best solution would be to include the `gulp` call at the beginning of the `deposit` and `withdraw`. In case of withdrawing, there should also be an option to avoid calling `gulp` as the emergency case.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | GrowthDeFi WHEAT |
| Report Date | N/A |
| Finders | Sergii Kravchenko, David Oz Kashi,  Dominik Muhs |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/06/growthdefi-wheat/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

