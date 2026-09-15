---
# Core Classification
protocol: Open Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29349
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-opendollar
source_link: https://code4rena.com/reports/2023-10-opendollar
github_link: https://github.com/code-423n4/2023-10-opendollar-findings/issues/429

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
finders_count: 16
finders:
  - 0xlemon
  - MrPotatoMagic
  - ge6a
  - 0xAadi
  - yashar
---

## Vulnerability Title

[M-01] `ODSafeManager#allowSAFE()` cannot be executed either by the proxy contract or any other address.

### Overview


This bug report is about the inability to execute the `allowSAFE()` function in the `BasicActions` contract. This function is responsible for granting an address the capability to manage the Safe. Due to this, the proxy contract is unable to execute `allowSAFE()`, leading to the inaccessibility of several critical functions for authorized users. The functionality of essential operations such as `modifySAFECollateralization()`, `transferCollateral()`, `transferInternalCoins()`, `quitSystem()`, `enterSystem()`, `moveSAFE()`, `removeSAFE()`, and `protectSAFE()` is currently halted due to this bug.

The bug was tested using the Foundry tool by placing a test file in the `test/nft/anvil/` folder and running `forge t --fork-url http://127.0.0.1:8545 --match-path test/nft/anvil/NFTTestAnvil.t.sol -vvv`. The tests showed that both calls to the `allowSAFE()` were failing, meaning the proxy contract was unable to allow an address to manage the safe.

The recommended mitigation step is to implement the necessary functions in the `BasicActions` contract to execute the necessary functions in the `ODSafeManager` contract. The severity of the bug was decreased to Medium since it can be addressed operationally by deploying another implementation contract.

### Original Finding Content


"According to the GEB framework, the proxy contracts (`ODProxy`) are designed to interact with the Safe Manager (`ODSafeManager`) through the Proxy Action contract (`BasicActions`). The pivotal function, `allowSAFE()`, is responsible for granting an address the capability to manage the Safe. Unfortunately, the `BasicActions` contract lacks the implementation of the `allowSAFE()` function. Consequently, the proxy contract is unable to execute `allowSAFE()`, leading to the inaccessibility of several critical functions for authorized users.

The functionality of essential operations such as `modifySAFECollateralization()`, `transferCollateral()`, `transferInternalCoins()`, `quitSystem()`, `enterSystem()`, `moveSAFE()`, `removeSAFE()`, and `protectSAFE()` is currently halted due to the inability to allow users to manage the Safe.

In addition to the absent `allowSAFE()` implementation, the following functions are also not yet implemented in the `BasicActions` contract and these functions are not directly executable by proxy contract: `allowHandler()`, `modifySAFECollateralization()`, `transferCollateral()`, `transferInternalCoins()`, `quitSystem()`, `enterSystem()`, `moveSAFE()`, `removeSAFE()`, and `protectSAFE()`."

### Proof of Concept

Place the following test file in `test/nft/anvil/` and run `forge t --fork-url http://127.0.0.1:8545 --match-path test/nft/anvil/NFTTestAnvil.t.sol -vvv`

<details>

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.19;

import 'forge-std/console.sol';
import {AnvilFork} from '@test/nft/anvil/AnvilFork.t.sol';
import {Vault721} from '@contracts/proxies/Vault721.sol';
import {IODSafeManager} from '@interfaces/proxies/IODSafeManager.sol';
import {ODProxy} from '@contracts/proxies/ODProxy.sol';

contract NFTTestAnvil is AnvilFork {

  function test_setup() public {
    assertEq(totalVaults, vault721.totalSupply());
    checkProxyAddress();
    checkVaultIds();
  }

// Function to test open safe and allow safe with direct call
  function test_allowSafeDirectCall() public {
    address _proxy = proxies[0];
    bytes32 cType = cTypes[0];
    address user = users[0];

    vm.startPrank(user);  

    uint256 safeId = safeManager.openSAFE(cType,_proxy);
    IODSafeManager.SAFEData memory sData = safeManager.safeData(safeId);
    assertEq(_proxy,sData.owner);

    // allowSAFE call will fail
    vm.expectRevert(IODSafeManager.SafeNotAllowed.selector);
    safeManager.allowSAFE(safeId, user, 1);

    vm.stopPrank();
  }

  // Function to test open safe and allow safe with proxy delegation call
  function test_allowSafeWithProxyExecute() public {
    address _proxy = proxies[0];
    bytes32 cType = cTypes[0];
    address user = users[0];

    vm.startPrank(user);  

    uint256 safeId = openSafe2(cType,_proxy);
    IODSafeManager.SAFEData memory sData = safeManager.safeData(safeId);
    assertEq(_proxy,sData.owner);

    // allowSAFE call will fail
    vm.expectRevert();
    allowSafe(_proxy, safeId, user, 1);

    vm.stopPrank();
  }

  function openSafe2(bytes32 _cType, address _proxy) public returns (uint256 _safeId) {
    bytes memory payload = abi.encodeWithSelector(basicActions.openSAFE.selector, address(safeManager), _cType, _proxy);
    bytes memory safeData = ODProxy(_proxy).execute(address(basicActions), payload);
    _safeId = abi.decode(safeData, (uint256));
  }

  function allowSafe(address _proxy, uint256 _safe, address _usr, uint256 _ok) public  {
    bytes memory payload = abi.encodeWithSelector(safeManager.allowSAFE.selector,_safe, _usr, _ok);
    ODProxy(_proxy).execute(address(safeManager), payload);
  }  
}
```

</details>

Here you can see, both call to the `allowSAFE()` are failing, ie proxy contract cannot able to allow an address to manage the safe.

See the second test case, when we are calling the `allowSAFE()` with `delegatecall` the context of the target(`ODSafeManager`) has changed and the call get failed.

### Tools Used

Foundry

### Recommended Mitigation Steps

Implement necessary functions in the `BasicActions` contract to execute necessary functions in the `ODSafeManager` contract.

**[MiloTruck (Judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-10-opendollar-findings/issues/429#issuecomment-1800716203):**
 > Since `BasicActions.sol` does not have a function to call `allowSafe()`, users will not be able to interact with `ODSafeManager` through their proxies.
> 
> However, since this can be addressed operationally by deploying another implementation contract, there isn't any permanent DOS of the protocol's functionality. Therefore, medium severity is appropriate.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Open Dollar |
| Report Date | N/A |
| Finders | 0xlemon, MrPotatoMagic, ge6a, 0xAadi, yashar, T1MOH, nmirchev8, 0xprinc, Giorgio, m4k2, perseus, 0xDemon, Greed, xAriextz, Arz, btk |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-opendollar
- **GitHub**: https://github.com/code-423n4/2023-10-opendollar-findings/issues/429
- **Contest**: https://code4rena.com/reports/2023-10-opendollar

### Keywords for Search

`vulnerability`

