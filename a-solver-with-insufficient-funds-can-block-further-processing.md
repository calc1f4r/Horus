---
# Core Classification
protocol: Fastlane Atlas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36819
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
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
  - Riley Holterhus
  - Blockdev
  - Gerard Persoon
---

## Vulnerability Title

A solver with insufficient funds can block further processing

### Overview


The bug report discusses a problem with a specific function called _settle() in the GasAccounting.sol file. The function is supposed to handle the costs associated with a Solver, but if the Solver does not have enough funds, the function reverts and blocks the processing of other solvers. This is not the expected behavior, as users would expect the next solver in the list to be used instead. The report suggests disallowing certain actions and recommends wrapping all solver-related actions in a try/catch statement. The bug has been solved in a pull request, which includes changes to the reconcile() function and blocking certain actions after it has been called. The issue has been verified by Spearbit.

### Original Finding Content

## Medium Risk Report

## Severity
**Medium Risk**

## Context
- `GasAccounting.sol#L254-L298`
- `GasAccounting.sol#L225-L246`

## Description
The function `_settle()` reverts if the Solver can't pay for the costs. When the function `_settle()` reverts, the `metacall()` also reverts. The costs could be gas usage or any `Borrow()`s after `validateBalances()`. This behavior allows a solver with insufficient funds to block further processing of the other solvers. However, a user would expect that when a solver fails, the next solver in the list would be used.

In comparison, when a solver doesn't win, and via `_releaseSolverLock()`, the gas `_assign()`ment fails, that error is ignored.

**Note:** `Borrow()`s after `validateBalances()` are questionable, see issue "Borrow()s after validateBalances()".

```solidity
function _settle( /*...*/ ) /*...*/ {
    // ...
    if (_assign(winningSolver, amountOwed, true, false)) {
        revert InsufficientTotalBalance((_claims + _withdrawals) - deposits);
    }
    // ...
}

function _releaseSolverLock( /*...*/ ) /*...*/ {
    // ...
    _assign(solverOp.from, gasUsed, false, bidFind); // failure to assign is ignored
}
```

## Recommendation
- Consider disallowing `Borrow()`s after `validateBalances()`, see issue "Borrow()s after validateBalances()".
- Consider wrapping all solver-related actions in a try/catch. For example, by implementing the following steps in `solverMetaTryCatch()` as well:
  - `_allocateValue()`
  - `_executePostOpsCall()`
  - `_settle()`

## Fastlane
**Solved in PR 227:**
1. `reconcile()` must be called, and only during the `SolverOperation` phase.
2. `borrow()` is blocked after `reconcile()` has been called, even if it is still during the `SolverOperation` phase.

## Spearbit
**Verified.**

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Fastlane Atlas |
| Report Date | N/A |
| Finders | Riley Holterhus, Blockdev, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf

### Keywords for Search

`vulnerability`

