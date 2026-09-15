# zk-rollup 2

> 144 nodes · cohesion 0.14

## Key Concepts

- **Move Merkle Proof Verification Vulnerabilities [CRITICAL]** (73 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 1: Merkle Proof Replay via Missing Index in Hash — move-merkle-001** (65 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Missing PIL / AIR Constraints** (63 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 7: JALR imm_sign Unconstrained (RISC-V zkVM)** (63 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 8: Bitmap Claim Tracking Overflow — move-merkle-008 [CRITICAL]** (63 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 1: Missing PIL Constraint for SMT Inclusion** (61 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 6: partial_sha256_var_interstitial Hash Collision (Undersized Input)** (61 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 7: Odd-Length Proof Padding Bypass — move-merkle-007 [CRITICAL]** (61 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **proof_forgery** (60 connections) — `DB/general/restaking/EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md`
- **Pattern 2: Underconstrained Carry Value in Binary State Machine** (59 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 5: SHA256 AIR Unconstrained final_hash at Last Block** (59 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 2: Flawed Merkle Proof Verification Logic — move-merkle-002** (59 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 3: Missing Range Constraint on Division Remainder (zkEVM Opcode)** (57 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Pattern 4: IsLtArraySubAir Soundness Issue (RISC-V Circuit)** (57 connections) — `DB/zk-rollup/circuit-constraints.md`
- **Cryptographic Weaknesses in Proof Systems** (57 connections) — `DB/zk-rollup/proof-verification.md`
- **Pattern 6: Resource Index Collision Enabling Claim Spoofing — move-merkle-006 [CRITICAL]** (57 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 1: Missing On-Chain ZK Proof Verification** (55 connections) — `DB/zk-rollup/proof-verification.md`
- **1. 51% Attack via Arbitrary Execution [CRITICAL]** (55 connections) — `DB/general/dao-governance-vulnerabilities/governance-takeover.md`
- **Pattern 2: Incorrect Randomness Computation Allows Proof Forgery** (53 connections) — `DB/zk-rollup/proof-verification.md`
- **5. Unrestricted Deployment/Election Takeover** (53 connections) — `DB/general/dao-governance-vulnerabilities/governance-takeover.md`
- **Pattern 3: Unchecked Merkle Verification Return Value — move-merkle-003** (53 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 4: Fee Bypass at Maximum Fee Setting — move-merkle-004** (53 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 5: Missing Domain Separation Between Leaf and Internal Nodes — move-merkle-005 [CRITICAL]** (53 connections) — `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- **Pattern 3: Plonk/Groth16 Verifiers Accept Untrusted Recursion VK Root** (51 connections) — `DB/zk-rollup/proof-verification.md`
- **Pattern 4: Weak Fiat-Shamir in LogUp Phase Enables Backdoored Circuits** (51 connections) — `DB/zk-rollup/proof-verification.md`
- *... and 119 more nodes in this community*

## Relationships

- [access-control](access-control.md) (35 shared connections)
- [general 2](general_2.md) (21 shared connections)
- [general 4](general_4.md) (14 shared connections)
- [general](general.md) (8 shared connections)
- [governance](governance.md) (8 shared connections)
- [defi 8](defi_8.md) (6 shared connections)
- [defi 6](defi_6.md) (5 shared connections)
- [proxy](proxy.md) (3 shared connections)
- [cosmos 7](cosmos_7.md) (1 shared connections)

## Source Files

- `DB/Sui-Move-specific/MOVE_MERKLE_VERIFICATION_VULNERABILITIES.md`
- `DB/general/dao-governance-vulnerabilities/governance-takeover.md`
- `DB/general/restaking/EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md`
- `DB/oracle/chainlink/CHAINLINK_VRF_VULNERABILITIES.md`
- `DB/zk-rollup/circuit-constraints.md`
- `DB/zk-rollup/proof-verification.md`

## Audit Trail

- EXTRACTED: 601 (38%)
- INFERRED: 989 (62%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*