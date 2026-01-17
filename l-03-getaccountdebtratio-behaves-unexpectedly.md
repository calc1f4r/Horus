---
# Core Classification
protocol: Fungify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31826
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
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
  - Zach Obront
---

## Vulnerability Title

[L-03] `getAccountDebtRatio()` behaves unexpectedly

### Overview

See description below for full details.

### Original Finding Content

The Comptroller's `getAccountDebtRatio()` is a public view function that can be called by external contracts to determine the debt ratio of a given account.

The function is defined as follows:

```solidity
function getAccountDebtRatio(address account) public view returns (uint, uint) {
    // uint[4] memory retVals; /* liquidity, shortfall, sumCollateral, sumBorrowPlusEffects */
    (Error err, uint[4] memory retVals) = getHypotheticalAccountLiquidityInternal(account, CToken(address(0)), 0, 0);
    if (retVals[1] == 0) {
        return (uint(err), 0);
    } else if (retVals[2] == 0) {
        return (uint(err), type(uint).max);
    }
    return (uint(err), retVals[3] * 1e18 / retVals[2]);
}
```
In the case where the account is in a shortfall, the function returns `borrows * 1e18 / collateral`, which tells us the ratio of how underwater the account is.

However, in the case where the account is solvent, the function overrides and returns `0`.

For external callers, a returned value of `0` implies that the account has no debt, which will not be accurate.

**Recommendation**

It is recommended to adapt the function to return the debt ratio correctly (which will require changes to the internal uses of the function in the liquidation flow). Rather than checking if the value is zero, the internal uses should be checking if the value is less than or equal to 1e18.

If this change is not desired, it is recommended to clearly specify in the function comments and documenation that it does not return a true debt ratio, and instead returns `0` for all solvent accounts.

**Review**

Comments added to explicitly explain the behavior in [7e0ee60622ddcbf384657da480ef9c851f2adc11](https://github.com/fungify-dao/taki-contracts/pull/9/commits/7e0ee60622ddcbf384657da480ef9c851f2adc11).

Renamed function to better capture behavior in [f2a13efd8a7c73f67ed8162c4ac075ee6a4d271b](https://github.com/fungify-dao/taki-contracts/pull/9/commits/f2a13efd8a7c73f67ed8162c4ac075ee6a4d271b).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Fungify |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

