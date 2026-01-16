---
# Core Classification
protocol: Concur Finance
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1400
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-concur-finance-contest
source_link: https://code4rena.com/reports/2022-02-concur
github_link: https://github.com/code-423n4/2022-02-concur-findings/issues/219

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
  - wrong_math
  - update_state_after_admin_action
  - admin

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - cccz
  - leastwood
  - cmichel
  - throttle
---

## Vulnerability Title

[H-01] Wrong reward token calculation in MasterChef contract

### Overview


This bug report is about an issue with the MasterChef contract, which is used to add new token pools for staking. When a new pool is added, the other existing pools should be updated, but currently they are not. This means that the rewards for users in the old pools are not computed correctly, and will always be smaller than they should be. 

Two scenarios are given to illustrate the issue. In the first, Alice and Bob both stake 10 tokens in the first pool, and when Bob withdraws his tokens he only receives half the reward he should have. In the second, Alice, Bob and Charlie all stake 10 tokens in the first pool, and when they try to withdraw their tokens they only receive 20% of the rewards they should have.

The recommended mitigation steps are to update all existing pools before adding a new pool, using the massUpdate() function that is already present in the code.

### Original Finding Content

_Submitted by throttle, also found by cccz, cmichel, and leastwood_

[MasterChef.sol#L86](https://github.com/code-423n4/2022-02-concur/blob/main/contracts/MasterChef.sol#L86)<br>

When adding new token pool for staking in MasterChef contract

```javascript
function add(address _token, uint _allocationPoints, uint16 _depositFee, uint _startBlock)
```

All other, already added, pools should be updated but currently they are not.<br>
Instead, only totalPoints is updated. Therefore, old (and not updated) pools will lose it's share during the next update.<br>
Therefore, user rewards are not computed correctly (will be always smaller).

### Proof of Concept

Scenario 1:

1.  Owner adds new pool (first pool) for staking with points = 100 (totalPoints=100)<br>
    and 1 block later Alice stakes 10 tokens in the first pool.
2.  1 week passes
3.  Alice withdraws her 10 tokens and claims X amount of reward tokens.<br>
    and 1 block later Bob stakes 10 tokens in the first pool.
4.  1 week passes
5.  Owner adds new pool (second pool) for staking with points = 100 (totalPoints=200)<br>
    and 1 block later Bob withdraws his 10 tokens and claims X/2 amount of reward tokens.<br>
    But he should get X amount

Scenario 2:

1.  Owner adds new pool (first pool) for staking with points = 100 (totalPoints=100).
2.  1 block later Alice, Bob and Charlie stake 10 tokens there (at the same time).
3.  1 week passes
4.  Owner adds new pool (second pool) for staking with points = 400 (totalPoints=500)
5.  Right after that, when Alice, Bob or Charlie wants to withdraw tokens and claim rewards they will only be able to claim 20% of what they should be eligible for, because their pool is updated with 20% (100/500) rewards instead of 100% (100/100) rewards for the past week.

### Recommended Mitigation Steps

Update all existing pools before adding new pool. Use the massUdpate() function which is already present ... but unused.

**[ryuheimat (Concur) confirmed](https://github.com/code-423n4/2022-02-concur-findings/issues/219)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-02-concur-findings/issues/219#issuecomment-1092858699):**
 > The warden has identified a fallacy in how `add`s logic work.
> 
> Ultimately rewards in this contract have to be linearly vested over time, adding a new pool would change the rate at which vesting in all pools will go.
> 
> For that reason, it is necessary to accrue the rewards that each pool generated up to that point, before changing the slope at which rewards will be distributed.
> 
> In this case add should massUpdateFirst.
> 
> Because this vulnerability ultimately breaks the accounting of the protocol, I believe High Severity to be appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Concur Finance |
| Report Date | N/A |
| Finders | cccz, leastwood, cmichel, throttle |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-concur
- **GitHub**: https://github.com/code-423n4/2022-02-concur-findings/issues/219
- **Contest**: https://code4rena.com/contests/2022-02-concur-finance-contest

### Keywords for Search

`Wrong Math, Update State After Admin Action, Admin`

