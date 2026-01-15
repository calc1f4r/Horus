---
# Core Classification
protocol: Euler Labs - Euler Price Oracle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35786
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf
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
  - Christos Pap
  - M4rio.eth
  - Christoph Michel
  - David Chaparro
  - Emanuele Ricci
---

## Vulnerability Title

The PythOracle won't work with positive expparameter

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
PythOracle.sol#L82

## Description
The Pyth oracle is using an `expparameter` to determine the decimals that the price will be normalized to result in the actual price. The formula is: 

```
price * 10^exp
```

We checked all the current feeds and the `expvalue` is between -5/-10. The current Solidity SDK also states that the `expcanNOT` be >= 0.

While we agree with most of the aforementioned reasonings to only support negative values for the `exp`, we've noticed in the code of the Pyth Client that the actual `expvalue` can be negative and positive:
- **add_price.rs#L44**: When you add a price, it checks the exponent.
- **utils.rs#L101-L106**: It can be between +-MAX_NUM_DECIMALS
- **c_oracle_header.rs#L14**: The `MAX_NUM_DECIMALS` has a value of 12 so theoretically it can be +-12.

Furthermore, we've talked with the Pyth team and they confirmed that currently they have set the check in the SDK to facilitate the discussions but they do not exclude the fact that this value can be positive in the future.

## Recommendation
Consider supporting positive `exp` for a more generalized integration of the PythOracle.

## Euler
Resolved in PR 32.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Euler Labs - Euler Price Oracle |
| Report Date | N/A |
| Finders | Christos Pap, M4rio.eth, Christoph Michel, David Chaparro, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-Oracle-April-2024.pdf

### Keywords for Search

`vulnerability`

