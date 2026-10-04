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
solodit_id: 41222
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#10-potential-misallocation-of-validators-in-_getdepositsallocation-function
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

Potential Misallocation of Validators in `_getDepositsAllocation` Function

### Overview


The report describes a problem in the StakingRouter contract's \_getDepositsAllocation function. If a deposit is made before the system updates the status of stuck validators, there is a risk that funds could be allocated to a Node Operator (NO) that has violated an exit request. This could lead to staking funds being deposited into a node operator that is not operating properly or has violated an exit request. The recommendation is to add a mechanism to ensure that the status of all validators, especially stuck validators, is updated before deposits are made. This can be done by adding a flag to the AccountingOracle contract that prevents new deposits from being made until the stuck validators update is finalized.

### Original Finding Content

##### Description
The issue is identified within the [\_getDepositsAllocation](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.8.9/StakingRouter.sol#L1406-L1434) function of the contract `StakingRouter`. If a deposit is made before the system updates the status of stuck validators, there is a risk that funds could be allocated to a Node Operator (NO) that has violated an exit request. This can occur because the calculation uses `availableValidatorsCount`, which may not reflect the true status if stuck validators have not been accounted for yet.

The issue is classified as **Medium** severity because it could lead to the misallocation of validators, resulting in staking funds being deposited into a node operator that is not operating properly or has violated an exit request. The most probable scenario is when NO loses private keys for validators and cannot exit them. In this case, the protocol may allocate new deposits for such NO if the deposit is made before the stuck keys update.

##### Recommendation
We recommend implementing a mechanism to ensure that the status of all validators, especially stuck validators, is updated before deposits are made. This can be done by adding a flag to the `AccountingOracle` contract that prevents new deposits from being made after a new report is submitted until the stuck validators update is finalized.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#10-potential-misallocation-of-validators-in-_getdepositsallocation-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

