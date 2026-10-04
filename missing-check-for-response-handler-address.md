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
solodit_id: 51884
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

Missing Check for Response Handler Address

### Overview


The `BaseBlueprint` contract has a function called `_getReponseTemplate` that retrieves a response handler address from storage. However, there is no check to ensure that the address is valid, which could lead to unexpected behavior or failure to process messages. The recommendation is to add a check to ensure the address is not set to `0x0` and the issue has been solved by the Concrete team.

### Original Finding Content

##### Description

In the `BaseBlueprint` contract, the `_getReponseTemplate` function is responsible for fetching the response handler address from storage. This address is used when sending a cross-chain messaging (CCCM) response. However, there is no validation to ensure that the address retrieved from storage is not the zero address (`0x0`). If an invalid or uninitialized address is used, it can result in the CCCM message failing to find a valid handler, leading to unexpected behavior or failure to process the message.

Failure to check the validity of this address could result in invalid messages being sent with no recipient to handle them. This could disrupt the protocol's cross-chain operations, particularly when expecting a response from another chain.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:C/A:N/D:N/Y:N/R:P/S:C (6.3)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:C/A:N/D:N/Y:N/R:P/S:C)

##### Recommendation

Add a check in the `_getReponseTemplate` function to ensure that the response handler address is valid and not set to `0x0`. If the address is invalid, revert the transaction to prevent sending a faulty CCCM message.

##### Remediation

**SOLVED**: The **Concrete team** solved the issue by adding an if condition to revert if the returned address is zero.

##### Remediation Hash

26faabb856f98d774ddbe689f6ee2327d0c538f5

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

