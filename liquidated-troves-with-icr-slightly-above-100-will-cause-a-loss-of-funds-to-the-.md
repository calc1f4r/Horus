---
# Core Classification
protocol: Bima
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46273
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a
source_link: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
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
  - santipu
---

## Vulnerability Title

Liquidated Troves with ICR slightly above 100% will cause a loss of funds to the Stability Pool 

### Overview


This bug report discusses an issue with the liquidation process in a specific contract. When a user's Trove (a type of account) is liquidated with a certain level of debt, it can cause a loss of funds for other users in a separate account called the StabilityPool. This is because the liquidation process uses a certain amount of the Trove's collateral as compensation for gas fees, which can make the Trove suddenly unhealthy and negatively impact the StabilityPool. This can lead to losses for users in the StabilityPool and potentially harm the overall health of the protocol. The recommendation to fix this issue is to change the liquidation process so that it does not use the StabilityPool when the Trove's debt is below a certain level.

### Original Finding Content

## LiquidationManager Issue Overview

## Context
- LiquidationManager.sol#L183
- LiquidationManager.sol#L314
- LiquidationManager.sol#L349

## Description
When a Trove is liquidated with an ICR slightly above 100% but still below 100.5%, it will cause a loss of funds for the users in the StabilityPool due to the collateral gas compensation. A Trove can be liquidated in two ways:

- If a Trove has an ICR lower than MCR but still higher than 100%, it should be liquidated using the StabilityPool.
- If the Trove has an ICR lower than 100%, it should be liquidated without the StabilityPool; instead, the debt and collateral are distributed within the same TroveManager.

This distinction is made so that liquidations that carry bad debt—i.e., debt without backing collateral—do not negatively impact the StabilityPool, but only that TroveManager. However, there is an edge case where a Trove has an ICR higher than 100% but still generates some bad debt due to the gas compensation.

The collateral gas compensation is a percentage of the total collateral of a Trove (0.5%) that is discounted from a Trove's collateral on liquidation and sent to the liquidator. This gas compensation can cause a Trove that is slightly healthy, meaning it has an ICR slightly above 100%, to be suddenly unhealthy without that 0.5% of collateral.

This issue will happen whenever a Trove is liquidated with an ICR that is above 100% but is below 100.5%. In these scenarios, the liquidation will offset the Trove's debt and collateral using the StabilityPool, causing losses to its depositors.

If the Trove is big enough, it can cause a significant loss to users in the StabilityPool, leading to some withdrawals from there and hurting the overall protocol health.

## Recommendation
To mitigate this issue, the liquidation functions should liquidate without using the StabilityPool when the Den's ICR is below 100.5% and not 100%.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Bima |
| Report Date | N/A |
| Finders | santipu |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a

### Keywords for Search

`vulnerability`

