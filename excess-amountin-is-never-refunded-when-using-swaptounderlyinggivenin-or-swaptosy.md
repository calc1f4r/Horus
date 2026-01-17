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
solodit_id: 54135
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
  - t0x1c
---

## Vulnerability Title

Excess amountIn is never refunded when using swapToUnderlyingGivenIn() or swapToSynth- GivenIn() 

### Overview

See description below for full details.

### Original Finding Content

## PegStabilityModule Issue Overview

## Context
- `PegStabilityModule.sol#L75-L78`
- `PegStabilityModule.sol#L107-L110`

## Description
In the DeFi space, it's standard practice that when users call the `swap()` function, any excess `amountIn` that is not needed for the `amountOut` swap is returned. However, in Euler, due to the protocol's rounding-down rules, any extra Synth or Underlying specified during `swapToUnderlyingGivenIn()` or `swapToSynthGivenIn()` is burned and not returned to the user.

### Scenario Explanation
Consider the following scenario, which has been reproduced in a Proof of Concept (PoC). Please refer to those tests for verifying the numbers:

- Alice wants to swap some of her Synth to receive 290,000 ether of the underlying.
- Assume a fee of 70% and a conversion rate of 1e18.

### Two Options
1. **Option 1**:
   - Alice can use the `swapToUnderlyingGivenOut()` function by specifying `amountOut` as 290,000 ether.
   - The PoC reveals that the protocol burns 966,666,666,666,666,666,666,666 of Alice's Synth and transfers 290,000 ether of the underlying.

2. **Option 2**:
   - Alice calls `swapToUnderlyingGivenIn()`, specifying `amountIn` as 966,666,666,666,666,666,666,669 (virtually sending an additional 3 wei of Synth).
   - The protocol burns all of this Synth while still providing Alice with 290,000 ether of the underlying.
   - The additional 3 wei are also burned and never returned to Alice.

This pattern is similarly observed when users swap the other way round using `swapToSynthGivenIn()`, as shown in the PoC. 

### Key Takeaway
The conversion rate is not strictly observed here, potentially skewing results if multiple users engage in this behavior.

## Proof of Concept
To examine this, add the following file at `test/unit/pegStabilityModules/IncorrectPegSwap.t.sol` and run both tests using:
```
forge test --mt test_t0x1c -vv
```

### Code Snippet
```solidity
// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;
import "forge-std/Test.sol";
import {PegStabilityModule, EVCUtil} from "../../../src/Synths/PegStabilityModule.sol";
import {ESynth, IEVC} from "../../../src/Synths/ESynth.sol";
import {TestERC20} from "../../mocks/TestERC20.sol";
import {EthereumVaultConnector} from "ethereum-vault-connector/EthereumVaultConnector.sol";

contract IncorrectPegSwap is Test {
    uint256 public TO_UNDERLYING_FEE = 7000;
    uint256 public TO_SYNTH_FEE = 7000;
    uint256 public BPS_SCALE = 10000;
    ESynth public synth;
    TestERC20 public underlying;
    PegStabilityModule public psm;
    IEVC public evc;
    address public owner = makeAddr("owner");
    address public wallet1 = makeAddr("wallet1");
    address public wallet2 = makeAddr("wallet2");

    function setUp() public {
        // Deploy EVC
        evc = new EthereumVaultConnector();
        // Deploy underlying
        underlying = new TestERC20("TestUnderlying", "TUNDERLYING", 18, false);
        // Deploy synth
        vm.prank(owner);
        synth = new ESynth(evc, "TestSynth", "TSYNTH");
        // Deploy PSM
        vm.prank(owner);
        psm = new PegStabilityModule(address(evc), address(synth), address(underlying), TO_UNDERLYING_FEE, TO_SYNTH_FEE, 1e18);
        vm.label(address(psm), "_PSM_");
        // Give PSM and wallets some underlying
        underlying.mint(address(psm), type(uint128).max / 2);
        underlying.mint(wallet1, type(uint128).max / 2);
        // Approve PSM to spend underlying
        vm.startPrank(wallet1);
        underlying.approve(address(psm), type(uint128).max - 1);
        synth.approve(address(psm), type(uint128).max - 1);
        vm.stopPrank();
        // Set PSM as minter
        vm.prank(owner);
        synth.setCapacity(address(psm), type(uint128).max);
        // Mint some synth to wallets
        vm.startPrank(owner);
        synth.setCapacity(owner, type(uint128).max);
        synth.mint(wallet1, type(uint128).max / 2);
        vm.stopPrank();
    }

    function test_t0x1c_SwapToUnderlying() public {
        uint256 amountOut = 290_000e18;
        vm.startPrank(wallet1);
        uint256 aIn = psm.swapToUnderlyingGivenOut(amountOut, wallet2);
        emit log_named_decimal_uint("synthAmountIn (Case 1)", aIn, 18);
        uint256 balanceBefore = synth.balanceOf(wallet1);
        uint256 aOut = psm.swapToUnderlyingGivenIn(aIn + 3, wallet2); // @audit-info : extra 3 wei supplied by the user while swapping
        assertEq(aOut, amountOut);
        emit log_named_decimal_uint("synthAmountIn (Case 2)", balanceBefore - synth.balanceOf(wallet1), 18);
        assertGt(balanceBefore - synth.balanceOf(wallet1), aIn); // @audit : Excess funds never returned
    }

    function test_t0x1c_SwapToSynth() public {
        uint256 amountOut = 290_000e18;
        vm.startPrank(wallet1);
        uint256 aIn = psm.swapToSynthGivenOut(amountOut, wallet2);
        emit log_named_decimal_uint("underlyingAmountIn (Case 1)", aIn, 18);
        uint256 balanceBefore = underlying.balanceOf(wallet1);
        uint256 aOut = psm.swapToSynthGivenIn(aIn + 3, wallet2); // @audit-info : extra 3 wei supplied by the user while swapping
        assertEq(aOut, amountOut);
        emit log_named_decimal_uint("underlyingAmountIn (Case 2)", balanceBefore - underlying.balanceOf(wallet1), 18);
        assertGt(balanceBefore - underlying.balanceOf(wallet1), aIn); // @audit : Excess funds never returned
    }
}
```
### Output
```
Ran 2 tests for test/unit/pegStabilityModules/IncorrectPegSwap.t.sol:PSMTest
[PASS] test_t0x1c_SwapToSynth() (gas: 110085)
Logs:
underlyingAmountIn (Case 1): 966666.666666666666666666
underlyingAmountIn (Case 2): 966666.666666666666666669
[PASS] test_t0x1c_SwapToUnderlying() (gas: 110574)
Logs:
synthAmountIn (Case 1): 966666.666666666666666666
synthAmountIn (Case 2): 966666.666666666666666669
```

## Recommendation
To solve this issue, perform a reverse calculation to determine the actual minimum `amountIn` required and only burn/pull that amount:

### Suggested Code Change
For `swapToUnderlyingGivenIn`:
```solidity
function swapToUnderlyingGivenIn(uint256 amountIn, address receiver) external returns (uint256) {
    uint256 amountOut = quoteToUnderlyingGivenIn(amountIn);
    if (amountIn == 0 || amountOut == 0) {
        return 0;
    }
    uint256 amountInRequired = amountOut * BPS_SCALE * PRICE_SCALE / (BPS_SCALE - TO_UNDERLYING_FEE) / conversionPrice;
    synth.burn(_msgSender(), amountInRequired);
    underlying.safeTransfer(receiver, amountOut);
    return amountOut;
}
```

For `swapToSynthGivenIn`:
```solidity
function swapToSynthGivenIn(uint256 amountIn, address receiver) external returns (uint256) {
    uint256 amountOut = quoteToSynthGivenIn(amountIn);
    if (amountIn == 0 || amountOut == 0) {
        return 0;
    }
    uint256 amountInRequired = amountOut * BPS_SCALE * conversionPrice / (BPS_SCALE - TO_SYNTH_FEE) / PRICE_SCALE;
    underlying.safeTransferFrom(_msgSender(), address(this), amountInRequired);
    synth.mint(receiver, amountOut);
    return amountOut;
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | t0x1c |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

