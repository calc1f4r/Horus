---
# Core Classification
protocol: Gorples Chef & Farm updates
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51277
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/entangle-labs/gorples-chef-and-farm-updates
source_link: https://www.halborn.com/audits/entangle-labs/gorples-chef-and-farm-updates
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

USERS REWARDS LOSS IF FARM SET START REWARDS AFTER DEPOSITS

### Overview

See description below for full details.

### Original Finding Content

##### Description

During the initialization of the **FarmState**, the **start\_time** is assigned a default value of zero. If this value is not modified before users make deposits, it will create the impression that the **FarmState** has started, allowing deposit to be performed and rewards to be obtained.

[*harvest.rs*](http://harvest.rs)

```
impl FarmState {
    pub const LEN: usize = 8 + 32 + 8 * 7;

    pub fn new(config: FarmConfig) -> Self {
        Self {
            admin: config.admin,
            xborpa_cooldown: config.xborpa_cooldown,
            xborpa_redeem_fee: config.xborpa_redeem_fee,
            xborpa_haircut: config.xborpa_haircut,
            total_borpa_minted: 0,
            total_xborpa: 0,
            allocated_reward_share: 0,
            start_time: 0,
        }
    }
```

When users make their first deposits, their new positions will be initialized through the `Harvest` instruction, updating their **last\_claim\_timestamp** to the current **unix\_timestamp**. The `Harvest` instruction handles the necessary calculations for users to receive rewards based on the **last\_claim\_timestamp** of their position at the time of the call.

However, the `SetStartRewards` instruction allows the admin to modify the **start\_time** at any moment.

*set\_start\_rewards.rs*

```
pub fn handle_set_start_rewards(ctx: Context<SetStartRewards>, start_time: u64) -> Result<()> {
    ctx.accounts
        .farm_state
        .set_start_rewards(start_time, ctx.accounts.clock.unix_timestamp as u64)?;
    Ok(())
```

[*state.rs*](http://state.rs)

```
pub fn set_start_rewards(
        &mut self,
        start_time: u64,
        now: u64,
    ) -> std::result::Result<(), CustomError> {
        /*if self.start_time != 0 && now > self.start_time {
            return Err(CustomError::RewardsAlreadyStarted);
        }*/
        if now > start_time && start_time != 0 {
            return Err(CustomError::InvalidStartTime);
        }
        self.start_time = start_time;
        Ok(())
```

  

If this value is changed to postpone the **start\_time** after deposits have been made, users who have previously deposited will lose the rewards corresponding to the days that have passed since they deposited.This occurs because rewards cannot be calculated until the Farm has started. Once the Farm begins, the `last_claim_timestamp` will be updated based on the time of the call.

*harvest.rs*

```
  if !self.farm_state.is_started(self.clock.unix_timestamp as u64) {
            return Ok(());
        }

        if self.position.last_claim_timestamp == 0
            || self.position.last_claim_timestamp < self.farm_state.start_time
        {
            self.position.last_claim_timestamp = self.clock.unix_timestamp as u64;
            return Ok(());
        }
```

##### BVSS

[AO:S/AC:L/AX:L/C:N/I:M/A:M/D:N/Y:C/R:N/S:U (2.5)](/bvss?q=AO:S/AC:L/AX:L/C:N/I:M/A:M/D:N/Y:C/R:N/S:U)

##### Recommendation

To address this issue, consider implementing one of the following options:

* Disallow deposits if the Farm has is not started.
* Prevent changes to the start time of the Farm State once deposits have been made.

### Remediation Plan

**RISK ACCEPTED:** The **Entangle team** accepted the risk related to this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Gorples Chef & Farm updates |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/entangle-labs/gorples-chef-and-farm-updates
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/entangle-labs/gorples-chef-and-farm-updates

### Keywords for Search

`vulnerability`

