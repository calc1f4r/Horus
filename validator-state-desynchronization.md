---
# Core Classification
protocol: Jito Steward
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47098
audit_firm: OtterSec
contest_link: https://www.jito.network/
source_link: https://www.jito.network/
github_link: https://github.com/jito-foundation/stakenet

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Kevin Chow
  - Robert Chen
---

## Vulnerability Title

Validator State Desynchronization

### Overview

The bug report describes an issue where removing validators immediately after a successful EpochMaintenance can cause the internal state of the Steward Program to become desynchronized with the external state of the stake pool validator list. This can occur when handling delinquent validators, as they may be removed from the list in the same epoch if there is no transient stake. The problem arises because the validator is marked for deactivation in one epoch but not removed until the next, leading to a discrepancy between the two systems. To address this issue, a mechanism needs to be implemented to flag delinquent validators for immediate removal and halt further progress until they are removed within the same epoch. This bug has been resolved in the 0425db0 patch.

### Original Finding Content

## Issue with Validator Removal and State Desynchronization

Removing validators immediately after a successful `EpochMaintenance` may result in the desynchronization of the internal state of the Steward Program with the external state of the stake pool validator list, particularly when handling delinquent validators. A validator may be removed from the list in the same epoch if there is no transient stake. 

The issue arises because the validator is marked for deactivation in one epoch but is not removed until the next. If the internal state of the Steward Program does not update synchronously with the stake pool’s external state, the Steward may think it still has the validator in its active pool while the stake pool has already removed it, creating a discrepancy between the two systems.

## Proof of Concept
1. `deactivate_delinquent` is called on a validator’s stake account during epoch 1, marking it as delinquent but not immediately removing it from the validator list.
2. `epoch_maintenance` is executed during epoch 2, which performs necessary checks and updates the internal state of the Steward Program.
3. `auto_remove_validator_from_pool` is called during the maintenance process, which attempts to remove the delinquent validator from the pool.
4. The stake pool operations may subsequently execute, which will remove the validator from the validator list, resulting in state desynchronization.

## Remediation
Implement a mechanism to flag delinquent validators for immediate removal, ensuring that the state machine halts further progress until these validators are removed within the same epoch.

## Patch
Resolved in `0425db0`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Jito Steward |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen |

### Source Links

- **Source**: https://www.jito.network/
- **GitHub**: https://github.com/jito-foundation/stakenet
- **Contest**: https://www.jito.network/

### Keywords for Search

`vulnerability`

