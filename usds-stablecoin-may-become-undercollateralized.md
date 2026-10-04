---
# Core Classification
protocol: Salty.IO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29621
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
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
finders_count: 2
finders:
  - Damilola Edwards
  - Richie Humphrey
---

## Vulnerability Title

USDS stablecoin may become undercollateralized

### Overview


This report discusses a low difficulty bug in the Salty.IO protocol related to data validation. It explains that in a downtrending market, a black swan event could cause the USDS stablecoin to become undercollateralized. When a loan is liquidated, 5% of the collateral is sent to the liquidator as a fee, but if 105% of the collateral is not received, the protocol will suffer a loss. Additionally, the collateral seized from liquidations is not immediately sold, which can cause problems in a downtrending market. The bug is further exacerbated by the fact that the collateralization ratio is calculated assuming that the price of USDS is $1. This can lead to losses for the protocol in a flash crash scenario. The report recommends short-term and long-term solutions, including analyzing the issue and creating a design specification to identify risks and weaknesses. 

### Original Finding Content

## Diﬃculty: Low

## Type: Data Validation

## Description
In a downtrending market, a black swan type event could cause the USDS stablecoin to become undercollateralized. When a loan is liquidated, 5% of the collateral is sent to the liquidator as a fee. If 105% of the collateral is not received, the protocol will suffer a loss.

Furthermore, the collateral seized from liquidations is not immediately sold; instead, it is registered as a counterswap to be sold the next time a matching buy order is placed. In a downtrending market, especially during a flash crash, this forces the protocol to retain these assets as they decline in value.

We also noted that the collateralization ratio is calculated assuming that the price of USDS is $1.

## Exploit Scenario
The market crashes, and liquidations are triggered. The liquidations result in the seizure of WBTC and WETH, which are deposited in the Pools contract until a counterswap occurs. As the market continues to fall, no buy orders are placed, and no counterswaps are triggered. Salty.IO suffers losses from being naked long the tokens. When the flash crash bottoms out and reverses, the counterswaps are immediately triggered, locking in the unrealized losses at the bottom.

## Recommendations
**Short term:** Analyze the issue and identify a possible solution for this problem. This problem does not have a simple solution and is inherent in the design of the protocol. Any solution should be thoughtfully considered and tested. Risks that are not addressed should be clearly documented.

**Long term:** Create a design specification that identifies the interactions and risks between the protocol’s features. Test scenarios combined with fuzzing can be used to simulate adverse market conditions and identify weaknesses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Salty.IO |
| Report Date | N/A |
| Finders | Damilola Edwards, Richie Humphrey |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-10-saltyio-securityreview.pdf

### Keywords for Search

`vulnerability`

