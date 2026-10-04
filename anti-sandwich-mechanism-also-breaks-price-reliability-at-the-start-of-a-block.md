---
# Core Classification
protocol: OpenZeppelin Uniswap Hooks v1.1.0 RC 1 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61388
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/openzeppelin-uniswap-hooks-v1.1.0-rc-1-audit
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Anti-Sandwich Mechanism Also Breaks Price Reliability at the Start of a Block

### Overview


The bug report is about a contract called `AntiSandwichHook` which is designed to prevent sandwich attacks on the Uniswap platform. However, the report states that the contract may not work as intended because it assumes that the starting price of a block is fair, which may not always be the case. This is because the contract makes it difficult for external arbitrageurs to restore the price to its fair market level, potentially leading to an inaccurate starting price for swaps. The report suggests considering this issue in the design of the contract or documenting it in the contract's description.

### Original Finding Content

[`AntiSandwichHook`](https://github.com/OpenZeppelin/uniswap-hooks/blob/087974776fb7285ec844ca090eab860bd8430a11/src/general/AntiSandwichHook.sol#L47) tries to stop sandwich attacks by making sure that swaps cannot happen at a better price than what was available at the start of the block. This only works if that starting price is fair. In regular Uniswap pools, it is hard to manipulate the price at the start of a block because doing so would leave the pool exposed to arbitrage. So, normally, the price at the start of a block is close to the real market price.

However, this assumption becomes invalid once the anti-sandwich mechanism is applied. Since the hook makes any within-block price improvements non-arbitrageable (by redistributing the excess back to LPs), external arbitrageurs are disincentivized from restoring the price to its fair market level after an imbalance-causing swap. As a result, it is entirely plausible that the price at the beginning of a block reflects a manipulated or stale state rather than true market conditions. This leads to the enforcement of swaps against an inaccurate "anchor price".

Consider whether this can be solved at the design level. If it is an assumption that must be made when using such contracts, consider reflecting it in the contract's docstrings.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | OpenZeppelin Uniswap Hooks v1.1.0 RC 1 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/openzeppelin-uniswap-hooks-v1.1.0-rc-1-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

