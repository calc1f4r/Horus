---
# Core Classification
protocol: Goat Trading
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31189
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/178
source_link: none
github_link: https://github.com/sherlock-audit/2024-03-goat-trading-judging/issues/94

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - AhmedAdam
---

## Vulnerability Title

M-6: Initial Liquidity provider can bypass the withdrawal limit

### Overview


The bug report describes a vulnerability in a protocol called Goat Trading. The issue was found by a user named AhmedAdam and it allows the initial liquidity provider to bypass the maximum withdrawal limit and withdraw all the liquidity they have, which can result in a rug pull. The protocol is supposed to restrict the initial liquidity provider to only withdraw 25% of their liquidity each week, but this check is not enforced if the number of withdrawals left is 1. This means that the initial liquidity provider can withdraw all their remaining tokens in one go, causing harm to the users of the protocol. The report includes a proof of concept and a code snippet showing where the vulnerability exists. The tool used to find this issue was a manual review. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-03-goat-trading-judging/issues/94 

## Found by 
AhmedAdam
## Summary

the initial liquidity provider can bypass maximum withdrawal limit and withdraw all the liquidity that he has leading to a rug pull.

## Vulnerability Detail

According to the protocol documentation, mandatory liquidity locks are implemented, restricting the initial liquidity provider to withdraw only 25% of their liquidity each week. The check for this restriction is enforced within the `_beforeTokenTransfer` function as follows: 
```solidity=910
if (amount > lpInfo.fractionalBalance) {
                    revert GoatErrors.BurnLimitExceeded();
                }
```
but this check isn't done if the number of withdrawals left for the lp is 1.
so the initial liquidity provider can withdraw the whole amount of lp tokens that he has, bypassing the 25% limit.

## Proof of Concept:

- Assume the initial liquidity provider holds 100 LP tokens of the pair tokenA/WETH, and the pool is in the AMM phase.
- Over the first three weeks, they burn 1 LP token each week.
- By the fourth week, they have 97 LP tokens remaining, and they withdraw all of them.
- This action effectively results in a rug pull, harming the users of the protocol.

## Impact

a key invariant of the system gets breached by having the inital liquidity provider able to bypass the withdraw limit

## Code Snippet

https://github.com/sherlock-audit/2024-03-goat-trading/blob/beb09519ad0c0ec0fdf5b96060fe5e4aafd71cff/goat-trading/contracts/exchange/GoatV1Pair.sol#L886-L909

## Tool used

Manual Review

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Goat Trading |
| Report Date | N/A |
| Finders | AhmedAdam |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-03-goat-trading-judging/issues/94
- **Contest**: https://app.sherlock.xyz/audits/contests/178

### Keywords for Search

`vulnerability`

