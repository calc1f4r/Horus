---
# Core Classification
protocol: Switchboard On-chain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47019
audit_firm: OtterSec
contest_link: https://switchboard.xyz/
source_link: https://switchboard.xyz/
github_link: https://github.com/switchboard-xyz/sbv3

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
  - Akash Gurugunti
  - Robert Chen
---

## Vulnerability Title

Failure To Add Delegation Pool To The Delegation Group

### Overview


This bug report discusses an issue with the delegation pool of an oracle not being linked to its delegation group in the program state. This can prevent the delegation group from advancing epochs and managing epoch-based operations such as reward distribution. The solution is to add the oracle's delegation pool to the delegation group in its queue. The issue has been resolved in patch f3a0733.

### Original Finding Content

## Oracle Delegation Pool Issue

The delegation pool of an Oracle is currently not added to the delegation group of its queue within the program state. The delegation group tracks epochs and is crucial for managing epoch-based operations such as reward distribution. If an Oracle’s delegation pool is not linked to its delegation group, it will prevent the delegation group from advancing epochs as expected. Since epoch advancement is directly tied to reward distribution mechanisms, it also prevents reward distribution in the `OracleHeartbeat` instruction.

## Remediation

Ensure to add the delegation pool of an Oracle to the delegation group of in its queue.

## Patch

Resolved in f3a0733.

© 2024 Otter Audits LLC. All Rights Reserved. 10/39

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Switchboard On-chain |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen |

### Source Links

- **Source**: https://switchboard.xyz/
- **GitHub**: https://github.com/switchboard-xyz/sbv3
- **Contest**: https://switchboard.xyz/

### Keywords for Search

`vulnerability`

