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
solodit_id: 30459
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

Unpredictable Behavior Due to Admin Front Running or General Bad Timing

### Overview


This bug report discusses a potential security issue in a system where administrators can make changes without warning. This could lead to malicious changes or accidental negative effects. The report recommends implementing a time lock system to give users advance notice of changes and ensure the behavior of the system is consistent. This could involve making upgrades require two steps with a mandatory waiting period in between.

### Original Finding Content

#### Description


In a number of cases, administrators of contracts can update or upgrade things in the system without warning. This has the potential to violate a security goal of the system.


Specifically, privileged roles could use front running to make malicious changes just ahead of incoming transactions, or purely accidental negative effects could occur due to the unfortunate timing of changes.


Some instances of this are more important than others, but in general, users of the system should have assurances about the behavior of the action they’re about to take.


#### Examples


* Upgradeable TU proxy
* Fee changes take effect immediately


**src/contracts/StakingContract.sol:L504-L512**



```
/// @notice Change the Operator fee
/// @param \_operatorFee Fee in Basis Point
function setOperatorFee(uint256 \_operatorFee) external onlyAdmin {
 if (\_operatorFee > StakingContractStorageLib.getOperatorCommissionLimit()) {
 revert InvalidFee();
 }
 StakingContractStorageLib.setOperatorFee(\_operatorFee);
 emit ChangedOperatorFee(\_operatorFee);
}

```
**src/contracts/StakingContract.sol:L513-L522**



```

/// @notice Change the Global fee
/// @param \_globalFee Fee in Basis Point
function setGlobalFee(uint256 \_globalFee) external onlyAdmin {
 if (\_globalFee > StakingContractStorageLib.getGlobalCommissionLimit()) {
 revert InvalidFee();
 }
 StakingContractStorageLib.setGlobalFee(\_globalFee);
 emit ChangedGlobalFee(\_globalFee);
}

```
#### Recommendation


The underlying issue is that users of the system can’t be sure what the behavior of a function call will be, and this is because the behavior can change at any time.


We recommend giving the user advance notice of changes with a time lock. For example, make all upgrades require two steps with a mandatory time window between them. The first step merely broadcasts to users that a particular change is coming, and the second step commits that change after a suitable waiting period.

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

