---
# Core Classification
protocol: Pyth Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48826
audit_firm: OtterSec
contest_link: https://pyth.network/
source_link: https://pyth.network/
github_link: https://github.com/pyth-network/governance.

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
  - Kevin Chow
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

TokenAccount Reload

### Overview

See description below for full details.

### Original Finding Content

## Withdraw Stake Function Risk Validation Issue

In the `withdraw_stake` function, risk validation is attempted after a transfer, but the custody token account needs to be reloaded to reflect its true balance.

## Code Snippet

```rust
src/lib.rs
transfer(
    CpiContext::from(&*ctx.accounts).with_signer(&[&[
        AUTHORITY_SEED.as_bytes(),
        ctx.accounts.stake_account_positions.key().as_ref(),
        &[stake_account_metadata.authority_bump],
    ]]),
    amount,
)?;
if utils::risk::validate(
    stake_account_positions,
    stake_account_custody.amount,
    unvested_balance,
    current_epoch,
    config.unlocking_duration,
).is_err() {
    Return
    Err(error!(ErrorCode::InsufficientWithdrawableBalance));
}
```

## Remediation

To make this validation functional, add a reload call after the transfer:

```rust
ctx.accounts.stake_account_custody.reload()?;
```

## Patch

Pyth Data Association acknowledges the finding and developed a patch for this issue: `#156`

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pyth Governance |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen, OtterSec |

### Source Links

- **Source**: https://pyth.network/
- **GitHub**: https://github.com/pyth-network/governance.
- **Contest**: https://pyth.network/

### Keywords for Search

`vulnerability`

