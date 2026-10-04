---
# Core Classification
protocol: Sophon Farming Program
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59240
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/sophon-farming-program/716f553c-5a5f-4faa-a3cc-a426f664c009/index.html
source_link: https://certificate.quantstamp.com/full/sophon-farming-program/716f553c-5a5f-4faa-a3cc-a426f664c009/index.html
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
finders_count: 2
finders:
  - Julio Aguilar
  - Ruben Koch
---

## Vulnerability Title

Missing Input Validation Could Cause Reverts

### Overview


The client has marked a bug as "Fixed" in the `SophonFarming.sol` file. The bug was related to the `boosterMultiplier` and `pointsPerBlock` variables, which could be set to very large values and cause problems with block withdrawals. This could also break pools and cause issues with rewards. Additionally, there is a lack of input validation for the zero address in owner-controlled functions. It is recommended to add input validation to prevent these issues in the future.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. An upper limit of `10001e18` for `pointsPerBlock` and `10e18` for `boosterMultiplier` has been added. Addressed in: `639e80bc9ca94c085a41be8001336a094e58b82b`.

**File(s) affected:**`SophonFarming.sol`

**Description:** Technically, the `boosterMultiplier` and `pointsPerBlock` are unbounded `uint256` and can therefore be set to arbitrary values. They can be configured in a way to cause integer overflows and deny block withdrawals. They may break pools indefinitely, if pools have rewards settled with a number close to `uint256.max`, causing subsequent accounting to overflow in the process.

Furthermore, most of the address-inputs from owner-controlled functions are unchecked for the zero address.

**Recommendation:** Consider adding reasonable input validation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Sophon Farming Program |
| Report Date | N/A |
| Finders | Julio Aguilar, Ruben Koch |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/sophon-farming-program/716f553c-5a5f-4faa-a3cc-a426f664c009/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/sophon-farming-program/716f553c-5a5f-4faa-a3cc-a426f664c009/index.html

### Keywords for Search

`vulnerability`

