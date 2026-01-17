---
# Core Classification
protocol: Axelar Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25366
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-07-axelar
source_link: https://code4rena.com/reports/2022-07-axelar
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

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-04] Missing checks for zero address

### Overview

See description below for full details.

### Original Finding Content


Checking addresses against zero-address during initialization or during setting is a security best-practice. However, such checks are missing in address variable initializations/changes in many places.

Impact: Allowing zero-addresses will lead to contract reverts and force redeployments if there are no setters for such address variables.

    https://github.com/code-423n4/2022-07-axelar/blob/9c4c44b94cddbd48b9baae30051a4e13cbe39539/contracts/AxelarGateway.sol#L229
    https://github.com/code-423n4/2022-07-axelar/blob/9c4c44b94cddbd48b9baae30051a4e13cbe39539/contracts/deposit-service/AxelarDepositService.sol#L19



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Axelar Network |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-axelar
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-07-axelar

### Keywords for Search

`vulnerability`

