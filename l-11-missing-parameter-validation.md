---
# Core Classification
protocol: Gro Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 426
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-gro-protocol-contest
source_link: https://code4rena.com/reports/2021-06-gro
github_link: https://github.com/code-423n4/2021-06-gro-findings/issues/90

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cmichel
  - 0xRajeev
---

## Vulnerability Title

[L-11] Missing parameter validation

### Overview

See description below for full details.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

## Vulnerability Details
Some parameters of functions are not checked for invalid values:
- `BaseVaultAdaptor.constructor`: The addresses should be checked for non-zero values
- `LifeGuard3Pool.constructor`: The addresses should be checked for non-zero values
- `Buoy3Pool.constructor`: The addresses should be checked for non-zero values
- `PnL.constructor`: The addresses should be checked for non-zero values
- `Controllable.setController`: Does not check that `newController != controller`

## Impact
A wrong user input or wallets defaulting to the zero addresses for a missing input can lead to the contract needing to redeploy or wasted gas.

## Recommended Mitigation Steps
Validate the parameters.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gro Protocol |
| Report Date | N/A |
| Finders | cmichel, 0xRajeev |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-gro
- **GitHub**: https://github.com/code-423n4/2021-06-gro-findings/issues/90
- **Contest**: https://code4rena.com/contests/2021-07-gro-protocol-contest

### Keywords for Search

`vulnerability`

