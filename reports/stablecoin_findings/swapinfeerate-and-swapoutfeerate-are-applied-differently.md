---
# Core Classification
protocol: Bitcorn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46352
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/2ce1f8e6-2000-4b3f-a131-58931e0c445e
source_link: https://cdn.cantina.xyz/reports/cantina_bitcorn_november2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Denis Miličević
  - Sujith Somraaj
---

## Vulnerability Title

SwapInFeeRate and SwapOutFeeRate are applied differently 

### Overview

See description below for full details.

### Original Finding Content

## Context
No context files were provided by the reviewer.

## Description
In **SwapFacility**, the swap-in fee is applied as a percentage to withhold on the collateral coming in. This means if the fee is 100%, there is a full clawback, and the user receives no `debtTokens`. 

The swap-out fee, on the other hand, is applied as a surcharge. Even if set to 100%, there isn't any actual clawback that occurs. Instead, a user has to enter debt-to-collateral at a 2:1 ratio, or double the price. This methodology is somewhat unintuitive compared to the former but has the benefit of ensuring that users always get something, and that a clawback isn’t possible (albeit this should be enforced via saner fee limits).

For the **feeRecipient**, this isn’t a particular issue, as they will receive the same fee amount on either side of the swap for the same collateral amounts. However, it could be quite perplexing to users that fees are charged in different methodologies across the swaps, making it hard to reason about.

## Recommendation
Decide on a consistent methodology for applying the fee to achieve the same fee capture style across swap types. The former is likely the most intuitive, in which case the withholding would be applied on the debt rather than as a surcharge. This would require changing the function 

```solidity
swapDebtForExactCollateral(uint256 collateralOut, uint256 debtInMax, address to, uint256 deadline)
```

to something closer to 

```solidity
swapExactDebtForCollateral(uint256 debtIn, uint256 collateralOutMin, address to, uint256 deadline)
```

which would also align it closer to the behavior of 

```solidity
swapExactCollateralForDebt(uint256 collateralIn, uint256 debtOutMin, address to, uint256 deadline)
```

This makes it quite simple to precalculate and reason about the minimum amounts in this case, as they should just be `(inAmt * (1 - swapRate))` in either case.

## Bitcorn
This was applied as a multifaceted change without a specific commit in `SwapFacility.sol#L182`.

## Cantina Managed
Verified fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Bitcorn |
| Report Date | N/A |
| Finders | Denis Miličević, Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_bitcorn_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/2ce1f8e6-2000-4b3f-a131-58931e0c445e

### Keywords for Search

`vulnerability`

