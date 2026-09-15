---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41241
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#19-missing-nonce-increment-in-addnodeoperator-function
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Missing Nonce Increment in `addNodeOperator` Function

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the function [addNodeOperator](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.4.24/nos/NodeOperatorsRegistry.sol#L317-L337) of the contract `NodeOperatorRegistry`. The current implementation does not increment the nonce within the `addNodeOperator` function, which is inconsistent with the behavior in related functions such as `activateNodeOperator` and `deactivateNodeOperator`. Although this omission does not impact the `obtainDepositData` function directly, it may lead to future issues with state tracking.

##### Recommendation
We recommend adding a nonce increment within the `addNodeOperator` function to ensure consistency across the contract and to prevent potential issues related to state tracking.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#19-missing-nonce-increment-in-addnodeoperator-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

