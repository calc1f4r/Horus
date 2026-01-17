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
solodit_id: 45454
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/178

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

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Audinarey
  - valuevalk
---

## Vulnerability Title

H-1: After closing synthetix position we don't update global data for liquidations

### Overview


This report discusses a bug in the Autonomint protocol that occurs after an admin closes a synthetix position. The bug prevents global variables from being updated, which means that dCDS depositors and the protocol cannot benefit from the liquidation and potential gains. The root cause of the bug is that the function responsible for closing the position does not update the necessary global variables. This is in contrast to how the protocol handles liquidation type 1, where many values are updated to make the protocol aware of the liquidated position and its collateral. The bug occurs after a liquidation type 2 event, where a short position is submitted for the liquidated collateral and then closed by the admin without updating global variables. This has a significant impact on dCDS depositors, as they are unable to withdraw their portion of the liquidation. The report suggests updating the global variables after closing the position to mitigate this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/178 

## Found by 
Audinarey, valuevalk

### Summary
After admin closes synthetix position we don't update any global variables, which means that dCDS depositors and the whole protocol cannot benefit from the liquidation and the potential gains from its shorted position. 

### Root Cause
`closeThePositionInSynthetix()` function in [borrowLiquidation.sol](https://github.com/sherlock-audit/2024-11-autonomint/blob/0d324e04d4c0ca306e1ae4d4c65f0cb9d681751b/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L371-L375) only closes the position and does not update any global variables like in the `liquidation type 1`

```solidity
    function closeThePositionInSynthetix() external onlyBorrowingContract {
        (, uint128 ethPrice) = borrowing.getUSDValue(borrowing.assetAddress(IBorrowing.AssetName.ETH));
        // Submit an order to close all positions in synthetix
        synthetixPerpsV2.submitOffchainDelayedOrder(-synthetixPerpsV2.positions(address(this)).size, ethPrice * 1e16);
    }
```

For reference in liquidation type 1 we update many values to make the protocol aware of the fact that we have a position liquidated and its collateral is ready to be taken from dCDS depositors opted-in for that. ( other values related to yield for ABOND also shall be updated, just like in liquidation type 1 )
```solidity
      // Update the CDS data
        cds.updateLiquidationInfo(omniChainData.noOfLiquidations, liquidationInfo);
        cds.updateTotalCdsDepositedAmount(cdsAmountToGetFromThisChain);
        cds.updateTotalCdsDepositedAmountWithOptionFees(cdsAmountToGetFromThisChain);
        cds.updateTotalAvailableLiquidationAmount(cdsAmountToGetFromThisChain);
        omniChainData.collateralProfitsOfLiquidators += depositDetail.depositedAmountInETH;

        // Update the global data
        omniChainData.totalCdsDepositedAmount -= liquidationAmountNeeded - cdsProfits; //! need to revisit this
        omniChainData.totalCdsDepositedAmountWithOptionFees -= liquidationAmountNeeded - cdsProfits;
        omniChainData.totalAvailableLiquidationAmount -= liquidationAmountNeeded - cdsProfits;
        omniChainData.totalInterestFromLiquidation += uint256(borrowerDebt - depositDetail.borrowedAmount);
        omniChainData.totalVolumeOfBorrowersAmountinWei -= depositDetail.depositedAmountInETH;
        omniChainData.totalVolumeOfBorrowersAmountinUSD -= depositDetail.depositedAmountUsdValue;
        omniChainData.totalVolumeOfBorrowersAmountLiquidatedInWei += depositDetail.depositedAmountInETH;

        // Update totalInterestFromLiquidation
        uint256 totalInterestFromLiquidation = uint256(borrowerDebt - depositDetail.borrowedAmount);

        // Update individual collateral data
        --collateralData.noOfIndices;
        collateralData.totalDepositedAmount -= depositDetail.depositedAmount;
        collateralData.totalDepositedAmountInETH -= depositDetail.depositedAmountInETH;
        collateralData.totalLiquidatedAmount += depositDetail.depositedAmount;
        // Calculate the yields
        uint256 yields = depositDetail.depositedAmount - ((depositDetail.depositedAmountInETH * 1 ether) / exchangeRate);

        // Update treasury data
        treasury.updateTotalVolumeOfBorrowersAmountinWei(depositDetail.depositedAmountInETH);
        treasury.updateTotalVolumeOfBorrowersAmountinUSD(depositDetail.depositedAmountUsdValue);
        treasury.updateDepositedCollateralAmountInWei(depositDetail.assetName, depositDetail.depositedAmountInETH);
        treasury.updateDepositedCollateralAmountInUsd(depositDetail.assetName, depositDetail.depositedAmountUsdValue);
        treasury.updateTotalInterestFromLiquidation(totalInterestFromLiquidation);
        treasury.updateYieldsFromLiquidatedLrts(yields);
        treasury.updateDepositDetails(user, index, depositDetail);

        globalVariables.updateCollateralData(depositDetail.assetName, collateralData);
        globalVariables.setOmniChainData(omniChainData);
```

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path
- Liquidation Type 2 occurs.
- 1x short position is submitted for the liquidated collateral
- After some time and profits from the short position, admin closes it
- Global variables are not updated, which means that the collateral is unused.

### Impact
- The dCDS depositors won't be able to withdraw their portion of that liquidation, as we never registered it on the global omnichain fields.

### PoC

_No response_

### Mitigation
After closing the short position update the global variables, so the protocol can work with the collateral thats now available to be withdrawn from dCDS depositors. Other factors such as yield for abond apply as well.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | Audinarey, valuevalk |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/178
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

