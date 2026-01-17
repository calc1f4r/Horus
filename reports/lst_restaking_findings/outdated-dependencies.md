---
# Core Classification
protocol: Restaking
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52119
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/solayer/restaking
source_link: https://www.halborn.com/audits/solayer/restaking
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

Outdated dependencies

### Overview

See description below for full details.

### Original Finding Content

##### Description

It was identifying during the assessment of the program `restaking` in-scope that its dependencies for the Anchor framework and also for Solana are not current.

```
[[package]]
name = "solana-program"
version = "1.18.7"
```

```
[[package]]
name = "anchor-lang"
version = "0.29.0"
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

It is recommended to update dependencies to their current versions, as specified:

* Solana: `v1.18.20`
* Anchor: `v0.31.0`

  

### Remediation Plan

**SOLVED:** The **Solayer team** has solved this issue as recommended. The commit hash containing the modification is `46c09073a6dad390f435dc76f17e35849f2c6d1b`.

##### Remediation Hash

<https://github.com/solayer-labs/restaking-program/commit/46c09073a6dad390f435dc76f17e35849f2c6d1b>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Restaking |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/solayer/restaking
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/solayer/restaking

### Keywords for Search

`vulnerability`

