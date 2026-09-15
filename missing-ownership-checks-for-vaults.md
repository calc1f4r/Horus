---
# Core Classification
protocol: Serum v4
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48841
audit_firm: OtterSec
contest_link: https://portal.projectserum.com/
source_link: https://portal.projectserum.com/
github_link: Repos in notes

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
  - William Wang
---

## Vulnerability Title

Missing ownership checks for vaults

### Overview


This report discusses a bug found in the Serum v4 Audit 12/41 program. The bug is located in the create_market.rs file, specifically on lines 88-89. The bug is related to the ownership of certain accounts, specifically the market and orderbook accounts. The report suggests that additional checks should be included for the base_vault and quote_vault accounts. The bug has been fixed in patch #51. The report is copyrighted by OtterSec LLC.

### Original Finding Content

## Dex V4 Program Processor

## File: `create_market.rs`

### Line: 88-89
```rust
check_account_owner(a.market, program_id, DexError::InvalidStateAccountOwner)?;
check_account_owner(a.orderbook, program_id, DexError::InvalidStateAccountOwner)?;
```

### Additional Checks
Additional checks for `base_vault` and `quote_vault` accounts should be included here.
```rust
check_account_owner(a.base_vault, &spl_token::ID, DexError::InvalidBaseVaultAccount)?;
check_account_owner(a.quote_vault, &spl_token::ID, DexError::InvalidQuoteVaultAccount)?;
```

### Patch
Fixed in #51.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Serum v4 |
| Report Date | N/A |
| Finders | Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://portal.projectserum.com/
- **GitHub**: Repos in notes
- **Contest**: https://portal.projectserum.com/

### Keywords for Search

`vulnerability`

