---
# Core Classification
protocol: Alchemix Transmuter
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49844
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm4mmjdju0000oni7kpb72tkx
source_link: none
github_link: https://github.com/Cyfrin/2024-12-alchemix

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

# Audit Details
report_date: unknown
finders_count: 90
finders:
  - rolando
  - holydevoti0n
  - 0xwsecteam
  - moo888
  - 0xmsf14
---

## Vulnerability Title

Old router retains token allowance after update

### Overview

See description below for full details.

### Original Finding Content

## Summary

The `setRouter` function, which is in both `StrategyArb` and `StrategyOp` contracts, fails to revoke the allowance of the old router when a new router is set. This leads to unintended permission where the previous router retains the ability to unauthorizedly spend the protocol's funds.

## Vulnerability Details

In the `setRouter` function, which is present in both `StrategyArb` and `StrategyOp` contracts, the code sets an allowance of type(uint256).max for the new router for the underlying token, but does not revoke the allowance of the old router. This means the old router, which also retains an allowance of `type(uint256).max`, continues to have spending permissions even after it is no longer being used, which is not in the protocol's intentions since the router is changed. The old router, which could also be compromised or malicious but doesn’t have to be, could still unauthorizedly spend the contract’s funds.

```solidity
function setRouter(address _router) external onlyManagement {
    router = _router;
    underlying.safeApprove(router, type(uint256).max);
}
```

* *NOTE*: A similar finding was reported by Cyfrin in their Beefy Finance audit , the link: <https://solodit.cyfrin.io/issues/strategypassivemanageruniswap-gives-erc20-token-allowances-to-unirouter-but-doesnt-remove-allowances-when-unirouter-is-updated-cyfrin-none-cyfrin-beefy-finance-markdown>

StrategyArb code: <https://github.com/Cyfrin/2024-12-alchemix/blob/82798f4891e41959eef866bd1d4cb44fc1e26439/src/StrategyArb.sol#L42>
StrategyOp code: <https://github.com/Cyfrin/2024-12-alchemix/blob/82798f4891e41959eef866bd1d4cb44fc1e26439/src/StrategyOp.sol#L48>

## PoC

To demonstrate the existence of this vulnerability, we use two mock contracts: `MockToken` and `MockTransmuter`. These contracts simulate the actual system components for testing purposes. The `MockToken` contract is a very basic `ERC20` implementation, used to represent both the synthetic asset and the underlying token. The `MockTransmuter` contract, on the other hand, is initialized with two token addresses, representing the `synthetic asset` and the `underlying token`, and serves as a mock transmuter in this setup.
`MockTrasmuter`:

```solidity
pragma solidity^ 0.8.18;
import {ERC20} from "../../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
contract Trasmuter{
    address public syntheticToken;
    address public underlyingToken;

    constructor(address asset, address underlying){
        syntheticToken= asset;
        underlyingToken = underlying;
    }
}
```

`MockToken`:

```solidity
pragma solidity ^0.8.18;

import {ERC20} from "../../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";

contract Token is ERC20 {
    
    constructor() ERC20("Asset/Underlying", "Asset/Underlying") {
       
    }
}
```

In the `setup`, the `StrategyOp` contract is deployed with the `synthetic asset` and `mock transmuter` as parameters. The deploying user is granted the `Management` role, allowing them to invoke the `setRouter` function and set a new router. Initially, the router is set to `0xa062aE8A9c5e11aaA026fc2670B0D65cCc8B2858`, with this address getting an  allowance of type(uint256).max for the `underlying token`.

The `test_vulnTest` function demonstrates the vulnerability. It stores the initial router address (oldRouter), updates the router to a new address (newRouter) using setRouter, and verifies the update. It then checks allowances, confirming that the old router retains its  allowance, even after being replaced. This unintended behavior allows the old router to retain spending permissions.

```Solidity
pragma solidity ^0.8.18;

import "forge-std/Test.sol";
import {StrategyOp} from "../StrategyOp.sol";
import {Trasmuter} from "./MockTransmuter.sol";
import {Token} from "./MockToken.sol";
import {Under} from "./MockUnderlying.sol";


contract VulnTest is Test {
    
    StrategyOp op;
    address user;
    Token asset ;
    Token under;
    //address of the new router
    address newRouter = address(3);
    Trasmuter transmuter;


    function setUp() public {
        asset = new Token();
        under = new Token();
        user= makeAddr("user");
        transmuter = new Trasmuter(address(asset), address(under));
        //Since the user is the one who is deploying the StrategyOp contract 
        //he will be granted a Managment role and he will be able to set new router
        vm.startPrank(user);
        op = new StrategyOp(
            address(asset),
            address(transmuter),
            "StrategyOp"
        );
    }

    function test_vulnTest() public {
        //
        address oldRouter = op.router();

        vm.startPrank(user);
        //changing router
        op.setRouter(newRouter);

        //checking if the router is changed
        assert(op.router()== newRouter);

        //checking that the old router retains underlying token allowance
        assert(type(uint256).max == op.underlying().allowance(address(op), oldRouter));

        assert(type(uint256).max == op.underlying().allowance(address(op), newRouter));
    }
    }
```

After running the test with `forge test`,  we receive the following output, confirming that the vulnerability exists.

```bash
Ran 1 test for src/test/VulnTest.t.sol:VulnTest
[PASS] test_vulnTest() (gas: 61976)
Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 23.20ms (2.25ms CPU time)

Ran 1 test suite in 101.64ms (23.20ms CPU time): 1 tests passed, 0 failed, 0 skipped (1 total tests)
```

## Impact

The previous router retains token approval even after being replaced, allowing it to unauthorizedly spend (or even steal, if it becomes malicious) the contract's funds, which is not in the protocol’s intentions since it has been updated.&#x20;

## Tools Used

* Manual code review
* Foundry

## Recommendations

Consider updating the `setRouter` function to revoke the allowance of the old router before setting the new router and granting it a new allowance. By revoking the allowance of the old router before approving the new one, the protocol ensures that no unused or unintended allowances remain active.

```diff
function setRouter(address _router) external onlyManagement {
    // Revoke allowance for the old router
   + underlying.safeApprove(router, 0);

    // Set new router and approve maximum allowance
    router = _router;
    underlying.safeApprove(router, type(uint256).max);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Alchemix Transmuter |
| Report Date | N/A |
| Finders | rolando, holydevoti0n, 0xwsecteam, moo888, 0xmsf14, otor, i_atiq, n3smaro, dobrevaleri, crunter, vladzaev, cipherhawk, 0xpinky, focusoor, mizila_firox, pro_king, ericselvig, yovchevyoan, davidjohn24, fourb, zanderbytexyz, strapontin, jainadhaar2002, auditism, freesultan, lordofterra, hi_there, sauronsol, gaurav11018, prof, oxtenma, nikolaihristov1999, kalogerone, pontifex, ognjenovicuros, allamloqman, 0xcnx, alix402, ro1sharkm, amarfares, future2xy, 1337web3, sancybars, y0ng0p3, abhan, ethworker, fondevs, godswillchiagorom20, zealousdream572, fresh, theirrationalone, ace_30, gioruggieri, setstacklist, biakia, karanel, dustinhuel2, regis, _frolic, kassyolisakwe, 0xmaxi, taiger4526, james07, yongu, 745fe9f9c2, 0xspryon, zhuying, 0xaman, 0x6a70, mladenov, y4y, jesjupyter, inh3l, galturok, 10ap17, joshuajee, waydou, 0xbrett8571, anonymousjoe, bladesec, goran |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-12-alchemix
- **Contest**: https://codehawks.cyfrin.io/c/cm4mmjdju0000oni7kpb72tkx

### Keywords for Search

`vulnerability`

