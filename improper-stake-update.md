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
solodit_id: 48019
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

Improper Stake Update

### Overview


The report discusses a bug in the handle_redeem function of the bucket module, which is responsible for redeeming $BUCK by taking collateral from bottles in ascending order. The bug occurs when the remaining redemption amount is less than the last bottle's buck amount, causing the loop to end prematurely and skip a necessary call to update the debtor's stakes. The bug has been fixed in the latest patch.

### Original Finding Content

## Handle Redeem in the Bucket Module

The `handle_redeem` function in the bucket module manages the redemption of `$BUCK` by taking collateral from the bottles in ascending order of their collateral ratio. 

## Code Snippet

```rust
} else {
    let redeemed_amount = compute_buck_value_to_collateral(
        remaining_redemption_amount,
        bucket.collateral_decimal,
        price,
        denominator
    );

    bottle::record_redeem(
        &mut bottle,
        redeemed_amount,
        remaining_redemption_amount
    );

    balance::join(
        &mut collateral_output,
        balance::split(&mut bucket.collateral_vault, redeemed_amount)
    );

    bottle::insert(
        &mut bucket.bottle_table,
        debtor,
        bottle,
        insertion_place
    );

    remaining_redemption_amount = 0;
    break;
};

// Update the debtor's stakes
bottle::update_stake_and_total_stake_by_debtor(
    &mut bucket.bottle_table,
    debtor
);
```

## Explanation

When redeeming bottles, the `else` case inside the `while` loop manages the last bottle's redemption. If the remaining redemption amount is less than the bottle's buck amount, the loop ends in the `else` case with a `break`, which skips the call to `bottle::update_stake_and_total_stake_by_debtor` on the last bottle.

## Remediation

To fix this issue, call `bottle::update_stake_and_total_stake_by_debtor` before the `break` statement in the `else` case.

### Patch

This issue was fixed in commit `2b68221`.

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

