# zk-rollup

> 145 nodes · cohesion 0.14

## Key Concepts

- **Move Merkle Proof Verification Vulnerabilities [CRITICAL]** (73 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 1: Merkle Proof Replay via Missing Index in Hash — move-merkle-001** (65 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 8: Bitmap Claim Tracking Overflow — move-merkle-008 [CRITICAL]** (63 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Missing PIL / AIR Constraints** (63 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 7: JALR imm_sign Unconstrained (RISC-V zkVM)** (63 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 7: Odd-Length Proof Padding Bypass — move-merkle-007 [CRITICAL]** (61 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 1: Missing PIL Constraint for SMT Inclusion** (61 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 6: partial_sha256_var_interstitial Hash Collision (Undersized Input)** (61 connections) — `DB/zk-rollup/circuit-constraints.md`
- **proof_forgery** (60 connections) — `DB/general/restaking/EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md`
- **Pattern 2: Flawed Merkle Proof Verification Logic — move-merkle-002** (59 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 2: Underconstrained Carry Value in Binary State Machine** (59 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 5: SHA256 AIR Unconstrained final_hash at Last Block** (59 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 6: Resource Index Collision Enabling Claim Spoofing — move-merkle-006 [CRITICAL]** (57 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 3: Missing Range Constraint on Division Remainder (zkEVM Opcode)** (57 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 4: IsLtArraySubAir Soundness Issue (RISC-V Circuit)** (57 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Cryptographic Weaknesses in Proof Systems** (57 connections) — `DB/zk-rollup/proof-verification.md`
- **1. 51% Attack via Arbitrary Execution [CRITICAL]** (55 connections) — `DB/general/dao-governance-vulnerabilities/governance-takeover.md`
- **Pattern 1: Missing On-Chain ZK Proof Verification** (55 connections) — `DB/zk-rollup/proof-verification.md`
- **5. Unrestricted Deployment/Election Takeover** (53 connections) — `DB/general/dao-governance-vulnerabilities/governance-takeover.md`
- **Pattern 3: Unchecked Merkle Verification Return Value — move-merkle-003** (53 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 4: Fee Bypass at Maximum Fee Setting — move-merkle-004** (53 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 5: Missing Domain Separation Between Leaf and Internal Nodes — move-merkle-005 [CRITICAL]** (53 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 2: Incorrect Randomness Computation Allows Proof Forgery** (53 connections) — `DB/zk-rollup/proof-verification.md`
- **2. Loss of Veto Power Enabling Takeover** (51 connections) — `DB/general/dao-governance-vulnerabilities/governance-takeover.md`
- **3. Centralized Governance Control** (51 connections) — `DB/general/dao-governance-vulnerabilities/governance-takeover.md`
- *... and 120 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- `DB/general/dao-governance-vulnerabilities/governance-takeover.md`
- `DB/general/restaking/EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md`
- `DB/oracle/chainlink/CHAINLINK_VRF_VULNERABILITIES.md`
- `DB/zk-rollup/circuit-constraints.md`
- `DB/zk-rollup/proof-verification.md`

## Audit Trail

- EXTRACTED: 601 (38%)
- INFERRED: 991 (62%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*