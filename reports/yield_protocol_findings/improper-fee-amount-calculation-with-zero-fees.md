---
# Core Classification
protocol: Streamflow
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48224
audit_firm: OtterSec
contest_link: https://streamflow.finance/
source_link: https://streamflow.finance/
github_link: https://github.com/streamflow-finance/aptos-streamflow-module

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
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Improper Fee Amount Calculation With Zero Fees

### Overview


This bug report is about an error in the code for calculating fees in a protocol. The code currently uses a function called "fee_amount" to calculate the fee for a given amount based on a parameter called "fees" which is measured in basis points (bps). However, there is an issue with the code when the value for "fees" is set to zero. In this case, the function incorrectly returns the total amount instead of zero as the fee. This means that if someone tries to calculate the fee for an amount of 125 with a bps of zero, the function will return 125 instead of the correct fee of zero. To fix this, the code needs to be modified to check for a value of 10000 for "fees" instead of zero. This issue has been addressed in a recent patch.

### Original Finding Content

## Documentation for `protocol::fee_amount`

The `protocol::fee_amount` function is used to calculate the fee for a given amount using the input parameter `fees` as basis points (bps).

## Code Implementation

```rust
sources/protocol.move
fun fee_amount(amount: u64, fees: u64): u64 {
    if (fees == 0) {
        return amount;
    };
    (amount * fees) / 10000
}
```

## Issue Description

Currently, the case of `fees == 0` incorrectly returns the total amount as the fee. Instead, the function should check for `fees == 10000` to return the total amount as the fee correctly.

### Proof of Concept

If the amount is `125` and the bps is zero, then the fee amount should be zero. However, in this case, the current implementation of `protocol::fee_amount` returns the total amount as the fee amount. 

Therefore, if we call:
```
fee_amount(125, 0)
```
then `125` will be returned instead of `0`.

## Remediation

To fix this issue, modify the check to:

```rust
if (fees == 10000) {
    return amount;
}
```

## Patch

The issue has been fixed in commit `bd4f2e9`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Streamflow |
| Report Date | N/A |
| Finders | Robert Chen, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://streamflow.finance/
- **GitHub**: https://github.com/streamflow-finance/aptos-streamflow-module
- **Contest**: https://streamflow.finance/

### Keywords for Search

`vulnerability`

