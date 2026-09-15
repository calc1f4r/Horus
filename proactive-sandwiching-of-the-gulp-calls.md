---
# Core Classification
protocol: GrowthDeFi WHEAT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13361
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/06/growthdefi-wheat/
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
  - dexes
  - cdp
  - yield
  - services
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Sergii Kravchenko
  - David Oz Kashi
  -  Dominik Muhs
---

## Vulnerability Title

Proactive sandwiching of the gulp calls

### Overview


This bug report is about an attack vector that affects the `gulp` functions in all the strategies and also fees collectors and the buyback adapters. This attack vector is significant when the exchange the trade is performed on allows significant changes in liquidity pools in a single transaction, the attacker can frontrun legitimate `gulp` calls with reasonable slippage values, and trades are performed, i.e. when `rewardToken != routingToken` and/or `routingToken != reserveToken` hold true. The client communicated this issue was addressed in commit 34c6b355795027d27ae6add7360e61eb6b01b91b.

Initially, it was suggested that the `onlyOwner` modifier should be added to the `gulp` function to ensure only authorized parties with reasonable slippages can execute trades on behalf of the strategy contracts. Furthermore, additional slippage checks can be added to avoid unwanted behavior of authorized addresses. However, in order to fix another issue, an alternative solution was proposed, which is to use oracles to restrict users from calling the `gulp` function with unreasonable slippage (more than 5% from the oracle’s moving average price). The side effect of this solution is that sometimes the outdated price will be used, meaning that when the price crashes, nobody will be able to call the `gulp`.

### Original Finding Content

#### Resolution



The client communicated this issue was addressed in commit 34c6b355795027d27ae6add7360e61eb6b01b91b.


#### Description


Each strategy token contract provides a `gulp` method to fetch pending rewards, convert them into the reserve token and split up the balances. One share is sent to the fee collector as a performance fee, while the rest is deposited into the respective `MasterChef` contract to accumulate more rewards. Suboptimal trades are prevented by passing a minimum slippage value with the function call, which results in revert if the expected reserve token amount cannot be provided by the trade(s).


The slippage parameter and the trades performed in `gulp` open the function up to proactive sandwich attacks. The slippage parameter can be freely set by the attacker, resulting in the system performing arbitrarily bad trades based on how much the attacker can manipulate the liquidity of involved assets around the `gulp` function call.


This attack vector is significant under the following assumptions:


* The exchange the trade is performed on allows significant changes in liquidity pools in a single transaction (e.g., not limiting transactions to X% of the pool amount),
* The attacker can frontrun legitimate `gulp` calls with reasonable slippage values,
* Trades are performed, i.e. when `rewardToken != routingToken` and/or `routingToken != reserveToken` hold true.


#### Examples


This affects the `gulp` functions in all the strategies:


* `PancakeSwapCompoundingStrategyToken`
* `AutoFarmCompoundingStrategyToken`
* `PantherSwapCompoundingStrategyToken`


and also fees collectors and the buyback adapters:


* `PantherSwapBuybackAdapter`
* `AutoFarmFeeCollectorAdapter`
* `PancakeSwapFeeCollector`
* `UniversalBuyback`


#### Recommendation


There are different possible solutions to this issue and all have some tradeoffs. Initially, we came up with the following suggestion:


* The `onlyOwner` modifier should be added to the `gulp` function to ensure only authorized parties with reasonable slippages can execute trades on behalf of the strategy contracts. Furthermore, additional slippage checks can be added to avoid unwanted behavior of authorized addresses, e.g., to avoid a bot setting unreasonable slippage values due to a software bug.


But in order to fix another issue (<https://github.com/ConsenSys/growthdefi-audit-2021-06/issues/8),> we came up with the alternative solution:


* Use oracles to restrict users from calling the `gulp` function with unreasonable slippage (more than 5% from the oracle’s moving average price). The side effect of that solution is that sometimes the outdated price will be used. That means that when the price crashes, nobody will be able to call the `gulp`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | GrowthDeFi WHEAT |
| Report Date | N/A |
| Finders | Sergii Kravchenko, David Oz Kashi,  Dominik Muhs |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/06/growthdefi-wheat/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

