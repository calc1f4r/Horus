---
# Core Classification
protocol: Tortuga
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48536
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

Potential DOS in delegation_service Pool

### Overview


The report discusses a bug in a service called delegation_service, where there is a limit on the number of direct delegators a pool can have. This limit can be exploited by a malicious user who can fill the list with fake delegators, preventing real delegators from staking. This can be combined with another vulnerability to bypass a minimum delegation amount and leave small amounts of funds in the pool, making the attack free. To solve this issue, it is suggested to impose a minimum delegation amount for the lifetime of the delegator's funds to ensure that all delegators are contributing meaningfully. A fix for this bug has been implemented in a recent patch.

### Original Finding Content

## Delegation Service Vulnerability

In `delegation_service`, there is a hard limit on the number of direct delegators a pool can have:  
**MAX_NUMBER_OF_DELEGATIONS** (currently 100).  

A malicious user could fill the delegator list with fake delegators, staking small amounts in order to prevent real delegators from staking. In conjunction with OS-TOR-ADV-00, an attacker could bypass the `min_delegation_amount` and leave dust amounts in the pool, effectively making this attack free.

## Remediation

In order to maximize efficiency for the validators, it is important to ensure that all delegators that wish to stake are able to. A `min_delegation_amount` imposed for the lifetime of the delegator’s funds could help ensure that all delegators are actually contributing to the validator’s total stake in a meaningful way. Consider implementing a fix for OS-TOR-ADV-00 with this issue in mind.

## Patch

Fixed in **af0d61f**.

© 2022 OtterSec LLC. All Rights Reserved. 9 / 19

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tortuga |
| Report Date | N/A |
| Finders | OtterSec, Harrison Green, Fineas Silaghi |

### Source Links

- **Source**: https://tortuga.finance/
- **GitHub**: https://github.com/MoveLabsXYZ/liquid-staking-ottersec
- **Contest**: https://tortuga.finance/

### Keywords for Search

`vulnerability`

