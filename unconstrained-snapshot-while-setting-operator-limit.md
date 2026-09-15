---
# Core Classification
protocol: Kilnfi Staking (Consensys)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30455
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/08/kilnfi-staking-consensys/
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
finders_count: 2
finders:
  -  Martin Ortner

  - Tejaswa Rastogi
---

## Vulnerability Title

Unconstrained Snapshot While Setting Operator Limit

### Overview


The bug report discusses a function called `setOperatorLimit` that allows a certain user to set or update the staking limit for an operator. The function has a condition that checks if the limit is being increased, the `_snapshot` must be ahead of the last validator edit. However, the parameter `_snapshot` can be any number, which is not ideal. Additionally, there are other functions called `addValidators` and `removeValidators` that update the `block.number` for the last validator edit, but do not constrain it. This can be confusing for users as there are no public functions to access this value. The recommendation is to either remove this functionality if it is not necessary or add logic to constrain the last validator edit or provide public functions for users to access it.

### Original Finding Content

#### Description


Function `setOperatorLimit` as the name says, allows the `SYS_ADMIN` to set/update the staking limit for an operator. The function ensures that if the limit is being increased, the `_snapshot` must be ahead of the last validator edit(`block.number` at which the last validator edit occurred). However, the parameter `_snapshot` is unconstrained and can be any number. Also, the functions `addValidators` and `removeValidators` update the `block.number` signifying the last validator edit, but never constrain the new edits with it. Since there are no publicly available functions to access this value, makes the functionality even more confusing and may be unnecessary.


**src/contracts/StakingContract.sol:L468-L473**



```
if (
 operators.value[\_operatorIndex].limit < \_limit &&
 StakingContractStorageLib.getLastValidatorEdit() > \_snapshot
) {
 revert LastEditAfterSnapshot();
}

```
#### Recommendation


If the functionality is not needed, consider removing it. Otherwise, add some necessary logic to either constrain the last validator edit or add public functions for the users to access it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Kilnfi Staking (Consensys) |
| Report Date | N/A |
| Finders |  Martin Ortner
, Tejaswa Rastogi |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/08/kilnfi-staking-consensys/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

