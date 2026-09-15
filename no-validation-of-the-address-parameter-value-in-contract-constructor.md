---
# Core Classification
protocol: PieDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28692
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/PieDAO/ExperiPie/README.md#1-no-validation-of-the-address-parameter-value-in-contract-constructor
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
  - MixBytes
---

## Vulnerability Title

No validation of the address parameter value in contract constructor

### Overview


This bug report is about the Pie-Dao ExperiPie codebase. The problem is that certain variables are being assigned the values of constructor input parameters without being checked first. If the value turns out to be zero, then there is no other functionality to set this variable and the contract must be redeployed. Specifically, the variables `lendingPool`, `lendingRegistry`, `basket`, `_assetShort`, `_assetLong`, `_priceFeed`, and `_synthetix` are all affected.

To fix this issue, it is necessary to add a check of the input parameter to zero before initializing the variables. This will ensure that the variables are not set to a zero value, and the contract will not need to be redeployed.

### Original Finding Content

##### Description
The variable is assigned the value of the constructor input parameter. But this parameter is not checked before this. If the value turns out to be zero, then it will be necessary redeploy the contract, since there is no other functionality to set this variable.

At the line https://github.com/pie-dao/ExperiPie/blob/facf3c246d9c43f5b1e0bad7dc2b0a9a2a2393c5/contracts/callManagers/LendingManager/LendingLogicAave.sol#L16 the `lendingPool` variable is set to the value of the `_lendingPool` input parameter.

At the line https://github.com/pie-dao/ExperiPie/blob/facf3c246d9c43f5b1e0bad7dc2b0a9a2a2393c5/contracts/callManagers/LendingManager/LendingLogicCompound.sol#L16 the `lendingRegistry` variable is set to the value of the `_lendingRegistry` input parameter.

At the line https://github.com/pie-dao/ExperiPie/blob/facf3c246d9c43f5b1e0bad7dc2b0a9a2a2393c5/contracts/callManagers/LendingManager/LendingManager.sol#L24 the `lendingRegistry` variable is set to the value of the `_lendingRegistry` input parameter.

At the line https://github.com/pie-dao/ExperiPie/blob/facf3c246d9c43f5b1e0bad7dc2b0a9a2a2393c5/contracts/callManagers/LendingManager/LendingManager.sol#L25 the variable `basket` is assigned the value of the input parameter` _basket`.

At the line https://github.com/pie-dao/ExperiPie/blob/facf3c246d9c43f5b1e0bad7dc2b0a9a2a2393c5/contracts/callManagers/RSIManager.sol#L31 values of the following variables are not checked: `_assetShort`,`_assetLong`, `_priceFeed`,`_basket`, `_synthetix`.

##### Recommendation
In all the cases, it is necessary to add a check of the input parameter to zero before initializing the variables.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | PieDAO |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/PieDAO/ExperiPie/README.md#1-no-validation-of-the-address-parameter-value-in-contract-constructor
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

