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
solodit_id: 53759
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/sushi/sushi-swap-stable-pool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/sushi/sushi-swap-stable-pool/review.pdf
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

decimals() is optional under the ERC-20 Standard

### Overview

See description below for full details.

### Original Finding Content

## Description

Although it is common practice to include the `decimals()` function in an ERC-20 token, the standard does not strictly require it and, in fact, explicitly states:

> **OPTIONAL** - This method can be used to improve usability, but interfaces and other contracts MUST NOT expect these values to be present.

OpenZeppelin also classifies this attribute as an optional extra.

The constructor of `StablePool.sol` assumes that `decimals()` will always be present. It is possible that an ERC-20 compliant stablecoin token could exist which this contract would never be able to support, as the constructor would revert on line [81] or line [82] when it attempts to call `ERC20(_token0/1).decimals()`.

## Recommendations

This issue is heavily mitigated by the widespread support for `decimals()` amongst ERC-20 tokens. However, if full compliance with the standard is desired, the number of decimals could be submitted as an input parameter to the constructor. This has the disadvantage of creating a possible source of input error which might not be immediately obvious until liquidity is added.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/sushi/sushi-swap-stable-pool/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/sushi/sushi-swap-stable-pool/review.pdf

### Keywords for Search

`vulnerability`

