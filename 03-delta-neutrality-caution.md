---
# Core Classification
protocol: Ethena Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29390
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-ethena
source_link: https://code4rena.com/reports/2023-10-ethena
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
  - staking_pool
  - decentralized_stablecoin

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[03] Delta neutrality caution

### Overview

See description below for full details.

### Original Finding Content

Users should be cautioned about the impermanent losses entailed arising from the delta-neutral stability strategy adopted by the protocol, specifically if the short positions were to encounter hefty losses. Apparently, the users could have held on to their collateral, e.g. `stETH or WETH`, and ended up a lot richer with the equivalent amount of `USDe`. I suggest all minting entries to begin with stable coins like `USDC, DAI etc` that could be converted to `stETH` to generate yield if need be instead of having users depositing `stETH` from their wallet reserves. Psychologically, this will make the users feel better as the mentality has been fostered more on preserving the 1:1 peg of `USDe` at all times. 



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ethena Labs |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-ethena
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-10-ethena

### Keywords for Search

`vulnerability`

