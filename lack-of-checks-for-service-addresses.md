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
solodit_id: 41226
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#4-lack-of-checks-for-service-addresses
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Lack of Checks for Service Addresses

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the `CSModule` contract. Specifically, there is a potential concern if the `rewardAddress` or `managerAddress` address of a Node Operator is one of the service addresses (`CSAccounting` for example). This could result in the user bond being reduced, and some funds becoming stuck in the accounting. Although this situation might seem acceptable under current conditions, it would be more robust to include appropriate checks during the initialization phase to prevent such scenarios.

The issue is classified as **Low** severity because the current implementation could lead to inefficiencies in fund management, though it does not directly compromise the security or functionality of the system.

##### Recommendation
We recommend adding validation checks during the Node Operator initialization phase to ensure that neither the `rewardAddress` nor the `managerAddress` address is one of the service addresses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#4-lack-of-checks-for-service-addresses
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

