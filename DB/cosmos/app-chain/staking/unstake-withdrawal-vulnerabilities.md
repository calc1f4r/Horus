---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: staking
vulnerability_type: unstake_withdrawal_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - unstake_bypass_cooldown
  - withdrawal_dos
  - withdrawal_amount_error
  - withdrawal_queue_manipulation
  - incomplete_withdrawal
  - withdrawal_replay
  - withdrawal_during_slash
  - emergency_withdrawal_abuse

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - staking
  - unstake
  - withdrawal
  - cooldown
  - delay
  - queue
  - exit
  - unbonding
  - unstaking_period
  
language: go
version: all
---

## References
- [h-01-buffer-silently-locks-staked-hype-in-contract-without-using-them-for-withdr.md](../../../../reports/cosmos_cometbft_findings/h-01-buffer-silently-locks-staked-hype-in-contract-without-using-them-for-withdr.md)
- [h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md](../../../../reports/cosmos_cometbft_findings/h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md)
- [staking-indexer-does-not-handle-one-transaction-spending-an-expired-unbonding-an.md](../../../../reports/cosmos_cometbft_findings/staking-indexer-does-not-handle-one-transaction-spending-an-expired-unbonding-an.md)
- [a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md](../../../../reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md)
- [h-06-minipoolmanager-node-operator-can-avoid-being-slashed.md](../../../../reports/cosmos_cometbft_findings/h-06-minipoolmanager-node-operator-can-avoid-being-slashed.md)
- [relayer-can-use-valid-evidence-of-one-trade-to-avoid-getting-slashed-for-another.md](../../../../reports/cosmos_cometbft_findings/relayer-can-use-valid-evidence-of-one-trade-to-avoid-getting-slashed-for-another.md)
- [unchecked-balance-change-could-lead-to-unfair-withdrawals.md](../../../../reports/cosmos_cometbft_findings/unchecked-balance-change-could-lead-to-unfair-withdrawals.md)
- [assignment-of-incorrect-reward-escrow.md](../../../../reports/cosmos_cometbft_findings/assignment-of-incorrect-reward-escrow.md)
- [h-13-a-payment-made-towards-multiple-liens-causes-the-borrower-to-lose-funds-to-.md](../../../../reports/cosmos_cometbft_findings/h-13-a-payment-made-towards-multiple-liens-causes-the-borrower-to-lose-funds-to-.md)
- [c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md](../../../../reports/cosmos_cometbft_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md)
- [h-01-_addrebalancerequest-may-use-outdated-balance-for-delegate-withdrawal-reque.md](../../../../reports/cosmos_cometbft_findings/h-01-_addrebalancerequest-may-use-outdated-balance-for-delegate-withdrawal-reque.md)
- [h-02-validatormanager-missing-fund-withdrawal-from-validator-in-deactivatevalida.md](../../../../reports/cosmos_cometbft_findings/h-02-validatormanager-missing-fund-withdrawal-from-validator-in-deactivatevalida.md)
- [_checkbalance-returns-an-incorrect-value-during-insolvency.md](../../../../reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md)
- [activation-of-queued-cutting-board-can-be-manipulated-leading-to-redirection-of-.md](../../../../reports/cosmos_cometbft_findings/activation-of-queued-cutting-board-can-be-manipulated-leading-to-redirection-of-.md)
- [validators-array-length-has-to-be-updated-when-the-validator-is-alienated.md](../../../../reports/cosmos_cometbft_findings/validators-array-length-has-to-be-updated-when-the-validator-is-alienated.md)
- [admin-balances-dont-account-for-potential-token-rebases.md](../../../../reports/cosmos_cometbft_findings/admin-balances-dont-account-for-potential-token-rebases.md)
- [fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md](../../../../reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md)
- [fund-distribution-may-not-incentivize-users-to-participate.md](../../../../reports/cosmos_cometbft_findings/fund-distribution-may-not-incentivize-users-to-participate.md)
- [m-03-frxeth-can-be-depegged-due-to-eth-staking-balance-slashing.md](../../../../reports/cosmos_cometbft_findings/m-03-frxeth-can-be-depegged-due-to-eth-staking-balance-slashing.md)
- [m-03-in-a-mass-slashing-event-node-operators-are-incentivized-to-get-slashed.md](../../../../reports/cosmos_cometbft_findings/m-03-in-a-mass-slashing-event-node-operators-are-incentivized-to-get-slashed.md)

## Vulnerability Title

**Unstaking and Withdrawal Processing Vulnerabilities**

### Overview

This entry documents 7 distinct vulnerability patterns extracted from 99 audit reports (33 HIGH, 66 MEDIUM severity) across 65 protocols by 19 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Withdrawal Dos

**Frequency**: 40/99 reports | **Severity**: MEDIUM | **Validation**: Strong (12 auditors)
**Protocols affected**: Asymmetry Finance, Stader Labs, Puffer Finance, Andromeda – Validator Staking ADO and Vesting ADO, ZetaChain Cross-Chain

This bug report discusses an issue with the DelegationManager contract that results in incorrect calculations of burnable shares during operator slashing events. The `_addQueuedSlashableShares()` function excludes `beaconChainETHStrategy` from cumulative scaled shares tracking, which leads to underc

**Example 1.1** [MEDIUM] — EigenLayer
Source: `beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
```solidity
// ❌ VULNERABLE: Withdrawal Dos
/// @dev Add to the cumulative withdrawn scaled shares from an operator for a given strategy
function _addQueuedSlashableShares(address operator, IStrategy strategy, uint256 scaledShares) internal {
    // @audit beaconChainETHStrategy is excluded from slashable shares tracking
    if (strategy != beaconChainETHStrategy) {
        uint256 currCumulativeScaledShares = _cumulativeScaledSharesHistory[operator][strategy].latest();
        _cumulativeScaledSharesHistory[operator][strategy].push({
            key: uint32(block.number),
            value: currCumulativeScaledShares + scaledShares
        });
    }
}
```

**Example 1.2** [MEDIUM] — EigenLayer
Source: `beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
```solidity
// ❌ VULNERABLE: Withdrawal Dos
// We want ALL shares added to the withdrawal queue in the window [block.number - MIN_WITHDRAWAL_DELAY_BLOCKS, block.number]
//
// To get this, we take the current shares in the withdrawal queue and subtract the number of shares
// that were in the queue before MIN_WITHDRAWAL_DELAY_BLOCKS.
uint256 curQueuedScaledShares = _cumulativeScaledSharesHistory[operator][strategy].latest();
uint256 prevQueuedScaledShares = _cumulativeScaledSharesHistory[operator][strategy].upperLookup({
    key: uint32(block.number) - MIN_WITHDRAWAL_DELAY_BLOCKS - 1
});
// The difference between these values is the number of scaled shares that entered the withdrawal queue
// less than or equal to MIN_WITHDRAWAL_DELAY_BLOCKS ago. These shares are still slashable.
uint256 scaledSharesAdded = curQueuedScaledShares - pr
```

#### Pattern 2: Withdrawal During Slash

**Frequency**: 19/99 reports | **Severity**: MEDIUM | **Validation**: Strong (10 auditors)
**Protocols affected**: Rio Network, Obol, Meta, Streamr, Curve Finance

The team has fixed a previous issue, but a new issue still exists. The `bondWithdrawal` function can only track one type of token, but the `BondManager` can support multiple tokens. This can lead to unexpected behavior in the `withdraw()` function. The team has made a second round of fixes by adding

**Example 2.1** [HIGH] — GoGoPool
Source: `h-06-minipoolmanager-node-operator-can-avoid-being-slashed.md`
```solidity
// ❌ VULNERABLE: Withdrawal During Slash
// No rewards means validation period failed, must slash node ops GGP.
if (avaxTotalRewardAmt == 0) {
    slash(minipoolIndex);
}
```

**Example 2.2** [HIGH] — GoGoPool
Source: `h-06-minipoolmanager-node-operator-can-avoid-being-slashed.md`
```solidity
// ❌ VULNERABLE: Withdrawal During Slash
uint256 avaxLiquidStakerAmt = getUint(keccak256(abi.encodePacked("minipool.item", index, ".avaxLiquidStakerAmt")));
uint256 expectedAVAXRewardsAmt = getExpectedAVAXRewardsAmt(duration, avaxLiquidStakerAmt);
uint256 slashGGPAmt = calculateGGPSlashAmt(expectedAVAXRewardsAmt);
```

#### Pattern 3: Withdrawal Amount Error

**Frequency**: 19/99 reports | **Severity**: MEDIUM | **Validation**: Strong (9 auditors)
**Protocols affected**: Rocket Pool Atlas (v1.2), Astaria, Radiant Riz Audit, Napier, Radiant Capital

The report discusses an issue with the `shutdown` function in the `RizLendingPool` contract. This function takes a snapshot of prices and calculates a ratio for slashing remaining users in the market. However, the owner of the `BadDebtManager` contract can modify this snapshot data without any restr

**Example 3.1** [HIGH] — Skale Token
Source: `gas-limit-for-bounty-and-slashing-distribution-addressed.md`
```solidity
// ❌ VULNERABLE: Withdrawal Amount Error
for (uint i = 0; i < shares.length; ++i) {
    skaleToken.send(address(skaleBalances), shares[i].amount, abi.encode(shares[i].holder));

    uint created = delegationController.getDelegation(shares[i].delegationId).created;
    uint delegationStarted = timeHelpers.getNextMonthStartFromDate(created);
    skaleBalances.lockBounty(shares[i].holder, timeHelpers.addMonths(delegationStarted, 3));
}
```

**Example 3.2** [HIGH] — Skale Token
Source: `gas-limit-for-bounty-and-slashing-distribution-addressed.md`
```solidity
// ❌ VULNERABLE: Withdrawal Amount Error
function slash(uint validatorId, uint amount) external allow("SkaleDKG") {
    ValidatorService validatorService = ValidatorService(contractManager.getContract("ValidatorService"));
    require(validatorService.validatorExists(validatorId), "Validator does not exist");

    Distributor distributor = Distributor(contractManager.getContract("Distributor"));
    TokenState tokenState = TokenState(contractManager.getContract("TokenState"));

    Distributor.Share[] memory shares = distributor.distributePenalties(validatorId, amount);
    for (uint i = 0; i < shares.length; ++i) {
        tokenState.slash(shares[i].delegationId, shares[i].amount);
    }
}
```

#### Pattern 4: Unstake Bypass Cooldown

**Frequency**: 8/99 reports | **Severity**: MEDIUM | **Validation**: Strong (6 auditors)
**Protocols affected**: Sapien - 2, Covalent, Increment, Ante Protocol, Onchainheroes Fishingvoyages

The client has marked a bug as "Fixed" and provided an explanation for the fix. The bug was related to the staking contract, which determines the multiplier a user gets based on staking amount and lockup period. However, the contract did not check if the lockup period had actually elapsed before all

**Example 4.1** [HIGH] — Covalent
Source: `h-02-unstake-should-update-exchange-rates-first.md`
```solidity
// ❌ VULNERABLE: Unstake Bypass Cooldown
// @audit shares are computed here with old rate
uint128 validatorSharesRemove = tokensToShares(amount, v.exchangeRate);
require(validatorSharesRemove > 0, "Unstake amount is too small");

if (v.disabledEpoch == 0) {
    // @audit rates are updated here
    updateGlobalExchangeRate();
    updateValidator(v);
    // ...
}
```

**Example 4.2** [MEDIUM] — Ante Protocol
Source: `looping-over-an-array-of-unbounded-size-can-cause-a-denial-of-service.md`
```solidity
// ❌ VULNERABLE: Unstake Bypass Cooldown
function _calculateChallengerEligibility() internal {
    uint256 cutoffBlock = failedBlock.sub(CHALLENGER_BLOCK_DELAY);
    for (uint256 i = 0; i < challengers.addresses.length; i++) {
        address challenger = challengers.addresses[i];
        if (eligibilityInfo.lastStakedBlock[challenger] < cutoffBlock) {
            eligibilityInfo.eligibleAmount = eligibilityInfo.eligibleAmount.add(
                _storedBalance(challengerInfo.userInfo[challenger], challengerInfo)
            );
        }
    }
}
```

#### Pattern 5: Withdrawal Queue Manipulation

**Frequency**: 6/99 reports | **Severity**: MEDIUM | **Validation**: Strong (5 auditors)
**Protocols affected**: Babylonchain, OETH Withdrawal Queue Audit, Berachain Pol, Kinetiq, Geode Liquid Staking

The `_checkBalance` function in the OETHVaultCore.sol contract is not returning the correct balance in certain scenarios. Specifically, if the WETH in the withdrawal queue exceeds the total amount of workable assets, the function should return a balance of 0 but instead returns the amount of WETH in

**Example 5.1** [HIGH] — Kinetiq
Source: `h-01-buffer-silently-locks-staked-hype-in-contract-without-using-them-for-withdr.md`
```solidity
// ❌ VULNERABLE: Withdrawal Queue Manipulation
if (operationType == OperationType.UserWithdrawal) {
            // Buffer handling uses 18 decimal precision
            uint256 currentBuffer = hypeBuffer;
            uint256 amountFromBuffer = Math.min(amount, currentBuffer);

            if (amountFromBuffer > 0) {
                hypeBuffer = currentBuffer - amountFromBuffer;
                amount -= amountFromBuffer;
                emit BufferDecreased(amountFromBuffer, hypeBuffer);
            }

            // If fully fulfilled from buffer, return
            if (amount == 0) {
                return;
            }
        }
```

**Example 5.2** [HIGH] — Kinetiq
Source: `h-01-buffer-silently-locks-staked-hype-in-contract-without-using-them-for-withdr.md`
```solidity
// ❌ VULNERABLE: Withdrawal Queue Manipulation
function cancelWithdrawal(address user, uint256 withdrawalId) external onlyRole(MANAGER_ROLE) whenNotPaused {
        WithdrawalRequest storage request = _withdrawalRequests[user][withdrawalId];
        require(request.hypeAmount > 0, "No such withdrawal request");

        uint256 hypeAmount = request.hypeAmount;
        uint256 kHYPEAmount = request.kHYPEAmount;
        uint256 kHYPEFee = request.kHYPEFee;

        // Check kHYPE balances
        require(kHYPE.balanceOf(address(this)) >= kHYPEAmount + kHYPEFee, "Insufficient kHYPE balance");

        // Clear the withdrawal request
        delete _withdrawalRequests[user][withdrawalId];
        totalQueuedWithdrawals -= hypeAmount;

        // Return kHYPE tokens to user (including fees)
        kHYPE.transfer(user, kHYPEAmount + kHYPEFe
```

#### Pattern 6: Incomplete Withdrawal

**Frequency**: 6/99 reports | **Severity**: MEDIUM | **Validation**: Strong (5 auditors)
**Protocols affected**: Astaria, Cabal, Radiant Riz Audit, Bemo Finance, Switchboard On-chain

The vulnerability in the maybe_execute_stake_rewards function in OracleHeartbeat arises from incorrect utilization of the remaining_accounts.oracle_switch_reward_escrow account for distributing rewards. This results in the oracle's WSOL reward escrow failing to set up properly and no funds being tra

**Example 6.1** [HIGH] — Switchboard On-chain
Source: `assignment-of-incorrect-reward-escrow.md`
```solidity
// ❌ VULNERABLE: Incomplete Withdrawal
pub fn maybe_execute_stake_rewards(
    [...]
) -> Result<()> {
    [...]
    if let Some(oracle_wsol_reward_escrow) = &remaining_accounts.oracle_switch_reward_escrow {
        let res = NativeEscrow::spl_transfer(
            &ctx.accounts.token_program,
            &ctx.accounts.queue_escrow.to_account_info(),
            &oracle_wsol_reward_escrow.to_account_info(),
            &ctx.accounts.program_state.to_account_info(),
            &[&[STATE_SEED, &[state.bump]]],
            std::cmp::min(
                reward.saturating_sub(slash),
                oracle_wsol_reward_escrow.amount,
            ),
        );
        [...]
    }
}
```

**Example 6.2** [MEDIUM] — Cabal
Source: `m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md`
```solidity
// ❌ VULNERABLE: Incomplete Withdrawal
// Simplified logic from process_xinit_unstake
    entry fun process_xinit_unstake(account: &signer, staker_addr: address, unstaking_type: u64, unstake_amount: u64) acquires ModuleStore, CabalStore, LockExempt {
        // ... permission checks, reward compounding ...
        let m_store = borrow_global_mut<ModuleStore>(@staking_addr);
        let x_init_amount = m_store.staked_amounts[unstaking_type];

        // --- VULNERABILITY ---
        // 'unstake_amount' is the original amount burned (== total supply in this case).
        // 'sx_init_amount' reads the supply *after* the burn in initiate_unstake, so it's 0.
        let sx_init_amount = option::extract(&mut fungible_asset::supply(m_store.cabal_stake_token_metadata[unstaking_type])); // Returns 0

        // This attempts bigdecimal
```

#### Pattern 7: Withdrawal Replay

**Frequency**: 1/99 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: EigenLayer

Summary:

The calculation for the beacon chain slashing factor in the EigenPodManager contract is not accounting for existing operator slashing and deposit scaling factors, resulting in an edge case where stakers can withdraw more funds than they should after being slashed. The recommended solution 

**Example 7.1** [HIGH] — EigenLayer
Source: `incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md`
```solidity
// ❌ VULNERABLE: Withdrawal Replay
finalWithdrawableShares = depositShares × dsf × slashingFactor
                        = depositShares × dsf × (maxMagnitude × bcsf)
                        = 32 × 1 × (0.5 × 0.5)
                        = 8
```

**Example 7.2** [HIGH] — EigenLayer
Source: `incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md`
```solidity
// ❌ VULNERABLE: Withdrawal Replay
EigenPodManager.sol::_reduceSlashingFactor()
prevRestakedBalanceWei = prevRestakedBalanceWei.mulWad(maxMagnitude).mulWad(dsf);
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 33 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 99
- HIGH severity: 33 (33%)
- MEDIUM severity: 66 (66%)
- Unique protocols affected: 65
- Independent audit firms: 19
- Patterns with 3+ auditor validation (Strong): 6

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

> `unstake`, `withdrawal`, `cooldown`, `delay`, `queue`, `exit`, `unbonding`, `unstaking-period`, `withdrawal-request`, `force-exit`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
