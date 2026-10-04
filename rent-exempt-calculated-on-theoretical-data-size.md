---
# Core Classification
protocol: Solana Stake Pool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48374
audit_firm: OtterSec
contest_link: https://solana.com/
source_link: https://solana.com/
github_link: https://github.com/solana-labs/solana-program-library/tree/master/stake-pool

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
finders_count: 3
finders:
  - Harrison Green
  - OtterSec
  - Filippo Barsanti
---

## Vulnerability Title

Rent-Exempt Calculated On Theoretical Data Size

### Overview

See description below for full details.

### Original Finding Content

## Rent-Exempt Calculations in Stake Program

Ensure rent-exempt calculations are performed on actual data size instead of theoretical data size. For example, in `AddValidatorToPool`, the rent-exempt calculation on the `reserve_pool` is performed on the default account size:

```rust
let space = std::mem::size_of::<stake::state::StakeState>();
let stake_minimum_delegation = stake::tools::get_minimum_delegation()?;
let required_lamports = minimum_delegation(stake_minimum_delegation)
    .saturating_add(rent.minimum_balance(space));
```

If it was possible to create a Stake account larger than the default (200 bytes), this computation would be inaccurate and the stake account may be able to be closed here.

**Note:** The stake program validates the account size during initialization, and during a split, the remaining lamports must be either greater than the minimum requirement or zero.

## Remediation

Calculate minimum rent on the actual size of the account.

## Patch

Fixed in #4000. The minimum rent is now calculated based on the same value used to allocate the account space, instead of always using the theoretical size.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Solana Stake Pool |
| Report Date | N/A |
| Finders | Harrison Green, OtterSec, Filippo Barsanti |

### Source Links

- **Source**: https://solana.com/
- **GitHub**: https://github.com/solana-labs/solana-program-library/tree/master/stake-pool
- **Contest**: https://solana.com/

### Keywords for Search

`vulnerability`

