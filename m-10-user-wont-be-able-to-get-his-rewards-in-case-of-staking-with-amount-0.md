---
# Core Classification
protocol: Behodler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42462
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-behodler
source_link: https://code4rena.com/reports/2022-01-behodler
github_link: https://github.com/code-423n4/2022-01-behodler-findings/issues/146

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
  - cross_chain
  - services
  - cdp
  - dexes
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-10] user won't be able to get his rewards in case of staking with amount = 0

### Overview


This bug report is about an issue with the `stake()` function in the Limbo.sol contract. If a user has a pending reward and calls the function with an `amount` parameter of 0, they will not receive their reward and the reward debt will cover it. This is because the reward calculation is only done if the staked amount is greater than 0, and the reward debt is updated even if the amount is 0. A developer has confirmed and commented on the issue, suggesting that the simplest solution is to remove the if statement, but a judge has increased the severity from Low to Medium as users can lose their rewards.

### Original Finding Content

_Submitted by CertoraInc, also found by Randyyy_

#### Limbo.sol (`stake()` function)

If a user has a pending reward and he calls the `stake` function with `amount = 0`, he won't be able to get his reward (he won't get the reward, and the reward debt will cover the reward)

That's happening because the reward calculation is done only if the staked amount (given as a parameter) is greater than 0, and it updates the reward debt also if the amount is 0, so the reward debt will be updated without the user will be able to get his reward

**[gititGoro (Behodler) confirmed and commented](https://github.com/code-423n4/2022-01-behodler-findings/issues/146#issuecomment-1029415967):**
 > Good catch! I'd be interested in your mitigation step being provided. 
> 
> To me, it looks like the simplest solution is just to remove that if statement. Users who stake zero will pay unnecessary gas costs but the contract shouldn't have to optimise gas consumption for undesired behaviour.

**[Jack the Pug (judge) increased severity from Low to Medium and commented](https://github.com/code-423n4/2022-01-behodler-findings/issues/146#issuecomment-1053338078):**
 > Upgraded to `Med` as users can lose their rewards.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Behodler |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-behodler
- **GitHub**: https://github.com/code-423n4/2022-01-behodler-findings/issues/146
- **Contest**: https://code4rena.com/reports/2022-01-behodler

### Keywords for Search

`vulnerability`

