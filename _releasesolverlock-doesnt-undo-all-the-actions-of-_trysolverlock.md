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
solodit_id: 36785
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Fastlane-Spearbit-Security-Review-April-2024.pdf
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
  - Riley Holterhus
  - Blockdev
  - Gerard Persoon
---

## Vulnerability Title

_releaseSolverLock() doesn't undo all the actions of _trySolverLock()

### Overview


The bug report discusses a high-risk issue in the GasAccounting.sol code. The function _releaseSolverLock() does not properly undo all the actions of the _trySolverLock() function, leaving the value of _solverLock set to the latest solver. This allows unauthorized calls to the reconcile() function and can lead to incorrect values in the withdrawals variable. Furthermore, _releaseSolverLock() is not always called, which can result in solvers not being reimbursed or receiving gas costs. The report recommends making changes to the _releaseSolverLock() function and renaming it to _handleSolverAccounting(). The issue has been resolved in PR 271 and verified by Spearbit.

### Original Finding Content

## Severity: High Risk

**Context:**  
GasAccounting.sol#L208-L246, GasAccounting.sol#L129-L134

**Description:**  
The function `_releaseSolverLock()` doesn't undo all the actions of `_trySolverLock()`.  
Function `_releaseSolverLock()` keeps `_solverLock` set to the (latest) solver, which means that in the `AllocateValue` hook and `PostOps` hook this value is still set. This allows `reconcile()` to still be called, even after it has been made authorized. See issue "reconcile() can be called by anyone".

Function `_releaseSolverLock()` doesn't undo the addition to withdrawals. This is good for the winning solver because the ETH has been sent to `solverMetaTryCatch()`. However, if `solverMetaTryCatch()` reverts, this is not good. The value of withdrawals will increase with every unsuccessful solver until eventually it is higher than the `address(this).balance`. After that, the next solvers will fail because `_borrow()` will return false. Also see issue "Check with withdrawals in _borrow() not correct".

Furthermore, `_releaseSolverLock()` isn't always called, see issues:
- "Solvers don't always reimburse the bundler".
- "Winning solver doesn't get gas costs _assign() ed".

Sometimes, `_releaseSolverLock()` is called without `_trySolverLock()`:
- "_releaseSolverLock() can be run without _trySolverLock()".

Additionally, function `_releaseSolverLock()` assigns used gas, which isn't shown in the function name.

```solidity
function _trySolverLock(SolverOperation calldata solverOp) internal returns (bool valid) {
    if (_borrow(solverOp.value)) {
        _solverLock = uint256(uint160(solverOp.from));
        return true;
    } else {
        return false;
    }
}

function _releaseSolverLock( /*...*/ ) /*...*/ {
    // doesn't set _solverLock
    // doesn't change withdrawals
}

function _borrow(uint256 amount) internal returns (bool valid) {
    // ...
    if (address(this).balance < amount + claims + withdrawals) return false;
    withdrawals += amount;
    return true;
}
```

**Recommendation:**  
Decrease withdrawals if `solverMetaTryCatch()` has reverted. This could be done by moving the `_borrow()` from `_trySolverLock()` to a `borrow()` inside `solverMetaTryCatch()`. In that case `{ value: solverOp.value }` should not be sent to `solverMetaTryCatch()`. After this change, the values would be returned to their original value after a revert of `solverMetaTryCatch()`. Also see issue "Check with withdrawals in _borrow() not correct".

`_releaseSolverLock()` should preferably set `_solverLock` to `_UNLOCKED_UINT`. To save some gas, this can also be done before the `AllocateValue` hook and `PostOps` hook, so for example at the end of function `_executeSolverOperation()`. Consider changing the function name of `_releaseSolverLock()` to indicate it is also used to assign used gas.

**Fastlane:**  
Resolved in PR 271. There is no longer a `_trySolverLock()` function, and instead, the logic it used to hold (i.e., `_borrow()` the `solverOp.value` and if that succeeds, set `_solverLock` to the current solver) is now done directly in `solverCall()` before Atlas calls directly to the solver. If the solver call or the postSolver call fails, this `solverCall()` function fails in a try-catch style, reverting the effects of what used to be `_trySolverLock()`.  
`_releaseSolverLock()` has been renamed to `_handleSolverAccounting()`. We still do not set `_solverLock` to `_UNLOCKED_UINT` in `_handleSolverAccounting()` (if a solver fails). The case of no successful solver is handled explicitly in `_settle()` and does not use the "stale" solver address in `_solverLock`.

**Spearbit:**  
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

