---
# Core Classification
protocol: 0xhoneyjar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52968
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/1fce4414-74e9-490b-ac89-cf65755563d2
source_link: https://cdn.cantina.xyz/reports/cantina_honeyjar_february2025.pdf
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
  - chris
  - Cryptara
---

## Vulnerability Title

Whitelisted Vaults Not Receiving Accumulated Rewards 

### Overview


This bug report discusses an issue with a function called setWhitelistedVault in a smart contract called fatBERA.sol. The problem occurs when a vault is not initially whitelisted and then later becomes whitelisted. During the time when the vault was not whitelisted, it should have been accruing rewards, but those rewards are lost when it becomes whitelisted. This is because rewards are only tracked for effective balances, and when a vault is not whitelisted, its effective balance is 0. The provided proof of concept demonstrates this issue and suggests a solution to update rewards before changing the whitelisted status of a vault. This bug has already been fixed in the code.

### Original Finding Content

## Context: fatBERA.sol#L262-L264

## Description
When a vault is initially not whitelisted and later becomes whitelisted using `setWhitelistedVault`, any rewards that should have accrued to the vault during the period before whitelisting are lost. The vault does not receive any retroactive rewards for the time it was accumulating shares, but before it was officially marked as whitelisted.

This occurs because rewards are only tracked for effective balances, and whitelisted vaults have an effective balance of 0, meaning no rewards are recorded for them. However, when a vault is not whitelisted, its shares are considered for rewards, but the rewards are not properly accounted for when transitioning the vault to a whitelisted state.

The provided proof of concept demonstrates that after transferring shares to an unwhitelisted vault and then calling `notifyRewardAmount`, the vault does not accrue rewards. Even after advancing time and whitelisting the vault, it still does not receive rewards for the period before whitelisting.

## Proof of Concept
```solidity
function test_WhitelistingVaultAfterAccumulatingRewards() public {
    address vaultAddress = makeAddr("vault");
    // Alice deposits 100 WBERA
    uint256 depositAmount = 100e18;
    vm.prank(alice);
    vault.deposit(depositAmount, alice);
    // Alice transfers shares to an unwhitelisted vault
    uint256 transferAmount = 50e18;
    vm.prank(alice);
    vault.transfer(vaultAddress, transferAmount);
    // Notify rewards so that the vault accrues some rewards
    uint256 rewardAmount = 20e18;
    vm.prank(admin);
    vault.notifyRewardAmount(address(wbera), rewardAmount);
    // Capture the rewards after the notification and warp
    uint256 rewardsBeforeWhitelistingAndWarp = vault.previewRewards(vaultAddress, address(wbera));
    console2.log("rewardsBeforeWhitelistingAndWarp", rewardsBeforeWhitelistingAndWarp);
    assertEq(rewardsBeforeWhitelistingAndWarp, 0, "Vault should not accrue rewards before whitelisting");
    // Warp time forward to let rewards accumulate
    uint256 warpTime = 3 days;
    vm.warp(block.timestamp + warpTime);
    // Capture rewards before whitelisting
    uint256 rewardsBeforeWhitelisting = vault.previewRewards(vaultAddress, address(wbera));
    console2.log("rewardsBeforeWhitelisting", rewardsBeforeWhitelisting);
    // Whitelist the vault
    vm.prank(admin);
    vault.setWhitelistedVault(vaultAddress, true);
    // Warp more time to check if vault earns new rewards
    vm.warp(block.timestamp + warpTime);
    // Capture rewards after whitelisting
    uint256 rewardsAfterWhitelisting = vault.previewRewards(vaultAddress, address(wbera));
    console2.log("rewardsAfterWhitelisting", rewardsAfterWhitelisting);
    // Verify that the amount of rewards is at least for the period between the notify and whitelisting
    assertEq(rewardsAfterWhitelisting, rewardsBeforeWhitelisting, "Vault should not accrue new rewards after being whitelisted");
}
```

## Recommendation
To ensure vaults do not lose accrued rewards when transitioning from a non-whitelisted state to a whitelisted one, `setWhitelistedVault` should first update rewards for the vault before modifying its whitelisted status. This ensures that any pending rewards are correctly accounted for before setting the vault’s effective balance to zero. 

Implementing an `_updateRewards(vaultAddress)` call before changing the `isWhitelistedVault` status ensures the vault receives rewards accrued before being whitelisted.

```solidity
function setWhitelistedVault(address vaultAddress, bool status) external onlyRole(DEFAULT_ADMIN_ROLE) {
    if (!isWhitelistedVault[vaultAddress]){
        _updateRewards(vaultAddress);
    }
    isWhitelistedVault[vaultAddress] = status;
}
```

## HoneyJar
Fixed in commit `6a577737`.

## Cantina Managed
Fixed as recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | 0xhoneyjar |
| Report Date | N/A |
| Finders | chris, Cryptara |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_honeyjar_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/1fce4414-74e9-490b-ac89-cf65755563d2

### Keywords for Search

`vulnerability`

