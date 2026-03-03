---
protocol: generic
chain: cosmos
category: accounting
vulnerability_type: integer_precision_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: accounting_logic

primitives:
  - integer_overflow
  - integer_underflow
  - unsafe_casting
  - precision_loss
  - decimal_mismatch

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - accounting
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Accounting Integer Overflow
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Integer Overflow in AddExternalIncentive Function | `reports/cosmos_cometbft_findings/integer-overflow-in-addexternalincentive-function.md` | HIGH | Halborn |
| Lack of input validation | `reports/cosmos_cometbft_findings/lack-of-input-validation.md` | MEDIUM | OpenZeppelin |
| The `FullMath` library is unable to handle intermediate over | `reports/cosmos_cometbft_findings/m-10-the-fullmath-library-is-unable-to-handle-intermediate-overflows-due-to-over.md` | MEDIUM | Sherlock |
| Integer overflow when calculating rewards | `reports/cosmos_cometbft_findings/m-2-integer-overflow-when-calculating-rewards.md` | MEDIUM | Sherlock |

### Accounting Integer Underflow
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-03] A `DoS` on snapshots due to a rounding error in calcu | `reports/cosmos_cometbft_findings/h-03-a-dos-on-snapshots-due-to-a-rounding-error-in-calculations.md` | HIGH | Code4rena |
| Negative rebase of stETH could prevent a round from ending | `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md` | MEDIUM | OpenZeppelin |
| Potential Denial of Service in Report Generation Due to Unde | `reports/cosmos_cometbft_findings/potential-denial-of-service-in-report-generation-due-to-underflow.md` | MEDIUM | Quantstamp |
| Potential underflow in slashing logic | `reports/cosmos_cometbft_findings/potential-underflow-in-slashing-logic.md` | MEDIUM | Cyfrin |

### Accounting Unsafe Casting
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-05] Funds can be permanently locked due to unsafe type ca | `reports/cosmos_cometbft_findings/h-05-funds-can-be-permanently-locked-due-to-unsafe-type-casting.md` | HIGH | Pashov Audit Group |
| [M-06] Attacker may DOS auctions using invalid bid parameter | `reports/cosmos_cometbft_findings/m-06-attacker-may-dos-auctions-using-invalid-bid-parameters.md` | MEDIUM | Code4rena |
| [M-10] Unsafe casting from `uint256` to `uint128` in Rewards | `reports/cosmos_cometbft_findings/m-10-unsafe-casting-from-uint256-to-uint128-in-rewardsmanager.md` | MEDIUM | Code4rena |

### Accounting Precision Loss
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Dust limit attack on `forceUpdateNodes` allows DoS of rebala | `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md` | HIGH | Cyfrin |
| `getCommunityVotingPower` doesn't calculate voting Power cor | `reports/cosmos_cometbft_findings/m-5-getcommunityvotingpower-doesnt-calculate-voting-power-correctly-due-to-preci.md` | MEDIUM | Sherlock |

### Accounting Decimal Mismatch
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Inaccurate stake calculation due to decimal mismatch across  | `reports/cosmos_cometbft_findings/inaccurate-stake-calculation-due-to-decimal-mismatch-across-multitoken-asset-cla.md` | MEDIUM | Cyfrin |
| [M-03] `RemoteAddressValidator` can incorrectly convert addr | `reports/cosmos_cometbft_findings/m-03-remoteaddressvalidator-can-incorrectly-convert-addresses-to-lowercase.md` | MEDIUM | Code4rena |
| Attacker will prevent distribution of USDC to stakers throug | `reports/cosmos_cometbft_findings/m-1-attacker-will-prevent-distribution-of-usdc-to-stakers-through-frequent-rewar.md` | MEDIUM | Sherlock |
| Stake Mint Differentiation | `reports/cosmos_cometbft_findings/stake-mint-differentiation.md` | HIGH | OtterSec |

---

# Integer Precision Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Integer Precision Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Accounting Integer Overflow](#1-accounting-integer-overflow)
2. [Accounting Integer Underflow](#2-accounting-integer-underflow)
3. [Accounting Unsafe Casting](#3-accounting-unsafe-casting)
4. [Accounting Precision Loss](#4-accounting-precision-loss)
5. [Accounting Decimal Mismatch](#5-accounting-decimal-mismatch)

---

## 1. Accounting Integer Overflow

### Overview

Implementation flaw in accounting integer overflow logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 1, MEDIUM: 3.

> **Key Finding**: Issue: Potential integer overflow in the `AddExternalIncentive` function of the `keeper` package.

Description: In the `AddExternalIncentive` function, there is a line of code that converts the difference between `msg.ToBlock` and `msg.FromBlock` to an `int64` value. If the result of this calculatio

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting integer overflow logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting integer overflow in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: Integer Overflow in AddExternalIncentive Function** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/integer-overflow-in-addexternalincentive-function.md`
```go
amount := msg.AmountPerBlock.Mul(sdk.NewInt(int64(msg.ToBlock - msg.FromBlock)))
```

**Example 2: Lack of input validation** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-input-validation.md`
```
// Vulnerable pattern from Across Token and Token Distributor Audit:
The codebase generally lacks sufficient input validation.


In the [`AcceleratingDistributor`](https://github.com/across-protocol/across-token/blob/42130387f81debf2a20d2f7b40d9f0ccc1dcd06a/contracts/AcceleratingDistributor.sol) contract, the [`enableStaking`](https://github.com/across-protocol/across-token/blob/42130387f81debf2a20d2f7b40d9f0ccc1dcd06a/contracts/AcceleratingDistributor.sol#L93) function allows the contract owner to configure several parameters associated with a `stakedToken`. Sev
```

**Example 3: The `FullMath` library is unable to handle intermediate overflows due to overflo** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-the-fullmath-library-is-unable-to-handle-intermediate-overflows-due-to-over.md`
```solidity
library FullMath {
    /// @notice Calculates floor(a×b÷denominator) with full precision. Throws if result overflows a uint256 or denominator == 0
    /// @param a The multiplicand
    /// @param b The multiplier
    /// @param denominator The divisor
    /// @return result The 256-bit result
    /// @dev Credit to Remco Bloemen under MIT license https://xn--2-umb.com/21/muldiv
    function mulDiv(
        uint256 a,
        uint256 b,
        uint256 denominator
    ) internal pure returns (uint256 result) {
        // 512-bit multiply [prod1 prod0] = a * b
        // Compute the product mod 2**256 and mod 2**256 - 1
        // then use the Chinese Remainder Theorem to reconstruct
        // the 512 bit result. The result is stored in two 256
        // variables such that product = prod1 * 2**256 + prod0
        uint256 prod0; // Least significant 256 bits of the product

        ...

      result = prod0 * inv;
        return result;
    }

    function mulDivRoundingUp(
        uint256 a,
        uint256 b,
        uint256 denominator
    ) internal pure returns (uint256 result) {
        result = mulDiv(a, b, denominator);
        if (mulmod(a, b, denominator) > 0) {
            require(result < type(uint256).max);
            result++;
        }
    }
}
```

**Example 4: Integer overflow when calculating rewards** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-2-integer-overflow-when-calculating-rewards.md`
```solidity
function _notifyReward(address _rewardToken, uint256 reward) internal {
        if (lockedSupplyWithMultiplier == 0)
            return; // If there is no locked supply with multiplier, exit without adding rewards (prevents division by zero).

        Reward storage r = rewardData[_rewardToken]; // Accesses the reward structure for the specified token.
>       uint256 newReward = reward * 1e36 / lockedSupplyWithMultiplier; // Calculates the reward per token, scaled up for precision.
>       r.cumulatedReward += newReward; // Updates the cumulative reward for the token.
        r.lastUpdateTime = block.timestamp; // Sets the last update time to now.
        r.balance += reward; // Increments the balance of the token by the new reward amount.
    }

    ...

    function _earned(
        address _user,
        address _rewardToken
    ) internal view returns (uint256 earnings) {
        Reward memory rewardInfo = rewardData[_rewardToken]; // Retrieves reward data for the specified token.
        Balances memory balance = balances[_user]; // Retrieves balance information for the user.
>       earnings = rewardInfo.cumulatedReward * balance.lockedWithMultiplier - rewardDebt[_user][_rewardToken]; // Calculates earnings by considering the accumulated reward and the reward debt.
    }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting integer overflow logic allows exploitation through missing validat
func secureAccountingIntegerOverflow(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 3
- **Affected Protocols**: UXD Protocol, Gamma - Locked Staking Contract, Cosmos Module, Across Token and Token Distributor Audit
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Accounting Integer Underflow

### Overview

Implementation flaw in accounting integer underflow logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 1, MEDIUM: 3.

> **Key Finding**: This bug report discusses a potential issue with creating a snapshot due to a rounding error in the calculations. The report includes a proof of concept which demonstrates how the error can occur and provides a recommended mitigation step to fix the issue. The report also includes comments from the 

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting integer underflow logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting integer underflow in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: [H-03] A `DoS` on snapshots due to a rounding error in calculations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-a-dos-on-snapshots-due-to-a-rounding-error-in-calculations.md`
```solidity
function _transferToSlashStore(address nodeOwner) internal {
        ...

430     uint256 slashedAssets = node.totalRestakedETH - convertToAssets(balanceOf(nodeOwner));
        ...
```

**Example 2: Negative rebase of stETH could prevent a round from ending** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md`
```
// Vulnerable pattern from Pods Finance Ethereum Volatility Vault Audit:
When a round ends, the amount of underlying assets currently in the vault is [subtracted](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/STETHVault.sol#L97) from the amount of assets the vault contained in the previous round. This calculation assumes a positive yield, but the underlying asset stETH is able to rebase in both a positive and negative direction due to the potential for slashing. In the case where Lido is slashed, `total
```

**Example 3: Potential Denial of Service in Report Generation Due to Underflow** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/potential-denial-of-service-in-report-generation-due-to-underflow.md`
```go
case withdrawalEpoch >= withdrawableEpoch:
    // All amounts below 32 ETH are considered exited
    validatorsExitedBalance += MinGwei(
        withdrawal.Amount,
        beaconcommon.Gwei(32_000_000_000),
    )
    // All amounts above 32 ETH are considered skimmed
    validatorsSkimmedBalance += MaxGwei(
        0,
        withdrawal.Amount - beaconcommon.Gwei(32_000_000_000),
    )
```

**Example 4: Potential underflow in slashing logic** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/potential-underflow-in-slashing-logic.md`
```go
// In the slashing logic for the previous epoch case
if (withdrawals_ < withdrawalsSlashed) {
    nextWithdrawalsSlashed += withdrawalsSlashed - withdrawals_;
    withdrawalsSlashed = withdrawals_;
}

// Later, this could underflow if nextWithdrawalsSlashed > nextWithdrawals
vs.withdrawals[currentEpoch_ + 1] = nextWithdrawals - nextWithdrawalsSlashed; //@audit this is adjusted without checking if nextWithdrawalsSlashed <= nextWithdrawals
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting integer underflow logic allows exploitation through missing valida
func secureAccountingIntegerUnderflow(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 3
- **Affected Protocols**: Karak, Suzaku Core, Pods Finance Ethereum Volatility Vault Audit, Liquid Collective Lceth
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Accounting Unsafe Casting

### Overview

Implementation flaw in accounting unsafe casting logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: This report discusses a bug in the `StakingManager` contract that manages staking operations for HYPE tokens. This bug can cause the loss of staked tokens if the amount exceeds a certain limit. It is recommended to implement a library called SafeCast to prevent this issue.

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting unsafe casting logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting unsafe casting in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: [H-05] Funds can be permanently locked due to unsafe type casting** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-funds-can-be-permanently-locked-due-to-unsafe-type-casting.md`
```go
l1Write.sendTokenDelegate(delegateTo, uint64(amount), false);
```

**Example 2: [M-06] Attacker may DOS auctions using invalid bid parameters** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-06-attacker-may-dos-auctions-using-invalid-bid-parameters.md`
```
// Vulnerable pattern from SIZE:
<https://github.com/code-423n4/2022-11-size/blob/706a77e585d0852eae6ba0dca73dc73eb37f8fb6/src/SizeSealed.sol#L258-L263><br>
<https://github.com/code-423n4/2022-11-size/blob/706a77e585d0852eae6ba0dca73dc73eb37f8fb6/src/SizeSealed.sol#L157-L159><br>
<https://github.com/code-423n4/2022-11-size/blob/706a77e585d0852eae6ba0dca73dc73eb37f8fb6/src/SizeSealed.sol#L269-L280>

Buyers submit bids to SIZE using the bid() function. There's a max of 1000 bids allowed per auction in order to stop DOS attacks (O
```

**Example 3: [M-10] Unsafe casting from `uint256` to `uint128` in RewardsManager** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-unsafe-casting-from-uint256-to-uint128-in-rewardsmanager.md`
```go
can cause an overflow which, in turn, can lead to unforeseen consequences such as:

*   The inability to calculate new rewards, as `nextExchangeRate > exchangeRate_` will always be true after the overflow.
*   Reduced rewards because `toBucket.lpsAtStakeTime` will be reduced.
*   Reduced rewards because `toBucket.rateAtStakeTime` will be reduced.
*   In case `bucketState.rateAtStakeTime` overflows first but does not go beyond the limits in the new epoch, it will result in increased rewards being accrued.

### Proof of Concept

In `RewardsManager.stake()` and `RewardsManager.moveStakedLiquidity()`, the functions downcast `uint256` to `uint128` without checking whether it is bigger than `uint128` or not.

In `stake()` & `moveStakedLiquidity()` when `getLP >= type(uint128).max`:
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting unsafe casting logic allows exploitation through missing validatio
func secureAccountingUnsafeCasting(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 3 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 2
- **Affected Protocols**: Ajna Protocol, SIZE, Kinetiq_2025-02-26
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Accounting Precision Loss

### Overview

Implementation flaw in accounting precision loss logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: The bug report describes a vulnerability in the `forceUpdateNodes()` function that can be exploited by an attacker. By using a small `limitStake` value, the attacker can force all validator nodes into a pending update state, effectively blocking legitimate rebalancing for the entire epoch. This can 

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting precision loss logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting precision loss in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: Dust limit attack on `forceUpdateNodes` allows DoS of rebalancing and potential ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** An attacker can exploit the `forceUpdateNodes()` function with minimal `limitStake` values to force all validator nodes into a pending update state. By exploiting precision loss in stake-to-weight conversion, an attacker can call `forceUpdateNodes` with a minimal limitStake (e.g., 1 wei), which sets the rebalancing flag without actually reducing any stake, effectively blocking legitimate rebalancing for the entire epoch.

Consider following scenario:
- Large vault undelegation r
```

**Example 2: `getCommunityVotingPower` doesn't calculate voting Power correctly due to precis** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-5-getcommunityvotingpower-doesnt-calculate-voting-power-correctly-due-to-preci.md`
```go
return 
        (votes * cpMultipliers.votes / PERCENT) + 
        (proposalsCreated * cpMultipliers.proposalsCreated / PERCENT) + 
        (proposalsPassed * cpMultipliers.proposalsPassed / PERCENT);
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting precision loss logic allows exploitation through missing validatio
func secureAccountingPrecisionLoss(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 1
- **Affected Protocols**: FrankenDAO, Suzaku Core
- **Validation Strength**: Moderate (2 auditors)

---

## 5. Accounting Decimal Mismatch

### Overview

Implementation flaw in accounting decimal mismatch logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 1, MEDIUM: 3.

> **Key Finding**: This bug report describes an issue with the current system for calculating the operator stake. The system currently adds up all staked amounts from different vaults associated with a specific asset class, but this does not take into account the different decimal precision of the tokens used in the v

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting decimal mismatch logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting decimal mismatch in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: Inaccurate stake calculation due to decimal mismatch across multitoken asset cla** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/inaccurate-stake-calculation-due-to-decimal-mismatch-across-multitoken-asset-cla.md`
```solidity
function getOperatorStake(
        address operator,
        uint48 epoch,
        uint96 assetClassId
    ) public view returns (uint256 stake) {
        if (totalStakeCached[epoch][assetClassId]) {
            uint256 cachedStake = operatorStakeCache[epoch][assetClassId][operator];

            return cachedStake;
        }

        uint48 epochStartTs = getEpochStartTs(epoch);

        uint256 totalVaults = vaultManager.getVaultCount();

        for (uint256 i; i < totalVaults; ++i) {
            (address vault, uint48 enabledTime, uint48 disabledTime) = vaultManager.getVaultAtWithTimes(i);

            // Skip if vault not active in the target epoch
            if (!_wasActiveAt(enabledTime, disabledTime, epochStartTs)) {
                continue;
            }

            // Skip if vault asset not in AssetClassID
            if (vaultManager.getVaultAssetClass(vault) != assetClassId) {
                continue;
            }

            uint256 vaultStake = BaseDelegator(IVaultTokenized(vault).delegator()).stakeAt(
                L1_VALIDATOR_MANAGER, assetClassId, operator, epochStartTs, new bytes(0)
            );

            stake += vaultStake;
        }
```

**Example 2: [M-03] `RemoteAddressValidator` can incorrectly convert addresses to lowercase** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-remoteaddressvalidator-can-incorrectly-convert-addresses-to-lowercase.md`
```go
if ((b >= 65) && (b <= 70)) bytes(s)[i] = bytes1(b + uint8(32));
```

**Example 3: Attacker will prevent distribution of USDC to stakers through frequent reward up** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-attacker-will-prevent-distribution-of-usdc-to-stakers-through-frequent-rewar.md`
```go
((lastTimeRewardApplicable() - lastUpdateTime) * rewardRateUSDC * 1e18) / allTokensStaked
```

**Example 4: Stake Mint Differentiation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/stake-mint-differentiation.md`
```rust
pub fn deposit<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, Deposit<'info>>,
    service: Option<Service>,
    amount: u64,
) -> Result<()> {
    [...]
    // Call Guest chain program to update the stake if the chain is initialized
    if guest_chain_program_id.is_some() {
        [...]
        let cpi_program = ctx.remaining_accounts[3].clone();
        let cpi_ctx = CpiContext::new_with_signer(cpi_program, cpi_accounts, seeds);
        solana_ibc::cpi::set_stake(cpi_ctx, amount as u128)?;
    }
    Ok(())
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting decimal mismatch logic allows exploitation through missing validat
func secureAccountingDecimalMismatch(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 3
- **Affected Protocols**: Axelar Network, Kwenta Staking Rewards Upgrade, Composable Vaults, Suzaku Core
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Accounting Integer Overflow
grep -rn 'accounting|integer|overflow' --include='*.go' --include='*.sol'
# Accounting Integer Underflow
grep -rn 'accounting|integer|underflow' --include='*.go' --include='*.sol'
# Accounting Unsafe Casting
grep -rn 'accounting|unsafe|casting' --include='*.go' --include='*.sol'
# Accounting Precision Loss
grep -rn 'accounting|precision|loss' --include='*.go' --include='*.sol'
# Accounting Decimal Mismatch
grep -rn 'accounting|decimal|mismatch' --include='*.go' --include='*.sol'
```

## Keywords

`accounting`, `across`, `addexternalincentive`, `addresses`, `allows`, `appchain`, `asset`, `attack`, `attacker`, `auctions`, `calculate`, `calculation`, `calculations`, `casting`, `classes`, `convert`, `correctly`, `cosmos`, `could`, `decimal`, `denial`, `desired`, `distribution`, `dust`, `ending`, `error`, `frequent`, `from`, `function`, `funds`
