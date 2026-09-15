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
solodit_id: 32713
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

Inconsistencies When Adding a New Collateral Type

### Overview


The `initializeIlk` function in the `IonPool` contract allows for adding a new type of collateral. However, there are some features that need to be completed before the new collateral type is fully supported. These include initializing the spot oracle, debt ceiling, dust limit, interest rate module, and whitelist. To make this process safer and easier, it is recommended to combine all initialization steps into one function or make it atomic. The Ion Protocol team has acknowledged this issue and plans to resolve it by using Gnosis Multisend for atomic initialization.

### Original Finding Content

The [`initializeIlk` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L190) of the `IonPool` contract allows for adding a new collateral type. This function only includes features to partially support the addition of a new collateral type and calls to additional functions are expected to occur before the new collateral type is fully supported. Specifically:


* The spot oracle must be initialized using the [`updateIlkSpot` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L215).
* The debt ceiling must be initialized using the [`updateIlkDebtCeiling` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L231).
* The dust limit must be initialized using the [`updateIlkDust` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L248).
* The interest rate module must be updated with an instance that supports the new collateral type using the [`updateInterestRateModule` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L277).
* The whitelist must be updated with an instance that supports the new collateral type using the [`updateWhitelist` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L295). The current implementation of the `Whitelist` contract would default to allowing anyone to borrow against the new collateral type.


To minimize the attack surface and ensure adding new collateral types is less error-prone, consider consolidating all of the initialization logic into a single function, or making the initialization procedure otherwise atomic.


***Update:** Acknowledged, will resolve. Ion Protocol team stated:*



> *Initialization procedure for adding new collateral types will be done atomically through Gnosis Multisend.*

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

