---
# Core Classification
protocol: Deriverse Dex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64530
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
github_link: none

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
  - RajKumar
  - Ctrus
  - Alexzoid
  - JesJupyter
---

## Vulnerability Title

Referral Incentives Disabled for All Legitimate Users During Any Liquidation

### Overview


This bug report describes an issue where the `margin_call` flag is set to true for all subsequent orders after detecting a liquidation, causing referral rewards to be disabled for all users regardless of whether they are involved in the liquidation or not. This affects the overall incentive system and can result in losses for legitimate users. The recommended solution is to only set the `margin_call` flag for actual liquidation trades. This issue has been fixed in the latest version of the protocol.

### Original Finding Content

**Description:** Once the engine detects any instrument that requires liquidation (`is_long_margin_call` or `is_short_margin_call`), the `margin_call` flag is set to true for every subsequent `new_perp_order`. This flag is passed unchanged into `match_{ask,bid}_orders`, which disables referral payouts while it is `true`. As a result, all users— even those submitting normal orders unrelated to the liquidation — stop receiving/producing referral rewards for as long as any liquidation candidate remains. This global switch was likely intended only for actual liquidation trades.

In `new_perp_order.rs` the code sets `margin_call = engine.is_long_margin_call() || engine.is_short_margin_call();`

```rust
    let margin_call = engine.is_long_margin_call() || engine.is_short_margin_call();
    if !margin_call {
        engine.state.header.perp_spot_price_for_withdrowal = engine.state.header.perp_underlying_px;
    }
```

That boolean is forwarded to `PerpEngine::match_{ask,bid}_orders` via `MatchOrdersStaticArgs`

```rust
        if engine.cross(price, OrderSide::Ask) {
            (remaining_qty, _, ref_payment) = engine.match_ask_orders(
                Some(&mut client_community_state),
                &MatchOrdersStaticArgs {
                    price,
                    qty: data.amount,
                    ref_discount,
                    ref_ratio: header.ref_program_ratio,
                    ref_expiration: header.ref_program_expiration,
                    ref_client_id: header.ref_client_id,
                    trades_limit: 0,
                    margin_call,
                    client_id: client_state.temp_client_id,
                },
            )?;
        }
```

Referral rebates are conditioned on `!args.margin_call in perp_engine.rs`: when `margin_call` is `true`, ref_payment is forced to zero.
```rust
        let ref_payment = if self.time < args.ref_expiration && !args.margin_call {
            ((fees - rebates) as f64 * args.ref_ratio) as i64
        } else {
            0
        };
```

Liquidation routines (`check_long_margin_call, check_short_margin_call`) also pass `margin_call: true` explicitly, but there is no distinction between liquidation-triggered fills and ordinary orders.
```rust
    if buy {
        if engine.check_short_margin_call()? < MAX_MARGIN_CALL_TRADES {
            engine.check_long_margin_call()?;
        }
    } else if engine.check_long_margin_call()? < MAX_MARGIN_CALL_TRADES {
        engine.check_short_margin_call()?;
    }
```

Therefore, the presence of any liquidation candidate globally blocks referral rewards for all traders, regardless of who is being liquidated.


**Impact:** Legitimate users lose their expected referral incentives whenever any other account is under liquidation. Although not an immediate loss of funds, it represents a systemic incentive failure affecting all participants during stressed periods.

**Recommended Mitigation:** Restrict the `margin_call` flag to trades that are actually part of liquidation flows.

**Deriverse:** Fixed in commit [bc9bd6](https://github.com/deriverse/protocol-v1/commit/bc9bd6ab49dd15dcf2c3d83559fa4ad0bd6777d9).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Deriverse Dex |
| Report Date | N/A |
| Finders | RajKumar, Ctrus, Alexzoid, JesJupyter |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

