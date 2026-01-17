---
# Core Classification
protocol: Tangent_2025-10-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63872
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-10-30.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-04] Double-floor rounding in borrow path slightly favors users

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

In the borrow flow, both conversions use floor rounding, which (a) slightly underestimates current debt and (b) mints slightly fewer debt shares for the same borrowed amount (≤1 wei USG per operation). While economically negligible, this bias is systematic. 
```solidity
    function _borrow(address receiver, uint256 USGToBorrow, uint256 collatAmount, bool isLeverage) internal returns (uint256, uint256) {
        _verifyIsBorrowNotPaused();
        _verifyDebtInputNotZero(USGToBorrow);
        uint256 newDebtIndex = _checkpointIR();

        uint256 _userDebtShares = userDebtShares[msg.sender];

>>      uint256 newUserDebt = USGToBorrow + _convertToAmount(_userDebtShares, newDebtIndex); 

        //  Cache the new value in USG of the debt
>>      uint256 newUserDebtShares = _convertToShares(USGToBorrow, newDebtIndex);
<..>

    function _convertToAmount(uint256 debtShares, uint256 index) internal pure returns (uint256) {
        return _mulDiv(debtShares, index, RAY);
    }
<..>
    function _convertToShares(uint256 debt, uint256 index) internal pure returns (uint256) {
        return _mulDiv(debt, RAY, index);
    }    
```
Keep `amount` with floor but mint debt shares with **ceil** (e.g., `shares = mulDivRoundingUp(amount, RAY, index)`), or use OZ’s `Math.mulDiv(amount, RAY, index, Math.Rounding.Up)`, ensuring symmetric, protocol-friendly accounting.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tangent_2025-10-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-10-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

