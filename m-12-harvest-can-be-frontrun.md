---
# Core Classification
protocol: yAxis
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 783
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-yaxis-contest
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/140

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
  - front-running

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xsanson
---

## Vulnerability Title

[M-12] Harvest can be frontrun

### Overview


This bug report is about the potential for a bad actor to frontrun the harvest in the `NativeStrategyCurve3Crv._harvest` function. The bad actor could do this by imbalancing the Uniswap pair when swapping WETH to a stablecoin and by not considering the slippage when minting the 3CRV tokens during the `_addLiquidity` internal function. The proof of concept is available at the link provided in the report. The recommended mitigation steps include adding two additional estimated quantities to the `_harvest(_estimatedWETH, _estimatedYAXIS)` function.

### Original Finding Content

_Submitted by 0xsanson_

#### Impact
In the `NativeStrategyCurve3Crv._harvest` there are two instances that a bad actor could use to frontrun the harvest.

First, when we are swapping WETH to a stablecoin by calling `_swapTokens(weth, _stableCoin, _remainingWeth, 1)` the function isn't checking the slippage, leading to the risk to a frontun (by imbalancing the Uniswap pair) and losing part of the harvesting profits.

Second, during the `_addLiquidity` internal function: this calls `stableSwap3Pool.add_liquidity(amounts, 1)` not considering the slippage when minting the 3CRV tokens.

#### Proof of Concept
[`NativeStrategyCurve3Crv.sol` L108](https://github.com/code-423n4/2021-09-yaxis/blob/main/contracts/v3/strategies/NativeStrategyCurve3Crv.sol#L108)

#### Tools Used
editor

#### Recommended Mitigation Steps
In the function `_harvest(_estimatedWETH, _estimatedYAXIS)` consider adding two additional estimated quantities: one for the swapped-out stablecoin and one for the minted 3CRV.

**[BobbyYaxis (yAxis) acknowledged](https://github.com/code-423n4/2021-09-yaxis-findings/issues/140)**

**[uN2RVw5q commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/140#issuecomment-932765993):**
 > On second thought, I think this is a valid issue.
>
> > consider adding two additional estimated quantities: one for the swapped-out stablecoin and one for the minted 3CRV.
>
> This suggestion should be considered.

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/140#issuecomment-943477587):**
 > Warden identified two paths for front-running
>
> Since these are ways to extract value, severity is Medium

**BobbyYaxis (yAxis) noted:**
> Mitigated in PR 114: https://github.com/yaxis-project/metavault/pull/114



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | 0xsanson |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/140
- **Contest**: https://code4rena.com/contests/2021-09-yaxis-contest

### Keywords for Search

`Front-Running`

