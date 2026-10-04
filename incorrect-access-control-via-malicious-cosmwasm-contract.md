---
# Core Classification
protocol: Shido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37653
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Shido.md
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
  - Zokyo
---

## Vulnerability Title

Incorrect Access Control via Malicious `CosmWasm` Contract

### Overview


Severity: Medium
Status: Acknowledged
Description: The system has a problem with how it controls access when using a specific type of contract called CosmWasm through a feature called IBC. 
Impact: This could result in unauthorized access to important information, loss of money, or the creation of unexpected tokens. 
Likelihood: This bug is not very common, but it is possible if someone has the ability to use these specific contracts. 
Recommendation: To fix this issue, update a specific part of the system called "github.com/cosmos/ibc-go/v7/modules/core/keeper" to version 7.4.0 or higher.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**: 

The system is vulnerable to incorrect access control through the deployment and use of a malicious CosmWasm contract via IBC interactions.

**Impact:** 

This could lead to unauthorized access to sensitive data, loss of funds, or unexpected minting of tokens.

**Likelihood:** 

Low to moderate, as it requires the ability to deploy and execute malicious contracts.

**Recommendation**: 

Upgrade github.com/cosmos/ibc-go/v7/modules/core/keeper to version 7.4.0 or higher to address this vulnerability.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Shido |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Shido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

