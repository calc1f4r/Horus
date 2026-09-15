# zk-rollup

> 79 nodes · cohesion 0.36

## Key Concepts

- **Fee Theft and Manipulation** (85 connections) — `DB/zk-rollup/gas-accounting.md`
- **Gas Calculation Errors** (83 connections) — `DB/zk-rollup/gas-accounting.md`
- **Pattern 1: Paymaster Refunds spentOnPubdata Instead of Burning** (83 connections) — `DB/zk-rollup/gas-accounting.md`
- **Pattern 3: Gas Calculation Uses Unchecked Free Variables** (83 connections) — `DB/zk-rollup/gas-accounting.md`
- **Pattern 4: Burning User Gas in sendCompressedBytecode** (83 connections) — `DB/zk-rollup/gas-accounting.md`
- **Pattern 5: Incorrect commitScalar Underpays Sequencer** (83 connections) — `DB/zk-rollup/gas-accounting.md`
- **Pattern 6: Batch Fees Multiplier Cap Bypassed with Multiple Calls** (83 connections) — `DB/zk-rollup/gas-accounting.md`
- **Pattern 2: Operator Steals All Gas Provided for L1→L2 Transactions** (81 connections) — `DB/zk-rollup/gas-accounting.md`
- **Pattern 7: Bytecode Compression Bypass Completeness Checks** (81 connections) — `DB/zk-rollup/gas-accounting.md`
- **Pattern 3: Address Aliasing Locks ETH** (81 connections) — `DB/zk-rollup/l1-l2-messaging.md`
- **Pattern 6: CrossDomainMessenger Cannot Guarantee Replayability** (81 connections) — `DB/zk-rollup/l1-l2-messaging.md`
- **L1 → L2 Transaction Failures** (79 connections) — `DB/zk-rollup/l1-l2-messaging.md`
- **L2 → L1 Withdrawal Issues** (79 connections) — `DB/zk-rollup/l1-l2-messaging.md`
- **Pattern 1: Loss of Funds When L1→L2 Transaction Fails in Bootloader** (79 connections) — `DB/zk-rollup/l1-l2-messaging.md`
- **Pattern 2: MsgValueSimulator Non-Zero Value Calls Sender Itself** (79 connections) — `DB/zk-rollup/l1-l2-messaging.md`
- **Pattern 5: Paymaster Refunds spentOnPubdata to User** (79 connections) — `DB/zk-rollup/l1-l2-messaging.md`
- **Pattern 4: Attacker Fills L2ToL1MessagePasser Merkle Tree** (77 connections) — `DB/zk-rollup/l1-l2-messaging.md`
- **5. Gas Payment Issues** (59 connections) — `DB/bridge/hyperlane/hyperlane-integration-vulnerabilities.md`
- **4. Handle Function Vulnerabilities** (55 connections) — `DB/bridge/hyperlane/hyperlane-integration-vulnerabilities.md`
- **1. ISM Validation Vulnerabilities [HIGH]** (53 connections) — `DB/bridge/hyperlane/hyperlane-integration-vulnerabilities.md`
- **3. Router Configuration Issues** (53 connections) — `DB/bridge/hyperlane/hyperlane-integration-vulnerabilities.md`
- **2. Message Replay Attacks** (49 connections) — `DB/bridge/hyperlane/hyperlane-integration-vulnerabilities.md`
- **bootloader** (34 connections) — `DB/zk-rollup/gas-accounting.md`
- **Mailbox** (26 connections) — `DB/bridge/hyperlane/hyperlane-integration-vulnerabilities.md`
- **requestL2Transaction** (20 connections) — `DB/zk-rollup/gas-accounting.md`
- *... and 54 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `DB/bridge/hyperlane/hyperlane-integration-vulnerabilities.md`
- `DB/zk-rollup/gas-accounting.md`
- `DB/zk-rollup/l1-l2-messaging.md`

## Audit Trail

- EXTRACTED: 452 (38%)
- INFERRED: 748 (62%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*