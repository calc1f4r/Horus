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
solodit_id: 30477
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#4-unsafe-contract-deployment-and-update-process
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

Unsafe contract deployment and update process

### Overview


This bug report highlights an issue with the deployment process of the KelpDAO-contracts. Currently, the deployment and update process is done in two separate transactions, which can allow third parties to intervene and potentially take control over the contracts. The report recommends using a new function called `upgradeAndCall` to update and initialize the contracts in a single transaction, ensuring better security and control.

### Original Finding Content

##### Description
This issue is identified in the [deployment](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/script/foundry-scripts/DeployLRT.s.sol) scripts and in the history of deploy transactions [[1]](https://etherscan.io/tx/0xf892b9a4e7566e3630103a60244d641ea7a6176a63663a78d1ffdf86859eac15), [[2]](https://etherscan.io/tx/0x9b96b6956ec46895f6b81c261490ebdef9715cdf2aadd772b97d78f5451964a3).

The deployment and update process for the `TransparentUpgradeableProxy` contracts is currently made using two sequential transactions: 
* Update the proxy implementation 
* Invoke the `initialize` function or an update routine.

This approach gives third parties an opportunity to intervene in the deployment or update phase, potentially taking governance control over the deployed contracts. 

##### Recommendation
We recommend utilizing the `upgradeAndCall` function introduced by `EIP-1967` and passing the calldata to the constructor of the proxy to udpate and initialize contracts using a single atomic transaction.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#4-unsafe-contract-deployment-and-update-process
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

