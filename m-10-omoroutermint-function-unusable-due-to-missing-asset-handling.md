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
solodit_id: 53340
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

[M-10] `OmoRouter.mint` function unusable due to missing asset handling

### Overview


This bug report discusses an issue with the `OmoRouter.mint()` function in the Omo protocol. The function is supposed to call another function called `IOmoVault.mint()` to mint shares for a receiver, but it is currently not working properly. This is because the function is not pulling assets from the user and is not approving the vault to spend the deposited assets. As a result, the `mint()` function is unusable. The recommendation is to update the `OmoRouter.mint()` function to pull assets from the user and approve the vault before calling `IOmoVault.mint()`. This will fix the issue and make the function work properly.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `OmoRouter.mint()` function is intended to call `IOmoVault(vault).mint()`, where the vault pulls assets from the router and mints shares for the `receiver, however, the implementation is incomplete and lacks key steps to facilitate this process:

1. The function does not pull assets from the user.
2. The function does not approve the vault to spend the deposited assets.

as a result, the vault will be unable to pull the required assets, rendering the `mint()` function unusable.

```javascript
// OmoRouter
  function mint(
        uint256 vaultId,
        uint256 shares,
        address receiver
    ) external onlyWhitelisted returns (uint256 assets) {
        address vault = vaultFactory.getVault(vaultId);
        if (!isVaultEnabled[msg.sender][vault]) revert VaultNotEnabled();
        return IOmoVault(vault).mint(shares, receiver);
    }
```

## Recommendation

Update `OmoRouter.mint()` function to pull the assets that will be deposited from the user, and approve the `OmoVault` to spend the deposited assets before calling `IOmoVault(vault).mint()`:

```diff
function mint(
    uint256 vaultId,
    uint256 shares,
    address receiver
) external onlyWhitelisted returns (uint256 assets) {
    address vault = vaultFactory.getVault(vaultId);
    if (!isVaultEnabled[msg.sender][vault]) revert VaultNotEnabled();

+   ERC20 token = ERC20(IERC4626(vault).asset());

+   uint256 initialBalance = token.balanceOf(address(this));
+   token.safeTransferFrom(msg.sender, address(this), shares);
+   uint256 receivedAssets = token.balanceOf(address(this)) - initialBalance;

+   token.safeApprove(vault, receivedAssets);

    return IOmoVault(vault).mint(shares, receiver);
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

