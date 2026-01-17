---
# Core Classification
protocol: Adrena
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46814
audit_firm: OtterSec
contest_link: https://www.adrena.xyz/
source_link: https://www.adrena.xyz/
github_link: https://github.com/AdrenaDEX/adrena

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
finders_count: 2
finders:
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Missing Validation Logic

### Overview

See description below for full details.

### Original Finding Content

## Open Position Short

In open_position_short, stable coins, while typically pegged to a stable value such as one USD, may fluctuate in their market confidence due to market conditions or other factors affecting confidence in their stability. Thus, assuming a stable coin’s value is exactly one USD when it is actually trading at a slightly higher or lower value may impact fee calculations.

## Remediation

1. Ensure to check the confidence of the collateral stable coin.
2. Check `governance_realm`, `governance_realm_config`, `governance_governing_token_holding`, and `governance_governing_token_owner_record` accounts before initiating a CPI into `spl_governance`.

© 2024 Otter Audits LLC. All Rights Reserved. 49/59

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Adrena |
| Report Date | N/A |
| Finders | Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://www.adrena.xyz/
- **GitHub**: https://github.com/AdrenaDEX/adrena
- **Contest**: https://www.adrena.xyz/

### Keywords for Search

`vulnerability`

