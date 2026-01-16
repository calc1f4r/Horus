---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: staking
vulnerability_type: state_inconsistency

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - EndBlocker
  - RemoveStakes
  - UnbondingTime
  - Redelegation
  - ValidatorBond
  - LiquidShares
  - precompile

# Impact Classification
severity: medium_to_high
impact: fund_loss
exploitability: 0.5
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - staking
  - delegation
  - unbonding
  - slashing
  - precompile
  - state_sync
  
language: go
version: all
---

## References
- [h-7-removestakes-and-removedelegatestakes-silently-handle-errors-in-endblocker.md](../../../reports/cosmos_cometbft_findings/h-7-removestakes-and-removedelegatestakes-silently-handle-errors-in-endblocker.md)
- [m-12-changes-of-the-unbondingtime-are-not-accounted-for.md](../../../reports/cosmos_cometbft_findings/m-12-changes-of-the-unbondingtime-are-not-accounted-for.md)
- [inconsistencies-in-slash-redelegation.md](../../../reports/cosmos_cometbft_findings/inconsistencies-in-slash-redelegation.md)
- [m-20-claiming-delegation-rewards-via-the-precompile-can-result-in-a-loss-of-zeta.md](../../../reports/cosmos_cometbft_findings/m-20-claiming-delegation-rewards-via-the-precompile-can-result-in-a-loss-of-zeta.md)
- [delegators-can-redelegate-stakes-to-jailed-delegatee.md](../../../reports/cosmos_cometbft_findings/delegators-can-redelegate-stakes-to-jailed-delegatee.md)

## Vulnerability Title

**Staking State Management and Synchronization Vulnerabilities**

### Overview

Cosmos SDK appchains implementing custom staking logic frequently contain state management vulnerabilities that can lead to inconsistent stake accounting, fund loss, or denial of service. Silent error handling in EndBlocker stake removals, parameter changes not accounted for in queued operations, slashing not properly updating all related state (validator bonds, liquid shares), and EVM-Cosmos state desynchronization in precompiles are common patterns that result in economic exploits or locked funds.

### Vulnerability Description

#### Root Cause

The fundamental issues arise from:
1. **Silent error handling in EndBlocker**: Stake removal errors swallowed, leading to inconsistent state where users receive tokens but stake records remain
2. **Parameter changes not tracked**: Changes to `UnbondingTime` affect queued unbondings, breaking withdrawal order assumptions
3. **Incomplete slash accounting**: Slashing doesn't update `ValidatorBondShare` or `LiquidShares` for redelegated stakes
4. **EVM-Cosmos state desync**: Precompile calls modify Cosmos state but EVM statedb overwrites on commit
5. **Missing validator state checks**: Redelegation allowed to jailed/inactive validators

#### Attack Scenario

**Scenario 1: Double Unstaking via Silent Error**
1. User queues stake removal
2. In EndBlocker, tokens sent to user successfully
3. State update (`RemoveReputerStake`) fails due to some condition
4. Error silently swallowed, processing continues
5. User's stake record still exists - can queue another removal
6. User receives double their stake

**Scenario 2: Unbonding Queue DoS**
1. Governance reduces `UnbondingTime` from 21 days to 14 days
2. User A had queued unbonding at T+21 (completion at day 21)
3. User B queues unbonding at T+14 (completion at day 14)
4. Withdrawal loop iterates from front, finds User A's entry not yet complete
5. Breaks loop - User B cannot withdraw even though their unbonding is complete
6. User B's tokens locked until User A's original completion time

**Scenario 3: Reward Loss via State Desync**
1. ZEVM contract stakes tokens via staking precompile
2. Contract accumulates delegation rewards over time
3. Contract updates storage variable (triggers EVM statedb caching)
4. Contract calls `claimRewards` precompile - ZETA received in Cosmos state
5. EVM execution ends, statedb committed to Cosmos state
6. Cosmos balance overwritten with cached EVM balance (pre-reward)
7. ZETA rewards permanently lost

#### Vulnerable Pattern Examples

**Example 1: Silent Error Handling in EndBlocker** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: Errors silently ignored, state becomes inconsistent
func RemoveStakes(sdkCtx sdk.Context, blockHeight int64, k keeper.Keeper) {
    removals, err := k.GetStakeRemovalsForBlock(sdkCtx, blockHeight)
    if err != nil {
        return // Silent error!
    }
    
    for _, removal := range removals {
        // Step 1: Send tokens to staker
        err = k.SendCoinsFromModuleToAccount(sdkCtx, removal.Staker, removal.Amount)
        if err != nil {
            continue // Silent continue on failure
        }
        
        // Step 2: Update state
        err = k.RemoveReputerStake(sdkCtx, removal.TopicID, removal.Staker, removal.Amount)
        if err != nil {
            continue // ❌ Tokens sent but state NOT updated!
            // User can queue another removal for same stake
        }
    }
}
```

**Example 2: Unbonding Queue Broken by Parameter Change** [Approx Severity: MEDIUM]
```rust
// ❌ VULNERABLE: Assumes ordered completion times based on queue order
fn execute_withdraw_fund(deps: DepsMut, env: Env) -> Result<Response, ContractError> {
    let mut funds: Vec<Coin> = vec![];
    
    loop {
        match UNSTAKING_QUEUE.front(deps.storage).unwrap() {
            Some(UnstakingTokens { payout_at, .. }) if payout_at <= env.block.time => {
                // Process this entry
                if let Some(UnstakingTokens { fund, .. }) = 
                    UNSTAKING_QUEUE.pop_front(deps.storage)? 
                {
                    funds.push(fund)
                }
            }
            _ => break, // ❌ Breaks when first non-expired entry found!
        }
    }
    // If UnbondingTime decreased, newer entries may expire before older ones
    // But we break at first non-expired, blocking newer expired entries
}
```

**Example 3: Incomplete Slash Accounting** [Approx Severity: MEDIUM]
```go
// ❌ VULNERABLE: ValidatorBondShare and LiquidShares not updated
func (k Keeper) SlashRedelegation(ctx context.Context, srcValidator types.Validator,
    redelegation types.Redelegation, infractionHeight int64, slashFactor math.LegacyDec,
) (totalSlashAmount math.Int, err error) {
    // ... calculate sharesToUnbond
    
    tokensToBurn, err := k.Unbond(ctx, delegatorAddress, valDstAddr, sharesToUnbond)
    if err != nil {
        return math.ZeroInt(), err
    }
    
    // ❌ MISSING: If redelegation involves validatorBond, should update:
    // validator.ValidatorBondShare -= sharesToUnbond
    
    // ❌ MISSING: If delegatorAddress is liquid staker, should update:
    // validator.LiquidShares -= sharesToUnbond
    
    return tokensToBurn, nil
}
```

**Example 4: EVM-Cosmos State Desynchronization** [Approx Severity: MEDIUM]
```go
// ❌ VULNERABLE: ZETA rewards not added to EVM statedb
func (c *Contract) ClaimRewards(ctx sdk.Context, evm *vm.EVM, contract *vm.Contract,
    method *abi.Method, args []interface{},
) ([]byte, error) {
    delegatorAddress := contract.Caller()
    
    // Claims rewards, ZETA received in Cosmos bank state
    rewards, err := c.distributionKeeper.WithdrawDelegationRewards(ctx, 
        sdk.AccAddress(delegatorAddress.Bytes()), validatorAddr)
    
    for _, coin := range rewards {
        if coin.Denom == "azeta" {
            continue // ❌ Skipped! Not added to EVM statedb
        }
        // Only non-ZETA tokens processed...
    }
    
    return method.Outputs.Pack(true)
    // When EVM state commits to Cosmos, ZETA balance overwritten with stale value
}
```

**Example 5: Redelegation to Jailed Validator** [Approx Severity: MEDIUM]
```go
// ❌ VULNERABLE: New delegatee's jailed status not checked
func (k msgServer) Redelegate(goCtx context.Context, msg *types.MsgRedelegate) 
    (*types.MsgRedelegateResponse, error) {
    ctx := sdk.UnwrapSDKContext(goCtx)
    
    // Checks source delegatee is not jailed
    srcValidator, found := k.GetValidator(ctx, msg.SrcValidatorAddr)
    if srcValidator.IsJailed() {
        return nil, ErrValidatorJailed
    }
    
    // ❌ MISSING: Check destination validator is not jailed!
    // dstValidator, found := k.GetValidator(ctx, msg.DstValidatorAddr)
    // if dstValidator.IsJailed() { return nil, ErrValidatorJailed }
    
    // Allows redelegation to jailed validator
    return k.BeginRedelegation(ctx, msg.DelegatorAddr, msg.SrcValidatorAddr, 
        msg.DstValidatorAddr, msg.Amount)
}
```

### Impact Analysis

#### Technical Impact
- Double stake withdrawal from silent error handling
- Unbonding queue blocked, funds inaccessible
- Validator bond/liquid shares accounting corrupted
- EVM state overwrites Cosmos state, losing rewards
- Stakes locked in jailed validators

#### Business Impact
- Direct fund loss from double withdrawals
- Denial of service for legitimate unbonding requests
- Slashing calculations incorrect, affecting validator economics
- Users lose staking rewards through state desync
- Locked funds until validator unjailed (may be permanent)

#### Affected Scenarios
- Any chain with custom staking modules
- EVM-enabled chains with staking precompiles
- Chains using liquid staking (LSM)
- CosmWasm contracts managing unbonding queues
- Governance changes to staking parameters

### Secure Implementation

**Fix 1: Use Cache Context for Atomic State Updates**
```go
// ✅ SECURE: Atomic updates using cache context
func RemoveStakes(sdkCtx sdk.Context, blockHeight int64, k keeper.Keeper) {
    removals, err := k.GetStakeRemovalsForBlock(sdkCtx, blockHeight)
    if err != nil {
        sdkCtx.Logger().Error("failed to get stake removals", "error", err)
        return
    }
    
    for _, removal := range removals {
        // Use cache context for atomic operation
        cacheCtx, write := sdkCtx.CacheContext()
        
        // Step 1: Update state first (can fail without side effects)
        err = k.RemoveReputerStake(cacheCtx, removal.TopicID, removal.Staker, removal.Amount)
        if err != nil {
            sdkCtx.Logger().Error("failed to remove stake", "error", err)
            continue
        }
        
        // Step 2: Send tokens
        err = k.SendCoinsFromModuleToAccount(cacheCtx, removal.Staker, removal.Amount)
        if err != nil {
            sdkCtx.Logger().Error("failed to send coins", "error", err)
            continue // No state committed
        }
        
        // Only write if both succeeded
        write()
    }
}
```

**Fix 2: Sort Unbonding Queue by Completion Time**
```rust
// ✅ SECURE: Process all expired entries regardless of queue order
fn execute_withdraw_fund(deps: DepsMut, env: Env) -> Result<Response, ContractError> {
    let mut funds: Vec<Coin> = vec![];
    let mut remaining: Vec<UnstakingTokens> = vec![];
    
    // Drain queue and separate expired vs not-yet-expired
    while let Some(entry) = UNSTAKING_QUEUE.pop_front(deps.storage)? {
        if entry.payout_at <= env.block.time {
            funds.push(entry.fund);
        } else {
            remaining.push(entry);
        }
    }
    
    // Re-add non-expired entries
    for entry in remaining {
        UNSTAKING_QUEUE.push_back(deps.storage, &entry)?;
    }
    
    // Return all expired funds
    Ok(Response::new().add_message(BankMsg::Send { ... }))
}
```

**Fix 3: Sync EVM State After Precompile Rewards**
```go
// ✅ SECURE: Add claimed rewards to EVM statedb
func (c *Contract) ClaimRewards(ctx sdk.Context, evm *vm.EVM, contract *vm.Contract,
    method *abi.Method, args []interface{},
) ([]byte, error) {
    delegatorAddress := contract.Caller()
    
    rewards, err := c.distributionKeeper.WithdrawDelegationRewards(ctx, 
        sdk.AccAddress(delegatorAddress.Bytes()), validatorAddr)
    
    for _, coin := range rewards {
        if coin.Denom == "azeta" {
            // Sync ZETA balance to EVM statedb
            zetaAmount := coin.Amount.BigInt()
            currentBalance := evm.StateDB.GetBalance(delegatorAddress)
            newBalance := new(big.Int).Add(currentBalance, zetaAmount)
            evm.StateDB.SetBalance(delegatorAddress, newBalance) // ✅ Sync!
        }
        // Process other tokens...
    }
    
    return method.Outputs.Pack(true)
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `if err != nil { continue }` in EndBlocker stake operations
- Pattern 2: FIFO queue with `break` on first non-matching condition
- Pattern 3: `SlashRedelegation` without ValidatorBondShare update
- Pattern 4: Precompile returning without syncing statedb
- Pattern 5: `Redelegate` without destination validator status check
```

#### Audit Checklist
- [ ] EndBlocker operations use cache context for atomicity
- [ ] Errors in EndBlocker logged, not silently swallowed
- [ ] Unbonding queue processes all expired entries
- [ ] Slash operations update all related state (bonds, liquid shares)
- [ ] EVM precompiles sync state changes back to statedb
- [ ] Redelegation checks destination validator is not jailed/inactive
- [ ] Parameter changes don't break existing queued operations

### Real-World Examples

| Protocol | Audit Firm | Severity | Issue |
|----------|------------|----------|-------|
| Allora | Sherlock | HIGH | Silent error handling in EndBlocker stake removal |
| Andromeda | Sherlock | MEDIUM | UnbondingTime changes break withdrawal queue |
| Cosmos LSM | OtterSec | MEDIUM | Slash redelegation doesn't update ValidatorBondShare |
| ZetaChain | Sherlock | MEDIUM | ZETA rewards lost due to EVM-Cosmos state desync |
| Elixir | TrailOfBits | MEDIUM | Redelegation allowed to jailed validators |

### Keywords for Search

`EndBlocker, RemoveStakes, RemoveDelegateStakes, UnbondingTime, UNSTAKING_QUEUE, SlashRedelegation, ValidatorBondShare, LiquidShares, precompile, statedb, delegation_rewards, redelegate, jailed_validator, cache_context, atomic_state`
