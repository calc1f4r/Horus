---
# Core Classification
protocol: aragonOS
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50951
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/aragon/aragonos-smart-contract-security-assessment-1
source_link: https://www.halborn.com/audits/aragon/aragonos-smart-contract-security-assessment-1
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
  - Halborn
---

## Vulnerability Title

UNTRUSTED PLUGIN USAGE CAN CAUSE DOS

### Overview


This bug report discusses an issue that can occur when installing or upgrading a plugin on a platform. If the plugin self-destructs during the process, it can cause the contract and DAO to become nonfunctional. This can also happen if the implementation contract is not properly validated. The impact of this bug is rated as a 5 out of 10, with a likelihood of 1 out of 10. The recommendation is to use the new `_disableInitializers` feature implemented by the Aragon team to prevent any issues during initialization or take-over. This issue has been solved by the team.

### Original Finding Content

##### Description

Installing or upgrading a plugin without prior validation can lead to the contract and DAO being nonfunctional. This is possible if a plugin does self-destruct during the installation or upgrade. Furthermore, not only caution should be taken during the installation/upgradability but also on the deployed implementation contract as it would lead all proxied contracts to be unusable.

##### Score

Impact: 5  
Likelihood: 1

##### Recommendation

**SOLVED**: The `Aragon team` added `_disableInitializers` and stated that no action could happen due to a bad implementation initialization or take-over.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | aragonOS |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/aragon/aragonos-smart-contract-security-assessment-1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/aragon/aragonos-smart-contract-security-assessment-1

### Keywords for Search

`vulnerability`

