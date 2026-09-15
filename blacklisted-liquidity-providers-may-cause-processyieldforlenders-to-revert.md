---
# Core Classification
protocol: Huma Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35913
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Huma-2024-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Huma-2024-Spearbit-Security-Review.pdf
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
finders_count: 4
finders:
  - 0xLeastwood
  - Saw-Mon and Natalie
  - Jonatas Martins
  - Kankodu
---

## Vulnerability Title

Blacklisted liquidity providers may cause processYieldForLenders to revert

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
- **Files**: `TrancheVault.sol#L421-L444`, `PoolSafe.sol#L44-L49`

## Description
Many stablecoins maintain blacklists that frequently block accounts that are suspected of illicit activity. If a non-reinvesting lender is blacklisted, then it is no longer possible to process yield for other non-reinvesting lenders until they are forced to become a reinvesting lender.

```solidity
function processYieldForLenders() external {
    uint256 len = nonReinvestingLenders.length;
    uint256 price = convertToAssets(DEFAULT_DECIMALS_FACTOR);
    uint96[2] memory tranchesAssets = pool.currentTranchesAssets();
    
    for (uint256 i = 0; i < len; i++) {
        address lender = nonReinvestingLenders[i];
        uint256 shares = ERC20Upgradeable.balanceOf(lender);
        uint256 assets = (shares * price) / DEFAULT_DECIMALS_FACTOR;
        DepositRecord memory depositRecord = _getDepositRecord(lender);
        
        if (assets > depositRecord.principal) {
            uint256 yield = assets - depositRecord.principal;
            tranchesAssets[trancheIndex] -= uint96(yield);
            // Round up the number of shares the lender has to burn in order to receive
            // the given amount of yield. Round-up applies the favor-the-pool principle.
            shares = Math.ceilDiv(yield * DEFAULT_DECIMALS_FACTOR, price);
            ERC20Upgradeable._burn(lender, shares);
            poolSafe.withdraw(lender, yield);
            emit YieldPaidOut(lender, yield, shares);
        }
    }
    poolSafe.resetUnprocessedProfit();
    pool.updateTranchesAssets(tranchesAssets);
}
```

## Recommendation
For the sake of smoothness, implementing a try/catch statement for the `poolSafe.withdraw()` call is worth adding.

## Huma
Try/catch has been added in PR 405. We also fixed the same issue in the EA replacement function as discussed in the past. We also discovered by ourselves that `FirstLossCover` has the same problem, so we fixed that as well.

## Spearbit
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Huma Finance |
| Report Date | N/A |
| Finders | 0xLeastwood, Saw-Mon and Natalie, Jonatas Martins, Kankodu |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Huma-2024-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Huma-2024-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

