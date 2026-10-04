---
# Core Classification
protocol: Surge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6705
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/51
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-surge-judging/issues/154

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 21
finders:
  - Dug
  - Hle
  - 0xnuel
  - kiki\_dev
  - ahmedovv
---

## Vulnerability Title

M-3: # [H-02] Approve and transferFrom functions of Pool tokens are subject to front-run attack.

### Overview


This bug report is about the `Approve` and `transferFrom` functions of Pool tokens being subject to front-run attack. The `approve` method overwrites the current allowance regardless of whether the spender already used it or not. This allows the spender to front-run and spend the amount before the new allowance is set. If the malicious spender's transaction is executed before the original transaction, they can gain access to more tokens than they should have been allowed, resulting in users losing their pool tokens. The bug was found by a team of 18 people, and manual review was used as a tool. The recommendation is to use `increaseAllowance` and `decreaseAllowance` instead of `approve` as OpenZeppelin ERC20 implementation.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-surge-judging/issues/154 

## Found by 
Handle, weeeh\_, kiki\_dev, ast3ros, Delvir0, Tricko, Tomo, menox, MalfurionWhitehat, Respx, Kaiziron, Dug, dipp, ABA, Cryptor, 0xnuel, wzrdk3lly, 0xhacksmithh, RaymondFam, bytes032, ahmedovv

## Summary

`Approve` and `transferFrom` functions of Pool tokens are subject to front-run attack because the `approve` method overwrites the current allowance regardless of whether the spender already used it or not. In case the spender spent the amonut, the `approve` function will approve a new amount.

## Vulnerability Detail

The `approve` method overwrites the current allowance regardless of whether the spender already used it or not. It allows the spender to front-run and spend the amount before the new allowance is set.

Scenario:

- Alice allows Bob to transfer N of Alice's tokens (N>0)  by calling the `pool.approve` method, passing the Bob's address and N as the method arguments
- After some time, Alice decides to change from N to M (M>0) the number of Alice's tokens Bob is allowed to transfer, so she calls the `pool.approve` method again, this time passing the Bob's address and M as the method arguments
- Bob notices the Alice's second transaction before it was mined and quickly sends another transaction that calls the `pool.transferFrom` method to transfer N Alice's tokens somewhere
- If the Bob's transaction will be executed before the Alice's transaction, then Bob will successfully transfer N Alice's tokens and will gain an ability to transfer another M tokens
Before Alice noticed that something went wrong, Bob calls the `pool.transferFrom` method again, this time to transfer M Alice's tokens.
- So, an Alice's attempt to change the Bob's allowance from N to M (N>0 and M>0) made it possible for Bob to transfer N+M of Alice's tokens, while Alice never wanted to allow so many of her tokens to be transferred by Bob.

## Impact

It can result in losing pool tokens of users when he approve pool tokens to any malicious account.

## Code Snippet

https://github.com/sherlock-audit/2023-02-surge/blob/main/surge-protocol-v1/src/Pool.sol#L284
https://github.com/sherlock-audit/2023-02-surge/blob/main/surge-protocol-v1/src/Pool.sol#L299

## Tool used

Manual Review

## Recommendation

Use `increaseAllowance` and `decreaseAllowance` instead of approve as OpenZeppelin ERC20 implementation. Please see details here:

https://forum.openzeppelin.com/t/explain-the-practical-use-of-increaseallowance-and-decreaseallowance-functions-on-erc20/15103/4

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Surge |
| Report Date | N/A |
| Finders | Dug, Hle, 0xnuel, kiki\_dev, ahmedovv, bytes032, menox, Delvir0, wzrdk3lly, Cryptor, Kaiziron, Tomo, weeeh\_, ast3ros, 0xhacksmithh, RaymondFam, Respx, Tricko, ABA, dipp, MalfurionWhitehat |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-surge-judging/issues/154
- **Contest**: https://app.sherlock.xyz/audits/contests/51

### Keywords for Search

`vulnerability`

