---
# Core Classification
protocol: Tortugal TIP
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48029
audit_firm: OtterSec
contest_link: https://tortuga.finance/
source_link: https://tortuga.finance/
github_link: https://github.com/MoveLabsXYZ/liquid-staking-ottersec

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
finders_count: 3
finders:
  - OtterSec
  - Harrison Green
  - Fineas Silaghi
---

## Vulnerability Title

Potential Denial Of Service In Pool

### Overview


The delegation_service has a limit on the number of direct delegators a pool can have, currently set at 100. However, a malicious user can exploit this by filling the list with fake delegators, preventing real delegators from staking. This can be combined with another issue, OS-TOR-PRO-01, to bypass the minimum delegation amount and leave small amounts in the pool, creating a free exploit. To fix this, it is recommended to allow all delegators to stake and implement a minimum delegation amount to ensure meaningful contributions. The issue has been fixed in version af0d61f. 

### Original Finding Content

## Delegation Service Vulnerability

In `delegation_service`, there is a hard limit on the number of direct delegators a pool may have:  
**MAX_NUMBER_OF_DELEGATIONS**, which currently equals **100**. 

A malicious user may fill the delegator list with fake delegators, staking small amounts to prevent real delegators from staking. In conjunction with **OS-TOR-PRO-01**, an attacker may bypass the `min_delegation_amount` and leave dust amounts in the pool, effectively making a free exploit.

## Remediation

Ensure that all delegators wishing to stake may stake to maximize efficiency for the validators. A `min_delegation_amount` imposed for the lifetime of the delegator’s funds helps ensure that all delegators are meaningfully contributing to the validator’s total stake. Consider implementing a fix for **OS-TOR-PRO-01** with this issue in mind.

## Patch

Fixed in **af0d61f**.

© 2023 OtterSec LLC. All Rights Reserved. 9 / 24

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tortugal TIP |
| Report Date | N/A |
| Finders | OtterSec, Harrison Green, Fineas Silaghi |

### Source Links

- **Source**: https://tortuga.finance/
- **GitHub**: https://github.com/MoveLabsXYZ/liquid-staking-ottersec
- **Contest**: https://tortuga.finance/

### Keywords for Search

`vulnerability`

