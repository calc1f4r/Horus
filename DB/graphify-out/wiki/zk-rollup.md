# zk-rollup

> 147 nodes · cohesion 0.17

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
- **Batch Hashing and Commitment Bugs** (77 connections) — `DB/zk-rollup/batch-processing.md`
- **Pattern 1: Batcher Frame Decoding Inconsistency Causes Consensus Split** (75 connections) — `DB/zk-rollup/batch-processing.md`
- **Pattern 2: EIP-4844 Blob Incompatibility Halts Block Processing** (75 connections) — `DB/zk-rollup/batch-processing.md`
- **Pattern 3: Rollup Cannot Split Batches Across Blobs → Block Stuffing** (75 connections) — `DB/zk-rollup/batch-processing.md`
- **Pattern 4: Malformed Blob Transaction Crashes Validator Nodes** (75 connections) — `DB/zk-rollup/batch-processing.md`
- **Pattern 5: Memory Corruption Causing Incorrect Batch Hashes (Scroll)** (75 connections) — `DB/zk-rollup/batch-processing.md`
- **Pattern 6: Incorrect basefee Calculation on Taiko Rollup** (75 connections) — `DB/zk-rollup/batch-processing.md`
- **Pattern 7: inChallenge Incorrectly Reset in revertBatch** (75 connections) — `DB/zk-rollup/batch-processing.md`
- **3. Message Replay Attacks** (71 connections) — `DB/bridge/wormhole/wormhole-integration-vulnerabilities.md`
- **1. VAA Parsing Vulnerabilities [HIGH]** (69 connections) — `DB/bridge/wormhole/wormhole-integration-vulnerabilities.md`
- *... and 122 more nodes in this community*

## Relationships

- [oracle](oracle.md) (49 shared connections)
- [general 2](general_2.md) (32 shared connections)
- [defi 8](defi_8.md) (31 shared connections)
- [bridge](bridge.md) (17 shared connections)
- [defi 4](defi_4.md) (16 shared connections)
- [bridge 2](bridge_2.md) (15 shared connections)
- [zk-rollup 3](zk-rollup_3.md) (15 shared connections)
- [general](general.md) (8 shared connections)
- [token](token.md) (6 shared connections)
- [defi](defi.md) (3 shared connections)
- [zk-rollup 5](zk-rollup_5.md) (2 shared connections)
- [defi 7](defi_7.md) (1 shared connections)

## Source Files

- `DB/account-abstraction/aa-signature-replay-attacks.md`
- `DB/amm/concentrated-liquidity/dos-arithmetic-initialization.md`
- `DB/bridge/custom/cross-chain-general-vulnerabilities.md`
- `DB/bridge/wormhole/wormhole-integration-vulnerabilities.md`
- `DB/general/bridge/cross-chain-bridge-vulnerabilities.md`
- `DB/zk-rollup/batch-processing.md`
- `DB/zk-rollup/bridge-vulnerabilities.md`
- `DB/zk-rollup/l1-l2-messaging.md`
- `DB/zk-rollup/sequencer-issues.md`

## Audit Trail

- EXTRACTED: 744 (37%)
- INFERRED: 1278 (63%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*