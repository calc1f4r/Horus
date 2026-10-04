---
# Core Classification
protocol: DexodusV2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52401
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dexodus/dexodusv2
source_link: https://www.halborn.com/audits/dexodus/dexodusv2
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
  - Halborn
---

## Vulnerability Title

Missing Position Validation for Orders and Potential DOS via Invalid Orders

### Overview

The report discusses a bug in the `order` function which does not validate the existence of a position for decrease orders. This can lead to underflow errors and a DOS vulnerability, where attackers can spam invalid orders and overload the system. The recommendation is to add a position validation check for decrease orders to ensure the position exists and has sufficient collateral and size. The bug has been solved by performing an existence check via the position key and its size.

### Original Finding Content

##### Description

The `order` function does **not validate the existence of a position** for **decrease orders** (`orderType != 0`). This allows creating orders without a valid position, leading to:

1. **Underflow Errors:** Invalid size or collateral can cause **reverts** during `modifyPosition` execution.
2. **DOS Vulnerability:** Attackers can **spam invalid orders**, overloading the system and blocking valid ones.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:H/D:N/Y:N/R:P/S:C (5.5)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:H/D:N/Y:N/R:P/S:C)

##### Recommendation

Add a **position validation check** for `orderType != 0` to ensure the position exists and has **sufficient collateral and size**. This prevents invalid orders from being processed and reduces the risk of **DOS attacks** and **underflows**. Adding spam protection or rate limits can further secure the system.

##### Remediation

**SOLVED:** The Automation contracts are performing an existence check via the position key and its size.

##### Remediation Hash

2a9423c22a20ceddb37bd7c4a166e686817373a6

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | DexodusV2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/dexodus/dexodusv2
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/dexodus/dexodusv2

### Keywords for Search

`vulnerability`

