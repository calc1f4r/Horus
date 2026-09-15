---
# Core Classification
protocol: Nume
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31652
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-03-05-Nume.md
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
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-08] RegistrationFacet.changeVerificationAddress() zero check missed

### Overview

See description below for full details.

### Original Finding Content

`RegistrationFacet.changeVerificationAddress()` allows setting `AppStorage.numeStorage().verificationAddress` as the zero address. It is not correct for future signature checks used in `SettlementsFacet`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nume |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-03-05-Nume.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

