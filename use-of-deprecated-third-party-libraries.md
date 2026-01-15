---
# Core Classification
protocol: Reservoir
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51147
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/fortunafi/reservoir-updated
source_link: https://www.halborn.com/audits/fortunafi/reservoir-updated
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
  - Halborn
---

## Vulnerability Title

Use of Deprecated Third-Party Libraries

### Overview

See description below for full details.

### Original Finding Content

##### Description

The codebase utilizes two outdated third-party libraries, which could pose security and maintenance risks. Specifically:

1. The library `chainlink` version `1.11.0` is being used. The latest version available for the `1.x.x` branch is `1.13.3` (from mid-2023) and, for the `2.x.x` is `2.11.0`.
2. The library `openzeppelin-contracts` version `4.8.1` is in use.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:L/A:L/D:N/Y:N/R:N/S:U (3.1)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:L/A:L/D:N/Y:N/R:N/S:U)

##### Recommendation

Consider updating the libraries in use to the latest stable version available.

Remediation plan
----------------

**ACKNOWLEDGED**: The **FortunaFi team** acknowledges that Chainlink 1.11.0 and openzeppelin-contracts 4.8.1 are not the latest versions and intentionally use them as they have been more tested by the community than newer versions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Reservoir |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/fortunafi/reservoir-updated
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/fortunafi/reservoir-updated

### Keywords for Search

`vulnerability`

