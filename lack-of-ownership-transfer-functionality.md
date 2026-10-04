---
# Core Classification
protocol: Coinlend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20933
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-29-Coinlend.md
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

Lack of Ownership Transfer Functionality

### Overview


A bug report has been submitted concerning the lack of a transferOwnership function in the contract. This function would allow the current owner to transfer ownership to a new address. Without this function, the owner's keys are vulnerable if compromised and there is no way to transfer ownership to a DAO or other governance contract. The report recommends implementing a transferOwnership function that emits an event to record the change of ownership, as well as additional security measures such as a delay or multi-signature requirement for ownership transfers.

### Original Finding Content

**Description:**

 The contract does not provide a way to change the owner of the contract. This is a potential issue because if the owner's keys are compromised, there is no way to transfer ownership to a new address. Additionally, if a governance system is implemented in the future, there is no way to transfer ownership to a DAO or other governance contract.

This is a common feature in many smart contracts and is usually implemented with a transferOwnership function that can only be called by the current owner. The function takes a new owner address as a parameter and sets the owner state variable to this new address.

**Recommendations:**

Implement a transferOwnership function that allows the current owner to transfer ownership to a new address. This function should emit an event to record the change of ownership. Also, consider implementing additional security measures, such as a delay or multi-signature requirement for ownership transfers.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Coinlend |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-29-Coinlend.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

