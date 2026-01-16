---
# Core Classification
protocol: Biconomy
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1646
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest
source_link: https://code4rena.com/reports/2022-03-biconomy
github_link: https://github.com/code-423n4/2022-03-biconomy-findings/issues/180

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
  - front-running

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
  - Cantor_Dust
---

## Vulnerability Title

[M-18]  Possible frontrun on deposits on LiquidityPool

### Overview


This bug report is about a vulnerability in a LiquidityPool smart contract. The vulnerability allows malicious users to double dip on rewards by front-running deposits. This is achieved by manipulating the liquidity pool state from either a deficient or excessive state.

The vulnerability is enabled by the lack of time-weighted checks to calculate the available vs. supplied liquidity. As a result, it is trivial for malicious users to front-run deposits and control the liquidity of the liquidity pool.

The recommended mitigation steps include allowing each deposit to manipulate the liquidity pool state from either a deficient or excessive state, using an alternative approach to calculating rewards such as a dutch auction style deposit system, and recording liquidity states at specific block timestamps and checking against the timestamp for the current block state.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-03-biconomy/blob/main/contracts/hyphen/LiquidityPool.sol#L255
https://github.com/code-423n4/2022-03-biconomy/blob/main/contracts/hyphen/LiquidityPool.sol#L175-L188


## Vulnerability details

## Impact
Rewards are given to a user for depositing either ERC20 tokens or their native token into the LiquidityPool. This reward is used to incentivize users to deposit funds into the liquidity pool when the pool is not in an equilibrium state.

For regular users, this liquidity pool state fluctuates based on the frequency and amount of deposits made to the liquidity pool. If a malicious user can control the state of the liquidity pool before a victim deposits tokens into the liquidity pool, they can gain double rewards.

To gain these double rewards, a malicious user can watch the mempool for transactions that will receive a reward when the deposit occurs. When a malicious user sees that victim deposit, the malicious user can attach a higher fee to their transaction and initiate a deposit. This will allow the malicious user's transaction to front-run before the victim's transaction.

Once the malicious user's deposit is complete, the liquidity pool state will be in a near equilibrium state. Then, the victim's deposit will occur which causes the liquidity pool state to no longer be in equilibrium.

Finally, the malicious user will make a final deposit gaining yet another reward for bringing the liquidity pool state back to equilibrium.

To sum up, a malicious user can create a sandwich attack where they deposit their own tokens before and after a victim's transaction. This will allow the malicious user to double dip and gain rewards twice due to victim's deposit.

## Proof of Concept
Let's look at the depositNative function which is the simpler of the two deposit functions.

The key component in the depositNative function is the getRewardAmount which can be found here (https://github.com/code-423n4/2022-03-biconomy/blob/main/contracts/hyphen/LiquidityPool.sol#L255) . The getRewardAmount calculates how much available vs supplied liquidity exists in the liquidity pool. There are no (https://github.com/code-423n4/2022-03-biconomy/blob/main/contracts/hyphen/LiquidityPool.sol#L175-L188) time-weighted checks to calculate the available vs. supplied liquidity. With a lack of checks for time-weight and that there are no frontrun checks against deposits, it's trivial to front-run deposits and control the liquidity of the liquidity such that the reward amount can be double-dipped.

## Tools Used
Text editor

## Recommended Mitigation Steps

   1. By allowing each deposit to manipulate the liquidity pool state from either a deficient or excessive state, malicious users can double dip on rewards.
  2.  Alternative approaches to calculating rewards is possible, for example a dutch auction style deposit system where rewards are distributed evenly could reduce an impact of a frontrun attack.
 3.   A simpler approach is to record liquidity states at specific block timestamps and check against the timestamp for the current block state.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | WatchPug, Cantor_Dust |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-biconomy
- **GitHub**: https://github.com/code-423n4/2022-03-biconomy-findings/issues/180
- **Contest**: https://code4rena.com/contests/2022-03-biconomy-hyphen-20-contest

### Keywords for Search

`Front-Running`

