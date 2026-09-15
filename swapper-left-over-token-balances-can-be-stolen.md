---
# Core Classification
protocol: Timeless
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6762
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - yield
  - yield_aggregator
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - JayJonah
  - Christoph Michel
---

## Vulnerability Title

Swapper left-over token balances can be stolen

### Overview


This bug report is about the Swapper and UniswapV3Swapper contracts. It is possible for anyone to steal token balances from the Swapper contract by using the Swapper.doZeroExSwap with useSwapperBalance and tokenOut = tokenToSteal, or by setting arbitrary token approvals to arbitrary spenders on behalf of the Swapper contract using UniswapV3Swapper.swapUnderlyingToXpyt. 

The recommendation is for all transactions to move all tokens in and out of the contract atomically when performing swaps, in order to not leave any left-over token balances or be susceptible to front-running attacks. This is acknowledged as the intended way to use Swapper and it should not hold any tokens before and after a transaction.

### Original Finding Content

## Swapper Contract Security Concerns

## Context
- **Swapper**: `Swapper.sol#L133`
- **Uniswap V3 Swapper**: `UniswapV3Swapper.sol#L187`

## Description
The `Swapper` contract may never have any left-over token balances after performing a swap because token balances can be stolen by anyone in several ways:
- By using `Swapper.doZeroExSwap` with `useSwapperBalance` and `tokenOut = tokenToSteal`
- Arbitrary token approvals to arbitrary spenders can be set on behalf of the `Swapper` contract using `UniswapV3Swapper.swapUnderlyingToXpyt`.

## Recommendation
All transactions must atomically move all tokens in and out of the contract when performing swaps to prevent any left-over token balances or susceptibility to front-running attacks.

## Timeless
Acknowledged, this is the intended way to use `Swapper`: it should not hold any tokens before and after a transaction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Timeless |
| Report Date | N/A |
| Finders | JayJonah, Christoph Michel |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Timeless-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

