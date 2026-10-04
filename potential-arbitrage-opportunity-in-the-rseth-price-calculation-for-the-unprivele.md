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
solodit_id: 30475
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#2-potential-arbitrage-opportunity-in-the-rseth-price-calculation-for-the-unpriveleged-users
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

Potential arbitrage opportunity in the rsETH price calculation for the unpriveleged users

### Overview


The report states that there is a bug in the Chainlink price oracles system. This bug allows attackers to predict upcoming price updates and manipulate them for their own gain. The updateRSETHPrice function is particularly vulnerable and can be used to force a profitable price change. The report also mentions that the withdraw feature is not currently implemented, making it difficult to assess the safety of the system. The report recommends using alternative approaches, such as a collaterial-debt approach or AMM liquidity pool, for multi-asset pools instead of relying on price oracles.

### Original Finding Content

##### Description
Due to the nature of the Chainlink price oracles, the upcoming price updates are predictable. Additionally, the predictable price update can be forced by an attacker by calling the updateRSETHPrice function, which is decentralized/unrestricted. It allows the attacker to predict a profitable price deviation and perform a deposit, external DEX swap, or withdraw to get a guaranteed profit from their actions.

Currently, the withdraw functionality is not implemented, so we can't assess whether it would be safe or not.
##### Recommendation
For the multi-asset pools, we recommend using a collaterial-debt approach or AMM liquidity pool approach. Using price oracles for determining the exchange rate within multi-asset pools is generally not recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | KelpDAO |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/KelpDAO/README.md#2-potential-arbitrage-opportunity-in-the-rseth-price-calculation-for-the-unpriveleged-users
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

