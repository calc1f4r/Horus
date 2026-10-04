---
# Core Classification
protocol: Tea
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46111
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/39be06ba-70a1-44a4-b963-dc0c1e66c5e1
source_link: https://cdn.cantina.xyz/reports/cantina_teaxyz_december2024.pdf
github_link: none

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
finders_count: 2
finders:
  - m4rio
  - Sujith Somraaj
---

## Vulnerability Title

Increase test coverage 

### Overview

See description below for full details.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
There is less than complete test coverage of key contracts under review. Adequate test coverage and regular reporting are essential to ensure the codebase works as intended. Insufficient code coverage may lead to unexpected issues and regressions.

## Recommendation
Add to test coverage, ensuring all execution paths/branches are covered. The missing test cases are added as follows:

## Test Transfer Functionality
```solidity
function test_transfer_functionality() public {
    vm.warp(block.timestamp + 365 days);
    // Mint some tokens to alice
    vm.prank(initialGovernor.addr);
    mintManager.mintTo(alice.addr, 100);
    // Test transfer
    vm.prank(alice.addr);
    tea.transfer(bob.addr, 50);
    assertEq(tea.balanceOf(alice.addr), 50);
    assertEq(tea.balanceOf(bob.addr), 50);
}
```

## Test Approve and TransferFrom
```solidity
function test_approve_and_transferFrom() public {
    vm.warp(block.timestamp + 365 days);
    // Mint some tokens to alice
    vm.prank(initialGovernor.addr);
    mintManager.mintTo(alice.addr, 100);
    // Alice approves Bob to spend 30 tokens
    vm.prank(alice.addr);
    tea.approve(bob.addr, 30);
    // Bob transfers 20 tokens from Alice to himself
    vm.prank(bob.addr);
    tea.transferFrom(alice.addr, bob.addr, 20);
    assertEq(tea.balanceOf(alice.addr), 80);
    assertEq(tea.balanceOf(bob.addr), 20);
    assertEq(tea.allowance(alice.addr, bob.addr), 10);
}
```

## Test Burn Functionality
```solidity
function test_burn_succeed() public {
    vm.warp(block.timestamp + 365 days);
    vm.prank(initialGovernor.addr);
    mintManager.mintTo(alice.addr, 1);
    vm.prank(alice.addr);
    tea.approve(address(this), 1);
    tea.burnFrom(alice.addr, 1);
    assertEq(tea.totalSupply(), tea.INITIAL_SUPPLY());
    assertEq(tea.totalMinted(), tea.INITIAL_SUPPLY() + 1);
    assertEq(tea.balanceOf(alice.addr), 0);
}
```

## Test Zero Address Transfers
```solidity
function test_zero_address_transfers() public {
    vm.warp(block.timestamp + 365 days);
    vm.prank(initialGovernor.addr);
    mintManager.mintTo(alice.addr, 100);
    vm.prank(alice.addr);
    vm.expectRevert(abi.encodeWithSelector(IERC20Errors.ERC20InvalidReceiver.selector, address(0)));
    tea.transfer(address(0), 50);
}
```

## Test Mint to Zero Address
```solidity
function test_mint_toZeroAddress_reverts() external {
    vm.warp(block.timestamp + 365 days);
    vm.prank(initialGovernor.addr);
    vm.expectRevert(abi.encodeWithSelector(IERC20Errors.ERC20InvalidReceiver.selector, address(0)));
    mintManager.mintTo(address(0), 100);
}
```

## Test Multiple Mints Within Period
```solidity
function test_mint_multipleMints_withinPeriod_reverts() external {
    // First mint after 1 year
    vm.warp(block.timestamp + 365 days);
    vm.startPrank(initialGovernor.addr);
    // Mint 1% first
    uint256 onePercent = (tea.totalSupply() * 10) / mintManager.DENOMINATOR();
    mintManager.mintTo(initialGovernor.addr, onePercent);
    // Try to mint another 1% - should fail as the mint period has not elapsed
    uint256 onePointFivePercent = (tea.totalSupply() * 10) / mintManager.DENOMINATOR();
    vm.expectRevert("MintManager: minting not permitted yet");
    mintManager.mintTo(initialGovernor.addr, onePointFivePercent);
    vm.stopPrank();
}
```

## Test Minting at Period Boundary
```solidity
function test_mint_exactlyAtPeriodBoundary_reverts() external {
    uint256 ts = block.timestamp;
    // First mint after 1 year
    vm.warp(ts + 365 days);
    vm.prank(initialGovernor.addr);
    mintManager.mintTo(initialGovernor.addr, 100);
    // Try minting exactly at mintPermittedAfter (should fail)
    vm.warp(ts + 365 days + mintManager.MINT_PERIOD() - 1);
    vm.prank(initialGovernor.addr);
    vm.expectRevert("MintManager: minting not permitted yet");
    mintManager.mintTo(initialGovernor.addr, 100);
}
```

## Test Minting at Cap Limit
```solidity
function test_mint_exactlyAtCap_succeeds() external {
    vm.warp(block.timestamp + 365 days);
    vm.startPrank(initialGovernor.addr);
    // Calculate exact 2% of total supply
    uint256 exactCap = (tea.totalSupply() * mintManager.MINT_CAP()) / mintManager.DENOMINATOR();
    mintManager.mintTo(initialGovernor.addr, exactCap);
    // Verify balance increased by exactly 2%
    assertEq(
        tea.balanceOf(initialGovernor.addr),
        tea.INITIAL_SUPPLY() + exactCap
    );
    vm.stopPrank();
}
```

## Test Upgrade from Owner (with more assertions)
```solidity
function test_upgrade_fromOwner_succeeds() external {
    // Upgrade to new mintManager
    vm.prank(initialGovernor.addr);
    mintManager.upgrade(alice.addr);
    // Check pending state
    assertEq(tea.owner(), address(mintManager));
    assertEq(tea.pendingOwner(), alice.addr);
    vm.prank(alice.addr);
    tea.acceptOwnership();
    // New manager is alice.addr
    assertEq(tea.owner(), alice.addr);
    assertEq(tea.pendingOwner(), address(0));
}
```

The above tests use `IERC20Errors` from `@openzeppelin/contracts/interfaces/draft-IERC6093.sol`; hence, import them appropriately.

**Tea:** Fixed in commit f79268d7.  
**Cantina Managed:** Fixed. Other branch of `TokenDeploy.sol#L53` can never be covered ig.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Tea |
| Report Date | N/A |
| Finders | m4rio, Sujith Somraaj |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_teaxyz_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/39be06ba-70a1-44a4-b963-dc0c1e66c5e1

### Keywords for Search

`vulnerability`

