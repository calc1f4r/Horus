---
# Core Classification
protocol: Aurorafastbridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21068
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
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
  - AuditOne
---

## Vulnerability Title

Redis db connection issue - Relayer fund loss Severity: Medium

### Overview


This bug report is about an issue with the fast bridge where a user was trying to get a token on the Ethereum (ETH) blockchain. The relayer, which is responsible for executing transactions on ETH, was unable to make an entry in Redis due to a redis issue. This caused the relayer to be unaware that the transaction had been made and therefore unable to issue an lp_unlock on the near side. After the bridge request expired, the user was able to unlock the token on both sides (ETH and near). The bug was resolved by reverting the transaction if a redis connection issue was present.

### Original Finding Content

**Description:**

User A use fast bridge to get token on ETH

Relayer executes the transaction on ETH but due to redis issue, the PENDING\_TRANSACTIONS entry could not be made in Redis

This causes Relayer to be unaware about this issue and Relayer now wont issue lp\_unlock on near side

After bridge request expire user can unlock the token. This means user gets both token on eth and near side

**Recommendations:**

 Revert if redis connection issue is present Status: Resolved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Aurorafastbridge |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

