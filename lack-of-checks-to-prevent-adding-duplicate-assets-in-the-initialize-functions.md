---
# Core Classification
protocol: Yieldnest
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35548
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-07-YieldNest.md
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
  - Zokyo
---

## Vulnerability Title

Lack Of Checks To Prevent Adding Duplicate Assets in the Initialize() Functions

### Overview


The bug report discusses an issue with the ynLSD contract, which is used to distribute shares to users. Currently, there are no checks in place to prevent duplicate assets from being added when initializing the contract. This can result in a larger value being distributed to users than expected. The recommendation is to add checks for the corresponding EigenLayer Strategy contract or to check if the asset already exists in the assets array. However, the client has decided to acknowledge the issue and leave it as is, as they believe the initialization process is handled by the YieldNest DAO and any duplicate assets would be avoided. 

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**

There exists no checks to prevent adding duplicate assets when attempting to initialize the ynLSD contract. The impact of duplicate assets lies in the totalAssets() function which determines the shares distributed to the users via the deposit() function. This may result in a larger value than expected.

**Recommendation**: 

It’s recommended that the ynLSD contract checks for its corresponding EigenLayer Strategy contract in order to prove existence when reinitializing or check if the asset exists in the assets array although the latter could be quite gas intensive.
Client comment: The decision is to acknowledge and leave this as is. The initialization is performed by the YieldNest DAO at launch time and presence of duplicates would be assumed to be avoided. If the ynLSD contract has duplicate assets it's immediately obvious at initialization time and is considered forfeit.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Yieldnest |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-07-YieldNest.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

