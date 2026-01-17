---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3690
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/83

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x4141
---

## Vulnerability Title

M-15: LiquidationAccountant.claim may revert for some tokens

### Overview


This bug report is about the issue M-15 found by 0x4141. It states that the `LiquidationAccountant.claim` function may initiate a transfer with the amount 0, which reverts for some tokens. This is due to some tokens (e.g., LEND) reverting when a transfer with amount 0 is initiated. If this happens, the funds are not claimable, leading to a loss of funds. The code snippet can be found at https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LiquidationAccountant.sol#L88 and the bug was found through manual review. The recommendation is to not initiate a transfer when the amount is zero.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/83 

## Found by 
0x4141

## Summary
`LiquidationAccountant.claim` may initiate a transfer with the amount 0, which reverts for some tokens.

## Vulnerability Detail
Some tokens (e.g., LEND -> see https://github.com/d-xo/weird-erc20#revert-on-zero-value-transfers) revert when a transfer with amount 0 is initiated. This can happen within `claim` when the `withdrawRatio` is 100%.

## Impact
In such a scenario, the funds are not claimable, leading to a loss of funds.

## Code Snippet
https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LiquidationAccountant.sol#L88

## Tool used

Manual Review

## Recommendation
Do not initiate a transfer when the amount is zero.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | 0x4141 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/83
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

