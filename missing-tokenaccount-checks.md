---
# Core Classification
protocol: Magna Airlock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48723
audit_firm: OtterSec
contest_link: https://www.magna.so/
source_link: https://www.magna.so/
github_link: https://github.com/magna-eng/airlock-sol-ottersec

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
  - Robert Chen
  - OtterSec
  - Rajvardhan Agarwal
---

## Vulnerability Title

Missing TokenAccount Checks

### Overview


The program has a bug in the withdraw instruction where it does not check if the beneficiary_ata is an associated token account. This means that anyone can create a TokenAccount and withdraw funds into it, potentially allowing an attacker to steal funds. While the funds can be recovered, it may be difficult for less technically skilled users. The code that is affected can be found in the file "programs/piecewise/lib.rs" and the fix is to enforce the beneficiary_ata field to be an associated token account. This has been addressed in a commit with the code "b1d8522". 

### Original Finding Content

## Vulnerability in Withdraw Instruction

In the withdraw instruction, the program does not enforce `beneficiary_ata` to be an associated token account. The Solana token program allows any user to create a `TokenAccount` with an arbitrary owner and mint. This could allow an attacker to withdraw funds into attacker-created `TokenAccounts`. 

While these funds can be recovered by the owner of the `TokenAccount` by tracking the transactions on-chain, this could potentially be difficult for technically unskilled users.

## Affected Code

The affected code can be found in the following code snippet:

```rust
#[account(mut,
token::mint = schedule.token_mint,
token::authority = schedule.beneficiary,
)]
beneficiary_ata: Box<Account<'info, token::TokenAccount>>,
```

## Remediation

The program must enforce the `beneficiary_ata` field to be an associated token account. For more information, please refer to the code snippet below:

```rust
#[account(
init_if_needed,
payer = signer,
associated_token::mint = token_mint,
associated_token::authority = beneficiary,
)]
beneficiary_ata: Box<Account<'info, token::TokenAccount>>,
```

## Patch

The `beneficiary_ata` account is now enforced to be an ATA. Fixed in commit `b1d8522`.

© 2022 OtterSec LLC. All Rights Reserved. 7 / 19

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Magna Airlock |
| Report Date | N/A |
| Finders | Robert Chen, OtterSec, Rajvardhan Agarwal |

### Source Links

- **Source**: https://www.magna.so/
- **GitHub**: https://github.com/magna-eng/airlock-sol-ottersec
- **Contest**: https://www.magna.so/

### Keywords for Search

`vulnerability`

