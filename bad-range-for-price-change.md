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
solodit_id: 28415
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#4-bad-range-for-price-change
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Bad range for price change

### Overview


This bug report is about the current version of the feed smart contract. It is possible to set a 100% allowed range for price change which is too large. Therefore, it is recommended to change the maximum allowed difference to 1000. This bug report is related to the StEthPriceFeed.vy file which can be found on the Github repository.

### Original Finding Content

##### Description
In the current version of feed smart contract, it is possible to set 100% (for assets with the same price it is very big range) allowed range for price change:
https://github.com/lidofinance/steth-price-feed/blob/459495f07c97d04f6e3839e7a3b32acfcade22ad/contracts/StEthPriceFeed.vy#L162
##### Recommendation
We recommend to change max allowed difference to `1000`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#4-bad-range-for-price-change
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

