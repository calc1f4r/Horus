---
# Core Classification
protocol: Astrolab
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62366
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-17-Astrolab.md
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
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[ASTRO-13] Wrong debt calculations during withdrawal

### Overview


Severity: Critical
Path: Crate.sol
Description: The functions safeWithdraw and safeRedeem have inconsistent debt calculation logic, allowing a bad actor to manipulate the system and potentially steal funds. This is due to the fact that the _withdraw() function decreases the liquidityPool.debt before executing the try/catch block, which can result in incorrect calculations and affect other functions such as increaseLiquidity, decreaseLiquidity, and assetToShare.
Remediation: The recommended solution is to move the decrease of liquidityPool.debt inside the try block to ensure accurate calculations and prevent potential attacks.
Status: This issue has been fixed.

### Original Finding Content

**Severity:** Critical

**Path:** Crate.sol

**Description:** The functions `safeWithdraw`, and `safeRedeem` have inconsistent debt calculation logic.

A bad actor can call `safeWithdraw/safeRedeem` function with such parameters that revert `swapVirtualToAsset` function call (for example, with a past deadline). That function is executed in try/catch block, but before the `try/catch` the `_withdraw()` function decreases `liquidityPool.debt`. Even if `swapToVirtualAsset()` reverts the `liquidityPool.debt` will already be decreased.

As a result, `_withdraw()` function decreases `crate.totalAssets()` twice. It affects all calculations, f.e `increaseLiquidity`, `decreaseLiquidity`, `rebalanceLiquidity`, `shareToAsset`, `assetToShare`, etc.
```    function _withdraw(
        uint256 _amount,
        uint256 _shares,
        uint256 _minAmountOut,
        uint256 _deadline,
        address _receiver,
        address _owner
    ) internal nonReentrant returns (uint256 recovered) {
        if (_amount == 0 || _shares == 0) revert AmountZero();

        // We spend the allowance if the msg.sender isn't the receiver
        if (msg.sender != _owner) {
            _spendAllowance(_owner, msg.sender, _shares);
        }

        // Check for rounding error since we round down in previewRedeem.
        if (convertToAssets(_shares) == 0)
            revert IncorrectAssetAmount(convertToAssets(_shares));

        // We burn the tokens
        _burn(_owner, _shares);

        // Allows to take a withdraw fee
        _amount = (_amount * (MAX_BPS - withdrawFee)) / MAX_BPS;

        if (liquidityPoolEnabled) {
            // We don't take into account the eventual slippage, since it will
            // be paid to the depositoors
            liquidityPool.debt -= Math.min(_amount, liquidityPool.debt);
            try
                liquidityPool.swap.swapVirtualToAsset(
                    _amount,
                    _minAmountOut,
                    _deadline,
                    _receiver
                )
            returns (uint256 dy) {
                recovered = dy;
            } catch {
                // if the swap fails, we send the funds available
                asset.safeTransfer(_receiver, _amount);
                recovered = _amount;
            }
        } else {
            // If the liquidity pool is not enabled, we send the funds available
            // This allows for the bootstrapping of the pool at start
            asset.safeTransfer(_receiver, _amount);
            recovered = _amount;
        }

        if (_minAmountOut > 0 && recovered < _minAmountOut)
            revert IncorrectAssetAmount(recovered);

        emit Withdraw(msg.sender, _receiver, _owner, _amount, _shares);
        return (recovered);
    }
```

**Remediation:**  We would recommend to move decreasing liquididyPool.dept decreasing in `try` block. 

**Status:**  Fixed


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Astrolab |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-17-Astrolab.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

