---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54627
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/e7dac53a-6098-4aa1-aa0f-ea44ee87050e
source_link: https://cdn.cantina.xyz/reports/cantina_badger_august2023.pdf
github_link: none

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
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hyh
  - StErMi
---

## Vulnerability Title

Partial liquidation and leaving bad debt undistributed can be optimal for liquidators to max- imize incentives received from other CDPs 

### Overview


The report discusses a potential issue with the LiquidationLibrary code, specifically in the function that calculates incentives for liquidators. The issue is that liquidators may have incentives to only partially liquidate the worst CDPs in order to maximize their rewards. This means that bad debt may be left behind and the overall health of the protocol may be compromised. The impact of this issue is assessed to be medium. The report recommends requiring that the CDP being liquidated is the worst one to prevent this issue. 

### Original Finding Content

## LiquidationLibrary Analysis

## Context
`LiquidationLibrary.sol#L539-L554`

## Description
Liquidators have incentives to avoid fully liquidating the bad CDPs until the very end of their liquidation sequence. This way they leave bad debt undistributed and maximize ICRs (Incremental Collateral Ratios) of the best liquidable CDPs, receiving more liquidation incentives, which linearly depend on the ICR when MCR (Minimum Collateral Ratio) > ICR > LICR (Liquidation Incentive Collateral Ratio).

On the same grounds as the issue "Liquidator can receive outsized incentives by aiming the best liquidable CDPs first", it is also profitable for a liquidator to perform only partial liquidation of the worst CDP containing bad debt to receive 3% of the maximal debt that can be burned partially, leaving only minimal collateral and the full bad debt part:

```solidity
function _calculateSurplusAndCap(
    // ...
) private view returns (uint256 cappedColPortion, uint256 collSurplus, uint256 debtToRedistribute) {
    // Calculate liquidation incentive for liquidator:
    // If ICR is less than 103%: give away 103% worth of collateral to liquidator, i.e., 
    // repaidDebt * 103% / price,
    // If ICR is more than 103%: give away min(ICR, 110%) worth of collateral to liquidator, i.e.,
    // repaidDebt * min(ICR, 110%) / price,

    uint256 _incentiveColl;
    if (_ICR > LICR) {
        _incentiveColl = (_totalDebtToBurn * (_ICR > MCR ? MCR : _ICR)) / _price;
    } else {
        if (_fullLiquidation) {
            // for full liquidation, there would be some bad debt to redistribute
            _incentiveColl = collateral.getPooledEthByShares(_totalColToSend);
            uint256 _debtToRepay = (_incentiveColl * _price) / LICR;
            debtToRedistribute = _debtToRepay < _totalDebtToBurn ? _totalDebtToBurn - _debtToRepay : 0;
        } else {
            // for partial liquidation, new ICR would deteriorate
            // since we give more incentive (103%) than current _ICR allowed
            // See the line below
            _incentiveColl = (_totalDebtToBurn * LICR) / _price;
        }
    }
    cappedColPortion = collateral.getSharesByPooledEth(_incentiveColl);
    cappedColPortion = cappedColPortion < _totalColToSend ? cappedColPortion : _totalColToSend;
    collSurplus = (cappedColPortion == _totalColToSend) ? 0 : _totalColToSend - cappedColPortion;
}
```

There is a minimal debt/collateral requirement in `partiallyLiquidate()`, that forms a boundary condition for the strategy, i.e. one has to leave enough debt at CDP to satisfy the `MIN_NET_COLL` based condition:

```solidity
function _requirePartialLiqDebtSize(
    uint256 _partialDebt,
    uint256 _entireDebt,
    uint256 _price
) internal view {
    require(
        // See the line below
        (_partialDebt + _convertDebtDenominationToBtc(MIN_NET_COLL, _price)) <= _entireDebt,
        "LiquidationLibrary: Partial debt liquidated must be less than total debt"
    );
}
```

The correspondence between liquidator reward obtainable on full liquidation and the profit from keeping bad debt undistributed and ICRs being higher depends on CDP sizes. Given big enough CDPs, the liquidator reward can be forfeited until the end. The risk of losing it if someone else performs a full liquidation, when liquidations are performed non-atomically, can be small compared to the indirect profit obtainable from keeping bad debt intact.

## Impact
Similarly, liquidation incentives will be maximized in excess of protocol logic and actual pool state, not only due to good ones being liquidated first, but also due to bad ones being liquidated only partially. Based on medium likelihood and impact setting, the severity is assessed to be medium.

## Recommendation
It looks like requiring that the CDP being liquidated has to be the worst one is needed, as otherwise there may be a hidden bad debt part remaining.

## Acknowledgments
- **BadgerDAO**: Acknowledged.
- **Cantina**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | hyh, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_badger_august2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/e7dac53a-6098-4aa1-aa0f-ea44ee87050e

### Keywords for Search

`vulnerability`

