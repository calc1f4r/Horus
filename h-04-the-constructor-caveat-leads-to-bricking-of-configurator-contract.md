---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: uncategorized
vulnerability_type: upgradable

# Attack Vector Details
attack_type: upgradable
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21141
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-lybra
source_link: https://code4rena.com/reports/2023-06-lybra
github_link: https://github.com/code-423n4/2023-06-lybra-findings/issues/673

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 2

# Context Tags
tags:
  - upgradable
  - initializer
  - initialization

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cthulhu\_cult
---

## Vulnerability Title

[H-04] The Constructor Caveat leads to bricking of Configurator contract.

### Overview


This bug report covers a bug found in Solidity code that is part of the LybraFinance system. The code is inside a constructor or part of a global variable declaration, and is not part of a deployed contract's runtime bytecode. This means that any state changes made in the constructor of a logic contract will not be reflected in the proxy's state. As a result, all the functions that rely on governance will be broken since the governance address is set to zero address.

To mitigate this issue, the code within the constructor should be moved to a regular "initializer" function, which should be called whenever the proxy links to this logic contract. Special care needs to be taken with this initializing function so that it can only be called once and use another initialization mechanism, since the governance address should be set in the initialize. Manual code review and Foundry for POC were used to identify and confirm the bug. The assessed type for this bug is Upgradable.

### Original Finding Content


In Solidity, code that is inside a constructor or part of a global variable declaration is not part of a deployed contract's runtime bytecode. This code is executed only once, when the contract instance is deployed. As a consequence of this, the code within a logic contract's constructor will never be executed in the context of the proxy's state. This means that any state changes made in the constructor of a logic contract will not be reflected in the proxy's state.
1.  This will lead to governance timelocks contract and the `curvePool` contract contain default values of zero values.
2.  As a result, all the functions that rely on governance will be broken, since the governance address is set to zero address.

### Proof of Concept

```
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import {ITransparentUpgradeableProxy} from "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";

import {LybraProxy} from "@lybra/Proxy/LybraProxy.sol";
import {LybraProxyAdmin} from "@lybra/Proxy/LybraProxyAdmin.sol";
import {GovernanceTimelock} from "@lybra/governance/GovernanceTimelock.sol";
import {PeUSDMainnet} from "@lybra/token/PeUSDMainnetStableVision.sol";
import {Configurator} from "@lybra/configuration/LybraConfigurator.sol";
import {EUSDMock} from "@mocks/mockEUSD.sol";
import {mockCurve} from "@mocks/mockCurve.sol";
import {mockUSDC} from "@mocks/mockUSDC.sol";

/* remappings used
@lybra=contracts/lybra/
@mocks=contracts/mocks/
 */
contract CounterScript is Test {
    address goerliEndPoint = 0xbfD2135BFfbb0B5378b56643c2Df8a87552Bfa23;

    LybraProxy proxy;
    LybraProxyAdmin admin;
    GovernanceTimelock govTimeLock;
    mockUSDC usdc;
    mockCurve curve;
    Configurator configurator;
    Configurator configuratorLogic;
     EUSDMock eusd;
    PeUSDMainnet peUsdMainnet;
    address owner = address(7);
    address[] govTimelockArr;

     function setUp() public {
         vm.startPrank(owner);
         govTimelockArr.push(owner);
         govTimeLock = new GovernanceTimelock(
             1,
             govTimelockArr,
             govTimelockArr,
             owner
         );

         usdc = new mockUSDC();
         curve = new mockCurve();
         eusd = new EUSDMock(address(configurator));
         //  _dao , _curvePool
         configuratorLogic = new Configurator(address(govTimeLock), address(curve));

         admin = new LybraProxyAdmin();
         proxy = new LybraProxy(address(configuratorLogic),address(admin),bytes(""));
         configurator = Configurator(address(proxy));

        peUsdMainnet = new PeUSDMainnet(
             address(configurator),
             8,
             goerliEndPoint
         );
         vm.stopPrank();
    }

    function test_LybraConfigurationContractDoesNotInitialize() public {
        vm.startPrank(address(owner));
        vm.expectRevert(); // Since the Governance time lock is set to zero. 
        configurator.initToken(address(eusd), address(peUsdMainnet));
    }
}
```

### Tools Used

1.  Manual Code review
2.  Foundry for POC

### Recommended Mitigation Steps

[LybraConfiguration.sol#L81](https://github.com/code-423n4/2023-06-lybra/blob/5d70170f2c68dbd3f7b8c0c8fd6b0b2218784ea6/contracts/lybra/configuration/LybraConfigurator.sol#L81) contracts should move the code within the constructor to a regular "initializer" function, and have this function be called whenever the proxy links to this logic contract. Special care needs to be taken with this initializing function so that it can only be called once and use another initialization mechanism, since the governance address should be set in the initialize.

### Assessed type

Upgradable

**[LybraFinance confirmed](https://github.com/code-423n4/2023-06-lybra-findings/issues/673#issuecomment-1635556436)**

**[0xean (judge) commented](https://github.com/code-423n4/2023-06-lybra-findings/issues/673#issuecomment-1655885310):**
 > On the fence re: severity here and could see the argument for this being M.  Will leave as submitted for now, but open to comment during QA on the topic. 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | cthulhu\_cult |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-lybra
- **GitHub**: https://github.com/code-423n4/2023-06-lybra-findings/issues/673
- **Contest**: https://code4rena.com/reports/2023-06-lybra

### Keywords for Search

`Upgradable, Initializer, Initialization`

