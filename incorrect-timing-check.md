---
# Core Classification
protocol: Adrena
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46799
audit_firm: OtterSec
contest_link: https://www.adrena.xyz/
source_link: https://www.adrena.xyz/
github_link: https://github.com/AdrenaDEX/adrena

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
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Incorrect Timing Check

### Overview


The current implementation of the function "has_ended" in the code is causing a bug where the stake is not considered ended even when the current time is equal to the end time. This is because the function is using the "<" operator instead of the "<=" operator. This bug is preventing the stake from being automatically finalized. To fix this, the code needs to be changed to use the "<=" operator. This issue has been resolved in a recent patch.

### Original Finding Content

## Audit Report: Vulnerabilities

## Current Implementation of `has_ended`

In the current implementation of `has_ended`, the stake is considered ended only if the current time is strictly greater than the end time (`stake_time + lock_duration`). `finalize_locked_stake` is designed to finalize a stake automatically once its locking period has ended. This process is managed by Sablier’s worker, which triggers the finalization at the exact end time stamp (`stake_time + lock_duration`).

```rust
> _state/user_staking.rs
pub fn has_ended(&self, current_time: i64) -> bool {
    (self.stake_time + self.lock_duration as i64) < current_time
}
```

If the worker calls `finalize_locked_stake` exactly at the end time, `current_time` will be equal to `stake_time + lock_duration`. Given the current implementation of `has_ended`, the condition:

```rust
(self.stake_time + self.lock_duration as i64) < current_time
```

will evaluate to false because the times are equal. This implies `has_ended` will return false, indicating that the staking period has not ended yet, even though it technically has.

```rust
> _public/staking/p/finalize_locked_stake.rs
pub fn finalize_locked_stake<'info>(
    ctx: Context<'_, '_, '_, 'info, FinalizeLockedStake<'info>>,
    params: &FinalizeLockedStakeParams,
) -> Result<()> {
    [...]
    // Preliminary checks
    {
        [...]
        require!(
            params.early_exit || locked_stake.has_ended(current_time),
            AdrenaError::InvalidStakeState
        );
        require!(!locked_stake.is_resolved(), AdrenaError::InvalidStakeState);
    }
    [...]
}
```

`finalize_locked_stake` checks whether the stake has ended via `has_ended`. Thus, if `has_ended` returns false, the function will return an error, preventing the stake from being finalized automatically.

---

## Remediation

In `has_ended`, utilize `<=` instead of `<`. This change ensures that the function correctly identifies the stake as ended when the current time is exactly equal to the end time. The same applies to the `finalize_genesis_lock` instruction invocation and `genesis_lock::has_campaign_ended` check.

**Patch**  
Resolved in `9efc589`.

---

© 2024 Otter Audits LLC. All Rights Reserved. 30/59

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Adrena |
| Report Date | N/A |
| Finders | Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://www.adrena.xyz/
- **GitHub**: https://github.com/AdrenaDEX/adrena
- **Contest**: https://www.adrena.xyz/

### Keywords for Search

`vulnerability`

