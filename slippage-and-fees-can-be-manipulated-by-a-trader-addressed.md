---
# Core Classification
protocol: Bancor V2 AMM Security Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13643
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/06/bancor-v2-amm-security-audit/
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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

Slippage and fees can be manipulated by a trader ✓ Addressed

### Overview


A bug report has been identified which allows users to optimize trading costs by adding liquidity to a converter contract before making a trade. This manipulation reduces slippage, and the trader can receive a part of the fees for this trade. An example is given which shows how the slippage can be reduced by adding liquidity. To address this issue, a new exit fee mechanism was introduced. This mechanism returns fewer tokens if the primary reserve is not in a balanced state. This should potentially make the manipulation non-profitable. However, in some cases, traders may still have an incentive to add liquidity before making the trade and then remove it to get a part of the fees. To completely fix the issue, some modification of the algorithm is required.

### Original Finding Content

#### Resolution



The issue was addressed by introducing an exit fee mechanism. When a liquidity provider wants to withdraw some liquidity, the smart contract returns fewer tokens if the primary reserve is not in the balanced state. So in most cases, the manipulations described in the issue should potentially be non-profitable anymore. Although, in some cases, the traders still may have some incentive to add liquidity before making the trade and remove it after to get a part of the fees (i.e., if the pool is going to be in a balanced state after the trade).


#### Description


Users are making trades against the liquidity pool (converter) with slippage and fees defined in the converter contract and Bancor formula.
The following steps can be done to optimize trading costs:


* Instead of just making a trade, a user can add a lot of liquidity (of both tokens, or only one of them) to the pool after taking a flash loan, for example.
* Make the trade.
* Remove the added liquidity.


Because the liquidity is increased on the first step, slippage is getting smaller for this trade. Additionally, the trader receives a part of the fees for this trade by providing liquidity.


One of the reasons why this is possible is described in another issue [issue 5.3](#loss-of-the-liquidity-pool-is-not-equally-distributed).


This technique of reducing slippage could be used by the trader to get more profit from any frontrunning/arbitrage opportunity and can help to deplete the reserves.


#### Example


Consider the initial state with an amplification factor of 20 and zero fees:



```
Initial state:
converter TKN balance = 10000000
converter TKN weight = 500000
converter BNT balance = 10000000
converter BNT weight = 500000

```
Here a user can make a trade with the following rate:


`-> Convert 9000000 TKN into 8612440 BNT.`


But if the user adds 100% of the liquidity in both tokens before the trade, the slippage will be lower:


`-> Convert 9000000 TKN into 8801955 BNT.`


#### Recommendation


Fixing this issue requires some modification of the algorithm.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Bancor V2 AMM Security Audit |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/06/bancor-v2-amm-security-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

