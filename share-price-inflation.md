---
# Core Classification
protocol: BlueFin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47477
audit_firm: OtterSec
contest_link: https://bluefin.io/
source_link: https://bluefin.io/
github_link: https://github.com/fireflyprotocol/elixir_bluefin_integration

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
finders_count: 2
finders:
  - Robert Chen
  - MichałBochnak
---

## Vulnerability Title

Share Price Inflation

### Overview


This bug report describes an issue in the withdraw_from_vault function where the share count is correctly reduced, but the corresponding adjustment to the vault_total_balance does not occur. This can result in temporary inflation of the share price and allow users to withdraw funds at a higher perceived share value. The report recommends adjusting the vault_total_balance to accurately reflect the reduction in shares and provides a patch for the issue. 

### Original Finding Content

## Vulnerability Report: `withdraw_from_vault` Function

In `withdraw_from_vault`, when a user withdraws funds, the share count (`vault.total_shares`) is appropriately reduced. However, a critical vulnerability arises as no corresponding adjustment occurs to `vault_total_balance`. Although `vault_total_balance` is calculated based on the current vault balance, it fails to account for the reduced shares resulting from the withdrawal. Consequently, the share price may experience temporary inflation, given that `vault_total_balance` remains unchanged despite the reduction in total shares.

> _sources/bluefin_vault.moverust_

```rust
entry fun withdraw_from_vault<USDC>(
    bluefin_perpetual: &BluefinPerpetual, 
    bluefin_bank: &BluefinBank<USDC>, 
    vault: &mut Vault<USDC>, 
    shares: u64, 
    ctx: &TxContext
) {
    [...]
    //
    // Calculate the USD amount to be given to the user based on the
    // shares he wants to cash in + the total shares in the vault
    // and the vault's current balance
    //
    // Get vault's total bank balance
    let vault_total_balance = vault_balance(vault.bank_account, bluefin_bank, bluefin_perpetual);
    [...]
}
```

The impact of this share price inflation on subsequent transactions lies in the utilization of the outdated `vault_total_balance` in calculations. This circumstance enables users to obtain more value for their shares than intended, resulting in inaccuracies in share conversions. The misalignment between the reduced share count and the unaltered `vault_total_balance` presents an opportunity for exploitation. Users may benefit from this situation by withdrawing funds at a higher perceived share value.

## Remediation

Adjust `vault_total_balance` when withdrawing shares. This adjustment should accurately reflect the reduction in shares and ensure the correct valuation of the remaining shares.

### Patch

Fixed in `05eb0d0`.

© 2024 Otter Audits LLC. All Rights Reserved. 13/18

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | BlueFin |
| Report Date | N/A |
| Finders | Robert Chen, MichałBochnak |

### Source Links

- **Source**: https://bluefin.io/
- **GitHub**: https://github.com/fireflyprotocol/elixir_bluefin_integration
- **Contest**: https://bluefin.io/

### Keywords for Search

`vulnerability`

