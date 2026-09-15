---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7306
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
  - wrong_math

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

Public vault's yIntercept is not updated when the full amount owed is not paid out by a Seaport auction.

### Overview


This bug report is related to the LienToken.sol#L587 of the auction. It is classified as a high-risk issue. The problem is that when the full amount owed for a lien is not paid out during the callback from Seaport to a collateral's ClearingHouse and if the payee is a public vault, the payee.totalAssets() would reflect a wrong value.

The recommendation is to call decreaseYIntercept with the difference ofamountOwed and the payment received from the Seaport auction sale when this scenario occurs. This issue has been solved by PR 219 and verified by Spearbit.

### Original Finding Content

## Severity: High Risk

**Context:** LienToken.sol#L587

**Description:** When the full `amountOwed` for a lien is not paid out during the callback from Seaport to a collateral's ClearingHouse and if the payee is a public vault, we would need to decrement the `yIntercept`, otherwise the `payee.totalAssets()` would reflect a wrong value.

**Recommendation:** When the above scenario happens make sure to call `decreaseYIntercept` with the difference of `amountOwed` and the payment received from the Seaport auction sale.

**Astaria:** Solved by PR 219.

**Spearbit:** Verified.

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

`Wrong Math`

