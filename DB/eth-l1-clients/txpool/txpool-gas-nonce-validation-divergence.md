---
vulnerability_class: txpool_validation_divergence
title: "Txpool Validation Divergence: gas/nonce/fee checks weaker than execution (mempool DoS & consensus drift)"
protocol: eth-l1-clients
category: Transaction Pool
vulnerability_type: validation_mismatch
attack_type: spam_tx_acceptance|mempool_dos|eip_violation|state_root_divergence
affected_component: txpool_validation|intrinsic_gas|nonce_checks|fee_caps
chain: ethereum
severity: medium
impact: mempool_dos|chain_split|consensus_divergence|node_halt
severity_range: "LOW to HIGH"
source: Immunefi Ethereum Protocol Attackathon 2024-2025 + Sigma Prime

primitives:
  - intrinsic_gas_txpool_vs_evm_mismatch
  - missing_block_gas_limit_check_in_txpool
  - sendrawtransaction_fee_check_bypass
  - eip2681_nonce_upper_bound_violation
  - wrong_nonce_execution_state_root_mismatch
  - pending_pool_subtraction_overflow_infinite_loop

affected_components:
  - txpool validateTx / senders
  - intrinsic gas calculators (txpool copy vs EVM copy)
  - RPC eth_sendRawTransaction fee checks
  - nonce increment logic in state transition

tags:
  - txpool
  - mempool
  - gas
  - nonce
  - erigon
  - nethermind
  - reth
  - eip-2681
  - consensus
  - attackathon

total_reports_analyzed: 6

# Pattern Identity (Required)
root_cause_family: validation_logic_duplicated_and_diverged
pattern_key: txpool_validation_gap | gas_nonce_fee_check_mismatch | mempool_dos_consensus_drift

# Interaction Scope
interaction_scope: external_entrypoint_to_consensus

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - validateTx
  - ValidateSerializedTxn
  - intrinsicGas
  - calcIntrinsicGas
  - IntrinsicGas
  - gasLimit
  - blockGasLimit
  - maxFeeCap
  - SendRawTransaction
  - nonce
  - SetNonce
  - "0xffffffffffffffff"
  - pendingPool
  - sub / checked_sub
---

# Txpool Gas/Nonce Validation Divergence (txpool weaker than execution)

## Overview

Every EL client validates transactions twice: once at mempool admission (cheap, pre-execution) and
once at execution (consensus-critical). When the two copies of "valid" drift apart — or when the
client's copy drifts from the EIP/geth reference — you get either (a) free mempool spam (txpool
accepts what will never execute) or (b) consensus divergence (execution accepts/rejects differently
than the reference). Six confirmed findings:

1. **Erigon intrinsic gas mismatch for AccessListTxType** (#38427): txpool computes less intrinsic
   gas than EVM execution → txs admitted that can never be mined; spam vector.
2. **Erigon missing block-gas-limit check at admission** (#38278): txs with gas > block limit enter
   the pool, never mineable, pure resource waste at zero cost to the attacker.
3. **Erigon SendRawTransaction fee check incorrect** (#38554): the "too many fees" guard is buggy.
4. **Nethermind EIP-2681 violation** (#38015): create-tx nonce upper bound enforced at 2^64-2
   instead of 2^64-1 → off-by-one consensus edge at account nonce ceiling.
5. **Nethermind wrong-nonce execution state-root divergence** (#37695): executing a tx with wrong
   nonce produces a state root different from geth/EELS (goevmlab statetest) → chain-split class.
6. **reth pending-pool subtraction overflow** (#38502): crafted tx set → infinite loop in pending
   pool → node halt without crash.

**Root Cause Statement**: This vulnerability exists because transaction validity logic is
duplicated between txpool admission and EVM execution (and across clients), and the copies diverge —
missing checks, different gas formulas, or off-by-one nonce bounds — letting attackers spam the
mempool for free or causing state-root/consensus divergence from the reference client.

**Observed Frequency**: 6 accepted findings in one competition; structural (every client ships 2+ copies of validation)
**Consensus Severity**: LOW (spam) to HIGH (state-root divergence #37695)

---

#### Agent Quick View

- Root cause statement: "This vulnerability exists because of validation_logic_duplicated_and_diverged (txpool vs EVM gas/nonce/fee)"
- Pattern key: `txpool_validation_gap | gas_nonce_fee_check_mismatch | mempool_dos_consensus_drift`
- Interaction scope: `external_entrypoint_to_consensus`
- Primary affected component(s): `txpool_validation`, `intrinsic_gas`
- High-signal code keywords: `validateTx`, `intrinsicGas`, `blockGasLimit`, `nonce`, `SendRawTransaction`
- Typical sink / impact: `mempool_dos` / `chain_split`
- Validation strength: `high`

#### Contract / Boundary Map

- Entry surface(s): RPC `eth_sendRawTransaction`, P2P tx gossip (NewPooledTransactionHashes)
- Contract hop(s): `raw tx -> txpool validateTx -> (mine) -> EVM validate + execute -> state root`
- Trust boundary crossed: `any transaction submitter (no stake, no identity)`
- Shared state or sync assumption: `txpool validity == execution validity == spec validity`

#### Valid Bug Signals

- Signal 1: Two distinct intrinsic-gas implementations (txpool path, EVM path) with different type/branch coverage — diff them line by line per tx type (legacy, 2930, 1559, 4844, 7702)
- Signal 2: No `tx.gas > header.gas_limit` rejection in `validateTx`
- Signal 3: RPC-level fee cap check uses a different formula than consensus `maxFeeCap`/`blobFeeCap` checks
- Signal 4: Nonce comparisons against `2^64-2` (EIP-2681 requires reject only at `2^64-1`)
- Signal 5: Statetest (goevmlab) fuzz shows post-tx state root differs from geth on nonce-invalid txs

#### False Positive Guards

- Not this bug when: txpool intentionally lenient AND execution is spec-exact (then it's only spam-class DoS, not consensus)
- Safe if: single shared validation function used by both txpool and executor, covered by cross-client differential tests
- Requires attacker control of: transaction content only (standard tx submission)
- Pool-eviction economics (fee-bumping, locals) mitigate but never eliminate zero-cost spam vectors

## Real Reports

### 1. Immunefi #38427 [BC-Low] — Discrepancy in Intrinsic Gas Calculation between Txpool and EVM Execution (CertiK, erigon)

Report: `reports/eth-l1-clients_findings/38427-bc-low-discrepancy-in-intrinsic-gas-calculation-between-txpool-and-evm-execution.md`
`validateTx()` (`txnprovider/txpool/pool.go#L815`, v3.0.0-alpha7) computes less intrinsic gas than
execution for AccessListTxType.

### 2. Immunefi #38278 [BC-Low] — Potential DoS to Mempool Due to Missing Gas Limit Check (CertiK, erigon)

Report: `reports/eth-l1-clients_findings/38278-bc-low-potential-dos-to-mempool-due-to-missing-gas-limit-check.md`
`ValidateSerializedTxn`/`ValidateTx`/`ParseTransaction` never check `tx.gas <= blockGasLimit`.

### 3. Immunefi #38554 [BC-Low] — Incorrect transaction fee check in SendRawTransaction (erigon)

Report: `reports/eth-l1-clients_findings/38554-bc-low-incorrect-transaction-fee-check-in-sendrawtransaction.md`

### 4. Immunefi #38015 [BC-Insight] — Violation of EIP-2681 in CREATE transaction (nethermind)

Report: `reports/eth-l1-clients_findings/38015-bc-insight-violation-of-eip-2681-in-create-transaction.md`
Create-tx nonce threshold 2^64-2 vs spec 2^64-1.

### 5. Immunefi #37695 [BC-Insight] — Executing transaction with wrong nonce → chain split via mismatched state root (Omik, nethermind)

Report: `reports/eth-l1-clients_findings/37695-bc-insight-executing-transaction-that-has-a-wrong-nonce-might-triggered-a-chain-split-due-to-m.md`
goevmlab statetest: wrong-nonce tx execution leaves Nethermind state root ≠ geth/EELS.

### 6. Immunefi #38502 [BC-Low] — Pending pool subtraction overflow causes node halt/shutdown (reth)

Report: `reports/eth-l1-clients_findings/38502-bc-low-pending-pool-subtraction-overflow-causes-node-halt-shutdown.md`
Crafted tx inputs → subtraction overflow → infinite loop in pending pool; node stays up but stops
processing transactions (halt class, worst availability impact).

### Related: Sigma Prime reth 2024 RETH-21 — Imported Transactions May Be Removed From Fetcher Without Being Added To The Pool (Low)

`reports/eth-l1-clients_findings/reth-sigp-2024.md` — tx lifecycle accounting divergence.

## Vulnerable Code Pattern (generic)

```go
// VULNERABLE: txpool intrinsic gas misses access-list charging that EVM applies (#38427)
func (p *TxPool) validateTx(txn *TxnSlot) DiscardReason {
    if txn.Gas < intrinsicGasCheap(txn) { return DiscardInvalidGas } // cheaper formula
    // missing: tx.gas <= blockGasLimit check (#38278)
    ...
}
// execution later requires txn.Gas >= intrinsicGasFull(txn) > intrinsicGasCheap(txn)
```

```python
# VULNERABLE: off-by-one nonce ceiling (#38015)
if tx.nonce >= 2**64 - 2: return INVALID   # EIP-2681: reject only 2**64 - 1
```

## Detection & Hunt Strategy

1. Locate every intrinsic-gas implementation in the repo (`grep -r intrinsic`); assert exactly one
   shared module, or diff all copies per tx type against EIP references (15000/21000 base,
   4800/16 access list rules, 7702/4844 modifiers).
2. Fuzz txpool admission vs block building: generate txs on the boundary of every validity rule,
   submit, and verify `admitted == includable`.
3. Run goevmlab/statetest differential suites for intentionally-invalid txs (bad nonce, over-ceiling
   nonce, insufficient intrinsic) and diff post-state roots against geth+EELS.
4. Grep nonce constants `0xfffffffffffffffe` vs `0xffffffffffffffff` for EIP-2681 conformance.
5. Test fee-cap math at uint256/uint128 extremes in RPC submission vs consensus validation.

## References

- `reports/eth-l1-clients_findings/38427-bc-low-discrepancy-in-intrinsic-gas-calculation-between-txpool-and-evm-execution.md`
- `reports/eth-l1-clients_findings/38278-bc-low-potential-dos-to-mempool-due-to-missing-gas-limit-check.md`
- `reports/eth-l1-clients_findings/38554-bc-low-incorrect-transaction-fee-check-in-sendrawtransaction.md`
- `reports/eth-l1-clients_findings/38015-bc-insight-violation-of-eip-2681-in-create-transaction.md`
- `reports/eth-l1-clients_findings/37695-bc-insight-executing-transaction-that-has-a-wrong-nonce-might-triggered-a-chain-split-due-to-m.md`
- `reports/eth-l1-clients_findings/38502-bc-low-pending-pool-subtraction-overflow-causes-node-halt-shutdown.md`
- `reports/eth-l1-clients_findings/reth-sigp-2024.md`
- `reports/eth-l1-clients_findings/public-audits-reports-reth-review-pdf.md`- `reports/eth-l1-clients_findings/public-audits-reports-rise-sigma-prime-rise-core-node-security-assessment-report-v2-0-pdf.md`- `reports/eth-l1-clients_findings/publications-ebridge-ethereum-bridge-zellic-audit-report-pdf.md`
- EIP-2681 (nonce upper bound), EIP-2930 (access list intrinsic gas), devp2p tx gossip specs
