---
# Core Classification
protocol: Mysten Labs Sui
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48095
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/sui

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
finders_count: 5
finders:
  - Cauê Obici
  - Michal Bochnak
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Potential Overflow In Threshold

### Overview


The bug report is about a function called "quorum_threshold" in the commitee.rs file, which is used to calculate a value called "StakeUnit". However, the function has a problem where it does not consider the voting rights of the Committee object when it is initialized. This leads to an incorrect value being returned due to an overflow. To fix this, the suggested solution is to replace the current implementation of the function with constants, as the total voting power and quorum threshold remain fixed and are not affected by changes in the stake. This issue has been fixed in a patch with the code "9bbf7b9".

### Original Finding Content

## Quorum Threshold Calculation Issue in `commitee.rs`

`commitee.rs` includes a helper function for calculating `quorum_threshold`. However, this function does not account for where the Committee object is initialized with voting rights, resulting in a return of an incorrect value due to an overflow.

## Code Snippet

```rust
pub fn quorum_threshold(&self) -> StakeUnit {
    // If N = 3f + 1 + k (0 <= k < 3)
    // then (2 N + 3) / 3 = 2f + 1 + (2k + 2)/3 = 2f + 1 + k = N - f
    2 * self.total_votes / 3 + 1 // overflow possible
}
```

## Remediation

Replace the current implementation of `quorum_threshold` with constants since the total voting power and quorum threshold remain fixed and are not affected by changes in the stake.

## Patch

Fixed in commit `9bbf7b9`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Labs Sui |
| Report Date | N/A |
| Finders | Cauê Obici, Michal Bochnak, James Wang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/sui
- **Contest**: https://mystenlabs.com/

### Keywords for Search

`vulnerability`

