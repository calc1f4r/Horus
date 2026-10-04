# defi

> 231 nodes · cohesion 0.10

## Key Concepts

- **Sequencer Economic Issues** (111 connections) — `DB/zk-rollup/sequencer-issues.md`
- **Message Channel DoS and Censorship** (107 connections) — `DB/zk-rollup/bridge-vulnerabilities.md`
- **Pattern 1: Token Bridge Reentrancy Corrupts Accounting** (103 connections) — `DB/zk-rollup/bridge-vulnerabilities.md`
- **Pattern 1: Access-Controlled Functions Fail During Sequencer Downtime** (97 connections) — `DB/zk-rollup/sequencer-issues.md`
- **Pattern 2: Dutch Auctions and Options Expire at Bad Prices During Downtime** (97 connections) — `DB/zk-rollup/sequencer-issues.md`
- **Pattern 3: Linea / Sequencer Censorship Locking User Funds** (97 connections) — `DB/zk-rollup/sequencer-issues.md`
- **Pattern 2: Wrong Token Order in Bridge Causes Incorrect Routing** (95 connections) — `DB/zk-rollup/bridge-vulnerabilities.md`
- **Pattern 4: Sequencer Underpaid Due to Incorrect commitScalar** (95 connections) — `DB/zk-rollup/sequencer-issues.md`
- **Pattern 5: Front-Running finalizeBlocks in Decentralized Sequencer Mode** (95 connections) — `DB/zk-rollup/sequencer-issues.md`
- **Protocol Functions Breaking During Sequencer Downtime** (95 connections) — `DB/zk-rollup/sequencer-issues.md`
- **Pattern 3: Router Signatures Replay Across Chains** (89 connections) — `DB/zk-rollup/bridge-vulnerabilities.md`
- **Pattern 4: Wrong ERC1155 Selector Locks Tokens in Bridge** (89 connections) — `DB/zk-rollup/bridge-vulnerabilities.md`
- **Pattern 5: USDC Blacklist Permanently Locks Bridge Funds** (89 connections) — `DB/zk-rollup/bridge-vulnerabilities.md`
- **Pattern 6: Single Reverting Withdrawal Blocks Entire Queue** (89 connections) — `DB/zk-rollup/bridge-vulnerabilities.md`
- **Token Accounting and Token Mapping Errors** (89 connections) — `DB/zk-rollup/bridge-vulnerabilities.md`
- **1. LST Oracle Manipulation via Upgradeable Proxies [HIGH]** (89 connections) — `DB/general/restaking/LRT_EXCHANGE_RATE_ORACLE_VULNERABILITIES.md`
- **2. Exchange Rate Sandwich / Frontrunning** (85 connections) — `DB/general/restaking/LRT_EXCHANGE_RATE_ORACLE_VULNERABILITIES.md`
- **1. Sandwich / Front-Running Reward Claims [HIGH]** (85 connections) — `DB/general/restaking/RESTAKING_REWARD_DISTRIBUTION_VULNERABILITIES.md`
- **4. Exchange Rate Calculation Errors** (79 connections) — `DB/general/restaking/LRT_EXCHANGE_RATE_ORACLE_VULNERABILITIES.md`
- **Batch Hashing and Commitment Bugs** (77 connections) — `DB/zk-rollup/batch-processing.md`
- **6. Share Value Appreciation Blocking Settlement** (77 connections) — `DB/general/restaking/LRT_EXCHANGE_RATE_ORACLE_VULNERABILITIES.md`
- **2. msg.sender Confusion in Reward Re-Staking** (77 connections) — `DB/general/restaking/RESTAKING_REWARD_DISTRIBUTION_VULNERABILITIES.md`
- **Pattern 1: Batcher Frame Decoding Inconsistency Causes Consensus Split** (75 connections) — `DB/zk-rollup/batch-processing.md`
- **Pattern 2: EIP-4844 Blob Incompatibility Halts Block Processing** (75 connections) — `DB/zk-rollup/batch-processing.md`
- **Pattern 3: Rollup Cannot Split Batches Across Blobs → Block Stuffing** (75 connections) — `DB/zk-rollup/batch-processing.md`
- *... and 206 more nodes in this community*

## Relationships

- [amm 2](amm_2.md) (52 shared connections)
- [access-control 2](access-control_2.md) (32 shared connections)
- [general 2](general_2.md) (32 shared connections)
- [defi 2](defi_2.md) (28 shared connections)
- [general](general.md) (20 shared connections)
- [bridge](bridge.md) (17 shared connections)
- [bridge 2](bridge_2.md) (15 shared connections)
- [defi 3](defi_3.md) (15 shared connections)
- [zk-rollup 2](zk-rollup_2.md) (15 shared connections)
- [proxy 4](proxy_4.md) (8 shared connections)
- [access-control](access-control.md) (7 shared connections)
- [defi 7](defi_7.md) (6 shared connections)

## Source Files

- `DB/account-abstraction/aa-signature-replay-attacks.md`
- `DB/amm/concentrated-liquidity/dos-arithmetic-initialization.md`
- `DB/amm/concentrated-liquidity/price-oracle-manipulation.md`
- `DB/bridge/custom/cross-chain-general-vulnerabilities.md`
- `DB/bridge/wormhole/wormhole-integration-vulnerabilities.md`
- `DB/general/bonding-curve/BONDING_CURVE_MATH_FORMULA_VULNERABILITIES.md`
- `DB/general/bridge/cross-chain-bridge-vulnerabilities.md`
- `DB/general/restaking/LRT_EXCHANGE_RATE_ORACLE_VULNERABILITIES.md`
- `DB/general/restaking/RESTAKING_REWARD_DISTRIBUTION_VULNERABILITIES.md`
- `DB/oracle/price-manipulation/defihacklabs-flashloan-oracle-2022-patterns.md`
- `DB/oracle/price-manipulation/flash-loan-oracle-manipulation.md`
- `DB/unique/defihacklabs/defihacklabs-novel-attack-patterns-2025-2026.md`
- `DB/zk-rollup/batch-processing.md`
- `DB/zk-rollup/bridge-vulnerabilities.md`
- `DB/zk-rollup/l1-l2-messaging.md`
- `DB/zk-rollup/sequencer-issues.md`

## Audit Trail

- EXTRACTED: 1053 (36%)
- INFERRED: 1894 (64%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*