---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: staking
vulnerability_type: stake_deposit_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - incorrect_stake_amount
  - duplicate_stake_counting
  - stake_without_payment
  - deposit_front_running
  - deposit_validation_missing
  - stake_balance_desync
  - first_depositor_attack
  - deposit_queue_manipulation

# Impact Classification
severity: medium
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - staking
  - stake
  - deposit
  - staking
  - validator
  - amount
  - balance
  - tracking
  - accounting
  
language: go
version: all
---

## References
- [a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md](../../../../reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md)
- [account-inconsistencies-in-bridge-tokens-instruction.md](../../../../reports/cosmos_cometbft_findings/account-inconsistencies-in-bridge-tokens-instruction.md)
- [deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md](../../../../reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md)
- [direct-deposits-enable-theft-of-a-validators-funds.md](../../../../reports/cosmos_cometbft_findings/direct-deposits-enable-theft-of-a-validators-funds.md)
- [discrepancies-in-deposit-functionality.md](../../../../reports/cosmos_cometbft_findings/discrepancies-in-deposit-functionality.md)
- [discrepancy-in-deposit-functionality.md](../../../../reports/cosmos_cometbft_findings/discrepancy-in-deposit-functionality.md)
- [elected-tss-nodes-can-avoid-slashing-by-having-insuﬃcient-deposits.md](../../../../reports/cosmos_cometbft_findings/elected-tss-nodes-can-avoid-slashing-by-having-insuﬃcient-deposits.md)
- [h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md](../../../../reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md)
- [h-08-attacker-can-deploy-vaults-with-a-malicious-staking-contract.md](../../../../reports/cosmos_cometbft_findings/h-08-attacker-can-deploy-vaults-with-a-malicious-staking-contract.md)
- [h-1-amount_claimable_per_share-accounting-is-broken-and-will-result-in-vault-ins.md](../../../../reports/cosmos_cometbft_findings/h-1-amount_claimable_per_share-accounting-is-broken-and-will-result-in-vault-ins.md)
- [h-1-h-01-wsteth-eth-curve-lp-token-price-can-be-manipulated-to-cause-unexpected-.md](../../../../reports/cosmos_cometbft_findings/h-1-h-01-wsteth-eth-curve-lp-token-price-can-be-manipulated-to-cause-unexpected-.md)
- [h-1-malicious-observer-can-drain-solana-bridge-by-adding-failed-deposit-transact.md](../../../../reports/cosmos_cometbft_findings/h-1-malicious-observer-can-drain-solana-bridge-by-adding-failed-deposit-transact.md)
- [_getnextvalidatorsfromactiveoperators-can-be-tweaked-to-find-an-operator-with-a-.md](../../../../reports/cosmos_cometbft_findings/_getnextvalidatorsfromactiveoperators-can-be-tweaked-to-find-an-operator-with-a-.md)
- [incomplete-validation-of-the-babylon-deposit-can-lead-to-babylon-dismissing-the-.md](../../../../reports/cosmos_cometbft_findings/incomplete-validation-of-the-babylon-deposit-can-lead-to-babylon-dismissing-the-.md)
- [lack-of-upper-limit-checks-allows-blocking-withdrawals.md](../../../../reports/cosmos_cometbft_findings/lack-of-upper-limit-checks-allows-blocking-withdrawals.md)
- [m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md](../../../../reports/cosmos_cometbft_findings/m-01-a-staker-with-verified-over-commitment-can-potentially-bypass-slashing-comp.md)
- [m-02-_depositether-does-not-increment-validator-indexcausing-all-deposits-to-fun.md](../../../../reports/cosmos_cometbft_findings/m-02-_depositether-does-not-increment-validator-indexcausing-all-deposits-to-fun.md)
- [m-02-the-stake-fees-are-not-tracked-on-chain.md](../../../../reports/cosmos_cometbft_findings/m-02-the-stake-fees-are-not-tracked-on-chain.md)
- [m-04-processing-all-withdrawals-before-all-deposits-can-cause-some-deposit-to-no.md](../../../../reports/cosmos_cometbft_findings/m-04-processing-all-withdrawals-before-all-deposits-can-cause-some-deposit-to-no.md)
- [m-05-attacker-can-partially-dos-l1-operations-in-stakingmanager-by-making-huge-n.md](../../../../reports/cosmos_cometbft_findings/m-05-attacker-can-partially-dos-l1-operations-in-stakingmanager-by-making-huge-n.md)

## Vulnerability Title

**Stake Deposit and Amount Tracking Vulnerabilities**

### Overview

This entry documents 8 distinct vulnerability patterns extracted from 145 audit reports (68 HIGH, 77 MEDIUM severity) across 94 protocols by 18 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Deposit Validation Missing

**Frequency**: 50/145 reports | **Severity**: HIGH | **Validation**: Strong (14 auditors)
**Protocols affected**: Popcorn, Asymmetry Finance, Tortugal TIP, Vault-Tec, MANTRA

This bug report is about OperatorsRegistry.1.sol, a pool for operators. The current algorithm finds the first index in the cached operators array with the minimum value for A, and tries to gather as many publicKey s and signature s from this operator's validators up to a max of _requestedAmount . Ho

**Example 1.1** [MEDIUM] — Liquid Collective
Source: `_getnextvalidatorsfromactiveoperators-can-be-tweaked-to-find-an-operator-with-a-.md`
```solidity
// ❌ VULNERABLE: Deposit Validation Missing
uint256 selectedFunded = operators[selectedOperatorIndex].funded;
uint256 currentFunded = operators[idx].funded;
uint256 selectedNonStoppedFundedValidators = (
    selectedFunded -
    operators[selectedOperatorIndex].stopped
);
uint256 currerntNonStoppedFundedValidators = (
    currentFunded -
    operators[idx].stopped
);
bool equalNonStoppedFundedValidators = (
    currerntNonStoppedFundedValidators ==
    selectedNonStoppedFundedValidators
);
bool hasLessNonStoppedFundedValidators = (
    currerntNonStoppedFundedValidators <
    selectedNonStoppedFundedValidators
);
bool hasMoreAllowedNonFundedValidators = (
    operators[idx].limit - currentFunded >
    operators[selectedOperatorIndex].limit - selectedFunded
);
if (
    hasLessNonStoppedFundedValidators ||
    (
        equalNonStoppe
```

**Example 1.2** [MEDIUM] — Liquid Collective
Source: `_getnextvalidatorsfromactiveoperators-can-be-tweaked-to-find-an-operator-with-a-.md`
```solidity
// ❌ VULNERABLE: Deposit Validation Missing
function depositToConsensusLayer(
    uint256[] calldata operatorIndexes,
    uint256[] calldata validatorCounts
) external
```

#### Pattern 2: Incorrect Stake Amount

**Frequency**: 31/145 reports | **Severity**: HIGH | **Validation**: Strong (10 auditors)
**Protocols affected**: Allora, Yieldy, Berachain Beaconkit, Kelp, Composable Vaults

This bug report describes an issue with the accounting system in a software program. The program is incorrectly counting certain funds twice, which can lead to incorrect calculations and potentially give users more money than they should have. This issue has been fixed by the developers, but it is i

**Example 2.1** [HIGH] — Casimir
Source: `accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md`
```solidity
// ❌ VULNERABLE: Incorrect Stake Amount
// Before start
latestActiveBalanceAfterFee = 32 ETH
latestActiveRewards = 0

// startReport()
reportSweptBalance = 0 (rewards is in BeaconChain)

// syncValidators()
reportActiveBalance = 32.105 ETH

// finalizeReport()
rewards = 0.105 ETH
change = rewards - latestActiveRewards = 0.105 ETH
gainAfterFee = 0.1 ETH
=> rewardStakeRatioSum is increased
=> latestActiveBalanceAfterFee = 32.1

sweptRewards = 0
=> latestActiveRewards = 0.105
```

**Example 2.2** [HIGH] — Casimir
Source: `accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md`
```solidity
// ❌ VULNERABLE: Incorrect Stake Amount
// Before start
latestActiveBalanceAfterFee = 32.1 ETH
latestActiveRewards = 0.105

// startReport()
reportSweptBalance = 0.105 (rewards is in EigenPod)

// syncValidators()
reportActiveBalance = 32 ETH

// finalizeReport()
rewards = 0.105 ETH
change = rewards - latestActiveRewards = 0
=> No update to rewardStakeRatioSum and latestActiveBalanceAfterFee

sweptRewards = 0.105
=> latestActiveBalanceAfterFee = 32 ETH (subtracted sweptReward without fee)
=> latestActiveRewards = rewards - sweptRewards = 0
```

#### Pattern 3: Stake Without Payment

**Frequency**: 14/145 reports | **Severity**: MEDIUM | **Validation**: Strong (7 auditors)
**Protocols affected**: Covalent, Olas, Persistence, Tortugal TIP, Cosmos LSM

The Forta team has identified a bug in their staking system that allows malicious actors to avoid punishment intended by the slashes and freezes. This is due to the fact that when any one of the active proposals against a subject gets to the end of its lifecycle, be it rejected, dismissed, executed,

**Example 3.1** [HIGH] — Forta Delegated Staking
Source: `a-single-unfreeze-dismisses-all-other-slashing-proposal-freezes-fixed.md`
```solidity
// ❌ VULNERABLE: Stake Without Payment
function dismissSlashProposal(uint256 \_proposalId, string[] calldata \_evidence) external onlyRole(SLASHING\_ARBITER\_ROLE) {
    \_transition(\_proposalId, DISMISSED);
    \_submitEvidence(\_proposalId, DISMISSED, \_evidence);
    \_returnDeposit(\_proposalId);
    \_unfreeze(\_proposalId);
}
```

**Example 3.2** [HIGH] — Forta Delegated Staking
Source: `a-single-unfreeze-dismisses-all-other-slashing-proposal-freezes-fixed.md`
```solidity
// ❌ VULNERABLE: Stake Without Payment
function rejectSlashProposal(uint256 \_proposalId, string[] calldata \_evidence) external onlyRole(SLASHING\_ARBITER\_ROLE) {
    \_transition(\_proposalId, REJECTED);
    \_submitEvidence(\_proposalId, REJECTED, \_evidence);
    \_slashDeposit(\_proposalId);
    \_unfreeze(\_proposalId);
}
```

#### Pattern 4: Deposit Front Running

**Frequency**: 12/145 reports | **Severity**: MEDIUM | **Validation**: Strong (6 auditors)
**Protocols affected**: Rio Network, DIA, Persistence, Opyn Crab Netting, Lido

This bug report is about a problem with the `deposit` function in the `Prestaking` contract. There are two ways that someone could exploit this function to disrupt the staking system. One way is by making very small deposits (1 wei) which would make it difficult for others to use the system. The oth

**Example 4.1** [MEDIUM] — Lido
Source: `lid-5-deposit-call-data-not-included-in-guardian-signature.md`
```solidity
// ❌ VULNERABLE: Deposit Front Running
function depositBufferedEther(
    uint256 blockNumber,
    bytes32 blockHash,
    bytes32 depositRoot,
    uint256 stakingModuleId,
    uint256 nonce,
    bytes calldata depositCalldata,
    Signature[] calldata sortedGuardianSignatures
) external validStakingModuleId(stakingModuleId) {
    if (quorum == 0 || sortedGuardianSignatures.length < quorum) revert DepositNoQuorum();

    bytes32 onchainDepositRoot = IDepositContract(DEPOSIT_CONTRACT).get_deposit_root();
    if (depositRoot != onchainDepositRoot) revert DepositRootChanged();

    if (!STAKING_ROUTER.getStakingModuleIsActive(stakingModuleId)) revert DepositInactiveModule();

    uint256 lastDepositBlock = STAKING_ROUTER.getStakingModuleLastDepositBlock(stakingModuleId);
    if (block.number - lastDepositBlock < minDepositBlockDist
```

**Example 4.2** [MEDIUM] — Liquid Ron
Source: `m-01-user-can-earn-rewards-by-frontrunning-the-new-rewards-accumulation-in-ron-s.md`
```solidity
// ❌ VULNERABLE: Deposit Front Running
User -> delegate -> RonStaking -> Wait atleast a day -> New Rewards
```

#### Pattern 5: Deposit Queue Manipulation

**Frequency**: 11/145 reports | **Severity**: MEDIUM | **Validation**: Strong (5 auditors)
**Protocols affected**: Cabal, ZetaChain Cross-Chain, Pheasant Network, Renzo, Pods Finance Ethereum Volatility Vault Audit

The StrategyManager::slashQueuedWithdrawal() function contains an 'indicesToSkip' parameter to skip malicious strategies, as documented in the function definition. This parameter is supposed to allow owners to still slash queued withdrawals that contain a malicious strategy, while skipping the malic

**Example 5.1** [HIGH] — EigenLayer
Source: `h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md`
```solidity
// ❌ VULNERABLE: Deposit Queue Manipulation
// keeps track of the index in the `indicesToSkip` array
    uint256 indicesToSkipIndex = 0;

    uint256 strategiesLength = queuedWithdrawal.strategies.length;
    for (uint256 i = 0; i < strategiesLength;) {
        // check if the index i matches one of the indices specified in the `indicesToSkip` array
        if (indicesToSkipIndex < indicesToSkip.length && indicesToSkip[indicesToSkipIndex] == i) {
            unchecked {
                ++indicesToSkipIndex;
            }
        } else {
            if (queuedWithdrawal.strategies[i] == beaconChainETHStrategy){
                    //withdraw the beaconChainETH to the recipient
                _withdrawBeaconChainETH(queuedWithdrawal.depositor, recipient, queuedWithdrawal.shares[i]);
            } else {
                // tell the s
```

**Example 5.2** [HIGH] — EigenLayer
Source: `h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md`
```solidity
// ❌ VULNERABLE: Deposit Queue Manipulation
function testSlashQueuedWithdrawal_IgnoresIndicesToSkip() external {
        address recipient = address(this);
        uint256 depositAmount = 1e18;
        uint256 withdrawalAmount = depositAmount;
        bool undelegateIfPossible = false;

        // Deposit into strategy and queue a withdrawal
        (IStrategyManager.QueuedWithdrawal memory queuedWithdrawal,,) =
            testQueueWithdrawal_ToSelf_NotBeaconChainETH(depositAmount, withdrawalAmount, undelegateIfPossible);

        // Slash the delegatedOperator
        slasherMock.freezeOperator(queuedWithdrawal.delegatedAddress);

        // Keep track of the balance before the slash attempt
        uint256 balanceBefore = dummyToken.balanceOf(address(recipient));

        // Assert that the strategies array only has one element
 
```

#### Pattern 6: First Depositor Attack

**Frequency**: 10/145 reports | **Severity**: MEDIUM | **Validation**: Strong (7 auditors)
**Protocols affected**: Scroll, l2geth, Cosmos LSM, Increment, BadgerDAO, Coinflip_2025-02-19

This bug report discusses a problem with the staking protocol that can lead to overestimation of the staking balance. This occurs when a payout fails to transfer after a game is completed, causing the amount to be stored in a separate account. However, the protocol continues to include this amount i

**Example 6.1** [HIGH] — Coinflip_2025-02-19
Source: `c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md`
```solidity
// ❌ VULNERABLE: First Depositor Attack
function transferPayout(address token, address recipient, uint256 amount) external {
    --- SNIPPED ---
    if (!callSucceeded) {
@<>     pendingPayouts[token][recipient] += amount;
        emit TransferFailed(token, recipient, amount);
        return false;
    }
    --- SNIPPED ---
}
```

**Example 6.2** [MEDIUM] — Cosmos LSM
Source: `inconsistencies-in-slash-redelegation.md`
```solidity
// ❌ VULNERABLE: First Depositor Attack
> func (k Keeper) SlashRedelegation(ctx context.Context, srcValidator types.Validator,
> redelegation types.Redelegation,
> infractionHeight int64, slashFactor math.LegacyDec,
> ) (totalSlashAmount math.Int, err error) {
> [...]
> tokensToBurn, err := k.Unbond(ctx, delegatorAddress, valDstAddr, sharesToUnbond)
> if err != nil {
> return math.ZeroInt(), err
> }
> [...]
> }
>
```

#### Pattern 7: Duplicate Stake Counting

**Frequency**: 9/145 reports | **Severity**: MEDIUM | **Validation**: Strong (5 auditors)
**Protocols affected**: Cabal, UMA DVM 2.0 Audit, MilkyWay, Tokemak, Ethereum Credit Guild

This bug report concerns the `_updateAccountSlashingTrackers` function in the `VotingV2` contract. The function contains an optimization that marks unresolved requests in a prior round (rolled votes) as deleted via an entry in the `deletedRequests` map. This is intended to reduce gas consumption as 

**Example 7.1** [HIGH] — UMA DVM 2.0 Audit
Source: `duplicate-request-rewards.md`
```solidity
// ❌ VULNERABLE: Duplicate Stake Counting
deletedRequests[1] = 1
deletedRequests[2] = 2
```

**Example 7.2** [MEDIUM] — Cabal
Source: `m-01-reentrancy-check-in-lock_stakingreentry_check-causes-concurrent-init-deposi.md`
```solidity
// ❌ VULNERABLE: Duplicate Stake Counting
fun reentry_check(
    staking_account: &mut StakingAccount,
    with_update: bool
) {
    let (height, _) = block::get_block_info();
    assert!(staking_account.last_height != height, error::invalid_state(EREENTER));

    if (with_update) {
        staking_account.last_height = height;
    };
}
```

#### Pattern 8: Stake Balance Desync

**Frequency**: 8/145 reports | **Severity**: HIGH | **Validation**: Strong (5 auditors)
**Protocols affected**: Cabal, Geodefi, XPress, Karak-June, Nibiru

This bug report describes a problem where the value of `creditedNodeETH` is not being updated correctly when the `finishWithdraw()` function is called. This can lead to an incorrect balance for users and can also be exploited by malicious users to prevent balance updates. The report recommends updat

**Example 8.1** [HIGH] — Karak-June
Source: `h-01-user-can-prevent-balance-updates-by-withdrawing.md`
```solidity
// ❌ VULNERABLE: Stake Balance Desync
// Calculate unattributed node balance
        uint256 nodeBalanceWei = node.nodeAddress.balance - node.creditedNodeETH;
```

**Example 8.2** [HIGH] — Karak-June
Source: `h-02-broken-balance-update-if-a-slash-event-happens.md`
```solidity
// ❌ VULNERABLE: Stake Balance Desync
// Calculate unattributed node balance
        uint256 nodeBalanceWei = node.nodeAddress.balance - node.creditedNodeETH;
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 68 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 145
- HIGH severity: 68 (46%)
- MEDIUM severity: 77 (53%)
- Unique protocols affected: 94
- Independent audit firms: 18
- Patterns with 3+ auditor validation (Strong): 8

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

> `stake`, `deposit`, `staking`, `validator`, `amount`, `balance`, `tracking`, `accounting`, `minimum-stake`, `over-allocation`, `double-counting`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
