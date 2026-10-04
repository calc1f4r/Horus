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
solodit_id: 36802
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

Circumvent AtlETH unbonding period

### Overview


The report discusses a bug in the GasAccounting.sol code, specifically in the function _assign(). This function allows for the usage of ETH that is bonded, but it can be abused in certain situations. The bug allows for a party to combine all roles (user, auctioneer, bundler, solver, and DappControl) and borrow ETH after the validateBalances() function has been called. This borrowed amount is then subtracted from the bonded balance, effectively freeing up the ETH without waiting for the AtlETH unbond period. The recommended solution is to follow the solution for "Borrow() s after validateBalances()" and the bug has been fixed in PR 227. Spearbit has verified the fix. The severity of this bug is considered medium risk.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
`GasAccounting.sol#L143-L185`

## Description
The function `_assign()` allows the usage of ETH that is bonded. This is what it is designed for. Here is an approach to abuse this:

- Assume one party combines all roles: user, auctioneer, bundler, solver, and DappControl.
- The party borrows ETH after `validateBalances()`, see issue "Borrow() s after validateBalances()".
- Assume the borrowed amount is less than the bonded balance of the party.
- With `_settle()`, the borrowed amount is subtracted from the bonded balance of the party.
- The party still possesses the borrowed amount.

So effectively, ETH is freed while it was bonded, without having to wait for the AtlETH unbond period.

```solidity
function _assign(address owner, uint256 amount, bool solverWon, bool bidFind) internal returns (bool isDeficit) {
    // ...
    EscrowAccountAccessData memory aData = accessData[owner];
    if (aData.bonded < amt) {
        // ...
    } else {
        aData.bonded -= amt;
    }
    accessData[owner] = aData;
    // ...
}
```

## Recommendation
See the solution for "Borrow() s after validateBalances()".

## Fastlane
Fixed in PR 227 by only allowing `borrow()` to be called in `SolverOperation` phase or before.

## Spearbit
Verified.

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

