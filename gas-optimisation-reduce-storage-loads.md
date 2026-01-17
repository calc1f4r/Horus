---
# Core Classification
protocol: Aave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19256
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Gas Optimisation - Reduce Storage Loads

### Overview

See description below for full details.

### Original Finding Content

## Description

Storage loads are an expensive gas operation with SLOAD costing 800 gas [3]. The functions `_executeRepay()` and `swapBorrowRateMode()` call the function `Helpers.getUserCurrentDebt()`. The function `Helpers.getUserCurrentDebt()` performs two SLOAD operations to obtain the stable debt token address and variable debt token address. These two addresses are already loaded in memory in `reserveCache` in the calling functions.

## Recommendations

Consider updating the two functions such that they use the addresses stored in memory rather than those from state storage.

---

## AAV-26 Miscellaneous General Statements - 2

## Asset Contracts/

**Status:** Open  
**Rating:** Informational

### Description

This section describes general observations made by the testing team during this assessment that do not have direct security implications:

- In `ReserveLogic.sol`, the function `_accrueToTreasury()` was renamed from `_mintToTreasury()`. However, the helper struct `MintToTreasuryLocalVars` was not renamed. Consider also updating this struct name.
  
- **Spelling and Typos:**
  - `ILendingPoolConfigurator.sol`
    - line [331]: "Freezes a reserve. A frozen reserve doesn’t allow any new deposit, borrow or rate swap" -> "... deposits, borrows, or rate swaps"
    - line [344]: "A paused reserve allow now user moves such as deposit, borrow, repay, swap interestrate, liquidate"
  - `LendingPoolConfigurator.sol`
    - line [491]: "/ /might happen is a reserve was dropped" -> "/ /might happen if ..."
  - `ReserveConfiguration.sol`
    - line [36]: "/ / bits 61 62 63 unused yet" -> "/ / bits 61 62 63 unused"
  - `AToken.sol`
    - line [175]: "... the interest ccrued." -> "... the interest accrued"

### Recommendations

Ensure that the comments are understood and acknowledged, and consider implementing the suggestions above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Aave |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/aave/aave-protocol/review.pdf

### Keywords for Search

`vulnerability`

