---
# Core Classification
protocol: Union Finance Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6393
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/44
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-union-judging/issues/4

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

protocol_categories:
  - dexes
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - weeeh\_
---

## Vulnerability Title

M-6: Index mismatch on vouchers and vouchees might lead to invalid borrower-voucher-staker association

### Overview


This bug report is about a potential issue in the smart contract "UserManager.sol" that can lead to an invalid borrower-voucher-staker association. If the borrower has only one vouche, and the staker has given more than one vouche to the borrower, the wrong value of `vouchees[staker][0].voucherIndex` might be overwritten. This could lead to a mismatch between the borrowers and stakers, potentially impacting the integrity of the contract. The tool used to identify the bug was manual review and vim. The recommendation is to check the `vouchers[borrower]` length before writing to the `vouchees` map.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-union-judging/issues/4 

## Found by 
weeeh\_

## Summary
In certain situation, we can have a wrong borrower-voucher-staker association on the smart contract `UserManager.sol`

## Vulnerability Detail
When `vouchers[borrower]` does contain only one element, which means borrower does only have one vouche, and the staker gave more than one vouche to borrowers, and so `vouchees[staker].length > 1` and `vouchees[staker][0].borrower != borrower`. Then as shown on loc https://github.com/sherlock-audit/2023-02-union/blob/main/union-v2-contracts/contracts/user/UserManager.sol#L604 the `vouchees[staker][0].voucherIndex` will be overwritten to 0, which might be the wrong value, because we are modifying the struct Vouchee associated to another borrower.

## Impact
The issue might impact the integrity of the contract by mismatching borrowers and stakers

## Code Snippet
https://github.com/sherlock-audit/2023-02-union/blob/main/union-v2-contracts/contracts/user/UserManager.sol#L583-L607

## Tool used
vim
Manual Review

## Recommendation
We suggest to check the `vouchers[borrower]` length before writing to `vouchees` map.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Union Finance Update |
| Report Date | N/A |
| Finders | weeeh\_ |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-union-judging/issues/4
- **Contest**: https://app.sherlock.xyz/audits/contests/44

### Keywords for Search

`vulnerability`

