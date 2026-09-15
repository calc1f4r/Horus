---
# Core Classification
protocol: Ajna
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6300
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/32
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/156

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - access_control

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Jeiwan
---

## Vulnerability Title

M-3: Anyone can transfer approved LP tokens

### Overview


This bug report is about the Pool.transferLPs function in the Pool.sol file of the 2023-01-ajna project on Github. The function allows for LP tokens to be transferred from one address to another, but it requires approval first. The problem is that anyone can call the function, not just the approved address, which can result in the lender's LP tokens being transferred at an inappropriate time, impacting the position management strategy of the lender. The recommendation is to consider allowing the calling of the function to only the owner or newOwner_. The bug report was found by Jeiwan and the tool used was manual review.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/156 

## Found by 
Jeiwan

## Summary
Anyone can call the `Pool.transferLPs` function and transfer previously approved LP tokens to the approved address.
## Vulnerability Detail
The [Pool.transferLPs](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/base/Pool.sol#L238) function allows to transfer LP tokens from one address to another. Even though it requires [approving](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/base/Pool.sol#L169) a transfer, actual transferring is left at the discretion of the approved address: approving allows the approved address to transfer LP tokens when appropriate. However, since the `Pool.transferLPs` function can be called by any address, the owner of the tokens may be impacted.
## Impact
Lender's LP tokens may be transferred to an approve address at an inappropriate time, impacting the position management strategy of the lender.
## Code Snippet
[Pool.sol#L238](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/base/Pool.sol#L238)
## Tool used
Manual Review
## Recommendation
Consider allowing calling the `Pool.transferLPs` function only to the `owner` or `newOwner_`.

## Discussion

**grandizzy**

removing will fix label, will address after Sherlock contest

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Ajna |
| Report Date | N/A |
| Finders | Jeiwan |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/156
- **Contest**: https://app.sherlock.xyz/audits/contests/32

### Keywords for Search

`Access Control`

