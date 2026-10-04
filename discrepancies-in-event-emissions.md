---
# Core Classification
protocol: Thala Swap + Math V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46719
audit_firm: OtterSec
contest_link: https://www.thalalabs.xyz/
source_link: https://www.thalalabs.xyz/
github_link: https://github.com/ThalaLabs/thala-modules/thalaswap_v2

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
  - Bartłomiej Wierzbiński
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Discrepancies in Event Emissions

### Overview

See description below for full details.

### Original Finding Content

## Liquidity and Swap Event Issues in thalaswap_v2

## 1. Issue with `add_liquidity_weighted`

In the current implementation of `pool::add_liquidity_weighted`, `AddLiquidityEvent` emits amounts (the raw values of assets initially provided to the function) instead of `remained_assets`, which is the actual amount of assets the user deposited into the pool.

```rust
>_ thalaswap_v2/sources/pool.move rust
public fun add_liquidity_weighted(pool_obj: Object<Pool>, assets: vector<FungibleAsset>):
→ (FungibleAsset, vector<FungibleAsset>) acquires PauseFlag, Pool {
    [...]
    event::emit(AddLiquidityEvent {
        pool_obj,
        metadata,
        amounts,
        minted_lp_token_amount: preview.minted_lp_token_amount,
        pool_balances: pool_balances(pool_obj),
    });
    (lp_token, refunds)
}
```

## 2. Issue with `swap_exact_out_stable` and `swap_exact_out_metastable`

In the current implementations of `swap_exact_out_stable` and `swap_exact_out_metastable`, the `amount_in` value logged by the `SwapEvent` is provided by the users. However, the `amount_in` that is passed by the user may differ from the actual `amount_in` needed to achieve the desired output (`amount_out`).

```rust
>_ thalaswap_v2/sources/pool.move rust
public fun swap_exact_out_stable([...]) [...] {
    [...]
    event::emit(SwapEvent {
        pool_obj,
        metadata: pool_assets_metadata(pool_obj),
        idx_in: preview.idx_in,
        idx_out: preview.idx_out,
        amount_in,
        amount_out,
        total_fee_amount: preview.total_fee_amount,
        protocol_fee_amount: preview.protocol_fee_amount,
        pool_balances: pool_balances(pool_obj),
    });
    [...]
}
```

## Remediation

1. Replace `amounts` in `AddLiquidityEvent` with `remained_assets` since it represents the actual assets deposited into the pool.
2. Pass the exact input amount that was actually utilized in the swap (`preview.amount_in`) to `SwapEvent` to ensure proper logging of swap parameters.

## Patch

1. Fixed in `7df3ae8`.
2. Fixed in `19dc5f1`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Thala Swap + Math V2 |
| Report Date | N/A |
| Finders | Bartłomiej Wierzbiński, Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://www.thalalabs.xyz/
- **GitHub**: https://github.com/ThalaLabs/thala-modules/thalaswap_v2
- **Contest**: https://www.thalalabs.xyz/

### Keywords for Search

`vulnerability`

