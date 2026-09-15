---
# Core Classification
protocol: Holograph
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22884
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-10-holograph
source_link: https://code4rena.com/reports/2022-10-holograph
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

protocol_categories:
  - dexes
  - bridge
  - services
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[05] Missing Contract-existence Checks Before Low-level Calls

### Overview

See description below for full details.

### Original Finding Content


Low-level calls return success if there is no code present at the specified address. 

### Recommended Mitigation Steps

In addition to the zero-address checks, add a check to verify that `<address>.code.length > 0`



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Holograph |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-holograph
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-10-holograph

### Keywords for Search

`vulnerability`

