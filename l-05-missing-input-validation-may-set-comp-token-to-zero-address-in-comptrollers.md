---
# Core Classification
protocol: Based Loans
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3999
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-based-loans-contest
source_link: https://code4rena.com/reports/2021-04-basedloans
github_link: https://github.com/code-423n4/2021-04-basedloans-findings/issues/20

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
  - bridge
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-05] Missing input validation may set COMP token to zero-address in Comptroller.sol

### Overview

See description below for full details.

### Original Finding Content

## Handle

0xRajeev


## Vulnerability details

## Impact

Function _setCompAddress() is used by admin to change the COMP token address. However, there is no zero-address validation on the parameter. This may accidentally set COMP token address to zero-address but it can be reset by the admin. Any interim transactions might hit exceptional behavior. 

## Proof of Concept

https://github.com/code-423n4/2021-04-basedloans/blob/5c8bb51a3fdc334ea0a68fd069be092123212020/code/contracts/Comptroller.sol#L1350-L1357


## Tools Used

Manual Analysis

## Recommended Mitigation Steps

Add zero-address check to _comp parameter of _setCompAddress().

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Based Loans |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-basedloans
- **GitHub**: https://github.com/code-423n4/2021-04-basedloans-findings/issues/20
- **Contest**: https://code4rena.com/contests/2021-04-based-loans-contest

### Keywords for Search

`vulnerability`

