---
# Core Classification
protocol: Pump Science
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49575
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-01-pump-science
source_link: https://code4rena.com/reports/2025-01-pump-science
github_link: https://code4rena.com/audits/2025-01-pump-science/submissions/F-3

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
  - shaflow2
  - Spearmint
---

## Vulnerability Title

[H-01] The `lock_pool` operation can be DoS

### Overview


The bug report states that there is a problem with the `lock_pool` operation in the `pump-science` program. The issue is that a malicious actor could create the required `lockEscrow` account before the `create_lock_escrow` transaction is executed, causing the transaction to fail and resulting in a Denial of Service (DoS) for the `lock_pool` operation. This is because the creation of the `lock_escrow` account does not require the owner's signature and can be derived using the `pool` and `owner` as seeds. 

To mitigate this issue, the report recommends checking if the `lock_escrow` account already exists before attempting to create it during the `lock_pool` process. This will prevent the DoS attack from occurring. The team behind the `pump-science` program has confirmed the existence of this bug. 

### Original Finding Content



<https://github.com/code-423n4/2025-01-pump-science/blob/768ef58478724bf6b464c9f0952e3e5a3b2a2613/programs/pump-science/src/instructions/migration/lock_pool.rs# L149>

The `lock_pool` operation requires the creation of a `lockEscrow` account. However, a malicious actor could preemptively create the `lockEscrow` account, causing the `create_lock_escrow` transaction to fail and resulting in a Denial of Service (DoS) for the `lock_pool` operation.

### Proof of Concept

During the `lock_pool` process, the `create_lock_escrow` function is called to create the `lock_escrow` account.
```

    // Create Lock Escrow
    let escrow_accounts = vec![
        AccountMeta::new(ctx.accounts.pool.key(), false),
        AccountMeta::new(ctx.accounts.lock_escrow.key(), false),
        AccountMeta::new_readonly(ctx.accounts.fee_receiver.key(), false),
        AccountMeta::new_readonly(ctx.accounts.lp_mint.key(), false),
        AccountMeta::new(ctx.accounts.bonding_curve_sol_escrow.key(), true), // Bonding Curve Sol Escrow is the payer/signer
        AccountMeta::new_readonly(ctx.accounts.system_program.key(), false),
    ];

    let escrow_instruction = Instruction {
        program_id: meteora_program_id,
        accounts: escrow_accounts,
        data: get_function_hash("global", "create_lock_escrow").into(),
    };

    invoke_signed(
        &escrow_instruction,
        &[
            ctx.accounts.pool.to_account_info(),
            ctx.accounts.lock_escrow.to_account_info(),
            ctx.accounts.fee_receiver.to_account_info(),
            ctx.accounts.lp_mint.to_account_info(),
            ctx.accounts.bonding_curve_sol_escrow.to_account_info(), // Bonding Curve Sol Escrow is the payer/signer
            ctx.accounts.system_program.to_account_info(),
        ],
        bonding_curve_sol_escrow_signer_seeds,
    )?;
```

However, the `lock_escrow` account is derived using the `pool` and `owner` as seeds, and its creation does not require the owner’s signature. This means that a malicious actor could preemptively create the `lock_escrow` account to perform a DoS attack on the `lock_pool` operation.
```

/// Accounts for create lock account instruction
#[derive(Accounts)]
pub struct CreateLockEscrow<'info> {
    /// CHECK:
    pub pool: UncheckedAccount<'info>,

    /// CHECK: Lock account
    #[account(
        init,
        seeds = [
            "lock_escrow".as_ref(),
            pool.key().as_ref(),
            owner.key().as_ref(),
        ],
        space = 8 + std::mem::size_of::<LockEscrow>(),
        bump,
        payer = payer,
    )]
    pub lock_escrow: UncheckedAccount<'info>,

    /// CHECK: Owner account
@>  pub owner: UncheckedAccount<'info>,

    /// CHECK: LP token mint of the pool
    pub lp_mint: UncheckedAccount<'info>,

    /// CHECK: Payer account
    #[account(mut)]
    pub payer: Signer<'info>,

    /// CHECK: System program.
    pub system_program: UncheckedAccount<'info>,
}
```

### Recommended mitigation steps

In the `lock_pool` process, check if the `lock_escrow` exists. If it exists, skip the creation process.

**Kulture (Pump Science) confirmed**

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Pump Science |
| Report Date | N/A |
| Finders | shaflow2, Spearmint |

### Source Links

- **Source**: https://code4rena.com/reports/2025-01-pump-science
- **GitHub**: https://code4rena.com/audits/2025-01-pump-science/submissions/F-3
- **Contest**: https://code4rena.com/reports/2025-01-pump-science

### Keywords for Search

`vulnerability`

