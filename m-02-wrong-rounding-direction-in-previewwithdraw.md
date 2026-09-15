---
# Core Classification
protocol: Astrolab
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58106
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Wrong rounding direction in previewWithdraw()

### Overview


The bug report discusses an issue with the `previewWithdraw` function in the EIP4626 Vault implementation. According to the EIP4626, the function should round up when performing division, but the current code rounds down and favors the caller instead of the contract. This can cause a revert when rounding errors occur, as the calculated shares will be smaller and fail the check for price in the `_withdraw()` function. The recommendation is to change the `previewWithdraw` function to round up when calculating shares. This bug has a low impact and high likelihood of occurring since the division happens in each transaction.

### Original Finding Content

## Severity

**Impact:** Low, because revert in mint() and violates EIP4626

**Likelihood:** High, because division happens in each tx

## Description

According to the [EIP4626 ](https://eips.ethereum.org/EIPS/eip-4626) `previewWithdraw` should round up when performing division:

> Finally, EIP-4626 Vault implementers should be aware of the need for specific, opposing rounding directions across the different mutable and view methods, as it is considered most secure to favor the Vault itself during calculations over its users:
>
> If (1) it’s calculating how many shares to issue to a user for a certain amount of the underlying tokens they provide or (2) it’s determining the amount of the underlying tokens to transfer to them for returning a certain amount of shares, it should round down.
>
> If (1) it’s calculating the amount of shares a user has to supply to receive a given amount of the underlying tokens or (2) it’s calculating the amount of underlying tokens a user has to provide to receive a certain amount of shares, it should round up.

But in current implementation code rounds down and favors the caller instead of the contract.

Function `withdraw()` uses `previewWithdraw()` to calculate shares and calls `_withdraw()`, as there is a check for price in `_withdraw()` to make sure user received price isn't better than current price, so that check will fail and cause revert when rounding errors happens. (calculated `_shares` will be smaller and the right side of the condition will be smaller)

```solidity
        // amount/shares cannot be higher than the share price (dictated by the inline convertToAssets below)
        if (_amount >= _shares.mulDiv(price * weiPerAsset, weiPerShare ** 2))
            revert AmountTooHigh(_amount);
```

## Recommendation

Change `previewWithdraw` so that it rounds up when calculating shares.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Astrolab |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

