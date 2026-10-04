---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28407
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/AAVE/Governance%20Crosschain%20Bridges%20V3/README.md#2-missing-zero-address-check-in-constructor
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

Missing zero address check in constructor

### Overview


This bug report is about a missing validation for a zero address in a line of code. This line of code is in the BridgeExecutorBase.sol file and can be found at https://github.com/aave/governance-crosschain-bridges/blob/9fd0609a2e14d546885f76211961f251d2e15cb9/contracts/BridgeExecutorBase.sol#L44. It is important to validate this address because the contract does not have a tool to change the guardian address.

The recommendation for this bug is to add a zero address validation. This will help ensure that the contract is secure and the guardian address is correct.

### Original Finding Content

##### Description
At the line https://github.com/aave/governance-crosschain-bridges/blob/9fd0609a2e14d546885f76211961f251d2e15cb9/contracts/BridgeExecutorBase.sol#L44
missing validation `_guardian` for zero address. It is important because contract has no tool to change `_guardian`.

##### Recommendation
It is recommended to add zero address validation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/AAVE/Governance%20Crosschain%20Bridges%20V3/README.md#2-missing-zero-address-check-in-constructor
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

