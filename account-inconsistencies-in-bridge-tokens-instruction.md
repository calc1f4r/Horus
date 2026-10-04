---
# Core Classification
protocol: Composable Bridge + PR
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47042
audit_firm: OtterSec
contest_link: https://www.composablefoundation.com/
source_link: https://www.composablefoundation.com/
github_link: https://github.com/ComposableFi/bridge-contract

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
finders_count: 3
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Account Inconsistencies In Bridge Tokens Instruction

### Overview


The report highlights a bug in the bridge_tokens instruction, where the token_mint is not being verified as the correct mint address associated with the receipt token at the time of deposit. This allows users to transfer tokens from any escrow account instead of just the intended one. Additionally, the staker account is not marked as a Signer, which is required for token transfers in Solana-IBC. The report suggests storing the restake_receipt_token_mint in Deposit and validating the token_mint against it, as well as declaring the staker account as a Signer and modifying the initialization of user_receipt_escrow_account so that the staker is set as the authority instead of the fee_payer. The issue has been resolved in the latest patch.

### Original Finding Content

## Bridge Tokens Instruction Review

In the `bridge_tokens` instruction, the `token_mint` is utilized to determine the type of token being transferred. However, the current implementation does not verify if `token_mint` is the correct mint address associated with the receipt token at the time of deposit. This lack of validation allows users to potentially transfer tokens from any escrow account, not just the intended one.

> _instructions/bridgetokens.rs rust

```rust
pub fn bridge_tokens<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, BridgeTokens<'info>>,
    deposit_index: u8,
) -> Result<()> {
    [...]
    let hashed_full_denom = 
    lib::hash::CryptoHash::digest(ctx.accounts.token_mint.key().to_string().as_ref());
    let denom = ibc::apps::transfer::types::PrefixedDenom::from_str(
        &ctx.accounts.token_mint.key().to_string(),
    )
    .unwrap();
    let token = ibc::apps::transfer::types::Coin {
        denom,
        amount: deposit.amount.into(),
    };
    [...]
}
```

Additionally, the `staker` account in the `BridgeTokens` instruction is not explicitly marked as a `Signer`. Solana-IBC requires that the staker account must be a `Signer` to authorize the transfer of tokens. If the staker is not a `Signer`, the transaction will not be validated correctly. Furthermore, `user_receipt_escrow_account` is initialized with the `fee_payer` as its authority. However, it is more appropriate for the staker to be designated as the authority for this account.

## Remediation

Store the `restake_receipt_token_mint` in `Deposit` and validate the `token_mint` against it. This ensures that each deposit record has a reference to the correct token mint that should be utilized. Also, declare the staker account as a `Signer` and modify the initialization of `user_receipt_escrow_account` so that the staker is set as the authority rather than the `fee_payer`.

## Patch

Resolved in `337399d`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Composable Bridge + PR |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.composablefoundation.com/
- **GitHub**: https://github.com/ComposableFi/bridge-contract
- **Contest**: https://www.composablefoundation.com/

### Keywords for Search

`vulnerability`

