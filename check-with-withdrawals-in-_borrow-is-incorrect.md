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
solodit_id: 36803
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

Check with withdrawals in _borrow() is incorrect

### Overview


This bug report discusses a medium risk issue in the GasAccounting.sol code. The problem is with the check for withdrawals in the _borrow() function, as it seems to be incorrect and results in double counting. The report provides an example to illustrate the issue and suggests a possible solution. It also mentions another issue related to the check in the _borrow() function. The report recommends changing the code and mentions that the issue has been solved in a pull request. It also states that the issue has been verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
- `GasAccounting.sol#L48-L55`
- `GasAccounting.sol#L129-L134`

## Description
The check with withdrawals in function `_borrow()` doesn't seem correct because the balance is decreased with `safeTransferETH`, while withdrawals are increased, leading to a double count. This example illustrates the issue:

- Assume claims and the initial value of withdrawals are negligible.
- Assume atlas contains 100 ETH.
- Try to borrow 75 ETH:
  - `(address(this).balance < amount + claims + withdrawals)` 
  - `100 ETH < 75 ETH + 0 + 0` 
  - This is ok to borrow.
  - After this, `withdrawals == 75 ETH` and `balance == 25 ETH`.
  
- Now try to borrow an extra 10 ETH:
  - `(address(this).balance < amount + claims + withdrawals)` 
  - `25 ETH < 10 ETH + 0 + 75 ETH` 
  - This is not ok to borrow.

Thus, you can't borrow the extra 10 ETH, even though atlas still has enough ETH. However, if you directly borrow 85 ETH, then there is no problem.

Also see the issue "_releaseSolverLock() doesn't undo all the actions of _trySolverLock()" for another problem with the check in `_borrow()`.

### Code Snippet
```solidity
function borrow(uint256 amount) external payable {
    // ...
    if (_borrow(amount)) {
        SafeTransferLib.safeTransferETH(msg.sender, amount);
    } else {
        revert InsufficientAtlETHBalance(address(this).balance, amount);
    }
}

function _borrow(uint256 amount) internal returns (bool valid) {
    if (amount == 0) return true;
    if (address(this).balance < amount + claims + withdrawals) return false;
    withdrawals += amount;
    return true;
}
```

## Recommendation
Consider changing the code to:
- Change 
```solidity
if (address(this).balance < amount + claims + withdrawals) return false;
```
to
```solidity
if (address(this).balance < amount + claims) return false;
```

## Fastlane
- Solved in PR 234.

## Spearbit
- Verified.

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

