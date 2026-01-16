---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7288
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - don't_update_state

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

setPayee doesn't update y intercept or slope, allowing vault owner to steal all funds

### Overview


This bug report details a high risk issue in LienToken.sol. When setPayee() is called, the payment for the lien is no longer expected to go to the vault. This can be used maliciously by a vault owner to artificially increase their totalAssets(), allowing them to withdraw a much larger amount of assets than they should be able to. It is recommended to adjust the y-intercept and slope of the old payee and the new payee immediately upon the payee being set. Alternatively, Astaria suggests removing the ability for the owner to change the payee altogether, as this would prevent the issue. Spearbit has confirmed that removing the setPayee function in the PR 205 solves the issue.

### Original Finding Content

## Severity: High Risk

## Context
- LienToken.sol#L868-878
- LienToken.sol#L165-173

## Description
When `setPayee()` is called, the payment for the lien is no longer expected to go to the vault. However, this change doesn't impact the vault's `y-intercept` or `slope`, which are used to calculate the vault's `totalAssets()`. 

This can be used maliciously by a vault owner to artificially increase their `totalAssets()` to any arbitrary amount:
1. Create a lien from the vault.
2. Set `Payee` to a non-vault address.
3. Buyout the lien from another vault (this will cause the other vault's `y-int` and `slope` to increase, but will not impact the `y-int` and `slope` of the original vault because it'll fail the check on L165 that payee is a public vault).
4. Repeat the process again going the other way, and repeat the full cycle until both vaults have the desired `totalAssets()`.

For an existing vault, a vault owner can withdraw a small amount of assets each epoch. If, in any epoch, they are one of the only users withdrawing funds, they can perform this attack immediately before the epoch is processed. The result is that the withdrawal shares will be multiplied by `totalAssets() / totalShares()` to get the withdrawal rate, which can be made artificially high enough to wipe out the entire vault.

## Recommendation
Adjust the `y-intercept` and `slope` of the old payee and the new payee immediately upon the payee being set.

## Astaria
We're thinking of removing the ability for the owner to change the payee altogether. There's no clear benefit to having this in the first place, since the payee would have no guarantees on receiving funds since we reset payee on LienToken transfers. We can just lock `setPayee()` to only be callable by a `WithdrawProxy` (if it needs auction funds), which is the primary use case anyway.

## Spearbit
Confirmed, removing the `setPayee` function in the following PR PR 205 solves the issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

`Don't update state`

