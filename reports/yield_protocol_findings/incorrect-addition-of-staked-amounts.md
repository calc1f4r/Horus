---
# Core Classification
protocol: Hubble Farms
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47762
audit_firm: OtterSec
contest_link: https://app.kamino.finance/
source_link: https://app.kamino.finance/
github_link: https://github.com/hubbleprotocol/farms

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
finders_count: 4
finders:
  - Akash Gurugunti
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Incorrect Addition Of Staked Amounts

### Overview


The report discusses a bug in a farming protocol where users experience a waiting period before their staked tokens become active and start earning rewards. The bug is caused by a function called update_user_rewards_tally_on_stake_increase, which adds a user's earned rewards to their rewards tally for each reward token. This function is called whenever there is an increase in the user's stake, whether it is an active stake or a pending stake that is still in the warm-up period. As a result, pending stakes are prematurely added to the rewards tally, leading to double rewards when the pending stakes become active. The recommended fix is to limit the usage of the function to only actively staked amounts. This bug has been fixed in a recent patch.

### Original Finding Content

## Stake Functionality in Farming Protocol

Stake is essential for users to enter the farming protocol and begin staking tokens. If there is no pending deposit period (i.e., `deposit_warmup_period` is zero), the function directly adds the staked tokens to the user’s active stake. However, if there is a pending deposit period, users experience a waiting period before their staked tokens become active and start earning rewards.

## Code Implementation

The function `update_user_rewards_tally_on_stake_increase` in the stake process adds a user’s earned rewards to their rewards tally for each reward token. Below is the relevant Rust code from `farm_operations.rs`:

```rust
pub fn stake(
    farm_state: &mut FarmState,
    user_state: &mut UserState,
    amount: u64,
    current_ts: u64,
) -> Result<StakeEffects> {
    [...]
    let stake_gained = if farm_state.deposit_warmup_period > 0 {
        // If there is a pending stake period, we add the stake to the pending
        user_state.pending_deposit_stake_ts = current_ts
            .checked_add(farm_state.deposit_warmup_period.into())
            .ok_or_else(|| dbg_msg!(FarmError::IntegerOverflow))?;
        let stake_gained = stake_ops::add_pending_deposit_stake(user_state, farm_state, amount)?;
        [...]
        stake_gained
    }
    [...]
    update_user_rewards_tally_on_stake_increase(farm_state, user_state, stake_gained)?;
}
```

## Problematic Behavior

The issue arises because `update_user_rewards_tally_on_stake_increase` is called whenever there is an increase in the user’s stake, whether it is an active stake or a pending stake that is still in the warm-up period. Thus, the function prematurely adds pending stakes to the rewards tally by calling `update_user_rewards_tally_on_stake_increase` for increases in both active and pending stakes.

This results in pending stakes being added to the rewards tally before they have officially become active and start earning rewards, which is problematic as `update_user_rewards_tally_on_stake_increase` is called again when the pending stakes turn active, effectively doubling the user's rewards tally for the same token.

## Hubble Farms Audit 04 | Vulnerabilities

### Remediation

Limit the utilization of `update_user_rewards_tally_on_stake_increase` solely to actively staked amounts.

### Patch

Fixed in commit `9949c09` by using `update_user_rewards_tally_on_stake_increase` on only actively staked amounts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Hubble Farms |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://app.kamino.finance/
- **GitHub**: https://github.com/hubbleprotocol/farms
- **Contest**: https://app.kamino.finance/

### Keywords for Search

`vulnerability`

