---
# Core Classification
protocol: Hybra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63712
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-10-hybra-finance
source_link: https://code4rena.com/reports/2025-10-hybra-finance
github_link: https://code4rena.com/audits/2025-10-hybra-finance/submissions/S-356

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
finders_count: 3
finders:
  - osok
  - Ibukun
  - odeili
---

## Vulnerability Title

[M-05] Rollover rewards are permanently lost due to flawed `rewardRate` calculation

### Overview


Bug report summary: A bug was found in the `GaugeCL.sol` contract of Hybra Finance by V12. The `notifyRewardAmount()` function miscalculates the `rewardRate` when a new epoch begins, causing rollover rewards from previous epochs to be permanently lost. This results in a permanent loss of funds, reduced LP yields, and waste of protocol resources. The recommended mitigation steps include correcting the `rewardRate` calculation to include the rollover amount. A proof of concept test is provided to reproduce the issue. The bug has been mitigated by Hybra Finance.

### Original Finding Content



*This issue was also [found](https://code4rena.com/audits/2025-10-hybra-finance/submissions/S-629) by [V12](https://v12.zellic.io).*

`GaugeCL.sol` [# L256](https://github.com/code-423n4/2025-10-hybra-finance/blob/66c42f3c9754f1b38942c69ebc0d3e4c0f8fdeb2/ve33/contracts/CLGauge/GaugeCL.sol# L256)

### Summary

The `notifyRewardAmount()` function miscalculates the `rewardRate` when a new epoch begins, causing `rollover` rewards from previous epochs to be permanently lost.

When `block.timestamp >= _periodFinish`, the function adds both the new `rewardAmount` and the previous epoch’s `clPool.rollover()` to form the `totalRewardAmount`. However, the `rewardRate` is derived only from `rewardAmount`, ignoring the rollover portion:
```

// @audit The total amount to be reserved includes rollover...
uint256 totalRewardAmount = rewardAmount + clPool.rollover();
if (block.timestamp >= _periodFinish) {
    // @audit but the rate calculation completely ignores the rollover.
    rewardRate = rewardAmount / epochTimeRemaining;

    // @audit The pool is synced with a CORRECT reserve but an INCORRECTLY LOW rate.
    clPool.syncReward({
        rewardRate: rewardRate,
        rewardReserve: totalRewardAmount, // Correct total
        periodFinish: epochEndTimestamp
    });
}
```

This mismatch means the pool receives the full reserve (new + rollover) but emits rewards too slowly to deplete it. The rollover portion remains stranded, and when the next epoch begins, it is overwritten and effectively erased.
The logic in the `else` branch fails to correct this issue; instead, it perpetuates the error. The updated rate is calculated using the old, already flawed `rewardRate`, ensuring that once `rollover` funds are stranded, they can never be reclaimed through subsequent reward notifications.

### Impact

1. Permanent Loss of Funds: Unclaimed rollover rewards are locked in the contract and cannot be recovered.
2. Reduced LP Yields: Liquidity providers earn less than intended, as part of their entitled rewards never distribute.
3. Protocol Resource Waste: Tokens from the treasury or partners are effectively burned, wasting incentive funds.

### Recommended mitigation steps

The `rewardRate` calculation should include the `rollover` amount to ensure the emission rate matches the total rewards available for distribution. This change guarantees that all `rollover` rewards are correctly accounted for and eventually distributed.
In `GaugeCL.sol`:
```

-   rewardRate = rewardAmount / epochTimeRemaining;
+   rewardRate = totalRewardAmount / epochTimeRemaining;
    clPool.syncReward({
        rewardRate: rewardRate,
        rewardReserve: totalRewardAmount,
        periodFinish: epochEndTimestamp })
```

Proof of concept

The following test reproduces the issue in three steps:

1. Add `100 ether` as rewards, then warp time forward so the entire amount becomes rollover.
2. Add `50 ether` as new rewards, triggering the flawed logic. The CLPool’s reserve is now `150 ether`, but the rate only allows `50 ether` to be distributed.
3. After another time warp and update, the pool’s accounted reserve is ~50 ether, while the actual gauge balance is `150 ether`. The ~100 ether difference represents the permanently lost rewards.
4. Copy the test below into `cl/test/C4PoC.t.sol`, then run: `forge test --mt test_PoC_RolloverRewardsAreLost -vv`

   
```

   import "forge-std/Test.sol";
   import "forge-std/console2.sol"; // Using console2 for better compatibility
   import {C4PoCTestbed} from "./C4PoCTestbed.t.sol";
   
```

import {MockERC20} from “contracts/mocks/MockERC20.sol”;
import {ICLPool} from “contracts/core/interfaces/ICLPool.sol”;
import {INonfungiblePositionManager} from “contracts/periphery/interfaces/INonfungiblePositionManager.sol”;

// =========================================================================================
// MOCK CONTRACT FOR THE POC
// Purpose: This mock contract isolates the specific vulnerable function from the full
// CLGauge contract. This allows for a focused test that is easy to understand and audit.
// =========================================================================================

contract MockVulnerableCLGauge\_Rollover {
ICLPool public immutable clPool;
MockERC20 public immutable rewardToken;
address public immutable DISTRIBUTION;
```

uint256 public _periodFinish;
uint256 public rewardRate;

constructor(address _clPool, address _rewardToken, address _distribution) {
    clPool = ICLPool(_clPool);
    rewardToken = MockERC20(_rewardToken);
    DISTRIBUTION = _distribution;
}

function _epochNext(uint256 timestamp) internal pure returns (uint256) {
    uint256 week = 604800;
    return ((timestamp / week) + 1) * week;
}

// THE VULNERABLE FUNCTION: A direct copy of the buggy logic from the original CLGauge contract
function notifyRewardAmount(address token, uint256 rewardAmount) external {
    require(msg.sender == DISTRIBUTION, "Only distribution");
    require(token == address(rewardToken), "Invalid reward token");
    clPool.updateRewardsGrowthGlobal();
    uint256 epochTimeRemaining = _epochNext(block.timestamp) - block.timestamp;
    uint256 epochEndTimestamp = block.timestamp + epochTimeRemaining;
    uint256 totalRewardAmount = rewardAmount + clPool.rollover();
    if (block.timestamp >= _periodFinish) {

        // `rewardRate` is calculated using ONLY the new `rewardAmount`.
        // It completely ignores the `clPool.rollover()` amount that was just calculated.
        rewardRate = rewardAmount / epochTimeRemaining;

        // The pool is synced with a CORRECT `rewardReserve` (including rollover)
        // but an INCORRECTLY LOW `rewardRate`. This mismatch is the root cause of the fund loss.
        clPool.syncReward({
            rewardRate: rewardRate,
            rewardReserve: totalRewardAmount,
            periodFinish: epochEndTimestamp
        });
    } else {
        revert("PoC focuses on the new reward period scenario");
    }
    rewardToken.transferFrom(DISTRIBUTION, address(this), rewardAmount);
    _periodFinish = epochEndTimestamp;
}
```

}

contract C4PoC is C4PoCTestbed {
function setUp() public override {
super.setUp();
}
```

function test_PoC_RolloverRewardsAreLost() public {
    // Step 1: Create a CL pool and necessary mock contracts for the test.
    address token0 = WETH < USDC ? WETH : USDC;
    address token1 = WETH < USDC ? USDC : WETH;

    uint256 amount0ToMint = 4000 * 1e6;
    uint256 amount1ToMint = 1 ether;

    MockERC20(token0).mint(deployer, amount0ToMint);
    MockERC20(token1).mint(deployer, amount1ToMint);

    vm.prank(deployer);
    MockERC20(token0).approve(address(nonfungiblePositionManager), type(uint256).max);
    vm.prank(deployer);
    MockERC20(token1).approve(address(nonfungiblePositionManager), type(uint256).max);

    vm.startPrank(deployer);
    nonfungiblePositionManager.mint(INonfungiblePositionManager.MintParams({
            token0: token0, token1: token1, tickSpacing: 2000,
            tickLower: -200000, tickUpper: 200000,
            amount0Desired: amount0ToMint,
            amount1Desired: amount1ToMint,
            amount0Min: 0, amount1Min: 0,
            recipient: deployer, deadline: block.timestamp,
            sqrtPriceX96: 2505414483750479311864138015344742
        }));
    vm.stopPrank();

    ICLPool clPool = ICLPool(poolFactory.getPool(token0, token1, 2000));
    assertTrue(address(clPool) != address(0), "Pool creation failed");

    // Step 2: Deploy our mock gauge and authorize it on the pool.
    // We use `vm.store` to bypass complex authorization mechanisms and directly
    // write our mock gauge's address into the pool's `gauge` storage slot (slot 3).
    MockERC20 rewardToken = new MockERC20("RewardToken", "RWD", 18);
    address rewardDistributor = makeAddr("rewardDistributor");
    MockVulnerableCLGauge_Rollover mockGauge = new MockVulnerableCLGauge_Rollover(
        address(clPool), address(rewardToken), rewardDistributor
    );

    bytes32 GAUGE_STORAGE_SLOT = bytes32(uint256(3));
    vm.store(
        address(clPool),
        GAUGE_STORAGE_SLOT,
        bytes32(uint256(uint160(address(mockGauge))))
    );
    assertEq(clPool.gauge(), address(mockGauge));

    uint256 reward1_to_be_lost = 100 ether;
    uint256 reward2_retained = 50 ether;
    rewardToken.mint(rewardDistributor, reward1_to_be_lost + reward2_retained);
    vm.prank(rewardDistributor);
    rewardToken.approve(address(mockGauge), type(uint256).max);

    // Step 3: EPOCH 1: Create a rollover situation
    // PRE-CONDITION: The pool has 0 staked liquidity, which is essential for this PoC
    // as it guarantees 100% of the undistributed reward will become rollover.
    vm.prank(rewardDistributor);
    mockGauge.notifyRewardAmount(address(rewardToken), reward1_to_be_lost);
    vm.warp(clPool.periodFinish() + 1);

    // Distribute 50 ether, triggering the vulnerability.
    vm.prank(rewardDistributor);
    mockGauge.notifyRewardAmount(address(rewardToken), reward2_retained);

    // Advance time and notify with 0. This finalizes the loss.
    vm.warp(clPool.periodFinish() + 1);
    vm.prank(rewardDistributor);
    mockGauge.notifyRewardAmount(address(rewardToken), 0);

    // Step 4: ASSERTION & PROOF
    uint256 finalGaugeBalance = rewardToken.balanceOf(address(mockGauge));
    uint256 finalPoolReserve = clPool.rewardReserve();
    uint256 lostAmount = finalGaugeBalance - finalPoolReserve;

    console2.log("--- Rollover Bug PoC Results ---");
    console2.log("Physical Token Balance in Gauge:", finalGaugeBalance);
    console2.log("Accounted Reward Reserve in Pool:", finalPoolReserve);
    console2.log("Amount of Stuck/Lost Tokens:", lostAmount);

    // Core Proof: The pool's final accounted reserve should only reflect the SECOND reward.
    // The first 100 ether reward has vanished from its books.
    uint256 dustTolerance = 1 ether; // A generous tolerance of 1 full token
    assertApproxEqAbs(
        finalPoolReserve,
        reward2_retained,
        dustTolerance,
        "BUG: Pool reserve should be approximately 50 ether"
    );

    // Final check: The amount of lost funds must equal the first reward.
    assertApproxEqAbs(
        lostAmount,
        reward1_to_be_lost,
        dustTolerance,
        "BUG: The lost amount should be approximately 100 ether"
    );
}
```

}
```

</details>

**[Hybra Finance mitigated](https://github.com/code-423n4/2025-11-hybra-finance-mitigation?tab=readme-ov-file# mitigations-of-high--medium-severity-issues):**
> fix - S-36 ClaimFees Steals Staking Rewards
> fix - S-841 rollover rewardRate calcuate
> fix - S-645 Missing unchecked block in Gauge Dependent Library Will Cause Freezing of Reward Calculations

**Status:** Mitigation confirmed. Full details in the [mitigation review reports from niffylord, rayss, and ZanyBonzy](https://code4rena.com/audits/2025-11-hybra-finance-mitigation-review/submissions/S-21).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Hybra Finance |
| Report Date | N/A |
| Finders | osok, Ibukun, odeili |

### Source Links

- **Source**: https://code4rena.com/reports/2025-10-hybra-finance
- **GitHub**: https://code4rena.com/audits/2025-10-hybra-finance/submissions/S-356
- **Contest**: https://code4rena.com/reports/2025-10-hybra-finance

### Keywords for Search

`vulnerability`

