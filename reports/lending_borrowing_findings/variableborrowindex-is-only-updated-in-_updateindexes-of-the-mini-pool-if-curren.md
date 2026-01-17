---
# Core Classification
protocol: Astera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62295
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
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
finders_count: 3
finders:
  - Saw-mon and Natalie
  - Cergyk
  - Jonatas Martins
---

## Vulnerability Title

variableBorrowIndex is only updated in _updateIndexes of the mini pool if currentLiquidityRate

### Overview


The bug report is about a medium risk issue in a code called MiniPoolReserveLogic.sol. The code has a nested "if" block that may cause problems. This means that one "if" statement is inside another "if" statement. This is not how it is supposed to be in the Aave v2 code. It is possible that this nested "if" block can cause issues due to rounding errors or other factors. The recommendation is to fix the code by separating the "if" blocks and updating the index separately. The bug has been fixed in a commit called 5ddd6f4b and has been verified by Spearbit.

### Original Finding Content

## Non-Zero Condition Review

**Severity:** Medium Risk  
**Context:** MiniPoolReserveLogic.sol#L320-L340  

**Description:**  
The second `if` block is nested in this context, although it is not nested in the lending pool's `ReserveLogic` library (in Aave v2 it is nested):

```solidity
if (currentLiquidityRate != 0) {
    // ...
    if (scaledVariableDebt != 0) {
        // ...
    }
}
```

It is possible that `scaledVariableDebt` is non-zero even when `currentLiquidityRate` is 0 due to rounding errors or, for example, when both the `Cod3x` and reserve's owner's reserve factors sum up to 100%.

**Recommendation:**  
Make sure the `if` blocks are not nested and let the index updates happen separately:

```solidity
if (currentLiquidityRate != 0) {
    // ...
}
if (scaledVariableDebt != 0) {
    // ...
}
```

**Astera:** Fixed in commit 5ddd6f4b.  
**Spearbit:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Astera |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Cergyk, Jonatas Martins |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

