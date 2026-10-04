---
# Core Classification
protocol: KelpDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30482
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#9-the-possible-inability-to-initialize-the-eigenpod-field
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

The possible inability to initialize the `eigenPod` field

### Overview


The `NodeDelegator.stakeETH` function has a bug that causes issues with initializing the `eigenPod` address. This can lead to incorrect accounting of withdrawals and rewards from the ETH restaking process. The bug is considered high priority and can only be fixed by updating the proxy with a new function. To prevent this bug, it is recommended to initialize the `eigenPod` field in the `stakeETH` function if it was not previously deployed using the `createEigenPod` function.

### Original Finding Content

##### Description
The problem has been identified in the [`NodeDelegator.stakeEth`](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/contracts/NodeDelegator.sol#L185) function.

Invoking the `stakeETH` method prior to executing `createEigenPod` leads to an implicit deployment of the `eigenPod`. However, this action fails to initialize its address within the `NodeDelegator` contract. Consequently, it blocks the `verifyWithdrawalCredentials` and `getETHEigenPodBalance` preventing accurate accounting of withdrawals and rewards derived from the ETH restaking in the pod. This condition persists until admin intervenes to update the implementation of proxy with a function that recovers the address. 

This issue is classified as `high` due to the inability to initialize `eigenPod`, which may result in discrepancies in the accounting of withdrawal and reward assets, affecting the `RSETHPrice` value. Recovery from this state is feasible only through a proxy update.

##### Recommendation
We recommend initializaing the `eigenPod` field in the `stakeETH` function, if it is wasn't deployed earlier explicitly using the `createEigenPod` call.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | KelpDAO |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#9-the-possible-inability-to-initialize-the-eigenpod-field
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

