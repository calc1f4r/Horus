---
# Core Classification
protocol: prePO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 23925
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-03-prepo
source_link: https://code4rena.com/reports/2022-03-prepo
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
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-01] Missing zero-address check in constructors and the setter functions

### Overview

See description below for full details.

### Original Finding Content


Missing checks for zero-addresses may lead to infunctional protocol, if the variable addresses are updated incorrectly.

### Proof of Concept

1.  Navigate to the following all contract functions: [PrePOMarket.sol#L44](https://github.com/code-423n4/2022-03-prepo/blob/d62d7146b27fd39a5f1358ffde08766724886cf5/contracts/core/PrePOMarket.sol#L44).

### Recommended Mitigation Steps

Consider adding zero-address checks in the discussed constructors:
require(newAddr != address(0));.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | prePO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-prepo
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-03-prepo

### Keywords for Search

`vulnerability`

