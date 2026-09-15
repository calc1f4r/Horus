---
# Core Classification
protocol: Adaswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57607
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-09-17-Adaswap.md
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
  - zokyo
---

## Vulnerability Title

Missing zero address validation for feeToSetter.

### Overview

See description below for full details.

### Original Finding Content

**Description**

Missing zero address validation of feeToSetter.
Location:
./core/contracts/AdaswapFactory.sol #9
./core/contracts/AdaswapFactory.sol #50

**Recommendation**

It is recommended to validate the variable_feeToSetter to contain a non-zero value before the assignment. Or implement the logic to delete the variable when it is set to zero address, which will allow you to get a gas refund for freeing up storage space. If for some reason it is necessary to permanently block access to changing_feeToSetter, that is, set a zero address in _feeToSetter, then instead of setting a zero value in_feeToSetter directly, you can delete it from the storage. That would provide a refund for this transaction (no more than half from the cost of the transaction or 15,000). In the original version, the zero address is set directly, and in the version with the deletion, the zero address will also be set to zero plus we will get a refund, but the deletion must be written in the code.

**Re-audit comment**

Resolved.
Decision:
Added validation in commit @84cbf03.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Adaswap |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-09-17-Adaswap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

