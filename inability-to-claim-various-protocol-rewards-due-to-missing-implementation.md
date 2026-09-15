---
# Core Classification
protocol: Level  Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46587
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/612f3254-f6a6-420d-8d51-fb058e4af022
source_link: https://cdn.cantina.xyz/reports/cantina_level_money_october_2024.pdf
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
finders_count: 3
finders:
  - Mario Poneder
  - Delvir0
  - Om Parikh
---

## Vulnerability Title

Inability to claim various protocol rewards due to missing implementation 

### Overview


This bug report is about a lack of mechanisms in the current implementation of a protocol that prevent users from claiming rewards from various sources. These rewards include staked AAVE tokens, rewards from specific incentive campaigns, and other protocol-specific rewards. This issue also affects the Reserve Manager Contract, where rewards from EigenLayer are not being claimed. As a result, these rewards are effectively locked in the protocol, causing a loss of value for participants and reducing the efficiency of the protocol. The recommendation is to implement a mechanism to claim rewards and ensure they are properly distributed or reinvested. This issue has been fixed in a recent code update.

### Original Finding Content

## Context
No context files were provided by the reviewer.

## Description
The current implementation lacks mechanisms to claim various rewards that accrue to the protocol from different sources. This affects:

## Aave Protocol Rewards:
- Staked AAVE tokens rewards.
- Chain-specific incentive campaign rewards (ARB, OP, ZKSYNC tokens).
- Protocol integration specific incentives (e.g., SNX incentives for providing sUSD).
- Other protocol-specific rewards.

## Reserve Manager Contract Rewards:
- EigenLayer rewards.

Rewards accrue to the wrapped rebasing token wrapper contract as it holds the underlying funds. There is no implementation to call `claimAllRewards` or utilize `allowClaimOnBehalf` functions on the `RewardsController` contract for Aave and `RewardsCoordinator` for EigenLayer.

## Impact
- Accrued rewards become effectively locked in the protocol.
- Loss of value for protocol participants who should benefit from these reward mechanisms.
- Reduced protocol efficiency as incentive mechanisms cannot be fully utilized.
- Potential compound effect as unclaimed rewards may also miss out on additional yield opportunities.

## Recommendation
- Implement mechanism to claim rewards from specific integrations.
- Ensure rewards are re-invested, distributed to the user, or withdrawn.
- Write test cases to verify the same.

## Level
Fixed in PR 25.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Level  Money |
| Report Date | N/A |
| Finders | Mario Poneder, Delvir0, Om Parikh |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_level_money_october_2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/612f3254-f6a6-420d-8d51-fb058e4af022

### Keywords for Search

`vulnerability`

