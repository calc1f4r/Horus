---
# Core Classification
protocol: Key Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26760
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2023-05-01-Key Finance.md
github_link: none

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
  - Guardian Audits
---

## Vulnerability Title

LPS-2 | onERC721Received Reentrancy

### Overview


This bug report is about the `unstakeAndWithdrawLpToken` function in the `LPStaker` contract. This function can cause re-entry into the `onERC721Received` function when the `withdrawToken` call is made, which can create an unexpected state where the token is still in the `tokensStaked` list of the owner, but not in the `idToOwner` or `stakedIndex`. This unexpected state can have unintended consequences on frontend systems and third party systems built on top of the `LPStaker` contract.

The recommended resolution is to either move the `withdrawToken` call to the end of the for loop, or add a reentrancy check to the `onERC721Received` function. The team ultimately decided to adopt the Check-Effects-Interactions approach.

### Original Finding Content

**Description**

During the `unstakeAndWithdrawLpToken` function, the `msg.sender` may re-enter into the `onERC721Received` function upon the `withdrawToken` call by transferring the withdrawn Uniswap V3 LP NFT back to the `LPStaker`.
This reentrancy can yield an unexpected state where the token still exists in the `tokensStaked` list for the owner, but not in the `idToOwner` or `stakedIndex`. Such an unexpected state may have unintended consequences and effect frontend systems reading from the contract or third party systems built on top of the `LPStaker`.

**Recommendation**

Move the `withdrawToken` call to the end of the for loop to follow Check-Effects-Interactions. Alternatively, add a reentrancy check to the `onERC721Received` function.

**Resolution**

Key Team: Check-Effects-Interactions was adopted.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | Key Finance |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2023-05-01-Key Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

