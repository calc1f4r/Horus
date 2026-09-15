---
# Core Classification
protocol: Octopus Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52724
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/octopus-network/octopus-network-near-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/octopus-network/octopus-network-near-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

IMPROPER ROLE-BASED ACCESS CONTROL POLICY

### Overview


The report highlights a bug where most of the important features are only accessible by the owner. This goes against the principle of least privilege, which ensures that only authorized users can access certain resources. The bug has been solved by the Octopus Network team by implementing role-based access control, which allows for different levels of authorization.

### Original Finding Content

##### Description

It was observed that most of the privileged functionality is controlled by the `owner`. Additional authorization levels are needed to implement the least privilege principle, also known as least-authority, which ensures only authorized processes, users, or programs can access the necessary resources or information. The ownership role is helpful in a simple system, but more complex projects require more roles by using role-based access control.

Code Location
-------------

The owner can access those functions:

* All functions in `sudo_actions.rs`
* All functions in `registry_settings_actions.rs`
* All functions in `registry_owner_actions.rs` except `count_voting_score`
* `set_owner` in `lib.rs`

##### Score

Impact: 5  
Likelihood: 3

##### Recommendation

**SOLVED**: The `Octopus Network` team solved the issue by adding role based access control functionality..

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Octopus Network |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/octopus-network/octopus-network-near-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/octopus-network/octopus-network-near-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

