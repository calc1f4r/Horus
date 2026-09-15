---
# Core Classification
protocol: yAxis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 782
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-09-yaxis-contest
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/112

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
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-11] wrong YAXIS estimates

### Overview


A bug report was filed for the `Harvester.getEstimates` contract in the code. The contract is used to estimate a `YAXIS` amount but uses the wrong path and/or amount. It currently uses a `WETH` input amount to compute a `YAXIS -> WETH` trade. This results in wrong trade amounts being returned which can lead to a large slippage and can be used for a sandwich attack. The recommended mitigation step is to fix the estimations computations by changing the path to `path[0] = WETH; path[1] = YAXIS` in `Harvester.getEstimates`.

### Original Finding Content

_Submitted by cmichel_

The `Harvester.getEstimates` contract tries to estimate a `YAXIS` amount but uses the wrong path and/or amount.

It currently uses a `WETH` **input** amount to compute a `YAXIS -> WETH` trade.

```solidity
address[] memory _path;
_path[0] = IStrategy(_strategy).want();
_path[1] = IStrategy(_strategy).weth();
// ...

_path[0] = manager.yaxis();
// path is YAXIS -> WETH now
// fee is a WETH precision value
uint256 _fee = _estimatedWETH.mul(manager.treasuryFee()).div(ONE_HUNDRED_PERCENT);
// this will return wrong trade amounts
_amounts = _router.getAmountsOut(_fee, _path);
_estimatedYAXIS = _amounts[1];
```

#### Impact
The estimations from `getEstimates` are wrong.
They seem to be used to provide min. amount slippage values `(_estimatedWETH, _estimatedYAXIS)` for the harvester when calling `Controller._estimatedYAXIS`.
These are then used in `BaseStrategy._payHarvestFees` and can revert the harvest transactions if the wrongly computed `_estimatedYAXIS` value is above the actual trade value.
Or they can allow a large slippage if the `_estimatedYAXIS` value is below the actual trade value, which can then be used for a sandwich attack.

#### Recommended Mitigation Steps
Fix the estimations computations.

As the estimations are used in `BaseStrategy._payHarvestFees`, the expected behavior seems to be trading `WETH` to `YAXIS`.
The path should therefore be changed to `path[0] = WETH; path[1] = YAXIS` in `Harvester.getEstimates`.


**[Haz077 (yAxis) acknowledged](https://github.com/code-423n4/2021-09-yaxis-findings/issues/112)**

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/112#issuecomment-943475050):**
 > Price estimates on Uniswap are dependent on which side of the swap you're making
>
> Sponsor has mitigated in later PR



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/112
- **Contest**: https://code4rena.com/contests/2021-09-yaxis-contest

### Keywords for Search

`vulnerability`

