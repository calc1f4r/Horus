---
# Core Classification
protocol: Mysten Republic Security Token
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46852
audit_firm: OtterSec
contest_link: https://www.mystenlabs.com/
source_link: https://www.mystenlabs.com/
github_link: https://github.com/MystenLabs/security-token

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
  - Michał Bochnak
  - Robert Chen
  - Sangsoo Kang
---

## Vulnerability Title

Risk of Compromising Snapshot Integrity

### Overview


The report discusses a vulnerability related to the process of taking a snapshot. This process relies on accurately counting the total number of tokens and distinguishing between locked and unlocked tokens. However, there is a problem with the "join" function which allows two different tokens to be merged, potentially changing the balance and total supply of tokens during the snapshot. This can cause the total supply to no longer match the sum of unlocked and locked tokens. To fix this issue, a locking mechanism needs to be implemented to prevent the "join" function from being used during the snapshot process. This issue has been resolved in the latest patch, f6fa43b.

### Original Finding Content

## Vulnerability Overview

The vulnerability concerns the integrity of the snapshot process. A successful snapshot relies on accurately capturing the total supply of tokens and distinguishing between those that are counted (unlocked) and those that are not (locked). 

The `join` function allows two different tokens to be merged into one, potentially altering the balances and total supply of tokens mid-snapshot. If tokens that are part of the snapshot join with those that are not, `total_supply` will no longer be equal to `unlocked_sum + locked_sum`.

## Remediation

Employ a locking mechanism to block `shared_token::join` during the snapshot process.

## Patch

Resolved in commit `f6fa43b`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mysten Republic Security Token |
| Report Date | N/A |
| Finders | Michał Bochnak, Robert Chen, Sangsoo Kang |

### Source Links

- **Source**: https://www.mystenlabs.com/
- **GitHub**: https://github.com/MystenLabs/security-token
- **Contest**: https://www.mystenlabs.com/

### Keywords for Search

`vulnerability`

