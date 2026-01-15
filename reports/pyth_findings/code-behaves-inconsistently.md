---
# Core Classification
protocol: Euler Price Oracle Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32434
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/price-oracle-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Code Behaves Inconsistently

### Overview

See description below for full details.

### Original Finding Content

The codebase incorporates several oracle adapters behind the same `IPriceOracle` interface. However, each specific adapter has its own set of assumptions and differences in the inner mechanics. There are also some inconsistencies between several adapters, specifically when it comes to prices being zero.


* Chainlink and Chronicle oracles prohibit the price from being zero.
* In the Lido oracle, if `inAmount` is small enough, the `outAmount` can be truncated to zero. The same can happen in the `Dai/sDai` oracle.
* Pyth, Uniswap V3, and Redstone oracles can directly return a zero price.


Consider implementing either of the following two changes to make the adapter behavior consistent:


* Prohibit the price from being zero (and negative) in all the adapters.
* Allow the price to be zero (and positive) in all the adapters and handle the special case of zero prices in the vaults.


***Update:** Partially resolved in [pull request #32](https://github.com/euler-xyz/euler-price-oracle/pull/32). Prices being truncated to zero are not deemed incorrect. The Euler team stated:*



> *We have modified `PythOracle` and `RedstoneCoreOracle` to reject a signed price of 0. Truncation to 0 is possible in all adapters and we consider it correct behavior. 0 is the correct answer for the question that `getQuote` answers: "the amount of `quote` corresponding to `inAmount` of `base`". Note that truncation is possible in all adapters, not just the ones mentioned.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Euler Price Oracle Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/price-oracle-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

