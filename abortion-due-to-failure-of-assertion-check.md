---
# Core Classification
protocol: Solend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46872
audit_firm: OtterSec
contest_link: https://save.finance/
source_link: https://save.finance/
github_link: https://github.com/solendprotocol/liquid-staking

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
finders_count: 2
finders:
  - Michał Bochnak
  - Robert Chen
---

## Vulnerability Title

Abortion Due to Failure of Assertion Check

### Overview

See description below for full details.

### Original Finding Content

## Liquid Staking Mint Assertion

The assertion in mint within `liquid_staking`, while intended to maintain the balance between Liquid Staking Tokens (LST) and SUI, may abort under certain conditions.

```rust
contracts/sources/liquid_staking.move

public fun mint<P: drop>(
    self: &mut LiquidStakingInfo<P>,
    system_state: &mut SuiSystemState,
    sui: Coin<SUI>,
    ctx: &mut TxContext
) -> Coin<P> {
    [...]
    // invariant: lst_out / sui_in <= old_lst_supply / old_sui_supply
    // -> lst_out * old_sui_supply <= sui_in * old_lst_supply
    assert!(
        (lst.value() as u128) * old_sui_supply <= (sui_balance.value() as u128) *
        old_lst_supply, EMintInvariantViolated
    );
    [...]
}
```

If `old_lst_supply == 0` and `old_sui_supply > 0`, the assertion will always fail. In this case, the conversion of the provided SUI amount to LST utilizing `sui_amount_to_lst_amount` will return the `sui_amount` itself.

## Remediation

Ensure to handle the above-specified case to prevent the failure of the assertion checks.

## Patch

Resolved in commit `f8b8b00`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Solend |
| Report Date | N/A |
| Finders | Michał Bochnak, Robert Chen |

### Source Links

- **Source**: https://save.finance/
- **GitHub**: https://github.com/solendprotocol/liquid-staking
- **Contest**: https://save.finance/

### Keywords for Search

`vulnerability`

