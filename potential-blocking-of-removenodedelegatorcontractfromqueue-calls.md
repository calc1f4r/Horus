---
# Core Classification
protocol: KelpDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30474
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#1-potential-blocking-of-removenodedelegatorcontractfromqueue-calls
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

Potential blocking of `removeNodeDelegatorContractFromQueue` calls

### Overview


The bug report is about a problem found in a function called `LRTDepositPool.removeNodeDelegatorContractFromQueue`. This function has a step that checks if the `NodeDelegator` being removed has a zero balance. However, this step can be manipulated by an external party, causing the removal process to fail. This is considered a `medium` risk because it could potentially block the removal process until the admin manually fixes it. The recommendation is to pull the tokens from the `NodeDelegator` during the removal process to prevent this issue.

### Original Finding Content

##### Description
The issue is found in the [`LRTDepositPool.removeNodeDelegatorContractFromQueue`](https://github.com/Kelp-DAO/KelpDAO-contracts/blob/8c62af6057402f4616cc2a1d3218a277a864ee2c/contracts/LRTDepositPool.sol#L263) function.

This function incorporates an internal verification to ensure the `NodeDelegator` expected to be removed has a zero balance. However, this process opens up the possibility of the manipulation through front-running, where an external party can send 1 wei of token to that `NodeDelegator`, thereby reverting the execution of the removal process. 

This vulnerability is classified as `medium` as it poses a risk to potentially blocking the removal process until admin updates the proxy implementation.

##### Recommendation
We recommend pulling the tokens from the `NodeDelegator` at the time of removal.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | KelpDAO |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#1-potential-blocking-of-removenodedelegatorcontractfromqueue-calls
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

