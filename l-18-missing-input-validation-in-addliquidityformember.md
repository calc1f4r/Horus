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
solodit_id: 4130
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/225

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

[L-18] Missing input validation in addLiquidityForMember()

### Overview

See description below for full details.

### Original Finding Content

## Handle

0xsanson


## Vulnerability details

## Impact
In Router.sol, the function addLiquidityForMember() doesn't check inputBase and inputToken. Since we know they can't both be zero (it wouldn't change anything and user pays the gas for nothing).

## Proof of Concept
https://github.com/code-423n4/2021-07-spartan/blob/main/contracts/Router.sol#L51

## Tools Used
editor

## Recommended Mitigation Steps
Consider adding a require `inputBase>0 || inputToken>0`.

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
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/225
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`vulnerability`

