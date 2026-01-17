---
# Core Classification
protocol: Compound Finance – Timelock Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11770
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-finance-patch-audit/
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Malicious pauseGuardian can prevent their replacement

### Overview


This bug report is about the difficulty an honest Comptroller admin may face when trying to replace a malicious/compromised pauseGuardian. To replace the current pauseGuardian, the Comptroller admin must call `_setPendingPauseGuardian` and pass in a new, honest pauseGuardian address. Then, the new, honest pauseGuardian must call `_acceptPauseGuardian`. However, if the current, malicious pauseGuardian can call `_setPendingPauseGuardian` before the honest pauseGuardian calls `_acceptPauseGuardian`, the malicious pauseGuardian will maintain control of the role. 

Although the admin can use a contract to call both `_setPendingPauseGuardian` and `_acceptPauseGuardian` in a single transaction, it is non-trivial. To resolve the issue, the compound team replaced `_setPendingPauseGuardian` and `_acceptPauseGuardian` with a single function, `_setPauseGuardian`, which allows only the admin to transfer the role of pauseGuardian to a different address.

### Original Finding Content

An honest Comptroller admin may find it difficult to replace a malicious/compromised pauseGuardian. To replace the current pauseGuardian, the Comptroller admin must first call [`_setPendingPauseGuardian`](https://github.com/compound-finance/compound-protocol/blob/f244c2270f905287cb731d8fd3693ac77f8404f9/contracts/Comptroller.sol#L979), passing in a new, honest pauseGuardian address. Then, the new, honest pauseGuardian must call [`_acceptPauseGuardian`](https://github.com/compound-finance/compound-protocol/blob/f244c2270f905287cb731d8fd3693ac77f8404f9/contracts/Comptroller.sol#L996).


If the current, malicious pauseGuardian can call `_setPendingPauseGuardian` (passing in any address they control) *after* the Comptroller admin calls `_setPendingPauseGuardian` and *before* the honest pauseGuardian calls `_acceptPauseGuardian`, then the malicious pauseGuardian maintains control of the role. In other words, once the Comptroller admin calls `_setPendingPauseGuardian`, there exists a race between the new, honest `pendingPauseGuardian` and the existing, malicious pauseGuardian to determine who gets the pauseGuardian role moving forward.


The admin can use a contract to call both `_setPendingPauseGuardian` and `_acceptPauseGuardian` in a single transaction, but that would be non-trivial.


If a malicious/compromised pauseGuardian is within the threat model, consider removing the pauseGuardian’s ability to change the `pendingPauseGuardian` address. Alternatively, consider replacing the offer/accept pattern with an admin-only function that directly sets the `pauseGuardian` address.


**Update:** *The compound team has resolved this issue by replacing `_setPendingPauseGuardian` and `_acceptPauseGuardian` with a single function, [`_setPauseGuardian`](https://github.com/compound-finance/compound-protocol/blob/681833a557a282fba5441b7d49edb05153bb28ec/contracts/Comptroller.sol#L981-L996), which allows only the admin to transfer the role of pauseGuardian to a different address.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Finance – Timelock Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-finance-patch-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

