---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4119
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/129

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
  - services
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-06] Unnecessary redundant check for basisPoints

### Overview

See description below for full details.

### Original Finding Content

## Handle

0xRajeev


## Vulnerability details

## Impact

The threshold check for basisPoints while a required part of input validation is an unnecessary redundant check because calcPart() does a similar upper bound check and the lower bound check on 0 is only an optimization.

## Proof of Concept

https://github.com/code-423n4/2021-07-spartan/blob/e2555aab44d9760fdd640df9095b7235b70f035e/contracts/Router.sol#L95

https://github.com/code-423n4/2021-07-spartan/blob/e2555aab44d9760fdd640df9095b7235b70f035e/contracts/Utils.sol#L65


## Tools Used

Manual Analysis

## Recommended Mitigation Steps

Remove redundant check to save gas and improve readability/maintainability.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/129
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`vulnerability`

