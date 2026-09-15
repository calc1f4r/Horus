---
# Core Classification
protocol: Brokkr Protocol P1 Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50439
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/brokkr/brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/brokkr/brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-assessment
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

BBRO TOKENS ARE LOST WHEN UNSTAKING OR CLAIMING REWARDS

### Overview


The bug report describes an issue with the staking-v1 contract where a user's information is completely removed from the STAKERS item when they try to unstake or claim BRO rewards. This happens when their total staked amount is zero and their pending BRO reward is also zero. This means that the user will not be able to claim their BRO rewards, even if they have some amount, and will lose all their bBRO tokens. The code responsible for this issue can be found in the contracts/staking-v1/src/commands.rs file. The impact of this bug is rated 3 out of 5 and the likelihood is 5 out of 5. The bug has been fixed in commit f9bbc72a85ff872b36691c4992d7a86439a4bba2.

### Original Finding Content

##### Description

When a user `unstake` or `claim BRO rewards` in **staking-v1** contract, his information is totally removed from `STAKERS` item if the following conditions are true:

* Total staked amount is zero
* Pending BRO reward is zero

Under the mentioned circumstances, the user won't be able to claim his bBRO rewards, even if the amount is greater than zero, i.e.: he totally loses all his bBRO tokens.

Code Location
-------------

User's information is totally removed from `STAKERS` item when he unstakes:

#### contracts/staking-v1/src/commands.rs

```
// decrease stake amount
state.total_stake_amount = state.total_stake_amount.checked_sub(amount)?;
staker_info.unlocked_stake_amount = staker_info.unlocked_stake_amount.checked_sub(amount)?;

if staker_info.pending_bro_reward.is_zero() && staker_info.total_staked()?.is_zero() {
    remove_staker_info(deps.storage, &sender_addr_raw);
} else {
    store_staker_info(deps.storage, &sender_addr_raw, &staker_info)?;
}

```

\color{black}\color{white}User's information is totally removed from `STAKERS` item when he claims his BRO rewards:

#### contracts/staking-v1/src/commands.rs

```
staker_info.pending_bro_reward = Uint128::zero();
staker_info.unlock_expired_lockups(&env.block)?;

if staker_info.total_staked()?.is_zero() {
    remove_staker_info(deps.storage, &sender_addr_raw);
} else {
    store_staker_info(deps.storage, &sender_addr_raw, &staker_info)?;
}

```

##### Score

Impact: 3  
Likelihood: 5

##### Recommendation

**SOLVED:** The issue was fixed in commit [f9bbc72a85ff872b36691c4992d7a86439a4bba2](https://github.com/block42-blockchain-company/brotocol-token-contracts/commit/f9bbc72a85ff872b36691c4992d7a86439a4bba2).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Brokkr Protocol P1 Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/brokkr/brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/brokkr/brokkr-protocol-p1-contracts-cosmwasm-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

