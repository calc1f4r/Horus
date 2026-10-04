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
solodit_id: 32717
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

Incorrect Interest Accrual When No Debt

### Overview


This bug report discusses an issue with the `_calculateRewardAndDebtDistribution` function in the `IonPool` contract. When there is no debt for a certain type of collateral, the function will return a `0` value for the `timestampIncrease` variable and the `lastRateUpdate` timestamp for that collateral type will remain unchanged. This means that the first user to open a debt position for that collateral type will immediately accrue interest starting from the unchanged `lastRateUpdate` timestamp. This leads to interest being applied on their debt from before their position was opened the next time interest is accrued. The suggested solution is to always increment the `lastRateUpdate` timestamp for each collateral type when interest is accrued, except when the protocol is in a safe pause state. This issue has been resolved in a recent pull request.

### Original Finding Content

When there is no debt for a collateral type, the `_calculateRewardAndDebtDistribution` function in the `IonPool` contract will [return `0` for the `timestampIncrease` value](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L454-L456) and the `lastRateUpdate` timestamp for the `ilk` will be unchanged. As a result, the first user to open a debt position for a collateral type when there is currently no debt against the collateral type will immediately accrue interest starting from the `lastRateUpdate` timestamp for the `ilk`. Since the timestamp was not incremented when [accruing interest](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L567) before their debt position is recorded internally, the user will have interest applied on their debt from before their position was opened the next time interest is accrued.


Consider always incrementing the [`lastRateUpdate` timestamp](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L114) for each `ilk` when interest is accrued regardless of whether there is debt against the collateral type except when the protocol is in a safe pause state.


***Update:** Resolved in [pull request #21](https://github.com/Ion-Protocol/ion-protocol/pull/21).*

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

