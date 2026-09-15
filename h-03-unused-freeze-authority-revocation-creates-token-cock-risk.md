---
# Core Classification
protocol: PumpScience_2024-12-24
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45119
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/PumpScience-security-review_2024-12-24.md
github_link: none

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

protocol_categories:
  - derivatives

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-03] Unused freeze authority revocation creates token cock risk

### Overview


A function in the codebase called `revoke_freeze_authority` is not being used when creating a pool, which can cause issues with token freezing after migration. This can give the program the ability to lock user tokens, which goes against the intended design. It is recommended to add the freeze authority revocation call to prevent this issue. 

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The codebase includes a `revoke_freeze_authority` function in `locker.rs` that is not being called during pool creation, despite being necessary to prevent tokens from being frozen after migration.

If the freeze authority is not revoked:

- The bonding curve program retains the ability to freeze token accounts
- This could potentially be used to lock user tokens after migration
- Goes against the intended design where locking should only be possible during pre-trading

**Code Location :** [locker.rs#L83](https://github.com/moleculeprotocol/pump-science-contract/blob/54daf1b93cf6abf955c69f043f73b4df671f97f7/programs/pump-science/src/state/bonding_curve/locker.rs#L83)

## Recommendations

It's recommended that the freeze authority revocation call be added.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | PumpScience_2024-12-24 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/PumpScience-security-review_2024-12-24.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

