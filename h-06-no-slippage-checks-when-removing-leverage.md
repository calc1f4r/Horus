---
# Core Classification
protocol: Peapods_2024-11-16
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45993
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-06] No slippage checks when removing leverage

### Overview


The report discusses a bug in the `LeverageManager` that can potentially cause a high impact and has a medium likelihood of occurring. The issue occurs when removing leverage, causing the pod token to be swapped for the borrow token. This swap has no slippage protection and can be exploited by a malicious attacker to use up all the pod tokens. As a result, the user may receive fewer tokens than expected. To fix this, it is recommended to allow users to specify the minimum amount of pod tokens they want to receive in the swap. This will ensure that the transaction will be reverted if the swap occurs at an unfavorable price.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

When removing leverage in the `LeverageManager`, it swaps the pod token for the borrow token:

```solidity
_podAmtRemaining = _swapPodForBorrowToken(_pod, _borrowToken, _podAmtReceived, _borrowAmtNeededToSwap);
```

This is an exact output swap, and `amountInMax` is set as the number of pod tokens available. This means there is 0 slippage protection in the swap. A malicious attacker can sandwich this transaction to cause maximal usage of the pod tokens when swapping to borrow tokens.

In the end, `_podAmtRemaining` will be very tiny, or `0` due to this, so the user is returned fewer tokens than they should be.

## Recommendations

It is recommended to allow the user to pass in `podAmtOutMin`, which is checked within `LeverageManager.callback()`, after `_removeLeverage()` occurs. This ensures that if the swap occurs at an unfavorable price, the entire transaction will revert.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Peapods_2024-11-16 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Peapods-security-review_2024-11-16.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

