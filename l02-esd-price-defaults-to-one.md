---
# Core Classification
protocol: Empty Set V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10917
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/empty-set-v2-audit/
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
  - yield
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L02] ESD price defaults to one

### Overview

See description below for full details.

### Original Finding Content

In the `StabilizerComptroller` contract, whenever the oracle becomes unhealthy, the protocol [sets immediately the `ema` to 1](https://github.com/emptysetsquad/emptyset/blob/bf9753ef9cd5b17236036257f290e0d0b850a029/protocol/contracts/src/stabilizer/StabilizerComptroller.sol#L167).


Whether this choice is intended to protect or stabilize the price of the `ESD` to a fixed price, it is not clear and straightforward why that would be the best mitigation to an unhealthy oracle.


Consider properly justifying this choice or the assumptions that are taken in place whenever the oracle becomes unhealthy.


***Update**: Acknowledged. The EmptySetSquad team statement for this issue:*



> 
> *Expected behavior since a stablecoin’s neutral price is $1.00.*
> 
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Empty Set V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/empty-set-v2-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

