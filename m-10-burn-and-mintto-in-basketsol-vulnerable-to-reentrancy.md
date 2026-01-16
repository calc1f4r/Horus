---
# Core Classification
protocol: Kuiper
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 798
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-kuiper-contest
source_link: https://code4rena.com/reports/2021-09-defiprotocol
github_link: https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/248

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - hack3r-0m
  - 0xalpharush
  - JMukesh
  - johnsterlacci
---

## Vulnerability Title

[M-10] burn and mintTo in Basket.sol vulnerable to reentrancy

### Overview


This bug report is about a vulnerability in the functions mintTo and burn in the Basket.sol contract. These functions make external calls prior to updating the state, allowing attackers to mint free basket tokens if the basket contains an ERC777 token. This is possible because the contract pulls an ERC777 token from the user and the attacker can reenter the mintTo function to mint more tokens than they deposited. The recommended mitigation step is to move external calls after state updates, as this is best practice in accordance with the check-effect-interact pattern.

### Original Finding Content

## Handle

0xalpharush


## Vulnerability details

## Impact

The functions [mintTo](https://github.com/code-423n4/2021-09-defiProtocol/blob/52b74824c42acbcd64248f68c40128fe3a82caf6/contracts/contracts/Basket.sol#L82) 
and [burn](https://github.com/code-423n4/2021-09-defiProtocol/blob/52b74824c42acbcd64248f68c40128fe3a82caf6/contracts/contracts/Basket.sol#L96) make external calls prior to updating the state. If a basket contains an ERC777 token, attackers can mint free basket tokens.

## Proof of Concept

An attacker could reenter the `mintTo` function when the contract pulls an ERC777 token from the user and mint more tokens than they deposited.

## Tools Used

Slither

## Recommended Mitigation Steps

Move external calls after state updates. It is best practice to make external calls after updating state in accordance with the check-effect-interact pattern.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Kuiper |
| Report Date | N/A |
| Finders | hack3r-0m, 0xalpharush, JMukesh, johnsterlacci |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-defiprotocol
- **GitHub**: https://github.com/code-423n4/2021-09-defiprotocol-findings/issues/248
- **Contest**: https://code4rena.com/contests/2021-09-kuiper-contest

### Keywords for Search

`vulnerability`

