---
# Core Classification
protocol: Derby
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 12334
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/13
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-derby-judging/issues/94

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
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Ch\_301
  - Met
---

## Vulnerability Title

M-39: Blacklisting a protocol leads to lower allocations

### Overview


This bug report was raised by Ch\_301 and Met and was found when manually reviewing the code. The issue is that blacklisting a protocol does not update the totalAllocatedTokens, which is used to calculate the new allocations. This can lead to lower token allocations to protocols and lower yield. The code snippet and tool used is not specified. The recommendation is to modify totalAllocatedTokens by the zeroed currentAllocations[_protocolNum]. The bug report is a duplicate of another issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-derby-judging/issues/94 

## Found by 
Ch\_301, Met

## Summary
Blacklisting a protocol does not update (decrease) the totalAllocatedTokens. It is used to calculate the new allocations and if it is larger than it should be it will lead to lower token allocations to protocols and lower yield.
## Vulnerability Detail
Blacklisting does not touch the variable (it decreases the currentAllocations[_protocolNum] but not the total)
https://github.com/sherlock-audit/2023-01-derby/blob/main/derby-yield-optimiser/contracts/Vault.sol#L477-L483

totalAllocatedTokens is only modified by delta allocations, there is no fix to it.
https://github.com/sherlock-audit/2023-01-derby/blob/main/derby-yield-optimiser/contracts/Vault.sol#L167-L170

The protocol allocation is calculated hereby, decreased by totalAllocatedTokens value.
https://github.com/sherlock-audit/2023-01-derby/blob/main/derby-yield-optimiser/contracts/Vault.sol#L209-L218

## Impact
Forever decreased token allocations to protocols and lower yield.
## Code Snippet

## Tool used

Manual Review

## Recommendation
totalAllocatedTokens by the zeroed currentAllocations[_protocolNum]



## Discussion

**sjoerdsommen**

duplicate with  https://github.com/sherlock-audit/2023-01-derby-judging/issues/95 https://github.com/sherlock-audit/2023-01-derby-judging/issues/94

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Derby |
| Report Date | N/A |
| Finders | Ch\_301, Met |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-derby-judging/issues/94
- **Contest**: https://app.sherlock.xyz/audits/contests/13

### Keywords for Search

`vulnerability`

