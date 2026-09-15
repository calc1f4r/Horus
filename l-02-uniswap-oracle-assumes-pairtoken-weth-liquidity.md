---
# Core Classification
protocol: Wild Credit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 475
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-wild-credit-contest
source_link: https://code4rena.com/reports/2021-07-wildcredit
github_link: https://github.com/code-423n4/2021-07-wildcredit-findings/issues/118

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
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[L-02] Uniswap oracle assumes PairToken <> WETH liquidity

### Overview

See description below for full details.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The `UniswapV3Oracle.tokenPrice` function gets the price by combining the chainlink ETH price with the TWAP prices of the `token <> pairToken` and `pairToken <> WETH` pools.
It is therefore required that the `pairToken <> WETH` pool exists and has sufficient liquidity to be tamper-proof.

## Impact
When listing lending pairs for tokens that have a WETH pair with low liquidity (at 0.3% fees) the prices can be easily manipulated leading to liquidations or underpriced borrows.
This can happen for tokens that don't use `WETH` as their default trading pair, for example, if they prefer a stablecoin, or `WBTC`.

## Recommendation
Ensure there's enough liquidity on the `pairToken <> WETH` Uniswap V3 0.3% pair, either manually or programmatically.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Wild Credit |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-wildcredit
- **GitHub**: https://github.com/code-423n4/2021-07-wildcredit-findings/issues/118
- **Contest**: https://code4rena.com/contests/2021-07-wild-credit-contest

### Keywords for Search

`vulnerability`

