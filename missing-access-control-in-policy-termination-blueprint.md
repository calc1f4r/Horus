---
# Core Classification
protocol: HUB v1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51880
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/concrete/hub-v1
source_link: https://www.halborn.com/audits/concrete/hub-v1
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

Missing Access Control in Policy termination blueprint

### Overview


This report highlights a vulnerability in the `PolicyTerminationBlueprint` contract that allows anyone to trigger foreclosure or reclamation operations on loans without proper authorization. This can lead to unauthorized access, financial losses, and system inconsistencies. The suggested solutions are to implement access control, restrict the functions to only be callable by the loan owner, or combine both approaches for added security. The issue has been solved by the Concrete team by adding access control.

### Original Finding Content

##### Description

The functions `forecloseLite`, `forecloseBeforeExpiration`, and `reclaimOrForecloseAfterExpiration` in the `PolicyTerminationBlueprint` contract lack any form of access control protection. Without proper access control, any entity can call these functions to trigger foreclosure or reclamation operations on the remote chain for any loan, irrespective of whether they have the authority to do so.

This vulnerability can lead to several critical issues: - Unauthorized users can trigger foreclosure actions on loans they do not own. - Malicious actors could modify loan fee values, triggering unintended consequences across the system. - The protocol could suffer financial losses or inconsistencies by allowing foreclosure operations without proper checks.

Currently, there are no restrictions that limit who can call these functions, which opens up the system to exploitation. These functions should either be protected by access control or restricted to loan owners.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:C/A:C/D:C/Y:C/R:N/S:C (10.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:C/A:C/D:C/Y:C/R:N/S:C)

##### Recommendation

1. **Implement Access Control:** Use role-based access control to limit who can call these sensitive functions. For instance, restricting these functions to be called only by the `BLUEPRINT_CALLER` role.
2. **Restrict to Loan Owner:** Alternatively, the functions should only be callable by the owner of the loan to prevent unauthorized access. This could be achieved by checking the loan ownership before proceeding.
3. **Combining Both Approaches:** The protocol can implement both access control and ownership checks for added security, ensuring only specific roles (like bots) or the loan owner can trigger these actions.

By applying these restrictions, the protocol ensures that only authorized entities can perform sensitive operations, reducing the risk of malicious exploitation and preserving the integrity of the loan management system.

##### Remediation

**SOLVED**: The **Concrete team** solved the issue by adding the access control.

##### Remediation Hash

26faabb856f98d774ddbe689f6ee2327d0c538f5

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | HUB v1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/concrete/hub-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/concrete/hub-v1

### Keywords for Search

`vulnerability`

