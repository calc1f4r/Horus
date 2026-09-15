---
# Core Classification
protocol: Marginfi Integration
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46934
audit_firm: OtterSec
contest_link: https://www.exponent.finance/
source_link: https://www.exponent.finance/
github_link: https://github.com/exponent-finance/exponent-core

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Discrepancy in Conversion of Synthetic Yield Tokens

### Overview


This bug report discusses a potential issue with the RedeemSy instruction in the Marginfi Integration Audit 04. It explains that there may be a discrepancy in the conversion of synthetic yield (SY) tokens to their corresponding base asset amounts due to changes in the share-to-asset conversion rate. This can result in the incorrect calculation of the base asset value when redeeming SY tokens. The report suggests a solution to ensure that the burning of SY tokens and redemption of base assets occur simultaneously to prevent this issue. The bug has been resolved in PR#569.

### Original Finding Content

## Discrepancy in Synthetic Yield Token Redemption

In the RedeemSy instruction, there is a potential discrepancy in the conversion of synthetic yield (SY) tokens (shares) to their corresponding base asset amounts. This discrepancy arises due to the way the share-to-asset conversion rate may change after the SY tokens are burned but before the base assets are redeemed. When a user initiates the RedeemSy instruction, the first step is to burn the specified amount of SY tokens (`amount`). Between the time the SY tokens are burned and the base assets are redeemed through the FakeRewards program, the asset share value may be updated.

```rust
>_ fake_rewards_sy/src/instructions/redeem_sy.rs
pub fn handler(ctx: Context<RedeemSy>, amount: u64) -> Result<()> {
    let bump = ctx.bumps.authority;
    
    // Burn SY tokens
    token_2022::burn(
        CpiContext::new(
            ctx.accounts.token_2022_program.to_account_info(),
            anchor_spl::token_2022::Burn {
                mint: ctx.accounts.mint_sy.to_account_info(),
                from: ctx.accounts.sy_account.to_account_info(),
                authority: ctx.accounts.owner.to_account_info(),
            },
        ),
        amount,
    )?;
    
    // Redeem shares from FakeRewards and transfer the base asset
    let seeds: [&[u8]; 2] = [crate::GLOBAL_AUTH_SEED, &[bump]];
    [...]
}
```

As a result, the calculation utilized to determine the number of base assets corresponding to the burned SY tokens (shares) may no longer be accurate, as the base amount to be redeemed is calculated via the asset share value at the time the SY tokens are burned. If this value changes before the redemption is complete, the resulting base amount will not accurately reflect the user’s intended redemption value. Consequently, the invariant check that ensures that the total supply of SY tokens (`mint_sy.supply`) and the corresponding base assets remain in balance will fail.

## Remediation

Ensure that the burning of SY tokens and the redemption of base assets occur atomically within a single transaction, minimizing the window during which the asset share value may change.

## Patch

Resolved in PR#569.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Marginfi Integration |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.exponent.finance/
- **GitHub**: https://github.com/exponent-finance/exponent-core
- **Contest**: https://www.exponent.finance/

### Keywords for Search

`vulnerability`

