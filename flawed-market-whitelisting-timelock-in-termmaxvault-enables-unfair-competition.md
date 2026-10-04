---
# Core Classification
protocol: Term Structure
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54906
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6f373ea8-adf6-45d2-8d72-a76fe5b7f21e
source_link: https://cdn.cantina.xyz/reports/cantina_competition_term_structure_february2025.pdf
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
finders_count: 2
finders:
  - BengalCatBalu
  - silverologist
---

## Vulnerability Title

Flawed Market Whitelisting Timelock in TermMaxVault Enables Unfair Competition 

### Overview


This report is about a bug found in the timelock mechanism of TermMaxVault, which is used for market whitelisting. The bug causes the timelock to not function properly, allowing curators to gain an unfair advantage by creating orders immediately after submitting markets for whitelisting. This can lead to unexpected competition for other market participants and a loss of potential profit. The bug has been fixed in two proposed solutions, and the fixes have been verified. 

### Original Finding Content

## Report on Timelock Mechanism in TermMaxVault

## Context
No context files were provided by the reviewer.

## Summary
The timelock mechanism designed to delay market whitelisting in TermMaxVault is not functioning.

## Finding Description
In the `TermMaxVault::submitMarket` function, when a new market is submitted for whitelisting, the `_pendingMarkets[market]` object is assigned a `validAt` value of 0. This causes the market to become eligible for whitelisting immediately, bypassing the expected delay.

As a consequence, curators can create orders earlier than anticipated, leading to unexpected competition for other market participants.

**Consider this scenario:**
- Alice, a lending market maker, creates an order at an interest rate of X%.
- The curator submits the market to the vault for whitelisting.
- Due to the flawed timelock, the market is instantly whitelisted. The curator then creates an order at a lower interest rate of Y% (< X%).
- Bob, a borrowing market taker, selects the curator's order because it offers a better rate.

While Bob benefits from a lower interest rate, Alice faces unfair and unexpected competition, losing the potential profit she would have earned if her order had been filled by Bob.

## Impact Explanation
The flawed timelock allows curators to gain a competitive advantage by creating orders immediately after submitting markets for whitelisting, resulting in unfair and unexpected competition for other market makers. This can lead to a loss of profit for them.

## Likelihood Explanation
Markets that are submitted for whitelisting never have to undergo the timelock delay.

## Proof of Concept
Execute the following test:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

import {Test} from "forge-std/Test.sol";
import {DeployUtils} from "./utils/DeployUtils.sol";
import {JSONLoader} from "./utils/JSONLoader.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ITermMaxVault} from "contracts/vault/TermMaxVault.sol";
import {PendingUint192} from "contracts/lib/PendingLib.sol";
import {MarketConfig, VaultInitialParams} from "contracts/storage/TermMaxStorage.sol";

contract TestTimelock is Test {
    address deployer = vm.randomAddress();
    address curator = vm.randomAddress();
    string testdata;
    ITermMaxVault vault;

    function setUp() public {
        vm.startPrank(deployer);
        testdata = vm.readFile(string.concat(vm.projectRoot(), "/test/testdata/testdata.json"));
        MarketConfig memory marketConfig = JSONLoader.getMarketConfigFromJson(vm.randomAddress(), testdata, ".marketConfig");
        marketConfig.maturity = uint64(block.timestamp + 90 days);
        VaultInitialParams memory initialParams = VaultInitialParams(
            deployer, curator, 86400, IERC20(vm.randomAddress()), 1000000e18, "Vault-DAI", "Vault-DAI", 0.5e8
        );
        vault = DeployUtils.deployVault(initialParams);
        vm.stopPrank();
    }

    function testMarketWhitelistNoTimelock() public {
        // check current timelock value
        assertEq(vault.timelock(), 86400);
        // submit market
        vm.prank(curator);
        address market = address(0x123);
        vault.submitMarket(market, true);
        // The validAt of the newly submitted market is the current time, without timelock
        PendingUint192 memory pendingMarket = vault.pendingMarkets(market);
        assertEq(pendingMarket.validAt, block.timestamp);
    }
}
```

## Recommendation
In `TermMaxVault`, when submitting a market for whitelisting, set the timelock properly:
- `_pendingMarkets[market].update(uint184(block.timestamp + _timelock), 0);`
+ `_pendingMarkets[market].update(0, _timelock);`

## Term Structure
Addressed in PR 4 and PR 5.

## Cantina Managed
Fixes verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Term Structure |
| Report Date | N/A |
| Finders | BengalCatBalu, silverologist |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_term_structure_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6f373ea8-adf6-45d2-8d72-a76fe5b7f21e

### Keywords for Search

`vulnerability`

