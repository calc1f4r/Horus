---
# Core Classification
protocol: Lotaheros
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21019
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-04-13-Lotaheros.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - AuditOne
---

## Vulnerability Title

Using weak source of randomness via block.timestamp for generating the Anity

### Overview


The bug report is about the use of block.timestamp being insecure in a random function. The input parameters are known values, which makes it easier for an attacker to guess the value and precompute multiple block.number. As a result, the attacker can mint the MintFounderHero and get maximum values for strAnity, agiAnity, and intAnity. To help address this issue, it is recommended that external sources of randomness via oracles like Chainlink VRF are used. This would make it more difficult for an attacker to guess the value and precompute multiple block.number.

### Original Finding Content

**Description:** 

Use of block.timestamp is insecure. There is no true source of randomness present in the random function. The input parameters are known values. This makes is easier for the attacker to guess the value. The attacker can precompute multiple block.number,where if he mints the MintFounderHero,he gets the maximum values for strAnity,agiAnity,intAnity. 

**Recommendations:** 

Using external sources of randomness via oracles like Chainlink VRF.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Lotaheros |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-04-13-Lotaheros.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

