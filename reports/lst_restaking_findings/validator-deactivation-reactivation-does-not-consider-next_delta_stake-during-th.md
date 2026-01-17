---
# Core Classification
protocol: Monad
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62909
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Monad-Spearbit-Security-Review-September-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Monad-Spearbit-Security-Review-September-2025.pdf
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
finders_count: 4
finders:
  - Haxatron
  - Dtheo
  - Guido Vranken
  - Rikard Hjort
---

## Vulnerability Title

Validator deactivation / reactivation does not consider next_delta_stake during the boundary pe-

### Overview

See description below for full details.

### Original Finding Content

## Risk Assessment

**Severity:** Low Risk

**Context:** No context files were provided by the reviewer.

## Description

Issue found in commit hash `4cbb1742cd31ee30a0d2c6edb698400d9d70f9d8`. When the validator's auth address next epoch stake falls below the `MIN_VALIDATE_STAKE`, the validator is deactivated in delegate:

```cpp
if (val.auth_address() == address &&
    (val.get_flags() & ValidatorFlagWithdrawn) &&
    del.get_next_epoch_stake() >= MIN_VALIDATE_STAKE) {
    val.clear_flag(ValidatorFlagWithdrawn);
    emit_validator_status_changed_event(val_id, val.get_flags());
}
```

When the validator's auth address is deactivated but its next epoch stake is increased in `precompile_undelegate`, the validator is then reactivated again:

```cpp
if (msg_sender == val.auth_address() &&
    del.get_next_epoch_stake() < MIN_VALIDATE_STAKE) {
    val.set_flag(ValidatorFlagWithdrawn);
    emit_validator_status_changed_event(val_id, val.get_flags());
}
```

The next epoch stake is defined to be the sum of the current stake and delta stake:

```cpp
uint256_t DelInfo::get_next_epoch_stake() const noexcept {
    return stake().load().native() + delta_stake().load().native();
}
```

In both cases, the next epoch stake is checked whether it is more than or equal to the `MIN_VALIDATE_STAKE`. However, this calculation does not include the fact that next delta stake can be promoted when an epoch progresses, which occurs when delegating during the boundary block. 

**Example:**

If `MIN_VALIDATE_STAKE` is 100 and we have the following validator:

- `stake = 100`
- `delta_stake = 0`
- `next_delta_stake = 100`

If the validator undelegates:

- `stake = 100` becomes `stake = 0`
- `delta_stake = 0` becomes `delta_stake = 0`
- `next_delta_stake = 100` remains `next_delta_stake = 100`

Then the next epoch stake will be 0, and this validator will be marked with `ValidatorFlagWithdrawn`. However, this does not include the fact that `next_delta_stake` will eventually be promoted, and the auth address next epoch stake will reach `MIN_VALIDATE_STAKE` again. Since validator deactivation and reactivation only occurs during delegate or `precompile_undelegate`, the flag will incorrectly persist until the auth address calls either of the two precompile functions.

## Recommendation

`get_next_epoch_stake` should be changed to:

`stake().load().native() + delta_stake().load().native() + next_delta_stake().load().native()`

### Proof:

- **Case 1:** Suppose we are not in a boundary period. Since `touch_delegator` is called before `get_next_epoch_stake`, that means `next_delta_stake = 0` as `next_delta_stake` must have been promoted and cannot have been set in a non-boundary period. Therefore, `get_next_epoch_stake` is functionally equivalent in a non-boundary period.

- **Case 2:** Suppose we are in a boundary period. As the snapshot of the current epoch has already been taken at the start of the boundary period, changing `get_next_epoch_stake` to `stake().load().native() + delta_stake().load().native() + next_delta_stake().load().native()` will ensure delegating during the boundary period is equivalent to delegating in a non-boundary period in the next epoch before the next epoch snapshot. As with the `delta_stake` and `next_delta_stake` promotion, `get_next_epoch_stake` will be equal for the current epoch and the next epoch.

Therefore, the recommended change fixes the issue.

**Category:** Labs  
**Fixed in commit:** 5aacb95d  
**Spearbit:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Monad |
| Report Date | N/A |
| Finders | Haxatron, Dtheo, Guido Vranken, Rikard Hjort |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Monad-Spearbit-Security-Review-September-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Monad-Spearbit-Security-Review-September-2025.pdf

### Keywords for Search

`vulnerability`

