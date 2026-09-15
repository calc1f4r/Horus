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
solodit_id: 52409
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dexodus/dexodusv2
source_link: https://www.halborn.com/audits/dexodus/dexodusv2
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

Missing Parameter Validation in Public Modify Position Function

### Overview

See description below for full details.

### Original Finding Content

##### Description

The public `modifyPosition` function does not validate its input parameters, such as ensuring `slippage` is less than `10000` or checking other parameter ranges for validity.

Without proper validation in the public function, invalid parameters may pass through and require Chainlink automation to handle them. This results in unnecessary automation triggers, only for the transaction to eventually revert due to invalid inputs, wasting gas and resources.

Additionally, the lack of validation in the public function means that automations rely on redundant checks inside internal functions, which could be skipped if parameters were pre-validated.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:L/D:N/Y:N/R:F/S:C (1.8)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:L/D:N/Y:N/R:F/S:C)

##### Recommendation

Validate all parameters in the public `modifyPosition` function to ensure they are within acceptable ranges before any further processing.

By enforcing these checks early, invalid transactions are filtered out without triggering automation, improving efficiency and reducing gas costs. Once validations are implemented in the public function, redundant checks inside automation handler functions can be safely removed.

##### Remediation

**ACKNOWLEDGED:** The **Dexodus team** acknowledged this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

