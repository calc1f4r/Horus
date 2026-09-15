---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57276
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 17
finders:
  - 0x23r0
  - io10
  - vasquez
  - lyuboslav
  - xcrypt
---

## Vulnerability Title

Deposits/Withdrawals can be DOS'ed if crvVault::withdraw produces any losses

### Overview

See description below for full details.

### Original Finding Content

## Summary

The Lending Pool's liquidity rebalancing mechanism interacts with a Curve vault to optimize liquidity distribution. However, the \_withdrawFromVault function in LendingPool hardcodes the max\_loss parameter to 0, making the system vulnerable to denial-of-service (DOS) if the Curve vault ever incurs a small, unavoidable loss. This prevents users from withdrawing or depositing funds, disrupting core protocol functionality.

## Vulnerability Details

Users who want to gain RAAC tokens have to deposit crvUSD via LendingPool::deposit which mints Rtokens in return which are then deposited in the stability pool to gain RAAC token rewards. See LendingPool::deposit:

```solidity

    /**
     * @notice Allows a user to deposit reserve assets and receive RTokens
     * @param amount The amount of reserve assets to deposit
     */
    function deposit(uint256 amount) external nonReentrant whenNotPaused onlyValidAmount(amount) {
        // Update the reserve state before the deposit
        ReserveLibrary.updateReserveState(reserve, rateData);

        // Perform the deposit through ReserveLibrary
        uint256 mintedAmount = ReserveLibrary.deposit(reserve, rateData, amount, msg.sender);

        // Rebalance liquidity after deposit
        _rebalanceLiquidity();

        emit Deposit(msg.sender, amount, mintedAmount);
    }

```

According to the documentation, users are allowed to withdraw assets they have deposited via LendingPool::withdraw at any time. See function:

```solidity
 /**
     * @notice Allows a user to withdraw reserve assets by burning RTokens
     * @param amount The amount of reserve assets to withdraw
     */
    function withdraw(uint256 amount) external nonReentrant whenNotPaused onlyValidAmount(amount) {
        if (withdrawalsPaused) revert WithdrawalsArePaused();

        // Update the reserve state before the withdrawal
        ReserveLibrary.updateReserveState(reserve, rateData);

        // Ensure sufficient liquidity is available
        _ensureLiquidity(amount);

        // Perform the withdrawal through ReserveLibrary
        (uint256 amountWithdrawn, uint256 amountScaled, uint256 amountUnderlying) = ReserveLibrary.withdraw(
            reserve,   // ReserveData storage
            rateData,  // ReserveRateData storage
            amount,    // Amount to withdraw
            msg.sender // Recipient
        );

        // Rebalance liquidity after withdrawal
        _rebalanceLiquidity();

        emit Withdraw(msg.sender, amountWithdrawn);
    }
```

LendingPool::deposit and LendingPool::withdraw both call LendingPool::\_rebalanceLiquidity(). This function sets a liquidity buffer ratio which is what determines whether RAAC should deposit excess liquidity to a curve vault to get rewards or not.  So it sets a buffer ratio and if the total available liquidity is greater than the buffer they should have, they deposit the excess into curve vault which is simply a crvUSD vault where users can deposit assets and gain rewards. if the total available liquidity is less than the buffer they should have, they withdraw the shortage from the curve vault. See function below:

```solidity
/**
     * @notice Rebalances liquidity between the buffer and the Curve vault to maintain the desired buffer ratio
     */
    function _rebalanceLiquidity() internal {
        // if curve vault is not set, do nothing
        if (address(curveVault) == address(0)) {
            return;
        }

        uint256 totalDeposits = reserve.totalLiquidity; // Total liquidity in the system
        uint256 desiredBuffer = totalDeposits.percentMul(liquidityBufferRatio);
        uint256 currentBuffer = IERC20(reserve.reserveAssetAddress).balanceOf(reserve.reserveRTokenAddress);

        if (currentBuffer > desiredBuffer) {
            uint256 excess = currentBuffer - desiredBuffer;
            // Deposit excess into the Curve vault
            _depositIntoVault(excess);
        } else if (currentBuffer < desiredBuffer) {
            uint256 shortage = desiredBuffer - currentBuffer;
            // Withdraw shortage from the Curve vault
            _withdrawFromVault(shortage);
        }

        emit LiquidityRebalanced(currentBuffer, totalVaultDeposits);
    }

```

The key DOS for deposits and withdrawals happens in LendingPool::\_withdrawFromVault. See below:

```solidity
 /**
     * @notice Internal function to withdraw liquidity from the Curve vault
     * @param amount The amount to withdraw
     */
    function _withdrawFromVault(uint256 amount) internal {
        curveVault.withdraw(amount, address(this), msg.sender, 0, new address[](0));
        totalVaultDeposits -= amount;
    }
}
```

The curve vault code can be viewed at  . The curve vault contains a withdraw function written in vyper. On inspection of that function, it can be seen that where LendingPool::\_withdrawFromVault passes 0 to the curve vault's withdraw function is a max\_loss variable where the caller specifies the maximum amount of losses they are willing to take during the withdrawal. See the following extracts from the vault code:

```python
def _redeem(
    sender: address, 
    receiver: address, 
    owner: address,
    assets: uint256,
    shares: uint256, 
    max_loss: uint256,
    strategies: DynArray[address, MAX_QUEUE]
) -> uint256:
    """
    This will attempt to free up the full amount of assets equivalent to
    `shares` and transfer them to the `receiver`. If the vault does
    not have enough idle funds it will go through any strategies provided by
    either the withdrawer or the default_queue to free up enough funds to 
    service the request.

    The vault will attempt to account for any unrealized losses taken on from
    strategies since their respective last reports.

    Any losses realized during the withdraw from a strategy will be passed on
    to the user that is redeeming their vault shares unless it exceeds the given
    `max_loss`.
    """
```

There is also the following line in the \_redeem function which is what handles the withdrawal:

```python
  # Check if there is a loss and a non-default value was set.
    if assets > requested_assets and max_loss < MAX_BPS:
        # Assure the loss is within the allowed range.
        assert assets - requested_assets <= assets * max_loss / MAX_BPS, "too much loss"

```

Since the hardcoded value passed as max\_loss is 0, if there is ever a situation where the vault strategy takes losses and needs to pass these losses on to the user, which is RAAC in this case, the transaction will simply revert with "too much loss". As a result, any function that calls  LendingPool::\_rebalanceLiquidity() will also revert which stops RAAC users from being able to perform key functionality. If the Curve vault’s strategy incurs even a tiny loss, no funds can be withdrawn, effectively halting the ability to deposit and withdraw funds in the Lending Pool.

I would write a POC for this but the curve vault is written in vyper and I would have to convert this to solidity which includes knowing what the curve default strategies are how to implement them which is time intensive and impractical when the issue is explainable in text.

## Impact

Denial of Service (DOS) for Deposits & Withdrawals: Since \_rebalanceLiquidity() is triggered in both deposit() and withdraw(), if \_withdrawFromVault() keeps reverting, no users will be able to deposit or withdraw funds.

Liquidity Freeze: Funds that should be withdrawn from the Curve vault remain stuck, leaving the Lending Pool with an insufficient balance to process withdrawals.

Protocol Downtime: If the Curve vault operates normally but produces small losses, the Lending Pool will remain permanently broken unless manually fixed by governance.

## Tools Used

Manual Review

## Recommendations

To prevent this issue:

Make max\_loss configurable: Introduce a function to update the maximum allowable loss dynamically.
Set a reasonable default max\_loss: Instead of 0, consider allowing a small, configurable loss (e.g., 1e16 for 1%).
Fail Gracefully: If a withdrawal reverts due to loss, allow the protocol to adjust or retry with a higher max\_loss.

Suggested Fix:
Modify \_withdrawFromVault() to allow adjustable max\_loss:

```solidity
uint256 public maxLoss = 1e16; // 1% loss tolerance (configurable by governance)

function setMaxLoss(uint256 _maxLoss) external onlyOwner {
    require(_maxLoss <= 1e18, "Max loss too high");
    maxLoss = _maxLoss;
}

function _withdrawFromVault(uint256 amount) internal {
    curveVault.withdraw(amount, address(this), msg.sender, maxLoss, new address );
otalVaultDeposits -= amount;
}
```

This ensures:

RAAC can withdraw funds even with minimal loss.
Governance can adjust maxLoss if needed.
Users are not indefinitely locked out of deposits/withdrawals.
By making maxLoss configurable, the protocol avoids system-wide failures while still ensuring losses remain minimal and controlled.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | 0x23r0, io10, vasquez, lyuboslav, xcrypt, t0x1c, 0xlouistsai, x1485967, whitekittyhacker, recur, orangesantra, mill1995, anonymousjoe, alexczm, 0xaadi, 1337web3, dobrevaleri |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

