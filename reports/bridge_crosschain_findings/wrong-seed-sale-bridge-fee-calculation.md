---
# Core Classification
protocol: Plutus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45565
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2020-07-21-Plutus.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

Wrong Seed sale bridge fee calculation

### Overview


The bug report states that the method claimSeedTokens relies on another method called getCurrentFee, which is only valid if a certain property called TGE is set. However, there is a possibility that the claimSeedTokens method can be called before the TGE property is set, which can cause errors. The recommendation is to add an extra check in the claimSeedTokens method to ensure that the TGE property is already initialized. This issue has been resolved.

### Original Finding Content

**Description**

Method claimSeedTokens depends on method getCurrentFee, that is valid only if TGE is set, but
method claimSeedTokens could be called even before property TGE is set.

**Recommendation**:

Method claimSeedTokens should have extra check if property TGE is already initialized.

**Re-audit comment**:

Resolved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Plutus |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2020-07-21-Plutus.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

