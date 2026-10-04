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
solodit_id: 53557
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

beaconChainSlashingFactor Is Negated After Delegation

### Overview

See description below for full details.

### Original Finding Content

## Description

The _increaseDelegation() function incorrectly assumes that the addedShares parameter corresponds to the number of added withdrawable shares. This leads to an incorrect deposit scaling factor (dsf) and operator shares update when the staker has been slashed on the beacon chain before delegating.

When a staker delegates to an operator, their depositedShares are used as the addedShares parameter in the _increaseDelegation() function:

```solidity
DelegationManager.sol::._delegate()
function _delegate(address staker, address operator) internal onlyWhenNotPaused(PAUSED_NEW_DELEGATION) {
    // ...
    // read staker's deposited shares and strategies to add to operator's shares
    // and also update the staker depositScalingFactor for each strategy
    (IStrategy[] memory strategies, uint256[] memory depositedShares) = getDepositedShares(staker);
    uint256[] memory slashingFactors = _getSlashingFactors(staker, operator, strategies);
    for (uint256 i = 0; i < strategies.length; ++i) {
        // forgefmt: disable-next-item
        _increaseDelegation({
            operator: operator,
            staker: staker,
            strategy: strategies[i],
            prevDepositShares: uint256(0),
            // @audit incorrectly assumes depositedShares = withdrawableShares
            addedShares: depositedShares[i],
            slashingFactor: slashingFactors[i]
        });
    }
}
```

The _increaseDelegation() function assumes that addedShares corresponds to withdrawable shares, which is the case for token strategies as no slashing has occurred. However, for `beaconChainETHStrategy`, it is possible for beacon chain slashing to occur before the staker is delegated, such that the assumption no longer holds true. This results in the operator being credited with more shares than they are entitled to.

```solidity
DelegationManager.sol::._increaseDelegation()
function _increaseDelegation(
    address operator,
    address staker,
    IStrategy strategy,
    uint256 prevDepositShares,
    uint256 addedShares, // @audit `addedShares` corresponds to an increase in withdrawable shares
    uint256 slashingFactor
) internal {
    // Ensure that the operator has not been fully slashed for a strategy
    // and that the staker has not been fully slashed if it is the beaconChainStrategy
    // This is to prevent a divWad by 0 when updating the depositScalingFactor
    require(slashingFactor != 0, FullySlashed());
    
    // Update the staker's depositScalingFactor. This only results in an update
    // if the slashing factor has changed for this strategy.
    DepositScalingFactor storage dsf = _depositScalingFactor[staker][strategy];
    // @audit dsf is incorrectly updated with `addedShares`
    dsf.update(prevDepositShares, addedShares, slashingFactor);
    
    emit DepositScalingFactorUpdated(staker, strategy, dsf.scalingFactor());
    
    // If the staker is delegated to an operator, update the operator's shares
    if (isDelegated(staker)) {
        // @audit operator shares is incorrectly increased by `addedShares`
        operatorShares[operator][strategy] += addedShares;
        emit OperatorSharesIncreased(operator, staker, strategy, addedShares);
    }
}
```

Furthermore, a staker that has been slashed on the beacon chain before delegation will be able to negate any slashing events prior to delegation. This is because the dsf is reset to 1 / slashingFactor on the initial deposit/delegation:

```solidity
SlashingLib.sol::update()
function update(
    DepositScalingFactor storage dsf,
    uint256 prevDepositShares,
    uint256 addedShares,
    uint256 slashingFactor
) internal {
    // If this is the staker's first deposit, set the scaling factor to
    // the inverse of slashingFactor
    if (prevDepositShares == 0) {
        // @audit this cancels out the slashingFactor, so any slashing events prior to delegation are negated
        dsf._scalingFactor = uint256(WAD).divWad(slashingFactor);
        return;
    }
    // ...
}
```

The actual issue has a high impact as it allows a staker to negate changes to their `beaconChainSlashingFactor` before delegating, and allows them to have more shares delegated to the operator than they are entitled to. This issue has an informational severity rating in the report as it was discovered by the EigenLayer team during the engagement.

## Recommendations

Consider implementing the following:
1. Scale `addedShares` by the `beaconChainSlashingFactor` for the `beaconChainETHStrategy` in the `_delegate()` function before calling `_increaseDelegation()`.
2. For the initial deposit/delegation, assign the dsf to 1 / maxMagnitude instead of 1 / slashingFactor.

## Resolution

The EigenLayer team has implemented the following:
1. Use `withdrawableShares` instead of `depositedShares` as the `addedShares` argument in `_increaseDelegation()`.
2. For the initial deposit/delegation, scale the current dsf by 1 / `operatorSlashingFactor` to selectively negate AVS slashing but maintain beacon chain slashing.

This issue has been resolved in PR #1045.

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

