---
# Core Classification
protocol: Pyth Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48824
audit_firm: OtterSec
contest_link: https://pyth.network/
source_link: https://pyth.network/
github_link: https://github.com/pyth-network/governance.

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
finders_count: 3
finders:
  - Kevin Chow
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Frozen Vesting Possible

### Overview

See description below for full details.

### Original Finding Content

## Periodic Vesting Concerns

With very large `num_periods` or `period_duration` in periodic vesting, it is possible to specify a schedule that never vests, resulting in tokens being non-withdrawable.

## Code Snippet

```rust
let time_passed: u64 = current_time
    .checked_sub(start_date)
    .unwrap()
    .try_into()
    .unwrap();
let periods_passed = time_passed / period_duration;
// Definitely round this one down
if periods_passed >= num_periods {
    0
} else {
    // Additional logic here
}
```

## Remediation

It may also be good practice to limit how far in the future the `num_periods` and `period_duration` can be (for example, one year), to prevent tokens from vesting for impractically long periods.

## Patch

Pyth Data Association acknowledges the finding but doesn't believe it has security implications. However, they may deploy a fix to address it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pyth Governance |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen, OtterSec |

### Source Links

- **Source**: https://pyth.network/
- **GitHub**: https://github.com/pyth-network/governance.
- **Contest**: https://pyth.network/

### Keywords for Search

`vulnerability`

