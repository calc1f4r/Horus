---
# Core Classification
protocol: Folks Finance Capital Market Protocol v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21278
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-11-folksfinance-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-11-folksfinance-securityreview.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Vara Prasad Bandaru
  - Josselin Feist
---

## Vulnerability Title

Risk of global state variable collision

### Overview


This bug report is about a potential issue with the loan application's global state which could cause a loan's params variable to collide with a pool variable. The params variable is stored at oﬀset 112 and the pools variable contains an array in which every slot contains 3 loans, and only slots 0–62 are assumed to be used for loans. If the pool's slots are used, there is no guarantee that the global state is being accessed through slots 0–62, which means that slot 112 can be used to store a loan. 

Exploitation of this issue would likely require exploitation of another bug, as the first element of params is an admin address and the first element of a loan variable is the pool application ID. If params collides with a pool variable, its admin address must collide with an application ID.

To address this issue, the short-term recommendation is to store the params variable at the oﬀset (Bytes(“params”)). Additionally, using a key with a value greater than 255 will prevent a collision. In the long term, creating documentation on the management of the global state and using unit and fuzz testing to check for potential collisions is recommended.

### Original Finding Content

## Security Assessment Report

**Diﬃculty:** High  
**Type:** Undeﬁned Behavior  
**Target:** `loan/loan_state.py`, `loan/loan.py`  

## Description
The layout of the loan application’s global state could cause a loan’s `params` variable to collide with a pool variable.

A loan has two types of variables:
- `params`, which is set by the owner and contains the loan parameters
- `pools`, which contains pool information

**CODE REDACTED**  
**DOCUMENTATION REDACTED**  

![Figure 7.1: REDACTED](#)  
![Figure 7.2: REDACTED](#)  

The `params` variable is stored at offset 112 (Bytes("p")). The `pools` variable contains an array in which every slot contains 3 loans, and only slots 0–62 are assumed to be used for loans.

When the pool’s slots are used, there is no guarantee that the global state is being accessed through slots 0–62. This means that slot 112 can be used to store a loan.

We set the difficulty rating of this issue to high because exploitation of the issue would likely require exploitation of another bug. This is because if slot 112 were used for a loan, its underlying values would likely not be directly usable, particularly because of the following:
- The first element of `params` is an admin address.
- The first element of a loan variable is the pool application ID.
- If `params` collides with a pool variable, its admin address must collide with an application ID.

## Exploit Scenario
Eve finds a lack of validation in the loan flow that allows her to trick the loan application into believing that there is a loan at slot 112. Eve uses the variable collision to change the system’s parameters and update the `oracle_adapter` ID. As a result, the system stops working.

## Recommendations
Short term, store the `params` variable at the offset (Bytes("params")). Because loan indexes are `uint8` values, using a key with a value greater than 255 will prevent a collision.

Long term, create documentation on the management of the global state, and use unit and fuzz testing to check for potential collisions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Folks Finance Capital Market Protocol v2 |
| Report Date | N/A |
| Finders | Vara Prasad Bandaru, Josselin Feist |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-11-folksfinance-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-11-folksfinance-securityreview.pdf

### Keywords for Search

`vulnerability`

