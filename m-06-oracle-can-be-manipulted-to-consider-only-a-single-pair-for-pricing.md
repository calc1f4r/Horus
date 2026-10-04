---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1253
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-12-vader
github_link: https://github.com/code-423n4/2021-12-vader-findings/issues/40

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

protocol_categories:
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - TomFrenchBlockchain
---

## Vulnerability Title

[M-06] Oracle can be manipulted to consider only a single pair for pricing

### Overview


This bug report is about a vulnerability in an oracle that can lead to a loss of resilience in pricing for a single pair. The vulnerability is caused by an attacker manipulating the reserves of the underlying pair with a flash loan attack. This attack will make a pool appear with an arbitrarily large currentLiquidityEvaluation, which will result in all other pairs contributing negligibly to the final result of the oracle. While this doesn't lead to a loss of funds, it can force the oracle to only use a malfunctioning or deprecated Chainlink price feed for the asset in any pool. The recommended mitigation step is to calculate fair reserves using the pool invariant and the fair prices of the two assets. A similar calculation should be performed which is specific for the Vader invariant.

### Original Finding Content

_Submitted by TomFrenchBlockchain_

Loss of resilience of oracle to a faulty pricing for a single pair.

#### Proof of Concept

In the oracle we calculate the TVL of each pool by pulling the reserves and multiplying both assets by the result of a supposedly manipulation resistant oracle (the oracle queries its previous value for USDV and pulls the foreign asset from chainlink).

<https://github.com/code-423n4/2021-12-vader/blob/fd2787013608438beae361ce1bb6d9ffba466c45/contracts/lbt/LiquidityBasedTWAP.sol#L353-L383>

This value can be manipulated by skewing the reserves of the underlying pair with a flashloan attack. An attacker can then make a pool appear with an arbitrarily large `currentLiquidityEvaluation` which will result in all other pairs contributing negligibly to the final result of the oracle.

This doesn't result in loss of funds by itself afaict but should there be an issue for the chainlink price feed for the asset in any pool then an attacker can force the oracle to only use that pool for pricing USDV/VADER

Medium risk as "Assets not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements." External requirements being a malfunctioning or deprecated chainlink pricefeed for any used asset.

Calculating TVL of the pool is equivalent to value of all LP tokens so for more information see this post: <https://blog.alphafinance.io/fair-lp-token-pricing/>

#### Recommended Mitigation Steps

Calculate fair reserves using the pool invariant and the fair prices of the two assets.

The above link contains a mitigates for Uniswap, a similar calculation would have to be performed which is specific for the Vader invariant.

**[SamSteinGG (Vader) disputed and commented](https://github.com/code-423n4/2021-12-vader-findings/issues/40#issuecomment-1001506397):**
 > The evaluation of liquidity for a particular pair is performed based on the reserves of the previous block rendering a flash loan attack impossible. Can the  warden clarify how he is expecting this to be exploited?



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | TomFrenchBlockchain |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-vader
- **GitHub**: https://github.com/code-423n4/2021-12-vader-findings/issues/40
- **Contest**: https://code4rena.com/contests/2021-12-vader-protocol-contest

### Keywords for Search

`vulnerability`

