---
# Core Classification
protocol: Autonomint Colored Dollar V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45515
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/799

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
finders_count: 4
finders:
  - John44
  - almurhasan
  - Ruhum
  - pashap9990
---

## Vulnerability Title

M-25: Treasury will run out of liquidated funds to give to withdrawing users causing withdrawals to fail

### Overview


The issue reported is that the treasury will eventually run out of funds to give to users who are trying to withdraw their funds, causing the withdrawals to fail. This is because the cached amount of liquidated assets is never decreased, leading the treasury to believe it has more funds than it actually does. This is caused by a code error in the CDSLib contract, where the value for liquidated collateral is not updated after a user withdraws their funds. This causes the contract to try to transfer the full amount in a given token, even if the treasury does not have enough funds. The impact of this bug is that users who have opted into liquidation will not be able to withdraw their funds. The suggested mitigation is to update the value in the `withdrawUser()` function.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/799 

## Found by 
John44, Ruhum, almurhasan, pashap9990

### Summary

The cached liquidated asset amount is never decreased causing the treasury to believe that it has more funds than it actual does.

### Root Cause

In [CDSLib.sol:687](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/lib/CDSLib.sol#L687), it calls `getLiquidatedCollateralToGive()` with the available liquidated assets set as `liquidatedCollateralAmountInWei(x)`:

```sol
              // call getLiquidatedCollateralToGive in cds library to get in which assests to give liquidated collateral
                (
                    totalWithdrawCollateralAmountInETH,
                    params.ethAmount,
                    weETHAmount,
                    rsETHAmount,
                    collateralToGetFromOtherChain
                ) = getLiquidatedCollateralToGive(
                    CDSInterface.GetLiquidatedCollateralToGiveParam(
                        params.ethAmount,
                        weETHAmount,
                        rsETHAmount,
                        interfaces.treasury.liquidatedCollateralAmountInWei(IBorrowing.AssetName.ETH),
                        interfaces.treasury.liquidatedCollateralAmountInWei(IBorrowing.AssetName.WeETH),
                        interfaces.treasury.liquidatedCollateralAmountInWei(IBorrowing.AssetName.WrsETH),
                        interfaces.treasury.totalVolumeOfBorrowersAmountLiquidatedInWei(),
                        params.weETH_ExchangeRate,
                        params.rsETH_ExchangeRate
                    )
                );
```

If the `liquidatedCollateralAmountInWei` for a token is bigger than the amount of tokens the contract needs, it will simply transfer the whole amount in that single token, see [CDSLib.sol:324](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/lib/CDSLib.sol#L324)

```sol
    function getLiquidatedCollateralToGive(
        CDSInterface.GetLiquidatedCollateralToGiveParam memory param
    ) public pure returns (uint128, uint128, uint128, uint128, uint128) {
        // calculate the amount needed in eth value
        uint256 totalAmountNeededInETH = param.ethAmountNeeded + (param.weETHAmountNeeded * param.weETHExRate) / 1 ether + (param.rsETHAmountNeeded * param.rsETHExRate) / 1 ether;
        // calculate amount needed in weeth value
        uint256 totalAmountNeededInWeETH = (totalAmountNeededInETH * 1 ether) / param.weETHExRate;
        // calculate amount needed in rseth value
        uint256 totalAmountNeededInRsETH = (totalAmountNeededInETH * 1 ether) / param.rsETHExRate;

        uint256 liquidatedCollateralToGiveInETH;
        uint256 liquidatedCollateralToGiveInWeETH;
        uint256 liquidatedCollateralToGiveInRsETH;
        uint256 liquidatedCollateralToGetFromOtherChainInETHValue;
        // If this chain has sufficient amount
        if (param.totalCollateralAvailableInETHValue >= totalAmountNeededInETH) {
            // If total amount is avaialble in eth itself
            if (param.ethAvailable >= totalAmountNeededInETH) {
                liquidatedCollateralToGiveInETH = totalAmountNeededInETH;
                // If total amount is avaialble in weeth itself
            } else if (param.weETHAvailable >= totalAmountNeededInWeETH) {
                // ...
            } else if (param.rsETHAvailable >= totalAmountNeededInRsETH) {
                // ...
            } else {
                // ...
            }
        } else {
            // ...
        }
        return (
            uint128(totalAmountNeededInETH),
            uint128(liquidatedCollateralToGiveInETH),
            uint128(liquidatedCollateralToGiveInWeETH),
            uint128(liquidatedCollateralToGiveInRsETH),
            uint128(liquidatedCollateralToGetFromOtherChainInETHValue)
        );
    }
```

The given amount is then transferred from the treasury, see [CDSLib.sol:825](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/lib/CDSLib.sol#L825):

```sol
                if (params.ethAmount != 0) {
                    params.omniChainData.collateralProfitsOfLiquidators -= totalWithdrawCollateralAmountInETH;
                    // Call transferEthToCdsLiquidators to tranfer eth
                    interfaces.treasury.transferEthToCdsLiquidators(
                        msg.sender,
                        params.ethAmount
                    );
                }
```

The same thing applies to weETH and wrsETH as well.

The issue is that after a user has withdrawn their funds, the cached available asset amount isn't decreased. In the treasury contract, `liquidatedCollateralAmountInWei` is only updated in the `updateDepositedCollateralAmountInWei()` function where the value is increased:

```sol
    function updateDepositedCollateralAmountInWei(
        IBorrowing.AssetName asset,
        uint256 amount
    ) external onlyCoreContracts {
        depositedCollateralAmountInWei[asset] -= amount;
        liquidatedCollateralAmountInWei[asset] += amount;
    }
```

So even after a user has withdrawn and the actual collateral asset balance has decreased, `liquidatedCollateralAmountInWei()` will return the same value. That will cause the CDSLib contract to again try to send the full amount in that given token ignoring the fact that the treasury doesn't hold enough funds. When the transfer is executed it will revert, causing the tx to revert and the user's funds to be stuck.

### Internal pre-conditions

none

### External pre-conditions

none

### Attack Path

none

### Impact

CDS users who have opted into liquidation won't be able to withdraw their funds.

### PoC

_No response_

### Mitigation

The value should be decreased in `withdrawUser()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | John44, almurhasan, Ruhum, pashap9990 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/799
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

