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
solodit_id: 51882
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/concrete/hub-v1
source_link: https://www.halborn.com/audits/concrete/hub-v1
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

Missing Validation for Loan Owner

### Overview


This bug report is about a problem in the `ProtectionBlueprint` contract where the function `enableConcreteLite` does not check if a specific loan exists before sending messages. This could lead to unwanted behavior and potentially compromise the security of the protocol. The report suggests uncommenting or adding validation for the loan, as well as checking if the loan exists in other functions. The Concrete team has accepted the risk and will only check the status of the loan instead of adding extra validation.

### Original Finding Content

##### Description

In the `ProtectionBlueprint` contract, the function `enableConcreteLite` does not validate if the `loanId_Owner` is set before proceeding. This missing validation could result in sending unnecessary cross-chain communication (CCCM) messages, which could impact the integrity of both on-chain and off-chain states. The commented-out lines in the code seem to be intended to perform this validation, but as it stands, the function can potentially send messages even when `loanId_Owner` is not set.

Moreover, several other functions within the contract use a `loanId` parameter but do not check if the associated loan actually exists. This could lead to unwanted behavior, such as attempting to perform operations on non-existent loans, affecting the protocol's state integrity.

These missing validations could open the door to unauthorized access, manipulation of loan-related data, or inconsistencies across the system.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:C/A:L/D:N/Y:N/R:P/S:C (6.6)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:C/A:L/D:N/Y:N/R:P/S:C)

##### Recommendation

1. **Uncomment or add validation for** `loanId_Owner`: Ensure that the `loanId_Owner` is validated before proceeding with any logic that sends CCCM messages or modifies state.
2. **Check if loan exists in other functions:** For any function that takes `loanId` as a parameter, ensure that it checks if the loan exists. This can be done by checking if the loan is set in storage or by validating other key attributes related to the loan.
3. **Avoid sending unnecessary CCCM messages:** Ensure that CCCM messages are only sent when necessary and after proper validation checks. This will avoid unnecessary communication and maintain the integrity of the app chain and any off-chain state.

By enforcing these validations, you can prevent unauthorized loan operations, improve protocol security, and maintain data consistency across the system.

##### Remediation

**RISK ACCEPTED**: The **Concrete team** accepted the risk of this finding. Checking the `concreteLite` status is enough; they do not need to add extra validation. If the loan exists, it should have `concreteLiteInfo`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

