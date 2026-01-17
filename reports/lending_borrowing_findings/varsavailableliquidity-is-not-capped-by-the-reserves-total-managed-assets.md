---
# Core Classification
protocol: Astera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62291
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Saw-mon and Natalie
  - Cergyk
  - Jonatas Martins
---

## Vulnerability Title

vars.availableLiquidity is not capped by the reserve's total managed assets

### Overview


This bug report discusses an issue related to the calculation of available liquidity in the MiniPoolDefaultReserveInterestRate and MiniPoolPiReserveInterestRateStrategy contracts. The formula used to calculate available liquidity assumes that there is enough liquidity in the lending pool reserve to cover the unused flow, which may not always be the case. To fix this, a cap should be placed on the available flow and the formula for calculating available liquidity should be modified. However, this issue has been resolved in a recent commit and is no longer applicable. 

### Original Finding Content

## Severity: Medium Risk

## Context
- MiniPoolDefaultReserveInterestRate.sol#L147-L149
- MiniPoolPiReserveInterestRateStrategy.sol#L106-L108

## Description
The following formula assumes there is enough liquidity in the corresponding tranched reserve in the lending pool to cover the unused flow (which might not be the case).

```solidity
vars.availableLiquidity = IERC20(asset).balanceOf(aToken) 
                        + IAToken(asset).convertToShares(flowLimiter.getFlowLimit(vars.underlying, minipool)) 
                        - IAToken(asset).convertToShares(vars.currentFlow);
```

Let's define `vars.flowLiquidity` as:

```solidity
vars.flowLiquidity = IAToken(asset).convertToShares(flowLimiter.getFlowLimit(vars.underlying, minipool)) 
                    - IAToken(asset).convertToShares(vars.currentFlow);
```

Then this `vars.flowLiquidity` needs to be capped by the liquidity available in the corresponding reserve in the lending pool:

```solidity
vars.flowLiquidity = min(
    vars.flowLiquidity,
    IAToken(asset).convertToShares(
        IAToken(asset).ATOKEN_ADDRESS().getTotalManagedAssets()
    )
);
```

## Recommendation
Based on the above, one should put a cap on the available flow and modify the formula used for `vars.availableLiquidity` as follows:

```solidity
vars.flowLiquidity = IAToken(asset).convertToShares(flowLimiter.getFlowLimit(vars.underlying, minipool)) 
                    - IAToken(asset).convertToShares(vars.currentFlow);

vars.flowLiquidity = min(
    vars.flowLiquidity,
    IAToken(asset).convertToShares(
        IAToken(asset).ATOKEN_ADDRESS().getTotalManagedAssets()
    )
);

vars.availableLiquidity = IERC20(asset).balanceOf(aToken) + vars.flowLiquidity;
```

## Astera
The unused flow has been removed from `vars.availableLiquidity` in commit `6c7bf89e`, and thus this issue does not apply anymore.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Astera |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Cergyk, Jonatas Martins |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

