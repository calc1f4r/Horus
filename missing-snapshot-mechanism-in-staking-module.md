---
# Core Classification
protocol: Merkle Token
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47103
audit_firm: OtterSec
contest_link: https://www.tauruslabs.xyz/
source_link: https://www.tauruslabs.xyz/
github_link: https://github.com/tauruslabs/merkle-contract

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
finders_count: 2
finders:
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Missing Snapshot Mechanism In Staking Module

### Overview


This bug report highlights an issue in the staking process where the absence of a snapshot mechanism can lead to problems with voting power and the integrity of past voting records. When users unlock their tokens, their voting power is removed without being recorded, causing discrepancies in previous votes and governance actions. Additionally, an increase in lock amount without updating the duration can result in an immediate boost in voting power, which may retroactively apply to previous epochs. The report suggests implementing a snapshot mechanism to preserve historical data and maintain the integrity of past voting records. This issue has been fixed in the latest version by keeping track of rewards from old epochs instead of calculating them based on active tokens.

### Original Finding Content

## Staking Voting Power Integrity Issues

In staking, where voting power is derived from locked tokens, the absence of a snapshot mechanism to record past voting powers may result in critical issues affecting the integrity of voting processes. When a user unlocks their tokens via unlock, their voting power is effectively removed. Without a snapshot mechanism to preserve historical voting power, this removal retroactively impacts past voting records, invalidating previous votes or governance actions that depended on the user’s voting power.

```rust
// staking.move rust
public fun unlock(_user: &signer, _vemkl_address: address) 
    acquires VoteEscrowedMKL, UserVoteEscrowedMKL, StakingEvents {
    let vemkl_object = object::address_to_object<VoteEscrowedMKL>(_vemkl_address);
    assert!(address_of(_user) == object::owner(vemkl_object), E_NOT_AUTHORIZED);
    let vemkl = move_from<VoteEscrowedMKL>(_vemkl_address);
    assert!(timestamp::now_seconds() >= vemkl.unlock_time, E_UNABLE_UNLOCK);
    [...]
}
```

The function `increase_lock_amount_and_duration` allows users to add more tokens to their lock and potentially extend the lock duration. However, if the duration is not updated, only the amount is increased, resulting in an immediate boost in voting power. This increase may retroactively apply to previous epochs, causing discrepancies. Additionally, when a user updates the lock duration, `increase_lock_amount_and_duration` sets a new lock time. Thus, the user loses their voting power for past epochs.

```rust
// staking.move rust
public fun increase_lock_amount_and_duration(_user: &signer, _vemkl_address: address, _fa: FungibleAsset, _unlock_time: u64) 
    acquires VoteEscrowedMKLConfig, VoteEscrowedMKL, VoteEscrowedPowers, StakingEvents {
    [...]
    if (_unlock_time > 0) {
        [...]
        assert!(vemkl.unlock_time <= _unlock_time, E_INVALID_LOCK_DURATION);
        vemkl.lock_time = new_lock_time;
        vemkl.unlock_time = _unlock_time;
    };
    [...]
}
```

## Remediation

Implement a snapshot mechanism in staking to preserve the historical data to maintain the integrity of past voting records.

## Patch

Fixed in `906ec95` by keeping track of rewards from old epochs instead of calculating them based on the active veMKL tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Merkle Token |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://www.tauruslabs.xyz/
- **GitHub**: https://github.com/tauruslabs/merkle-contract
- **Contest**: https://www.tauruslabs.xyz/

### Keywords for Search

`vulnerability`

