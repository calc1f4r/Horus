---
# Core Classification
protocol: Code Inc.
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53254
audit_firm: OtterSec
contest_link: https://getcode.com/
source_link: https://getcode.com/
github_link: https://github.com/code-payments/code-vm

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
finders_count: 3
finders:
  - Robert Chen
  - Tamta Topuria
  - Nicola Vella
---

## Vulnerability Title

Missing Canonical Bump Validation

### Overview


The process_init_timelock function has a bug where it does not check if the input bump values are correct. This means that the values given by the caller are not checked against the actual values that should be used. This can cause problems because it can result in different addresses being generated than expected. To fix this, the input bumps should be checked against the correct bumps. This bug has been fixed in PR#13.

### Original Finding Content

## Process Initialization Timelock Issue

`process_init_timelock` does not check that the input bumps are canonical. The bump values are taken directly from the caller without validating whether they match the canonical bumps derived programmatically. A canonical bump corresponds to the first valid seed value that may be used to generate a Program Derived Address (PDA). 

By not checking for the canonical bump, discrepancies may arise between the addresses expected by the program and those derived in real time, as the address would resolve to a different PDA than what the canonical calculation would yield.

## Remediation
- Validate that the provided bumps match the canonical bumps.

## Patch
- Resolved in PR#13.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Code Inc. |
| Report Date | N/A |
| Finders | Robert Chen, Tamta Topuria, Nicola Vella |

### Source Links

- **Source**: https://getcode.com/
- **GitHub**: https://github.com/code-payments/code-vm
- **Contest**: https://getcode.com/

### Keywords for Search

`vulnerability`

