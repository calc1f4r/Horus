---
# Core Classification
protocol: RegnumAurum_2025-08-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63404
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2025-08-12.md
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

[M-02] Same block deposit check blocks `StabilityPool` withdrawals during liquidation

### Overview


This bug report discusses an issue with the `StabilityPool` liquidation process in a specific smart contract. When liquidating user positions, there may not be enough funds available in the `StabilityPool` to cover the liquidation. In these cases, the contract withdraws the remaining funds from the `LendingPool`, which can cause the liquidation to fail due to a check in the code. This can lead to failed liquidations and increased costs for liquidators. The report recommends excluding the `StabilityPool` address from the check to prevent this issue from occurring.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

When the `StabilityPool` liquidates user positions, it may lack enough `crvUSDToken` to cover the liquidation. In such cases, it withdraws the shortfall from the `LendingPool`, which burns the corresponding `rToken` and transfers the underlying `crvUSD` to the `StabilityPool`:

```solidity
// LiquidationStrategyProxy contract:
function liquidateBorrower(address poolAdapter, address vaultAdapter, address user, bytes calldata data, uint256 minSharesOut) external onlyProxy {
        //...

        uint256 scaledPositionDebt = lendingPool.getPositionScaledDebt(poolAdapter, user, data);
        uint256 initialCRVUSDBalance = crvUSDToken.balanceOf(address(this));
        uint256 availableRTokens = rToken.balanceOf(address(this));

        // We need to get the amount of rToken that is needed to cover the debt, or 0 if the debt is covered
        uint256 rTokenAmountRequired = initialCRVUSDBalance >= scaledPositionDebt ? 0 : scaledPositionDebt - initialCRVUSDBalance;
        if (availableRTokens < rTokenAmountRequired) revert InsufficientBalance();

        // We unwind the position
        if (rTokenAmountRequired > 0) {
>>           lendingPool.withdraw(rTokenAmountRequired);
        }
        //...
}
```

At the end of liquidation, any leftover `crvUSDToken` (e.g. swapped from `iRAAC`) will be deposited back into the `LendingPool`. This deposit sets `depositBlock[StabilityPool] = block.number`:

```solidity
// LiquidationStrategyProxy contract
    function liquidateBorrower(address poolAdapter, address vaultAdapter, address user, bytes calldata data, uint256 minSharesOut) external onlyProxy {
    //...

        _handleLiquidation(poolAdapter, vaultAdapter, data, minSharesOut);

        // Deposit crvUSD back to get rTokens (including the excess)
        // Get the final crvUSD balance after the exchange
        uint256 finalCRVUSDBalance = crvUSDToken.balanceOf(address(this));
        if (finalCRVUSDBalance > 0) {
            // Approve lending pool to take crvUSD for deposit
            bool approveCRVUSDDeposit = crvUSDToken.approve(address(lendingPool), finalCRVUSDBalance);
            if (!approveCRVUSDDeposit) revert ApprovalFailed();
>>           lendingPool.deposit(finalCRVUSDBalance);
        }
        emit BorrowerLiquidated(user, IAssetAdapter(poolAdapter).getAssetToken(), data, scaledPositionDebt);
    }
```

```solidity
// LendingPool contract:
 function deposit(uint256 amount) external nonReentrant whenNotPaused onlyValidAmount(amount) notBlacklisted(msg.sender) {
        //...

>>       depositBlock[msg.sender] = block.number;

        //...
    }
```

If another liquidation occurs within the same block and again requires a withdrawal from the `LendingPool`, the `LendingPool.withdraw()` call will revert due to the following check in the `RToken._update()` when trying to transfer `rToken` from the `StabilityPool` to the `LendingPool` :

```solidity
 function _update(address from, address to, uint256 amount) internal override {
        //...
        if (ILendingPool(_lendingPool).isUserDepositInSameBlock(from)) revert CannotDepositAndTransferInSameBlock();
        //...
    }
```

This prevents liquidation from completing other liquidations in the same block, leading to failed liquidations and increased costs for liquidators due to accrued interest.

## Recommendations

Exclude the `StabilityPool` address from the block-based same-block deposit check:

```diff
// LendingPool contract:
 function deposit(uint256 amount) external nonReentrant whenNotPaused onlyValidAmount(amount) notBlacklisted(msg.sender) {
        //...

-       depositBlock[msg.sender] = block.number;
+       if (msg.sender != stabilityPool) depositBlock[msg.sender] = block.number;

        //...
    }
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RegnumAurum_2025-08-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RegnumAurum-security-review_2025-08-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

