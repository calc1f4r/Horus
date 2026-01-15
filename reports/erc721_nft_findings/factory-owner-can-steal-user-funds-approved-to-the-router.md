---
# Core Classification
protocol: Sudoswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6774
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_lending
  - payments

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Max Goodman
  - Mudit Gupta
  - Gerard Persoon
---

## Vulnerability Title

Factory Owner can steal user funds approved to the Router

### Overview


This bug report outlines a vulnerability in the LSSVMPair and LSSVMRouter contracts. The code in the factory intends to prevent router contracts from being approved for calls, as they can have access to user funds. However, a pair owner can still make arbitrary calls to any contract that has been approved by the factory owner, allowing them to potentially steal user funds. 

Sudoswap has addressed the immediate issue of adding/removing routers, however, the broader issue of the factory owner being able to potentially steal pool funds remains. Spearbit recommends that Sudoswap consider changing the architecture such that the router sends the NFTs to the pair when it calls the swap function, and that the pair should store reserve balances and check tokens received against it. Spearbit's recommendation has been acknowledged.

### Original Finding Content

## Severity: High Risk

## Context
- **Files:** LSSVMPair.sol#L687-695, LSSVMRouter.sol#L574

## Description
A pair owner can make arbitrary calls to any contract that has been approved by the factory owner. The code in the factory intends to prevent router contracts from being approved for calls because router contracts can have access to user funds. An example includes the `pairTransferERC20From()` function, which can be used to steal funds from any account that has given it approval.

The router contracts can nevertheless be whitelisted by first being removed as a router and then being whitelisted. This way, anyone can deploy a pair and use the `call` function to steal user funds.

## Recommendation
Spearbit recommends that Sudoswap consider changing the architecture such that the router simply sends the NFTs to the pair when it calls the swap function. If you want to remove the trust from the router, make the pair store reserve balances and check tokens received against it.

## Sudoswap
The immediate issue of adding/removing routers is addressed in this branch here. Every time a new router is added or removed, we only toggle the allowed flag, while `wasEverAllowed` is always true. `LSSVMPair.call()` now checks if we’ve ever approved a router. The broader issue of the factory owner being able to potentially steal pool funds is acknowledged, with other specific vectors mentioned in the audit addressed in other branches.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap |
| Report Date | N/A |
| Finders | Max Goodman, Mudit Gupta, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Sudoswap-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

