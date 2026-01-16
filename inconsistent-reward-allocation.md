---
# Core Classification
protocol: Marginfi Integration
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46931
audit_firm: OtterSec
contest_link: https://www.exponent.finance/
source_link: https://www.exponent.finance/
github_link: https://github.com/exponent-finance/exponent-core

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Inconsistent Reward Allocation

### Overview


There is a problem with how rewards are distributed in the Marginfi-standard and vault programs. The rewards are supposed to be based on the amount of SY tokens held, but in the vault program, they are based on the amount of YT tokens. This causes a discrepancy in the rewards received by users. Additionally, the calculation for the lambo_fund in the YieldTokenTracker is affected by this issue, leading to inaccurate emissions. The solution is to align the reward calculation methods and ensure that YT tokens are properly accounted for in the merge process. This issue has been resolved in a patch.

### Original Finding Content

## Discrepancy in Reward Distribution Between Marginfi Standard Program and Vault Program

There is a discrepancy between the utilization of **SY** and **YT** for reward distribution in the Marginfi-standard program and the vault program. 

In the Marginfi-standard program, the reward distribution is based on the amount of **SY** tokens held. This implies that the rewards are allocated proportionally to the **SY** tokens held by the users. However, the emissions calculated in the vault are based on the amount of **YT** tokens. The value of **YT** tokens depreciates as the **SY** exchange rate increases, resulting in a decrease in their value. Consequently, emissions are only allocated for the **sy_for_pt** amount, while rewards for **uncollected_sy** are not distributed to any user.

Furthermore, as the **SY** exchange rate increases, the amount of **YT** tokens decreases. This depreciation affects the emissions staging, resulting in a mismatch between the emissions staged and the actual rewards users should receive, depending on the timing of emissions staging relative to exchange rate changes.

```rust
>_ exponent_core/src/state/personal_yield_tracker.rs rust
fn calc_earned_emissions(&self, current_index: Number, lp_amount_user: u64) -> u64 {
    let delta = current_index - self.last_seen_index;
    let earned = delta * Number::from_natural_u64(lp_amount_user);
    earned.floor_u64()
}

pub fn dec_staged(&mut self, amount: u64) {
    self.staged = self
        .staged
        .checked_sub(amount)
        .expect("insufficient staged balance");
}
```

Additionally, `YieldTokenTracker::calc_earned_emissions` (shown above) calculates the **lambo_fund** using the **current_index** and **sy_balance**, derived from the **yt_balance**. Since **merge** does not account for **YT** tokens, these tokens remain in the yield position, resulting in an imbalance where **YT** tokens continue to contribute to the **lambo_fund** calculation, even though they should have been merged. Consequently, the emissions calculated based on these tokens will be inaccurate, resulting in incorrect emissions.

## Remediation

Align the reward calculation methods between the vault and the Marginfi standard program. Specifically, verify that both systems utilize a consistent metric for emission calculations. Also, ensure that **YT** tokens are correctly accounted for and converted to their **SY** equivalent before calculating emissions. **merge** should handle **YT** tokens properly to prevent them from remaining in the yield position.

## Patch

Resolved in **PR#606**.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Marginfi Integration |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.exponent.finance/
- **GitHub**: https://github.com/exponent-finance/exponent-core
- **Contest**: https://www.exponent.finance/

### Keywords for Search

`vulnerability`

