---
# Core Classification
protocol: Quadrata Lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61656
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html
source_link: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html
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
finders_count: 3
finders:
  - Roman Rohleder
  - Ibrahim Abouzied
  - Cristiano Silva
---

## Vulnerability Title

Unresolved Vulnerabilities From Old Compound Code

### Overview


The bug report is about a recent update that was made to a lending contract, which was meant to fix a re-entrancy issue. However, the update only partially fixed the issue and did not include any other potential issues or improvements from the latest version of the Compound protocol. The report recommends that the code be updated to the latest version for better stability.

### Original Finding Content

**Update**
Mitigated in commit [a235be](https://github.com/QuadrataNetwork/lending-contracts/tree/a235be), by re-fixing the explicitly mentioned re-entrancy issue from [compound commit 078356d](https://github.com/compound-finance/compound-protocol/pull/153/commits/078356d5e2e37e1032e61cf1ff586b5b51b5725b). However, other potential issues and/or improvements up until the recent compound version have not been incorporated.

**File(s) affected:**`All contracts`

**Recommendation:** We highly recommend rebasing the code to the latest (stable) version of the Compound protocol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Quadrata Lending |
| Report Date | N/A |
| Finders | Roman Rohleder, Ibrahim Abouzied, Cristiano Silva |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html

### Keywords for Search

`vulnerability`

