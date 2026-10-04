---
# Core Classification
protocol: Securitize Solana Redemption
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64311
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md
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
  - Naman
  - Giovanni Di Siena
  - Farouk
---

## Vulnerability Title

DoS in initialize via pre-created ATA for `off_ramp_authority`

### Overview


This bug report discusses an issue with the `initialize` instruction in a program called `off_ramp_authority`. This instruction creates a liquidity vault, which is a type of account used to store tokens. The problem is that this instruction can be used by anyone, without the owner's permission, to create the vault. This means that an attacker can create the vault before the owner does, causing the transaction to fail. This can be repeated multiple times, causing a denial of service. The recommended solution is to switch to a different instruction called `init_if_needed`, which prevents this type of attack. This bug has been fixed by the developers at Securitize and verified by Cyfrin.

### Original Finding Content

**Description:** The `initialize` instruction creates the liquidity vault as an **associated token account** for the program PDA `off_ramp_authority`:
```rust
#[account(
    init,
    payer = admin,
    associated_token::mint = liquidity_token_mint,
    associated_token::authority = off_ramp_authority,
    associated_token::token_program = liquidity_token_program,
)]
pub liquidity_token_vault: Box<InterfaceAccount<'info, TokenAccount>>;
```
Associated token accounts are globally derivable and can be created by **anyone** for any owner without the owner’s signature. Because both `off_ramp_state` and `off_ramp_authority` PDAs are deterministically derived from public seeds (counter and state key), an attacker can precompute the vault ATA and create it first. When `initialize` later runs with `init`, Anchor will fail with “already in use,” reverting the whole transaction.

**Impact:** Hard denial of service on program initialization for a given `(off_ramp_state, liquidity_token_mint)`. An attacker can repeatedly grief by precreating the ATA for each anticipated off_ramp ID, blocking deployment unless the admin changes parameters. This is cheap for the attacker and can be repeated.

**Recommended Mitigation:** Switch to `init_if_needed` to make initialization idempotent and immune to precreation:
```rust
#[account(
    init_if_needed,
    payer = admin,
    associated_token::mint = liquidity_token_mint,
    associated_token::authority = off_ramp_authority,
    associated_token::token_program = liquidity_token_program,
)]
pub liquidity_token_vault: Box<InterfaceAccount<'info, TokenAccount>>;
```
This accepts a pre-existing correct ATA and proceeds.


**Securitize:** Fixed in [1a8a098](https://github.com/securitize-io/bc-solana-redemption-sc/commit/1a8a0989c940eb8978ff3556bfc513ee0606f6dc).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Solana Redemption |
| Report Date | N/A |
| Finders | Alex Roan, Naman, Giovanni Di Siena, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

