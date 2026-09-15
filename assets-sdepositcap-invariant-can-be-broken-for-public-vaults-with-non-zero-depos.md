---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7317
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

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
  - validation
  - bypass_limit

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

assets < s.depositCap invariant can be broken for public vaults with non-zero deposit caps

### Overview


This bug report is about a check in the mint/deposit functions of the PublicVault.sol file which does not take into consideration the new shares/amount supplied to the endpoint. This means that the new shares/amount provided can be a really big number compared to s.depositCap, but the call will still go through. To fix this issue, it is recommended that the inequality assets < s.depositCap should be calculated beforehand and then the check should be performed.

### Original Finding Content

## Severity: Medium Risk

## Context
- PublicVault.sol#L207-L208
- PublicVault.sol#L231-L232

## Description
The following check in `mint` / `deposit` does not take into consideration the new shares / amount supplied to the endpoint, since the `yIntercept` in `totalAssets()` is only updated after calling `super.mint(shares, receiver)` or `super.deposit(amount, receiver)` with the `afterDeposit` hook.

```solidity
uint256 assets = totalAssets();
if (s.depositCap != 0 && assets >= s.depositCap) {
    revert InvalidState(InvalidStates.DEPOSIT_CAP_EXCEEDED);
}
```

Thus the new shares or amount provided can be a really big number compared to `s.depositCap`, but the call will still go through.

## Recommendation
To have the inequality `assets < s.depositCap` to be always correct, we would need to calculate the to-be-updated value of `assets` beforehand and then perform the check.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Bypass limit`

