---
# Core Classification
protocol: Raydium AMM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48316
audit_firm: OtterSec
contest_link: https://raydium.io/
source_link: https://raydium.io/
github_link: https://github.com/raydium-io/raydium-amm

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
finders_count: 4
finders:
  - Maher Azzouzi
  - Robert Chen
  - OtterSec
  - William Wang
---

## Vulnerability Title

Stale Open Orders Calculations

### Overview


The Raydium AMM (Automated Market Maker) has a bug that causes it to cancel orders on the orderbook in the direction of the swap, which can impact liquidity for large swaps. This is due to a calculation error where the cancellation of orders does not update the calculated free token counts, resulting in the AMM incorrectly skipping the settlement of funds on large swaps. As a result, these large swaps will fail. The bug can be fixed by either refreshing the open orders account or removing a check that verifies the balance in the open orders account. This issue has been resolved in the latest patch.

### Original Finding Content

## Raydium AMM Order Cancellation and Settlement Issues

During swap operations, the Raydium AMM will cancel orders on the orderbook in the direction of the swap in order to free up liquidity for potentially large swaps.

```rust
for ids in amm_order_ids_vec.iter() {
    Invokers::invoke_dex_cancel_orders_by_client_order_ids(
        serum_dex_info.clone(),
        market_info.clone(),
        bids_info.clone(),
        asks_info.clone(),
        open_orders_info.clone(),
        authority_info.clone(),
        event_queue_info.clone(),
        AUTHORITY_AMM,
        amm.nonce as u8,
        *ids,
    )?;
}
```

However, the subsequent calculation for settlement uses a cached OpenOrders account. This account is loaded previously in the instruction but crucially represents a copy of the actual underlying account data.

```rust
let (market_state, open_orders) = Processor::load_serum_market_order(
    market_info,
    open_orders_info,
    authority_info,
    &amm,
    false,
)?;
```

This means that the cancellation of orders will not update the calculated free token counts, causing the AMM to incorrectly skip the settlement of funds on large swaps.

```rust
if swap_amount_out > token_pc.amount
    && swap_amount_out <= token_pc.amount.checked_add(open_orders.native_pc_free).unwrap()
{
```

As a result, large swaps will fail. More precisely, if the amount of funds in the AMM’s reserves are insufficient to satisfy the swap, the swap will fail.

## Remediation

Consider either refreshing the open orders account to properly load the native PC and coin counts. Alternatively, remove this check to attempt the settlement of funds regardless of the balance in the open orders account. Note that assuming the AMM invariant holds, this check should always be true.

## Patch

Resolved in `0b25381`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Raydium AMM |
| Report Date | N/A |
| Finders | Maher Azzouzi, Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://raydium.io/
- **GitHub**: https://github.com/raydium-io/raydium-amm
- **Contest**: https://raydium.io/

### Keywords for Search

`vulnerability`

