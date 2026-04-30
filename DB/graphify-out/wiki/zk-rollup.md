# zk-rollup

> 61 nodes · cohesion 0.33

## Key Concepts

- **CREATE / CREATE2 / CREATE3 Incompatibilities** (69 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **msg.sender and Context Differences** (69 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Opcode and Precompile Divergences** (69 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Bytecode Compression** (67 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 1: CREATE2 Address Derivation Differs on ZKSync** (59 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 2: ecrecover Discrepancy in delegatecall Context on ZKSync** (59 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 3: Unauthorized Precompile Authorization Bypass via delegatecall** (59 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 4: Nonce Doesn't Increment for Reverted Child Deployments** (59 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 5: block.number Returns L1 Block Number on Arbitrum (Not L2)** (59 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Factory Reorg Attacks** (57 connections) — `DB/zk-rollup/reorg-attacks.md`
- **Pattern 1: questFactory Reorg Attack** (47 connections) — `DB/zk-rollup/reorg-attacks.md`
- **Pattern 2: Stealing Liquidity Pool Funds via Reorg** (47 connections) — `DB/zk-rollup/reorg-attacks.md`
- **Pattern 3: General Factory.create Reorg (Multiple Protocols)** (47 connections) — `DB/zk-rollup/reorg-attacks.md`
- **Pattern 4: CREATE vs CREATE2 Reorg Risk Comparison** (47 connections) — `DB/zk-rollup/reorg-attacks.md`
- **bytecode_compression** (36 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **address_collision** (28 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **bytecode_compressor** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **create2_opcode** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **create_opcode** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **ecrecover_precompile** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **extcodehash** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **msg_sender** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **nonce_tracker** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **authentication_bypass** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **deployment_failure** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- *... and 36 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `DB/zk-rollup/evm-incompatibilities.md`
- `DB/zk-rollup/reorg-attacks.md`

## Audit Trail

- EXTRACTED: 302 (48%)
- INFERRED: 329 (52%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*