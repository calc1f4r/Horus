---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: min/max_cap_validation

# Attack Vector Details
attack_type: min/max_cap_validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7320
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
  - min/max_cap_validation

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

Liens cannot be bought out once we've reached the maximum number of active liens on one collateral

### Overview


This bug report is about the buyoutLien function in the LienToken.sol file. The buyoutLien function is intended to transfer ownership of a lien from one user to another, but it was not working properly. The function calls the _createLien function, which has a check to ensure that no more than maxLiens can be taken out against one piece of collateral. This check was causing the function to revert when a user tried to buy out a lien when they already had maxLiens. The recommendation was to move this check from the _createLien function to the _appendStack function, which is only called when new liens are created rather than when they are bought out. The bug was fixed in PR 213 and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
LienToken.sol#L373-375

## Description
The `buyoutLien` function is intended to transfer ownership of a lien from one user to another. In practice, it creates a new lien by calling `_createLien` and then calls `_replaceStackAtPositionWithNewLien` to update the stack.

In the `_createLien` function, there is a check to ensure we don't take out more than `maxLiens` against one piece of collateral:

```solidity
if (params.stack.length >= s.maxLiens) {
    revert InvalidState(InvalidStates.MAX_LIENS);
}
```

The result is that, when we already have `maxLiens` and we try to buy one out, this function will revert.

## Recommendation
Move this check from `_createLien` into the `_appendStack` function, which is only called when new liens are created rather than when they are bought out.

## Astaria
Fixed in PR 213.

## Spearbit
Verified.

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

`Min/Max Cap Validation`

