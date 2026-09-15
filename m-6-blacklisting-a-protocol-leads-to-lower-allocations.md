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
solodit_id: 12236
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
finders_count: 1
finders:
  - Met
---

## Vulnerability Title

M-6: Blacklisting a protocol leads to lower allocations

### Overview


This bug report is about an issue with blacklisting a protocol in the Vault.sol contract. This issue was found by Met and has an impact of forever decreased token allocations to protocols and lower yield. The totalAllocatedTokens variable is only modified by delta allocations, and blacklisting does not touch the variable. The protocol allocation is calculated by the totalAllocatedTokens value, and if it is larger than it should be, it will lead to lower token allocations to protocols and lower yield. The recommendation to fix this issue is to totalAllocatedTokens by the zeroed currentAllocations[_protocolNum]. The discussion on the bug report was a duplicate of two other issues.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-derby-judging/issues/94 

## Found by 
Met

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
| Finders | Met |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-derby-judging/issues/94
- **Contest**: https://app.sherlock.xyz/audits/contests/13

### Keywords for Search

`vulnerability`

