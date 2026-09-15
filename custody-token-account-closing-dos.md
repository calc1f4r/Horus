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
solodit_id: 47207
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

Custody Token Account Closing DoS

### Overview


The report highlights a potential vulnerability in the settlement instructions for auctions involving the Wormhole CCTP bridge. The code assumes that the total transferable amount equals the order amount retrieved from the fastVAA. However, during the settlement process, it does not verify if this amount actually matches the funds in the prepared_custody_token account. This can lead to a failure in closing the account due to non-zero funds. The recommended solution is to use the actual token balance in the prepared_custody_token account instead of relying solely on the order amount. This issue has been resolved in the patch 307cc28.

### Original Finding Content

## Vulnerability Report: Wormhole CCTP Bridge

There is a potential vulnerability related to the settlement instructions for auctions involving the Wormhole CCTP bridge. The code assumes the total transferable amount equals `order.amount_in` retrieved from the `fastVAA`. However, during the settlement process, it does not verify if this amount actually matches the funds in the `prepared_custody_token` account.

## Code Reference

```rust
> _ auction/prepare_settlement/cctp.rsrust
fn handle_prepare_order_response_cctp(
    ctx: Context<PrepareOrderResponseCctp>,
    args: CctpMessageArgs,
) -> Result<()> {
    [...]
    let fast_vaa = ctx.accounts.fast_order_path.fast_vaa.load_unchecked();
    let order = LiquidityLayerMessage::try_from(fast_vaa.payload())
        .unwrap()
        .to_fast_market_order_unchecked();
    let amount_in = order.amount_in();
    ctx.accounts
        .prepared_order_response
        .set_inner(PreparedOrderResponse {
            bump: ctx.bumps.prepared_order_response,
            info: PreparedOrderResponseInfo {
                [...]
                amount_in,
                sender: order.sender(),
                redeemer: order.redeemer(),
                init_auction_fee: order.init_auction_fee(),
            },
            to_endpoint: ctx.accounts.fast_order_path.to_endpoint.info,
            redeemer_message: order.message_to_vec(),
        });
    [...]
}
```

Before settling the `PrepareOrderResponse`, if a small amount of tokens is transferred to the `prepared_custody_token` account, when the settlement instruction tries to close the `prepared_custody_token` account via `token::close_account`, it fails with non-zero funds because only the `order.amount_in` is transferred from that account instead of the total balance.

---

© 2024 Otter Audits LLC. All Rights Reserved. 6/20

## Wormhole Solana Audit 04 — Vulnerabilities

### Remediation

Instead of relying solely on `order.amount_in` from the fast VAA, the code should use the actual token balance in the `prepared_custody_token` account before attempting to close it.

### Patch

Resolved in 307cc28.

---

© 2024 Otter Audits LLC. All Rights Reserved. 7/20

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

