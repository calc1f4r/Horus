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
solodit_id: 6388
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/44
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-union-judging/issues/39

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
  - dexes
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ast3ros
---

## Vulnerability Title

M-1: # [M-04] voucherIndexes is not updated when member cancel the voucher

### Overview


This bug report concerns a vulnerability in the UserManager.sol contract of the Sherlock Audit 2023-02-union-judging project. It was found by ast3ros and involves the voucherIndexes not being updated when a staker or borrower cancel a voucher. This leads to incorrect indexing for the last voucher, which points to another voucher with a different staker. This could be exploited by malicious members. The code snippet provided in the report is from line 593 to 605 of the UToken.sol file. The issue was found manually, and the recommendation is to add an update voucherIndexes in the `_cancelVouchInternal` function.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-union-judging/issues/39 

## Found by 
ast3ros

## Summary

When staker or borrower cancel the voucher, the `voucherIndexes` for the lastVoucher is not updated.

## Vulnerability Details

The voucherIndexes is not updated when a voucher is cancelled.

## Impact

It leads to incorrect index for the last voucher, which points to another voucher with different staker. It could be a point to be exploit by malicious members.

## Code Snippet

https://github.com/sherlock-audit/2023-02-union/blob/main/union-v2-contracts/contracts/user/UserManager.sol#L593-L605

## Tool used

Manual

## Recommendation

Add update voucherIndexes in the `_cancelVouchInternal` function, below line 604 of UToken.sol:

            voucherIndexes[borrower][lastVoucher.staker] = removeVoucherIndex.Idx

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Union Finance Update |
| Report Date | N/A |
| Finders | ast3ros |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-union-judging/issues/39
- **Contest**: https://app.sherlock.xyz/audits/contests/44

### Keywords for Search

`vulnerability`

