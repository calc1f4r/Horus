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
solodit_id: 28125
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#2-no-validation-of-the-address-parameter-value-in-the-contract-constructor
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

No validation of the address parameter value in the contract constructor

### Overview


This bug report is about the variable "TREASURY" in the "LidoMevTxFeeVault.sol" file. The variable is assigned the value of the constructor input parameter, however, this parameter is not checked before being assigned. If the value turns out to be zero, then the contract will need to be redeployed, as there is no other functionality to set this variable.

The recommendation is that a check should be added to the input parameter to ensure that it is not zero before initializing the variable. This will ensure that the variable is always set to a value other than zero, and the contract does not need to be redeployed.

### Original Finding Content

##### Description
The variable is assigned the value of the constructor input parameter. But this parameter is not checked before this. If the value turns out to be zero, then it will be necessary to redeploy the contract, since there is no other functionality to set this variable.
At line 
https://github.com/lidofinance/lido-dao/blob/801d3e854efb33ff33a59fe51187e187047a6be2/contracts/0.8.9/LidoMevTxFeeVault.sol#L72 
the `TREASURY` variable is set to the value of the `_treasury` input parameter.
##### Recommendation
It is necessary to add a check of the input parameter to zero before initializing the variable.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#2-no-validation-of-the-address-parameter-value-in-the-contract-constructor
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

