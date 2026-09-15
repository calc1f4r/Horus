---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 641
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-08-yield-micro-contest-1
source_link: https://code4rena.com/reports/2021-08-yield
github_link: https://github.com/code-423n4/2021-08-yield-findings/issues/49

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
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xRajeev
---

## Vulnerability Title

[L-03] Missing input validation to check that end > start

### Overview

See description below for full details.

### Original Finding Content

## Handle

0xRajeev


## Vulnerability details

## Impact

setRewards() is missing input validation on parameters start and end to check if end > start. If accidentally set incorrectly, this will allow resetting new rewards while there is an ongoing one.


## Proof of Concept

https://github.com/code-423n4/2021-08-yield/blob/4dc46470e616dd0cbd9db9b4742e36c4d809e02c/contracts/utils/token/ERC20Rewards.sol#L74-L88

## Tools Used

Manual Analysis

## Recommended Mitigation Steps

Add a require() to check that end > start.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | 0xRajeev |

### Source Links

- **Source**: https://code4rena.com/reports/2021-08-yield
- **GitHub**: https://github.com/code-423n4/2021-08-yield-findings/issues/49
- **Contest**: https://code4rena.com/contests/2021-08-yield-micro-contest-1

### Keywords for Search

`vulnerability`

