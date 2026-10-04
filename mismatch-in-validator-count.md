---
# Core Classification
protocol: Jito Steward
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47099
audit_firm: OtterSec
contest_link: https://www.jito.network/
source_link: https://www.jito.network/
github_link: https://github.com/jito-foundation/stakenet

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
  - Kevin Chow
  - Robert Chen
---

## Vulnerability Title

Mismatch in Validator Count

### Overview

See description below for full details.

### Original Finding Content

## Analysis of `steward_state::compute_score`

In `steward_state::compute_score`, `num_pool_validators` is updated positively only once at the beginning of a cycle. During this update, it reflects the current number of validators in the pool. This adjustment ensures that new validators added to the pool at the start of the cycle are properly counted.

> _File: `steward/src/state/steward_state.rs` (Rust)_
```rust
pub fn compute_score(
    [...]
) -> Result<Option<ScoreComponents>> {
    if matches!(self.state_tag, StewardStateEnum::ComputeScores) {
        [...]
        if self.progress.is_empty()
            || current_epoch > self.current_epoch
            || slots_since_scoring_started > config.parameters.compute_score_slot_range
        {
            [...]
            self.num_pool_validators = num_pool_validators;
            self.validators_added = 0;
        }
        [...]
    }
    [...]
}
```

If a validator is added and then removed within the same cycle, the `num_pool_validators` gets decremented when the validator is removed, but this happens in `epoch_maintenance` during the next epoch. The decrement is done via `remove_validator`. However, `num_pool_validators` remains one lower than it should be after the validator removal because `compute_score` does not update `num_pool_validators` again until the next compute cycle starts (in the following epoch).

> _File: `steward/src/instructions/epoch_maintenance.rs` (Rust)_
```rust
pub fn handler([...]) -> Result<()> {
    [...]
    {
        [...]
        if let Some(validator_index_to_remove) = validator_index_to_remove {
            state_account.state.remove_validator(validator_index_to_remove)?;
        }
    }
    [...]
}
```

In `delegation::decrease_stake_calculation` (which adjusts stake distribution based on yield scores), it utilizes `num_pool_validators` to determine the range of validators that are eligible for rebalancing. Because `num_pool_validators` is one lower than it should be, the final validator may be excluded from the rebalancing process.

## Remediation
Ensure that `validators_added` is decremented properly.

## Patch
Resolved in `0275585`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Jito Steward |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen |

### Source Links

- **Source**: https://www.jito.network/
- **GitHub**: https://github.com/jito-foundation/stakenet
- **Contest**: https://www.jito.network/

### Keywords for Search

`vulnerability`

