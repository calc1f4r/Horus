---
# Core Classification
protocol: Kamino Lend Integration
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46938
audit_firm: OtterSec
contest_link: https://www.exponent.finance/
source_link: https://www.exponent.finance/
github_link: https://github.com/exponent-finance/exponent-core

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Faulty Distribution of Emissions

### Overview


The bug is caused by a misalignment in how rewards are distributed to staked and unstaked SY tokens. The index used to track reward allocation is only based on staked tokens, but it is also used to calculate rewards for unstaked tokens owned by the treasury. This results in incorrect reward distribution. To fix this, the index should be calculated based on the total supply of SY tokens, not just the staked portion. The issue has been resolved in PR#570.

### Original Finding Content

## Reward Allocation Issue

The issue arises from a misalignment in how rewards (emissions) are allocated to staked SY tokens and the treasury’s share for unstaked SY tokens. In the Emission structure, the `index` field is utilized to track how much reward (emissions) each staked SY token holder is entitled to. It is updated based on new emissions that are credited to the system. 

Currently, the index is calculated only based on the staked SY tokens, but it is also utilized to calculate the rewards for unstaked SY tokens (which belong to the treasury). This is problematic because the total emissions should be distributed based on the total supply of SY tokens, not just the staked portion.

## Code Example

```rust
pub fn increase_from_token_credit(&mut self, sy_supply: u64, token_amount: u64) {
    let index_delta = Number::from_ratio(token_amount.into(), sy_supply.into());
    self.index += index_delta;
    self.last_seen_total_accrued_emissions += token_amount as u128;
}
```

This may result in the incorrect allocation of rewards to both staked SY token holders and the treasury.

## Remediation

Ensure the index is calculated as the reward amount for the entire `sy_mint` supply, and not just for the staked SY tokens.

## Patch

Resolved in PR#570.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Kamino Lend Integration |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.exponent.finance/
- **GitHub**: https://github.com/exponent-finance/exponent-core
- **Contest**: https://www.exponent.finance/

### Keywords for Search

`vulnerability`

