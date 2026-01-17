---
# Core Classification
protocol: Claynosaurz
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54952
audit_firm: OtterSec
contest_link: https://claynosaurz.com/
source_link: https://claynosaurz.com/
github_link: https://github.com/Claynosaurz-Inc/staking-smart-contract

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
finders_count: 4
finders:
  - Kevin Chow
  - Robert Chen
  - Gabriel Ottoboni
  - Xiang Yin
---

## Vulnerability Title

Possibility of Underflow Due to Misconfiguration

### Overview

See description below for full details.

### Original Finding Content

## NFT Multiplier Update Issues

The `create_class` and `modify_class` functions do not correctly guarantee that an NFT’s multiplier is properly updated. The admin can supply an incorrect `token_mint_record`, which results in skipping the necessary updates to the class metadata. 

In `staking_actions::unstake`, the `current_multiplier` is adjusted based on the `class_pda`. If an incorrect `token_mint_record` is utilized by the admin when calling `create_class` or `modify_class`, and the multiplier is not properly applied, it may result in an underflow issue in `unstake` if the multiplier is not updated, as `staking_account.current_multiplier` may be less than `class.multiplier`.

> _claynosaurz-staking/src/instructions/staking_action.rs rust_

```rust
/// Unstakes an NFT by revoking the delegation and unlocking the NFT.
pub fn unstake(ctx: Context<StakingAction>) -> Result<()> {
    // Update staking data
    let staking_account = &mut ctx.accounts.staking_account;
    [...]
    // Adjust multiplier based on class PDA ownership (default to 1 if no class PDA)
    if let Ok(class) = Class::try_deserialize(&mut 
        &ctx.accounts.class_pda.to_account_info().data.borrow_mut()[..]) {
        staking_account.current_multiplier = staking_account.current_multiplier
            .checked_sub(class.multiplier)
            .ok_or(StakingError::Overflow)?;
    }
    [...]
}
```

As a result, the function will attempt to subtract a larger multiplier than what was originally assigned, resulting in an underflow and triggering the `StakingError::Overflow` error. Consequently, users will be unable to unstake their tokens.

## Remediation

Ensure that `create_class` and `modify_class` perform strict validation on `token_mint_record` before modifying multipliers.

## Patch

Fixed in `0b87d6e`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Claynosaurz |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen, Gabriel Ottoboni, Xiang Yin |

### Source Links

- **Source**: https://claynosaurz.com/
- **GitHub**: https://github.com/Claynosaurz-Inc/staking-smart-contract
- **Contest**: https://claynosaurz.com/

### Keywords for Search

`vulnerability`

