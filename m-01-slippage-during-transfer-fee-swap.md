---
# Core Classification
protocol: Berabot
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45355
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Berabot-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-01] Slippage During Transfer Fee Swap

### Overview


This bug report discusses a potential issue with the token `Berabot` where it can be vulnerable to sandwich attacks. This means that an attacker can manipulate the token's price and cause the `feeRecipient` to receive less `WBERA` tokens than expected. This can happen in two scenarios: when a fee-whitelisted address increases the balance of the pool, or when the `Berabot` balance is larger than a certain percentage. The impact of this bug is that an attacker can extract the fee value from the `feeRecipient`. The recommendation to fix this issue is to separate the swapping of tokens from the `_transfer()` function and implement a minimum amount out. The team has acknowledged this issue.

### Original Finding Content

## Severity

Medium Risk

## Description

If `Berabot` contains at least 0.02% of the `totalSupply` then a swap can be made during `_transfer()`. Such swaps can be vulnerable to sandwich attacks which can cause the `feeRecipient` to receive way less `WBERA` than the normal market price for the swapped tokens.

This is possible in 2 scenarios:

- Every fee-whitelisted address can perform the sandwich attack since they will not trigger an internal swap themselves when they increase the balance of the pool.
- If the `Berabot` balance is larger than 0.04%+ or 0.4%+ then again the front-running swap will be executed as normal but the second swap will cause the `feeRecipient` to get far fewer native tokens than expected.

## Impact

Token `feeRecipient` fee value can be extracted by an attacker.

## Recommendation

It is a design decision. One way to fix this is by separating the swapping of the tokens from the `_transfer()` function and implementing specifying minimum amount out.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Berabot |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Berabot-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

