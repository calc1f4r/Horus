---
# Core Classification
protocol: Mozaic Archimedes
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18998
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
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
  - Trust Security
---

## Vulnerability Title

TRST-M-2 Multisig could become permanently locked

### Overview


This bug report is about the Senate's ability to remove council members and adjust the threshold for quorum using the TYPE_ADJ_THRESHOLD proposal type. The issue is that there is an important security validation missing, which is that the new council member count and threshold number allow future proposals to pass. The team proposed a mitigation by verifying that councilMembers.length is greater than or equal to the threshold after the proposal is executed. The team then fixed the issue and the TYPE_ADJ_THRESHOLD proposal now checks if the new threshold is safe. However, this check is not done during owner removal.

### Original Finding Content

**Description:**
As described, the senate can remove council members. It can also adjust the threshold for 
quorum using the **TYPE_ADJ_THRESHOLD** proposal type. Both remove and adjust operations 
do not perform an important security validation, that the new council member count and 
threshold number allow future proposal to pass.

**Recommended Mitigation:**
Verify that **councilMembers.length >= threshold**, after execution of the proposal.

**Team Response:**
Fixed.

**Mitigation review:**
The TYPE_ADJ_THRESHOLD proposal now checks the new threshold is safe. However it is not 
checked during owner removal.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Mozaic Archimedes |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

