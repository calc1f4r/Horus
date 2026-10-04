---
# Core Classification
protocol: Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51609
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/anzen-finance/anzen-v2
source_link: https://www.halborn.com/audits/anzen-finance/anzen-v2
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

Important Values Not Explicitly Set in the Constructor

### Overview

See description below for full details.

### Original Finding Content

##### Description

Essential contract settings like mint fee rates, redeem fee rates and treasury addresses are not configured in the constructors of the affected contracts. This may break certain functionalities if those values are partially set afterwards.

For instance, in the USDz contract, if `mintFeeRate` is set without a corresponding treasury address, functionalities like `deposit()` and `depositBySPCT()` may stop working.

##### BVSS

[AO:S/AC:L/AX:L/C:N/I:H/A:H/D:H/Y:H/R:F/S:U (0.7)](/bvss?q=AO:S/AC:L/AX:L/C:N/I:H/A:H/D:H/Y:H/R:F/S:U)

##### Recommendation

Though the risk associated with this finding is low, it is advisable to enhance contract robustness by including explicit initializations for mint fees, redeem fees, and treasury addresses (if applicable) in the constructor. This preventive measure ensures a complete configuration during contract deployment, minimizing the possibility of operational disruptions due to partially set values.

Additionally, addressing this issue during deployment could simplify contract management and maintenance, contributing to a more streamlined and reliable operational framework.

  
  

### Remediation Plan

**ACKNOWLEDGED:** The **Anzen team** acknowledged the issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol V2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/anzen-finance/anzen-v2
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/anzen-finance/anzen-v2

### Keywords for Search

`vulnerability`

