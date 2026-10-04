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
solodit_id: 51162
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
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

WITHOUT POSSIBILITY TO SWAP ALL NATIVE TOKENS TO REWARD DENOMINATION

### Overview


The bug report states that the `ExecuteMsg::SwapToRewardDenom` message in the `krp-staking-contracts/basset_sei_reward` contract can only be executed by the `krp-staking-contracts/basset_sei_rewards_dispatcher` contract. However, there is no function in the dispatcher contract that allows for this swap to occur, making it impossible to swap native tokens to the reward denomination. This issue has been solved by the Kryptonite team in a recent commit.

### Original Finding Content

##### Description

Executing the `ExecuteMsg::SwapToRewardDenom` message in the **krp-staking-contracts/basset\_sei\_reward** contract is restricted for only the **krp-staking-contracts/basset\_sei\_rewards\_dispatcher** contract. However, there is no function in that contract that allows to execute the swap, which makes not possible to swap all native tokens to reward denomination.

Code Location
-------------

The **krp-staking-contracts/basset\_sei\_rewards\_dispatcher** contract does not call the `ExecuteMsg::SwapToRewardDenom` message:

#### krp-staking-contracts/contracts/basset\_sei\_rewards\_dispatcher/src/contract.rs

```
#[cfg_attr(not(feature = "library"), entry_point)]
pub fn execute(deps: DepsMut, env: Env, info: MessageInfo, msg: ExecuteMsg) -> StdResult<Response> {
 match msg {
  ExecuteMsg::SwapToRewardDenom {
   bsei_total_bonded: bsei_total_mint_amount,
   stsei_total_bonded: stsei_total_mint_amount,
  } => execute_swap(
   deps,
   env,
   info,
   bsei_total_mint_amount,
   stsei_total_mint_amount,
  ),
  ExecuteMsg::DispatchRewards {} => execute_dispatch_rewards(deps, env, info),
  ExecuteMsg::UpdateConfig {
   owner,
   hub_contract,
   bsei_reward_contract,
   stsei_reward_denom,
   bsei_reward_denom,
   krp_keeper_address,
   krp_keeper_rate,
  } => execute_update_config(
   deps,
   env,
   info,
   owner,
   hub_contract,
   bsei_reward_contract,
   stsei_reward_denom,
   bsei_reward_denom,
   krp_keeper_address,
   krp_keeper_rate,
  ),
  ExecuteMsg::UpdateSwapContract { swap_contract } => {
   update_swap_contract(deps, info, swap_contract)
  }
  ExecuteMsg::UpdateSwapDenom { swap_denom, is_add } => {
   update_swap_denom(deps, info, swap_denom, is_add)
  }
  ExecuteMsg::UpdateOracleContract { oracle_contract } => {
   update_oracle_contract(deps, info, oracle_contract)
  }
 }
}

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:H/D:N/Y:N/R:N/S:U (7.5)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:H/D:N/Y:N/R:N/S:U)

##### Recommendation

**SOLVED**: The `Kryptonite team` solved this issue in commit [a5c858c](https://github.com/KryptoniteDAO/krp-staking-contracts/pull/20/commits/a5c858cc8dd4d0e423cc83e3f21318c784f2428d).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

