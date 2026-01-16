---
# Core Classification
protocol: Dahlia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46372
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443
source_link: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
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
finders_count: 3
finders:
  - Saw-mon and Natalie
  - kankodu
  - Yorke Rhodes
---

## Vulnerability Title

Interest is not accrued before calling BorrowImpl.internalBorrow in Dahlia.supplyAndBorrow 

### Overview


The report discusses a bug in the code for the Dahlia protocol. The bug is related to the calculation of interest before borrowing assets. Due to this bug, the borrowed shares are calculated using outdated data, which can lead to incorrect results. The report recommends fixing the bug by ensuring that interest is accrued before calling the function for borrowing assets. The bug has been fixed in the latest commit for the Dahlia protocol.

### Original Finding Content

## Context
**Dahlia.sol#L252**

## Description
Interest is not accrued before calling `BorrowImpl.internalBorrow` in `Dahlia.supplyAndBorrow`. Accruing interest before calling `BorrowImpl.internalBorrow` is important; otherwise:

1. `borrowedShares` would be calculated with stale data.
2. The following inequality (BorrowImpl.sol#L81-L85) would also use stale data from before accruing interest: 

   ```solidity
   // Check if user has enough collateral
   (uint256 borrowedAssets, uint256 maxBorrowAssets) = MarketMath.calcMaxBorrowAssets(market,
   ownerPosition, collateralPrice);
   if (borrowedAssets > maxBorrowAssets) {
       revert Errors.InsufficientCollateral(borrowedAssets, maxBorrowAssets);
   }
   ```

   `borrowedAssets` would be calculated with stale data.

## Recommendation
Make sure to accrue interest before calling `BorrowImpl.internalBorrow`:

```solidity
_accrueMarketInterest(positions, market);
(borrowedAssets, borrowedShares) = BorrowImpl.internalBorrow(market, ownerPosition, borrowAssets, 0, owner,
receiver, 0);
```

## Status
**Dahlia:** Fixed in commit `bb8ce8fa`.  
**Cantina Managed:** Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Dahlia |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, kankodu, Yorke Rhodes |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443

### Keywords for Search

`vulnerability`

