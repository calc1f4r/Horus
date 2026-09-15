---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53556
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Incorrect _addShares() Can Lead to Over-Delegation After Slashing Upgrade

### Overview

See description below for full details.

### Original Finding Content

## Description

The `_addShares()` function in EigenPodManager does not take into account negative initial share balances when returning the number of shares added. This results in the operator being credited with more shares than they are entitled to and the `depositScalingFactor` being updated incorrectly.

Before the slashing upgrade, `podOwnerDepositShares` can become negative after a checkpoint if there is a queued withdrawal. After the upgrade, the negative shares are reconciled when completing the queued withdrawal by adding the withdrawable shares of the withdrawal back to `podOwnerDepositShares` to make it non-negative. However, when the queued withdrawal is completed with `receiveAsTokens = false`, `EigenPodManager._addShares()` returns shares without accounting for any initial negative shares:

```solidity
function _addShares(address staker, uint256 shares) internal returns (uint256, uint256) {
    require(staker != address(0), InputAddressZero());
    require(int256(shares) >= 0, SharesNegative());
    int256 sharesToAdd = int256(shares);
    int256 prevDepositShares = podOwnerDepositShares[staker];
    int256 updatedDepositShares = prevDepositShares + sharesToAdd;
    podOwnerDepositShares[staker] = updatedDepositShares;
    emit PodSharesUpdated(staker, sharesToAdd);
    emit NewTotalShares(staker, updatedDepositShares);
    
    if (updatedDepositShares <= 0) {
        return (0, 0);
    }
    
    // @audit `shares` is returned even if `prevDepositShares < 0'
    // resulting in an incorrect number of added shares
    return (prevDepositShares < 0 ? 0 : uint256(prevDepositShares), shares);
}
```

The returned shares value is used to increase the operator’s shares and the staker’s `depositScalingFactor` for the strategy:

```solidity
(uint256 prevDepositShares, uint256 addedShares) = shareManager.addShares({
    staker: withdrawal.staker,
    strategy: withdrawal.strategies[i],
    token: tokens[i],
    shares: sharesToWithdraw
});

// Update the staker's deposit scaling factor and delegate shares to their operator
_increaseDelegation({
    operator: newOperator,
    staker: withdrawal.staker,
    strategy: withdrawal.strategies[i],
    prevDepositShares: prevDepositShares,
    addedShares: addedShares,
    slashingFactor: newSlashingFactors[i]
});
```

```solidity
function _increaseDelegation(
    address operator,
    address staker,
    IStrategy strategy,
    uint256 prevDepositShares,
    uint256 addedShares,
    uint256 slashingFactor
) internal {
    // Ensure that the operator has not been fully slashed for a strategy
    // and that the staker has not been fully slashed if it is the beaconChainStrategy
    // This is to prevent a divWad by 0 when updating the depositScalingFactor
    require(slashingFactor != 0, FullySlashed());
    
    // Update the staker's depositScalingFactor. This only results in an update
    // if the slashing factor has changed for this strategy.
    DepositScalingFactor storage dsf = _depositScalingFactor[staker][strategy];
    
    // @audit the depositScalingFactor is updated with the incorrect number of shares
    dsf.update(prevDepositShares, addedShares, slashingFactor);
    emit DepositScalingFactorUpdated(staker, strategy, dsf.scalingFactor());
    
    // If the staker is delegated to an operator, update the operator's shares
    if (isDelegated(staker)) {
        // @audit the operator's shares are increased by the incorrect number of shares
        operatorShares[operator][strategy] += addedShares;
        emit OperatorSharesIncreased(operator, staker, strategy, addedShares);
    }
}
```

The actual issue has a high impact as it results in the operator being credited with more shares than they are entitled to. In the case of a `depositScalingFactor` update, which would occur if the `slashingFactor` has changed, then the operator would end up with more withdrawable shares than they are entitled to.

This issue has an informational severity rating in the report as it was discovered by the EigenLayer team during the engagement.

## Recommendations

Consider returning `updatedDepositShares` instead of `shares` from `EigenPodManager._addShares()` if `prevDepositShares < 0`.

## Resolution

`EigenPodManager._addShares()` has been updated to return `updatedDepositShares` instead of `shares` if `prevDepositShares < 0` as recommended above. This issue has been resolved in PR #1033.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf

### Keywords for Search

`vulnerability`

