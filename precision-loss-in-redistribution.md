---
# Core Classification
protocol: Bucket Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48020
audit_firm: OtterSec
contest_link: https://bucketprotocol.io/
source_link: https://bucketprotocol.io/
github_link: https://github.com/Bucket-Protocol/v1-core

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
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Precision Loss In Redistribution

### Overview


The report describes a bug in the bottle module of a protocol, which is responsible for redistributing collateral and debt amounts to users. The bug occurs when dividing the amounts by the total stake, leading to imprecise accumulation due to rounding down values. The suggested solution is to factor the accumulators with a value to avoid this precision loss. The bug has been fixed in the latest patch.

### Original Finding Content

## Record Redistribution in the Bottle Module

The `record_redistribution` function in the Bottle module handles the redistribution of collateral and debt amounts to all Bottle users. This is done by dividing the collateral and debt amounts by the total stake amount and adding the results to the accumulators.

## Code Snippet

```rust
protocol/sources/bottle.move
public(friend) fun record_redistribution(
    table: &mut BottleTable,
    collateral_amount: u64,
    debt_amount: u64,
) {
    table.reward_per_unit_stake = table.reward_per_unit_stake + collateral_amount /
        table.total_stake;
    table.debt_per_unit_stake = table.debt_per_unit_stake + debt_amount /
        table.total_stake;
}
```

## Precision Issue

Since the accumulators are not factored by some value, directly dividing the collateral and debt amounts by the total stake leads to less precise rounded-down values. This imprecision results in inaccurate accumulation.

## Remediation

To avoid precision loss, factor the collateral and debt accumulators with an appropriate value.

## Patch

The issue has been fixed in commit `b2daf7f`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Bucket Protocol |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec |

### Source Links

- **Source**: https://bucketprotocol.io/
- **GitHub**: https://github.com/Bucket-Protocol/v1-core
- **Contest**: https://bucketprotocol.io/

### Keywords for Search

`vulnerability`

