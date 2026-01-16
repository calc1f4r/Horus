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
solodit_id: 62368
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-17-Astrolab.md
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
  - Hexens
---

## Vulnerability Title

[ASTRO-24] Wrong rebalance implementation

### Overview


This bug report describes a medium severity issue in the Crate.sol code. When a user withdraws their assets or shares using the `withdraw()` or `redeem()` functions, the pool is not being rebalanced. This means that if another user also wants to withdraw, they may receive the wrong amount of shares and assets. This can result in a lower price for the shares and the protocol earning more from the transaction. The suggested solution is to rebalance the pool before each withdrawal and change the `revert` statement to an `if` statement to prevent the transaction from being reverted. This bug has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** Crate.sol

**Description:** When a user withdraws their assets or shares using the `withdraw()` or `redeem()` functions, the pool is not being rebalanced. Therefore, if the case of another user also wants to withdraw, they may end up withdrawing the wrong amount of shares since the shares will not be rebalanced at that point. This can result in a lower price for the shares, causing the second user to receive fewer assets than they should. Additionally, the protocol will earn more from this transaction.
```
    function _withdraw(
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

    // !SECTION

    /*//////////////////////////////////////////////////////////////
                        // SECTION LIQUIDITY MANAGEMENT
    //////////////////////////////////////////////////////////////*/

    // TODO: Should this function be whitelisted?
    /// @notice Rebalance the Liquidity pool using idle funds and liquid strats
    function rebalanceLiquidityPool()
        public
        whenNotPaused
        returns (uint256 earned)
    {
        // Reverts if we the LP is not enabled
        if (!liquidityPoolEnabled) revert LiquidityPoolNotSet();

        // We check if we have enough funds to rebalance
        uint256 toSwap = _getAmountToSwap(
            asset.balanceOf(address(this)),
            liquidityPool
        );

        if (toSwap == 0) revert NoFundsToRebalance();
        uint256 recovered = liquidityPool.swap.swapAssetToVirtual(
            toSwap,
            block.timestamp + 100
        );
        liquidityPool.debt += recovered;
        earned = recovered - Math.min(toSwap, recovered);

        emit LiquidityRebalanced(recovered, earned);
        emit SharePriceUpdated(sharePrice(), block.timestamp);
    }
```


**Remediation:**  Consider rebalancing before each withdrawal to ensure the correctness of the output amount. For not getting reverted, in case of the pool is already rebalanced, consider changing `revert` from `rebalanceLiquidityPool()` to f.e `if` statement implementation.

**Status:**  Fixed


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

