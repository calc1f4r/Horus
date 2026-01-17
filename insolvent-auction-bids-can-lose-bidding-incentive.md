---
# Core Classification
protocol: Derive
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53731
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Insolvent Auction Bids Can Lose Bidding Incentive

### Overview

See description below for full details.

### Original Finding Content

## Description

During an insolvent auction, it is possible for the exchange rate of cash to USDC to decrease. This decrease may reduce the funds received by the liquidator such that they make a loss. If the system receives an insolvent auction bid which cannot be covered by the cash in the Security Module, it will print cash. This printed cash can then cause the exchange rate of cash to USDC to decrease such that the USDC withdrawal fee is activated.

This withdrawal fee is dynamic and depends on the ratio of available USDC to the amount of cash in the system. As a result of this, it is possible that the withdrawal fee will be larger than the difference in printed cash and the accepted negative asset value taken on by the liquidator. If this is the case, then it is unlikely any liquidator will bid on these insolvent auctions and the bad debt may sit unresolved in the system.

While possible, this situation would only occur for very large insolvent auction bids, or when the system has little or no funds available in the Security Module, meaning this situation should be less likely to occur as time passes and cash accumulates in the Security Module. Furthermore, if the system becomes sufficiently insolvent, it is unlikely that any liquidator will bid on insolvent auctions as the impact of further insolvencies compounds the effect of this withdrawal fee as the ratio of USDC to cash degrades further.

## Recommendations

The testing team recommends determining the likelihood of these liquidations occurring and developing monitoring tools to detect such liquidations during the early protocol development. It may be beneficial for the Derive team to bid on such auctions if needed.

Alternatively, a successful insolvent liquidation bid could result in a forced USDC withdrawal prior to updating the cash to USDC exchange rate. This would ensure insolvent liquidations would always receive the exchange rate available prior to their bid at the cost of a larger socialised cost to other Derive participants. However, this solution would only solve isolated cases and it is likely that multiple insolvency auctions would occur in the same time period due to the nature of price volatility affecting liquidations.

## Resolution

The development team has acknowledged the issue with the following comment:

> "Given there is a withdrawal pause, there is little incentive for users to not bid on ongoing auctions when they happen at a larger scale. Assets are also marked assuming USDC == 1 within the current risk managers, so the values of the portfolios will generally scale with any depeg event. Finally, at the point of the insolvent auction running the full duration, bidders do not even need to bring collateral to bid on auctions, so there will always be someone incentivised to take on those positions."

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Derive |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/derive/review-round2.pdf

### Keywords for Search

`vulnerability`

