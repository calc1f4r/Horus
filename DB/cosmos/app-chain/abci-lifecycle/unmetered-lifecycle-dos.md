---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: abci_lifecycle
vulnerability_type: unmetered_execution_dos

# Attack Vector Details
attack_type: resource_exhaustion
affected_component: abci_lifecycle_handlers

# Technical Primitives
primitives:
  - beginblocker
  - endblocker
  - finalizeblock
  - abci_hooks
  - gas_metering
  - unbounded_iteration
  - chain_halt

# Impact Classification
severity: high
impact: chain_halt
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - cometbft
  - abci
  - chain_halt
  - dos
  - gas_metering
  - lifecycle
  
language: go
version: all
---

## References
- [linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md](../../../reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md)
- [linear-iteration-over-undelegations-with-unmetered-token-transfers-expose-a-perm.md](../../../reports/cosmos_cometbft_findings/linear-iteration-over-undelegations-with-unmetered-token-transfers-expose-a-perm.md)
- [h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md](../../../reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md)
- [h-7-removestakes-and-removedelegatestakes-silently-handle-errors-in-endblocker.md](../../../reports/cosmos_cometbft_findings/h-7-removestakes-and-removedelegatestakes-silently-handle-errors-in-endblocker.md)
- [unchecked-block-gas-limit.md](../../../reports/cosmos_cometbft_findings/unchecked-block-gas-limit.md)
- [potential-non-determinism-issue-in-finalizeblock.md](../../../reports/cosmos_cometbft_findings/potential-non-determinism-issue-in-finalizeblock.md)

## Vulnerability Title

**Unmetered ABCI Lifecycle Execution Enables Permissionless Chain Halts**

### Overview

Cosmos SDK appchains execute critical operations during ABCI lifecycle phases (`BeginBlock`, `EndBlock`, `FinalizeBlock`) without metered gas consumption. Attackers can exploit unbounded iteration over user-created data structures (rewards plans, delegations, unbondings), hook failures in automatic slashing paths, or silent error handling to cause prolonged chain halts, state corruption, or consensus failures. These vulnerabilities are particularly severe because lifecycle execution is permissionlessly triggered each block and errors in these phases halt the entire chain.

### Vulnerability Description

#### Root Cause

The fundamental issues arise from:
1. **Unmetered iteration**: `BeginBlock`/`EndBlock` iterate over user-controlled data structures without consuming gas, allowing attackers to create arbitrarily many entries
2. **Hook failure propagation**: Errors from hooks called during automatic operations (slashing, rewards distribution) propagate to ABCI, causing chain halt
3. **Silent error handling**: Some implementations log errors and `continue`, leaving state partially updated
4. **Non-determinism in lifecycle**: RPC calls or external dependencies in `FinalizeBlock` cause nodes to diverge
5. **Geometric amplification**: Attackers can cause exponentially growing processing time across successive blocks

#### Attack Scenario

**Scenario 1: Rewards Plan Flood (MilkyWay)**
1. Attacker creates thousands of rewards plans (each costs only a fixed fee, e.g., 1 TIA)
2. All plans are unboundedly iterated in unmetered `BeginBlock` execution
3. Single block processing takes minutes, halting the chain
4. Attack cost: ~$50,000; Impact: Indefinite chain halt

**Scenario 2: Unbonding Amplification**
1. Attacker accumulates multi-denom delegations across many blocks cheaply
2. Undelegates in batches, scheduling maturation for same time window
3. Each block processes 2x the unbondings of the previous due to geometric accumulation
4. Chain halts when single block must process arbitrary unbonding maturations

**Scenario 3: Hook Failure Chain Halt (MANTRA)**
1. Attacker creates tokenfactory denom and deposits as validator rewards
2. Sets `BeforeSendHook` to invalid address (non-contract EOA)
3. When validator is slashed, `BeginBlocker` calls slashing → unbond → hook → error
4. Error propagates to ABCI, halting chain entirely

**Scenario 4: Silent State Corruption (Allora)**
1. `EndBlocker` processes stake removals: sends coins, then updates state
2. If state update fails, error is logged but loop continues
3. User receives coins but state still shows stake exists
4. User can re-queue removal for same stakes, draining funds

#### Vulnerable Pattern Examples

**Example 1: Unbounded BeginBlock Iteration** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: Unbounded iteration over user-created plans
// File: allocation.go#L115-L117 (MilkyWay)
func (k Keeper) BeginBlocker(ctx sdk.Context) error {
    // No gas metering - executes in unmetered context
    plans := k.GetAllRewardsPlans(ctx) // Attacker can create unlimited plans
    
    for _, plan := range plans {
        // Each iteration costs real compute time but no gas
        k.AllocateRewards(ctx, plan)  // O(n) where n is attacker-controlled
    }
    return nil
}
```

**Example 2: Geometric Unbonding Amplification** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: Unbonding maturation with multi-denom delegations
// File: end_blocker.go#L11-L38 (MilkyWay)
func EndBlocker(ctx sdk.Context, k Keeper) error {
    unbondings := k.GetMatureUnbondings(ctx)
    
    for _, unbonding := range unbondings {
        // For 10 denoms: 109,380 unmetered gas vs 48,764 metered gas to create
        // Attacker pays 1x gas to schedule, chain pays 2x+ gas to process
        k.CompleteUnbonding(ctx, unbonding)  // Includes expensive SendCoins
    }
    return nil
}

// Attack economics (10 denoms per delegation):
// Metered gas to undelegate (attacker pays): 48,764
// Unmetered gas to complete (chain pays): 109,380 (>2x)
// At 20 denoms: >3x amplification ratio
```

**Example 3: Hook Failure Propagation to ABCI** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: Error from hook propagates to BeginBlocker
// Flow: BeginBlock -> SlashingBeginBlocker -> Slash -> Unbond -> Hook -> Error

// x/slashing/abci.go
func BeginBlocker(ctx sdk.Context, req abci.RequestBeginBlock, k keeper.Keeper) {
    for _, voteInfo := range req.LastCommitInfo.Votes {
        k.HandleValidatorSignature(ctx, voteInfo)  // Error = chain halt
    }
}

// Eventually calls:
// x/staking/keeper/delegation.go
func (k Keeper) Unbond(ctx sdk.Context, ...) error {
    // Hook can fail if BeforeSendHook set to invalid address
    if err := k.BeforeDelegationSharesModified(ctx, ...); err != nil {
        return err  // Error bubbles up to ABCI = CHAIN HALT
    }
    // ...
}
```

**Example 4: Silent Error Handling Creates State Corruption** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: Errors logged but loop continues with partial state
// File: stake_removals.go#L13-L63 (Allora)
func RemoveStakes(sdkCtx sdk.Context, currentBlock int64, k Keeper) {
    removals, _ := k.GetStakeRemovalsForBlock(sdkCtx, currentBlock)
    
    for _, stakeRemoval := range removals {
        // Step 1: Send coins to user
        err := k.SendCoinsFromModuleToAccount(sdkCtx, stakeRemoval.Amount)
        if err != nil {
            sdkCtx.Logger().Error("Error removing stake")
            continue  // User didn't get coins, okay
        }
        
        // Step 2: Update stake records
        err = k.RemoveReputerStake(sdkCtx, stakeRemoval)
        if err != nil {
            sdkCtx.Logger().Error("Error removing stake")
            continue  // ❌ User GOT coins but stake not removed!
            // User can queue another removal for same stake
        }
    }
}
```

**Example 5: Non-Determinism in FinalizeBlock** [Approx Severity: MEDIUM]
```go
// ❌ VULNERABLE: RPC call in FinalizeBlock causes non-determinism
// File: FinalizeBlock handler (Story)
func (app *App) FinalizeBlock(req abci.RequestFinalizeBlock) (resp abci.ResponseFinalizeBlock, err error) {
    // ... deterministic block processing ...
    
    // PostFinalize path calls CometBFT API via RPC
    err = app.PostFinalize(ctx)  // Network call - non-deterministic!
    if err != nil {
        return resp, err  // Some nodes fail, some succeed = CONSENSUS BREAK
    }
    return resp, nil
}

// The RPC call can fail due to:
// - Network timeout on some nodes
// - Connection errors
// - Different response times
// Leading to: Some nodes halt, others continue = chain split
```

### Secure Implementation Examples

**Example 1: Bounded Iteration with Gas Metering**
```go
// ✅ SECURE: Limit iterations AND charge gas
func (k Keeper) BeginBlocker(ctx sdk.Context) error {
    plans := k.GetAllRewardsPlans(ctx)
    
    // Hard cap on iterations per block
    maxIterations := k.GetMaxPlansPerBlock(ctx)
    processed := 0
    
    for _, plan := range plans {
        if processed >= maxIterations {
            break  // Process remaining in next block
        }
        
        // Charge gas proportional to work
        ctx.GasMeter().ConsumeGas(
            uint64(GasPerPlanAllocation),
            "rewards plan allocation",
        )
        
        k.AllocateRewards(ctx, plan)
        processed++
    }
    return nil
}
```

**Example 2: Scaling Gas Cost for Creation**
```go
// ✅ SECURE: Cost increases with total count
func (ms msgServer) CreateRewardsPlan(ctx context.Context, msg *MsgCreateRewardsPlan) error {
    existingPlans := ms.k.GetPlanCount(ctx)
    
    // Scaling gas cost prevents flooding
    baseGas := uint64(50000)
    scalingGas := uint64(existingPlans * 1000)
    ctx.GasMeter().ConsumeGas(baseGas + scalingGas, "rewards plan creation fee")
    
    // Or cap the number of denoms per delegation
    if len(msg.Denoms) > MaxDenomsPerDelegation {
        return ErrTooManyDenoms
    }
    
    return ms.k.CreatePlan(ctx, msg)
}
```

**Example 3: Hook Error Isolation**
```go
// ✅ SECURE: Isolate hook failures from consensus-critical paths
func (k Keeper) Unbond(ctx sdk.Context, ...) error {
    // Use cache context to isolate hook failures
    cacheCtx, write := ctx.CacheContext()
    
    err := k.BeforeDelegationSharesModified(cacheCtx, ...)
    if err != nil {
        // Log but don't halt chain - hook failures are not consensus-critical
        k.Logger(ctx).Error("hook failed, skipping rewards", "error", err)
        // Still proceed with unbonding
    } else {
        write()  // Commit hook state changes
    }
    
    // Critical unbonding logic continues regardless of hook
    return k.completeUnbond(ctx, ...)
}
```

**Example 4: Atomic State Updates with Cache Context**
```go
// ✅ SECURE: All-or-nothing state updates
func RemoveStakes(sdkCtx sdk.Context, currentBlock int64, k Keeper) {
    removals, _ := k.GetStakeRemovalsForBlock(sdkCtx, currentBlock)
    
    for _, stakeRemoval := range removals {
        // Use cache context - write only if everything succeeds
        cacheCtx, write := sdkCtx.CacheContext()
        
        // Step 1: Update state FIRST (in cache)
        err := k.RemoveReputerStake(cacheCtx, stakeRemoval)
        if err != nil {
            sdkCtx.Logger().Error("Error removing stake", "error", err)
            continue  // Cache discarded, nothing written
        }
        
        // Step 2: Send coins (in cache)
        err = k.SendCoinsFromModuleToAccount(cacheCtx, stakeRemoval.Amount)
        if err != nil {
            sdkCtx.Logger().Error("Error sending coins", "error", err)
            continue  // Cache discarded, nothing written
        }
        
        write()  // ✅ Both succeeded, commit atomic state change
    }
}
```

**Example 5: Deterministic FinalizeBlock**
```go
// ✅ SECURE: No external calls in deterministic ABCI paths
func (app *App) FinalizeBlock(req abci.RequestFinalizeBlock) (resp abci.ResponseFinalizeBlock, err error) {
    // All operations must be deterministic
    resp, err = app.processBlock(req)
    if err != nil {
        return resp, err
    }
    
    // PostFinalize operations that involve RPC:
    // - Must ignore errors (log only)
    // - Or execute asynchronously after block committed
    go func() {
        if err := app.PostFinalize(ctx); err != nil {
            app.Logger().Error("post-finalize failed", "error", err)
            // Never propagate to ABCI
        }
    }()
    
    return resp, nil  // Always return success for committed block
}
```

### Impact Analysis

**Technical Impact:**
- Chain halt: Block production stops indefinitely (HIGH severity)
- State corruption: Inconsistent state between coins sent and stake records (HIGH severity)
- Consensus break: Nodes diverge on block validity due to non-determinism (CRITICAL severity)
- Double-spend potential: Same stake can be withdrawn multiple times (HIGH severity)

**Business Impact:**
- Protocol reputation damage from chain halts
- Loss of user funds if state corruption allows double withdrawals
- Validator coordination required for manual recovery
- Potential need for hard fork to resolve consensus breaks

**Affected Scenarios:**
- Rewards distribution during `BeginBlock`
- Stake/delegation unbonding during `EndBlock`
- Automatic slashing for validator misbehavior
- Any module with unbounded user-created data structures
- Cross-chain operations with external dependencies

### Detection Patterns

**Code Review Patterns:**
```go
// Look for unbounded iteration in BeginBlocker/EndBlocker
pattern: func.*BeginBlocker|EndBlocker.*{
    for.*range.*Get.*All
    // or
    for.*range.*k\..*Iterator
}

// Look for silent error handling
pattern: if err != nil {
    .*Logger.*Error
    continue
}

// Look for hook calls in slashing/evidence paths
pattern: BeginBlocker.*Slash.*Hook

// Look for RPC/external calls in FinalizeBlock
pattern: FinalizeBlock.*rpc\.Call|http\.
```

**Audit Checklist:**
- [ ] All `BeginBlocker`/`EndBlocker` have bounded iteration or gas metering
- [ ] User-created data structures have creation cost scaling with total count
- [ ] Hook failures in automatic operations don't propagate to ABCI
- [ ] State updates use cache context for atomicity
- [ ] `FinalizeBlock` contains no non-deterministic operations
- [ ] Error handling doesn't leave partial state updates
- [ ] Multi-denom operations have bounded denom counts

### Real-World Examples

| Protocol | Vulnerability | Severity | Audit Firm |
|----------|--------------|----------|------------|
| MilkyWay | Unbounded rewards plan iteration in BeginBlock | HIGH | Cantina |
| MilkyWay | Geometric unbonding amplification in EndBlock | HIGH | Cantina |
| MANTRA Chain | Hook failure causes BeginBlocker chain halt | HIGH | Code4rena |
| Allora | Silent error handling in EndBlocker stake removal | HIGH | Sherlock |
| Skip Block-SDK | Unchecked block gas limit in PrepareProposal | HIGH | OtterSec |
| Story | Non-deterministic RPC in FinalizeBlock | MEDIUM | Security Audit |

### Keywords for Search

**Primary Terms:** BeginBlocker, EndBlocker, FinalizeBlock, chain_halt, unmetered_gas, lifecycle_dos
**ABCI Terms:** abci_lifecycle, BeginBlock, EndBlock, PrepareProposal, ProcessProposal, consensus_failure
**Attack Vectors:** unbounded_iteration, geometric_amplification, hook_failure, silent_error, state_corruption
**Impacts:** chain_halt, consensus_break, double_spend, state_inconsistency
**Related APIs:** GetAllRewardsPlans, CompleteUnbonding, SlashRedelegation, BeforeDelegationSharesModified
**Code Patterns:** for_range_getall, continue_after_error, rpc_in_finalize, unmetered_loop
**Protocol Examples:** milkyway, mantra_chain, allora, skip_block_sdk, story_protocol
