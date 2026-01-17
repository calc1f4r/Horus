---
# Core Classification
protocol: Hubble Kamino
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47877
audit_firm: OtterSec
contest_link: https://kamino.finance/
source_link: https://kamino.finance/
github_link: https://github.com/hubbleprotocol/kamino-lending

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
finders_count: 4
finders:
  - Akash Gurugunti
  - Robert Chen
  - Thibault Marboud
  - OtterSec
---

## Vulnerability Title

Inconsistent Calculation Of Max Withdraw Value

### Overview

See description below for full details.

### Original Finding Content

## Withdraw Obligation Collateral

`withdraw_obligation_collateral` utilizes the loan-to-value (LTV) ratio from the `withdraw_reserves` configuration to calculate `max_withdraw_value`, which may not align with the user’s obligation if the obligation’s elevation group is different from that of the reserve, resulting in incorrect maximum limits and a loss of funds for the user. `obligation.allowed_borrow_value` is calculated based on the loan-to-value on the elevation group; thus, it is best to maintain consistency and utilize the value specified in the associated elevation group.

## Lending Operations in Rust

```rust
pub fn withdraw_obligation_collateral(
    lending_market: &LendingMarket,
    withdraw_reserve: &Reserve,
    obligation: &mut Obligation,
    collateral_amount: u64,
    slot: Slot,
    withdraw_reserve_pk: Pubkey,
) -> Result<u64> {
    [...]
    let max_withdraw_value =
        obligation.max_withdraw_value(Rate::from_percent(loan_to_value_ratio_pct))?;
    [...]
}
```

## Proof of Concept

Suppose a lending protocol has two elevation groups: **Group A** and **Group B**. User A has an obligation associated with Group A, and they want to withdraw collateral from a reserve (call it **Reserve X**). Reserve X has its own loan-to-value ratio configured in its settings.

1. `withdraw_obligation_collateral` is called to withdraw collateral from User A’s obligation. It utilizes the loan-to-value ratio from Reserve X’s configuration to calculate `max_withdraw_value`.
2. However, since User A’s obligation is associated with Group A, the loan-to-value ratio they should follow is the one specific to Group A, not the generic loan-to-value ratio of Reserve X. The protocol allows different loan-to-value ratios for different elevation groups.
3. If the loan-to-value ratio for Group A is different from that of Reserve X, User A may be unable to withdraw as much collateral as they should based on their obligation’s configuration. They may withdraw less collateral than expected or encounter an error indicating that the withdrawal amount exceeds the maximum allowed by the configuration of Reserve X.

## Kamino Finance Audit 04 | Vulnerabilities

### Remediation

Ensure `withdraw_obligation_collateral` utilizes the loan-to-value ratio specific to the elevation group associated with the user’s obligation.

### Patch

Fixed in PR#110 by considering the loan-to-value ratio of the elevation group associated with the user’s obligation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Hubble Kamino |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, Thibault Marboud, OtterSec |

### Source Links

- **Source**: https://kamino.finance/
- **GitHub**: https://github.com/hubbleprotocol/kamino-lending
- **Contest**: https://kamino.finance/

### Keywords for Search

`vulnerability`

