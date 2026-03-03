---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: evm
vulnerability_type: evm_gas_handling_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - missing_intrinsic_gas
  - gas_refund_incorrect
  - stack_overflow_no_gas
  - precompile_gas_hardcode
  - gas_not_consumed_on_error
  - cross_vm_gas_mismatch
  - explicit_gas_limit_bypass
  - transaction_gas_vs_block

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - evm
  - EVM_gas
  - gas_metering
  - intrinsic_gas
  - gas_refund
  - stack_overflow
  - precompile_gas
  - Cosmos_EVM
  - gas_consumption
  
language: go
version: all
---

## References
- [antehandler-skipped-in-non-checktx-mode.md](../../../../reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md)
- [h-05-minievm-fails-to-charge-intrinsic-gas-costs-for-evm-transactions-allowing-t.md](../../../../reports/cosmos_cometbft_findings/h-05-minievm-fails-to-charge-intrinsic-gas-costs-for-evm-transactions-allowing-t.md)

## Vulnerability Title

**EVM Gas Handling and Metering Vulnerabilities in Cosmos Chains**

### Overview

This entry documents 2 distinct vulnerability patterns extracted from 2 audit reports (2 HIGH, 0 MEDIUM severity) across 2 protocols by 2 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Gas Not Consumed On Error

**Frequency**: 1/2 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Sei EVM

The Cosmos AnteHandlers are used to check the validity of transactions and prevent malicious transactions from being executed. However, some of the validators are skipped when not in CheckTx mode, allowing attackers to insert malformed transactions into block proposals. This can lead to incorrect ex

**Example 1.1** [HIGH] — Sei EVM
Source: `antehandler-skipped-in-non-checktx-mode.md`
```solidity
// ❌ VULNERABLE: Gas Not Consumed On Error
// sei-tendermint/internal/mempool/mempool.go
func (fc EVMFeeCheckDecorator) AnteHandle(ctx sdk.Context, tx sdk.Tx, simulate bool, next sdk.AnteHandler) (sdk.Context, error) {
    // Only check fee in CheckTx (similar to normal Sei tx)
    if !ctx.IsCheckTx() || simulate {
        return next(ctx, tx, simulate)
    }
    [...]
    anteCharge := txData.Cost()
    senderEVMAddr := evmtypes.MustGetEVMTransactionMessage(tx).Derived.SenderEVMAddr
    if state.NewDBImpl(ctx, fc.evmKeeper, true).GetBalance(senderEVMAddr).Cmp(anteCharge) < 0 {
        return ctx, sdkerrors.ErrInsufficientFunds
    }
    [...]
}
```

#### Pattern 2: Missing Intrinsic Gas

**Frequency**: 1/2 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Initia

The minievm, a program used for Ethereum Virtual Machine (EVM) transactions, fails to charge the proper amount of gas for certain operations, which can lead to a significant risk of denial of service (DoS) attacks. This is due to a lack of charging for intrinsic gas costs, which are considered neces

**Example 2.1** [HIGH] — Initia
Source: `h-05-minievm-fails-to-charge-intrinsic-gas-costs-for-evm-transactions-allowing-t.md`
```solidity
// ❌ VULNERABLE: Missing Intrinsic Gas
> ctx.GasMeter().ConsumeGas(params.TxSizeCostPerByte*storetypes.Gas(len(ctx.TxBytes())), "txSize")
>
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 2 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 2
- HIGH severity: 2 (100%)
- MEDIUM severity: 0 (0%)
- Unique protocols affected: 2
- Independent audit firms: 2
- Patterns with 3+ auditor validation (Strong): 0

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

> `EVM-gas`, `gas-metering`, `intrinsic-gas`, `gas-refund`, `stack-overflow`, `precompile-gas`, `Cosmos-EVM`, `gas-consumption`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
