---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18318
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

Missing zero-address check may allow re-initialization of pairs

### Overview

See description below for full details.

### Original Finding Content

## Security Report

## Severity
**Low Risk**

## Context
LSSVMPair.sol#L118-L126

## Description
`LSSVMPair.initialize()` checks if it is already initialized using `require(owner() == address(0), "Initialized");`. However, without a zero-address check on `_owner`, this can be true even later if the pair is initialized accidentally with `address(0)` instead of `msg.sender`. This is because `__Ownable_init` in `OwnableWithTransferCallback` does not disallow `address(0)` unlike `transferOwnership`. This is, however, not the case with the current implementation where `LSSVMPair.initialize()` is called from `LSSVMPairFactory` with `msg.sender` as the argument for `_owner`. 

Therefore, `LSSVMPair.initialize()` may be called multiple times.

## Recommendation
Add a zero-address check on the `_owner` parameter of `initialize()`.

## Responses
**Sudorandom Labs:** Acknowledged, no change as at the moment, we pass in caller to be the owner of pairs.  
**Spearbit:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

