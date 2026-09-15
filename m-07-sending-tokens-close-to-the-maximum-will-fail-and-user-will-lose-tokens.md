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
solodit_id: 1635
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/181

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
  - WatchPug
  - pedroais
---

## Vulnerability Title

[M-07] Sending tokens close to the maximum will fail and user will lose tokens

### Overview


A bug was found in the code of a LiquidityPool contract, which could result in users losing their funds. Specifically, when a user calls the deposit function, the reward amount is calculated and an event is emitted with the amount plus the reward as the transfer amount. The function checks if the amount is smaller than the max amount. An executor then listens to this event and calls sendFundsToUser with rewards plus the amount as the amount parameter. This function checks if the amount plus the reward is smaller than the max amount. 

The problem is that the amount transferred may be in the limit but the amount plus the reward could pass the limit and the executor won't be able to send the transaction, resulting in the user losing the funds. To prevent this, both checks should be made with the reward or without the reward, but the checks should be the same. 

For example, if the max transfer is set to 50 for token A, and Bob transfers 49 tokens, this will pass since 49<50. The reward is calculated in 2 tokens. The executor then calls sendFundsToUser with 52. This transaction will revert and the user will lose their tokens. 

The recommended mitigation step is for both checks to be made over the same amount, which is the amount plus the rewards.

### Original Finding Content

_Submitted by pedroais, also found by WatchPug_

[LiquidityPool.sol#L171](https://github.com/code-423n4/2022-03-biconomy/blob/04751283f85c9fc94fb644ff2b489ec339cd9ffc/contracts/hyphen/LiquidityPool.sol#L171)<br>
[LiquidityPool.sol#L273](https://github.com/code-423n4/2022-03-biconomy/blob/04751283f85c9fc94fb644ff2b489ec339cd9ffc/contracts/hyphen/LiquidityPool.sol#L273)<br>

When a user calls the deposit function the reward amount is calculated and an event is emited with amount+reward as the transfer amount. The function checks amount is smaller than the max amount.

An executor then listens to this event and calls sendFundsToUser with rewards + amount as the amount parameter. This function checks amount+reward is smaller than max amount.

This is a problem because the amount transferred may be in the limit but amount + reward could pass the limit and the executor won't be able to send the transaction. The user will lose the funds. Both checks should be made with the reward or without the reward but the checks should be the same for this not to happen.

Step by step :<br>
Max transfer is set to 50 for token A<br>
Bob transfers 49 tokens, this will pass since 49<50. The reward is calculated in 2 tokens.<br>
The executor then calls sendFundsToUser with 52. This transaction will revert and user will lose their tokens.<br>

This value of amount includes rewards but the previous check didn't include rewards: [LiquidityPool.sol#L273](https://github.com/code-423n4/2022-03-biconomy/blob/04751283f85c9fc94fb644ff2b489ec339cd9ffc/contracts/hyphen/LiquidityPool.sol#L273).

### Recommended Mitigation Steps

Both checks should be made over the same amount = amount + rewards

**[ankurdubey521 (Biconomy) disputed and commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/181#issuecomment-1082946519):**
 > We handle this issue by setting a slightly larger limit in the transfer config of each token on the destination chain.

**[pauliax (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-03-biconomy-findings/issues/181#issuecomment-1112625440):**
 > Even though the sponsor is already aware of and mitigates this issue, it could still be fixed algorithmically to prevent accidental loss of funds. I am leaving this as of medium severity.



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
| Finders | WatchPug, pedroais |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/181
- **Contest**: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest

### Keywords for Search

`vulnerability`

