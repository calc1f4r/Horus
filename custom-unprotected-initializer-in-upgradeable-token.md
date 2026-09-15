---
# Core Classification
protocol: Taunt Token
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57658
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-11-15-Taunt Token.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - zokyo
---

## Vulnerability Title

Custom unprotected initializer in upgradeable token.

### Overview


The token's upgrade feature uses a custom initializer instead of the recommended initializer, which could potentially lead to security vulnerabilities. Additionally, there are no deployment scripts available to ensure the proper deployment and initialization of the contract. It is recommended that the team provide these scripts for auditors to verify the correctness of the deployment and initialization process. After a re-audit, it has been confirmed that the Taunt team has provided the necessary deployment script to address this issue.

### Original Finding Content

**Description**

Being upgrabeable, the token utilizes the init() custom initializer and not the recommended, more common initialize()) with no restrictions for admins-only calls. This fact and the absence of deployment scripts makes it impossible to verify if the contract's proxy will be deployed and initialized properly. Thus, it is open to a set of possible exploits.

**Recommendation**

Provide deployment scripts/procedures so that the team of auditors can verify the correctness of Proxy deployment and contract initialization.

**Re-audit comment**

Verified.

Post-audit:

The Taunt team has provided the deployment script with the correct way of utilizing the custom initializer.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Taunt Token |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-11-15-Taunt Token.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

