---
# Core Classification
protocol: Light Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47077
audit_firm: OtterSec
contest_link: https://lightprotocol.com/
source_link: https://lightprotocol.com/
github_link: https://github.com/Lightprotocol

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
finders_count: 3
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Tuyết Dương
---

## Vulnerability Title

Insecure Context Management

### Overview


The vulnerability in this report is due to the lack of explicit access control when using CpiContextAccount in invoke_cpi. In the code, CpiContextAccount is used to hold or manage context information for cross-program invocation (CPI). However, there are no specific checks or restrictions on who can modify or access this CpiContextAccount. This lack of control can be exploited by injecting a different proof during the utilization of CpiContextAccount, especially when the context settings span multiple transactions and reset the context account, removing the unused invoke inputs. To fix this issue, strict access control mechanisms need to be implemented to ensure that only authorized entities can modify or interact with CpiContextAccount. This vulnerability has been resolved in patch 0e0fec6. © 2024 Otter Audits LLC. All Rights Reserved.

### Original Finding Content

## Vulnerability Overview

The vulnerability stems from the lack of explicit access control when utilizing `CpiContextAccount` in `invoke_cpi`. In `InvokeCpiInstruction`, `CpiContextAccount` is meant to hold or manage context information required for cross-program invocation (CPI). However, there are no specific checks or restrictions on who may modify or access this `CpiContextAccount`. 

This lack of control may be exploited by injecting a different proof during the utilization of `CpiContextAccount`, especially when the context settings span multiple transactions instead of one transaction, resetting the context account and removing the unutilized invoke inputs.

## Remediation

Implement strict access control mechanisms to ensure that only authorized entities may modify or interact with `CpiContextAccount`.

## Patch

Resolved in `0e0fec6`.

© 2024 Otter Audits LLC. All Rights Reserved. 23 / 53

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Light Protocol |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Tuyết Dương |

### Source Links

- **Source**: https://lightprotocol.com/
- **GitHub**: https://github.com/Lightprotocol
- **Contest**: https://lightprotocol.com/

### Keywords for Search

`vulnerability`

