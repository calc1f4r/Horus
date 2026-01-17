---
# Core Classification
protocol: Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51194
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
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

REPEATED EXECUTION MESSAGES

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `ExecuteMsg::MigrateUnbondWaitList` and `ExecuteMsg::UpdateParams` messages are repeated in the `execute` function from **krp-staking-contracts/basset\_sei\_hub** contract. Although this situation doesn't pose a security risk, it's included in the report as part of the DRY (Don't Repeat Yourself) principle used as a best practice in software development to improve the maintainability of code during all phases of its lifecycle.

Code Location
-------------

The `ExecuteMsg::MigrateUnbondWaitList` and `ExecuteMsg::UpdateParams` messages are repeated in the `execute` function:

#### krp-staking-contracts/contracts/basset\_sei\_hub/src/contract.rs

```
#[cfg_attr(not(feature = "library"), entry_point)]
pub fn execute(deps: DepsMut, env: Env, info: MessageInfo, msg: ExecuteMsg) -> StdResult<Response> {
 if let ExecuteMsg::MigrateUnbondWaitList { limit } = msg {
  return migrate_unbond_wait_lists(deps.storage, limit);
 }

 if let ExecuteMsg::UpdateParams {
  epoch_period,
  unbonding_period,
  peg_recovery_fee,
  er_threshold,
  paused,
 } = msg
 {
  return execute_update_params(
   deps,
   env,
   info,
   epoch_period,
   unbonding_period,
   peg_recovery_fee,
   er_threshold,
   paused,
  );
 }

```

#### krp-staking-contracts/contracts/basset\_sei\_hub/src/contract.rs

```
ExecuteMsg::WithdrawUnbonded {} => execute_withdraw_unbonded(deps, env, info),
ExecuteMsg::CheckSlashing {} => execute_slashing(deps, env),
ExecuteMsg::UpdateParams {
 epoch_period,
 unbonding_period,
 peg_recovery_fee,
 er_threshold,
 paused,
} => execute_update_params(
  deps,
  env,
  info,
  epoch_period,
  unbonding_period,
  peg_recovery_fee,
  er_threshold,
  paused,
 ),

```

#### krp-staking-contracts/contracts/basset\_sei\_hub/src/contract.rs

```
ExecuteMsg::RedelegateProxy {
 src_validator,
 redelegations,
} => execute_redelegate_proxy(deps, env, info, src_validator, redelegations),
ExecuteMsg::MigrateUnbondWaitList { limit: _ } => Err(StdError::generic_err("forbidden")),

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

**ACKNOWLEDGED**: The `Kryptonite team` acknowledged this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

