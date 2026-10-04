---
# Core Classification
protocol: Maha's Core
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52163
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/maha/mahas-core
source_link: https://www.halborn.com/audits/maha/mahas-core
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

Lack of zero address checks

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `initialize` function in the `PegStabilityModule` lacks validation checks for zero addresses, potentially leading to critical issues. Initializing contracts with zero addresses can result in unexpected behavior or security vulnerabilities, as zero addresses may represent invalid or unintentional destinations. Implementing checks to ensure addresses are not zero is essential to maintain contract integrity, prevent errors, and enhance overall security.

Besides, there are no zero checks in the following functions either:

* `mint`
* `redeem`
* `updateFeeDestination`

Regarding the contract `DDHub.sol`:

* `initialize`
* `setFeeCollector`

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:H/D:N/Y:N/R:F/S:U (1.9)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:H/D:N/Y:N/R:F/S:U)

##### Recommendation

Consider including pertinent address checks.

  

Remediation Plan
----------------

**ACKNOWLEDGED**: The **Maha team** acknowledged this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Maha's Core |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/maha/mahas-core
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/maha/mahas-core

### Keywords for Search

`vulnerability`

