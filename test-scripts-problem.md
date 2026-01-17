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
solodit_id: 28338
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/1inch%20Rewards%20Manager/README.md#2-test-scripts-problem
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

Test scripts problem

### Overview

See description below for full details.

### Original Finding Content

##### Description
This problem is not in the audit scope.
The following two tests do not work correctly:
`test_owner_recovers_erc20_to_own_address` and `test_owner_recovers_erc20_zero_amount`.

##### Recommendation
It is recommended to fix the tests.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/1inch%20Rewards%20Manager/README.md#2-test-scripts-problem
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

