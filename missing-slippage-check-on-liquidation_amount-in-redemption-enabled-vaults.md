---
# Core Classification
protocol: Securitize Solana Vault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64261
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md
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
  - Alex Roan
  - Al-Qa-Qa
  - Giovanni Di Siena
  - Farouk
---

## Vulnerability Title

Missing Slippage Check on `liquidation_amount` in Redemption-Enabled Vaults

### Overview


This bug report discusses an issue with the `liquidate_handler()` function, specifically with the `min_output_amount` argument. The check for this argument is only implemented for assets and not for the type of Vault, which results in incorrect slippage for liquidators. This means that the liquidator may receive less than the minimum amount they specified. The recommended mitigation is to move the liquidation check to the `else` block for Vaults that do not support Redemption and to add another check for the `liquidation_amount` for Vaults that do support Redemption. The issue has been acknowledged by the developers and the slippage documentation has been clarified.

### Original Finding Content

**Description:** When calling `liquidate_handler()` the liquidator provide the minimum amount of assets he is willing to receive. either assets or liquidation tokens

```rust
/// ## Arguments
...
/// - `min_output_amount`: An optional minimum output amount to ensure sufficient assets or liquidation tokens are received.
```

The slippage check is implemented only for assets before checking the type of the Vault weather it support Redemption or not.

```rust
>>  if let Some(min_output_amount) = min_output_amount {
        require_gt!(
            assets,
            min_output_amount,
            ScVaultError::InsufficientOutputAmount
        );
    }

    ...

    if let Some(ref redemption_program) = ctx.accounts.redemption_program {
        ...
        // Transfer received liquidation tokens to liquidator.
        transfer_from!(
            liquidation_token_vault,                                  // from
            liquidator_liquidation_ata,                        // to
            ctx.accounts.vault_authority,                             // authority
            ctx.accounts.liquidation_token_program.as_ref().unwrap(), // token_program
            liquidation_token_mint,                                   // mint
>>          liquidation_amount,                                       // amount
            liquidation_token_mint.decimals,                          // decimals
            vault_authority_signer                                    // signer
        );
    } else {
        ...
    }
```

As we can see the amount the liquidator receives in case of Redemption is not `assets` value calculated. it is `liquidation_amount` received after redeeming.

This wil result in incorrect slippage, as the liquidator will provide the minimum amount he is willing to receive from `liquidate token`, but the check will be made for `asset` instead.

**Impact:**
- Liquidator receives less than he wants

**Proof of Concept:**
- liquidator made the `min_output_amount` as `1000`
- firing `liquidate_handler`
- assets value is `1100` after calculations
- slippage passed
- firing `redemption_program::redeem()`
- liquidation_amount is `900`
- liquidator receives `900` token, although he mentioned he only accepts `1000` or more

**Recommended Mitigation:**
- Move the liquidation check and transfer it to the `else` block (the Vault that is not supporting Redemption)
- Make another liquidation check aganist `liquidation_amount` for Vaults supporting redemption

**Securitize:** Acknowledged, it’s acceptable from our side since it matches the behavior in the EVM version and we don’t intend to change it. However, the slippage documentation has been clarified in [56c8f9e](https://github.com/securitize-io/bc-solana-vault-sc/commit/56c8f9e8ac6420196ec2df3dddd5a8ee3a7e6965).

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Solana Vault |
| Report Date | N/A |
| Finders | Alex Roan, Al-Qa-Qa, Giovanni Di Siena, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-23-cyfrin-securitize-solana-vault-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

