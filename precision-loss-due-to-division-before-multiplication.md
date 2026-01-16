---
# Core Classification
protocol: Neutral Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61619
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/neutral-trade/52a6403b-648c-4ea6-be5e-c8b525acc9b7/index.html
source_link: https://certificate.quantstamp.com/full/neutral-trade/52a6403b-648c-4ea6-be5e-c8b525acc9b7/index.html
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 3

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Yamen Merhi
  - Hytham Farah
  - Mostafa Yassin
---

## Vulnerability Title

Precision Loss Due to Division Before Multiplication

### Overview


The client has marked a bug as "fixed" in the code. The bug affects the calculation of management fees and results in a loss of precision due to the use of sequential integer divisions. This leads to the protocol undercharging users for management fees over time. The bug is present in three files and can cause a slow but steady leak of value from the protocol's treasury. The recommendation is to refactor the code and perform all multiplications first, followed by a single division at the end. This will ensure mathematical accuracy and prevent value leakage.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `f1438d7c48b8e5accdb1fe6a4685433e2cbb8e85`.

**File(s) affected:**`programs/ntbundle/src/state/bundle.rs`, `programs/ntbundle/src/instructions/process_deposit.rs`, `programs/ntbundle/src/instructions/refund_deposit.rs`

**Description:** The current implementation for calculating management fees is susceptible to a loss of precision due to its reliance on sequential integer divisions. This will cause the protocol to undercharge users for management fees over the long term systematically.

```
let time_fraction = seconds_elapsed
                .checked_mul(bundle.asset_precision as u128)
                .ok_or(ErrorCode::MathError)?
                .checked_div(SECONDS_IN_YEAR)
                .ok_or(ErrorCode::MathError)?;

            // calculate fee percentage: (time_fraction * annual_fee_rate) / 10000
            let mgmt_fee_pct = time_fraction
                .checked_mul(annual_fee_rate)
                .ok_or(ErrorCode::MathError)?
                .checked_div(10000) // Convert from bps to decimal
                .ok_or(ErrorCode::MathError)?;
```

The calculation is performed in three steps:

A `time_fraction` is calculated, representing the portion of a year that has passed since the last fee collection. This calculation involves a division that truncates any remainder. The `time_fraction` is then used to calculate a `mgmt_fee_pct`, which involves another division and potential truncation.

Finally, this percentage is used to determine the `management_fee_shares`.

Because integer division in computing discards the remainder, any fractional component is lost at each step.

This error, while potentially small for any single calculation, compounds and guarantees that the final fee charged will be less than or equal to the correct amount, but never more. Over thousands of transactions and users, this results in a slow but steady leak of value from the protocol's treasury.

This is also the case for the P&L for shares:

```
let pnl_usd = pnl_per_share
    .checked_mul(user_bundle_account.shares)
    .ok_or(ErrorCode::MathError)?
    .checked_div(bundle.asset_precision as u128)
    .ok_or(ErrorCode::MathError)?;

// Step 2: Second division
let perf_fee_usd = pnl_usd
    .checked_mul(bundle.performance_fee as u128)
    .ok_or(ErrorCode::MathError)?
    .checked_div(10000)
    .ok_or(ErrorCode::MathError)?;

// Step 3: Third division
performance_fee_shares = perf_fee_usd
    .checked_mul(bundle.asset_precision as u128)
    .ok_or(ErrorCode::MathError)?
    .checked_div(share_price)
    .ok_or(ErrorCode::MathError)?;
```

**Recommendation:** To ensure mathematical accuracy and prevent value leakage, the management fee calculation should be refactored to perform all multiplications first, followed by a single division at the end.

This preserves the maximum precision throughout the calculation.

Instead of calculating intermediate values like `time_fraction` and `mgmt_fee_pct`, the final `management_fee_shares` should be calculated directly from the primary inputs (`user_bundle_account.shares`, `seconds_elapsed`, `bundle.management_fee_bps`) in one consolidated formula.

An example might look like this:

```
let numerator = user_bundle_account.shares
                .checked_mul(seconds_elapsed)
                .ok_or(ErrorCode::MathError)?
                .checked_mul(bundle.management_fee_bps as u128)
                .ok_or(ErrorCode::MathError)?;

            let denominator = (SECONDS_IN_YEAR as u128)
                .checked_mul(10000)
                .ok_or(ErrorCode::MathError)?;

            management_fee_shares = numerator
                .checked_div(denominator)
                .ok_or(ErrorCode::MathError)?;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 3/5 |
| Audit Firm | Quantstamp |
| Protocol | Neutral Trade |
| Report Date | N/A |
| Finders | Yamen Merhi, Hytham Farah, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/neutral-trade/52a6403b-648c-4ea6-be5e-c8b525acc9b7/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/neutral-trade/52a6403b-648c-4ea6-be5e-c8b525acc9b7/index.html

### Keywords for Search

`vulnerability`

