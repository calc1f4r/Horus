---
# Core Classification
protocol: Convergent
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47157
audit_firm: OtterSec
contest_link: https://convergent.so/
source_link: https://convergent.so/
github_link: https://github.com/Convergent-Finance/v1-contracts

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
finders_count: 2
finders:
  - Kevin Chow
  - Robert Chen
---

## Vulnerability Title

Incorrect Burn Amount

### Overview


The bug report describes an issue with the implementation of a function called "move_token_from_redeem" within the "redeem_collateral" code. The function is supposed to burn tokens for gas compensation, but the amount of tokens burned is determined by a variable called "pool_state.gas_compensation" instead of the intended variable "total_usv_gas_to_burn". This can result in the incorrect amount of tokens being burned. The suggested solution is to adjust the code to use "total_usv_gas_to_burn" directly. The bug was fixed in a patch with the code version "34b1a5a". 

### Original Finding Content

## Token Burn Process in `move_token_from_redeem`

In `move_token_from_redeem` within `redeem_collateral`, tokens are burned from `gas_compensation` if `total_usv_gas_to_burn` is greater than zero. However, the actual amount burned is determined by `pool_state.gas_compensation` rather than `total_usv_gas_to_burn`. The issue with this implementation is that it may not burn the correct amount of tokens as specified by `total_usv_gas_to_burn`. For proper redemption, the exact amount of `total_usv_gas_to_burn` should be burned.

> _trove-manager/src/instructions/redeem_collateral.rs_

```rust
fn move_token_from_redeem(
    ctx: Context<RedeemCollateral>,
    redemption_totals: &RedemptionTotals,
) -> Result<()> {
    [...]
    if redemption_totals.total_usv_gas_to_burn > 0 {
        burn(
            ctx.accounts
                .burn_stablecoin_from_gas_compensation_ctx()
                .with_signer(&[&authority_seed[..]]),
            pool_state.gas_compensation,
        )?;
    }
    [...]
}
```

## Remediation

Adjust the burn operation to utilize the `total_usv_gas_to_burn` amount directly.

## Patch

Resolved in 34b1a5a.

© 2024 Otter Audits LLC. All Rights Reserved. 14/19

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Convergent |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen |

### Source Links

- **Source**: https://convergent.so/
- **GitHub**: https://github.com/Convergent-Finance/v1-contracts
- **Contest**: https://convergent.so/

### Keywords for Search

`vulnerability`

