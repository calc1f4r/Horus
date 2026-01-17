---
# Core Classification
protocol: Dahlia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46374
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443
source_link: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
github_link: none

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
finders_count: 3
finders:
  - Saw-mon and Natalie
  - kankodu
  - Yorke Rhodes
---

## Vulnerability Title

Protocol and Reserve Fees cannot be withdrawn 

### Overview


This bug report discusses an issue with the withdrawal function in the InterestImpl.sol contract. The report states that while the correct recipients are assigned shares equivalent to the protocol and reserve fees, they are unable to withdraw because only the wrappedVault is allowed to call the Dahlia.withdraw function. This is because the fee recipients do not have any vault shares minted, preventing them from withdrawing through the vault. The report suggests updating the test to include additional checks for this issue and provides code for better readability. The recommendation is to add an additional function that allows the protocol fee recipient and reserve fee recipient to withdraw. The bug has been fixed in the Dahlia and Cantina Managed contracts. The risk level is medium.

### Original Finding Content

## Context
**File:** `InterestImpl.sol#L51`  
**Description:** Shares equivalent to the protocol and reserve fees are assigned to the correct recipient. However, they cannot withdraw because only the `wrappedVault` is allowed to call the `Dahlia.withdraw` function. The fee recipients do not have any vault shares minted, so they cannot withdraw through the vault either.

## Proof of Concept
Update the `test/core/integration/AccrueInterestIntegration.t.sol:AccrueInterestIntegrationTest.test_int_accrueInterest_withFees` to have the below additional checks.

### Here's the code with the diff formatting preserved and structured for better readability:

```solidity
function test_int_accrueInterest_withFees(
    TestTypes.MarketPosition memory pos,
    uint256 blocks,
    uint32 fee
) public {
    vm.pauseGasMetering();
    pos = vm.generatePositionInLtvRange(pos, TestConstants.MIN_TEST_LLTV, $.marketConfig.lltv);
    vm.dahliaSubmitPosition(pos, $.carol, $.alice, $);
    uint32 protocolFee = uint32(bound(uint256(fee), BoundUtils.toPercent(2), BoundUtils.toPercent(5)));
    uint32 reserveFee = uint32(bound(uint256(fee), BoundUtils.toPercent(1), BoundUtils.toPercent(2)));
    vm.startPrank($.owner);
    if (protocolFee != $.dahlia.getMarket($.marketId).protocolFeeRate) {
        $.dahlia.setProtocolFeeRate($.marketId, protocolFee);
    }
    if (reserveFee != $.dahlia.getMarket($.marketId).reserveFeeRate) {
        $.dahlia.setReserveFeeRate($.marketId, reserveFee);
    }
    vm.stopPrank();
    blocks = vm.boundBlocks(blocks);
    IDahlia.Market memory state = $.dahlia.getMarket($.marketId);
    uint256 totalBorrowBeforeAccrued = state.totalBorrowAssets;
    uint256 totalLendBeforeAccrued = state.totalLendAssets;
    uint256 totalLendSharesBeforeAccrued = state.totalLendShares;
    uint256 deltaTime = blocks * TestConstants.BLOCK_TIME;
    (uint256 interestEarnedAssets, uint256 newRatePerSec,) =
        $.marketConfig.irm.calculateInterest(
            deltaTime,
            state.totalLendAssets,
            state.totalBorrowAssets,
            state.fullUtilizationRate
        );
    uint256 protocolFeeShares = InterestImpl.calcFeeSharesFromInterest(
        state.totalLendAssets,
        state.totalLendShares,
        interestEarnedAssets,
        protocolFee
    );
    uint256 reserveFeeShares = InterestImpl.calcFeeSharesFromInterest(
        state.totalLendAssets,
        state.totalLendShares,
        interestEarnedAssets,
        reserveFee
    );
    vm.forward(blocks);
    if (interestEarnedAssets > 0) {
        vm.expectEmit(true, true, true, true, address($.dahlia));
        emit IDahlia.DahliaAccrueInterest(
            $.marketId,
            newRatePerSec,
            interestEarnedAssets,
            protocolFeeShares,
            reserveFeeShares
        );
    }
    $.dahlia.accrueMarketInterest($.marketId);
    IDahlia.Market memory stateAfter = $.dahlia.getMarket($.marketId);
    assertEq(stateAfter.totalLendAssets, totalLendBeforeAccrued + interestEarnedAssets, "total supply");
    assertEq(stateAfter.totalBorrowAssets, totalBorrowBeforeAccrued + interestEarnedAssets, "total borrow");
    assertEq(
        stateAfter.totalLendShares,
        totalLendSharesBeforeAccrued + protocolFeeShares + reserveFeeShares,
        "total lend shares"
    );
    IDahlia.UserPosition memory userPos1 = $.dahlia.getPosition($.marketId,
        ctx.wallets("PROTOCOL_FEE_RECIPIENT"));
    IDahlia.UserPosition memory userPos = $.dahlia.getPosition($.marketId,
        ctx.wallets("RESERVE_FEE_RECIPIENT"));
    assertEq(userPos1.lendShares, protocolFeeShares, "protocolFeeRecipient's lend shares");
    assertEq(userPos.lendShares, reserveFeeShares, "reserveFeeRecipient's lend shares");
    if (interestEarnedAssets > 0) {
        assertEq(stateAfter.updatedAt, block.timestamp, "last update");
    }
    + IDahlia.Market memory m = $.dahlia.getMarket($.marketId);
    + WrappedVault vault = WrappedVault(address(m.vault));
    + // Ensure both fee recipients have zero WrappedVault balances
    + assertEq(
    +     vault.balanceOf(address(ctx.wallets("RESERVE_FEE_RECIPIENT"))),
    +     0,
    +     "reserveFeeRecipient 's wrappedVault balance"
    + );
    + assertEq(
    +     vault.balanceOf(address(ctx.wallets("PROTOCOL_FEE_RECIPIENT"))),
    +     0,
    +     "protocolFeeRecipient 's wrappedVault balance"
    + );
    + // Verify that withdrawing directly from Dahlia fails for both fee recipients
    + address reserveFeeRecipient = ctx.wallets("RESERVE_FEE_RECIPIENT");
    + vm.startPrank(reserveFeeRecipient);
    + vm.expectRevert();
    + $.dahlia.withdraw($.marketId, userPos.lendShares, reserveFeeRecipient, reserveFeeRecipient);
    + vm.stopPrank();
    + address protocolFeeRecipient = ctx.wallets("PROTOCOL_FEE_RECIPIENT");
    + vm.startPrank(protocolFeeRecipient);
    + vm.expectRevert();
    + $.dahlia.withdraw($.marketId, userPos1.lendShares, protocolFeeRecipient, protocolFeeRecipient);
    + vm.stopPrank();
}
```

## Recommendation
Add an additional function that allows the protocol fee recipient and reserve fee recipient to withdraw.

### Status
- **Dahlia:** Fixed in commit `bb8ce8fa`.
- **Cantina Managed:** Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Dahlia |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, kankodu, Yorke Rhodes |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443

### Keywords for Search

`vulnerability`

