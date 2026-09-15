---
# Core Classification
protocol: Olympusdao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6681
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/50
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/128

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
  - services
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - 0x52
  - Bahurum
  - 0xlmanini
  - tives
  - minhtrng
---

## Vulnerability Title

M-5: Internal reward tokens can and likely will over commit rewards

### Overview


This bug report is about an issue found in the SingleSidedLiquidityVault.sol contract. The issue is that internal reward tokens accrue indefinitely, with no way to input a timestamp that they stop accruing, and no check that the contract has enough tokens to fund the rewards that it has committed to. As a result, the contract may over commit reward tokens and after the token balance of the contract has been exhausted, all further claims will fail. This could lead to users being unable to claim their rewards. The bug was found by tives, Bahurum, 0xlmanini, minhtrng, and 0x52, who used ChatGPT to identify the issue. The recommended solution is to add an end timestamp to the accrual of internal tokens, and to transfer the amount of tokens needed to fund the internal tokens from the caller when the token is added.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/128 

## Found by 
tives, Bahurum, 0xlmanini, minhtrng, 0x52

## Summary

Internal reward tokens accrue indefinitely with no way to change the amount that they accrue each block (besides removing them which has other issues) or input a timestamp that they stop accruing. Additionally there is no check that the contract has enough tokens to fund the rewards that it has committed to. As a result of this the contract may over commit reward tokens and after the token balance of the contract has been exhausted, all further claims will fail.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L674-L688

Internal reward tokens are added with a fixed _rewardPerSecond that will accrue indefinitely because it does not have an ending timestamp. As a result the contract won't stop accruing internal rewards even if it has already designated it's entire token balance. After it has over committed it will now be impossible for all users to claim their balance. Additionally claiming rewards is an all or nothing function meaning that once a single reward token starts reverting, it becomes impossible to claim any rewards at all.

## Impact

Internal reward tokens can over commit and break claiming of all reward tokens

## Code Snippet

https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/abstracts/SingleSidedLiquidityVault.sol#L674-L688

## Tool used

ChatGPT

## Recommendation

I recommend adding an end timestamp to the accrual of internal tokens. Additionally, the amount of tokens needed to fund the internal tokens should be transferred from the caller (or otherwise tracked) when the token is added.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Olympusdao |
| Report Date | N/A |
| Finders | 0x52, Bahurum, 0xlmanini, tives, minhtrng |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-olympus-judging/issues/128
- **Contest**: https://app.sherlock.xyz/audits/contests/50

### Keywords for Search

`vulnerability`

