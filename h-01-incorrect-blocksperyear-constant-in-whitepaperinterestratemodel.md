---
# Core Classification
protocol: Venus Protocol
chain: everychain
category: uncategorized
vulnerability_type: configuration

# Attack Vector Details
attack_type: configuration
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20769
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-venus
source_link: https://code4rena.com/reports/2023-05-venus
github_link: https://github.com/code-423n4/2023-05-venus-findings/issues/320

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
  - configuration

# Audit Details
report_date: unknown
finders_count: 23
finders:
  - DeliChainSec
  - BoltzmannBrain
  - volodya
  - Yardi256
  - 0xkazim
---

## Vulnerability Title

[H-01] Incorrect `blocksPerYear` constant in `WhitepaperInterestRateModel`

### Overview


The WhitePaperInterestRateModel contract is a fork from Compound Finance, which was designed to be deployed on Ethereum Mainnet. The contract uses a constant called `blocksPerYear` to calculate the interest rate of the market on a per-block basis. This constant assumes that there are 365 days a year and that the block-time is 15 seconds. However, Venus Protocol is deployed on the BNB chain, which has a block-time of only 3 seconds. This results in the interest rate per block on the BNB chain to be 5x greater than intended. 

The issue is that both `baseRatePerBlock` and `multiplierPerBlock` are affected and are 5x the value they should be. This also implies that the pool's interest rate is also 5 times more sensitive to utilization rate changes than intended. It is impossible for the market to arbitrage and adjust the interest rate back to the intended rate. Arbitrageurs will likely take advantage of the high supply rate, leading to a utilization ratio close to 0. 

To illustrate the issue, a Python script was created to plot the `WhitePaperInterestRateModel` curves for a 15 second and a 3 second block time. This shows how the interest rate per block is 5x greater than it's intended to be for markets that use the Whitepaper interest rate model.

### Original Finding Content


<https://github.com/code-423n4/2023-05-venus/blob/8be784ed9752b80e6f1b8b781e2e6251748d0d7e/contracts/WhitePaperInterestRateModel.sol#L17>

The interest rate per block is **5x** greater than it's intended to be for markets that use the Whitepaper interest rate model.

### Proof of Concept

The `WhitePaperInterestRateModel` contract is forked from Compound Finance, which was designed to be deployed on Ethereum Mainnet. The `blocksPerYear` constant inside the contract is used to calculate the interest rate of the market on a per-block basis and is set to **2102400**, which assumes that there are 365 days a year and that the block-time is **15 seconds**.

However, Venus Protocol is deployed on the BNB chain, which has a block-time of only **3 seconds**. This results in the interest rate per block on the BNB chain to be **5x** greater than intended.

Both `baseRatePerBlock` and `multiplierPerBlock` are affected and are **5x** the value they should be. This also implies that the pool's interest rate is also 5 times more sensitive to utilization rate changes than intended. It is impossible for the market to arbitrage and adjust the interest rate back to the intended rate as seen in the PoC graph below. It's likely that arbitrageurs will deposit as much collateral as possible to take advantage of the high supply rate, leading to a utilization ratio close to 0.

The following Python script plots the `WhitePaperInterestRateModel` curves for a 15 second and a 3 second block time.

```python
import matplotlib.pyplot as plt



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Venus Protocol |
| Report Date | N/A |
| Finders | DeliChainSec, BoltzmannBrain, volodya, Yardi256, 0xkazim, zzykxx, MohammedRizwan, peritoflores, Brenzee, ast3ros, Franfran, Lilyjjo, fs0c, SaeedAlipoor01988, sces60107, Bauchibred, BPZ, berlin-101, thekmj, carlitox477, sashik\_eth, Team\_Rocket |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-venus
- **GitHub**: https://github.com/code-423n4/2023-05-venus-findings/issues/320
- **Contest**: https://code4rena.com/reports/2023-05-venus

### Keywords for Search

`Configuration`

