---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28419
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#4-events-not-emitting
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Events not emitting

### Overview

See description below for full details.

### Original Finding Content

##### Description
In the current version of feed contract after change of some storage variables events not emitting:
https://github.com/lidofinance/steth-price-feed/blob/459495f07c97d04f6e3839e7a3b32acfcade22ad/contracts/StEthPriceFeed.vy#L117
https://github.com/lidofinance/steth-price-feed/blob/459495f07c97d04f6e3839e7a3b32acfcade22ad/contracts/StEthPriceFeed.vy#L144
https://github.com/lidofinance/steth-price-feed/blob/459495f07c97d04f6e3839e7a3b32acfcade22ad/contracts/StEthPriceFeed.vy#L155
##### Recommendation
We recommend to add events and emit them in functions `update_safe_price`, `set_admin` and `set_max_safe_price_difference`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#4-events-not-emitting
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

