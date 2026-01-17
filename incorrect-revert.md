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
solodit_id: 36218
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/SanityChecker/README.md#7-incorrect-revert
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

Incorrect revert

### Overview

See description below for full details.

### Original Finding Content

##### Description
`IncorrectAppearedValidators` should show `churnLimit`, but instead of it, the revert shows `_appearedValidators`: https://github.com/lidofinance/core/blob/efeff81c18f85451ebf98e8fd8bb78b8eb0095f6/contracts/0.8.9/sanity_checks/OracleReportSanityChecker.sol#L782.

##### Recommendation
We recommend updating the specification of the `IncorrectAppearedValidators` revert.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/SanityChecker/README.md#7-incorrect-revert
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

