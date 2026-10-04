---
# Core Classification
protocol: Exceed Finance Liquid Staking & Early Purchase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58764
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
source_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
github_link: none

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
  - István Böhm
  - Mustafa Hasan
  - Darren Jensen
---

## Vulnerability Title

Incorrect Authority Used for Token Transfer Prevents All Redemptions

### Overview


The client has marked a bug as "Fixed" in a recent update. The issue was found in the `early_purchase::redeem_receipt::handler()` function, which is responsible for transferring tokens during sale receipt redemption. However, the `token::transfer` CPI is incorrectly configured with the buyer as the authority for the transfer. The recommendation is to modify the CPI to use the sale's PDA as the authority instead. This bug has been addressed in the update `c3a83a530d0eddb65b0b7a780d02b474e56c4881` and unit tests have been updated to ensure the accuracy of the distributed tokens. The affected file is `programs/early-purchase/src/instructions/redeem_receipt.rs`.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `c3a83a530d0eddb65b0b7a780d02b474e56c4881`. The client provided the following explanation:

> The Sale struct was modified to store its ID and bump so that signer seeds could be constructed in the redeem_receipt instruction. Unit tests were updated to prove that the tokens are transferred and that the distributed amount is accurate.

**File(s) affected:**`programs/early-purchase/src/instructions/redeem_receipt.rs`

**Description:** The`early_purchase::redeem_receipt::handler()`function is responsible for transferring the `purchase_mint`tokens from the sale's ATA (`config_purchase_ata`) to the buyer's ATA (`buyer_purchase_ata`) during sale receipt redemption. However, the `token::transfer` CPI is incorrectly configured with the`buyer`as the authority for this transfer:

```
token::transfer(
    CpiContext::new(
        purchase_program.to_account_info(),
        token::Transfer {
            from: config_purchase_ata.to_account_info(),
            to: buyer_purchase_ata.to_account_info(),
            authority: buyer.to_account_info(),
        },
    ),
    num_tokens_pending,
)
```

**Recommendation:** Consider modifying the`token::transfer`CPI to use the`sale.to_account_info()`PDA as the authority for the transfer.

```
token::transfer(
    CpiContext::new(
        purchase_program.to_account_info(),
        token::Transfer {
            from: config_purchase_ata.to_account_info(),
            to: buyer_purchase_ata.to_account_info(),
            authority: sale.to_account_info(),
        },
    ),
    num_tokens_pending,
)
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Exceed Finance Liquid Staking & Early Purchase |
| Report Date | N/A |
| Finders | István Böhm, Mustafa Hasan, Darren Jensen |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html

### Keywords for Search

`vulnerability`

