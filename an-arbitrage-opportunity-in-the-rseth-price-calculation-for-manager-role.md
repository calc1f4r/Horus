---
# Core Classification
protocol: KelpDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30471
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#2-an-arbitrage-opportunity-in-the-rseth-price-calculation-for-manager-role
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

An arbitrage opportunity in the rsETH price calculation for MANAGER role

### Overview


The report states that there is a bug in the `swapAssetWithinDepositPool` function that allows users with the `MANAGER` role to make profitable trades even if some of their permissions have been revoked. The report recommends using a different approach, such as a collaterial-debt approach or AMM liquidity pool approach, for multi-asset pools instead of relying on price oracles.

### Original Finding Content

##### Description
There is an arbitrage opportunity for the `MANAGER` role using the `swapAssetWithinDepositPool` function. Even if some `MANAGER` permissions are revoked, the permission to call `swapAssetWithinDepositPool` is enough to perform profitable arbitrage.
##### Recommendation
For the multi-asset pools, we recommend using a collaterial-debt approach or AMM liquidity pool approach. Using price oracles for determining the exchange rate within multi-asset pools is generally not recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | KelpDAO |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#2-an-arbitrage-opportunity-in-the-rseth-price-calculation-for-manager-role
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

