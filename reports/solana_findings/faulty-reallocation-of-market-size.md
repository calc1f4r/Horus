---
# Core Classification
protocol: Exponent Core
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46959
audit_firm: OtterSec
contest_link: https://www.exponent.finance/
source_link: https://www.exponent.finance/
github_link: https://github.com/exponent-finance/exponent-core

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
finders_count: 3
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Faulty Reallocation of Market Size

### Overview


This bug report discusses a vulnerability in a program that handles Cross-Program Invocation (CPI) accounts. The issue occurs when reallocating the MarketTwo account in the AddMarketEmission instruction. The problem is that the program uses the wrong CPI accounts for the reallocation, which can lead to incorrect size calculations and insufficient space for new data. The report suggests fixing this issue by updating the reallocation process to accurately reflect the size requirements based on the input CPI accounts. The bug has been resolved in PR#529.

### Original Finding Content

## Vulnerability Analysis

The vulnerability concerns the incorrect handling of CPI (Cross-Program Invocation) accounts during the reallocation of the MarketTwo account in the `AddMarketEmission` instruction. Specifically, the issue is that the `market.cpi_accounts` are utilized for reallocation instead of the `cpi_accounts` provided as input to the handler function.

```rust
> _ market_two/admin/add_market_emission.rs
pub fn update_market(&mut self, cpi_accounts: CpiAccounts) {
    self.market.cpi_accounts = cpi_accounts;
}
```

This implies that when the account is resized, it relies on the existing `cpi_accounts` in the market account. Ideally, the realloc should be based on the `cpi_accounts` passed in through the handler function input, not on the current state of the market account. If the `market.cpi_accounts` are outdated or incorrect, reallocating the account based on this data may result in an incorrect size calculation. Thus, there will be insufficient space for the new `MarketEmission` data.

## Remediation

Ensure that the realloc operation accurately reflects the size requirements based on the input `cpi_accounts` provided in the handler function.

## Patch

Resolved in PR#529.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Exponent Core |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.exponent.finance/
- **GitHub**: https://github.com/exponent-finance/exponent-core
- **Contest**: https://www.exponent.finance/

### Keywords for Search

`vulnerability`

