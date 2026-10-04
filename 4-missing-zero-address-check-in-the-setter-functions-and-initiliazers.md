---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25301
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-illuminate
source_link: https://code4rena.com/reports/2022-06-illuminate
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
  - cdp
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[4] Missing zero-address check in the setter functions and initiliazers

### Overview

See description below for full details.

### Original Finding Content


Missing checks for zero-addresses may lead to infunctional protocol, if the variable addresses are updated incorrectly.

### Proof of Concept

Navigate to the following contracts.

https://github.com/code-423n4/2022-06-illuminate/blob/main/marketplace/MarketPlace.sol#L109<br>

https://github.com/code-423n4/2022-06-illuminate/blob/main/marketplace/MarketPlace.sol#L98<br>

https://github.com/code-423n4/2022-06-illuminate/blob/main/lender/Lender.sol#L129<br>

https://github.com/code-423n4/2022-06-illuminate/blob/main/lender/Lender.sol#L137<br>

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
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-illuminate
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-06-illuminate

### Keywords for Search

`vulnerability`

