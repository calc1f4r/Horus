---
# Core Classification
protocol: Mysten Deepbook
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47064
audit_firm: OtterSec
contest_link: https://mystenlabs.com/
source_link: https://mystenlabs.com/
github_link: https://github.com/MystenLabs/deepbookv3

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
  - Robert Chen
  - Sangsoo Kang
  - MichałBochnak
---

## Vulnerability Title

Code Optimizations

### Overview

See description below for full details.

### Original Finding Content

## Mysten Deepbook Audit 05 — General Findings

## Issues

1. In `big_vector::drop` when a `BigVector` instance is dropped, it recursively deallocates all its nodes in a single transaction. If the `BigVector` is large, containing more than 1000 nodes, this will exceed the object runtime limits imposed by the Sui blockchain (e.g., `object_runtime_max_num_cached_objects` and `object_runtime_max_num_store_entries`), resulting in transaction failure.

2. In `pool`, there is a potential scalability issue. If a user has a large number of open orders, attempting to cancel all of them in a single transaction may result in exceeding the `max_computation_budget` or `max_num_event_emit`.

3. The assertions in `pool::swap_exact_quantity` check that at least one of `base_quantity` or `quote_quantity` is greater than zero, and both `base_quantity` and `quote_quantity` are not greater than zero simultaneously. The expression `((base_quantity > 0) != (quote_quantity > 0))` evaluates to true if exactly one of `base_quantity` or `quote_quantity` is greater than zero. This is equivalent to the combined logic of the original two assertions.

    ```rust
    > _pool.moverust
    public fun swap_exact_quantity<BaseAsset, QuoteAsset>(
    [...]
    ): (Coin<BaseAsset>, Coin<QuoteAsset>, Coin<DEEP>) {
        let mut base_quantity = base_in.value();
        let quote_quantity = quote_in.value();
        assert!(base_quantity > 0 || quote_quantity > 0, EInvalidQuantityIn);
        assert!(!(base_quantity > 0 && quote_quantity > 0), EInvalidQuantityIn);
        [...]
    }
    ```

4. Prevent the creation of a pool that is both whitelisted and stable, as a utilization of Deep tokens, which are essential for fee collection in non-whitelisted pools, will not be possible in stable pools.

## Remediation

1. Modify `big_vector::drop` to distribute the node deletion process across multiple transactions.

2. Allow users to specify the number of orders they want to cancel in a single transaction.

3. Replace the two assertions in `swap_exact_quantity` with the above expression.

4. Add an assertion to check if both `whitelisted_pool` and `stable_pool` are not set to true simultaneously, instead of setting `self.stable = false` regardless of the whitelisted parameter.

## Patch

1. Resolved in PR #176.

2. Resolved in PR #174.

3. Resolved in PR #188.

4. Resolved in PR #215.

© 2024 Otter Audits LLC. All Rights Reserved. 20/27

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Deepbook |
| Report Date | N/A |
| Finders | Robert Chen, Sangsoo Kang, MichałBochnak |

### Source Links

- **Source**: https://mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/deepbookv3
- **Contest**: https://mystenlabs.com/

### Keywords for Search

`vulnerability`

