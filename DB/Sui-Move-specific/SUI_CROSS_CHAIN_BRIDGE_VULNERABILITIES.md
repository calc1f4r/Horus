---
# Core Classification (Required)
protocol: generic
chain: sui|zetachain
category: cross_chain_bridge
vulnerability_type: bridge_security|cross_chain_messaging|state_sync|inbound_validation

# Attack Vector Details (Required)
attack_type: state_manipulation|dos|validation_bypass|fund_theft
affected_component: bridge_committee|cctx|gas_price|coin_type|receiver_validation|nonce|evm_state|flow_limiter

# Technical Primitives (Required)
primitives:
  - zetaclient
  - cctx
  - outbound_tx
  - inbound_tx
  - gas_price
  - coin_type
  - receiver_module
  - tss_signer
  - nonce
  - epoch
  - committee
  - blocklist
  - flow_limiter
  - bridge_message
  - axelar_gateway
  - sui_bridge

# Impact Classification (Required)
severity: high
impact: fund_loss|dos|state_corruption|chain_halt
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - sui
  - zetachain
  - axelar
  - bridge
  - cross_chain
  - cctx
  - gas_price
  - tss
  - committee
  - nonce
  - evm
  - go
  - rust

# Version Info
language: go|move|rust
version: all

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | bridge_committee | bridge_security

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - ObserveInTx
  - axelar_gateway
  - blocklist
  - bridge_message
  - burn
  - cctx
  - coin_type
  - committee
  - deposit
  - epoch
  - flow_limiter
  - gas_price
  - inbound_tx
  - nonce
  - outbound_tx
  - receiver_module
  - sui_bridge
  - tss_signer
  - zetaclient
---

## References & Source Reports

> **For Agents**: Read the full report for each finding at the referenced path.

### ZetaChain Sui Integration Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Dirty EVM State Changes Despite Failure | `reports/sui_move_findings/h-2-dirty-evm-state-changes-are-persisted-despite-sui-deposit-failure.md` | HIGH | Sherlock | ZetaChain |
| User DoS via Outbound Nonce | `reports/sui_move_findings/m-1-user-is-able-to-dos-outbound-cctxs-via-nonce-manipulation.md` | MEDIUM | Sherlock | ZetaChain |
| DoSed Sui Node Blocks InTx Observation | `reports/sui_move_findings/m-11-dosed-sui-node-leads-to-not-observing-intxs.md` | MEDIUM | Sherlock | ZetaChain |
| Sui Receiver Lacks Validation | `reports/sui_move_findings/m-12-sui-receiver-lacks-validation.md` | MEDIUM | Sherlock | ZetaChain |
| Zeta Coin Type Validation | `reports/sui_move_findings/m-24-zeta-coin-type-for-sui-is-improperly-validated.md` | MEDIUM | Sherlock | ZetaChain |
| Outbound CCTXs Resigning | `reports/sui_move_findings/m-25-outbound-cctxs-to-sui-are-resigned-even-if-they-have-already-been.md` | MEDIUM | Sherlock | ZetaChain |
| Sui TSS Drained via Gas Manipulation | `reports/sui_move_findings/m-5-sui-tss-can-be-drained-due-to-the-wrong-gas-coin-amount.md` | MEDIUM | Sherlock | ZetaChain |
| Wrong PostGasPrice Usage | `reports/sui_move_findings/m-6-wrong-postgasprice-is-set-for-sui-outbound-transactions.md` | MEDIUM | Sherlock | ZetaChain |

### Sui Bridge / Axelar Vulnerabilities
| Report | Path | Severity | Audit Firm | Protocol |
|--------|------|----------|------------|----------|
| Inability to End Epoch | `reports/sui_move_findings/inability-to-end-an-epoch.md` | HIGH | OtterSec | Sui Bridge |
| Blocklist Validation Order Mismatch | `reports/sui_move_findings/blocklist-validation-order-mismatch.md` | MEDIUM | OtterSec | Sui Bridge |
| Incorrect Flow Tracking | `reports/sui_move_findings/utilization-of-incorrect-flow-tracking.md` | HIGH | OtterSec | Axelar |
| Incorrect Function Call | `reports/sui_move_findings/incorrect-function-call.md` | MEDIUM | OtterSec | Axelar |

### Artifacts Index
| Artifact | Source | Type |
|----------|--------|------|
| `artifacts/6-sherlock-contest-857.html` | ZetaChain Sherlock Contest | HTML |
| `artifacts/13-github.com-axelarnetwork-axelar-cgp-sui-3c5.html` | Axelar CGP Sui GitHub | HTML |

---

# Sui Cross-Chain Bridge Vulnerabilities — Comprehensive Database

**A Complete Pattern-Matching Guide for Cross-Chain Bridge Security on Sui (ZetaChain, Axelar, Sui Bridge)**

---

## Table of Contents

1. [EVM State Persistence Despite Sui Failure](#1-evm-state-persistence-despite-sui-failure)
2. [Outbound Nonce Manipulation DoS](#2-outbound-nonce-manipulation-dos)
3. [Sui Node DoS Blocks InTx Observation](#3-sui-node-dos-blocks-intx-observation)
4. [Missing Receiver Module Validation](#4-missing-receiver-module-validation)
5. [Improper Coin Type Validation](#5-improper-coin-type-validation)
6. [Duplicate CCTX Re-signing](#6-duplicate-cctx-re-signing)
7. [TSS Fund Drainage via Gas Manipulation](#7-tss-fund-drainage-via-gas-manipulation)
8. [Wrong Gas Price for Outbound Transactions](#8-wrong-gas-price-for-outbound-transactions)
9. [Epoch Transition Failure via Duplicate PubKey](#9-epoch-transition-failure-via-duplicate-pubkey)
10. [Blocklist Iterator State Bug](#10-blocklist-iterator-state-bug)
11. [Cross-Chain Flow Rate Direction Mismatch](#11-cross-chain-flow-rate-direction-mismatch)
12. [Wrong Integration Function Call](#12-wrong-integration-function-call)

---

## 1. EVM State Persistence Despite Sui Failure

### Overview

When ZetaChain processes a cross-chain call from EVM → Sui, the EVM state changes (token burns, balance updates) are persisted even when the Sui deposit transaction fails. This creates an inconsistency where tokens are burned on EVM but never minted on Sui.

> **Validation strength**: Strong — 1 HIGH report from Sherlock on ZetaChain
> **Frequency**: 1/69 reports



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | bridge_committee | bridge_security`
- Interaction scope: `multi_contract`
- Primary affected component(s): `bridge_committee|cctx|gas_price|coin_type|receiver_validation|nonce|evm_state|flow_limiter`
- High-signal code keywords: `ObserveInTx`, `axelar_gateway`, `blocklist`, `bridge_message`, `burn`, `cctx`, `coin_type`, `committee`
- Typical sink / impact: `fund_loss|dos|state_corruption|chain_halt`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `bridge_committee.function -> cctx.function -> coin_type.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Critical input parameter not validated against expected range or format
- Signal 2: Oracle data consumed without staleness check or sanity bounds
- Signal 3: User-supplied address or calldata forwarded without validation
- Signal 4: Missing check allows operation under invalid or stale state

#### False Positive Guards

- Not this bug when: Validation exists but is in an upstream function caller
- Safe if: Parameter range is inherently bounded by the type or protocol invariant
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

The EVM side commits state changes before confirming the Sui-side transaction succeeded. When the Sui deposit fails (e.g., due to gas issues, module errors), the EVM changes are already finalized, causing permanent fund loss.

### Vulnerable Pattern Examples

**Example 1: EVM Burns Persisted, Sui Deposit Fails** [HIGH]
> 📖 Reference: `reports/sui_move_findings/h-2-dirty-evm-state-changes-are-persisted-despite-sui-deposit-failure.md`
```go
// ❌ VULNERABLE (Go, zetaclient): EVM state committed before Sui confirmation
func ProcessCrossChainTx(ctx sdk.Context, cctx *types.CrossChainTx) error {
    // Step 1: Apply EVM state changes (burn tokens)
    err := applyEVMChanges(ctx, cctx)
    if err != nil {
        return err
    }
    // EVM changes are now committed to the state
    
    // Step 2: Execute Sui deposit
    err = executeSuiDeposit(ctx, cctx)
    if err != nil {
        // BUG: EVM changes already persisted — tokens burned but not minted
        // Should revert EVM changes, but they're already committed
        return err  // Sui fails but EVM changes remain
    }
    return nil
}
```

### Secure Implementation

```go
// ✅ SECURE: Use two-phase commit or cache-and-commit pattern
func ProcessCrossChainTx(ctx sdk.Context, cctx *types.CrossChainTx) error {
    // Use a cached context — changes only commit if both succeed
    cachedCtx, writeFn := ctx.CacheContext()
    
    // Step 1: Apply EVM state changes in cached context
    err := applyEVMChanges(cachedCtx, cctx)
    if err != nil {
        return err
    }
    
    // Step 2: Execute Sui deposit
    err = executeSuiDeposit(cachedCtx, cctx)
    if err != nil {
        // Cached context discarded — EVM changes NOT persisted
        return err
    }
    
    // Both succeeded — commit all changes atomically
    writeFn()
    return nil
}
```

---

## 2. Outbound Nonce Manipulation DoS

### Overview

Users can manipulate outbound CCTX nonces to block other users' cross-chain transactions. By submitting transactions that consume specific nonces, an attacker prevents legitimate outbound transfers from being processed.

> **Validation strength**: Moderate — 1 MEDIUM report from Sherlock on ZetaChain
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Nonce Consumption Blocks Others** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/m-1-user-is-able-to-dos-outbound-cctxs-via-nonce-manipulation.md`
```go
// ❌ VULNERABLE: Sequential nonce allows targeted blocking
func GetNextOutboundNonce(ctx sdk.Context, chain chains.Chain) uint64 {
    nonce := k.GetOutboundNonce(ctx, chain)
    k.SetOutboundNonce(ctx, chain, nonce+1)
    return nonce
    // If attacker causes nonce N to fail, all subsequent nonces (N+1, N+2, ...) 
    // are blocked until N is resolved
}
```

### Secure Implementation

```go
// ✅ SECURE: Use nonce gap handling or parallel nonce pools
func ProcessOutboundWithRetry(ctx sdk.Context, cctx *types.CrossChainTx) error {
    nonce := GetNextOutboundNonce(ctx, cctx.DestChain)
    cctx.OutboundNonce = nonce
    
    // If this nonce fails, mark it for retry without blocking subsequent nonces
    if err := executeOutbound(ctx, cctx); err != nil {
        k.AddToRetryQueue(ctx, cctx)
        // Don't block subsequent nonces — process them in parallel
        return nil
    }
    return nil
}
```

---

## 3. Sui Node DoS Blocks InTx Observation

### Overview

If the Sui full node used by the zetaclient for transaction observation goes down (DoS), inbound transactions are not observed and cross-chain messages are lost.

> **Validation strength**: Moderate — 1 MEDIUM report from Sherlock on ZetaChain
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Single Node Dependency** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/m-11-dosed-sui-node-leads-to-not-observing-intxs.md`
```go
// ❌ VULNERABLE: Single RPC endpoint, no failover
type SuiObserver struct {
    rpcClient *sui.Client  // Single node — if DoSed, all observation stops
}

func (o *SuiObserver) ObserveInTx(ctx context.Context) error {
    events, err := o.rpcClient.GetEvents(ctx, o.cursor)
    if err != nil {
        return err  // All inbound observation halted
    }
    // ...
}
```

### Secure Implementation

```go
// ✅ SECURE: Multiple RPC endpoints with failover
type SuiObserver struct {
    rpcClients []*sui.Client  // Multiple nodes
    activeIdx  int
}

func (o *SuiObserver) ObserveInTx(ctx context.Context) error {
    var lastErr error
    for i := 0; i < len(o.rpcClients); i++ {
        idx := (o.activeIdx + i) % len(o.rpcClients)
        events, err := o.rpcClients[idx].GetEvents(ctx, o.cursor)
        if err != nil {
            lastErr = err
            continue  // Try next node
        }
        o.activeIdx = idx  // Remember working node
        return o.processEvents(events)
    }
    return fmt.Errorf("all nodes failed: %w", lastErr)
}
```

---

## 4. Missing Receiver Module Validation

### Overview

When sending tokens from ZetaChain to Sui, the receiver address should be validated as a valid Sui address/module. Without validation, tokens sent to invalid addresses are permanently lost.

> **Validation strength**: Moderate — 1 MEDIUM report from Sherlock on ZetaChain
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: No Receiver Address Validation** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/m-12-sui-receiver-lacks-validation.md`
```go
// ❌ VULNERABLE: Receiver not validated before creating outbound CCTX
func CreateOutboundToSui(ctx sdk.Context, receiver string, amount uint64) error {
    // No validation that receiver is a valid Sui address
    // No check that receiver module exists on Sui
    cctx := &types.CrossChainTx{
        Receiver: receiver,  // Could be anything — invalid address = lost funds
        Amount:   amount,
    }
    return k.ProcessOutbound(ctx, cctx)
}
```

### Secure Implementation

```go
// ✅ SECURE: Validate Sui address format before processing
func CreateOutboundToSui(ctx sdk.Context, receiver string, amount uint64) error {
    // Validate Sui address format (32 bytes, hex-encoded with 0x prefix)
    if !isValidSuiAddress(receiver) {
        return fmt.Errorf("invalid Sui receiver address: %s", receiver)
    }
    cctx := &types.CrossChainTx{
        Receiver: receiver,
        Amount:   amount,
    }
    return k.ProcessOutbound(ctx, cctx)
}

func isValidSuiAddress(addr string) bool {
    if !strings.HasPrefix(addr, "0x") {
        return false
    }
    bytes, err := hex.DecodeString(addr[2:])
    return err == nil && len(bytes) == 32
}
```

---

## 5. Improper Coin Type Validation

### Overview

ZetaChain's Sui integration must validate coin types to ensure the correct asset is being transferred. Improper validation allows sending wrong coin types through the bridge.

> **Validation strength**: Moderate — 1 MEDIUM report from Sherlock on ZetaChain
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Coin Type String Not Properly Validated** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/m-24-zeta-coin-type-for-sui-is-improperly-validated.md`
```go
// ❌ VULNERABLE: Partial string match allows coin type spoofing
func ValidateSuiCoinType(coinType string) bool {
    return strings.Contains(coinType, "zeta")
    // "0x...::fake_zeta::ZETA" would pass this check
    // Should validate full type path: package_id::module::struct
}
```

### Secure Implementation

```go
// ✅ SECURE: Validate full coin type path against known registry
func ValidateSuiCoinType(coinType string, expectedPackage string) bool {
    // Full type format: {package_id}::{module}::{struct}
    parts := strings.Split(coinType, "::")
    if len(parts) != 3 {
        return false
    }
    return parts[0] == expectedPackage  // Exact package ID match
}
```

---

## 6. Duplicate CCTX Re-signing

### Overview

Outbound CCTXs that have already been signed by the TSS may be re-signed unnecessarily, wasting gas and potentially creating conflicting transactions on the destination chain.

> **Validation strength**: Moderate — 1 MEDIUM report from Sherlock on ZetaChain
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Already-Signed CCTXs Re-processed** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/m-25-outbound-cctxs-to-sui-are-resigned-even-if-they-have-already-been.md`
```go
// ❌ VULNERABLE: No check for existing signature
func SignOutboundCCTX(ctx sdk.Context, cctx *types.CrossChainTx) error {
    // Missing: if cctx.HasSignature() { return nil }
    signature, err := tss.Sign(cctx.GetSignBytes())
    if err != nil {
        return err
    }
    cctx.OutboundSignature = signature
    // Re-signing wastes TSS resources and can create double-spend risk
    return nil
}
```

### Secure Implementation

```go
// ✅ SECURE: Check for existing signature before re-signing
func SignOutboundCCTX(ctx sdk.Context, cctx *types.CrossChainTx) error {
    if len(cctx.OutboundSignature) > 0 {
        return nil  // Already signed, skip
    }
    signature, err := tss.Sign(cctx.GetSignBytes())
    if err != nil {
        return err
    }
    cctx.OutboundSignature = signature
    return nil
}
```

---

## 7. TSS Fund Drainage via Gas Manipulation

### Overview

The TSS (Threshold Signature Scheme) signer funds gas for outbound Sui transactions. If the gas coin amount calculation is wrong, an attacker can craft transactions that drain the TSS gas fund.

> **Validation strength**: Moderate — 1 MEDIUM report from Sherlock on ZetaChain
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: Wrong Gas Coin Amount** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/m-5-sui-tss-can-be-drained-due-to-the-wrong-gas-coin-amount.md`
```go
// ❌ VULNERABLE: Gas coin amount not properly bounded
func BuildSuiOutbound(cctx *types.CrossChainTx) (*sui.Transaction, error) {
    gasCoin := cctx.GetGasCoin()
    // BUG: gasCoin.Amount not validated against actual gas cost
    // Attacker can set artificially high gas, draining TSS
    tx := sui.NewTransaction(
        sui.WithGasBudget(gasCoin.Amount),  // Unbounded gas budget
        // ...
    )
    return tx, nil
}
```

### Secure Implementation

```go
// ✅ SECURE: Cap gas budget and validate against estimated cost
func BuildSuiOutbound(cctx *types.CrossChainTx) (*sui.Transaction, error) {
    estimatedGas := estimateSuiGas(cctx)
    maxGas := estimatedGas * 2  // 2x safety margin
    if maxGas > MAX_GAS_BUDGET {
        maxGas = MAX_GAS_BUDGET
    }
    tx := sui.NewTransaction(
        sui.WithGasBudget(maxGas),
        // ...
    )
    return tx, nil
}
```

---

## 8. Wrong Gas Price for Outbound Transactions

### Overview

Using the wrong gas price for Sui outbound transactions can cause them to be underpaid (stuck) or overpaid (wasting TSS funds).

> **Validation strength**: Moderate — 1 MEDIUM report from Sherlock on ZetaChain
> **Frequency**: 1/69 reports

### Vulnerable Pattern Examples

**Example 1: PostGasPrice Not Matching Sui Network** [MEDIUM]
> 📖 Reference: `reports/sui_move_findings/m-6-wrong-postgasprice-is-set-for-sui-outbound-transactions.md`
```go
// ❌ VULNERABLE: Uses EVM gas price model for Sui
func SetPostGasPrice(ctx sdk.Context, cctx *types.CrossChainTx) {
    // BUG: Uses chain_id lookup that returns EVM gas price format
    gasPrice := k.GetGasPrice(ctx, cctx.DestChainId)
    cctx.PostGasPrice = gasPrice
    // Sui uses a different gas model (reference gas price, not gwei)
}
```

### Secure Implementation

```go
// ✅ SECURE: Use Sui-specific gas price query
func SetPostGasPrice(ctx sdk.Context, cctx *types.CrossChainTx) {
    if chains.IsSuiChain(cctx.DestChainId) {
        refGasPrice, err := suiClient.GetReferenceGasPrice(ctx)
        if err != nil {
            return err
        }
        cctx.PostGasPrice = refGasPrice
    } else {
        cctx.PostGasPrice = k.GetGasPrice(ctx, cctx.DestChainId)
    }
}
```

---

## 9. Epoch Transition Failure via Duplicate PubKey

### Overview

The Sui Bridge committee management uses `vec_map::insert` which aborts on duplicate keys. If two validators register with the same bridge public key, the epoch transition fails and the bridge halts.

> **Validation strength**: Strong — 1 HIGH report from OtterSec on Sui Bridge
> **Frequency**: 1/69 reports

See [Object Model Entry, Section 7](SUI_MOVE_OBJECT_MODEL_VULNERABILITIES.md#7-committee--epoch-management-bugs) for full details.

---

## 10. Blocklist Iterator State Bug

### Overview

The blocklist validation loop in Sui Bridge doesn't reset its iterator between list entries, causing incorrect validation that either blocks valid members or passes invalid ones.

> **Validation strength**: Strong — 1 MEDIUM report from OtterSec on Sui Bridge
> **Frequency**: 1/69 reports

See [Object Model Entry, Section 7](SUI_MOVE_OBJECT_MODEL_VULNERABILITIES.md#7-committee--epoch-management-bugs) for full details.

---

## 11. Cross-Chain Flow Rate Direction Mismatch

### Overview

Axelar's cross-chain gateway on Sui tracks inbound and outbound token flows for rate limiting. Calling `add_flow_out` instead of `add_flow_in` (or vice versa) corrupts the rate limiter, allowing unlimited transfers in one direction while blocking the other.

> **Validation strength**: Strong — 1 HIGH report from OtterSec on Axelar
> **Frequency**: 1/69 reports

See [DeFi Logic Entry, Section 4](SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md#4-incorrect-flow-rate-tracking) for full details.

---

## 12. Wrong Integration Function Call

### Overview

When integrating cross-chain message handling with flow limiters, calling the wrong function (e.g., `add_flow_out` for received messages) silently corrupts state.

> **Validation strength**: Moderate — 1 MEDIUM report from OtterSec on Axelar
> **Frequency**: 1/69 reports

See [DeFi Logic Entry, Section 5](SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md#5-wrong-function-call-in-integration) for full details.

---

## Prevention Guidelines

### Cross-Chain Bridge Best Practices
1. **Atomic State Changes**: Use cached contexts or two-phase commits for cross-chain operations
2. **Nonce Resilience**: Implement nonce gap handling — failed nonces shouldn't block subsequent ones
3. **Node Redundancy**: Use multiple RPC endpoints with automatic failover
4. **Address Validation**: Validate destination chain address format before processing CCTXs
5. **Full Type Matching**: Validate complete coin type paths (package::module::struct), not partial strings
6. **Idempotent Signing**: Check for existing signatures before re-signing CCTXs
7. **Gas Budget Caps**: Bound gas budgets against estimated costs with safety margins
8. **Chain-Specific Gas Models**: Use chain-appropriate gas price queries (Sui reference gas ≠ EVM gwei)
9. **Duplicate Key Prevention**: Check for key existence before `vec_map::insert` in committee management
10. **Direction-Aware Rate Limiting**: Map inbound/outbound operations to correct flow limiter calls

### Testing Requirements
- Test cross-chain transactions with Sui-side failures — verify EVM state rollback
- Simulate nonce gaps and verify recovery
- Test with unreachable Sui nodes — verify failover
- Test coin type validation with adversarial type strings
- Verify gas budget bounds with extreme values
- Test epoch transitions with duplicate validator registrations
- Verify flow limiter directions with bidirectional traffic

---

### Keywords for Search

`zetachain`, `zetaclient`, `cctx`, `cross_chain_tx`, `outbound_nonce`, `inbound_tx`, `sui_observer`, `tss`, `threshold_signature`, `gas_coin`, `gas_price`, `reference_gas_price`, `coin_type`, `receiver`, `sui_address`, `epoch_transition`, `committee`, `bridge_pubkey`, `blocklist`, `flow_limiter`, `add_flow_in`, `add_flow_out`, `axelar_gateway`, `sui_bridge`, `cached_context`, `two_phase_commit`, `nonce_manipulation`, `node_dos`, `re_signing`, `duplicate_pubkey`, `vec_map_insert`

### Related Vulnerabilities
- `DB/bridge/` — Generic bridge vulnerability patterns
- `DB/bridge/layerzero/` — LayerZero-specific patterns
- `DB/bridge/wormhole/` — Wormhole-specific patterns

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

`ObserveInTx`, `axelar`, `axelar_gateway`, `blocklist`, `bridge`, `bridge_message`, `bridge_security|cross_chain_messaging|state_sync|inbound_validation`, `burn`, `cctx`, `coin_type`, `committee`, `cross_chain`, `cross_chain_bridge`, `deposit`, `epoch`, `evm`, `flow_limiter`, `gas_price`, `go`, `inbound_tx`, `nonce`, `outbound_tx`, `receiver_module`, `rust`, `sui`, `sui_bridge`, `tss`, `tss_signer`, `zetachain`, `zetaclient`
