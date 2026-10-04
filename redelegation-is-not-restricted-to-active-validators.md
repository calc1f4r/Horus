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
solodit_id: 51167
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

REDELEGATION IS NOT RESTRICTED TO ACTIVE VALIDATORS

### Overview


This bug report is about a function called `execute_redelegate_proxy` in the `krp-staking-contracts/basset_sei_hub` contract. This function does not restrict redelegation to only active validators, which can cause unexpected situations. For example, if the owner accidentally delegates to a non-active validator and wants to fix it by redelegating to an active validator, they will have to wait for a cooldown period. The code for this function can be found in the `krp-staking-contracts/contracts/basset_sei_hub/src/contract.rs` file. The BVSS score for this issue is 5.0, and the Kryptonite team has already solved it in commit `7de9f39`.

### Original Finding Content

##### Description

The `execute_redelegate_proxy` function in the **krp-staking-contracts/basset\_sei\_hub** contract does not restrict that redelegation is done only to active validators, which could create unexpected situations. For example, if the owner mistakenly delegates to a non-active validator and wants to fix it by redelegating again to an active validator, he will need to wait a cooldown period (because of consecutive redelegations) to carry out this task.

Code Location
-------------

#### krp-staking-contracts/contracts/basset\_sei\_hub/src/contract.rs

```
if sender_contract_addr != validators_registry_contract && sender_contract_addr != conf.creator
{
 return Err(StdError::generic_err("unauthorized"));
}

let messages: Vec<CosmosMsg> = redelegations
 .into_iter()
 .map(|(dst_validator, amount)| {
  cosmwasm_std::CosmosMsg::Staking(StakingMsg::Redelegate {
                src_validator: src_validator.clone(),
                dst_validator,
                amount,
  })
 })
 .collect();

```

##### BVSS

[AO:A/AC:L/AX:M/C:N/I:N/A:H/D:N/Y:N/R:N/S:U (5.0)](/bvss?q=AO:A/AC:L/AX:M/C:N/I:N/A:H/D:N/Y:N/R:N/S:U)

##### Recommendation

**SOLVED**: The `Kryptonite team` solved this issue in commit [7de9f39](https://github.com/KryptoniteDAO/krp-staking-contracts/pull/22/commits/7de9f39498e34d1fe0629532a0dfbc8e30eeb58e).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

