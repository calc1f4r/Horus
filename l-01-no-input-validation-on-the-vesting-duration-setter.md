---
# Core Classification
protocol: Pump
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31410
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-11-01-Pump.md
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
  - Pashov
---

## Vulnerability Title

[L-01] No input validation on the vesting duration setter

### Overview

See description below for full details.

### Original Finding Content

The `setVestingDuration` method in `PumpV1` has no input validation, meaning it allows the protocol owner to set any value as `vestingDuration`. There are two potential problems with this - using the value of 0, which would lead to DoS of the protocol, because division by zero reverts the transaction, and using a too big of a value which would make the vesting rate of a user to be 0. Implement lower and upper bounds for the `vestingDuration` value.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Pump |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-11-01-Pump.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

