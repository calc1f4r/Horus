---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17894
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
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
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Ether can be deposited into CurveAMO_V3 but not retrieved from it

### Overview

See description below for full details.

### Original Finding Content

## Patching Report

**Type:** Patching  
**Target:** contracts/library/*  

**Difficulty:** Low  

## Description  
The `CurveAMO_V3` contract has a payable `initialize()` function but lacks a function for withdrawing the funds. This issue is somewhat mitigated, however, by the fact that the Curve AMO contract operates by delegating withdrawals to a proxy capable of extracting funds.

```solidity
function initialize(
    address _frax_contract_address,
    address _fxs_contract_address,
    address _collateral_address,
    address _creator_address,
    address _custodian_address,
    address _timelock_address,
    address _frax3crv_metapool_address,
    address _three_pool_address,
    address _three_pool_token_address,
    address _pool_address
) public payable initializer {
```
_Figure 14.1: contracts/Curve/CurveAMO_V3.sol#L109-L120_

## Exploit Scenario  
Alice, a member of the Frax Finance team, calls `initialize()` with ETH and is subsequently unable to directly retrieve the transferred funds from the contract.

## Recommendations  
**Short term:** Either remove the `payable` keyword from the `initialize()` function or document why a payable initialize function is necessary.  
**Long term:** Use static analysis tools like Slither to detect structural issues such as contracts with non-retrievable funds.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | Travis Moore | Frax Finance travis@frax.ﬁnance Spencer Michaels, Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxFinance.pdf

### Keywords for Search

`vulnerability`

