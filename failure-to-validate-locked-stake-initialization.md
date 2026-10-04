---
# Core Classification
protocol: Adrena
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46800
audit_firm: OtterSec
contest_link: https://www.adrena.xyz/
source_link: https://www.adrena.xyz/
github_link: https://github.com/AdrenaDEX/adrena

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
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Failure To Validate Locked Stake Initialization

### Overview


The bug report discusses an issue with the finalize_locked_stake function, where an empty slot from the locked_stakes vector is retrieved as a valid LockedStake. This is due to the function passing through preliminary checks, despite the slot being uninitialized. The suggested solution is to check if the locked stake has been initialized before finalizing it. The issue has been resolved in a recent patch.

### Original Finding Content

## Documentation on finalize_locked_stake

In `finalize_locked_stake`, when `params.thread_id` is zero, it retrieves the first element of the `locked_stakes` vector via `iter_mut().find()`. Consequently, an empty slot from the `locked_stakes` vector is fetched as a valid `LockedStake`. Despite being uninitialized, the function will still pass through the preliminary checks (`params.early_exit` and stake ending checks), and `locked_stake.resolved` will be set to true, resulting in an invalid state of the `locked_stakes` vector.

## Remediation

Check whether the locked stake has been initialized in `finalize_locked_stake`.

## Patch

Resolved in commit `9db44d`.

© 2024 Otter Audits LLC. All Rights Reserved. 32/59

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Adrena |
| Report Date | N/A |
| Finders | Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://www.adrena.xyz/
- **GitHub**: https://github.com/AdrenaDEX/adrena
- **Contest**: https://www.adrena.xyz/

### Keywords for Search

`vulnerability`

