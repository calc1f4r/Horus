---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55412
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Multi%20Scope/README.md#1-unvalidated-cross-chain-request-parameters-in-requestoracle
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
  - MixBytes
---

## Vulnerability Title

Unvalidated Cross-Chain Request Parameters in RequestOracle

### Overview


The audit found that the `request` function in the `RequestOracle` contract has several security vulnerabilities. These include a lack of checks to validate certain inputs, which could lead to users sending requests to non-existing chains and unnecessary network load. Additionally, the variables `_mailbox` and `_messageBody` can be controlled by users, increasing the risk of unauthorized actions. The severity of these issues is classified as medium due to the potential for system manipulation and data loss. To address these concerns, it is recommended to implement a whitelist function, use a trusted mailbox instead of user-provided ones, and add robust checks for the message body. A whitelisting mechanism should also be put in place to prevent unauthorized operations and ensure that only approved domains and receivers can initiate requests.

### Original Finding Content

##### Description
The audit identified multiple security vulnerabilities in the `request` function of the `RequestOracle` contract:

Lack of Whitelisting: 
   - No checks in place to validate `_destinationDomain` and `receiver`
   - Potential for users to send requests to non-existing chains
   - Risk of unnecessary network load

Mailbox and Message Body Exposure:
   - `_mailbox` and `_messageBody` variables can be controlled by users
   - Possibility of calling `dispatch` method on an unofficial contract

The issues are classified as **Medium** severity due to the potential for system manipulation and unintended operations that could lead to data loss.

##### Recommendation
We recommend implementing the following security measures:
- Add a whitelist function to validate `_destinationDomain` and `receiver`
- Utilize `trustedMailBox` instead of user-provided `_mailbox`
- Implement robust sanity checks for `_messageBody`
- Create a whitelisting mechanism to prevent unauthorized operations
- Ensure only approved domains and receivers can initiate requests

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Multi%20Scope/README.md#1-unvalidated-cross-chain-request-parameters-in-requestoracle
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

