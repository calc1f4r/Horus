---
# Core Classification
protocol: Tradable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44937
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-01-Tradable.md
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
  - Zokyo
---

## Vulnerability Title

Missing zero address check for endpoint

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**:  Resolved

**Description**

In the TradableSettingsMessageAdapter contract, there is a missing zero address check for the endpoint in the constructor. 
Similarly, in the TradableSideVault contract, there is a missing zero address check for the endpoint in the constructor. It is important to add a zero address check here because the endpoint can be set only once.
In addition to this, in the TradableSideVault contract,  there is a missing zero address check for adminUser in setAdminUser() function.

**Recommendation**: 

It is advised to add a proper require check for the same.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tradable |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-01-Tradable.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

