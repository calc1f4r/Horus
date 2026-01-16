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
solodit_id: 57171
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 66
finders:
  - victortheoracle
  - nikolaihristov1999
  - vs_
  - allamloqman
  - holydevoti0n
---

## Vulnerability Title

Incorrect DebtToken totalSupply Scaling Breaks Interest Rate Calculations

### Overview


This bug report highlights an issue with the `DebtToken` contract that affects the interest rate calculations in the protocol. The problem lies in the `totalSupply` function, which always returns a scaled-down value instead of scaling it up. This leads to incorrect utilization rates, interest rates, and liquidation thresholds, which can break the protocol's economic model. The bug can be fixed by changing the scaling direction in the `totalSupply` function. 

### Original Finding Content

## Summary

The `DebtToken` contract has an arithmetic error in its `totalSupply` function that causes it to always return a scaled-down value instead of scaling it up, leading to incorrect utilization rate calculations throughout the protocol. This affects interest rate calculations, liquidations and index calulation.

## Vulnerability Details

### Source

* [DebtToken.sol - totalSupply](https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/tokens/DebtToken.sol)

The issue lies in the incorrect scaling direction in `totalSupply`:

```solidity
function totalSupply() public view override(ERC20, IERC20) returns (uint256) {
    uint256 scaledSupply = super.totalSupply();
    return scaledSupply.rayDiv(ILendingPool(_reservePool).getNormalizedDebt()); // @audit should be rayMul
}
```

This scaled total supply is then used in multiple critical protocol functions:

1. In `LendingPool::finalizeLiquidation`:

```solidity
function finalizeLiquidation(address userAddress) external nonReentrant onlyStabilityPool {
    // ...
    reserve.totalUsage = newTotalSupply; // @audit uses incorrectly scaled totalSupply
    // ...
    ReserveLibrary.updateInterestRatesAndLiquidity(reserve, rateData, amountScaled, 0);
}
```

1. In `LendingPool::borrow`:

```solidity
function borrow(uint256 amount) external nonReentrant whenNotPaused onlyValidAmount(amount) {
    // ...
    reserve.totalUsage = newTotalSupply; // @audit uses incorrectly scaled totalSupply
    // ...
    ReserveLibrary.updateInterestRatesAndLiquidity(reserve, rateData, amountScaled, 0);
}
```

1. The incorrect scaling propagates to interest rate calculations in `ReserveLibrary`:

```solidity
function updateInterestRatesAndLiquidity(
    ReserveData storage reserve,
    ReserveRateData storage rateData,
    uint256 liquidityAdded,
    uint256 liquidityTaken
) internal {
    uint256 totalLiquidity = reserve.totalLiquidity;
    uint256 totalDebt = reserve.totalUsage; // @audit uses incorrectly scaled totalSupply

    uint256 utilizationRate = calculateUtilizationRate(reserve.totalLiquidity, reserve.totalUsage);

    // These rates are all calculated with incorrect utilization
    rateData.currentUsageRate = calculateBorrowRate(
        rateData.primeRate,
        rateData.baseRate,
        rateData.optimalRate,
        rateData.maxRate,
        rateData.optimalUtilizationRate,
        utilizationRate
    );

    rateData.currentLiquidityRate = calculateLiquidityRate(
        utilizationRate,
        rateData.currentUsageRate,
        rateData.protocolFeeRate,
        totalDebt
    );
}
```

### POC

```solidity

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {Test} from "forge-std/Test.sol";
import {DebtToken} from "../contracts/core/tokens/DebtToken.sol";
import "../contracts/libraries/math/WadRayMath.sol";
import {console} from "forge-std/console.sol";

contract MockLendingPool {
    function getNormalizedDebt() external pure returns (uint256) {
        return 1.1e27; // Setting the normalized debt to 1.1 in ray
    }
}

contract DebtTokenPoc is Test {
    using WadRayMath for uint256;

    DebtToken debtToken;
    address owner;
    address user1;
    MockLendingPool lendingPool;

    function setUp() public {
        lendingPool = new MockLendingPool();
        owner = address(this);
        user1 = makeAddr("user1");

        debtToken = new DebtToken("DebtToken", "DT", owner);
        debtToken.setReservePool(address(lendingPool));

        // Mint some initial supply - using the mint function with index
        vm.startPrank(address(lendingPool));
        debtToken.mint(user1, user1, 1000e18, WadRayMath.RAY);
        vm.stopPrank();
    }

    function test_incorrect_total_supply_scaling() public {
        // Get the total supply
        uint256 totalSupply = debtToken.totalSupply();
        uint256 scaledTotalSupply = debtToken.scaledTotalSupply();

        console.log("Scaled total supply: %s", scaledTotalSupply);
        console.log("Total supply (incorrectly scaled down): %s", totalSupply);
        console.log("Total supply (should be scaled up): %s", scaledTotalSupply.rayMul(1.1e27));

        // This will pass because totalSupply is incorrectly scaled down
        assertFalse(totalSupply > scaledTotalSupply, "Total supply should be larger than scaled supply");
    }

    function test_utilization_rate_impact() public {
        uint256 totalLiquidity = 1000e18;
        uint256 incorrectTotalDebt = debtToken.totalSupply();
        uint256 correctTotalDebt = debtToken.scaledTotalSupply().rayMul(1.1e27);

        // Calculate utilization rates
        uint256 incorrectUtilization = (incorrectTotalDebt * 1.1e27) / totalLiquidity;
        uint256 correctUtilization = (correctTotalDebt * 1.1e27) / totalLiquidity;

        console.log("Incorrect utilization rate: %s", incorrectUtilization);
        console.log("Correct utilization rate: %s", correctUtilization);

        assertTrue(incorrectUtilization < correctUtilization, "Utilization rate is underreported");
    }
}

```

### Impact of Incorrect Scaling

For example, with a normalizedDebt of 1.1:

* Actual total supply: 1000 tokens
* Current incorrect scaling: 1000 / 1.1 ≈ 909.09 tokens
* Correct scaling should be: 1000 \* 1.1 = 1100 tokens

This means:

1. Utilization rates are severely underreported
2. Interest rates are miscalculated
3. Liquidation thresholds may not trigger when they should
4. Protocol's economic model is fundamentally broken

## Tools Used

* Manual code review

## Recommendations

1. Fix the scaling direction in DebtToken::totalSupply:

```diff
function totalSupply() public view override(ERC20, IERC20) returns (uint256) {
    uint256 scaledSupply = super.totalSupply();
-   return scaledSupply.rayDiv(ILendingPool(_reservePool).getNormalizedDebt());
+   return scaledSupply.rayMul(ILendingPool(_reservePool).getNormalizedDebt());
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | victortheoracle, nikolaihristov1999, vs_, allamloqman, holydevoti0n, t0x1c, petersr, davide, bshyuunn, wickie, frndz0ne, kapten_crtz, patitonar, 0xb0k0, takarez, 0x23r0, kwakudr, robertodf99, hailthelord, ace_30, attentioniayn, kiteweb3, farismaulana, aksoy, notbozho, greese, mahdikarimi, saurabh_singh, tadev, recur, danzero, bluedragon, opecon, olugbenga, iam0ti, calc1f4r, zwang88, 0xbrett8571, cipherhawk, 0xlouistsai, kirobrejka, agent3bood, whitekittyhacker, almur100, mill1995, sl1, h2134, wiasliaw, 01chenqing, oldmonk, oxelmiguel, io10, tinnohofficial, joicygiore, trtrth, gritty, lyuboslav, meeve, ibukunola, xcrypt, infect3d, udogodwin2k22, 0xphantom, elhajin, glightspeed2 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

