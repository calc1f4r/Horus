---
# Core Classification
protocol: DeFi Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33564
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#1-collateral-price-growth-may-cause-hard-liquidation
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

Collateral price growth may cause hard liquidation

### Overview

See description below for full details.

### Original Finding Content

##### Description
When the oracle price changes, the AMM tick price changes by approximately 3.3 times more. If a user's position were replaced with stablecoins, its health would be determined by the market price of the collateral that can be purchased from the AMM with those stablecoins, and dynamic fees would not taken into account.

This may create a scenario where hard liquidations may occur even though the price of the collateral goes up:

1. A hacker buys the lenders' collateral from the AMM.
2. The hacker inflates the oracle price of the collateral by 2%.
3. The hacker can then `liquidate()` the lenders because their `health < 0`, as their positions, being replaced with stablecoins, can now purchase 3.3 times less collateral in AMM compared to the real market.

This situation may only arise if the hacker is able to inflate the oracle price between two trades within one or two blocks.

##### Recommendation
Oracle selection recommendations:

1. Ensure that the oracle's price cannot fluctuate mid-block. The price should be determined by the last transaction in the previous block. Most EMA oracles in Curve stable swap pools meet this criterion.
2. Note, that the `EmaPriceOracle.vy` file in the project repository is implemented **incorrectly** and **must not** be used: https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/oracles/EmaPriceOracle.vy
3. Avoid integrating with low-liquidity tokens to reduce the likelihood of 2-block attacks.
4. Increase AMM fees, as recommended in the comment: https://github.com/curvefi/curve-stablecoin/blob/e0096068be93afa09687aaf3e96e0d75e289109d/tests/lending/test_oracle_attack.py.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DeFi Money |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#1-collateral-price-growth-may-cause-hard-liquidation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

