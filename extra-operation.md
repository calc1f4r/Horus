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
solodit_id: 28163
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/In-protocol%20Coverage/README.md#1-extra-operation
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

Extra operation

### Overview

See description below for full details.

### Original Finding Content

##### Description
At the line
https://github.com/lidofinance/lido-dao/blob/ee1991b3bbea2a24b042b0a4433be04301992656/contracts/0.8.9/SelfOwnedStETHBurner.sol#L223
checks the value of the `_token` variable. But if the value of the variable is zero, then the code on line 228 will not be executed.
Similarly for the line:
https://github.com/lidofinance/lido-dao/blob/ee1991b3bbea2a24b042b0a4433be04301992656/contracts/0.8.9/SelfOwnedStETHBurner.sol#L239
##### Recommendation
It is necessary to remove redundant operations.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/In-protocol%20Coverage/README.md#1-extra-operation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

