---
# Core Classification
protocol: Bellum Core
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52354
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/bellum-exchange/bellum-core
source_link: https://www.halborn.com/audits/bellum-exchange/bellum-core
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

Missing Zero Address Validation

### Overview

See description below for full details.

### Original Finding Content

##### Description

In `BellumFactory` contract, the constructor accepts critical addresses (`owner_`, `tjRouter_`, `pharaohRouter_`, `incentivizer_`) without validating that they are not the zero address (**0x0**). If any of these parameters are accidentally set to the zero address, it could lead to locked functionality or loss of funds since:

  

* Zero address owner would make the contract permanently ownerless
* Invalid router addresses would break core trading functionality
* Zero address incentivizer would lead to lost token incentives

##### BVSS

[AO:S/AC:L/AX:M/R:N/S:U/C:N/A:H/I:H/D:N/Y:H (1.5)](/bvss?q=AO:S/AC:L/AX:M/R:N/S:U/C:N/A:H/I:H/D:N/Y:H)

##### Recommendation

Add zero address validation checks in the constructor:

```
require(owner_ != address(0), "Zero address not allowed for owner");
require(tjRouter_ != address(0), "Zero address not allowed for TJ router");
require(pharaohRouter_ != address(0), "Zero address not allowed for Pharaoh router");
require(incentivizer_ != address(0), "Zero address not allowed for incentivizer");
```

##### Remediation

**SOLVED**: The suggested mitigation was implemented by the **Bellum Exchange team**.

##### Remediation Hash

357ab688b7677125df61c3661d0865bea0652542

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Bellum Core |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/bellum-exchange/bellum-core
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/bellum-exchange/bellum-core

### Keywords for Search

`vulnerability`

