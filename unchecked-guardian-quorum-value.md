---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41215
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#3-unchecked-guardian-quorum-value
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

Unchecked Guardian Quorum Value

### Overview


This bug report is about a problem in the code of a contract called `DepositSecurityModule`. The issue is in a function called `_setGuardianQuorum` which allows setting a value for something called a "guardian quorum". The problem is that the code does not check if the new value is higher than the number of active guardians, which could cause problems for the contract's operation and decision-making. The severity of this issue is classified as "Medium" because it could cause disruptions and governance issues. The recommendation is to add a step in the code to make sure that the new quorum value is not higher than the current number of guardians.

### Original Finding Content

##### Description
The issue is identified within the [\_setGuardianQuorum](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.8.9/DepositSecurityModule.sol#L247-L254) function of the `DepositSecurityModule` contract. The function allows setting a guardian quorum value without checking if it exceeds the number of active guardians.

The issue is classified as **Medium** severity because it could lead to operational disruptions and governance issues if the quorum set is greater than the number of available guardians.

##### Recommendation
We recommend introducing a validation step within the `_setGuardianQuorum` function to ensure that the new quorum value does not exceed the current number of guardians.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#3-unchecked-guardian-quorum-value
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

