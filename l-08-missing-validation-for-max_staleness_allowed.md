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
solodit_id: 63276
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

[L-08] Missing validation for `max_staleness_allowed`

### Overview

See description below for full details.

### Original Finding Content



The `max_staleness_allowed` variable is assigned a value but is not considered in the price validation logic from the oracle account. This oversight allows the system to use outdated price data without any constraints, potentially leading to inaccurate token valuations.  

The issue originates in the `initialize_global_state_ix` function:  

```rust
pub fn initialize_global_state_ix(
    ctx: Context<InitializeGlobalState>,
    start_time: i64,
    end_time: i64,
    tokens_for_sale: u64,
) -> Result<()> {
    ...
    
    oracle_account.max_staleness_allowed = u64::MAX;
    ...
}
```  

Furthermore, the function `get_token_value_usd` retrieves token prices using `get_token_price`, but there is no check to ensure the retrieved price is within the allowed staleness threshold:  

```rust
pub fn get_token_value_usd(&self, mint: Pubkey, amount: u128, decimals: u8) -> Result<u64> {
    let price = self.get_token_price(mint)? as u128;
    let value_in_u128 = price
        .checked_mul(amount)
        .ok_or_else(|| SaleError::MathOverflow)?
        .checked_div(10u128.pow(decimals as u32))
        .ok_or_else(|| SaleError::MathOverflow)?;
    let value_in_u64: u64 = value_in_u128
        .try_into()
        .map_err(|_| SaleError::MathOverflow)?;
    Ok(value_in_u64)
}
```  

Without validating `max_staleness_allowed`, the contract risks using outdated or manipulated prices, which could lead to incorrect token valuations and unfair trading conditions.  

Recommendations:  

Implement a `max_staleness_allowed` check in the price validation logic to ensure that token prices remain up to date. This check should be enforced when retrieving the token price in `get_token_price`. Example:  

```rust
pub fn get_token_price(&self, mint: Pubkey) -> Result<u64> {
    if self.last_update_timestamp + self.max_staleness_allowed < Clock::get()?.unix_timestamp {
        return Err(SaleError::StalePriceData.into());
    }

    if mint == constants::DEPOSIT_MINT1 || mint == constants::DEPOSIT_MINT2 {
        return Ok(100_000);
    } else if mint == constants::DEPOSIT_MINT3 && mint == self.mint {
        return Ok(self.price);
    } else {
        return Err(SaleError::UnsupportedMint);
    }
}
```





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

