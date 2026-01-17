---
# Core Classification
protocol: Genius Solana Program V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51981
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/shuttle-labs/genius-solana-program
source_link: https://www.halborn.com/audits/shuttle-labs/genius-solana-program
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Missing validation for src\_chain\_id and dest\_chain\_id in create\_order

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `create_order` function is responsible for creating a new order for a user to transfer tokens across different blockchains. It checks the deposit amount, verifies that the user has sufficient fees, and sets the details for the order, including the source and destination chains (`src_chain_id` and `dest_chain_id`). However, the function does not verify that the source and destination chains are distinct. As we can see in the snippet below, the values for `src_chain_id` and `dest_chain_id` are directly assigned from the function parameters without any validation:

```
    pub fn process_instruction(
        ctx: Context<Self>,
        amount: u64,
        seed: [u8; 32],
        trader: [u8; 32],
        receiver: [u8; 32],
        src_chain_id: u32,
        dest_chain_id: u32,
        token_in: [u8; 32],
        fee: u64,
        min_amount_out: u64,
        token_out: [u8; 32],
    ) -> Result<()> {
        msg!("deposit USDC amount: {:?}", amount);
        let price_update = &mut ctx.accounts.price_update;
        let feed_id: [u8; 32] = get_feed_id_from_hex(FEED_ID)?;
        let price = price_update.get_price_no_older_than(&Clock::get()?, MAXIMUM_AGE, &feed_id)?;

        // Adjust price to floating-point by scaling with 10^exponent
        let adjusted_price: f64 = (price.price as f64) * 10f64.powi(price.exponent);

        require!(adjusted_price > 0.99, GeniusError::StableCoinPriceTooLow);

        if ctx.accounts.order.status != OrderStatus::Unexistant {
            return err!(GeniusError::OrderAlreadyExists);
        }

        let min_fee = ctx.accounts.target_chain_min_fee.min_fee;
        if min_fee > fee {
            return err!(GeniusError::InsufficientFees);
        }

        ctx.accounts.order.amount_in = amount;
        ctx.accounts.order.seed = seed;
        ctx.accounts.order.trader = trader;
        ctx.accounts.order.receiver = receiver;
        ctx.accounts.order.src_chain_id = src_chain_id;
        ctx.accounts.order.dest_chain_id = dest_chain_id;
        ctx.accounts.order.token_in = token_in;
        ctx.accounts.order.fee = fee;
        ctx.accounts.order.status = OrderStatus::Created;
        ctx.accounts.order.min_amount_out = min_amount_out;
        ctx.accounts.order.token_out = token_out;

        ctx.accounts.asset.unclaimed_fees += fee;

        let signer = &ctx.accounts.signer;
        let orchestrator = &ctx.accounts.orchestrator;
        let orchestrator_state = &ctx.accounts.orchestrator_state;

        // Convert signer key and orchestrator key to [u8; 32] for comparison
        let signer_key_bytes: [u8; 32] = signer.key().to_bytes();
        let orchestrator_key_bytes: [u8; 32] = orchestrator.key().to_bytes();
        require!(
            signer_key_bytes == trader || signer_key_bytes == orchestrator_key_bytes,
            GeniusError::UnauthorizedSigner
        );
        require!(
            orchestrator_state.authorized == true,
            GeniusError::IllegalOrchestrator
        );

        // Transfer USDC from orchestrator to vault
        token_transfer_user(
            ctx.accounts.ata_signer.to_account_info().clone(),
            ctx.accounts.signer.to_account_info().clone(),
            ctx.accounts.ata_vault.to_account_info().clone(),
            ctx.accounts.token_program.to_account_info().clone(),
            amount,
        )
    }
```

  

Without checking that the source and destination chains are different, the user may end up paying fees for a transaction that is essentially redundant, leading to unnecessary costs. This could be especially problematic in a system where chain-to-chain transfers are intended, and users may mistakenly believe their funds are being transferred across chains when they are not.

##### BVSS

[AO:S/AC:L/AX:L/R:F/S:U/C:N/A:N/I:N/D:N/Y:N (0.0)](/bvss?q=AO:S/AC:L/AX:L/R:F/S:U/C:N/A:N/I:N/D:N/Y:N)

##### Recommendation

Consider adding a validation step that checks whether the `src_chain_id` and `dest_chain_id` are distinct. If they are the same, the function should reject the transaction or notify the user about the issue.

##### Remediation

**SOLVED:** The **Genius team** solved the issue by adding a check to validate that both chains are different.

##### Remediation Hash

<https://github.com/Shuttle-Labs/genius-contracts-solana/commit/aa405a61f21126150294b17e7f18c9d626cf3b76>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Genius Solana Program V2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/shuttle-labs/genius-solana-program
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/shuttle-labs/genius-solana-program

### Keywords for Search

`vulnerability`

