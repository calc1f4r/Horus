---
# Core Classification
protocol: Ozean Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49225
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Ozean%20Finance/README.md#10-missing-zero-address-checks-in-constructor
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

Missing Zero Address Checks in Constructor

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the constructor of contract `LGEMigrationV1`. Multiple parameters, including `_owner`, `_l1StandardBridge`, `_l1LidoTokensBridge`, `_usdxBridge`, `_lgeStaking`, `_usdc`, and `_wstETH`, are not validated to ensure they are non-zero addresses. This can lead to misconfiguration and unexpected behavior if these parameters are incorrectly initialized.

The issue is classified as **Low** severity because it does not directly compromise security but can result in operational inefficiencies or require redeployment if discovered later.

##### Recommendation
We recommend adding `require` statements in the constructor to ensure that all addresses passed as parameters are non-zero, preventing misconfiguration and maintaining the integrity of the deployment.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Ozean Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Ozean%20Finance/README.md#10-missing-zero-address-checks-in-constructor
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

