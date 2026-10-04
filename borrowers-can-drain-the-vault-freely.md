---
# Core Classification
protocol: Steadefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35558
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-15-Steadefi.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

BORROWERS CAN DRAIN THE VAULT FREELY

### Overview


The report describes a bug where borrowers can take assets without leaving any collateral, allowing them to run away with the assets and not pay back their debt. This can lead to a scenario where one borrower can take all the funds from multiple lenders. The bug also affects the ability to withdraw assets and can impact the calculation of shares for users. The report recommends implementing a mechanism to force borrowers to deposit collateral and adding more rules to govern borrowing. It also suggests decentralizing the approval process for borrowers.

### Original Finding Content

**Severity:** Medium	

**Status:** Acknowledged

**Description**

Borrowers are allowed to borrow assets but they are not paying any collateral so that they can leave with the asset and never pay their debt back. The borrow() function is only callable by users set as borrowers so that any user set as borrower can drain the vault easily and freely.

This can lead to scenarios where any single authorized borrower can run away with all the funds of all the lenders or depositors. For example, let’s say there are 2 depositors- Alice and Jim. Alice deposits 10 x 10**18 of Native tokens while Jim deposits 1 x 10**18 Native tokens. Then it is possible that an authorized borrower say Bob borrows all of 11 x 10**18 tokens and runs away.

borrow(uint256 borrowAmt):
```solidity
function borrow(uint256 borrowAmt) external nonReentrant whenNotPaused onlyBorrower {
   if (borrowAmt == 0) revert Errors.InsufficientBorrowAmount();
   if (borrowAmt > totalAvailableAsset()) revert Errors.InsufficientLendingLiquidity();

   // Update vault with accrued interest and latest timestamp
   _updateVaultWithInterestsAndTimestamp(0);

   // Calculate debt amount
   uint256 _debt = totalBorrows == 0 ? borrowAmt : borrowAmt * totalBorrowDebt / totalBorrows;

   // Update vault state
   totalBorrows = totalBorrows + borrowAmt;
   totalBorrowDebt = totalBorrowDebt + _debt;

   // Update borrower state
   Borrower storage borrower = borrowers[msg.sender];
   borrower.debt = borrower.debt + _debt;
   borrower.lastUpdatedAt = block.timestamp;

   // Transfer borrowed token from vault to manager
   asset.safeTransfer(msg.sender, borrowAmt); 
   emit Borrow(msg.sender, _debt, borrowAmt);
 }

```

The described scenario is directly affecting the `withdraw()` functionality. If a borrower drains the vault freely then the rest of the users will not be able to withdraw any asset by calling the `withdraw()` function.

The described scenario would also impact on the amount of shares calculation for user’s minting.

`_shares = assetAmt * totalSupply() / (totalAsset() - assetAmt);`


`totalAsset()` is used as denominator in the operation and totalAsset() is:
```solidity
function totalAsset() public view returns (uint256) {
   return totalBorrows + _pendingInterests(0) + totalAvailableAsset(); 
}
```

As it can bee seen totalAsset() is not only the actual amount of assets in the vault (totalAvailableAsset()) but the addition of it with every pending interest and the total amount of borrows (totalBorrows). This means that if a borrower can borrow unlimited amount without any collateral he can freely inflate totalAsset() and a consequence reduce the amount of shares calculated.

**Proof of concept:**
```solidity
function testBorrowTheWholeVaultFreely() public {
       vm.startPrank(address(alice));
       vault.approveBorrower(address(bob)); // Approve Bob as borrower
       vm.stopPrank();

       deal(jim, 10 ether);
       vm.startPrank(jim);
       vault.depositNative{value: 1 ether}(1 ether, 0); // User deposit 1 ether
       vm.stopPrank();

       vm.startPrank(bob);
       uint256 balanceBefore = IERC20(asset).balanceOf(bob);
       vault.borrow(1 ether); // bob borrowers 1 ether and does not pay it back
       uint256 balanceAfter = IERC20(asset).balanceOf(bob);


       assert(balanceAfter > balanceBefore);
       assert(balanceAfter == balanceBefore + 1 ether);
   }

```
**Recommendation:**

The borrow function must implement a mechanism that forces the borrower to deposit a collateral when borrowing assets. This collateral should be kept by the contract/protocol until borrowers pay their debt back. Ideally the collateral should be able to get liquidated, enforcing the borrower to keep a healthy position.

It is advised to add robust and concrete rules that govern borrowing of the assets. This can be done by adding more rules in the smart contract or writing a Borrow smart contract that governs and securely manages borrowing from the Vault including the borrow() function. In addition to that it is advised to decentralize the calling of approveBorrower() function further by the usage of multisigs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Steadefi |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-05-15-Steadefi.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

