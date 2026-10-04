---
# Core Classification
protocol: Wormhole Solana
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47209
audit_firm: OtterSec
contest_link: https://wormhole.com/
source_link: https://wormhole.com/
github_link: https://github.com/wormhole-foundation/example-liquidity-layer

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
finders_count: 2
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
---

## Vulnerability Title

Missing Endpoint Check

### Overview


The report states that there is a bug in the function "settle_auction_none_local" which fails to verify the endpoint information within the PreparedOrderResponse account. This means that the function does not check if the "to_endpoint" field in the account is set to "Local" before proceeding with settlement on the Solana chain. As a result, this may lead to the settlement process attempting to deliver orders from a remote chain on Solana instead of routing them to the target chain, resulting in lost or inaccessible funds for the intended recipient. The suggested solution is to verify the "to_endpoint" field before proceeding with settlement. This bug has been resolved in version #194.

### Original Finding Content

## Settle Auction None Local Failure

The `settle_auction_none_local` function fails to verify the endpoint information within the `PreparedOrderResponse` account. It does not check if the `to_endpoint` field in the `PreparedOrderResponse` account is set to `Local` before proceeding with settlement on the Solana chain. Consequently, this may result in the settlement process attempting to deliver orders from a remote chain on Solana instead of routing them to the target chain, resulting in lost or inaccessible funds for the legitimate recipient.

> _auction/settle/none/local.rs_

```rust
pub fn settle_auction_none_local(ctx: Context<SettleAuctionNoneLocal>) -> Result<()> {
    [...]
    let super::SettledNone {
        user_amount: amount,
        fill,
    } = super::settle_none_and_prepare_fill(
        super::SettleNoneAndPrepareFill {
            prepared_order_response: &mut ctx.accounts.prepared.order_response,
            prepared_custody_token,
            auction: &mut ctx.accounts.auction,
            fee_recipient_token: &ctx.accounts.fee_recipient_token,
            custodian,
            token_program,
        },
        ctx.bumps.auction,
    )?;
    [...]
}
```

## Remediation

The `settle_auction_none_local` function should verify that `order_response.to_endpoint` is `Local` before proceeding with the settlement.

## Patch

Resolved in #194.

© 2024 Otter Audits LLC. All Rights Reserved. 9/20

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Wormhole Solana |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen |

### Source Links

- **Source**: https://wormhole.com/
- **GitHub**: https://github.com/wormhole-foundation/example-liquidity-layer
- **Contest**: https://wormhole.com/

### Keywords for Search

`vulnerability`

