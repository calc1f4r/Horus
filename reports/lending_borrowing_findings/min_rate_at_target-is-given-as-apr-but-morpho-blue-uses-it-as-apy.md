---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40866
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad
source_link: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
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

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Christoph Michel
---

## Vulnerability Title

min_rate_at_target is given as apr but morpho blue uses it as apy 

### Overview


The report states that there is a bug in the ConstantsLib.sol file at line 12. The issue is related to the compounding interest for Morpho Blue. The current MIN_RATE_AT_TARGET value is causing a discrepancy in the annual percentage rate (APR) and the actual APY (yearly compounded interest rate). The APR is currently set at 0.1%, but the desired lower bound of 0.1% cannot be achieved due to the incorrect calculation of the APY. The report recommends using the correct APY values to fix this bug.

### Original Finding Content

## ConstantsLib.sol#L12

## Description
Morpho Blue is compounding the interest, see [Morpho.sol#L477](https://example.com/Morpho.sol#L477). The `MIN_RATE_AT_TARGET` specified here is given as a value that would result in a 0.1% APR (annual percentage rate, non-compounding). 

As Morpho Blue is compounding, this value must be given such that it results in an APY of 0.1%. We need to compute it the same way as Morpho as:

\[ e^{nx} - 1 = 0.001 \]

where \( n = 365 \) days. Solving for \( nx \) gives \( 0.0009995 \). Therefore, \( x = \text{MAX_RATE_AT_TARGET} = \frac{0.0009995 \text{ ether}}{365 \text{ days}} \). 

The current value of \( \frac{0.001 \text{ ether}}{365 \text{ days}} \) would lead to an actual Morpho Blue APY (yearly compounded interest rate) of:

\[ e^{0.001} = 0.0010005 = 0.10005\% \]

The desired lower bound of 0.1% cannot be reached.

## Recommendation
Consider using the correct APY values mentioned above.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad

### Keywords for Search

`vulnerability`

