---
# Core Classification
protocol: Evoq
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45923
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-09-Evoq.md
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

Missing Address Validation in Setters

### Overview


This bug report describes an issue in EvoqGovernance.sol where certain governance or admin functions can accidentally set important addresses to the zero address. This can cause problems with the protocol's logic and lead to unexpected failures. The scenario given is when an owner or multisig mistakenly calls setPositionsManager(address(0)), causing subsequent calls to positionsManager to fail. The recommendation is to add a requirement that the new address is not equal to address(0) and to implement a timelock or review process before making changes to critical parameters. The bug has been resolved.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description (Contracts & Functions)**:

EvoqGovernance.sol (e.g., setPositionsManager(), setTreasuryVault(), etc.)
Certain governance or admin functions allow setting critical addresses (like positionsManager, treasuryVault) to the zero address. This breaks protocol logic if a call to address(0) silently no-ops or otherwise fails unexpectedly, yet returns success.

**Scenario:**

An owner or multisig calls setPositionsManager(address(0)) by mistake.
The system’s subsequent calls to positionsManager become calls to address(0), effectively doing nothing or reverting unpredictably.
Operations dependent on positionsManager fail until corrected.

**Recommendation:**

Add require(_newAddress != address(0), "Zero address not allowed") in all setters for critical addresses.
Implement a timelock or thorough review step before finalizing critical parameter changes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Evoq |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2025-01-09-Evoq.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

