---
# Core Classification
protocol: Wagmi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34095
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Wagmi-security-review.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Protocol charges platform fees twice

### Overview


The bug report describes an issue where platform fees are being charged twice when a user repays an underwater loan. This results in the LP being unable to collect their rewards after the fees have been collected. This bug has a high impact and a low likelihood of occurring. The report includes a code snippet that shows how the fees are being charged twice and a recommendation on how to fix it. 

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

LP can call the repay on an underwater loan to retrieve their tokens back without their position being restored. If there are no other positions associated with this loan, the caller will receive the collateral minus platform fees and a liquidation bonus. However, there is an issue where platform fees are being charged twice.

```solidity
        if (params.isEmergency) {
            (!underLiquidation).revertError(ErrLib.ErrorCode.FORBIDDEN);
            (
                uint256 removedAmt,
                uint256 feesAmt,
                bool completeRepayment
            ) = _calculateEmergencyLoanClosure(
                    zeroForSaleToken,
                    params.borrowingKey,
                    currentFees,
                    borrowing.borrowedAmount
                );
            (removedAmt == 0).revertError(ErrLib.ErrorCode.LIQUIDITY_IS_ZERO);
            // Subtract the removed amount and fees from borrowedAmount and feesOwed
            borrowing.borrowedAmount -= removedAmt;
            borrowing.dailyRateCollateralBalance -= feesAmt;
>>          feesAmt =
                _pickUpPlatformFees(borrowing.holdToken, feesAmt) /
                Constants.COLLATERAL_BALANCE_PRECISION;
            // Deduct the removed amount from totalBorrowed
            unchecked {
                holdTokenRateInfo.totalBorrowed -= removedAmt;
            }
            // If loansInfoLength is 0, remove the borrowing key from storage and get the liquidation bonus
            if (completeRepayment) {
                LoanInfo[] memory empty;
                _removeKeysAndClearStorage(borrowing.borrower, params.borrowingKey, empty);
>>              feesAmt =
                  _pickUpPlatformFees(borrowing.holdToken, currentFees) /
                    Constants.COLLATERAL_BALANCE_PRECISION +
                    liquidationBonus;
            } else {
```

This will break protocol accounting since the recorded sum of tokens will be greater than the actual amount.

Here is the coded POC in `LiquidityBorrowingManager.t.sol`:

```solidity
    function testDoublePlatformFee() public {
        uint128 minLiqAmt = _minimumLiquidityAmt(253_320, 264_600);
        address[] memory tokens = new address[](1);
        tokens[0] = address(WETH);
        address vault = borrowingManager.VAULT_ADDRESS();

        vm.startPrank(bob);
        borrowingManager.borrow(createBorrowParams(tokenId, minLiqAmt), block.timestamp + 1);
        bytes32[] memory key = borrowingManager.getBorrowingKeysForTokenId(tokenId);
        vm.stopPrank();

        ILiquidityBorrowingManager.FlashLoanRoutes memory routes;
        ILiquidityBorrowingManager.SwapParams[] memory swapParams;

        ILiquidityBorrowingManager.RepayParams memory repay = ILiquidityBorrowingManager.RepayParams({
            isEmergency: true,
            routes: routes,
            externalSwap: swapParams,
            borrowingKey: key[0],
            minHoldTokenOut: 0,
            minSaleTokenOut: 0
        });

        // time to repay underwater loan
        vm.warp(block.timestamp + 86401);
        vm.prank(alice);
        (uint saleOut, uint holdToken) = borrowingManager.repay(repay, block.timestamp + 1);

        borrowingManager.collectProtocol(address(this), tokens);

        vm.expectRevert(bytes("W-ST"));
        vm.prank(alice);
        borrowingManager.collectLoansFees(tokens);
    }
```

In this scenario LP is unable to collect the rewards after platform fees were collected.

**Recommendations**

```diff
            if (completeRepayment) {
                LoanInfo[] memory empty;
                _removeKeysAndClearStorage(borrowing.borrower, params.borrowingKey, empty);
+               feesAmt +=
-                   _pickUpPlatformFees(borrowing.holdToken, currentFees) /
-                   Constants.COLLATERAL_BALANCE_PRECISION +
                    liquidationBonus;
            } else {
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Wagmi |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Wagmi-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

