---
protocol: generic
chain: cosmos
category: evm
vulnerability_type: evm_gas_handling_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: evm_logic

primitives:
  - intrinsic_gas_missing
  - gas_refund_error
  - precompile_gas_hardcode
  - gas_not_consumed_error
  - gas_mismatch_call

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - evm
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: denial_of_service
pattern_key: denial_of_service | evm_logic | evm_gas_handling_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - AnteHandle
  - balance
  - gas_mismatch_call
  - gas_not_consumed_error
  - gas_refund_error
  - intrinsic_gas_missing
  - malicious
  - mint
  - precompile_gas_hardcode
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Evm Intrinsic Gas Missing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-05] Minievm fails to charge intrinsic gas costs for EVM t | `reports/cosmos_cometbft_findings/h-05-minievm-fails-to-charge-intrinsic-gas-costs-for-evm-transactions-allowing-t.md` | HIGH | Code4rena |

### Evm Gas Refund Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-04] Gas refunds use block gas instead of transaction gas, | `reports/cosmos_cometbft_findings/m-04-gas-refunds-use-block-gas-instead-of-transaction-gas-leading-to-incorrect-r.md` | MEDIUM | Code4rena |

### Evm Precompile Gas Hardcode
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-06] Hardcoded gas used in ERC20 queries allows for block  | `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md` | HIGH | Code4rena |
| [M-03] Gas used mismatch in failed contract calls can lead t | `reports/cosmos_cometbft_findings/m-03-gas-used-mismatch-in-failed-contract-calls-can-lead-to-wrong-gas-deductions.md` | MEDIUM | Code4rena |

### Evm Gas Not Consumed Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| AnteHandler Skipped In Non-CheckTx Mode | `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md` | HIGH | OtterSec |
| [H-04] Gas is not consumed when precompile method fail, allo | `reports/cosmos_cometbft_findings/h-04-gas-is-not-consumed-when-precompile-method-fail-allowing-resource-consumpti.md` | HIGH | Code4rena |
| [H-07] EVM stack overflow error leads to no gas being charge | `reports/cosmos_cometbft_findings/h-07-evm-stack-overflow-error-leads-to-no-gas-being-charged-which-can-be-exploit.md` | HIGH | Code4rena |
| [M-03] Gas used mismatch in failed contract calls can lead t | `reports/cosmos_cometbft_findings/m-03-gas-used-mismatch-in-failed-contract-calls-can-lead-to-wrong-gas-deductions.md` | MEDIUM | Code4rena |

### Evm Gas Mismatch Call
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-03] Gas used mismatch in failed contract calls can lead t | `reports/cosmos_cometbft_findings/m-03-gas-used-mismatch-in-failed-contract-calls-can-lead-to-wrong-gas-deductions.md` | MEDIUM | Code4rena |

---

# Evm Gas Handling Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Evm Gas Handling Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Evm Intrinsic Gas Missing](#1-evm-intrinsic-gas-missing)
2. [Evm Gas Refund Error](#2-evm-gas-refund-error)
3. [Evm Precompile Gas Hardcode](#3-evm-precompile-gas-hardcode)
4. [Evm Gas Not Consumed Error](#4-evm-gas-not-consumed-error)
5. [Evm Gas Mismatch Call](#5-evm-gas-mismatch-call)

---

## 1. Evm Intrinsic Gas Missing

### Overview

Implementation flaw in evm intrinsic gas missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: The minievm, a program used for Ethereum Virtual Machine (EVM) transactions, fails to charge the proper amount of gas for certain operations, which can lead to a significant risk of denial of service (DoS) attacks. This is due to a lack of charging for intrinsic gas costs, which are considered neces



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of denial_of_service"
- Pattern key: `denial_of_service | evm_logic | evm_gas_handling_vulnerabilities`
- Interaction scope: `single_contract`
- Primary affected component(s): `evm_logic`
- High-signal code keywords: `AnteHandle`, `balance`, `gas_mismatch_call`, `gas_not_consumed_error`, `gas_refund_error`, `intrinsic_gas_missing`, `malicious`, `mint`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Unbounded loop over user-controlled array can exceed block gas limit
- Signal 2: External call failure causes entire transaction to revert
- Signal 3: Attacker can grief operations by manipulating state to cause reverts
- Signal 4: Resource exhaustion through repeated operations without rate limiting

#### False Positive Guards

- Not this bug when: Loop iterations are bounded by a reasonable constant
- Safe if: External call failures are handled gracefully (try/catch or pull pattern)
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Implementation flaw in evm intrinsic gas missing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm intrinsic gas missing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: [H-05] Minievm fails to charge intrinsic gas costs for EVM transactions, allowin** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-05-minievm-fails-to-charge-intrinsic-gas-costs-for-evm-transactions-allowing-t.md`
```go
> ctx.GasMeter().ConsumeGas(params.TxSizeCostPerByte*storetypes.Gas(len(ctx.TxBytes())), "txSize")
>
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm intrinsic gas missing logic allows exploitation through missing validatio
func secureEvmIntrinsicGasMissing(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: HIGH: 1
- **Affected Protocols**: Initia
- **Validation Strength**: Single auditor

---

## 2. Evm Gas Refund Error

### Overview

Implementation flaw in evm gas refund error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The report highlights a mismatch in the EVM implementation where gas fees are deducted upfront based on each transaction's individual gas limit, but the refund calculation uses the cumulative block gas usage. This results in users receiving incorrect (lower) refunds than they should, causing them to

### Vulnerability Description

#### Root Cause

Implementation flaw in evm gas refund error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm gas refund error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: [M-04] Gas refunds use block gas instead of transaction gas, leading to incorrec** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-gas-refunds-use-block-gas-instead-of-transaction-gas-leading-to-incorrect-r.md`
```go
// https://github.com/code-423n4/2024-11-nibiru/blob/84054a4f00fdfefaa8e5849c53eb66851a762319/app/evmante/evmante_gas_consume.go#L100-L105
		fees, err := keeper.VerifyFee(
			txData,
			evm.EVMBankDenom,
			baseFeeMicronibiPerGas,
			ctx.IsCheckTx(),
		)
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm gas refund error logic allows exploitation through missing validation, in
func secureEvmGasRefundError(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Nibiru
- **Validation Strength**: Single auditor

---

## 3. Evm Precompile Gas Hardcode

### Overview

Implementation flaw in evm precompile gas hardcode logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: This bug report describes a vulnerability in the `funtoken` precompile code, which allows an EVM caller to access information about tokens in the Cosmos and EVM spaces. The vulnerability lies in the `balance` and `sendToBank` methods, which make calls to the `evmKeeper.ERC20().BalanceOf` and `evmKee

### Vulnerability Description

#### Root Cause

Implementation flaw in evm precompile gas hardcode logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm precompile gas hardcode in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: [H-06] Hardcoded gas used in ERC20 queries allows for block production halt from** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md`
```go
File: funtoken.go
265: func (p precompileFunToken) balance(
266: 	start OnRunStartResult,
267: 	contract *vm.Contract,
268: ) (bz []byte, err error) {
---
285: 	erc20Bal, err := p.evmKeeper.ERC20().BalanceOf(funtoken.Erc20Addr.Address, addrEth, ctx)
286: 	if err != nil {
287: 		return
288: 	}
```

**Example 2: [M-03] Gas used mismatch in failed contract calls can lead to wrong gas deductio** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-gas-used-mismatch-in-failed-contract-calls-can-lead-to-wrong-gas-deductions.md`
```go
if evmResp.Failed() {
    k.ResetGasMeterAndConsumeGas(ctx, evmResp.GasUsed) // Only consumes gas for this tx
    // ... error handling
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm precompile gas hardcode logic allows exploitation through missing validat
func secureEvmPrecompileGasHardcode(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 1
- **Affected Protocols**: Nibiru
- **Validation Strength**: Single auditor

---

## 4. Evm Gas Not Consumed Error

### Overview

Implementation flaw in evm gas not consumed error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 3, MEDIUM: 1.

> **Key Finding**: The Cosmos AnteHandlers are used to check the validity of transactions and prevent malicious transactions from being executed. However, some of the validators are skipped when not in CheckTx mode, allowing attackers to insert malformed transactions into block proposals. This can lead to incorrect ex

### Vulnerability Description

#### Root Cause

Implementation flaw in evm gas not consumed error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm gas not consumed error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: AnteHandler Skipped In Non-CheckTx Mode** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/antehandler-skipped-in-non-checktx-mode.md`
```go
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

**Example 2: [H-04] Gas is not consumed when precompile method fail, allowing resource consum** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-gas-is-not-consumed-when-precompile-method-fail-allowing-resource-consumpti.md`
```go
if err != nil {
    return nil, err
}

// Gas consumed by a local gas meter
contract.UseGas(startResult.CacheCtx.GasMeter().GasConsumed())
```

**Example 3: [H-07] EVM stack overflow error leads to no gas being charged, which can be expl** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-07-evm-stack-overflow-error-leads-to-no-gas-being-charged-which-can-be-exploit.md`
```go
// evm sometimes return 0 gasRemaining, but it's not an out of gas error.
if gasRemaining == 0 && err != nil && err != vm.ErrOutOfGas {
	return nil, common.Address{}, nil, types.ErrEVMCreateFailed.Wrap(err.Error())
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm gas not consumed error logic allows exploitation through missing validati
func secureEvmGasNotConsumedError(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: HIGH: 3, MEDIUM: 1
- **Affected Protocols**: Nibiru, Sei EVM, Initia
- **Validation Strength**: Moderate (2 auditors)

---

## 5. Evm Gas Mismatch Call

### Overview

Implementation flaw in evm gas mismatch call logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: There is a bug in the code that handles failed contract calls in `call_contract.go`. The code only consumes gas for the failed transaction, but does not account for previously accumulated block gas usage. This means that the actual gas used in the block may not match what is consumed in the gas mete

### Vulnerability Description

#### Root Cause

Implementation flaw in evm gas mismatch call logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies evm gas mismatch call in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to evm operations

### Vulnerable Pattern Examples

**Example 1: [M-03] Gas used mismatch in failed contract calls can lead to wrong gas deductio** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-gas-used-mismatch-in-failed-contract-calls-can-lead-to-wrong-gas-deductions.md`
```go
if evmResp.Failed() {
    k.ResetGasMeterAndConsumeGas(ctx, evmResp.GasUsed) // Only consumes gas for this tx
    // ... error handling
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in evm gas mismatch call logic allows exploitation through missing validation, i
func secureEvmGasMismatchCall(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Nibiru
- **Validation Strength**: Single auditor

---

## Detection Patterns

### Automated Detection
```
# Evm Intrinsic Gas Missing
grep -rn 'evm|intrinsic|gas|missing' --include='*.go' --include='*.sol'
# Evm Gas Refund Error
grep -rn 'evm|gas|refund|error' --include='*.go' --include='*.sol'
# Evm Precompile Gas Hardcode
grep -rn 'evm|precompile|gas|hardcode' --include='*.go' --include='*.sol'
# Evm Gas Not Consumed Error
grep -rn 'evm|gas|not|consumed|error' --include='*.go' --include='*.sol'
# Evm Gas Mismatch Call
grep -rn 'evm|gas|mismatch|call' --include='*.go' --include='*.sol'
```

## Keywords

`abuse`, `accesslist`, `allowing`, `allows`, `amounts`, `antehandler`, `appchain`, `being`, `block`, `call`, `calls`, `chain`, `charge`, `compensation`, `computational`, `consume`, `consumed`, `consumption`, `contract`, `cosmos`, `costs`, `deductions`, `dispatching`, `error`, `evm`, `exploited`, `failed`, `fails`, `from`, `gas`

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`AnteHandle`, `appchain`, `balance`, `cosmos`, `defi`, `evm`, `evm_gas_handling_vulnerabilities`, `gas_mismatch_call`, `gas_not_consumed_error`, `gas_refund_error`, `intrinsic_gas_missing`, `malicious`, `mint`, `precompile_gas_hardcode`, `staking`
