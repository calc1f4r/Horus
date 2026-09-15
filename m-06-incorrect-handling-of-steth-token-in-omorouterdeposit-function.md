---
# Core Classification
protocol: Omo_2025-01-25
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53336
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-06] Incorrect handling of `stETH` token in `OmoRouter.deposit()` function

### Overview


This bug report is about a problem with the `OmoRouter.deposit()` function in the OmoVaults contract. The issue occurs when using the `stETH` token, which is one of the supported assets in the contract. The problem is that the function does not handle transfers of `stETH` correctly, causing it to transfer 1-2 wei less than the specified amount. This leads to the contract trying to deposit more tokens than it actually received, resulting in a failed transaction due to insufficient balance. The same issue also exists in other functions related to deposits and repayments. The report recommends updating the `OmoRouter.deposit()` function to correctly deposit the actual amount received.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

- The `OmoRouter.deposit()` function doesn't correctly handle the `stETH` token, which is one of the LST tokens supported as an underlying asset in `OmoVaults`, the issue arises because `stETH` transfers **1-2 wei less than the amount specified during a `safeTransferFrom` operation**.

- This leads to the `OmoRouter` contract approving and attempting to deposit more tokens than it has received, causing the subsequent `OmoVault.deposit()` call to revert due to insufficient contract balance (received is less than deposited).

```javascript
 function deposit(
        uint256 vaultId,
        uint256 assets,
        address receiver
    ) external onlyWhitelisted returns (uint256 shares) {
        address vault = vaultFactory.getVault(vaultId);
        if (!isVaultEnabled[msg.sender][vault]) revert VaultNotEnabled();

        // Get the underlying token using IERC4626
        ERC20 token = ERC20(IERC4626(vault).asset());

        // Transfer tokens from user to router
        token.safeTransferFrom(msg.sender, address(this), assets);

        // Approve vault to spend tokens
        token.safeApprove(vault, assets);

        // Deposit into vault
        shares = IOmoVault(vault).deposit(assets, receiver);

        return shares;
    }
```

- The same issue exists in:
  - `OmoVault.deposit()` function when whitelisted users interact directly with the function.
  - `OmoVault.topOff()` and `OmoAgent.repayAsset()` functions.

## Recommendations

Update `OmoRouter.deposit()` to deposit the actual amount received:

```diff
 function deposit(
        uint256 vaultId,
        uint256 assets,
        address receiver
    ) external onlyWhitelisted returns (uint256 shares) {
        address vault = vaultFactory.getVault(vaultId);
        if (!isVaultEnabled[msg.sender][vault]) revert VaultNotEnabled();

        // Get the underlying token using IERC4626
        ERC20 token = ERC20(IERC4626(vault).asset());

        // Transfer tokens from user to router
+       uint256 balanceBefore = token.balanceOf(address(this));
        token.safeTransferFrom(msg.sender, address(this), assets);
+       uint256 amountToDeposit = token.balanceOf(address(this)) - balanceBefore;
        // Approve vault to spend tokens
-       token.safeApprove(vault, assets);
+       token.safeApprove(vault, amountToDeposit);

        // Deposit into vault
-       shares = IOmoVault(vault).deposit(assets, receiver);
+       shares = IOmoVault(vault).deposit(amountToDeposit, receiver);

        return shares;
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Omo_2025-01-25 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Omo-security-review_2025-01-25.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

