# zk-rollup

> 75 nodes · cohesion 0.27

## Key Concepts

- **CREATE / CREATE2 / CREATE3 Incompatibilities** (71 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **msg.sender and Context Differences** (71 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Opcode and Precompile Divergences** (71 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 1: CREATE2 Address Derivation Differs on ZKSync** (71 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 2: ecrecover Discrepancy in delegatecall Context on ZKSync** (71 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 3: Unauthorized Precompile Authorization Bypass via delegatecall** (71 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 4: Nonce Doesn't Increment for Reverted Child Deployments** (71 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Pattern 5: block.number Returns L1 Block Number on Arbitrum (Not L2)** (71 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Bytecode Compression** (69 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **Untested Runtime Upgrades Shift Layout/Indices and Strand Bridge Funds** (67 connections) — `DB/substrate/lifecycle/runtime-upgrade-storage-migration.md`
- **Factory Reorg Attacks** (57 connections) — `DB/zk-rollup/reorg-attacks.md`
- **Pattern 1: questFactory Reorg Attack** (57 connections) — `DB/zk-rollup/reorg-attacks.md`
- **Pattern 2: Stealing Liquidity Pool Funds via Reorg** (57 connections) — `DB/zk-rollup/reorg-attacks.md`
- **Pattern 3: General Factory.create Reorg (Multiple Protocols)** (57 connections) — `DB/zk-rollup/reorg-attacks.md`
- **Pattern 4: CREATE vs CREATE2 Reorg Risk Comparison [CRITICAL]** (57 connections) — `DB/zk-rollup/reorg-attacks.md`
- **bytecode_compression** (36 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **address_collision** (28 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **reports/zk_rollup_findings/m-08-factorycreate-is-vulnerable-to-reorg-attacks.md** (22 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **state_corruption** (20 connections) — `DB/substrate/lifecycle/runtime-upgrade-storage-migration.md`
- **bytecode_compressor** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **create2_opcode** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **create_opcode** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **ecrecover_precompile** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **extcodehash** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- **msg_sender** (18 connections) — `DB/zk-rollup/evm-incompatibilities.md`
- *... and 50 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `DB/substrate/lifecycle/runtime-upgrade-storage-migration.md`
- `DB/zk-rollup/evm-incompatibilities.md`
- `DB/zk-rollup/reorg-attacks.md`

## Audit Trail

- EXTRACTED: 313 (40%)
- INFERRED: 464 (60%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*