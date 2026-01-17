---
# Core Classification
protocol: generic
chain: cosmos
category: denial_of_service
vulnerability_type: hook_callback_abuse

# Attack Vector Details
attack_type: denial_of_service
affected_component: module_hooks

# Technical Primitives
primitives:
  - tokenfactory_hooks
  - beforesend_hook
  - staking_hooks
  - plugin_callbacks
  - external_callbacks
  - BeforeDelegationSharesModified

# Impact Classification
severity: high
impact: fund_lockup
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - tokenfactory
  - staking
  - hooks
  - callbacks
  - chain_halt
  - funds_stuck

# Version Info
language: go
version: all
---

## References
- [ref-1]: reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md
- [ref-2]: reports/cosmos_cometbft_findings/h-1-rogue-plugin-can-become-unremovable-and-halt-all-staking-and-claiming.md
- [ref-3]: reports/cosmos_cometbft_findings/staking-and-withdrawal-operations-might-be-blocked.md
- [ref-4]: reports/cosmos_cometbft_findings/m-02-denial-of-service-via-large-payload-storage-exhaustion.md

## Vulnerability Title

**Malicious Hook/Callback Denial of Service in Cosmos SDK Modules**

### Overview

Cosmos SDK modules and custom appchain implementations frequently use hook patterns (BeforeSendHook, BeforeDelegationSharesModified, plugin callbacks) to extend functionality. When these hooks can be controlled by untrusted parties or can fail in unhandled ways, attackers can exploit them to block critical operations, lock user funds, or even halt the entire chain. This vulnerability class affects TokenFactory modules, staking/distribution hooks, and external plugin systems.

### Vulnerability Description

#### Root Cause

The fundamental issue is that **hook/callback execution is on the critical path** of important operations (token transfers, staking actions, reward distribution) but the hook's behavior can be:
1. **Controlled by untrusted parties** (token creators can set arbitrary hook addresses)
2. **Designed to fail intentionally** (malicious plugins returning errors or overflow values)
3. **Dependent on external state** that can be manipulated (DISABLED flags, storage values)

When hooks fail and the calling code doesn't gracefully handle failures, the entire operation reverts, creating denial of service conditions.

#### Attack Scenario

**Scenario 1: TokenFactory BeforeSendHook Chain Halt (HIGH)**

1. Attacker creates a TokenFactory denomination
2. Attacker mints tokens and deposits them to a validator's reward pool via `MsgDepositValidatorRewardsPool`
3. Attacker sets `BeforeSendHook` to an invalid address (EOA instead of contract)
4. All staking actions now fail because `BeforeDelegationSharesModified` must distribute rewards, but reward transfer fails due to malicious hook
5. If a delegator has a pending redelegation when a validator gets slashed, the `BeginBlocker` panics and halts the chain

**Scenario 2: Rogue Plugin Overflow Attack (HIGH)**

1. Plugin is added to StakingModule
2. Plugin turns malicious (bug or upgrade)
3. Plugin returns `2**256-1` in `claim()` causing overflow
4. Plugin returns `false` for `deactivated()` preventing removal
5. All staking operations (stake, claim, exit) are frozen

**Scenario 3: External Hook Revert Blocking (MEDIUM)**

1. Staking contract calls external hook (e.g., `beforeLockUpdate`)
2. Hook contract has `require` statement based on controllable state
3. Admin or attacker sets state that causes hook to revert
4. All staking and withdrawal operations blocked

#### Vulnerable Pattern Examples

**Example 1: TokenFactory BeforeSendHook DoS** [Severity: HIGH]
```go
// ❌ VULNERABLE: No validation that hook address is a valid contract
func (k Keeper) SetBeforeSendHook(ctx sdk.Context, denom string, contractAddr string) error {
    // Only checks that sender is denom admin - no contract validation
    if !k.IsDenomAdmin(ctx, denom, msg.Sender) {
        return ErrUnauthorized
    }
    
    // Attacker can set ANY address including EOA
    k.setBeforeSendHook(ctx, denom, contractAddr)
    return nil
}

// When transferring tokens with this denom:
func (k Keeper) TrackBeforeSend(ctx sdk.Context, from, to sdk.AccAddress, amount sdk.Coin) error {
    hook := k.GetBeforeSendHook(ctx, amount.Denom)
    if hook != "" {
        // This will FAIL if hook is not a valid contract
        // Error propagates up and blocks the transfer
        return k.callBeforeSendHook(ctx, hook, from, to, amount)
    }
    return nil
}
```

**Example 2: Staking Hook Failure Propagation** [Severity: HIGH]
```go
// ❌ VULNERABLE: Hook failure blocks critical staking operations
func (k Keeper) BeforeDelegationSharesModified(ctx sdk.Context, delAddr sdk.AccAddress, valAddr sdk.ValAddress) error {
    // Must withdraw rewards before modifying delegation
    _, err := k.withdrawDelegationRewards(ctx, delAddr, valAddr)
    if err != nil {
        // Error propagates up - if rewards contain tokens with malicious hooks,
        // ALL staking actions fail (delegate, undelegate, redelegate)
        return err
    }
    return nil
}

// Called from BeginBlocker during slashing - chain halts on error!
func (k Keeper) SlashRedelegation(ctx sdk.Context, ...) {
    // Unbond calls BeforeDelegationSharesModified
    if err := k.Unbond(ctx, delAddr, valAddr, shares); err != nil {
        // BeginBlocker receives error -> chain halt
        panic(err)
    }
}
```

**Example 3: Plugin Overflow Attack** [Severity: HIGH]
```solidity
// ❌ VULNERABLE: No bounds checking on plugin return values
function _claim(address account, address to, bytes calldata auxData) private returns (uint256) {
    uint256 total;
    for (uint256 i = 0; i < nPlugins; i++) {
        try IPlugin(plugins[i]).claim(account, to, parsedAuxData[i]) returns (uint256 xClaimed) {
            // Malicious plugin returns 2**256-1, causing overflow
            total += xClaimed;  // OVERFLOW!
        } catch {
            emit PluginClaimFailed(plugins[i]);
        }
    }
    return total;
}

// ❌ VULNERABLE: Plugin can prevent its own removal
function removePlugin(address plugin) external onlyRole(PLUGIN_EDITOR_ROLE) {
    // Malicious plugin returns false forever
    require(IPlugin(plugin).deactivated(), "Plugin not deactivated");
    // Never reached - plugin is unremovable
}
```

**Example 4: External Hook State Dependency** [Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: Hook depends on external controllable state
function _stake(uint256 amount) internal {
    // External call to hook
    incentivesController.beforeLockUpdate(msg.sender);
    
    // If hook reverts, staking is blocked
    _balances[msg.sender] += amount;
}

// In Disqualifier.sol
function processUser(address user) external {
    _processUserWithBounty(user);
}

function _processUserWithBounty(address user) internal {
    // DISABLED can be set by admin - blocks all staking/withdrawals
    require(!DISABLED, "Disqualifier disabled");
    // ...
}
```

### Impact Analysis

#### Technical Impact
- **Chain Halt**: BeginBlocker errors cause consensus failure and network stoppage
- **State Corruption**: Partial operations leave inconsistent state
- **Hook Loop Dependencies**: Circular hook calls can exhaust gas
- **Permanent Lockup**: No way to bypass malicious hooks without chain upgrade

#### Business Impact
- **Frozen Funds**: Users cannot unstake, withdraw, or claim rewards
- **Validator Operations Blocked**: Cannot redelegate away from misbehaving validators
- **Protocol Reputation**: Chain halts cause loss of user trust
- **Recovery Costs**: Requires governance action or chain upgrade to fix

#### Affected Scenarios
- TokenFactory token transfers when BeforeSendHook set to invalid address
- All staking operations when reward tokens have malicious hooks
- Slashing during BeginBlocker with poisoned reward tokens
- Plugin-based staking systems with upgradeable plugins
- Any hook that depends on external contract state

### Secure Implementation

**Fix 1: Validate Hook Addresses Are Valid Contracts**
```go
// ✅ SECURE: Validate hook is a valid CosmWasm contract
func (k Keeper) SetBeforeSendHook(ctx sdk.Context, denom string, contractAddr string) error {
    if !k.IsDenomAdmin(ctx, denom, msg.Sender) {
        return ErrUnauthorized
    }
    
    // Validate contract exists and implements required interface
    addr, err := sdk.AccAddressFromBech32(contractAddr)
    if err != nil {
        return err
    }
    
    // Check it's actually a contract
    if !k.wasmKeeper.HasContractInfo(ctx, addr) {
        return ErrInvalidHookAddress
    }
    
    // Optionally: whitelist allowed hook contracts
    if !k.IsWhitelistedHook(ctx, addr) {
        return ErrHookNotWhitelisted
    }
    
    k.setBeforeSendHook(ctx, denom, contractAddr)
    return nil
}
```

**Fix 2: Graceful Hook Failure Handling**
```go
// ✅ SECURE: Catch hook failures and handle gracefully
func (k Keeper) TrackBeforeSend(ctx sdk.Context, from, to sdk.AccAddress, amount sdk.Coin) error {
    hook := k.GetBeforeSendHook(ctx, amount.Denom)
    if hook == "" {
        return nil
    }
    
    // Use cached context to isolate hook execution
    cacheCtx, write := ctx.CacheContext()
    
    err := k.callBeforeSendHook(cacheCtx, hook, from, to, amount)
    if err != nil {
        // Log failure but don't block transfer
        k.Logger(ctx).Error("BeforeSendHook failed", "denom", amount.Denom, "error", err)
        // Emit event for monitoring
        ctx.EventManager().EmitEvent(sdk.NewEvent("hook_failed", ...))
        // Optionally: disable the malicious hook
        k.disableHook(ctx, amount.Denom)
        return nil  // Continue with transfer
    }
    
    write()  // Commit hook state changes only on success
    return nil
}
```

**Fix 3: Force Remove Malicious Plugins**
```solidity
// ✅ SECURE: Add force removal option for emergencies
function removePlugin(address plugin, bool force) external onlyRole(PLUGIN_EDITOR_ROLE) {
    if (!force) {
        require(IPlugin(plugin).deactivated(), "Plugin not deactivated");
    }
    // Force removal bypasses plugin cooperation
    _removePluginFromList(plugin);
    emit PluginRemoved(plugin, force);
}

// ✅ SECURE: Use safe math and bounds checking
function _claim(address account, address to, bytes calldata auxData) private returns (uint256) {
    uint256 total;
    uint256 MAX_CLAIM = type(uint128).max;  // Reasonable upper bound
    
    for (uint256 i = 0; i < nPlugins; i++) {
        try IPlugin(plugins[i]).claim(account, to, parsedAuxData[i]) returns (uint256 xClaimed) {
            // Bound check prevents overflow
            require(xClaimed <= MAX_CLAIM, "Claim amount too large");
            total += xClaimed;
        } catch {
            emit PluginClaimFailed(plugins[i]);
        }
    }
    return total;
}
```

**Fix 4: Isolate Hook State Dependencies**
```solidity
// ✅ SECURE: Don't let external state block critical operations
function _stake(uint256 amount) internal {
    // Try hook but don't block on failure
    try incentivesController.beforeLockUpdate(msg.sender) {
        // Hook succeeded
    } catch {
        // Log failure but continue staking
        emit HookFailed("beforeLockUpdate", msg.sender);
    }
    
    _balances[msg.sender] += amount;
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- MsgSetBeforeSendHook or similar hook registration without address validation
- BeforeDelegationSharesModified/AfterDelegation hooks that can fail
- Plugin.claim() or similar with unchecked return values
- Hooks called from BeginBlocker/EndBlocker without error handling
- External calls in critical paths without try/catch
- Require statements in hooks dependent on mutable state
```

#### Audit Checklist
- [ ] Can untrusted parties set hook addresses?
- [ ] Are hook addresses validated as valid contracts?
- [ ] What happens when hooks fail - does it block operations?
- [ ] Are hooks called from BeginBlocker/EndBlocker?
- [ ] Can plugin return values cause overflow?
- [ ] Can plugins prevent their own removal?
- [ ] Do hooks depend on externally controllable state?
- [ ] Is there emergency bypass for malicious hooks?

### Real-World Examples

#### Known Audit Findings
- **MANTRA Chain** (Code4rena 2024) - HIGH: BeforeSendHook can halt chain via invalid address
- **Telcoin** (Sherlock 2023) - HIGH: Rogue plugin halts all staking via overflow
- **Radiant Capital** (Zokyo 2022) - MEDIUM: Hook state blocks staking/withdrawals
- **Toki Bridge** (Shieldify) - MEDIUM: Callback gas exhaustion blocks IBC channel

### Prevention Guidelines

#### Development Best Practices
1. **Whitelist Hook Contracts**: Only allow governance-approved contracts as hooks
2. **Validate Hook Addresses**: Verify contract exists and implements required interface
3. **Graceful Failure**: Catch hook errors and continue critical operations
4. **Bound Return Values**: Validate plugin/hook return values are within expected ranges
5. **Emergency Bypass**: Implement force-removal for malicious hooks/plugins
6. **Isolate Hook State**: Don't let hook failures block user fund access
7. **Monitor Hooks**: Log and alert on hook failures for quick response

#### Testing Requirements
- Unit tests for hook registration with invalid addresses
- Integration tests for hook failure scenarios
- Fuzzing hook return values for overflow
- Test BeginBlocker behavior with failing hooks
- Test emergency removal of malicious plugins

### Keywords for Search

`BeforeSendHook`, `BeforeDelegationSharesModified`, `AfterDelegationModified`, `tokenfactory`, `hook_callback`, `plugin_dos`, `staking_hook`, `chain_halt`, `BeginBlocker_panic`, `hook_revert`, `callback_failure`, `plugin_overflow`, `unremovable_plugin`, `external_callback`, `hook_validation`, `fund_lockup`, `cosmos_sdk_hooks`, `module_hooks`, `delegation_hooks`, `reward_distribution_hooks`

### Related Vulnerabilities

- [Epoch Snapshot Timing Manipulation](../staking-delegation/epoch-snapshot-timing-manipulation.md)
- [Slashing Evasion Bypass](../staking-delegation/slashing-evasion-bypass.md)
