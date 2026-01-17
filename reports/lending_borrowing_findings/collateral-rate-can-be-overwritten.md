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
solodit_id: 32709
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

Collateral Rate Can Be Overwritten

### Overview


The `IonPool` contract has a bug where the `rate` stored for a collateral type can be overwritten using the `initializeIlk` function. This can happen if there are 256 or more collateral types initialized. When this occurs, the `rate` for the first 256 collateral types in the `ilks` array will be overwritten. This can lead to a decrease in outstanding debt for all debt positions against the affected collateral type, causing the contract to be in an inconsistent state. To fix this, the length of the `ilks` array should be checked to ensure it is 256 or less after new data is pushed in the `initializeIlk` function. This issue has been resolved in a recent pull request.

### Original Finding Content

Within the `IonPool` contract, the [`rate` stored for a collateral type](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L113) can be overwritten using the `initializeIlk` function. If 256 or more collateral types have been initialized, subsequent calls to `initializeIlk` will [overwrite the rates](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L203) within the first 256 indices in the `ilks` array.


Overwriting the `rate` for one of the collateral types would immediately decrease the outstanding debt for all debt positions against the collateral type as the `rate` tracks the accumulated interest on debt. As a result, the contract would be in an inconsistent state where the outstanding debt for the collateral type would be less than what lenders are owed.


Consider explicitly validating that the length of the `ilks` array is 256 or less after pushing the new ilk data within the `initializeIlk` function.


***Update:** Resolved in [pull request #26](https://github.com/Ion-Protocol/ion-protocol/pull/26).*

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

