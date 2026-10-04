---
# Core Classification
protocol: Museumofmahomes
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26481
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-MuseumOfMahomes.md
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
  - Pashov
---

## Vulnerability Title

[L-04] Contract is not working as a state machine

### Overview

See description below for full details.

### Original Finding Content

Currently it is possible for the `metadataOwner` to set the `redeemOpen` value to `true` while the `revealOpen` hasn't been set to `true` yet. There should be a sequence/flow of how the contract works - first minting, then revealing, then redeem (or redeem right after reveal). Allow setting `redeemOpen` to `true` only if `revealOpen == true`, and also allow setting `revealOpen` to `true` only when mint is completed (`totalSupply == MAX_SUPPLY`).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Museumofmahomes |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-MuseumOfMahomes.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

