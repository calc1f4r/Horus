---
# Core Classification
protocol: Thetanuts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56503
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-16-Thetanuts.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

Assertion always fails in case there are lent tokens.

### Overview


The bug report is about a modifier called checkInvariant() in the CommonV1.sol file. The report states that there is an issue with the "require" statement on line 90, which will always fail if tokens are sent to Aave. This is because the balance cannot be higher than the sum of "vaultCollatSize" and "collatLentOut". The recommendation is to check if the modifier is working properly and not causing any problems with the vault's operation.

### Original Finding Content

**Description**

CommonV1.sol, modifier checkInvariant().
“Require” in line 90 will always fail in case there are tokens, sent to Aave, since balance cannot
be greater, than “vaultCollatSize + collatLentOut”

**Recommendation**:

Verify that the modifier works as intended and doesn’t prevent operation of the vault.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Thetanuts |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-16-Thetanuts.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

