---
# Core Classification
protocol: Symmetry
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48611
audit_firm: OtterSec
contest_link: https://www.symmetry.fi/
source_link: https://www.symmetry.fi/
github_link: https://github.com/symmetry-protocol/funds-program

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
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
  - Rajvardhan Agarwal
---

## Vulnerability Title

Validate Rules Missing Check

### Overview

See description below for full details.

### Original Finding Content

## Validate Rules Utility

In the `validate_rules` utility, the program allows `rules[i].num_assets` to be greater than 1 even if `rules[i].filter_by` is set as `FIXED_ASSET`. It can be seen in the code snippet below, that the `generate_weights` function adds uninitialized tokens from `rule.rule_assets` in such a scenario.

## Code Snippet

```rust
pub fn generate_weights(
    token_stats: &TokenStats,
    rule: &Rule,
) -> Vec<(u64, u64)> {
    let mut rule_assets = Vec::new();
    for j in 0..rule.num_assets as usize {
        let token = rule.rule_assets[j];
        let token_stats_info = token_stats.stats[token as usize][rule.weight_days as usize];
        let mut raw_weight: u64 = MAX_RULE_WEIGHT;
        // for fixed asset raw_weight should stay MAX_RULE_WEIGHT
        if rule.filter_by != FIXED_ASSET {
            [...]
        }
        rule_assets.push((token, asset_weight));
    }
}
```

## Remediation

A sanity check should be added in the `validate_rules` function to ensure that `rules[i].num_assets` is 1 if `rules[i].filter_by` is equal to `FIXED_ASSET`.

© 2022 OtterSec LLC. All Rights Reserved. 24 / 28

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Symmetry |
| Report Date | N/A |
| Finders | Robert Chen, Ajay Kunapareddy, OtterSec, Rajvardhan Agarwal |

### Source Links

- **Source**: https://www.symmetry.fi/
- **GitHub**: https://github.com/symmetry-protocol/funds-program
- **Contest**: https://www.symmetry.fi/

### Keywords for Search

`vulnerability`

