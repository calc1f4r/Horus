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
solodit_id: 48223
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

Incorrect Withdraw Fee Calculation On Update

### Overview


The bug report states that in the protocol::update function, there is an issue with the fee calculation for automatic withdrawals. The code currently uses the contract's start time to calculate the fee, which results in the fee being recalculated for a period that the user has already paid for. The recommended solution is to use the old_end_time instead of the contract's start time for fee calculation. This issue has been fixed in the code by calculating the additional fee from the old_end_time.

### Original Finding Content

## Update on Protocol Fee Calculation

In `protocol::update`, the change in `amount_per_period` triggers an additional fee calculation using `withdrawal_fees` based on `contract.start`.

**File**: `sources/protocol.move`

```rust
if (old_end_time < contract.end && contract.meta.automatic_withdrawal) {
    let additional_withdrawal_fees = withdrawal_fees(
        contract.start,
        contract.end, 
        contract.meta.withdrawal_frequency, 
        get_tx_fee()
    );
    coin::transfer<AptosCoin>(
        authority, 
        get_withdrawor_address(),
        additional_withdrawal_fees
    );
}
```

However, using the start time for fee calculation results in the fee being recalculated for the period that the user has already paid for.

## Remediation
Use `old_end_time` instead of `contract.start` in `protocol::update` when calculating the additional fee using `withdrawal_fees`.

## Patch
Fixed in `bd4f2e9` by calculating the additional fee from `old_end_time`.

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

