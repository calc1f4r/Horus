---
# Core Classification
protocol: Opyn Crab Netting
chain: everychain
category: dos
vulnerability_type: dos

# Attack Vector Details
attack_type: dos
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5648
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/26
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/148

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 4

# Context Tags
tags:
  - dos

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - 0x52
  - chainNue
  - yixxas
  - rotcivegaf
  - Jeiwan
---

## Vulnerability Title

H-3: Adverary can DOS contract by making a large number of deposits/withdraws then removing them all

### Overview


This bug report is about an issue found in the code of the Opyn Finance's Crab Netting contract. The issue is that an adversary can DOS the contract by making a large number of deposits/withdraws and then removing them all, leaving a large number of blank entries in the withdraw/deposit. This would require the contract to read the blank entries from memory and skip them when processing the withdraws/deposits, which uses up gas for each blank entry. If the adversary makes the list long enough then it will be impossible to fill without going over the block gas limit. This could permanently DOS the contract. 

Two potential solutions have been proposed. The first would be to limit the number of deposits/withdraws that can be processed in a single netting. The second would be to allow the owner to manually skip withdraws/deposits by calling an function that increments depositsIndex and withdrawsIndex. A fix was accepted and implemented, allowing the owner to set the withdrawsIndex and depositIndex and skip the queue index forward if there is some issue with the queue elements.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/148 

## Found by 
indijanc, rotcivegaf, hyh, chainNue, rvierdiiev, Met, 0x52, KingNFT, Jeiwan, adriro, yixxas

## Summary

When a user dequeues a withdraw or deposit it leaves a blank entry in the withdraw/deposit. This entry must be read from memory and skipped when processing the withdraws/deposits which uses gas for each blank entry. An adversary could exploit this to DOS the contract. By making a large number of these blank deposits they could make it impossible to process any auction. 

## Vulnerability Detail

        while (_quantity > 0) {
            Receipt memory deposit = deposits[i];
            if (deposit.amount == 0) {
                i++;
                continue;
            }
            if (deposit.amount <= _quantity) {
                // deposit amount is lesser than quantity use it fully
                _quantity = _quantity - deposit.amount;
                usdBalance[deposit.sender] -= deposit.amount;
                amountToSend = (deposit.amount * 1e18) / _price;
                IERC20(crab).transfer(deposit.sender, amountToSend);
                emit USDCDeposited(deposit.sender, deposit.amount, amountToSend, i, 0);
                delete deposits[i];
                i++;
            } else {
                // deposit amount is greater than quantity; use it partially
                deposits[i].amount = deposit.amount - _quantity;
                usdBalance[deposit.sender] -= _quantity;
                amountToSend = (_quantity * 1e18) / _price;
                IERC20(crab).transfer(deposit.sender, amountToSend);
                emit USDCDeposited(deposit.sender, _quantity, amountToSend, i, 0);
                _quantity = 0;
            }
        }

The code above processes deposits in the order they are submitted. An adversary can exploit this by withdrawing/depositing a large number of times then dequeuing them to create a larger number of blank deposits. Since these are all zero, it creates a fill or kill scenario. Either all of them are skipped or none. If the adversary makes the list long enough then it will be impossible to fill without going over block gas limit.

## Impact

Contract can be permanently DOS'd

## Code Snippet

https://github.com/sherlock-audit/2022-11-opyn/blob/main/crab-netting/src/CrabNetting.sol#L362-L386

## Tool used

Manual Review

## Recommendation

Two potential solutions. The first would be to limit the number of deposits/withdraws that can be processed in a single netting. The second would be to allow the owner to manually skip withdraws/deposits by calling an function that increments depositsIndex and withdrawsIndex.

## Discussion

**sanandnarayan**

fix: https://github.com/opynfinance/squeeth-monorepo/pull/805

**thec00n**

Allows the owner to set the `withdrawsIndex` and `depositIndex` and so to skip the queue index forward if there is some issue with the queue elements. At least this should allow the auction functions to continue to work.   

**jacksanford1**

FIx accepted

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Opyn Crab Netting |
| Report Date | N/A |
| Finders | 0x52, chainNue, yixxas, rotcivegaf, Jeiwan, hyh, KingNFT, indijanc, adriro, rvierdiiev, Met |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-opyn-judging/issues/148
- **Contest**: https://app.sherlock.xyz/audits/contests/26

### Keywords for Search

`DOS`

