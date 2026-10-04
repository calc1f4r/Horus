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
solodit_id: 46957
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

Inconsistent Handling of Interest Rate Adjustments

### Overview


The report discusses a vulnerability in the way a system called "vault" handles interest adjustments during emergency scenarios. This vulnerability allows attackers to withdraw more SY (a type of currency) than they should be able to. The report suggests a solution to fix this vulnerability and states that it has been resolved in two patches.

### Original Finding Content

## Vulnerability Overview

The vulnerability concerns a flaw in the way Vault handles interest adjustments when the exchange rate fluctuates, specifically in emergency scenarios. When the exchange rate increases, the SY amount that was previously tied to PT (Principal Tokens) moves to an uncollected_sy pool. This is a mechanism to account for the fact that more SY is now required for the same amount of PT. In the opposite scenario, when the exchange rate decreases (negative interest case), there is protection to prevent interest amounts from being reduced.

While protections exist to prevent a decrease in the SY amount when the exchange rate falls, there are no corresponding checks to prevent the sy_for_pt amount from increasing.

## Code Snippet

> _ vault/stage_yield.rs rust

```rust
pub fn handle_stage_yt_yield(
    vault: &mut Vault,
    vault_yield_position: &mut YieldTokenPosition,
    user_yield_position: &mut YieldTokenPosition,
    sy_state: &SyState,
    now: u32,
) -> Result<()> {
    // update vault indexees from SY state
    // and stage any yield to the vault's robot account
    update_vault_yield(vault, vault_yield_position, now, sy_state);
    // TODO - consider removing this check, since deeper in the stack we check for this
    require!(
        !vault.is_in_emergency_mode(),
        ExponentCoreError::VaultInEmergencyMode
    );
    yield_position_earn(vault, user_yield_position, sy_state);
    // Set SY for PT
    vault.set_sy_for_pt();
    Ok(())
}
```

Normally, `update_vault_yield`, which manages these calculations, is not allowed to execute in emergency mode as shown above. Emergency mode is designed to prevent unauthorized or incorrect adjustments during critical conditions. However, in `withdraw_yt` and `merge`, the emergency status of the vault is not verified as in `update_vault_yield`. Consequently, an attacker may exploit this by withdrawing more `sy_amount` than they should be able to, based on the current state of the vault.

## Remediation

Ensure that `withdraw_yt` and `merge` verify the emergency status of the vault before proceeding with operations that affect SY amounts.

## Patch

Resolved in PR#536 and PR#548.

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

