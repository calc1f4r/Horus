---
# Core Classification
protocol: Dahlia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46373
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443
source_link: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
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
finders_count: 3
finders:
  - Saw-mon and Natalie
  - kankodu
  - Yorke Rhodes
---

## Vulnerability Title

WrappedVault share transfers results in stuck funds 

### Overview


The report highlights a bug in the WrappedVault contract where transferring WrappedVault shares to another address does not properly update the corresponding Dahlia shares. This leads to issues where the recipient cannot withdraw funds and the original sender cannot withdraw funds despite holding the Dahlia shares. The report recommends updating the transfer logic to ensure proper transfer of Dahlia shares. Additionally, it suggests adding Transfer events in various scenarios for full ERC20 compliance. The bug has been fixed in a recent commit and the missing Transfer events have been addressed in a pull request.

### Original Finding Content

## WrappedVault Issues and Recommendations

## Context
- **Files Involved:** WrappedVault.sol#L455, WrappedVault.sol#L462

## Description
Only the `wrappedVault` is allowed to lend and withdraw assets to/from the Dahlia lending contract. Users can interact with `wrappedVault` through its deposit and withdraw functions. When a user deposits assets into `wrappedVault`, they are minted shares of `wrappedVault` as expected. 

Internally, `wrappedVault` calls `dahlia.lend` and assigns the Dahlia shares to the receiver (the depositor) instead of keeping them for itself. This ensures that individual accounting for `claimInterest` works correctly for each depositor.

However, an issue arises when a user transfers their `wrappedVault` shares to another address:
- The sender's `wrappedVault` balance is reduced, and the recipient's balance increases. The corresponding Dahlia shares, however, remain assigned to the original sender and do not update to reflect the transfer.

### Critical Issues
- The recipient cannot withdraw funds because they lack sufficient Dahlia shares.
- The original sender cannot withdraw funds because their `wrappedVault` balance is insufficient, despite still holding the Dahlia shares.

## Proof of Concept
Add the following test in `test/core/integration/WrappedVault.t.sol`:

```solidity
function testTransferDoesNotWork() public {
    address fromAddress = REGULAR_USER;
    address toAddress = REFERRAL_USER;
    uint256 depositAmount = 1 ether;
    MockERC20(address(token)).mint(fromAddress, depositAmount);
    
    vm.startPrank(fromAddress);
    token.approve(address(testIncentivizedVault), depositAmount);
    uint256 shares = testIncentivizedVault.deposit(depositAmount, fromAddress);
    testIncentivizedVault.transfer(toAddress, shares);
    vm.stopPrank();
    
    // neither the fromAddress, nor the toAddress can get funds back
    // this fails because in dahlia accounting toAddress doesn't have the shares
    vm.startPrank(toAddress);
    vm.expectRevert();
    testIncentivizedVault.withdraw(depositAmount, toAddress, toAddress);
    vm.stopPrank();
    
    // this fails because wrapperVault balance has been transferred to toAddress
    vm.startPrank(fromAddress);
    vm.expectRevert();
    testIncentivizedVault.withdraw(depositAmount, fromAddress, fromAddress);
    vm.stopPrank();
}
```

## Recommendation
Update the transfer logic to ensure proper transfer of Dahlia shares when `wrappedVault` shares are transferred.

**Dahlia:** Fixed in commit `dcc59d44`.

## Cantina Managed Issues
### Missing Transfer Events
A token contract that creates new tokens **SHOULD** trigger a Transfer event with the `_from` address set to `0x0` when tokens are created.
1. When `WrappedVault` shares are minted in the `WrappedVault._deposit` function, no Transfer event is emitted with `from = address(0)` and `to = receiver`. Consider adding this for full ERC20 compliance.
2. Additionally, the same Transfer event should be emitted when the `protocolFeeRecipient` and `reserveFeeRecipient` have their shares minted.
3. An equivalent Transfer event is also required when a withdraw occurs, with the `to` address set to `0x0`.
4. This should also apply when a user claims interest. If tokens are being "burned", it must be reflected via a Transfer event.

**Dahlia:** Addressed Transfer event in PR 25.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Dahlia |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, kankodu, Yorke Rhodes |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443

### Keywords for Search

`vulnerability`

