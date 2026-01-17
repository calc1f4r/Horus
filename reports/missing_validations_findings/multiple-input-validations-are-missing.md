---
# Core Classification
protocol: Gorples Farm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51323
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/entangle-labs/gorples-farm
source_link: https://www.halborn.com/audits/entangle-labs/gorples-farm
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

Multiple input validations are missing

### Overview

See description below for full details.

### Original Finding Content

##### Description

The provided `Farm` program in-scope performs some administrative tasks such as `configure_farm`, `configure_pool` and `add_pool`. These instructions are closely related to state modifications that will affect the `FarmState` account.

In the `Configure Pool` instruction, there is no validation for the parameters `total_reward_share`, `deposit_fee_rate` and `xborpa_percent`, as follows:

`- src/instructions/configure_pool.rs`

```
pub fn handle_configure_pool(
    ctx: Context<ConfigurePool>,
    total_reward_share: u64,
    deposit_fee_rate: u64,
    xborpa_percent: u64,
) -> Result<()> {
    ctx.accounts
        .farm_state
        .register_pool_allocation(ctx.accounts.pool.total_reward_share, total_reward_share)?;
    ctx.accounts.pool.total_reward_share = total_reward_share;
    ctx.accounts.pool.deposit_fee_rate = deposit_fee_rate;
    ctx.accounts.pool.xborpa_percent = xborpa_percent;
    Ok(())
}
```

  

In the `Configure Farm` instruction, there is no validation in place for the `xborpa_cooldown`, `xborpa_redeem_fee` and `xborpa_haircut` parameters, as follows:

```
pub fn handle_configure_farm(
    ctx: Context<ConfigureFarm>,
    xborpa_cooldown: u64,
    xborpa_redeem_fee: u64,
    xborpa_haircut: u64,
) -> Result<()> {
    ctx.accounts
        .farm_state
        .set_params(xborpa_cooldown, xborpa_redeem_fee, xborpa_haircut);
    Ok(())
}
```

  

In the `Create Pool` instruction, there is no validation in place for the parameters `total_reward_share`, `deposit_fee_rate` and `xborpa_percent`, as follows:

`- src/instructions/create_pool.rs`

```
pub fn handle_create_pool(
    ctx: Context<CreatePool>,
    total_reward_share: u64,
    deposit_fee_rate: u64,
    xborpa_percent: u64,
) -> Result<()> {
    ctx.accounts.pool.mint0 = ctx.accounts.mint0.key();
    ctx.accounts.pool.mint1 = ctx.accounts.mint1.key();
    ctx.accounts
        .farm_state
        .register_pool_allocation(0, total_reward_share)?;
    ctx.accounts.pool.total_reward_share = total_reward_share;
    ctx.accounts.pool.deposit_fee_rate = deposit_fee_rate;
    ctx.accounts.pool.xborpa_percent = xborpa_percent;
    Ok(())
}
```

  

All the values casted in these examples are used widely in the protocol, in instructions like `harvest`, `deposit`, `withdraw`, `claim_redeem`, and others. The lack of validation of the inputs given to configuration instructions can lead to miscalculations when executing user-facing instructions.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

It is recommended to perform input validation over the parameters that are given to administrative instructions.

  

### Remediation Plan

**ACKNOWLEDGED:** The **Entangle team** acknowledged this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Gorples Farm |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/entangle-labs/gorples-farm
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/entangle-labs/gorples-farm

### Keywords for Search

`vulnerability`

