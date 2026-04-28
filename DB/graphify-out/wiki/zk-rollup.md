# zk-rollup

> 121 nodes · cohesion 0.14

## Key Concepts

- **arbitrum** (78 connections) — `DB/index.json`
- **batch-processing** (78 connections) — `DB/index.json`
- **circuit** (78 connections) — `DB/index.json`
- **fraud-proof** (78 connections) — `DB/index.json`
- **optimism** (78 connections) — `DB/index.json`
- **reorg** (78 connections) — `DB/index.json`
- **rollup** (78 connections) — `DB/index.json`
- **sequencer** (78 connections) — `DB/index.json`
- **zk-rollup** (78 connections) — `DB/index.json`
- **zksync** (78 connections) — `DB/index.json`
- **Horus Vulnerability DB** (56 connections) — `DB`
- **bytecode_compression** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Bytecode Compression** (16 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **CREATE / CREATE2 / CREATE3 Incompatibilities** (16 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **msg.sender and Context Differences** (16 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Opcode and Precompile Divergences** (16 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 1: CREATE2 Address Derivation Differs on ZKSync** (16 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 2: ecrecover Discrepancy in delegatecall Context on ZKSync** (16 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 3: Unauthorized Precompile Authorization Bypass via delegatecall** (16 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 4: Nonce Doesn't Increment for Reverted Child Deployments** (16 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 5: block.number Returns L1 Block Number on Arbitrum (Not L2)** (16 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Fee Theft and Manipulation** (15 connections) — `DB/zk-rollup/gas-accounting.md`
- **Gas Calculation Errors** (15 connections) — `DB/zk-rollup/gas-accounting.md`
- **Pattern 1: Paymaster Refunds spentOnPubdata Instead of Burning** (15 connections) — `DB/zk-rollup/gas-accounting.md`
- **Pattern 2: Operator Steals All Gas Provided for L1→L2 Transactions** (15 connections) — `DB/zk-rollup/gas-accounting.md`
- *... and 96 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `DB`
- `DB/account-abstraction/aa-erc7579-module-system-enable-mode.md`
- `DB/account-abstraction/aa-paymaster-gas-accounting-vulnerabilities.md`
- `DB/account-abstraction/aa-session-key-permission-abuse.md`
- `DB/account-abstraction/aa-signature-replay-attacks.md`
- `DB/index.json`
- `DB/zk-rollup/batch-processing.md`
- `DB/zk-rollup/bridge-vulnerabilities.md`
- `DB/zk-rollup/circuit-constraints.md`
- `DB/zk-rollup/evm-incompatibilities.md`
- `DB/zk-rollup/fraud-proofs.md`
- `DB/zk-rollup/gas-accounting.md`
- `DB/zk-rollup/l1-l2-messaging.md`
- `DB/zk-rollup/proof-verification.md`
- `DB/zk-rollup/reorg-attacks.md`
- `DB/zk-rollup/sequencer-issues.md`

## Audit Trail

- EXTRACTED: 931 (90%)
- INFERRED: 101 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*