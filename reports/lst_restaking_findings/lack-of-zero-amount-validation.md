---
# Core Classification
protocol: Restaking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52118
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/solayer/restaking
source_link: https://www.halborn.com/audits/solayer/restaking
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

Lack of Zero Amount validation

### Overview

See description below for full details.

### Original Finding Content

##### Description

The program in-scope does not prevent the `restake` and `unrestake` methods from being called with `amount == 0`.

  

`- programs/restaking-program/src/contexts/restaking.rs`

```
    pub fn restake(ctx: Context<Restaking>, amount: u64) -> Result<()> {
        // Check if solayer_signer has signed the restake transaction
        // since we will impose TVLs caps at different epochs
        /*let solayer_signer: &UncheckedAccount<'_> = &ctx.accounts.solayer_signer;
        if !solayer_signer.is_signer {
            return Err(ProgramError::MissingRequiredSignature.into());
        }*/

        ctx.accounts.thaw_rst_account()?;
        ctx.accounts.stake(amount)?;
        ctx.accounts.mint_rst(amount)?;
        // Check if RST mints should be frozen
        if !is_liquid_rst_mints(&ctx.accounts.rst_mint.key()) {
            ctx.accounts.freeze_rst_account()?;
        }
        Ok(())
    }

    pub fn unrestake(ctx: Context<Restaking>, amount: u64) -> Result<()> {
        ctx.accounts.thaw_rst_account()?;
        ctx.accounts.unstake(amount)?;
        ctx.accounts.burn_rst(amount)?;
        // Check if RST mints should be frozen
        if !is_liquid_rst_mints(&ctx.accounts.rst_mint.key()) {
            ctx.accounts.freeze_rst_account()?;
        }
        Ok(())
    }
```

  

The entry-point functions in `lib.rs` does not handle this verification either. While this condition does not lead to immediate financial loss, it should be checked to keep overall consistency.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

Consider adding a verification before the execution of the `restake` and `unrestake` methods, blocking operations with `amount == 0`.

  

### Remediation Plan

**ACKNOWLEDGED:** The **Solayer team** acknowledged this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Restaking |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/solayer/restaking
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/solayer/restaking

### Keywords for Search

`vulnerability`

