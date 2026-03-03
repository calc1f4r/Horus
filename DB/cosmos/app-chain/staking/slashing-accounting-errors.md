---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: staking
vulnerability_type: slashing_accounting_errors

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - slash_amount_miscalculation
  - slash_share_dilution
  - over_slashing
  - under_slashing
  - slash_balance_update
  - slash_reward_interaction
  - slash_pending_operations
  - cumulative_slash_error

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - staking
  - slashing_calculation
  - over_slashing
  - under_slashing
  - slash_amount
  - share_dilution
  - penalty_calculation
  - slash_accounting
  
language: go
version: all
---

## References
- [erc-4337-call-to-_payprefund-may-lead-to-the-validator-stake-being-split.md](../../../../reports/cosmos_cometbft_findings/erc-4337-call-to-_payprefund-may-lead-to-the-validator-stake-being-split.md)
- [flawed-implementation-of-reward-score-calculation.md](../../../../reports/cosmos_cometbft_findings/flawed-implementation-of-reward-score-calculation.md)
- [funds-allocated-for-rewards-can-be-locked-in-the-contract.md](../../../../reports/cosmos_cometbft_findings/funds-allocated-for-rewards-can-be-locked-in-the-contract.md)
- [h-01-slashing-isnt-supported-in-the-rebasing-mechanism.md](../../../../reports/cosmos_cometbft_findings/h-01-slashing-isnt-supported-in-the-rebasing-mechanism.md)
- [h-02-validity-and-contests-bond-ca-be-incorrectly-burned-for-the-correct-and-ult.md](../../../../reports/cosmos_cometbft_findings/h-02-validity-and-contests-bond-ca-be-incorrectly-burned-for-the-correct-and-ult.md)
- [h-03-node-operator-is-getting-slashed-for-full-duration-even-though-rewards-are-.md](../../../../reports/cosmos_cometbft_findings/h-03-node-operator-is-getting-slashed-for-full-duration-even-though-rewards-are-.md)
- [the-exponential-decay-logic-slashes-stakers-principal-amount.md](../../../../reports/cosmos_cometbft_findings/the-exponential-decay-logic-slashes-stakers-principal-amount.md)
- [overpayment-to-bidder-in-slash-function-due-to-incorrect-amount-transfer.md](../../../../reports/cosmos_cometbft_findings/overpayment-to-bidder-in-slash-function-due-to-incorrect-amount-transfer.md)
- [wrong-maths-in-getnonslashrate.md](../../../../reports/cosmos_cometbft_findings/wrong-maths-in-getnonslashrate.md)
- [c-02-operator-can-still-claim-rewards-after-being-removed-from-governance.md](../../../../reports/cosmos_cometbft_findings/c-02-operator-can-still-claim-rewards-after-being-removed-from-governance.md)
- [h09-slash-process-can-be-bypassed.md](../../../../reports/cosmos_cometbft_findings/h09-slash-process-can-be-bypassed.md)
- [slashing-mechanism-grants-exponentially-more-rewards-than-expected.md](../../../../reports/cosmos_cometbft_findings/slashing-mechanism-grants-exponentially-more-rewards-than-expected.md)
- [_checkvalidatorbehavior-is-mistakenly-using-the-current-validator-balance.md](../../../../reports/cosmos_cometbft_findings/_checkvalidatorbehavior-is-mistakenly-using-the-current-validator-balance.md)
- [in-votekickpolicyonflag-targetstakeatriskweitarget-might-be-greater-than-stakedw.md](../../../../reports/cosmos_cometbft_findings/in-votekickpolicyonflag-targetstakeatriskweitarget-might-be-greater-than-stakedw.md)
- [m-06-_getrewardsamountpervault-might-be-using-an-outdated-vault-power.md](../../../../reports/cosmos_cometbft_findings/m-06-_getrewardsamountpervault-might-be-using-an-outdated-vault-power.md)
- [m-11-in-the-revertbatch-function-inchallenge-is-set-to-false-incorrectly-causing.md](../../../../reports/cosmos_cometbft_findings/m-11-in-the-revertbatch-function-inchallenge-is-set-to-false-incorrectly-causing.md)
- [m-12-bond-tokens-hlg-can-get-permanently-stuck-in-operator.md](../../../../reports/cosmos_cometbft_findings/m-12-bond-tokens-hlg-can-get-permanently-stuck-in-operator.md)
- [m-14-any-duration-can-be-passed-by-node-operator.md](../../../../reports/cosmos_cometbft_findings/m-14-any-duration-can-be-passed-by-node-operator.md)
- [m-16-deth-eth-lptokeneth-can-become-depegged-due-to-eth-20-reward-slashing.md](../../../../reports/cosmos_cometbft_findings/m-16-deth-eth-lptokeneth-can-become-depegged-due-to-eth-20-reward-slashing.md)
- [m-24-profitmanagers-creditmultiplier-calculation-does-not-count-undistributed-re.md](../../../../reports/cosmos_cometbft_findings/m-24-profitmanagers-creditmultiplier-calculation-does-not-count-undistributed-re.md)

## Vulnerability Title

**Slashing Accounting and Calculation Errors**

### Overview

This entry documents 8 distinct vulnerability patterns extracted from 50 audit reports (18 HIGH, 32 MEDIUM severity) across 41 protocols by 14 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Slash Reward Interaction

**Frequency**: 18/50 reports | **Severity**: MEDIUM | **Validation**: Strong (9 auditors)
**Protocols affected**: Streamr, Tanssi_2025-04-30, Taiko, Maia DAO Ecosystem, GoGoPool

The bug report discusses an issue with the `_checkValidatorBehavior()` function in the OracleManager.sol file. This function is responsible for checking the reasonableness of changes in the slashed amount and rewards amount. The problem arises when tolerance levels, represented as percentages of the

**Example 1.1** [MEDIUM] — Kinetiq LST
Source: `_checkvalidatorbehavior-is-mistakenly-using-the-current-validator-balance.md`
```solidity
// ❌ VULNERABLE: Slash Reward Interaction
slashingBps = (10 / 90) % > SlashingTolerance (10%).
```

**Example 1.2** [HIGH] — Switchboard On-chain
Source: `flawed-implementation-of-reward-score-calculation.md`
```solidity
// ❌ VULNERABLE: Slash Reward Interaction
pub fn calculate_slash(stats: &OracleStatsAccountData, reward: u64) -> u64 {
    let slash_score = stats.finalized_epoch.slash_score;
    if slash_score == 0 {
        return 0;
    }
    let reward_score = stats.finalized_epoch.reward_score;
    Decimal::from(reward)
        .saturating_mul(reward_score.into())
        .checked_div(slash_score.into())
        .unwrap()
        .to_u64()
        .unwrap_or(0)
}
```

#### Pattern 2: Over Slashing

**Frequency**: 15/50 reports | **Severity**: MEDIUM | **Validation**: Strong (6 auditors)
**Protocols affected**: Smoothly, Cabal, UMA DVM 2.0 Audit, Nexus_2024-11-29, ZetaChain

A bug has been identified in the `deleteOperators` method, which is used when operators must be slashed. This bug leaves the `operatorRewards` mapping untouched when an operator is removed, meaning they can still claim their accrued rewards, even if they are acting maliciously or are inactive. This 

**Example 2.1** [MEDIUM] — Liquid Collective
Source: `coverage-funds-might-be-pulled-not-only-for-the-purpose-of-covering-slashing-los.md`
```solidity
// ❌ VULNERABLE: Over Slashing
if (((_maxIncrease + previousValidatorTotalBalance) - executionLayerFees) > _validatorTotalBalance) {
    coverageFunds = _pullCoverageFunds(
        ((_maxIncrease + previousValidatorTotalBalance) - executionLayerFees) - _validatorTotalBalance
    );
}
```

**Example 2.2** [MEDIUM] — Liquid Collective
Source: `coverage-funds-might-be-pulled-not-only-for-the-purpose-of-covering-slashing-los.md`
```solidity
// ❌ VULNERABLE: Over Slashing
if (previousValidatorTotalBalance > _validatorTotalBalance + executionLayerFees) {
    coverageFunds = _pullCoverageFunds(
        ((_maxIncrease + previousValidatorTotalBalance) - executionLayerFees) - _validatorTotalBalance
    );
}
```

#### Pattern 3: Under Slashing

**Frequency**: 6/50 reports | **Severity**: MEDIUM | **Validation**: Strong (5 auditors)
**Protocols affected**: Lido, Brahma, Telcoin, Pods Finance Ethereum Volatility Vault Audit, Coinbase Liquid Staking Token Audit

This bug report is about a vulnerability in the HolographOperator.sol code on GitHub. The vulnerability occurs when the selected operator fails to complete the job, either intentionally or innocently, and the gas price has spiked and not gone down below the set gasPrice. In this situation, the bridg

**Example 3.1** [HIGH] — Brahma
Source: `trst-h-1-user-fee-token-balance-can-be-drained-in-a-single-operation-by-a-malici.md`
```solidity
// ❌ VULNERABLE: Under Slashing
if (feeToken == ETH) 
   {uint256 totalFee = (gasUsed + GAS_OVERHEAD_NATIVE) * tx.gasprice;
     totalFee = _applyMultiplier(totalFee);
       return (totalFee, recipient, TokenTransfer._nativeTransferExec(recipient, totalFee));
            } else {uint256 totalFee = (gasUsed + GAS_OVERHEAD_ERC20) * tx.gasprice;
      // Convert fee amount value in fee tokenuint256 feeToCollect =PriceFeedManager(_addressProvider.priceFeedManager()).getTokenXPriceInY(totalFee, ETH, feeToken);
  feeToCollect = _applyMultiplier(feeToCollect);
 return (feeToCollect, recipient, TokenTransfer._erc20TransferExec(feeToken, recipient, feeToCollect));}
```

#### Pattern 4: Slash Amount Miscalculation

**Frequency**: 5/50 reports | **Severity**: MEDIUM | **Validation**: Strong (5 auditors)
**Protocols affected**: Meta, Kinetiq_2025-02-26, Kinetiq LST, Primev, Holograph

This bug report describes a problem in the code of a smart contract that could cause permanent corruption. The problem occurs when the oracle reports a decrease in the amount of rewards or penalties for a validator. This is not accounted for in the code, so the validator manager's accounting becomes

**Example 4.1** [MEDIUM] — Kinetiq LST
Source: `any-decrease-in-slashed-or-rewarded-amounts-reported-will-make-validatormanager-.md`
```solidity
// ❌ VULNERABLE: Slash Amount Miscalculation
// ValidatorManager.sol#L469-L503

/// @notice Report a reward event for a validator
/// @param validator Address of the validator to be rewarded
/// @param amount Amount of rewards for the validator
function reportRewardEvent(address validator, uint256 amount) external onlyRole(ORACLE_ROLE) validatorActive(validator) {
    require(amount > 0, "Invalid reward amount");
    // Update reward amounts
    totalRewards += amount; // @audit has to follow Oracle updates
    validatorRewards[validator] += amount;
    emit RewardEventReported(validator, amount);
}

/* ========== SLASHING ========== */

/// @notice Report a slashing event for a validator
/// @param validator Address of the validator to be slashed
/// @param amount Amount to slash from the validator
function reportSlashingEvent(addre
```

**Example 4.2** [MEDIUM] — Kinetiq_2025-02-26
Source: `m-06-improper-execution-order-in-generateperformance.md`
```solidity
// ❌ VULNERABLE: Slash Amount Miscalculation
function generatePerformance() external whenNotPaused onlyRole(OPERATOR_ROLE) returns (bool) {
        if (
            !_checkValidatorBehavior(
                validator, previousSlashing, previousRewards, avgSlashAmount, avgRewardAmount, avgBalance
            )
        ) {
            validatorManager.deactivateValidator(validator);
            continue;
        }

        if (avgSlashAmount > previousSlashing) {
            uint256 newSlashAmount = avgSlashAmount - previousSlashing;
            validatorManager.reportSlashingEvent(validator, newSlashAmount);
        }

        if (avgRewardAmount > previousRewards) {
            uint256 newRewardAmount = avgRewardAmount - previousRewards;
            validatorManager.reportRewardEvent(validator, newRewardAmount);
        }

        va
```

#### Pattern 5: Cumulative Slash Error

**Frequency**: 2/50 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Dria, Kakeru Contracts

The `execute_bond` function in the **basset\_inj\_hub** contract has an issue where the **stinj** exchange rate is not updated correctly. This is because the `update_stinj_exchange_rate` function is only called when the bond type is `BondType::BondRewards`, instead of `BondType::StInj`. The recommen

#### Pattern 6: Slash Balance Update

**Frequency**: 2/50 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Kinetiq_2025-02-26, Mantle Network

The report discusses a bug in the code where the function `OracleManager::generatePerformance` is supposed to update the stats of every validator and their total balance. However, if there are any rewards or slashing amounts, the code will revert if the new slashing amount is greater than the valida

**Example 6.1** [HIGH] — Kinetiq_2025-02-26
Source: `h-04-reportslashingevent-reverts-if-outdated-balance-is-below-slashing-amount.md`
```solidity
// ❌ VULNERABLE: Slash Balance Update
function generatePerformance() external whenNotPaused onlyRole(OPERATOR_ROLE) returns (bool) {
        // ..

        // Update validators with averaged values
        for (uint256 i = 0; i < validatorCount; i++) {
            // ...

            // Handle slashing
            if (avgSlashAmount > previousSlashing) {
                uint256 newSlashAmount = avgSlashAmount - previousSlashing;
@>                validatorManager.reportSlashingEvent(validator, newSlashAmount);
            }

            // ...
        }

        // ...

        return true;
    }
```

**Example 6.2** [HIGH] — Kinetiq_2025-02-26
Source: `h-04-reportslashingevent-reverts-if-outdated-balance-is-below-slashing-amount.md`
```solidity
// ❌ VULNERABLE: Slash Balance Update
function reportSlashingEvent(address validator, uint256 amount)
       // ...
    {
        require(amount > 0, "Invalid slash amount");

        Validator storage val = _validators[_validatorIndexes.get(validator)];
@>        require(val.balance >= amount, "Insufficient stake for slashing");

        // Update balances
        unchecked {
            // These operations cannot overflow:
            // - val.balance >= amount (checked above)
            // - totalBalance >= val.balance (invariant maintained by the contract)
            val.balance -= amount;
            totalBalance -= amount;
        }

       // ...
    }
```

#### Pattern 7: Slash Pending Operations

**Frequency**: 1/50 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Karak

This bug report describes a problem with the `NativeVault` function in the `Core` contract. When an operator creates a `NativeVault`, they can set the `slashStore` address to be different from the `assetSlashingHandlers` address for ETH. This causes the `slashAssets()` function to always revert, mak

**Example 7.1** [HIGH] — Karak
Source: `h-02-the-operator-can-create-a-nativevault-that-can-be-silently-unslashable.md`
```solidity
// ❌ VULNERABLE: Slash Pending Operations
for (uint256 i = 0; i < queuedSlashing.vaults.length; i++) {
        IKarakBaseVault(queuedSlashing.vaults[i]).slashAssets(
            queuedSlashing.earmarkedStakes[i],
            self.assetSlashingHandlers[IKarakBaseVault(queuedSlashing.vaults[i]).asset()]
        );
    }
```

**Example 7.2** [HIGH] — Karak
Source: `h-02-the-operator-can-create-a-nativevault-that-can-be-silently-unslashable.md`
```solidity
// ❌ VULNERABLE: Slash Pending Operations
if (slashingHandler != self.slashStore) revert NotSlashStore();
```

#### Pattern 8: Slash Share Dilution

**Frequency**: 1/50 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Jito Restaking

This bug report discusses a vulnerability in a vault system where the underlying tokens have been completely slashed, resulting in a balance of zero deposited tokens but still having outstanding VRT tokens in circulation. This can lead to an unfair outcome for new depositors as the current implement

**Example 8.1** [HIGH] — Jito Restaking
Source: `slashing-induced-share-dilution.md`
```solidity
// ❌ VULNERABLE: Slash Share Dilution
if self.tokens_deposited() == 0 {
```

**Example 8.2** [HIGH] — Jito Restaking
Source: `slashing-induced-share-dilution.md`
```solidity
// ❌ VULNERABLE: Slash Share Dilution
/// Calculate the amount of VRT tokens to mint based on the amount of tokens deposited in the vault.
/// If no tokens have been deposited, the amount is equal to the amount passed in.
/// Otherwise, the amount is calculated as the pro-rata share of the total VRT supply.
pub fn calculate_vrt_mint_amount(&self, amount: u64) -> Result<u64, VaultError> {
    if self.tokens_deposited() == 0 {
        return Ok(amount);
    }
    amount
        .checked_mul(self.vrt_supply())
        .and_then(|x| x.checked_div(self.tokens_deposited()))
        .ok_or(VaultError::VaultOverflow)
}
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 18 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 50
- HIGH severity: 18 (36%)
- MEDIUM severity: 32 (64%)
- Unique protocols affected: 41
- Independent audit firms: 14
- Patterns with 3+ auditor validation (Strong): 4

### Detection Patterns

#### Code Patterns to Look For
```
- Missing balance update before/after token transfers
- Unchecked return values from staking/delegation operations
- State reads without freshness validation
- Arithmetic operations without overflow/precision checks
- Missing access control on state-modifying functions
- Linear iterations over unbounded collections
- Race condition windows in multi-step operations
```

#### Audit Checklist
- [ ] Verify all staking state transitions update balances atomically
- [ ] Check that slashing affects all relevant state (pending, queued, active)
- [ ] Ensure withdrawal requests cannot bypass cooldown periods
- [ ] Validate that reward calculations handle all edge cases (zero stake, partial periods)
- [ ] Confirm access control on all administrative and state-modifying functions
- [ ] Test for frontrunning vectors in all two-step operations
- [ ] Verify iteration bounds on all loops processing user-controlled data
- [ ] Check cross-module state consistency after complex operations

### Keywords for Search

> `slashing-calculation`, `over-slashing`, `under-slashing`, `slash-amount`, `share-dilution`, `penalty-calculation`, `slash-accounting`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
