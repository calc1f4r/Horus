---
# Core Classification
protocol: LayerZero V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47233
audit_firm: OtterSec
contest_link: https://layerzero.network/
source_link: https://layerzero.network/
github_link: https://github.com/LayerZero-Labs/monorepo

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
  - Robert Chen
  - Jessica Clendinen
---

## Vulnerability Title

Charging Fee For Native Operations

### Overview


The quote::get_pre_fee_amount_ld function is used to calculate the pre-fee amount needed to obtain a specified post-fee amount, taking into account any transfer fees set up in the TransferFeeConfig extension. However, it does not differentiate between different types of OFT operations, such as adapter-based transactions and native operations like minting and burning. This means that transfer fees are applied universally, without considering the specific context of the operation. For example, in the case of native operations like minting and burning, applying transfer fees is not appropriate as these operations are internal to the token's lifecycle and should not be subject to the same fees as external transfers. To fix this issue, the functionality needs to be refactored to properly distinguish between adapter-based and native operations. The bug has been fixed in version 4aff686. 

### Original Finding Content

## Pre-Fee Amount Calculation

The `quote::get_pre_fee_amount_ld` function calculates the pre-fee amount needed to obtain a specified post-fee amount, taking into account any transfer fees set up in the `TransferFeeConfig` extension. However, this function does not differentiate between various types of OFT operations, such as adapter-based transactions and native operations like minting and burning.

> _of t/src/instructions/quote.rs_

```rust
pub fn get_pre_fee_amount_ld(
    token_mint: &InterfaceAccount<anchor_spl::token_interface::Mint>,
    amount_ld: u64,
) -> Result<u64> {
    let token_mint_info = token_mint.to_account_info();
    let token_mint_data = token_mint_info.try_borrow_data()?;
    let token_mint_unpacked = StateWithExtensions::<Mint>::unpack(&token_mint_data)?;

    Ok(if let Ok(transfer_fee) = token_mint_unpacked.get_extension::<TransferFeeConfig>() {
        transfer_fee
            .get_epoch_fee(Clock::get()?.epoch)
            .calculate_pre_fee_amount(amount_ld)
            .ok_or(ProgramError::InvalidArgument)?
    } else {
        amount_ld
    })
}
```

However, it applies the transfer fee calculation universally, without accounting for the specific context of the operation. For instance, in the case of native operations such as minting and burning, applying transfer fees is not appropriate. These operations are internal to the token’s lifecycle and should not be subject to the same transfer fees that external transfers incur.

## Remediation

Refactor the functionality to properly distinguish between adapter-based and native operations.

## Patch

Fixed in `4aff686`.

© 2024 Otter Audits LLC. All Rights Reserved. 7/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | LayerZero V2 |
| Report Date | N/A |
| Finders | Robert Chen, Jessica Clendinen |

### Source Links

- **Source**: https://layerzero.network/
- **GitHub**: https://github.com/LayerZero-Labs/monorepo
- **Contest**: https://layerzero.network/

### Keywords for Search

`vulnerability`

