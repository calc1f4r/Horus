---
# Core Classification
protocol: Tokensfarm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57651
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-28-TokensFarm.md
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
  - zokyo
---

## Vulnerability Title

Possible Denial-of-Service in migration functionality.

### Overview


The bug report is about a function called "migrateUserStakes" in two different files, "Perpetual TokensFarm.sol" and "Perpetual TokensFarmSDK.sol". There is a "require" statement in this function that checks if the user's stake has the correct epoch ID. However, there may be a situation where the user has a stake with a lower epoch ID, causing the migration to be blocked. This was discovered during an audit of the new migration feature. The recommendation is to change the "require" statement to an "if" statement to prevent this issue. The bug has been resolved.

### Original Finding Content

**Description**

Perpetual TokensFarm.sol: function migrateUserStakes(), line 539.
Perpetual TokensFarmSDK.sol: function migrate UserStakes(), line 538.
There is a "require" statement which validates that the epoch ID of the user's stake strictly equals to epochId` - 1. Yet, there might be a case when the user has a stake, whose epoch ID is lower than 'epochId' 1. Thus, migration would be blocked until the user withdraws such a stake. The issue was found during the third iteration of the audit in the newly added migration functionality.

**Recommendation**

Consider changing "require" to "if" so that migration is not blocked in such a scenario.

**Re-audit comment**

Resolved

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tokensfarm |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-28-TokensFarm.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

