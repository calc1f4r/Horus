---
# Core Classification
protocol: MakerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54446
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ccf91a4a-d29b-40e7-b48e-2669edc06b7e
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_dssallocator_sep2023.pdf
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
finders_count: 3
finders:
  - m4rio
  - shung
  - Christoph Michel
---

## Vulnerability Title

The fee parameter is missing from event emitting within the DepositorUniV3.sol 

### Overview

See description below for full details.

### Original Finding Content

## Context
- `DepositorUniV3.sol#L254`
- `DepositorUniV3.sol#L298`
- `DepositorUniV3.sol#L327`

## Description
Within the `deposit`, `withdraw`, and `collect` functions, an event is emitted with various parameters. However, the `fee` parameter is missing, which can help the off-chain infrastructure to identify the right pool that the deposit or withdrawal was performed with. The logic to get a Uniswap v3 pool is the following:

```
_getPool(p.gem0, p.gem1, p.fee)
```

## Recommendation
Consider adding the `fee` parameter to the events within the `deposit`, `withdraw`, and `collect` functions.

## MakerDAO
Fixed in commit `5dea8ea`.

## Cantina
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, shung, Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_dssallocator_sep2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ccf91a4a-d29b-40e7-b48e-2669edc06b7e

### Keywords for Search

`vulnerability`

