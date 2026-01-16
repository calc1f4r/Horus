---
# Core Classification
protocol: Heurist
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45795
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-04-Heurist.md
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

Missing Upper Bound on vestPeriod

### Overview


The report discusses a bug in the StHEU contract that allows the contract owner to set an unlimited vesting period for users' tokens. This could lead to centralization and potential loss of liquidity and usability for users. The recommendation is to add a reasonable upper limit to prevent this abuse and ensure users can claim their tokens.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**

In the StHEU contract, the setVestPeriod function allows the contract owner to update the vesting period via setVestPeriod
While the function ensures that newPeriod is non-zero, there is no upper bound on the value that can be set for the vesting period. This lack of an upper bound introduces a centralization risk, where the contract owner could set an unreasonably long vesting period (e.g., 100 years or more), effectively locking users' stHEU tokens indefinitely and preventing them from claiming their HEU tokens.
The absence of an upper limit on the vesting period gives the owner significant control over users' ability to claim tokens. If the owner sets an excessively long vesting period, users may be unable to access their HEU tokens for an extended time, potentially leading to a loss of liquidity and usability.

**Recommendation**: 

Introduce a reasonable upper bound on the vesting period to prevent abuse and ensure that users can eventually claim their tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Heurist |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-04-Heurist.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

