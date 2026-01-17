---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25836
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/281

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

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - caventa
  - obront
---

## Vulnerability Title

[M-20] Users can liquidate themselves before others, allowing them to take 13% above their borrowers

### Overview


This bug report is about a function in the AstariaRouter.sol code called `canLiquidate()`. This function allows a borrower to liquidate their own loan even if the loan has not expired, which gives them an unfair advantage over their lenders. To demonstrate this, a proof of concept was provided where a borrower puts up collateral, takes out a loan, and then liquidates it right before it expires. This allows them to keep the loan and get a bonus of 1.3 WETH. The recommended mitigation step is to not allow users to liquidate their own loans until they are liquidatable by the public. This bug was confirmed by SantiagoGregory (Astaria).

### Original Finding Content


<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/AstariaRouter.sol#L611-L619>

The `canLiquidate()` function allows liquidations to take place if either (a) the loan is over and still exists or (b) the caller owns the collateral.

In the second case, due to the liquidation fee (currently 13%), this can give a borrower an unfair position to be able to reclaim a percentage of the liquidation that should be going to their lenders.

### Proof of Concept

*   A borrower puts up a piece of collateral and takes a loan of 10 WETH
*   The collateral depreciates in value and they decide to keep the 10 WETH
*   Right before the loans expire, the borrower can call `liquidate()` themselves
*   This sets them as the `liquidator` and gives them the first 13% return on the auction
*   While the lenders are left at a loss, the borrower gets to keep the 10 WETH and get a 1.3 WETH bonus

### Recommended Mitigation Steps

Don't allow users to liquidate their own loans until they are liquidatable by the public.

**[SantiagoGregory (Astaria) confirmed](https://github.com/code-423n4/2023-01-astaria-findings/issues/281)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | caventa, obront |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/281
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

