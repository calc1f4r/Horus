---
# Core Classification
protocol: Soonaverse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20971
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-04-06-Soonaverse.md
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

It's not guaranteed that users will receive the rewards

### Overview


This bug report concerns a problem with the Staking contract, which is a type of smart contract used for rewards. The issue is that users must trust the contract owner to add rewards after deployment, and if the user stakes and waits to receive a reward, the owner could simply not add the rewards into the Staking contract. It is recommended to add functionality into the initialize function to validate the rewards sent to the Staking contract and add another function to retrieve not used rewards after the expiring date. This would ensure that users are able to receive their rewards without having to trust the contract owner.

### Original Finding Content

**Description:** 

The users should believe in the contract owner to add the rewards after deployment, if the user stake waiting to receive a reward the owner could simply not add the rewards into the Staking contract.

The owner should send the rewards through initialize function guaranteeing that the user will have the rewards.

**Recommendations:**

 It is recommended to add functionality into initialize to validate the rewards sent to the Staking contract and add another function to retrieve not used rewards after the expiring date.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Soonaverse |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-04-06-Soonaverse.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

