---
# Core Classification
protocol: Trader Joe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1344
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-trader-joe-contest
source_link: https://code4rena.com/reports/2022-01-trader-joe
github_link: https://github.com/code-423n4/2022-01-trader-joe-findings/issues/127

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
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - kirk-baird
  - 0v3rf10w  static
---

## Vulnerability Title

[M-11] Re-enterable Code When Making a Deposit to Stake

### Overview


A bug report has been raised on the RocketJoeToken contract which is part of the 2022-01-trader-joe project. The bug would allow the entire rJoe balance to be drained from the contract if an attacker was able to gain control of the execution during the rJoe::tranfer() function. This is a medium risk vulnerability as it requires rJoe to relinquish control during tranfer() which it does not currently do. 

The vulnerable function is deposit() which is located at RocketJoeStaking.sol#L96. This function calculates a variable called pending using two state variables user.amount and user.rewardDebt, and then calls _safeRJoeTransfer() passing in pending as the amount. If an attacker was able to gain control of the execution during the rJoe::tranfer() function they would be able to reenter deposit() and the value calculated for pending would be the same as the previous iteration hence they would again be transferred pending rJoe tokens. The process could be repeated until the entire rJoe balance of the contract has been transferred to the attacker.

Two possible mitigations have been recommended. The first is to use the openzeppelin reentrancy guard over the deposit() function which will prevent multiple deposits being made simultaneously. The second is to follow the checks-effects-interactions pattern. This would involve updating all state variables before making any external calls.

### Original Finding Content

_Submitted by kirk-baird, also found by 0v3rf10w and static_

Note: this attack requires `rJoe` to relinquish control during `tranfer()` which under the current [RocketJoeToken](https://github.com/code-423n4/2022-01-trader-joe/blob/main/contracts/RocketJoeToken.sol) it does not. Thus this vulnerability is raised as medium rather than high. Although it's not exploitable currently, it is a highly risky code pattern that should be avoided.

This vulnerability would allow the entire rJoe balance to be drained from the contract.

#### Proof of Concept

The function [deposit()](https://github.com/code-423n4/2022-01-trader-joe/blob/main/contracts/RocketJoeStaking.sol#L96) would be vulnerable to reentrancy if rJoe relinquished control flow.

The following lines show the reward calculations in variable `pending`. These calculations use two state variables `user.amount` and `user.rewardDebt`. Each of these are updated after `_safeRJoeTransfer()`.

Thus if an attacker was able to get control flow during the `rJoe::tranfer()` function they would be able to reenter `deposit()` and the value calculated for `pending`would be the same as the previous iteration hence they would again be transferred `pending` rJoe tokens. During the rJoe transfer the would again gain control of the execution and call `deposit()` again. The process could be repeated until the entire rJoe balance of the contract has been transferred to the attacker.

```solidity
if (user.amount > 0) {
    uint256 pending = (user.amount * accRJoePerShare) /
        PRECISION -
        user.rewardDebt;
    _safeRJoeTransfer(msg.sender, pending);
}
user.amount = user.amount + _amount;
user.rewardDebt = (user.amount * accRJoePerShare) / PRECISION;
```

#### Recommended Mitigation Steps

There are two possible mitigations. First is to use the [openzeppelin reentrancy guard](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/security/ReentrancyGuard.sol) over the `deposit()` function which will prevent multiple deposits being made simultaneously.

The second mitigation is to follow the [checks-effects-interactions](https://docs.soliditylang.org/en/v0.8.11/security-considerations.html#re-entrancy) pattern. This would involve updating all state variables before making any external calls.

**[cryptofish7 (Trader Joe) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2022-01-trader-joe-findings/issues/127#issuecomment-1026161071):**
 > Disagree with severity
> 
> Fix: https://github.com/traderjoe-xyz/rocket-joe/pull/142

**[LSDan (judge) commented](https://github.com/code-423n4/2022-01-trader-joe-findings/issues/127#issuecomment-1047788682):**
 > I agree with the warden's assessment of risk on this one. Leaving it unaddressed would represent a potential future compromise if it was forgotten about by the team.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Trader Joe |
| Report Date | N/A |
| Finders | kirk-baird, 0v3rf10w  static |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-trader-joe
- **GitHub**: https://github.com/code-423n4/2022-01-trader-joe-findings/issues/127
- **Contest**: https://code4rena.com/contests/2022-01-trader-joe-contest

### Keywords for Search

`vulnerability`

