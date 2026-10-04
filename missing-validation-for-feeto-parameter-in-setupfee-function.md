---
# Core Classification
protocol: Fabric Labs Zipper Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57064
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-fabriclabs-zipperprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-fabriclabs-zipperprotocol-securityreview.pdf
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
  - Quan Nguyen
---

## Vulnerability Title

Missing validation for feeTo parameter in setupFee function

### Overview

See description below for full details.

### Original Finding Content

## Description
The `setupFee` function lacks validation for the `feeTo` parameter, which could potentially allow setting a zero address as the fee recipient. The contract has two functions for managing fee recipients: `setupFee` for initial configuration and `updateFeeTo` for subsequent changes. The `updateFeeTo` function validates that `feeTo` is not the zero address, indicating that sending fees to the zero address is considered invalid. However, this same validation is missing in the `setupFee` function despite setting the same critical parameter.

This inconsistency creates a security gap during the initial fee setup while preventing the same issue during updates, suggesting an oversight rather than a deliberate design decision.

## Exploit Scenario
An administrator with the `EDITOR_ROLE` accidentally sets the `feeTo` parameter to the zero address when initially configuring fees for a new chain using the `setupFee` function. All fees collected for transactions on that chain are sent to the zero address and become permanently inaccessible.

## Recommendations
- **Short term**: Add the missing validation check to `setupFee` to match the validation in `updateFeeTo`.
- **Long term**: Implement comprehensive test coverage for initialization scenarios. Create test cases that explicitly check for proper validation of critical parameters during initial configuration and ensure consistency between initial setup and update functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Fabric Labs Zipper Protocol |
| Report Date | N/A |
| Finders | Quan Nguyen |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-fabriclabs-zipperprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-fabriclabs-zipperprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

