---
# Core Classification
protocol: Pump_2025-03-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63277
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Pump-security-review_2025-03-18.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-09] Hardcoded stablecoin price

### Overview

See description below for full details.

### Original Finding Content


In `states.rs` the function `get_token_price` assumes the prices of stablecoins to be always 1 USD.
```rust
pub fn get_token_price(&self, mint: Pubkey) -> Result<u64> {
    if mint == constants::DEPOSIT_MINT1 || mint == constants::DEPOSIT_MINT2 {
        return Ok(100000);
    } else if mint == constants::DEPOSIT_MINT3 && mint == self.mint {
        return Ok(self.price);
    } else {
        return err!(SaleError::UnsupportedMint);
    }
}
```

This hardcoded price will lead to issues at depegging events. For example, if the stable depegs to 0.95, the users can still contribute the stable coin and get assigned tokens of value equal to 1 USD instead of 0.95 USD.

Recommendations:

Consider adding an oracle price for stablecoins as well.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Pump_2025-03-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Pump-security-review_2025-03-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

