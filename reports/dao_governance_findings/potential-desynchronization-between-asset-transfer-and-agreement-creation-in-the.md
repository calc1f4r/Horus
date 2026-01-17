---
# Core Classification
protocol: dForce
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34265
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#3-potential-desynchronization-between-asset-transfer-and-agreement-creation-in-the-timelock
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

Potential desynchronization between asset transfer and agreement creation in the `TimeLock`

### Overview


This bug report discusses an issue with the code for asset transfers and agreement creation in the `TimeLock` smart contract. Currently, these two processes are treated as separate, which can lead to frozen assets and unsatisfiable agreements. The recommendation is to synchronize these processes within the `TimeLock` smart contract to maintain consistency.

### Original Finding Content

##### Description
In the audited code, asset transfer and agreement creation are treated as two separate processes.

- Assets can be transferred to the `TimeLock` without creating an agreement, leading to them being frozen.
- An agreement can be created without transferring assets and may be satisfied using assets intended for other agreements, rendering those agreements unsatisfiable.

Related code - agreement creation: https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/DefaultTimeLock.sol#L47
##### Recommendation
Although the asset transfer and the agreement creation are currently synchronized (outside of the `TimeLock` smart contract), we recommend synchronizing them within the `TimeLock` smart contract itself to maintain the `TimeLock` state consistency.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#3-potential-desynchronization-between-asset-transfer-and-agreement-creation-in-the-timelock
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

