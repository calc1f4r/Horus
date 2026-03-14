# Staking: Beacon Chain Proof & Attestation Invariants

> Canonical invariants for beacon chain proof verification, attestation validation,
> EigenPod accounting, and validator state management. Mined from EigenLayer,
> beacon chain specifications, and the Vulnerability Database. Language-agnostic
> and protocol-agnostic.
> Consumed by `invariant-writer` as seed context.

## Metadata

- **Category**: staking
- **Subcategory**: beacon-chain-proofs
- **Sources**: EigenLayer, Ethereum Beacon Chain Spec, Lido, Casimir, Avail
- **Last updated**: 2026-03-13
- **Invariant count**: 10

---

## Invariants

### STAKING-BEACON-001: Proof Forgery Prevention

**Property (English):**
Beacon chain state proofs must be verified against a trusted beacon block root. A user must not be able to submit a beacon state proof that references a block root not anchored in the beacon block root oracle. Partial proof verification (e.g., verifying body against state but not state against block root) is insufficient.

**Property (Formal):**
$$\forall \text{proof}(p): \text{verify}(p.\text{leaf}, p.\text{path}, p.\text{stateRoot}) \land \text{verify}(p.\text{stateRoot}, p.\text{blockPath}, \text{oracleBlockRoot})$$

Both verification steps must succeed — the leaf against the state root AND the state root against a trusted block root.

**Mode:** NEGATIVE
**Priority:** CRITICAL
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires beacon chain interaction)

**Conditions:**
- Applies to any contract verifying beacon chain Merkle proofs
- The oracle block root must be from a trusted source (e.g., EIP-4788 beacon roots contract)
- Proof indices must be validated against expected ranges

**Source Evidence:**
- Protocol: EigenLayer | File: `DB/general/restaking/EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md`
- Report: `reports/eigenlayer_findings/m-02-verification-of-singlevalidatorstateproof-is-incomplete.md`

**Why This Matters:**
Incomplete proof verification allows an attacker to forge validator balances, claim false withdrawals, or steal restaked ETH.

**Known Violations (from DB):**
- `general-defi-eigenpod-beacon-chain-vulnerabilities-1-proof-forgery-via-incomplete-ve-000`

---

### STAKING-BEACON-002: Beacon State Root Upgrade Safety

**Property (English):**
When beacon chain data structures change across hard forks (e.g., Capella → Deneb), proof verification logic must correctly handle the new GeneralizedIndex values and field offsets. A hard fork must not silently break proof verification.

**Property (Formal):**
$$\forall \text{fork}(f): \text{GenIndex}(f) \neq \text{GenIndex}(f-1) \implies \text{verifier.update}(f) \text{ before } \text{fork.activation}(f)$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires beacon chain proof verification)

**Conditions:**
- Applies to any contract using beacon chain Merkle proofs with hardcoded generalized indices
- Must be updated for every Ethereum consensus layer hard fork that changes beacon state layout
- EIP-4788 block root exposure changed Merkle tree structure

**Source Evidence:**
- Protocol: EigenLayer | File: `DB/general/restaking/EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md`
- Report: `reports/eigenlayer_findings/beacon-state-root-upgrade-breakage.md`

**Why This Matters:**
Stale generalized indices after a hard fork make all proofs fail (DoS) or allow forged proofs (theft).

**Known Violations (from DB):**
- `general-defi-eigenpod-beacon-chain-vulnerabilities-2-beacon-state-root-upgrade-break-001`

---

### STAKING-BEACON-003: StakedButUnverified Accounting Accuracy

**Property (English):**
The `stakedButNotVerifiedEth` (or equivalent) counter must accurately track ETH that has been sent to the beacon chain deposit contract but has not yet been verified via a beacon chain proof. Deposits must increment this counter, and successful balance proofs must decrement it.

**Property (Formal):**
$$\text{stakedUnverified}(t) = \sum \text{deposits}(0..t) - \sum \text{verifiedProofs}(0..t)$$

$$\text{stakedUnverified}(t) \geq 0 \quad \forall t$$

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires beacon chain deposit tracking)

**Conditions:**
- Applies to EigenPod-style contracts that bridge between EL and CL
- Verification proofs must use the actual beacon balance, not the 32 ETH assumption

**Source Evidence:**
- Protocol: EigenLayer | File: `DB/general/restaking/EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md`

**Why This Matters:**
Incorrect unverified ETH accounting inflates or deflates the pod's reported balance, affecting share price and withdrawal amounts.

**Known Violations (from DB):**
- `general-defi-eigenpod-beacon-chain-vulnerabilities-3-stakedbutunverifiednativeeth-ac-002`

---

### STAKING-BEACON-004: Permissionless Proof Access Control

**Property (English):**
If beacon chain proof verification is permissionless (anyone can submit proofs), the protocol must ensure that malicious proof submission cannot harm the pod owner. Specifically, submitting a balance proof showing a slashed validator must not cause unexpected accounting consequences for the pod.

**Property (Formal):**
$$\forall \text{prover}(p), \text{pod}(\pi): \text{submitProof}(p, \pi, \text{validProof}) \implies \text{balance}(\pi)' \geq \text{actualBalance}(\pi)$$

No proof submission by any party can set the pod balance below its true beacon chain balance.

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires permissionless proof submission)

**Conditions:**
- Applies when any address can verify a validator's balance proof
- Attacker may time proof submission to coincide with slashing events
- Must handle: old proofs submitted after balance recovery

**Source Evidence:**
- Protocol: EigenLayer | File: `DB/general/restaking/EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md`

**Why This Matters:**
Malicious proof timing lets attackers lock in a slashed balance before the validator recovers, extracting value from the pod owner.

**Known Violations (from DB):**
- `general-defi-eigenpod-beacon-chain-vulnerabilities-4-permissionless-proof-verificati-003`

---

### STAKING-BEACON-005: Slashing Factor Calculation Correctness

**Property (English):**
The beacon chain slashing penalty calculation must match the consensus spec exactly. The effective balance, the slashing amount, and the proportional penalty must all use the correct epoch boundaries and total slashed amounts.

**Property (Formal):**
$$\text{penalty}(v) = \frac{\text{effectiveBalance}(v) \times \text{adjustedTotalSlash}}{32 \times \text{totalActiveBalance}}$$

The adjusted total slash is bounded: $\text{adjustedTotalSlash} = \min(3 \times \text{totalSlashed}, \text{totalActiveBalance})$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires beacon chain slashing modeling)

**Conditions:**
- Applies to contracts that replicate or rely on beacon chain slashing calculations
- Off-by-one in epoch selection changes the total slashed denominator significantly

**Source Evidence:**
- Protocol: EigenLayer | File: `DB/general/restaking/EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md`

**Why This Matters:**
Incorrect slashing factor miscalculates the penalty — either under-penalizing (protocol risk) or over-penalizing (staker loss).

**Known Violations (from DB):**
- `general-defi-eigenpod-beacon-chain-vulnerabilities-5-slashing-factor-miscalculation-004`

---

### STAKING-BEACON-006: Proof Timestamp Boundary Correctness

**Property (English):**
Timestamp comparisons for proof validity windows must use consistent boundaries (exclusive vs inclusive). A proof submitted at exactly the boundary timestamp must either always be accepted or always rejected — not depend on implementation inconsistency.

**Property (Formal):**
$$\text{proofTime} \in [\text{windowStart}, \text{windowEnd}] \quad \text{consistently across all checks}$$

If the protocol uses exclusive upper bounds, it must use exclusive everywhere; if inclusive, inclusive everywhere.

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires time-bounded proof windows)

**Conditions:**
- Applies to any proof verification with time-based validity windows
- Off-by-one at boundary creates edge case where valid proofs are rejected or invalid proofs accepted

**Source Evidence:**
- Protocol: EigenLayer | File: `DB/general/restaking/EIGENPOD_BEACON_CHAIN_VULNERABILITIES.md`

**Why This Matters:**
Boundary inconsistency causes proofs at the exact boundary to be accepted or rejected non-deterministically.

**Known Violations (from DB):**
- `general-defi-eigenpod-beacon-chain-vulnerabilities-6-timestamp-boundary-errors-005`

---

### STAKING-BEACON-007: Validator Double-Verification Prevention

**Property (English):**
Each validator's balance proof must be processable only once per proof window/epoch. Re-submitting the same proof (or a proof for the same validator at the same checkpoint) must be rejected.

**Property (Formal):**
$$\forall v, \text{checkpoint}(c): \text{verified}(v, c) = \text{true} \implies \text{revert}(\text{verifyProof}(v, c))$$

**Mode:** NEGATIVE
**Priority:** HIGH
**Multi-Call:** YES
**Universality:** CONDITIONAL (requires beacon chain proof checkpoints)

**Conditions:**
- Applies to checkpoint-style proof verification systems
- Must track per-validator-per-checkpoint verification status

**Source Evidence:**
- Protocol: EigenLayer | File: `src/contracts/pods/EigenPod.sol` (verifyCheckpointProofs)

**Why This Matters:**
Double verification inflates the reported balance, allowing excess withdrawals or share minting.

---

### STAKING-BEACON-008: Withdrawal Credential Validation

**Property (English):**
When verifying a validator via beacon chain proof, the withdrawal credentials must point to the expected EigenPod (or equivalent contract). Accepting a proof for a validator whose withdrawal credentials point elsewhere allows claiming ownership of another entity's validator.

**Property (Formal):**
$$\forall \text{verify}(v, \text{pod}): \text{withdrawalCredentials}(v) = \text{address}(\text{pod})$$

**Mode:** POSITIVE
**Priority:** CRITICAL
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires withdrawal credential binding)

**Conditions:**
- Applies to any contract that validates beacon chain validator ownership
- Must check 0x01 prefix withdrawal credentials match the contract address

**Source Evidence:**
- Protocol: EigenLayer | File: `src/contracts/pods/EigenPod.sol`
- Ethereum Consensus Spec: Withdrawal credentials format

**Why This Matters:**
Without credential validation, anyone can claim any validator by providing a valid proof for someone else's validator.

---

### STAKING-BEACON-009: Attestation Timeliness and Freshness

**Property (English):**
Attestation data used for validation (e.g., beacon state roots, validator set commitments) must not be older than a defined freshness threshold. Stale attestations may reference a state that no longer reflects current validator balances or statuses.

**Property (Formal):**
$$\forall \text{attestation}(a): \text{block.timestamp} - a.\text{timestamp} \leq \text{MAX\_ATTESTATION\_AGE}$$

**Mode:** POSITIVE
**Priority:** HIGH
**Multi-Call:** NO
**Universality:** UNIVERSAL

**Conditions:**
- Applies to any system consuming attestation or beacon state data
- MAX_ATTESTATION_AGE must account for finality delay (~13 minutes on Ethereum)
- Must reject attestations from before the last finalized epoch

**Source Evidence:**
- Ethereum Consensus Spec: Attestation validity rules
- Protocol: Avail, EigenLayer attestation services

**Why This Matters:**
Stale attestations can reference pre-slashing balances or pre-exit validator states, causing incorrect accounting.

---

### STAKING-BEACON-010: Active Validator Set Consistency

**Property (English):**
The on-chain tracked set of active validators must be consistent with the beacon chain state. When a validator exits, is slashed, or becomes inactive on the beacon chain, the on-chain record must be updated within the proof/checkpoint cycle.

**Property (Formal):**
$$\forall v \in \text{trackedValidators}: \text{beaconStatus}(v, t) = \text{exited} \implies \text{onChainStatus}(v, t + \text{PROOF\_CYCLE}) = \text{exited}$$

**Mode:** POSITIVE
**Priority:** MEDIUM
**Multi-Call:** NO
**Universality:** CONDITIONAL (requires on-chain validator tracking)

**Conditions:**
- Applies to protocols that maintain an on-chain validator registry
- Update lag must be bounded by proof cycle duration

**Source Evidence:**
- Protocol: EigenLayer, Lido (node operator registry)

**Why This Matters:**
Stale validator records inflate reported staking power, affecting reward distribution and governance weight.
