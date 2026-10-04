---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6921
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - hack3r-0m
  - Jay Jonah
  - Christoph Michel
  - Emanuele Ricci
---

## Vulnerability Title

RewardsManagerAave does not verify token addresses

### Overview


This bug report concerns the RewardsManagerForAave.sol smart contract, which is used to manage rewards for Aave's three different types of tokens. The bug was that the public accrueUserUnclaimedRewards function allowed an attacker to pass in an sToken address and steal from the contract. The code assumed that if the token was not the variable debt token, then it must be the aToken, and used the user’s supply balance for the reward calculation.

To fix the issue, the code was changed to verify the token address to be either an aToken or vToken, and to require a valid asset address. The fix was implemented in PR #554. The bug was acknowledged and the report was closed.

### Original Finding Content

## Severity: Critical Risk

## Context
`RewardsManagerForAave.sol#L145-L147`

## Description
Aave has 3 different types of tokens: aToken, stable debt token, and variable debt token (a/s/vToken). Aave’s incentive controller can define rewards for all of them, but Morpho never uses a stable-rate borrow token (sToken). 

The public `accrueUserUnclaimedRewards` function allows passing arbitrary token addresses for which to accrue user rewards. Current code assumes that if the token is not the variable debt token, then it must be the aToken, and uses the user’s supply balance for the reward calculation as follows:

```solidity
uint256 stakedByUser = reserve.variableDebtTokenAddress == asset
? positionsManager.borrowBalanceInOf(reserve.aTokenAddress, _user).onPool
: positionsManager.supplyBalanceInOf(reserve.aTokenAddress, _user).onPool;
```

An attacker can accrue rewards by passing in an sToken address and steal from the contract. The steps are as follows:
1. Attacker supplies a large amount of tokens for which sToken rewards are defined.
2. The aToken reward index is updated to the latest index, but the sToken index is not initialized.
3. Attacker calls `accrueUserUnclaimedRewards([sToken])`, which will compute the difference between the current Aave reward index and the user’s sToken index, then multiply it by their supply balance.
4. The user-accumulated rewards in `userUnclaimedRewards[user]` can be withdrawn by calling `PositionManager.claimRewards([sToken, ...])`.
5. Attacker withdraws their supplied tokens again.

The abovementioned steps can be performed in one single transaction to steal unclaimed rewards from all Morpho positions.

## Recommendation
Verify the token address to be either an aToken or vToken.

```solidity
function accrueUserUnclaimedRewards(address[] calldata _assets, address _user) {
    // ...
    for (uint256 i = 0; i < _assets.length; i++) {
        address asset = _assets[i];
        DataTypes.ReserveData memory reserve = lendingPool.getReserveData(
            IGetterUnderlyingAsset(asset).UNDERLYING_ASSET_ADDRESS()
        );
        // ...
        uint256 stakedByUser;
        if (reserve.variableDebtTokenAddress == asset) {
            stakedByUser = positionsManager.borrowBalanceInOf(reserve.aTokenAddress, _user).onPool;
        } else {
            require(reserve.aTokenAddress == asset, "invalid asset");
            stakedByUser = positionsManager.supplyBalanceInOf(reserve.aTokenAddress, _user).onPool;
        }
        // ...
    }
}
```

## Morpho
Fixed, the recommendation has been implemented in PR #554.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | hack3r-0m, Jay Jonah, Christoph Michel, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation`

