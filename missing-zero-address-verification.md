---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55427
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Multi%20Scope/README.md#9-missing-zero-address-verification
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

Missing Zero Address Verification

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is associated with the `addOracle` function in the `DIAOracleV2Meta` contract. Specifically, the function lacks a check for zero addresses when adding a new oracle. If an oracle with a zero address is added, it will trigger the `getValue` function to revert abruptly.

##### Recommendation
We recommend implementing a validation check specifically for zero addresses in the `addOracle` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Multi%20Scope/README.md#9-missing-zero-address-verification
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

