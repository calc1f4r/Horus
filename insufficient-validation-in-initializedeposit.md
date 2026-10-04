---
# Core Classification
protocol: FCHAIN Validator and Staking Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55351
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fchain-validator-and-staking-contracts-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Insufficient Validation in initializeDeposit

### Overview

See description below for full details.

### Original Finding Content

The [`initializeDeposit` function](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L303-L306) allows deposits of both native tokens and lockups for licenses. However, in the case where [`fNodesTokenIDs` is empty](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L305) and `msg.value == 0`, the function will execute successfully without making any changes to the validator or delegator's stake, thereby, causing unnecessary gas consumption.

Following the "fail early and loudly" principle, consider adding a check for the length of `fNodesTokenIDs` and `msg.value`, reverting with a descriptive error if both of these values are 0.

***Update:** Resolved in [pull request #48](https://github.com/0xFFoundation/fchain-contracts/pull/48).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | FCHAIN Validator and Staking Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fchain-validator-and-staking-contracts-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

