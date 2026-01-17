---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: gas_metering
vulnerability_type: gas_manipulation

# Attack Vector Details
attack_type: resource_exhaustion
affected_component: evm_gas_metering

# Technical Primitives
primitives:
  - gas_meter
  - intrinsic_gas
  - evm_execution
  - ante_handler
  - precompiles
  - accesslist

# Impact Classification
severity: high
impact: denial_of_service
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - evm
  - ethermint
  - gas
  - dos
  - chain_halt
  
language: go
version: all
---

## References
- [h-05-minievm-fails-to-charge-intrinsic-gas-costs-for-evm-transactions-allowing-t.md](../../../reports/cosmos_cometbft_findings/h-05-minievm-fails-to-charge-intrinsic-gas-costs-for-evm-transactions-allowing-t.md)
- [h-07-evm-stack-overflow-error-leads-to-no-gas-being-charged-which-can-be-exploit.md](../../../reports/cosmos_cometbft_findings/h-07-evm-stack-overflow-error-leads-to-no-gas-being-charged-which-can-be-exploit.md)
- [m-10-a-single-malicious-observer-can-exploit-the-infinite-gas-meter-to-grief-zet.md](../../../reports/cosmos_cometbft_findings/m-10-a-single-malicious-observer-can-exploit-the-infinite-gas-meter-to-grief-zet.md)
- [m-04-gas-refunds-use-block-gas-instead-of-transaction-gas-leading-to-incorrect-r.md](../../../reports/cosmos_cometbft_findings/m-04-gas-refunds-use-block-gas-instead-of-transaction-gas-leading-to-incorrect-r.md)
- [h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md](../../../reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md)

## Vulnerability Title

**EVM Gas Metering Bypass in Cosmos SDK Appchains Enables DoS Attacks**

### Overview

Cosmos SDK appchains integrating EVM functionality (via Ethermint, MiniEVM, or similar) often have incorrect gas metering between the Cosmos SDK and EVM execution contexts. Missing intrinsic gas charges, infinite gas meters for privileged messages, incorrect refund calculations, and hardcoded gas limits in precompiles can all be exploited for denial of service attacks or to abuse computational resources without proper compensation.

### Vulnerability Description

#### Root Cause

The fundamental issues arise from:
1. **Missing intrinsic gas charges**: EIP-2930 access list costs not being charged upfront
2. **Infinite gas meters**: Privileged message types using unbounded gas, exploitable via message bundling
3. **Stack overflow gas bypass**: EVM errors like stack overflow returning `gasRemaining=0` without charging
4. **Hardcoded gas limits**: Precompile EVM calls using fixed gas regardless of available transaction gas
5. **Block vs transaction gas**: Refund calculations using cumulative block gas instead of individual transaction gas

#### Attack Scenario

**Scenario 1: Access List Exploitation**
1. Attacker crafts EVM transaction with large access list (many contract addresses)
2. Normal cost should be 2600 gas per cold access, but only tx byte cost (~300 gas) is charged
3. Attacker gets 2300 gas worth of computation for free per access list entry
4. Repeated abuse allows consuming network resources without proper compensation

**Scenario 2: Infinite Gas Meter Abuse**
1. Attacker bundles expensive messages with privileged message type (e.g., `MsgGasPriceVoter`)
2. Ante handler detects privileged message and switches to infinite gas meter
3. All messages in transaction execute without gas limits
4. Block space filled with spam, preventing legitimate transactions

**Scenario 3: Precompile Recursion**
1. Attacker deploys contract that calls precompile with hardcoded 100,000 gas
2. Precompile calls back into EVM with another hardcoded gas amount
3. Infinite recursion possible as 63/64 rule is bypassed
4. Validators crash, block production halts

#### Vulnerable Pattern Examples

**Example 1: Missing Intrinsic Gas Charge** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: No intrinsic gas charged for access list
func (k *Keeper) EVMCallWithTracer(
    ctx sdk.Context,
    caller common.Address,
    contract *common.Address,
    input []byte,
    value *big.Int,
    gas uint64,
    accessList types.AccessList, // Access list not charged!
) (*types.MsgEthereumTxResponse, error) {
    // Access list entries should cost 2400 gas each (EIP-2930)
    // But they are processed without charging intrinsic gas
    evm := k.NewEVM(ctx, caller, tracer)
    ret, gasRemaining, err := evm.Call(caller, *contract, input, gas, value)
    // Gas charged only AFTER execution, missing intrinsic costs
}
```

**Example 2: Infinite Gas Meter for Bundled Messages** [Approx Severity: MEDIUM]
```go
// ❌ VULNERABLE: Infinite gas if ANY message is privileged
func NewAnteHandler(options HandlerOptions) (sdk.AnteHandler, error) {
    return func(ctx sdk.Context, tx sdk.Tx, simulate bool) (sdk.Context, error) {
        found := false
        for _, msg := range tx.GetMsgs() {
            switch msg.(type) {
            case *cctxtypes.MsgGasPriceVoter, *cctxtypes.MsgVoteOnObservedInboundTx:
                found = true
                break // Found one privileged message
            }
        }
        if found {
            // ALL messages get infinite gas, not just privileged ones!
            return newCosmosAnteHandlerNoGasLimit(options)
        }
        return newCosmosAnteHandler(options)
    }
}
```

**Example 3: Hardcoded Gas in Precompile Calls** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: Fixed gas allows 63/64 rule bypass
const Erc20GasLimitQuery = 100_000 // Hardcoded!

func (k Keeper) LoadERC20BigInt(ctx sdk.Context, contract common.Address) (*big.Int, error) {
    res, err := k.CallContract(
        ctx,
        abi,
        evm.EVM_MODULE_ADDRESS,
        &contract,
        false,
        Erc20GasLimitQuery, // Always 100_000 regardless of caller's gas
        "balanceOf",
    )
    // Enables infinite recursion - each call gets fresh 100k gas
}
```

**Example 4: Stack Overflow Gas Bypass** [Approx Severity: HIGH]
```go
// ❌ VULNERABLE: No gas charged on stack overflow
func (k *Keeper) EVMCallWithTracer(...) (*Response, error) {
    ret, gasRemaining, err := evm.Call(...)
    
    // Stack overflow returns gasRemaining=0 but err != ErrOutOfGas
    if gasRemaining == 0 && err != nil && err != vm.ErrOutOfGas {
        return nil, types.ErrEVMCallFailed.Wrap(err.Error())
        // Returns error WITHOUT consuming gas from gas meter!
    }
    
    // Dispatched calls via CosmosPrecompile exploit this
    // No gas charged = free computation
}
```

### Impact Analysis

#### Technical Impact
- Block production halted from infinite recursion or resource exhaustion
- Validators slashed for missing blocks
- Chain state corruption from inconsistent gas accounting
- Block gas meter inaccurate, affecting fee market

#### Business Impact
- Complete service unavailability during attacks
- Validator operational costs increased from spam
- Users unable to process transactions
- Network reputation damage

#### Affected Scenarios
- Any Cosmos chain with EVM integration (Ethermint, MiniEVM, Evmos forks)
- Chains with privileged message types using special gas handling
- Precompiles that make EVM calls with hardcoded gas
- Observer/validator networks with special transaction handling

### Secure Implementation

**Fix 1: Charge Intrinsic Gas Including Access List**
```go
// ✅ SECURE: Charge intrinsic gas before execution
func (k *Keeper) EVMCallWithTracer(
    ctx sdk.Context,
    msg *types.MsgEthereumTx,
) (*types.MsgEthereumTxResponse, error) {
    // Calculate intrinsic gas per EIP-2930
    intrinsicGas := IntrinsicGas(msg.Data, msg.AccessList, msg.To == nil)
    
    // Charge upfront
    if err := k.ConsumeGas(ctx, intrinsicGas, "intrinsic"); err != nil {
        return nil, err
    }
    
    // Now execute with remaining gas
    remainingGas := msg.Gas - intrinsicGas
    ret, gasRemaining, err := evm.Call(..., remainingGas, ...)
}
```

**Fix 2: Check ALL Messages for Infinite Gas**
```go
// ✅ SECURE: Only use infinite gas if ALL messages are privileged
func NewAnteHandler(options HandlerOptions) (sdk.AnteHandler, error) {
    return func(ctx sdk.Context, tx sdk.Tx, simulate bool) (sdk.Context, error) {
        allPrivileged := true
        for _, msg := range tx.GetMsgs() {
            switch msg.(type) {
            case *cctxtypes.MsgGasPriceVoter, *cctxtypes.MsgVoteOnObservedInboundTx:
                // This message is privileged
            default:
                allPrivileged = false
                break
            }
        }
        if allPrivileged {
            return newCosmosAnteHandlerNoGasLimit(options)
        }
        return newCosmosAnteHandler(options) // Normal gas limits
    }
}
```

**Fix 3: Use Caller's Gas with 63/64 Rule**
```go
// ✅ SECURE: Respect EIP-150 63/64 gas rule
func (p precompileFunToken) balance(contract *vm.Contract) ([]byte, error) {
    // Calculate max gas as 63/64 of available gas
    availableGas := contract.Gas
    maxGas := availableGas - availableGas/64
    
    erc20Bal, err := p.evmKeeper.ERC20().BalanceOf(
        funtoken.Erc20Addr.Address,
        addrEth,
        ctx,
        maxGas, // Use dynamic gas limit
    )
    return erc20Bal, err
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `Erc20GasLimitQuery` or similar hardcoded gas constants
- Pattern 2: `newCosmosAnteHandlerNoGasLimit` with partial message checks
- Pattern 3: EVM calls without `IntrinsicGas()` charging
- Pattern 4: `gasRemaining == 0 && err != ErrOutOfGas` returning without gas consumption
- Pattern 5: `ctx.GasMeter().ConsumeGas()` called AFTER EVM execution
```

#### Audit Checklist
- [ ] Intrinsic gas charged before EVM execution
- [ ] Access list costs properly accounted (2400 gas per entry)
- [ ] Infinite gas meters only apply to ALL messages, not mixed transactions
- [ ] Precompile EVM calls respect 63/64 gas forwarding rule
- [ ] All EVM error paths consume appropriate gas
- [ ] Gas refunds use per-transaction gas, not block gas

### Real-World Examples

| Protocol | Audit Firm | Severity | Issue |
|----------|------------|----------|-------|
| Initia MiniEVM | Code4rena | HIGH | Missing intrinsic gas for access list |
| Initia MiniEVM | Code4rena | HIGH | Stack overflow returns without gas charge |
| ZetaChain | Code4rena | MEDIUM | Infinite gas meter exploitable via bundling |
| Nibiru | Code4rena | MEDIUM | Gas refunds use block gas not tx gas |
| Nibiru | Code4rena | HIGH | Hardcoded gas in precompile causes halt |

### Keywords for Search

`intrinsic_gas, access_list, EIP2930, infinite_gas_meter, gas_refund, block_gas, transaction_gas, stack_overflow, ErrOutOfGas, precompile_gas, hardcoded_gas, gas_limit, DoS, chain_halt, ante_handler, gas_metering, EVM_gas`
