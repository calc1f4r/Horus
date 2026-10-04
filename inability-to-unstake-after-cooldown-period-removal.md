---
# Core Classification
protocol: Level
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40397
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/131241f5-7399-476e-acd1-dc57c8f00e39
source_link: https://cdn.cantina.xyz/reports/cantina_level_jun2024.pdf
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
finders_count: 4
finders:
  - Delvir0
  - tchkvsky
  - MiloTruck
  - phaze
---

## Vulnerability Title

Inability to unstake after cooldown period removal 

### Overview


This bug report discusses an issue with the StakedlvlUSD smart contract, specifically with the cooldown process for users who want to unstake their shares. Currently, if a user initiates the cooldown process and then the cooldown duration is reduced or removed, the user will not be able to unstake immediately. This can be problematic in emergency situations where the protocol needs to allow immediate unstaking. The report recommends storing the cooldown start time instead of the end time to address this issue. The code snippet provided shows the necessary modifications to the contract. 

### Original Finding Content

## Cooldown Process and Unstaking Issue

## Context
- `StakedlvlUSD.sol#L484-L529`
- `StakedlvlUSD.sol#L442-L482`
- `StakedlvlUSD.sol#L531-L543`

## Description
Users that have initiated the cooldown process will be unable to unstake when the cooldown period is reduced or removed.

When a user initiates the cooldown process for their shares by calling `cooldownAssets` or `cooldownShares`, the cooldown end time is stored for the user. However, if the cooldown duration is reduced or removed (through `setCooldownDuration`) after a user has initiated the cooldown process, the user will not be able to unstake immediately as their cooldown end time will not be adjusted accordingly. This is because the protocol stores the end time during cooldown initiation and does not use a relative time calculation.

This issue can become problematic in emergency situations where the protocol might need to allow immediate unstaking by setting the cooldown duration to zero. In such scenarios, users who had previously initiated a cooldown would be unable to access their funds, while users who hadn’t would be able to unstake immediately.

The following proof of concept demonstrates the scenario:

```solidity
function testCoolDownPeriodReduction() public {
    // Set cooldown duration to be 7 days
    vm.prank(owner);
    stakedlvlUSD.setCooldownDuration(7 days);
    
    // Alice and Bob both deposit 100 ether assets
    uint256 amount = 100 ether;
    _mintApproveDeposit(alice, amount);
    _mintApproveDeposit(bob, amount);
    uint256 shares = stakedlvlUSD.balanceOf(alice);
    
    // Alice initiates share cooldown process in anticipation of unstaking
    vm.startPrank(alice);
    stakedlvlUSD.cooldownShares(shares, alice);
    vm.stopPrank();
    
    // An issue related to the protocol's solvency
    // forces immediate action to allow all users to
    // unstake by removing the cooldown duration
    vm.prank(owner);
    stakedlvlUSD.setCooldownDuration(0);
    
    // Alice's attempt to unstake or redeem shares is blocked
    vm.startPrank(alice);
    vm.expectRevert(IStakedlvlUSDCooldown.InvalidCooldown.selector);
    stakedlvlUSD.unstake(alice);
    
    // Alice's shares are in the silo
    vm.expectRevert("ERC4626: redeem more than max");
    stakedlvlUSD.redeem(shares, alice, alice);
    vm.stopPrank();
    
    // Bob is able to redeem his shares
    shares = stakedlvlUSD.balanceOf(bob);
    vm.prank(bob);
    stakedlvlUSD.redeem(shares, bob, bob);
}
```

## Recommendation
Instead of storing the cooldown end time, consider storing the cooldown start time instead.

```solidity
struct UserCooldown {
    // - uint104 cooldownEnd;
    + uint104 cooldownStart;
    uint256 underlyingShares;
}
```

This requires modifying the `cooldownAssets` and the `cooldownShares` functions to note the cooldown start time.

```solidity
// - cooldowns[owner].cooldownEnd =
// -     uint104(block.timestamp) +
// -     cooldownDuration;
// + cooldowns[owner].cooldownStart = uint104(block.timestamp);
```

When a user calls `unstake`, the cooldown end time will be computed given the user’s cooldown start time and the current cooldown duration.

```solidity
function unstake(address receiver) external {
    UserCooldown storage userCooldown = cooldowns[msg.sender];
    uint256 shares = userCooldown.underlyingShares;
    // + uint256 cooldownEnd = userCooldown.cooldownStart + cooldownDuration;
    // + if (block.timestamp >= cooldownEnd) {
    // +     userCooldown.cooldownStart = 0;
    // - if (block.timestamp >= userCooldown.cooldownEnd) {
    // -     userCooldown.cooldownEnd = 0;
    userCooldown.underlyingShares = 0;
    // ...
    } else {
        revert InvalidCooldown();
    }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Level |
| Report Date | N/A |
| Finders | Delvir0, tchkvsky, MiloTruck, phaze |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_level_jun2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/131241f5-7399-476e-acd1-dc57c8f00e39

### Keywords for Search

`vulnerability`

