---
# Core Classification
protocol: Blueberry
chain: everychain
category: uncategorized
vulnerability_type: deposit/reward_tokens

# Attack Vector Details
attack_type: deposit/reward_tokens
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6641
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/41
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/140

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - deposit/reward_tokens
  - missing-logic

protocol_categories:
  - leveraged_farming
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jeiwan
  - cducrest-brainbot
  - rvierdiiev
---

## Vulnerability Title

H-4: Fail to accrue interests on multiple token positions

### Overview


This bug report is about an issue in the BlueBerryBank.sol smart contract. The functions `borrow`, `repay`, `lend`, or `withdrawLend` call `poke(token)` to trigger interest accrual on the concerned token, but fail to do so for other token debts of the concerned position. This could lead to wrong calculation of position's debt and whether the position is liquidatable. 

The calculation of whether a position is liquidatable takes into account all the different debt tokens within the position, but the debt accrual has been triggered only for one of these tokens. This results in the debt value of the position being lower than what it should be and a position seen as not liquidatable while it should be liquidatable. 

The impact of this bug is that users may be able to operate on their position leading them in a virtually liquidatable state while not reverting as interests were not applied. This will worsen the debt situation of the bank and lead to overall more liquidatable positions.

The bug was found by cducrest-brainbot, rvierdiiev, and Jeiwan, and was identified using manual review. The recommendation is to review how token interests are triggered and to accrue interests on every debt token of a position at the beginning of execute.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/140 

## Found by 
cducrest-brainbot, rvierdiiev, Jeiwan

## Summary

In `BlueBerryBank.sol` the functions `borrow`, `repay`, `lend`, or `withdrawLend` call `poke(token)` to trigger interest accrual on concerned token, but fail to do so for other token debts of the concerned position.  This could lead to wrong calculation of position's debt and whether the position is liquidatable.

## Vulnerability Detail

Whether a position is liquidatable or not is checked at the end of the `execute` function, the execution should revert if the position is liquidatable. 

The calculation of whether a position is liquidatable takes into account all the different debt tokens within the position. However, the debt accrual has been triggered only for one of these tokens, the one concerned by the executed action. For other tokens, the value of `bank.totalDebt` will be lower than what it should be. This results in the debt value of the position being lower than what it should be and a position seen as not liquidatable while it should be liquidatable. 

## Impact

Users may be able to operate on their position leading them in a virtually liquidatable state while not reverting as interests were not applied. This will worsen the debt situation of the bank and lead to overall more liquidatable positions.

## Code Snippet

execute checking isLiquidatable without triggering interests:

https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L607

actions only poke one token (here for borrow): 

https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L709-L715

bank.totalDebt is used to calculate a position's debt while looping over every tokens: 

https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L451-L475

The position's debt is used to calculate the risk:

https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L477-L495

The risk is used to calculate whether a debt is liquidatable:

https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L497-L505

## Tool used

Manual Review

## Recommendation

Review how token interests are triggered. Probably need to accrue interests on every debt token of a position at the beginning of execute.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry |
| Report Date | N/A |
| Finders | Jeiwan, cducrest-brainbot, rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/140
- **Contest**: https://app.sherlock.xyz/audits/contests/41

### Keywords for Search

`Deposit/Reward tokens, Missing-Logic`

