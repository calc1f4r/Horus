---
# Core Classification
protocol: Pump Science
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49582
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-01-pump-science
source_link: https://code4rena.com/reports/2025-01-pump-science
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
finders_count: 0
finders:
---

## Vulnerability Title

[03] Lack of Maximum Input Amount Validation in Swap Function Could Lead to Unnecessary Transaction Failures

### Overview

See description below for full details.

### Original Finding Content


The Pump Science protocol’s swap functionality, implemented in the `Swap` instruction, validates the minimum input amount but lacks validation for maximum input amounts. In the `validate()` function, we only see:
```

require!(exact_in_amount > &0, ContractError::MinSwap);
```

While there is a check for minimum input, there’s no upper bound validation. This could lead to unnecessary transaction failures in two scenarios:

1. For token purchases (base\_in = false):

   * If user inputs amount > bonding curve’s `real_sol_reserves`
   * Transaction will fail later in `apply_buy()` but gas is already consumed
2. For token sales (base\_in = true):

   * If user inputs amount > their token balance
   * Transaction will fail at token transfer but gas is already consumed

The issue is especially relevant because the bonding curve’s available liquidity changes over time, and users might not be aware of the current limits when submitting transactions.

### Impact

Users may experience unnecessary transaction failures and gas wastage when submitting swap transactions with amounts that exceed available liquidity or their balance.

### Recommendation

Add maximum amount validations in the `validate()` function:
```

pub fn validate(&self, params: &SwapParams) -> Result<()> {
    // ... existing validations ...

    if params.base_in {
        require!(
            params.exact_in_amount <= self.user_token_account.amount,
            ContractError::InsufficientBalance
        );
    } else {
        require!(
            params.exact_in_amount <= self.bonding_curve.real_sol_reserves,
            ContractError::InsufficientLiquidity
        );
    }

    Ok(())
}
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Pump Science |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2025-01-pump-science
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2025-01-pump-science

### Keywords for Search

`vulnerability`

