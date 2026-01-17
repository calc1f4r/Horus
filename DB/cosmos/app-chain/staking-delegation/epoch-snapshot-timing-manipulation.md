---
# Core Classification (Required)
protocol: generic
chain: everychain
category: staking
vulnerability_type: epoch_timing_manipulation

# Attack Vector Details (Required)
attack_type: timing_attack|economic_exploit|frontrunning
affected_component: epoch_accounting|snapshot_logic|reward_calculation

# Technical Primitives (Required)
primitives:
  - epoch_transition
  - snapshot_timing
  - stake_caching
  - reward_calculation
  - supply_snapshot
  - balance_checkpoint
  - same_block_attack
  - future_epoch_caching
  - double_counting
  - state_desynchronization

# Impact Classification (Required)
severity: medium_to_high
impact: reward_theft|fund_loss|accounting_corruption
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - staking
  - epoch
  - snapshot
  - reward_distribution
  - timing_attack
  - frontrunning
  - defi
  - liquid_staking
  
language: solidity|move|go|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Epoch/Snapshot Timing Manipulation Reports
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Suzaku - Future Epoch Cache Manipulation | `reports/cosmos_cometbft_findings/future-epoch-cache-manipulation-via-calcandcachestakes-allows-reward-manipulatio.md` | HIGH | Cyfrin |
| Cabal - Supply Snapshot Desynchronization | `reports/cosmos_cometbft_findings/m-03-attacker-can-desynchronize-supply-snapshot-during-same-block-unstake-reduci.md` | MEDIUM | Code4rena |
| Suzaku - Stake Over-Allocation | `reports/cosmos_cometbft_findings/operator-can-over-allocate-the-same-stake-to-unlimited-nodes-within-one-epoch-ca.md` | MEDIUM | Cyfrin |
| Karak - Snapshot Prevention via Validator Creation | `reports/cosmos_cometbft_findings/m-04-preventing-balance-updates-by-adding-a-new-validator-in-the-current-block.md` | MEDIUM | Pashov Audit Group |
| Casimir - Double Accounting in Reward Ratio | `reports/cosmos_cometbft_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md` | HIGH | Cyfrin |
| Elixir - Orphaned Rewards Captured by First Staker | `reports/cosmos_cometbft_findings/m-02-orphaned-rewards-captured-by-first-staker.md` | MEDIUM | Pashov Audit Group |
| Zivoe - Flashloan Yield Distribution Manipulation | `reports/cosmos_cometbft_findings/m-11-zivoeydldistributeyield-yield-distribution-is-flash-loan-manipulatable.md` | MEDIUM | Sherlock |
| Celo - Slash Frontrunning to Avoid Penalty | `reports/cosmos_cometbft_findings/m03-users-can-avoid-some-slashing-penalties-by-front-running.md` | MEDIUM | Trail of Bits |
| Ajna - Snapshot Average Loan Frontrunning | `reports/cosmos_cometbft_findings/m-10-adversary-can-grief-kicker-by-frontrunning-kickauction-call-with-a-large-am.md` | MEDIUM | Sherlock |

---

# Epoch/Snapshot Timing and Reward Manipulation Vulnerabilities

**A Comprehensive Pattern-Matching Guide for Staking Protocol Epoch Timing and Reward Calculation Audits**

---

## Table of Contents

1. [Overview](#overview)
2. [Vulnerability Description](#vulnerability-description)
3. [Vulnerable Pattern Examples](#vulnerable-pattern-examples)
4. [Impact Analysis](#impact-analysis)
5. [Secure Implementation](#secure-implementation)
6. [Detection Patterns](#detection-patterns)
7. [Real-World Examples](#real-world-examples)
8. [Prevention Guidelines](#prevention-guidelines)

---

## Overview

Epoch/Snapshot Timing Manipulation vulnerabilities occur in staking protocols when the timing boundaries of epochs, snapshots, or reward calculation periods are not properly enforced, allowing attackers to exploit race conditions, same-block attacks, future epoch caching, or state desynchronization to inflate their reward shares, double-count stakes, or corrupt accounting. These vulnerabilities are particularly prevalent in liquid staking, delegation, and validator management systems where epoch-based accounting determines reward distribution.

---

## Vulnerability Description

### Root Cause

The fundamental issues arise from:

1. **Missing Epoch Validation**: Functions that cache or calculate stake values don't validate that the epoch is not in the future, allowing attackers to lock in current stake values for epochs that haven't occurred yet
2. **Same-Block State Desynchronization**: When snapshot and burn/transfer operations occur in the same block, supply snapshots record pre-operation values while balance lookups return post-operation values
3. **Stake Not Locked on Node Creation**: Operators can create unlimited validators in a single epoch without locking their stake, causing weight inflation and reward theft
4. **Double-Counting Unclaimed Rewards**: Delayed balances or rewards that haven't been claimed are re-counted in subsequent reports, inflating reward ratios
5. **Orphaned Reward Capture**: First staker after an empty period captures all accumulated rewards at 1:1 ratio
6. **Snapshot Blocking via Timing Attacks**: Creating validators or modifying state in the same block as snapshot creation can prevent finalization

### Root Cause Statement Formula

> "This vulnerability exists because [EPOCH/SNAPSHOT TIMING BOUNDARY] is not validated in [STAKE CACHING/REWARD CALCULATION COMPONENT] allowing [TIMING MANIPULATION/SAME-BLOCK ATTACK] leading to [REWARD THEFT/ACCOUNTING CORRUPTION]."

### Attack Scenario Categories

#### Scenario 1: Future Epoch Cache Manipulation
1. Attacker observes current high stake value
2. Attacker calls `calcAndCacheStakes()` for a future epoch (e.g., epoch 5 while currently in epoch 1)
3. Current stake values are cached for the future epoch
4. Attacker withdraws stake before the future epoch arrives
5. When epoch 5 arrives, attacker still receives rewards based on cached (higher) stake values
6. Other participants are diluted despite attacker no longer having stake

#### Scenario 2: Same-Block Supply Desynchronization
1. Manager submits `snapshot()` transaction to record total supply at block H
2. Attacker monitors mempool and submits `unstake()` to execute in same block H
3. Supply snapshot records pre-burn value S₀
4. Attacker's burn reduces live supply, but snapshot is not updated
5. Balance lookup falls back to live (post-burn) balance
6. Reward calculation uses `post_burn_balance / pre_burn_supply`
7. Sum of all reward shares < 100%, reducing everyone's rewards
8. Missing rewards remain stranded in pool

#### Scenario 3: Unlimited Node Registration
1. Operator has 1000 ETH staked
2. Operator calls `addNode()` to register first validator with 1000 ETH weight
3. `operatorLockedStake` is NOT incremented after node creation
4. Operator calls `addNode()` again - sees full 1000 ETH as "available"
5. Operator creates 10 validators, each with 1000 ETH weight
6. Reward calculation uses 10,000 ETH weight for operator who only staked 1000 ETH
7. Operator captures 10x their fair share of epoch rewards

#### Scenario 4: Double-Counting Delayed Rewards
1. Validator earns 0.105 ETH in beacon chain rewards
2. Report processes: rewards counted in `rewardStakeRatioSum`
3. Rewards swept to EigenPod but not yet claimed
4. Next report starts: `reportSweptBalance` counts same 0.105 ETH again
5. `rewardStakeRatioSum` increased twice for same rewards
6. Users can withdraw more ETH than actually exists

#### Scenario 5: Orphaned Rewards Capture
1. Protocol has zero stakers (all unstaked)
2. 100 tokens distributed as rewards via `transfer_in_rewards()`
3. No check that stakers exist - rewards accepted
4. Alice stakes 1000 tokens - gets 1000 shares (1:1 ratio)
5. Vesting completes - Alice's 1000 shares now represent 1100 tokens
6. Alice redeems for 100 token profit (stolen community rewards)

---

## Vulnerable Pattern Examples

**Example 1: Missing Future Epoch Validation** [Approx Severity: HIGH]
```solidity
// ❌ VULNERABLE: No validation that epoch is not in the future
function calcAndCacheStakes(uint48 epoch, uint96 assetClassId) public returns (uint256 totalStake) {
    uint48 epochStartTs = getEpochStartTs(epoch); // No epoch timing validation!
    
    // Caches current stake values for ANY epoch, including future ones
    address[] memory operators = getOperatorList();
    for (uint256 i = 0; i < operators.length; i++) {
        uint256 stake = vault.getOperatorStakeAt(operators[i], epochStartTs);
        operatorStakeCache[epoch][assetClassId][operators[i]] = stake;
        totalStake += stake;
    }
    
    totalStakeCached[epoch][assetClassId] = true; // Locks in stale values for future epoch
    return totalStake;
}

// Subsequent calls return cached (potentially stale) values
function getOperatorStake(address operator, uint48 epoch, uint96 assetClassId) 
    public view returns (uint256 stake) 
{
    if (totalStakeCached[epoch][assetClassId]) {
        return operatorStakeCache[epoch][assetClassId][operator]; // Returns cached value
    }
    // ...
}
```

**Example 2: Same-Block Supply Snapshot Desynchronization** [Approx Severity: MEDIUM]
```move
// ❌ VULNERABLE: burn() doesn't update supply snapshot for current block
public fun burn(burn_cap: &BurnCapability, fa: FungibleAsset) acquires ManagingRefs, HolderStore {
    let metadata = burn_cap.metadata;
    let refs = borrow_global<ManagingRefs>(object::object_address(&metadata));
    
    // Burn reduces the LIVE supply
    fungible_asset::burn(&refs.burn_ref, fa);
    
    // ❌ MISSING: No check if current block is snapshot block
    // ❌ MISSING: No update to supply_snapshots table for current block
    // The recorded supply for this block remains the stale, pre-burn value
}

// Balance lookup skips writing for same-block operations
fun check_snapshot(c_balance: &mut CabalBalance, current_snapshot_block: u64) {
    let current_block_height = block::get_current_block_height();
    
    // ❌ VULNERABLE: Same-block condition prevents balance recording
    if (current_block_height == current_snapshot_block) {
        return; // Early return - no balance written for this block!
    }
    
    // This path never reached for same-block unstakes
    table::add(&mut c_balance.snapshot, key, c_balance.balance);
}

// Fallback returns LIVE (post-burn) balance instead of snapshot value
fun get_snapshot_balance_internal(cabal_balance: &CabalBalance, block_height: u64): u64 {
    let iter = table::iter(&cabal_balance.snapshot, option::some(key), option::none(), 2);
    
    if (!table::prepare<vector<u8>, u64>(iter)) {
        // ❌ Fallback: returns live balance (post-burn) when no snapshot entry
        return cabal_balance.balance;
    }
    // ...
}
```

**Example 3: Stake Not Locked on Node Creation** [Approx Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: operatorLockedStake not incremented after node registration
function addNode(
    bytes32 nodeId,
    bytes calldata blsKey,
    uint256 stakeAmount
) external {
    address operator = msg.sender;
    
    // Check available stake
    uint256 available = _getOperatorAvailableStake(operator);
    require(available >= stakeAmount, "Insufficient available stake");
    
    // Register the node with stake weight
    _registerNode(nodeId, blsKey, operator, stakeAmount);
    
    // ❌ MISSING: operatorLockedStake[operator] += stakeAmount;
    // Next call to addNode() will see SAME available stake!
}

function _getOperatorAvailableStake(address operator) internal view returns (uint256) {
    uint256 totalStake = getOperatorStake(operator, getCurrentEpoch());
    uint256 lockedStake = operatorLockedStake[operator]; // Never increased!
    
    if (totalStake <= lockedStake) {
        return 0;
    }
    return totalStake - lockedStake; // Returns full stake every time
}
```

**Example 4: Double-Counting Unclaimed Rewards** [Approx Severity: HIGH]
```solidity
// ❌ VULNERABLE: Delayed funds counted multiple times in reports
function startReport() external {
    // Counts all funds in EigenPod as "swept" balance
    reportSweptBalance = eigenPod.balance(); // Includes unclaimed rewards!
}

function finalizeReport() external {
    uint256 rewards = reportActiveBalance - latestActiveBalance;
    
    // If previous rewards still in EigenPod (unclaimed), they're counted again
    if (reportSweptBalance > 0) {
        // ❌ Same rewards counted in rewardStakeRatioSum TWICE:
        // 1. First report: counted as active rewards
        // 2. Second report: counted again as swept balance
        rewardStakeRatioSum += calculateRatio(rewards);
    }
    
    // No tracking of whether these rewards were already counted
}
```

**Example 5: Orphaned Rewards to First Staker** [Approx Severity: MEDIUM]
```move
// ❌ VULNERABLE: No check for active stakers before distributing rewards
public fun transfer_in_rewards(amount: u64, clock: &Clock) acquires Management {
    let management = borrow_global_mut<Management>(@sdeusd);
    
    // ❌ MISSING: assert!(total_supply(management) > 0, ENoActiveStakers);
    // Rewards accepted even when no stakers exist
    update_vesting_amount(management, amount, clock);
}

// First staker gets 1:1 ratio regardless of accumulated rewards
public fun convert_to_shares(assets: u64): u64 acquires Management {
    let management = borrow_global<Management>(@sdeusd);
    let total_supply = total_supply(management);
    let total_assets = total_assets(management);
    
    if (total_supply == 0 || total_assets == 0) {
        // ❌ First staker gets 1:1 even if unvested rewards exist
        return assets;
    }
    
    return (assets * total_supply) / total_assets;
}
```

**Example 6: Validator Creation Blocks Snapshot** [Approx Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: Validator creation timestamp equals snapshot timestamp
function validateWithdrawalCredentials(bytes32 validatorId) external {
    ValidatorDetails storage details = validators[validatorId];
    
    // Sets timestamp to current block
    details.lastBalanceUpdateTimestamp = block.timestamp;
    
    // If called in same block as startSnapshot(), this blocks finalization
    node.remainingProofs++;
}

function startSnapshot() external {
    node.currentSnapshotTimestamp = block.timestamp;
    node.remainingProofs = getValidatorCount();
}

function validateSnapshotProofs(bytes32 validatorId) external {
    ValidatorDetails storage details = validators[validatorId];
    
    // ❌ If validator created same block as snapshot, this reverts
    if (details.lastBalanceUpdateTimestamp >= node.currentSnapshotTimestamp) {
        revert ValidatorAlreadyProved(); // Can never prove this validator!
    }
    
    // Snapshot never finalizes because remainingProofs never reaches 0
    node.remainingProofs--;
}
```

**Example 7: Checkpoint Protection Bypass for Slashing** [Approx Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: Same-block stake update blocks slashing
modifier checkpointProtection(address account) {
    uint256 numCheckpoints = _stakes[account]._checkpoints.length;
    require(
        numCheckpoints == 0 || 
        _stakes[account]._checkpoints[numCheckpoints - 1]._blockNumber != block.number,
        "Cannot exit in the same block as another stake"
    );
    _;
}

function slash(address account, uint256 amount) external onlySlasher checkpointProtection(account) {
    // ❌ If attacker frontruns with stake(1), this reverts
    // Checkpoint was updated in same block, modifier fails
    _claimAndExit(account, amount);
}

function stake(uint256 amount) external {
    // Attacker calls stake(1) before slash() in same block
    _stakes[msg.sender]._checkpoints.push(Checkpoint({
        _blockNumber: block.number, // Updates checkpoint to current block
        _value: getCurrentStake(msg.sender) + amount
    }));
}
```

---

## Impact Analysis

### Technical Impact

| Impact Category | Description | Severity |
|-----------------|-------------|----------|
| **Reward Inflation** | Attackers capture disproportionate share of epoch rewards | HIGH |
| **Accounting Corruption** | Sum of balances ≠ total supply invariant broken | HIGH |
| **Double Counting** | Same funds counted multiple times in reward calculations | HIGH |
| **Snapshot DoS** | Balance updates permanently blocked via timing attacks | MEDIUM |
| **Stake Weight Inflation** | Operator weight exceeds actual stake, diluting others | MEDIUM |
| **Orphaned Fund Theft** | Community rewards captured by first staker after empty period | MEDIUM |

### Business Impact

- **Direct Fund Loss**: Attackers extract rewards meant for honest stakers (8/9 reports)
- **Protocol Insolvency Risk**: Users can withdraw more than protocol holds (2/9 reports)
- **Trust Degradation**: Unfair reward distribution damages protocol reputation
- **Griefing Vector**: Attackers can reduce everyone's rewards without direct profit (3/9 reports)
- **Governance Bypass**: Slashing can be avoided via timing attacks (2/9 reports)

### Affected Scenarios

1. **Epoch Transitions**: Critical window where state is being cached/calculated
2. **Validator Registration**: Node creation during active epoch
3. **Reward Distribution Events**: Snapshot timing around distribution calls
4. **Unstaking Operations**: Burns that affect supply snapshots
5. **Slashing Events**: Checkpoint-based protections can be exploited
6. **Empty Pool Periods**: First depositor after zero-staker period

---

## Secure Implementation

**Fix 1: Epoch Validation for Cache Operations**
```solidity
// ✅ SECURE: Validates epoch is not in the future
function calcAndCacheStakes(uint48 epoch, uint96 assetClassId) public returns (uint256 totalStake) {
    uint48 currentEpoch = getCurrentEpoch();
    require(epoch <= currentEpoch, "Cannot cache future epochs"); // Added validation
    
    // Also prevent re-caching if already cached
    require(!totalStakeCached[epoch][assetClassId], "Already cached");
    
    uint48 epochStartTs = getEpochStartTs(epoch);
    // ... rest of caching logic
}
```

**Fix 2: Same-Block Supply Snapshot Update**
```move
// ✅ SECURE: Updates supply snapshot on burn if it's the snapshot block
public fun burn(burn_cap: &BurnCapability, fa: FungibleAsset) acquires ManagingRefs, HolderStore, ModuleStore {
    let metadata = burn_cap.metadata;
    let refs = borrow_global<ManagingRefs>(object::object_address(&metadata));
    
    // Burn reduces the LIVE supply
    fungible_asset::burn(&refs.burn_ref, fa);
    
    // ✅ Check if current block is snapshot block and update
    let current_block = block::get_current_block_height();
    let module_store = borrow_global_mut<ModuleStore>(@module_addr);
    
    if (current_block == module_store.current_snapshot_block) {
        // Update the supply snapshot to reflect the burn
        let new_supply = fungible_asset::supply(metadata);
        table::upsert(&mut module_store.supply_snapshots, current_block, new_supply);
    }
}
```

**Fix 3: Lock Stake on Node Creation**
```solidity
// ✅ SECURE: Locks stake immediately when node is created
function addNode(
    bytes32 nodeId,
    bytes calldata blsKey,
    uint256 stakeAmount
) external {
    address operator = msg.sender;
    
    uint256 available = _getOperatorAvailableStake(operator);
    require(available >= stakeAmount, "Insufficient available stake");
    
    _registerNode(nodeId, blsKey, operator, stakeAmount);
    
    // ✅ Lock the stake immediately
    operatorLockedStake[operator] += stakeAmount;
    
    emit StakeLocked(operator, stakeAmount);
}
```

**Fix 4: Track Claimed vs Unclaimed Rewards**
```solidity
// ✅ SECURE: Prevents double-counting of unclaimed rewards
function startReport() external {
    // Track only NEW swept balance, not total
    uint256 currentPodBalance = eigenPod.balance();
    reportSweptBalance = currentPodBalance - previouslyTrackedSweptBalance;
    previouslyTrackedSweptBalance = currentPodBalance;
}

function finalizeReport() external {
    uint256 rewards = reportActiveBalance - latestActiveBalance;
    
    // Only count new rewards, not previously tracked ones
    uint256 newRewards = calculateNewRewards(rewards, reportSweptBalance);
    rewardStakeRatioSum += calculateRatio(newRewards);
    
    // Mark these rewards as tracked
    trackedRewards += newRewards;
}
```

**Fix 5: Require Active Stakers for Reward Distribution**
```move
// ✅ SECURE: Prevents reward distribution when no stakers exist
public fun transfer_in_rewards(amount: u64, clock: &Clock) acquires Management {
    let management = borrow_global_mut<Management>(@sdeusd);
    
    // ✅ Require active stakers before accepting rewards
    assert!(total_supply(management) > 0, error::invalid_state(ENoActiveStakers));
    
    update_vesting_amount(management, amount, clock);
}
```

**Fix 6: Prevent Same-Block Validator Creation for Snapshots**
```solidity
// ✅ SECURE: Prevents validator creation in same block as snapshot
function validateWithdrawalCredentials(bytes32 validatorId) external {
    ValidatorDetails storage details = validators[validatorId];
    
    // ✅ Prevent creation if snapshot is active in this block
    require(
        node.currentSnapshotTimestamp != block.timestamp,
        "Cannot create validator during snapshot"
    );
    
    details.lastBalanceUpdateTimestamp = block.timestamp;
    node.remainingProofs++;
}
```

**Fix 7: Separate Checkpoint Protection from Slashing**
```solidity
// ✅ SECURE: Slashing bypasses checkpoint protection
function slash(address account, uint256 amount) external onlySlasher {
    // ✅ No checkpoint protection for slashing - always allowed
    // Slashing must execute regardless of same-block stakes
    _forceClaimAndExit(account, amount);
}

function stake(uint256 amount) external checkpointProtection(msg.sender) {
    // Checkpoint protection only on voluntary actions
    _addStake(msg.sender, amount);
}
```

---

## Detection Patterns

### Code Patterns to Look For

```
Pattern 1: Cache/snapshot functions without epoch/block validation
- calcAndCacheStakes(), snapshot(), checkpoint() without time checks
- getEpochStartTs(epoch) called without epoch <= currentEpoch validation

Pattern 2: Same-block early returns in balance/supply snapshots
- if (current_block == snapshot_block) return;
- Missing snapshot update in burn/transfer functions

Pattern 3: Missing stake locking after node/validator creation
- addNode(), registerValidator() without incrementing lockedStake
- getAvailableStake() that doesn't account for pending registrations

Pattern 4: Balance lookups with fallback to live state
- if (!snapshot_exists) return live_balance;
- Table/mapping lookups that fall through to current values

Pattern 5: Reward distribution without staker existence check
- transfer_in_rewards() without total_supply > 0 assertion
- distributeRewards() that accepts funds to empty pools

Pattern 6: Checkpoint-based protection applied to slashing
- checkpointProtection modifier on slash() function
- Same-block checks that can be triggered by attacker
```

### Audit Checklist

- [ ] **Epoch Validation**: All epoch-based cache operations validate epoch <= currentEpoch
- [ ] **Same-Block Handling**: Snapshot and burn/transfer operations update snapshots atomically
- [ ] **Stake Locking**: Node creation immediately locks the corresponding stake amount
- [ ] **Double-Count Prevention**: Delayed/unclaimed rewards tracked separately and not re-counted
- [ ] **Empty Pool Protection**: Reward distribution requires active stakers
- [ ] **Snapshot Finalization**: Validator creation can't block snapshot completion
- [ ] **Slashing Independence**: Slashing bypasses checkpoint-based protections
- [ ] **Balance Fallback**: Live balance fallback doesn't cause state desynchronization
- [ ] **Epoch Transition Atomicity**: Critical state changes are atomic across epoch boundaries
- [ ] **Cache Immutability**: Once cached, epoch data cannot be manipulated

---

## Real-World Examples

### Affected Protocols

| Protocol | Vulnerability | Severity | Audit Firm | Year |
|----------|---------------|----------|------------|------|
| Suzaku Core | Future epoch cache manipulation | HIGH | Cyfrin | 2025 |
| Cabal | Supply snapshot desynchronization | MEDIUM | Code4rena | 2025 |
| Suzaku Core | Stake over-allocation | MEDIUM | Cyfrin | 2025 |
| Karak | Snapshot blocking via validator creation | MEDIUM | Pashov | 2024 |
| Casimir | Double-counting delayed rewards | HIGH | Cyfrin | 2024 |
| Elixir | Orphaned rewards first staker capture | MEDIUM | Pashov | 2025 |
| Zivoe | Flashloan yield distribution manipulation | MEDIUM | Sherlock | 2024 |
| Celo | Slash frontrunning via locked gold | MEDIUM | Trail of Bits | 2023 |
| Ajna | Snapshot average frontrunning | MEDIUM | Sherlock | 2023 |

### Attack Patterns Observed

1. **Future Epoch Caching**: Lock in favorable stake values for future reward calculations
2. **Same-Block Mempool Monitoring**: Submit unstake in same block as manager's snapshot
3. **Unlimited Validator Registration**: Create multiple validators without stake locking
4. **Report Timing Exploitation**: Start new reports before claiming delayed rewards
5. **First Staker Timing**: Stake immediately after empty period to capture orphaned rewards

---

## Prevention Guidelines

### Development Best Practices

1. **Epoch Boundary Enforcement**: Always validate `epoch <= currentEpoch` before caching
2. **Atomic State Updates**: Update all related state (supply, balances, caches) atomically
3. **Immediate Stake Locking**: Lock stake the moment a validator/node is registered
4. **Claimed Reward Tracking**: Maintain separate accounting for claimed vs unclaimed rewards
5. **Staker Existence Checks**: Require `totalSupply > 0` before accepting reward distributions
6. **Slashing Independence**: Slashing logic should bypass user-triggerable protections

### Testing Requirements

**Unit Tests**:
- Test epoch caching with future epochs (should revert)
- Test same-block snapshot and burn operations (should update snapshot)
- Test multiple node registrations in same epoch (should lock stake cumulatively)
- Test reward distribution to empty pool (should revert)

**Integration Tests**:
- Simulate mempool monitoring attack scenarios
- Test epoch transitions with pending operations
- Verify reward distribution across multiple epochs with varying stake

**Fuzz Testing Targets**:
- Epoch parameters in cache functions
- Block timing around snapshot operations
- Multiple node registrations per operator per epoch
- Reward distribution timing relative to staker exits

---

## References

### Related Vulnerabilities

- [Slashing Evasion and Bypass](./slashing-evasion-bypass.md) - Compounds with epoch timing for slashing avoidance
- [Staking State Management](./staking-state-management.md) - Related state synchronization issues

### Technical Documentation

- [Cosmos SDK Epoch Module](https://docs.cosmos.network/main/modules/epochs)
- [EIP-4626 Share Accounting](https://eips.ethereum.org/EIPS/eip-4626)
- [Snapshot-Based Reward Distribution Patterns](https://www.paradigm.xyz/2021/02/merkle-distributor)

---

## Keywords for Search

`epoch`, `snapshot`, `timing_attack`, `same_block`, `future_epoch`, `cache_manipulation`, `reward_theft`, `double_counting`, `stake_inflation`, `weight_inflation`, `supply_desynchronization`, `balance_checkpoint`, `orphaned_rewards`, `first_staker`, `epoch_transition`, `validator_registration`, `stake_locking`, `reward_calculation`, `frontrunning_snapshot`, `mempool_monitoring`, `checkpoint_protection`, `slashing_bypass`, `accounting_corruption`, `reward_ratio`, `epoch_caching`, `stake_caching`, `totalStakeCached`, `operatorStakeCache`, `calcAndCacheStakes`, `rewardStakeRatioSum`, `supply_snapshots`, `transfer_in_rewards`, `convert_to_shares`, `validateSnapshotProofs`

---

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-01-XX | Variant Analysis | Initial creation from 9 audit reports |
