---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: precompile
vulnerability_type: state_manipulation

# Attack Vector Details
attack_type: fund_theft
affected_component: evm_precompile

# Technical Primitives
primitives:
  - precompile
  - delegatecall
  - statedb
  - msg.value
  - calldata
  - EVMC_CALL

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.7
financial_impact: critical

# Context Tags
tags:
  - cosmos_sdk
  - evm
  - ethermint
  - precompile
  - delegatecall
  - staking
  - state_sync
  
language: go
version: all
---

## References
- [h-2-dirty-evm-state-changes-are-not-committed-before-precompile-calls-resulting-.md](../../../reports/cosmos_cometbft_findings/h-2-dirty-evm-state-changes-are-not-committed-before-precompile-calls-resulting-.md)
- [m-29-stateful-precompiles-panic-on-empty-calldata-which-can-be-exploited-to-prev.md](../../../reports/cosmos_cometbft_findings/m-29-stateful-precompiles-panic-on-empty-calldata-which-can-be-exploited-to-prev.md)
- [delegatecall-to-staking-precompile-allows-theft-of-all-staked-mon.md](../../../reports/cosmos_cometbft_findings/delegatecall-to-staking-precompile-allows-theft-of-all-staked-mon.md)
- [h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md](../../../reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md)
- [h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md](../../../reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md)

## Vulnerability Title

**EVM Precompile Security Vulnerabilities in Cosmos SDK Appchains**

### Overview

Cosmos SDK appchains with EVM integration (Ethermint, Evmos, custom implementations) expose native Cosmos SDK functionality through EVM precompiles. These precompiles frequently contain critical vulnerabilities: delegatecall allowing theft of staked funds by reusing msg.value, dirty EVM state not committed before Cosmos operations enabling double-spending, panics on empty calldata causing transaction failures, and hook exploitation for denial of service. These issues can lead to complete fund theft, double-spending, or chain halt.

### Vulnerability Description

#### Root Cause

The fundamental issues arise from:
1. **DELEGATECALL not blocked**: State-changing precompiles accept delegatecall, reusing msg.value/msg.sender from caller context
2. **Dirty state not committed**: EVM state changes before precompile call not written to Cosmos state
3. **Missing calldata validation**: Precompiles assume at least 4 bytes (function selector), panic on shorter input
4. **Hook exploitation**: Bank module hooks (BlockBeforeSend) can execute arbitrary logic during precompile token transfers
5. **Hardcoded gas limits**: Fixed gas for internal calls bypasses 63/64 rule, enables infinite recursion

#### Attack Scenario

**Scenario 1: Delegatecall Fund Theft**
1. Attacker deploys malicious contract that receives native tokens
2. User sends tokens to malicious contract thinking it's safe
3. Malicious contract delegatecalls staking precompile with msg.value
4. Precompile records user's stake but tokens stay in malicious contract
5. Attacker withdraws from staking precompile (recorded stake)
6. Attacker also keeps tokens in malicious contract - double spend!

**Scenario 2: Double-Spend via Dirty State**
1. Contract holds 100 ZETA tokens
2. Contract transfers 100 ZETA to recipient (EVM state dirty, not committed)
3. Contract immediately calls staking precompile to stake 100 ZETA
4. Precompile reads Cosmos state (still shows 100 ZETA balance)
5. Staking succeeds - 100 ZETA staked
6. EVM execution ends, dirty transfer committed
7. Total: 200 ZETA spent with only 100 ZETA balance

**Scenario 3: Outbound CCTX Stuck via Empty Calldata**
1. Cross-chain transaction targets precompile address
2. Transaction includes empty calldata (0 bytes)
3. Precompile panics trying to read 4-byte function selector
4. Panic propagates to Cosmos SDK, message fails
5. Cross-chain transaction remains pending indefinitely

#### Vulnerable Pattern Examples

**Example 1: Delegatecall Not Blocked** [Approx Severity: CRITICAL]
```cpp
// ❌ VULNERABLE: No check for EVMC message kind
Result<byte_string> StakingContract::precompile_delegate(
    byte_string_view const input, 
    evmc_address const &msg_sender,  // Inherited from delegatecall!
    evmc_uint256be const &msg_value) // Reused from original call!
{
    // msg_value is reused without actual transfer to precompile
    // Attacker's contract keeps tokens but stake is recorded
    
    // Records stake based on msg_value
    state_.set_storage(STAKING_CONTRACT_ADDRESS, 
        user_stake_key(msg_sender), msg_value);
    
    // User can withdraw from staking = double the tokens!
}
```

**Example 2: Dirty EVM State Not Committed** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: EVM state changes not committed before Cosmos action
func (c *Contract) Stake(ctx sdk.Context, evm *vm.EVM, 
    contract *vm.Contract, method *abi.Method, args []interface{},
) ([]byte, error) {
    stakerAddress := contract.Caller()
    amount := args[0].(*big.Int)
    
    // At this point, EVM statedb may have "dirty" (uncommitted) changes
    // e.g., user transferred tokens in Solidity before calling this
    
    // Cosmos SDK reads OLD bank balance (dirty changes not visible!)
    err := c.stakingKeeper.Delegate(ctx, 
        sdk.AccAddress(stakerAddress.Bytes()), 
        sdk.NewIntFromBigInt(amount), validatorAddr)
    
    // SubBalance on EVM side doesn't check for underflow!
    stateDB := evm.StateDB.(precompiletypes.ExtStateDB)
    stateDB.SubBalance(stakerAddress, uint256.NewInt(amount.Uint64()))
    // ❌ No underflow check - if dirty transfer already spent tokens,
    // this subtraction may underflow or conflict
    
    return method.Outputs.Pack(true)
}
```

**Example 3: Panic on Empty Calldata** [Approx Severity: MEDIUM]
```go
// ❌ VULNERABLE: Assumes input is at least 4 bytes
func (c *Contract) RequiredGas(input []byte) uint64 {
    var methodID [4]byte
    copy(methodID[:], input[:4]) // ❌ PANIC if len(input) < 4!
    
    method, err := BankABI.MethodById(methodID[:])
    if err != nil {
        return 0
    }
    return GasConfig[method.Name]
}

func (c *Contract) Run(evm *vm.EVM, contract *vm.Contract, 
    readOnly bool) ([]byte, error) {
    methodID := contract.Input[:4] // ❌ PANIC if len(Input) < 4!
    
    method, err := BankABI.MethodById(methodID)
    // ...
}
```

**Example 4: BlockBeforeSend Hook Exploitation** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: Hook called during precompile token transfer
func (k Keeper) BlockBeforeSend(ctx sdk.Context, from, to sdk.AccAddress, 
    amt sdk.Coins) error {
    
    // Attacker sets malicious hook that:
    // 1. Reverts to block all token transfers
    // 2. Consumes excessive gas
    // 3. Modifies state in unexpected ways
    
    hook, found := k.GetHook(ctx, amt.GetDenomByIndex(0))
    if found {
        // Executes arbitrary CosmWasm/EVM code during bank transfer!
        return k.executeHook(ctx, hook, from, to, amt)
    }
    return nil
}
```

### Impact Analysis

#### Technical Impact
- Complete theft of staked funds via delegatecall
- Double-spending of native tokens
- Denial of service from panics
- Chain halt from infinite recursion
- Cross-chain transactions stuck indefinitely

#### Business Impact
- All staked funds at risk of theft
- Token economics broken by double-spend
- Network unavailability during attacks
- Cross-chain bridge failures
- Loss of user confidence in security

#### Affected Scenarios
- Any EVM chain with staking precompiles
- Cross-chain protocols using precompiles
- Bank/token precompiles with hooks
- Any stateful precompile accepting native tokens
- CCTX finalization targeting precompiles

### Secure Implementation

**Fix 1: Enforce EVMC_CALL for State-Changing Precompiles**
```cpp
// ✅ SECURE: Block delegatecall and staticcall for state changes
Result<byte_string> StakingContract::precompile_delegate(
    evmc_message const &msg,  // Full message with kind
    byte_string_view const input)
{
    // Enforce CALL only - block DELEGATECALL and CALLCODE
    if (msg.kind != EVMC_CALL) {
        return Result<byte_string>::err(
            "State-changing precompile requires CALL");
    }
    
    // Also check not STATICCALL for state changes
    if (msg.flags & EVMC_STATIC) {
        return Result<byte_string>::err(
            "Cannot modify state in static context");
    }
    
    // Now safe to use msg.sender and msg.value
    // They are from direct caller, not inherited
}
```

**Fix 2: Commit EVM State Before Cosmos Operations**
```go
// ✅ SECURE: Commit dirty state before Cosmos SDK calls
func (c *Contract) Stake(ctx sdk.Context, evm *vm.EVM, 
    contract *vm.Contract, method *abi.Method, args []interface{},
) ([]byte, error) {
    stakerAddress := contract.Caller()
    amount := args[0].(*big.Int)
    
    // Commit current EVM state changes to Cosmos state FIRST
    stateDB := evm.StateDB.(precompiletypes.ExtStateDB)
    if err := stateDB.Commit(); err != nil {
        return nil, err
    }
    
    // Verify balance in committed state
    balance := stateDB.GetBalance(stakerAddress)
    amountU256 := uint256.MustFromBig(amount)
    if balance.Cmp(amountU256) < 0 {
        return nil, errors.New("insufficient balance")
    }
    
    // Now Cosmos SDK sees correct, committed state
    err := c.stakingKeeper.Delegate(ctx, ...)
    
    // Subtract with underflow check
    if err := stateDB.SubBalanceWithCheck(stakerAddress, amountU256); err != nil {
        return nil, err
    }
}
```

**Fix 3: Validate Calldata Length Before Access**
```go
// ✅ SECURE: Check calldata length before reading
func (c *Contract) RequiredGas(input []byte) uint64 {
    if len(input) < 4 {
        return 0 // Return 0 gas for invalid input
    }
    
    var methodID [4]byte
    copy(methodID[:], input[:4])
    
    method, err := BankABI.MethodById(methodID[:])
    if err != nil {
        return 0
    }
    return GasConfig[method.Name]
}

func (c *Contract) Run(evm *vm.EVM, contract *vm.Contract, 
    readOnly bool) ([]byte, error) {
    if len(contract.Input) < 4 {
        return nil, errors.New("calldata too short")
    }
    
    methodID := contract.Input[:4]
    // ...
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: Precompile using msg.sender/msg.value without EVMC kind check
- Pattern 2: Cosmos SDK calls before EVM statedb commit
- Pattern 3: `input[:4]` without length validation
- Pattern 4: Bank hooks called during precompile transfers
- Pattern 5: `SubBalance` without overflow/underflow check
```

#### Audit Checklist
- [ ] State-changing precompiles reject DELEGATECALL and CALLCODE
- [ ] State-changing precompiles check EVMC_STATIC flag
- [ ] EVM state committed before Cosmos SDK operations
- [ ] SubBalance includes underflow check
- [ ] Calldata length validated before access
- [ ] Bank hooks bounded in gas and functionality
- [ ] Internal EVM calls respect 63/64 gas rule

### Real-World Examples

| Protocol | Audit Firm | Severity | Issue |
|----------|------------|----------|-------|
| Monad | Spearbit | CRITICAL | Delegatecall to staking precompile allows theft |
| ZetaChain | Sherlock | HIGH | Dirty EVM state enables double-spending |
| ZetaChain | Sherlock | MEDIUM | Empty calldata panic blocks CCTXs |
| Nibiru | Code4rena | HIGH | Hardcoded gas enables infinite recursion |
| Nibiru | Code4rena | HIGH | BlockBeforeSend hook DoS |

### Keywords for Search

`precompile, delegatecall, EVMC_CALL, EVMC_DELEGATECALL, msg.value, msg.sender, statedb, dirty_state, commit, SubBalance, calldata, RequiredGas, Run, panic, BlockBeforeSend, hook, staking_precompile, double_spend, fund_theft`
