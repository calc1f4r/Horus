---
# Core Classification
protocol: Zkdx
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37504
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-18-zkDX.md
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
  - Zokyo
---

## Vulnerability Title

Governance control is centralized through a single gov address.

### Overview


This report discusses a potential issue with the `VaultPriceFeed` contract, which has a single address responsible for important governance actions. This creates a risk of a single point of failure if the address is compromised. The recommendation is to implement a decentralized governance control, an emergency stop mechanism, and transparency and monitoring measures to mitigate this risk. 

### Original Finding Content

**Severity** : Medium

**Status** : Acknowledged

**Description**

The contract `VaultPriceFeed` employs a single gov address for critical governance actions, it introduces a significant risk by creating a single point of failure. If the private key associated with the gov address is compromised, an attacker gains the capability to manipulate crucial contract settings, potentially leading to system-wide vulnerabilities or exploitation.

https://github.com/zkDX-DeFi/Smart_Contracts/blob/35f1d4b887bd5b0fc580b7d9fe951c4b550c9897/contracts/core/VaultPriceFeed.sol#L13

**Recommendation**

Decentralized Governance Control: Implement a multi-signature mechanism or a decentralized autonomous organization (DAO) structure for critical governance decisions.

Emergency Stop Mechanism: Introduce an emergency stop feature that can be activated by multiple parties in case of a detected compromise. This can halt critical contract functions until a thorough investigation is conducted.

Transparency and Monitoring: Maintain transparency about governance actions with the community or stakeholders. Implement monitoring and alert systems for governance-related activities to detect unusual patterns that may indicate a compromise.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zkdx |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-18-zkDX.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

