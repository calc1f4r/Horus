---
# Core Classification
protocol: Keep3r.Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56914
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Keep3r.Network/Sunset/README.md#1-missing-validations-in-constructor
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

Missing Validations in Constructor

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified within the `__init__` function of the `vKP3R Snapshot Distribution` contract.
The constructor lacks validations for input parameters, even though the contract is tailored for a specific airdrop. In particular, the `TOKEN` address is not checked for being the zero address, and the `SNAPSHOT` block number is not validated to ensure it is not set in the future.
The issue is classified as **Low** severity because these missing checks, although not immediately exploitable in the current context, could lead to future misconfigurations or vulnerabilities if the contract is reused or modified.
<br/>
##### Recommendation
We recommend adding explicit validations in the constructor to ensure that the `TOKEN` address is not the zero address and that the `SNAPSHOT` block number is not set in the future.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Keep3r.Network |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Keep3r.Network/Sunset/README.md#1-missing-validations-in-constructor
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

