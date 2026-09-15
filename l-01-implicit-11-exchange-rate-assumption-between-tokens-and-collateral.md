---
# Core Classification
protocol: Tangent_2025-12-08
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64049
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-12-08.md
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

[L-01] Implicit 1:1 exchange rate assumption between tokens and `collateral`

### Overview

See description below for full details.

### Original Finding Content


_Acknowledged_

The market contract architecture implicitly assumes a 1:1 exchange rate between `receipt` tokens and `collateral` tokens. This assumption is not documented and could lead to incorrect accounting or value transfer if **a future market implementation uses receipt tokens with a non-1:1 exchange rate** (e.g., yield-bearing vault tokens that accumulate value over time).

The `_withdraw` function in MarketCore calculates withdrawal amounts in collateral units and passes this value directly to `_transferCollateralWithdraw`:

```solidity
function _withdraw(uint256 amountToWithdraw, bool isReceiptOut) internal {
    // ... validation logic ...
    _transferCollateralWithdraw(msg.sender, amountToWithdraw, isReceiptOut);
}
```

In market implementations like `CurveGaugeMarket and StakeDaoVaultV2Market`, when `isReceipt = true`, the code transfers the same amount of receipt tokens without any exchange rate conversion:

```solidity
// CurveGaugeMarket.sol:43-52
function _transferCollateralWithdraw(address to, uint256 collatToWithdraw, bool isReceipt) internal override {
    if (isReceipt) {
        IGauge(receiptToken).transfer(to, collatToWithdraw);  
    } else {
        IGauge(receiptToken).withdraw(collatToWithdraw);
        collatToken.transfer(to, collatToWithdraw);
    }
}
```
This only works correctly if receipt tokens and collateral tokens maintain a 1:1 exchange rate.

Currently, all implemented markets (Curve Gauge, StakeDao Vault) appear to maintain 1:1 ratios. However, this is an implicit assumption that is not enforced or documented.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tangent_2025-12-08 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tangent-security-review_2025-12-08.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

