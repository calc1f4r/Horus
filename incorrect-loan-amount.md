---
# Core Classification
protocol: Hedge Vault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48835
audit_firm: OtterSec
contest_link: https://www.hedge.so/
source_link: https://www.hedge.so/
github_link: https://github.com/Hedge-Finance/hedge-vault/.

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
  - Mohan Pedhapati
  - OtterSec
---

## Vulnerability Title

Incorrect Loan Amount

### Overview


The report states that there is a bug in the calculation of denormalized loans in a program called Hedge Vault. This bug allows attackers to create small amounts of USH tokens without increasing their liabilities. The bug only affects collaterals with a non-zero interest rate. The code snippets provided show that the division in the first block produces a decimal, which is then rounded down in the second block. This allows the attacker to repeatedly take out small loans without increasing the vault's debt. The report recommends rounding up the denormalized amount to fix the bug. The patch for this bug has been fixed in the latest update of the program.

### Original Finding Content

## Small Loans Denormalization Issue

Small loans are not properly rounded while calculating the denormalized loan using the `denormalize` function. This allows an attacker to mint small quantities of USH tokens for free without increasing their liabilities.  

It is important to note that this issue only affects collaterals with a non-zero interest rate. The following snippets show the affected code. The division in the first block `[0]` produces a decimal if the cumulative rate is greater than the amount, which gets rounded down in the second block `[1]`.

## Affected Code Snippets

### 1. `denormalize` Function

**File:** `programs/hedge-vault/src/account_data/vault_type.rs`

```rust
pub fn denormalize(&self, amount: u64) -> Result<Decimal> {
    let cumulative_rate = Decimal::from_account(self.cumulative_rate);
    let denormalized_amount = Decimal::from_u64(amount).unwrap() / cumulative_rate; // [0]
    Ok(denormalized_amount)
}
```

### 2. Loan Processing

**File:** `programs/hedge-vault/src/processors/loan_vault.rs`

```rust
let denormalized_loan_amount = vault_type_account
    .denormalize(normalized_loan_amount)?
    .to_u64() // [1]
    .unwrap();

[...]
vault_account.denormalized_debt += denormalized_loan_amount;
```

## Proof of Concept

The impact of the rounding bugs depends on whether it can be repeatedly triggered. The loan can be taken as long as the vault is not under-collateralized. 

Our proof of concept repeatedly takes out very small loans without increasing the vault’s debt. In our case, the loan amount is "1," so that the `denormalized_loan_amount` gets rounded down to zero.

The following is the output of the script, which iteratively takes a loan one hundred times with a loan amount of "1". As we can see, the debt of the vault stays the same, but the balance of the token account increases by `0.000000001 * 100`.

```bash
$ anchor test tests/os-hdg-adv-01.ts
Before Balance: 100
Before Vault denormalizedDebt: 99983418542
Looping times: 100
After Balance: 100.0000001
After Vault denormalizedDebt: 99983418542
```

## Remediation

It is recommended to round up the `denormalized_amount`.

## Patch

Round up the denormalized amount. Fixed in #95.

```rust
let denormalized_loan_amount = vault_type_account
    .denormalize(normalized_loan_amount)?
    .ceil()
    .to_u64()
    .unwrap();
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Hedge Vault |
| Report Date | N/A |
| Finders | Robert Chen, Mohan Pedhapati, OtterSec |

### Source Links

- **Source**: https://www.hedge.so/
- **GitHub**: https://github.com/Hedge-Finance/hedge-vault/.
- **Contest**: https://www.hedge.so/

### Keywords for Search

`vulnerability`

