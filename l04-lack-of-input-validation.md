---
# Core Classification
protocol: Notional Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11155
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/notional-audit/
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
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L04] Lack of input validation

### Overview

See description below for full details.

### Original Finding Content

There are several instances of `external` functions failing to validate the input parameters they are provided. For example:


* In the `setParameters` function on [line 94 of `CashMarket.sol`](https://github.com/notional-finance/contracts/blob/b6fc6be4622422d0e34c90e77f2ec9da18596b8c/contracts/CashMarket.sol#L94) and the `createCashGroup` function on [line 140 of `Portfolios.sol`](https://github.com/notional-finance/contracts/blob/b6fc6be4622422d0e34c90e77f2ec9da18596b8c/contracts/Portfolios.sol#L140), `maturityLength` can be set arbitrarily. In practice, a market with an extremely large maturity length would likely not have many participants. Even so, if `maturityLength` were too large, it would lead to erroneous cash ladders. If `maturityLength` were set to zero, it would lead to reversions caused by division by zero.
* In the `setFee` function on [line 150 of `CashMarket.sol`](https://github.com/notional-finance/contracts/blob/b6fc6be4622422d0e34c90e77f2ec9da18596b8c/contracts/CashMarket.sol#L150), neither `liquidityFee` nor `transactionFee` are given upper bounds. Values that are too large will lead to reversions in several critical functions.
* In the `setParameters` function on [line 94 of `CashMarket.sol`](https://github.com/notional-finance/contracts/blob/b6fc6be4622422d0e34c90e77f2ec9da18596b8c/contracts/CashMarket.sol#L94), `numMaturities` can be set to `0` which would cause reversions in several critical functions.
* In the `settleCashBalanceBatch` function on [line 682 of `Escrow.sol`](https://github.com/notional-finance/contracts/blob/b6fc6be4622422d0e34c90e77f2ec9da18596b8c/contracts/Escrow.sol#L682), the length of `values` and `payers` is not required to be equal. Unequal lengths will lead to a reversion after potentially burning non-negligible amounts of gas.
* In the `setHaircuts` function on [line 100 of `Portfolios.sol`](https://github.com/notional-finance/contracts/blob/b6fc6be4622422d0e34c90e77f2ec9da18596b8c/contracts/Portfolios.sol#L100), the values passed in for the various “haircuts” can be arbitrarily large. This is in contradiction with the intention of the codebase and the comment provided in the [NatSpec `@notice` tag of this same function](https://github.com/notional-finance/contracts/blob/b6fc6be4622422d0e34c90e77f2ec9da18596b8c/contracts/Portfolios.sol#L93).
* In the `updateCashGroup` function [on line 182 of `Portfolios.sol`](https://github.com/notional-finance/contracts/blob/b6fc6be4622422d0e34c90e77f2ec9da18596b8c/contracts/Portfolios.sol#L182), the NatSpec comments list several guidelines for each input, but none of those guidelines are enforced in the code.


To avoid errors and unexpected system behavior, consider explicitly restricting the range of inputs that can be accepted for all externally-provided inputs via `require` clauses where appropriate.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Notional Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/notional-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

