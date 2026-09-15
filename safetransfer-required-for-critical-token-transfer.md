---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19617
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

safeTransfer Required for Critical Token Transfer

### Overview


The bug report is about a transfer function on line 93 of StargateAdapter.sol which fails when called with USDT. This causes a revert of the call to sgReceive(), leaving the tokens transferred from Stargate in the SushiXSwap contract on the destination chain, where they can be transferred away freely by any user. The suggested recommendation is to use safeTransfer for the transfer on line 93. Additionally, the report mentions that the amountOut is not converted to shares.

### Original Finding Content

## Description

The transfer function on line [93] of `StargateAdapter.sol` will fail if called with USDT, one of the two tokens intended to be used in the function. This will cause a revert of the call to `sgReceive()`, which will leave the tokens transferred from Stargate in the SushiXSwap contract on the destination chain, where they can be transferred away freely by any user.

## Recommendations

Use `safeTransfer` for the transfer on line [93].

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf

### Keywords for Search

`vulnerability`

