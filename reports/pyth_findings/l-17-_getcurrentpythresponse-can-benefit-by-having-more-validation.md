---
# Core Classification
protocol: Apollon Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53870
audit_firm: Recon Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
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
  - Alex The Entreprenerd
---

## Vulnerability Title

[L-17] `_getCurrentPythResponse` can benefit by having more validation

### Overview

See description below for full details.

### Original Finding Content

**Impact**

Pyth works as follows:
- It returns an integer
- It returns an exponent by which to scale the integer for the price
- it returns the publishTime
- and a confidence interval

The reason why Pyth includes a confidence interval is due to the impossibility of chosing a single price that is the "correct" price

**Mitigation**

Consider implementing additional checks, you could take inspiration from Euler's multi-audited feeds:
https://github.com/euler-xyz/euler-price-oracle/blob/master/src/adapter/pyth/PythOracle.sol

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Recon Audits |
| Protocol | Apollon Report |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

