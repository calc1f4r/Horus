---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: revert_inside_hook

# Attack Vector Details
attack_type: revert_inside_hook
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5894
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/116

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - revert_inside_hook

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - Trust
  - ronnyx2017
  - rotcivegaf
  - Lambda
  - HE1M
---

## Vulnerability Title

[H-07] GiantLP with a transferHookProcessor cant be burned, users’ funds will be stuck in the Giant Pool

### Overview


This bug report is about a vulnerability found in the GiantLP, GiantMevAndFeesPool and SyndicateRewardsProcessor contracts. The vulnerability occurs when the GiantLP token is burned and the `to` address is address(0x00). The GiantMevAndFeesPool.beforeTokenTransfer will call the function `SyndicateRewardsProcessor._distributeETHRewardsToUserForToken` which has a zero address check in the first line. This will cause any withdraw function with a burning operation of the GiantLP token to revert, leaving the user's funds stuck in the Giant Pool contracts. 

To prove this vulnerability, the tester wrote a test about `GiantMevAndFeesPool.withdrawETH` function which was used to withdraw eth from the Giant Pool and it was reverted. The test was run with the Foundry tool and the test log was included in the report.

The recommended mitigation step is to skip the update rewards for the zero address.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/main/contracts/liquid-staking/GiantLP.sol#L39-L47
https://github.com/code-423n4/2022-11-stakehouse/blob/main/contracts/liquid-staking/GiantMevAndFeesPool.sol#L73-L78
https://github.com/code-423n4/2022-11-stakehouse/blob/main/contracts/liquid-staking/SyndicateRewardsProcessor.sol#L51-L57


## Vulnerability details

## Impact
The GiantLP with a transferHookProcessor will call `transferHookProcessor.beforeTokenTransfer(_from, _to, _amount)` when it's transferred / minted / burned. 

But the `to` address is address(0x00) in the erc20 `_burn` function. The GiantMevAndFeesPool.beforeTokenTransfer will call the function `SyndicateRewardsProcessor._distributeETHRewardsToUserForToken` will a zero address check in the first line:
```
function _distributeETHRewardsToUserForToken(...) internal {
    require(_recipient != address(0), "Zero address");
```

So any withdraw function with a operation of burning the GiantLP token with a transferHookProcessor will revert because of the zero address check. The users' funds will be stuck in the Giant Pool contracts.

## Proof of Concept
I wrote a test about `GiantMevAndFeesPool.withdrawETH` function which is used to withdraw eth from the Giant Pool. It will be reverted.

test/foundry/LpBurn.t.sol
```
pragma solidity ^0.8.13;

// SPDX-License-Identifier: MIT
import {GiantPoolTests} from "./GiantPools.t.sol";

contract LpBurnTests is GiantPoolTests {
    function testburn() public{
        address feesAndMevUserOne = accountOne; vm.deal(feesAndMevUserOne, 4 ether);
        vm.startPrank(feesAndMevUserOne);
        giantFeesAndMevPool.depositETH{value: 4 ether}(4 ether);
        giantFeesAndMevPool.withdrawETH(4 ether);
        vm.stopPrank();
    }
}
```

run test
```
forge test --match-test testburn -vvv
```

test log:
```
...
...
    ├─ [115584] GiantMevAndFeesPool::withdrawETH(4000000000000000000) 
    │   ├─ [585] GiantLP::balanceOf(0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266) [staticcall]
    │   │   └─ ← 4000000000000000000
    │   ├─ [128081] GiantLP::burn(0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266, 4000000000000000000) 
    │   │   ├─ [126775] GiantMevAndFeesPool::beforeTokenTransfer(0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266, 0x0000000000000000000000000000000000000000, 4000000000000000000) 
    │   │   │   ├─ [371] GiantLP::totalSupply() [staticcall]
    │   │   │   │   └─ ← 4000000000000000000
    │   │   │   ├─ emit ETHReceived(amount: 4000000000000000000)
    │   │   │   ├─ [585] GiantLP::balanceOf(0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266) [staticcall]
    │   │   │   │   └─ ← 4000000000000000000
    │   │   │   ├─ [0] 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266::fallback{value: 4000000000000000000}() 
    │   │   │   │   └─ ← ()
    │   │   │   ├─ emit ETHDistributed(user: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266, recipient: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266, amount: 4000000000000000000)
    │   │   │   ├─ [2585] GiantLP::balanceOf(0x0000000000000000000000000000000000000000) [staticcall]
    │   │   │   │   └─ ← 0
    │   │   │   └─ ← "Zero address"
    │   │   └─ ← "Zero address"
    │   └─ ← "Zero address"
    └─ ← "Zero address"
```

## Tools Used
foundry

## Recommended Mitigation Steps
skip update rewards for zero address.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | Trust, ronnyx2017, rotcivegaf, Lambda, HE1M, 9svR6w |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/116
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Revert Inside Hook`

