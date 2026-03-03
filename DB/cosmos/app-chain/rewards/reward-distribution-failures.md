---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: rewards
vulnerability_type: reward_distribution_failures

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - reward_stuck_contract
  - reward_distribution_dos
  - missing_reward_update
  - reward_after_removal
  - yield_distribution_error
  - incentive_misalignment
  - reward_escrow_error
  - reward_checkpoint_error

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - rewards
  - reward_distribution
  - stuck_rewards
  - distribution_failure
  - reward_loss
  - yield_distribution
  - incentive_misalignment
  - reward_escrow
  
language: go
version: all
---

## References
- [h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md](../../../../reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md)
- [front-running-redeem-can-prevent-indexers-from-receiving-rewards-for-allocations.md](../../../../reports/cosmos_cometbft_findings/front-running-redeem-can-prevent-indexers-from-receiving-rewards-for-allocations.md)
- [h-02-invalid-validation-in-_farmplots-function-allowing-a-malicious-user-repeate.md](../../../../reports/cosmos_cometbft_findings/h-02-invalid-validation-in-_farmplots-function-allowing-a-malicious-user-repeate.md)
- [h-06-bgt-stake-rewards-are-locked.md](../../../../reports/cosmos_cometbft_findings/h-06-bgt-stake-rewards-are-locked.md)
- [h-09-attackers-can-force-the-rewards-to-be-stuck-in-the-contract-with-malicious-.md](../../../../reports/cosmos_cometbft_findings/h-09-attackers-can-force-the-rewards-to-be-stuck-in-the-contract-with-malicious-.md)
- [h-1-non-functional-vote-if-there-is-one-bribe-rewarder-for-this-pool.md](../../../../reports/cosmos_cometbft_findings/h-1-non-functional-vote-if-there-is-one-bribe-rewarder-for-this-pool.md)
- [h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md](../../../../reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md)
- [h-03-incorrect-boost-management-leads-to-staking-reward-loss.md](../../../../reports/cosmos_cometbft_findings/h-03-incorrect-boost-management-leads-to-staking-reward-loss.md)
- [h-04-staking-rewards-can-be-drained.md](../../../../reports/cosmos_cometbft_findings/h-04-staking-rewards-can-be-drained.md)
- [h-10-missing-isepochclaimed-validation.md](../../../../reports/cosmos_cometbft_findings/h-10-missing-isepochclaimed-validation.md)
- [h-20-possibly-reentrancy-attacks-in-_distributeethrewardstouserfortoken-function.md](../../../../reports/cosmos_cometbft_findings/h-20-possibly-reentrancy-attacks-in-_distributeethrewardstouserfortoken-function.md)
- [immediate-stake-cache-updates-enable-reward-distribution-without-p-chain-confirm.md](../../../../reports/cosmos_cometbft_findings/immediate-stake-cache-updates-enable-reward-distribution-without-p-chain-confirm.md)
- [execution-failure-of-_updatereward-function-due-to-uninitialized-_rewarddistribu.md](../../../../reports/cosmos_cometbft_findings/execution-failure-of-_updatereward-function-due-to-uninitialized-_rewarddistribu.md)
- [m-01-vault-creator-can-prevent-users-from-claiming-staking-rewards.md](../../../../reports/cosmos_cometbft_findings/m-01-vault-creator-can-prevent-users-from-claiming-staking-rewards.md)
- [m-02-incorrect-updateglobalexchangerate-implementation.md](../../../../reports/cosmos_cometbft_findings/m-02-incorrect-updateglobalexchangerate-implementation.md)
- [m-1-division-by-zero-in-cvgrewards_distributecvgrewards-leads-to-locked-funds.md](../../../../reports/cosmos_cometbft_findings/m-1-division-by-zero-in-cvgrewards_distributecvgrewards-leads-to-locked-funds.md)
- [m-14-lockup-of-vestings-or-completion-time-can-be-bypassed-due-to-missing-check-.md](../../../../reports/cosmos_cometbft_findings/m-14-lockup-of-vestings-or-completion-time-can-be-bypassed-due-to-missing-check-.md)
- [m-9-claimfees-may-cause-some-external-rewards-to-be-locked-in-the-contract.md](../../../../reports/cosmos_cometbft_findings/m-9-claimfees-may-cause-some-external-rewards-to-be-locked-in-the-contract.md)
- [missing-tick-and-liquidity-checks-in-_decodeandreward-currentonlytrue-enables-fr.md](../../../../reports/cosmos_cometbft_findings/missing-tick-and-liquidity-checks-in-_decodeandreward-currentonlytrue-enables-fr.md)
- [m-05-changing-voteweighting-contract-can-result-in-lost-staking-incentives.md](../../../../reports/cosmos_cometbft_findings/m-05-changing-voteweighting-contract-can-result-in-lost-staking-incentives.md)

## Vulnerability Title

**Reward Distribution and Loss Vulnerabilities**

### Overview

This entry documents 5 distinct vulnerability patterns extracted from 20 audit reports (12 HIGH, 8 MEDIUM severity) across 18 protocols by 7 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Reward Stuck Contract

**Frequency**: 9/20 reports | **Severity**: MEDIUM | **Validation**: Strong (3 auditors)
**Protocols affected**: Covalent, Popcorn, Roots_2025-02-09, MANTRA, Olympusdao

This bug report discusses a vulnerability in the game economy of Munchables that allows for repeated farming and reward collection from a plot, even after the landlord has unlocked funds. This gives certain players an unfair advantage and disrupts the balance of the game. The proof of concept code s

**Example 1.1** [HIGH] — Munchables
Source: `h-02-invalid-validation-in-_farmplots-function-allowing-a-malicious-user-repeate.md`
```solidity
// ❌ VULNERABLE: Reward Stuck Contract
if (_getNumPlots(landlord) < _toiler.plotId) {
                timestamp = plotMetadata[landlord].lastUpdated;
                toilerState[tokenId].dirty = true;
            }
```

**Example 1.2** [HIGH] — Roots_2025-02-09
Source: `h-06-bgt-stake-rewards-are-locked.md`
```solidity
// ❌ VULNERABLE: Reward Stuck Contract
function _tryToBoost() internal {
            if (queued > 0 && blockDelta > 8191) {
            rewardCache.activateBoost(validator);
        }
```

#### Pattern 2: Missing Reward Update

**Frequency**: 4/20 reports | **Severity**: HIGH | **Validation**: Strong (3 auditors)
**Protocols affected**: Sorella Labs, Popcorn, Roots_2025-02-09, XDEFI

This bug report is about a reentrancy vulnerability in the _safeMint function of the XDEFIDistribution.sol contract. This function is called by the lock function which changes the totalDepositedXDEFI variable. Since the updateDistribution function does not have the noReenter modifier, an attacker ca

**Example 2.1** [HIGH] — XDEFI
Source: `h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md`
```solidity
// ❌ VULNERABLE: Missing Reward Update
function _safeMint(
    address to,
    uint256 tokenId,
    bytes memory _data
) internal virtual {
    _mint(to, tokenId);
    require(
        _checkOnERC721Received(address(0), to, tokenId, _data),
        "ERC721: transfer to non ERC721Receiver implementer"
    );
}
...
function _checkOnERC721Received(
    address from,
    address to,
    uint256 tokenId,
    bytes memory _data
) private returns (bool) {
    if (to.isContract()) {
        try IERC721Receiver(to).onERC721Received(_msgSender(), from, tokenId, _data) returns (bytes4 retval) {
            return retval == IERC721Receiver.onERC721Received.selector;
```

**Example 2.2** [HIGH] — XDEFI
Source: `h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md`
```solidity
// ❌ VULNERABLE: Missing Reward Update
function lock(uint256 amount_, uint256 duration_, address destination_) external noReenter returns (uint256 tokenId_) {
    // Lock the XDEFI in the contract.
    SafeERC20.safeTransferFrom(IERC20(XDEFI), msg.sender, address(this), amount_);

    // Handle the lock position creation and get the tokenId of the locked position.
    return _lock(amount_, duration_, destination_);
}
...
    function _lock(uint256 amount_, uint256 duration_, address destination_) internal returns (uint256 tokenId_) {
    // Prevent locking 0 amount in order generate many score-less NFTs, even if it is inefficient, and such NFTs would be ignored.
    require(amount_ != uint256(0) && amount_ <= MAX_TOTAL_XDEFI_SUPPLY, "INVALID_AMOUNT");

    // Get bonus multiplier and check that it is not zero (which validates t
```

#### Pattern 3: Reward Checkpoint Error

**Frequency**: 4/20 reports | **Severity**: HIGH | **Validation**: Moderate (2 auditors)
**Protocols affected**: Olas, Suzaku Core, Ajna Protocol, Stakehouse Protocol

A bug has been found in the Ajna codebase, which allows users to claim rewards even when they have already been claimed. This is due to the \_claimRewards function not validating if isEpochClaimed mapping is true. This function is used in the claimRewards and moveStakedLiquidity functions, but the l

**Example 3.1** [HIGH] — Suzaku Core
Source: `immediate-stake-cache-updates-enable-reward-distribution-without-p-chain-confirm.md`
```solidity
// ❌ VULNERABLE: Reward Checkpoint Error
// In initializeValidatorStakeUpdate():
function _initializeValidatorStakeUpdate(address operator, bytes32 validationID, uint256 newStake) internal {
    uint48 currentEpoch = getCurrentEpoch();

    nodeStakeCache[currentEpoch + 1][validationID] = newStake;
    nodePendingUpdate[validationID] = true;

    // @audit P-Chain operation initiated but NOT confirmed
    balancerValidatorManager.initializeValidatorWeightUpdate(validationID, scaledWeight);
}
```

**Example 3.2** [HIGH] — Suzaku Core
Source: `immediate-stake-cache-updates-enable-reward-distribution-without-p-chain-confirm.md`
```solidity
// ❌ VULNERABLE: Reward Checkpoint Error
function getOperatorUsedStakeCachedPerEpoch(uint48 epoch, address operator, uint96 assetClass) external view returns (uint256) {
    // Uses cached stake regardless of P-Chain confirmation status
    bytes32[] memory nodesArr = this.getActiveNodesForEpoch(operator, epoch);
    for (uint256 i = 0; i < nodesArr.length; i++) {
        bytes32 nodeId = nodesArr[i];
        bytes32 validationID = balancerValidatorManager.registeredValidators(abi.encodePacked(uint160(uint256(nodeId))));
        registeredStake += getEffectiveNodeStake(epoch, validationID); // @audit Uses unconfirmed stake
    }
```

#### Pattern 4: Reward Distribution Dos

**Frequency**: 2/20 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Qoda DAO, Virtuals Protocol

This bug report describes an issue with the `_updateReward` function in the `VeQoda` contract. This function is important and is used in other functions such as `stake`, `unstake`, and `_updateVeTokenCache`. However, the `_rewardDistributors` address set is not properly initialized, causing the func

**Example 4.1** [MEDIUM] — Qoda DAO
Source: `execution-failure-of-_updatereward-function-due-to-uninitialized-_rewarddistribu.md`
```solidity
// ❌ VULNERABLE: Reward Distribution Dos
function stake(address account, bytes32 method, uint256 amount) external {
        if (amount <= 0) {
            revert CustomErrors.ZeroStakeAmount();
        }

        // Calculate unclaimed reward before balance update
        _updateReward(account);
```

**Example 4.2** [MEDIUM] — Qoda DAO
Source: `execution-failure-of-_updatereward-function-due-to-uninitialized-_rewarddistribu.md`
```solidity
// ❌ VULNERABLE: Reward Distribution Dos
function unstake(bytes32 method, uint256 amount) external {
        if (amount <= 0) {
            revert CustomErrors.ZeroUnstakeAmount();
        }

        // User cannot over-unstake
        if (_userInfo[msg.sender][method].amount < amount) {
            revert CustomErrors.InsufficientBalance();
        }

        // Calculate unclaimed reward before balance update
        _updateReward(msg.sender);
```

#### Pattern 5: Reward Escrow Error

**Frequency**: 1/20 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: The Graph Timeline Aggregation Audit

The `redeem` function in `Escrow.sol` allows Indexers to receive query rewards by submitting a signed Receipt Aggregate Voucher (RAV) and `allocationIDProof`. However, anyone with knowledge of a valid `signedRAV` and `allocationIDProof` can call `redeem` and receive the rewards, regardless of whethe


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 12 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 20
- HIGH severity: 12 (60%)
- MEDIUM severity: 8 (40%)
- Unique protocols affected: 18
- Independent audit firms: 7
- Patterns with 3+ auditor validation (Strong): 2

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

> `reward-distribution`, `stuck-rewards`, `distribution-failure`, `reward-loss`, `yield-distribution`, `incentive-misalignment`, `reward-escrow`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
