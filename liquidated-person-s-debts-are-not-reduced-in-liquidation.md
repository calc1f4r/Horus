---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40212
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
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
finders_count: 2
finders:
  - cccz
  - Patrick Drotleff
---

## Vulnerability Title

Liquidated person 's debts are not reduced in liquidation 

### Overview


The bug report is about a problem in the code for a smart contract called Vault.sol. The issue occurs when someone's collateral is liquidated, which means it is used to repay their debts. However, the code does not update the liquidated person's position, which means they can be liquidated multiple times until their collateral reaches zero. This was demonstrated in a proof of concept where the collateral was reduced to zero but the debt remained unchanged. The recommendation is to change the code to fix this issue. The bug has been fixed in two different versions of the code. The risk level of this bug is considered to be medium.

### Original Finding Content

## Vulnerability Report

## Context
**File:** Vault.sol  
**Lines:** 245-246

## Description
After liquidation, the liquidator's TCAPV2 is burned to repay the liquidated person's debts. However, during liquidation, the `modifyPosition()` function is not called to update the position of the liquidated person to reduce the debt. This oversight allows the liquidated person to be liquidated repeatedly until their collateral reaches zero:

```solidity
pocket.withdraw(user, liquidationReward, msg.sender);
TCAPV2.burn(msg.sender, burnAmount);
emit Liquidated(msg.sender, user, pocketId, liquidationReward, burnAmount);
```

## Proof of Concept
The proof of concept demonstrates that after liquidation, the collateral is zero while the debt remains unchanged:

```solidity
function test_POC() public {
    address user = address(0xb0b);
    uint amount = 1e18;
    vm.assume(user != address(0) && user != address(vaultProxyAdmin));
    uint256 depositAmount = deposit(user, amount);
    vm.assume(depositAmount > 0);
    vm.prank(user);
    uint256 mintAmount = bound(amount, 1, depositAmount);
    vault.mint(pocketId, mintAmount);
    uint256 collateralValue = vault.collateralValueOfUser(user, pocketId);
    console.logUint(collateralValue); // 1000e18
    uint256 mintValue = vault.mintedValueOf(mintAmount);
    console.logUint(mintValue); // 1000e18
    uint256 multiplier = mintValue * 10_000 / (collateralValue);
    vm.assume(multiplier > 1);
    feed.setMultiplier(multiplier - 1);
    tCAPV2.mint(address(this), mintAmount);
    vm.expectEmit(true, true, true, true);
    emit IVault.Liquidated(address(this), user, pocketId, depositAmount, mintAmount);
    console.logUint(vault.mintedValueOfUser(user, pocketId)); // 1000e18
    collateralValue = vault.collateralValueOfUser(user, pocketId);
    console.logUint(collateralValue); // 99.9e18
    vault.liquidate(user, pocketId, mintAmount);
    collateralValue = vault.collateralValueOfUser(user, pocketId);
    console.logUint(collateralValue); // 0
    console.logUint(vault.mintedValueOfUser(user, pocketId)); // 1000e18
}
```

## Recommendation
Change to:

```solidity
+ $.modifyPosition(_toMintId(user, pocketId), -burnAmount.toInt256());
pocket.withdraw(user, liquidationReward, msg.sender);
TCAPV2.burn(msg.sender, burnAmount);
emit Liquidated(msg.sender, user, pocketId, liquidationReward, burnAmount);
```

## Cryptex
Fixed in commits **50c7925a** and **441a8137**.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | cccz, Patrick Drotleff |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a

### Keywords for Search

`vulnerability`

