---
# Core Classification
protocol: Rivus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58230
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Rivus-security-review.md
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

[C-01] Unlimited token transfer

### Overview


The report highlights a bug in the function `getSharesByMintedRsTAO()` which is used to calculate the amount of shares corresponding to a certain amount of RsTAO. The issue is that when the total minted amount is 0, the function returns 0 instead of the actual amount. This can lead to various problems such as transferring unlimited tokens to third party contracts and extracting value from contracts with small deposits. The report recommends fixing this bug by returning the actual amount when the total minted tokens are 0 and applying the same fix to COMAI contracts.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

Function `getSharesByMintedRsTAO()` has been used to calculate amount of shares that corresponds to the RsTAO amount and it's been used in multiple functions like `_transfer()` and `_mintRsTAO()`. The issue is that the function `getSharesByMintedRsTAO()` returns 0 when the total minted amount is 0 while it should have returned the amount itself. This has multiple impacts like transferring unlimited tokens while the total mint is 0, this is the POC:

1. Suppose RivusTAO is recently deployed or for other reasons (upgrade or ...) the total amount is zero.
2. Now attacker can transfer unlimited tokens to 3rd party contracts like DEX or lending platforms and credit tokens for himself.
3. This is possible because when RivusTAO wants to transfer tokens in the `_transfer()` it would call `getSharesByMintedRsTAO()` to calculate the share amount and the share amount would be 0, so the code would have no problem transferring 0 shares.
4. In the end the 3rd party contract would charge the user account while in reality, it didn't receive any tokens. The `transferFrom()` call would return true and won't revert.

There are other impacts. Function `_mintRsTAO()` uses `getSharesByMintedRsTAO()` too and when the return amount is 0 then the code uses `amount` to mint shares. The issue is that the return amount of `getSharesByMintedRsTAO()` can be 0 because of the rounding error (small values of `amount`) and the code should have minted 0 shares while it would mint >0 shares. This can be used to extract value from contracts with small deposit amounts while the share price is high.

This issue exists for rsCOMAI and RivusCOMAI contracts too.

## Recommendations

When the total minted tokens are 0 then the code should return `amount` in `getSharesByMintedRsTAO()`. The function `getMintedRsTAOByShares()` should be fixed too. Those fixes should be applied to COMAI contracts too.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Rivus |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Rivus-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

