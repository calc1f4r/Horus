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
solodit_id: 54190
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
finders_count: 2
finders:
  - Alex The Entreprenerd
  - Akshay Srivastav
---

## Vulnerability Title

IRM synth rate always moves even when no trade is possible due to swap fees 

### Overview

See description below for full details.

### Original Finding Content

## Impact of IRMSynth Fee Logic

## Context
IRMSynth.sol#L88-L101

## Impact
All swaps have fees, both in the PSM as well as on any AMM. The logic for IRM Synth to compute its next interest rate is as follows:

```solidity
if (quote < targetQuote) {
    // If the quote is less than the target, increase the rate
    rate = rate * ADJUST_FACTOR / ADJUST_ONE;
} else {
    // If the quote is greater than the target, decrease the rate
    rate = rate * ADJUST_ONE / ADJUST_FACTOR;
}
```

The logic for `_computeRate` in `IRMSynth` is computing a price; however, this spot price will not include:
- The Oracle Drift.
- The Swap Fees necessary to move the price.
- The gas cost necessary to move the price.

This will result in interest rates changing even when no actual arbitrage or market making operation is possible.

## Proof of Concept
- Get any quote price.
- See that the actual execution inclusive of fees will be higher cost.
- Borrowers are being charged incorrectly as the price inclusive of fees should not move the rate in that direction.

The proof of concept will run with the following logs, showing how a No-Arb opportunity causes rates to increase:

- `quote` 999999999999999999
- `withFee` 989999999999999999
- `startRate` 158443692534057154
- `endRate` 1716690817191148858

## Solidity Code
```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import {EVaultTestBase} from "./EVaultTestBase.t.sol";
import "src/EVault/shared/types/Types.sol";
import "src/EVault/shared/Constants.sol";
import {ERC20, Context} from "openzeppelin-contracts/token/ERC20/ERC20.sol";
import "src/Synths/IRMSynth.sol";
import {console2} from "forge-std/Test.sol";

contract MockSynth is ERC20 {
    constructor() ERC20("MockSynth", "SYNTH"){}
    function mint(address to, uint256 amt) external {
        _mint(to, amt);
    }
}

contract MockAMMAndPricer {
    uint256 resA;
    uint256 resB;
    uint256 fee = 100; // 1% in BPS
    uint256 MAX_BPS = 10_000;

    function getQuote(uint256 inAmount, address base, address quote) external view returns (uint256 outAmount) {
        return inAmount * resA / resB;
    }

    function getRatio() public returns (uint256) {
        return resA/resB;
    }

    function setResA(uint256 _resA) external {
        resA = _resA;
    }

    function setResB(uint256 _resB) external {
        resB = _resB;
    }

    function getOutWithFee(uint256 inAmount) external view returns (uint256) {
        uint256 quotedAmt = inAmount * resA / resB;
        uint256 afterFee = quotedAmt * (MAX_BPS - fee) / MAX_BPS;
        return afterFee;
    }
}

contract POC_Test is EVaultTestBase {
    using TypesLib for uint256;

    function setUp() public override {
        // There are 2 vaults deployed with bare minimum configuration:
        // - eTST vault using assetTST as the underlying
        // - eTST2 vault using assetTST2 as the underlying
        // Both vaults use the same MockPriceOracle and unit of account.
        // Both vaults are configured to use IRMTestDefault interest rate model.
        // Both vaults are configured to use 0.2e4 max liquidation discount.
        // Neither price oracles for the assets nor the LTVs are set.
        super.setUp();
        // In order to further configure the vaults, refer to the Governance module functions.
    }

    function test_POC() external {
        MockAMMAndPricer pricer = new MockAMMAndPricer();
        MockSynth synth = new MockSynth();
        // Set price at .99999/1, leading to raise in rates
        pricer.setResA(1e18 - 1);
        pricer.setResB(1e18);
        uint256 quote = pricer.getQuote(1e18, address(synth), address(124));
        uint256 withFee = pricer.getOutWithFee(1e18);
        console2.log("quote", quote);
        console2.log("withFee", withFee);
        // Set IRM at 1e18
        IRMSynth irm = new IRMSynth(address(synth), address(124), address(pricer), 1e18);
        uint256 startRate = irm.computeInterestRate(address(124), uint256(1), uint256(1));
        for(uint256 i; i < 25; i++) {
            vm.warp(block.timestamp + irm.ADJUST_INTERVAL());
            irm.computeInterestRate(address(124), uint256(1), uint256(1));
        }
        uint256 endRate = irm.computeInterestRate(address(124), uint256(1), uint256(1));
        assertGt(endRate, startRate, "Rate increase");
        console2.log("startRate", startRate);
        console2.log("endRate", endRate);
    }
}
```

## Recommendation
Account for swap fees and oracle drift, and add a buffer at which the price will cause rates to remain static. Oracle Drift can be quantified in the worst case as the Deviation Threshold minus 1 wei. Technically, the real drift could be higher due to the delay for oracle updates.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | Alex The Entreprenerd, Akshay Srivastav |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

