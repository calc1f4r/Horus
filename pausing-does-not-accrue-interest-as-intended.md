---
# Core Classification
protocol: Ion Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32710
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ion-protocol-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Pausing Does Not Accrue Interest as Intended

### Overview


The `pauseSafeActions` function in the `IonPool` contract is not accruing interest when the contract is paused. This is because the internal `_pause` function is called before the `_accrueInterest` function, which does not accrue interest when the contract is in a safe paused state. To fix this, the order of the internal function calls should be switched. This issue has been resolved in pull request #27.

### Original Finding Content

The [`pauseSafeActions` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L332) of the `IonPool` contract is intended to accrue interest when the contract is paused. Within this function, the internal `_pause` function is called first followed by the `_accrueInterest` function. As a result, interest will not be accrued since the [`_accrueInterest` function does not accrue interest when the contract is in a safe paused state](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L376).


Consider switching the order of the internal function calls within `pauseSafeActions`.


***Update:** Resolved in [pull request #27](https://github.com/Ion-Protocol/ion-protocol/pull/27).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ion Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ion-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

