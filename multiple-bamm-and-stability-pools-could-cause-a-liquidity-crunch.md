---
# Core Classification
protocol: Threshold
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54699
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e
source_link: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
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
finders_count: 3
finders:
  - Alex The Entreprenerd
  - luksgrin
  - Kurt Barry
---

## Vulnerability Title

Multiple BAMM and Stability Pools could cause a liquidity crunch 

### Overview

See description below for full details.

### Original Finding Content

## BAMM.sol#L169

## Description
Multiple Stability Pools may cause a lack of liquidity during liquidations. This could be due to BAMM Stakers not moving from one BAMM to another during periods of volatility. 

### Example:

#### Period A
- BTC price is extremely flat.
- ETH price is more volatile.
- All BTC minters end up staking in the ETH Stability Pool because the APR is higher.

#### Period B
- BTC starts having liquidations (one day of excessive volatility).
- Because stakers need time to move their funds (and they have to perform this themselves), liquidity is insufficient to handle the liquidation, causing debt and collateral redistribution.

This can create a scenario in which some liquidations may not be performed optimally, resulting in potentially more bad debt being formed.

## Recommendation
It is worth weighing whether it would be best to have one Stability Pool that can handle liquidations on multiple systems, or whether the separate system is resilient enough. A yield farming vault that moves THUSD from one Stability Pool to another may also be a way to offer higher APR to stakers, as well as ensure that liquidity is available when necessary.

## Threshold USD
It's economically feasible in this model to take "ever-larger loans", but it's not against future earnings per se. The Initial Protocol Loan is scaled to a size intended to cover all cases, currently set at 100M thUSD. It could be set at 1B, 10B, 100B, or higher; the number is irrelevant and imaginary.

### What truly happens is this:
When a liquidation occurs, roughly ~10% is profit to the stability pool (and thus the PCV). The stability pool will exchange thUSD for collateral worth ~10% more than the thUSD provided. This is instant profit to the PCV. Due to this, it can absorb an endless supply of collateral while taking no loss. For example, a 100M liquidation would wipe out the stability pool but leave the PCV with ~$10M in more value (profit). We could just as easily have seeded the pool with 1B if more appropriate.

The main risk (of loss) becomes the balancing act rather than the draw from the stability pool itself. With ~10% profit, there is room for ~10% fluctuations to the downside until the balancing is complete before the PCV runs at a loss. In Bitcoin, 10% movement usually takes days. Given that BAMM is set up to constantly offer liquidated collateral for sale, it's intended that the collateral will be returned back to the PCV as thUSD in due time, with exceptions being rare circumstances of very high fluctuation in the markets / black swans.

B. Protocol's own analysis shows that these events will average out over time, but in rare instances where the PCV would incur a real loss (debt) such as during large liquidations and a fast dropping market, it would first cancel out debt against already built-up profits incurred in the protocol (from loans, earlier liquidations, redemptions). If loss exceeds this sum, then no withdrawals can be made from the PCV until debts are repaid; this promise of future earnings is where we can ask what limits the market is willing to accept before losing trust in the peg. I argue quite a lot if we look at fractional reserve stablecoins.

As stated earlier, PCV is the main depositor in the stability pool and there's no yield farming. Since all profits from loans accrue into the PCV, it will have a steady stream of thUSD entering the pools and the IPC will work as a sufficient buffer in times of high volatility.

BAMM offers collateral up for sale; naturally, arbitragers should step in to fulfill this order once profitable. Liquidity would need to be strong in either the tBTC/thUSD pair and ETH/thUSD pair or by proxy thUSD/USDC pair, tBTC/WBTC pair, or similar.

I expect these pairs (tBTC/WBTC and thUSD/stablecoin) to be commissioned by the DAO with yield farming APRs to incentivize sufficient liquidity.

## Cantina
Threshold team's plans are deemed adequate to mitigate any concerns regarding liquidity crunches.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Threshold |
| Report Date | N/A |
| Finders | Alex The Entreprenerd, luksgrin, Kurt Barry |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e

### Keywords for Search

`vulnerability`

