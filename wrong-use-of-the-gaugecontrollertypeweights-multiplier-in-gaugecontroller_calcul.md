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
solodit_id: 57161
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
finders_count: 4
finders:
  - heheboii
  - glightspeed2
  - uddercover
  - kodyvim
---

## Vulnerability Title

Wrong use of the `GaugeController::typeWeights` multiplier in `GaugeController::_calculateReward` causes a reduction in gauge rewards instead

### Overview


Summary:

The code for calculating rewards in the GaugeController contract is incorrect, causing a reduction in the amount of rewards received. This is because the typeWeights multiplier is used as a divisor instead of a multiplier. The vulnerability was discovered through manual review and testing. It is recommended to fix the code by adding an additional calculation to the return statement.

### Original Finding Content

## Summary

Wrong use of the `GaugeController::typeWeights` multiplier in `GaugeController::_calculateReward` causes a reduction in gauge rewards instead

## Vulnerability Details

In the code docs, typeWeights are specified as multipliers for the actual gauge weight.

```Solidity
     /**
     * @notice Type weights and periods
     * @dev Tracking for gauge type weights and their time periods
@>   * typeWeights: Weight multipliers for each gauge type
     * typePeriods: Period data for each gauge type
     */
    mapping(GaugeType => uint256) public typeWeights;
```

But the way it is used in \`GaugeController::\_calculateReward\` , makes it a divisor instead. 

```Solidity
function _calculateReward(address gauge) public view returns (uint256) {
        .
        .
        .
  
@>      uint256 typeShare = (typeWeights[g.gaugeType] * WEIGHT_PRECISION) / MAX_TYPE_WEIGHT;

        // Calculate period emissions based on gauge type
        uint256 periodEmission = g.gaugeType == GaugeType.RWA ? _calculateRWAEmission() : _calculateRAACEmission();
@>     return (periodEmission * gaugeShare * typeShare) / (WEIGHT_PRECISION * WEIGHT_PRECISION);
    }
```

This makes the final reward returned, significantly less than expected.

**POC**

To use foundry in the codebase, follow the hardhat guide here: [Foundry-Hardhat hybrid integration by Nomic foundation](https://hardhat.org/hardhat-runner/docs/advanced/hardhat-and-foundry)

```Solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {ERC20Mock} from "../../../../contracts/mocks/core/tokens/ERC20Mock.sol";
import {FeeCollector} from "../../../../contracts/core/collectors/FeeCollector.sol";
import {Treasury} from "../../../../contracts/core/collectors/Treasury.sol";
import {RAACToken} from "../../../../contracts/core/tokens/RAACToken.sol";
import {veRAACToken} from "../../../../contracts/core/tokens/veRAACToken.sol";
import {GaugeController, IGaugeController} from "../../../../contracts/core/governance/gauges/GaugeController.sol";
import {RAACGauge} from "../../../../contracts/core/governance/gauges/RAACGauge.sol";
import {Test, console} from "forge-std/Test.sol";

contract UnitTest is Test {
    FeeCollector feeCollector;
    Treasury treasury;
    RAACToken raacToken;
    veRAACToken veRAACTok;
    GaugeController gaugeController;
    RAACGauge raacGauge;
    RAACGauge raacGauge2;
    address repairFund;
    address admin;
    address rewardToken;
    uint256 initialSwapTaxRate = 100; //1%
    uint256 initialBurnTaxRate = 50; //0.5%

    function setUp() public {
        repairFund = makeAddr("repairFund");
        admin = makeAddr("admin");
        rewardToken = address(new ERC20Mock("Reward Token", "RWT"));

        treasury = new Treasury(admin);

        raacToken = new RAACToken(admin, initialSwapTaxRate, initialBurnTaxRate);
        veRAACTok = new veRAACToken(address(raacToken));
        feeCollector = new FeeCollector(address(raacToken), address(veRAACTok), address(treasury), repairFund, admin);

        vm.startPrank(admin);
        raacToken.setFeeCollector(address(feeCollector));
        raacToken.setMinter(admin);
        gaugeController = new GaugeController(address(veRAACTok));
        raacGauge = new RAACGauge(rewardToken, address(veRAACTok), address(gaugeController));
        raacGauge2 = new RAACGauge(rewardToken, address(veRAACTok), address(gaugeController));
        vm.stopPrank();
    }

    function testTypeWeightMultiplierDecreasesRewardsInstead() public {
        uint256 initialWeight = 5000; //50%

        //admin creates and adds gauges
        vm.startPrank(admin);
        gaugeController.addGauge(address(raacGauge), IGaugeController.GaugeType.RAAC, initialWeight);
        gaugeController.addGauge(address(raacGauge2), IGaugeController.GaugeType.RAAC, initialWeight);
        vm.stopPrank();

        // At least 50% of the periodEmission should go to the gauge
        uint256 periodEmission = gaugeController._calculateRAACEmission();
        uint256 expectedMinimumReward = periodEmission / 2;
        uint256 reward = gaugeController._calculateReward(address(raacGauge));

        // reward is less than the expected minimum by 50%/5000 bips which is the value of typeshare
        console.log("Period emission: ", periodEmission);
        console.log("Reward: ", reward);
        console.log("Expected minimum reward: ", expectedMinimumReward);
        assertLt(reward, expectedMinimumReward);
    }
```

## Impact

Reward allocated is significantly reduced

## Tools Used

Manual review, foundry test suite

## Recommendations

```diff
function _calculateReward(address gauge) public view returns (uint256) {
        .
        .
        .
-       return (periodEmission * gaugeShare * typeShare) / (WEIGHT_PRECISION * WEIGHT_PRECISION);
+       return ((periodEmission * gaugeShare * typeShare) / (WEIGHT_PRECISION * WEIGHT_PRECISION)) + ((periodEmission * gaugeShare) / (WEIGHT_PRECISION));
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
| Finders | heheboii, glightspeed2, uddercover, kodyvim |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

