---
# Core Classification
protocol: generic
chain: everychain
category: zk_proof_verification
vulnerability_type: missing_verification|fiat_shamir_weakness|vk_root_untrusted|randomness_bias|witness_leakage

# Attack Vector Details
attack_type: proof_forgery|zkp_bypass|economic_exploit|privacy_violation
affected_component: on_chain_verifier|fiat_shamir_challenge|verification_key|randomness_generation

# Technical Primitives
primitives:
  - plonk_verifier
  - groth16_verifier
  - fiat_shamir
  - verification_key
  - recursive_proof
  - vk_root
  - logup
  - zkLogin
  - randomness
  - challenge
  - witness_privacy
  - on_chain_verification

# Impact Classification
severity: critical
impact: proof_forgery|fund_theft|privacy_violation|economic_exploit
exploitability: 0.25
financial_impact: critical

# Context Tags
tags:
  - zk_rollup
  - proof_system
  - groth16
  - plonk
  - stark
  - fiat_shamir
  - verification_key
  - recursion
  - zkLogin
  - sui_move
  - on_chain_verifier

language: solidity|rust|circom|move
version: all

# Pattern Identity (Required)
root_cause_family: weak_randomness
pattern_key: weak_randomness | on_chain_verifier | missing_verification

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - challenge
  - execute
  - executeZkLogin
  - fiat_shamir
  - groth16_verifier
  - logup
  - on_chain_verification
  - plonk_verifier
  - randomness
  - recursive_proof
  - verification_key
  - verify
  - verifyWithTrustedVK
  - vk_root
  - witness_privacy
  - zkLogin
---

## References & Source Reports

### Missing / Bypassed On-Chain Verification

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing On-Chain ZK Proof Verification (zkLogin) | `reports/zk_rollup_findings/missing-on-chain-zk-proof-verification.md` | HIGH | Quantstamp |
| Potential Economic Gain via False Proofs | `reports/zk_rollup_findings/potential-economic-gain-when-submitting-false-proofs.md` | HIGH | Multiple |

### Cryptographic Weaknesses in Proof Systems

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect Randomness Computation Allows Proof Forgery | `reports/zk_rollup_findings/incorrect-randomness-computation-allows-proof-forgery.md` | HIGH | Trail of Bits |
| Plonk/Groth16 Verifiers Accept Untrusted Recursion VK Root | `reports/zk_rollup_findings/m-01-plonkgroth16-verifiers-accept-proofs-with-untrusted-recursion-vk-root.md` | MEDIUM | Spearbit |
| Weak Fiat-Shamir in LogUp Phase | `reports/zk_rollup_findings/weak-fiat-shamir-implementation-for-the-logup-phase-allows-crafting-backdoored-c.md` | HIGH | Trail of Bits |
| Malicious Verifier Recovers Private Witness Values | `reports/zk_rollup_findings/m-4-malicious-verifier-will-recover-private-witness-values-breaking-zero-knowled.md` | MEDIUM | Multiple |
| Unbounded Decimal Public Inputs Enable Verifier-Side DoS | `reports/zk_rollup_findings/m-07-unbounded-decimal-public-inputs-enable-verifier-side-dos-via-oversized-nume.md` | MEDIUM | Multiple |
| Public Verifier API Panics on Malformed Inputs | `reports/zk_rollup_findings/m-04-public-verifier-api-panics-on-malformed-inputs-enabling-dos.md` | MEDIUM | Multiple |

---

## Vulnerability Title

**ZK Proof Verification Weaknesses — Missing Checks, Fiat-Shamir Flaws, and Untrusted Verification Keys**

### Overview

ZK proof verification vulnerabilities occur when on-chain or off-chain verifiers fail to fully validate proofs. This includes completely skipping verification, using weak randomness in Fiat-Shamir transforms, accepting proofs with attacker-controlled verification keys, and leaking private witness data to the verifier. These bugs break the core security properties of ZK systems: soundness (false → unacceptable), zero-knowledge (privacy), and completeness.

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of weak_randomness"
- Pattern key: `weak_randomness | on_chain_verifier | missing_verification`
- Interaction scope: `single_contract`
- Primary affected component(s): `on_chain_verifier|fiat_shamir_challenge|verification_key|randomness_generation`
- High-signal code keywords: `challenge`, `execute`, `executeZkLogin`, `fiat_shamir`, `groth16_verifier`, `logup`, `on_chain_verification`, `plonk_verifier`
- Typical sink / impact: `proof_forgery|fund_theft|privacy_violation|economic_exploit`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: On-chain randomness derived from block.timestamp, block.number, or blockhash
- Signal 2: Randomness source observable by miners/validators before commitment
- Signal 3: No commit-reveal or VRF scheme for random number generation
- Signal 4: Seed is predictable or manipulable by transaction ordering

#### False Positive Guards

- Not this bug when: Chainlink VRF or similar verifiable randomness is used
- Safe if: Commit-reveal scheme with sufficient delay prevents prediction
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

ZK proof verification bugs arise from:
1. **Missing verification**: Code branches that unconditionally set `is_verified = true` without checking a ZK proof
2. **Weak randomness**: Fiat-Shamir challenges derived from insufficient entropy (predictable, biasable)
3. **Untrusted VK root**: Recursive proof systems where the prover-supplied verification key root is not validated against a trusted on-chain constant
4. **Private witness leakage**: Deterministic challenge generation allows the verifier to reverse-engineer private inputs
5. **Input validation gaps**: Verifier API panics or reverts on malformed proofs, enabling DoS

---

### Pattern 1: Missing On-Chain ZK Proof Verification

**Frequency**: 1/8 reports | **Validation**: Strong (Dipcoin Perpetual - Quantstamp)

#### Attack Scenario

1. Protocol uses an off-chain/hybrid ZK authentication scheme (e.g., zkLogin on Sui/Move)
2. The on-chain `verify_signature()` function checks the scheme byte
3. When `scheme == SIGNED_USING_ZK_WALLET (3)`, the function sets `is_verified = true` WITHOUT validating any ZK proof on-chain
4. Any off-chain bug in the ZK verification pipeline makes authentication completely bypassable
5. Attacker submits any signature claiming `SIGNED_USING_ZK_WALLET` to bypass authentication for any user account

**Example 1: zkLogin Bypass via Missing On-Chain Verification** [HIGH]

```move
// ❌ VULNERABLE: library.move - verify_signature()
fun verify_signature(scheme: u8, public_key: vector<u8>, sig: vector<u8>, msg: vector<u8>): bool {
    let is_verified = false;
    if (scheme == ECDSA_SCHEME) {
        is_verified = ecdsa_verify(&sig, &public_key, &msg);
    } else if (scheme == ED25519_SCHEME) {
        is_verified = ed25519_verify(&sig, &public_key, &msg);
    } else if (scheme == SIGNED_USING_ZK_WALLET) {
        // ❌ No ZK proof verification here!
        // Public key is accepted unconditionally
        is_verified = true;  // BUG: any public_key accepted for zkLogin
    };
    is_verified
}
```

**Fix:**
```move
// ✅ SECURE: Verify ZK proof on-chain for zkLogin scheme
} else if (scheme == SIGNED_USING_ZK_WALLET) {
    // Verify the zkLogin proof against the public key on-chain
    is_verified = zklogin_verify_proof(&sig, &public_key, &msg);
};
```

---

### Pattern 2: Incorrect Randomness Computation Allows Proof Forgery

**Frequency**: 1/8 reports | **Validation**: Strong (Trail of Bits)

#### Root Cause

In interactive proof systems converted to non-interactive via Fiat-Shamir, the "random" challenge must be derived from all previous transcript values. If the randomness computation is incorrect — for example, hashing the wrong subset of committed values, using a predictable seed, or allowing the prover to influence entropy — the prover can bias challenges to craft valid proofs for false statements.

#### Attack Scenario

1. Prover generates multiple commitments and includes them in the transcript
2. The Fiat-Shamir challenge is computed as `H(C1, C2, ...)` but due to a bug, some `Ci` are excluded
3. Prover searches for commitment values where the resulting challenge `c` satisfies their desired proof equation
4. Since the challenge computation is incomplete/predictable, the search space is reduced from the full field to a tractable subset
5. Attacker produces a valid-looking proof for an incorrect statement

**Example 2: Biased Fiat-Shamir Challenge** [HIGH]
```rust
// ❌ VULNERABLE: Incorrect randomness — missing some commitments in transcript
fn compute_challenge(
    commitment_a: Fr,
    commitment_b: Fr,
    // BUG: commitment_c is also part of the relation but excluded here
) -> Fr {
    let mut transcript = Transcript::new();
    transcript.append_point(commitment_a);
    transcript.append_point(commitment_b);
    // MISSING: transcript.append_point(commitment_c);
    transcript.challenge()  // Challenge is predictable if attacker controls C_c
}
```

**Fix:**
```rust
// ✅ SECURE: Include ALL public commitments in the Fiat-Shamir transcript
fn compute_challenge_secure(
    commitment_a: Fr,
    commitment_b: Fr,
    commitment_c: Fr,  // Must include ALL commitments
    public_inputs: &[Fr],
) -> Fr {
    let mut transcript = Transcript::new();
    transcript.append_point(commitment_a);
    transcript.append_point(commitment_b);
    transcript.append_point(commitment_c);
    for pi in public_inputs { transcript.append_scalar(*pi); }
    transcript.challenge()
}
```

---

### Pattern 3: Plonk/Groth16 Verifiers Accept Untrusted Recursion VK Root

**Frequency**: 1/8 reports | **Validation**: Moderate (Spearbit)

#### Root Cause

In recursive proof systems (e.g., Groth16 with Fflonk recursion, Plonk with proof composition), the inner verifier circuit uses a "verification key root" to identify which set of circuits is being verified. If the on-chain verifier accepts this VK root as **prover-supplied input** rather than checking it against a hard-coded trusted constant, a malicious prover can supply a different VK root pointing to a different (malicious) circuit that accepts false proofs.

**Example 3: Untrusted VK Root** [MEDIUM]
```solidity
// ❌ VULNERABLE: On-chain Groth16 verifier accepts prover-supplied VK root
function verify(
    uint256[2] calldata proof_a,
    uint256[2][2] calldata proof_b,
    uint256[2] calldata proof_c,
    uint256[] calldata public_inputs  // public_inputs[0] = vk_root (attacker-controlled!)
) external returns (bool) {
    // vk_root is part of public inputs → attacker provides their own VK root
    // pointing to a circuit that accepts any false statement
    return groth16Verifier.verify(proof_a, proof_b, proof_c, public_inputs);
}
```

**Fix:**
```solidity
// ✅ SECURE: Hard-code the trusted VK root; reject proofs with different roots
bytes32 immutable TRUSTED_VK_ROOT;

function verify(
    uint256[2] calldata proof_a,
    uint256[2][2] calldata proof_b,
    uint256[2] calldata proof_c,
    uint256[] calldata public_inputs
) external returns (bool) {
    // Enforce vk_root matches the TRUSTED constant
    require(bytes32(public_inputs[0]) == TRUSTED_VK_ROOT, "Untrusted VK root");
    return groth16Verifier.verify(proof_a, proof_b, proof_c, public_inputs);
}
```

---

### Pattern 4: Weak Fiat-Shamir in LogUp Phase Enables Backdoored Circuits

**Frequency**: 1/8 reports | **Validation**: Strong (Trail of Bits)

#### Root Cause

LogUp (a lookup argument used in STARK/Plonky2 proofs) uses Fiat-Shamir to generate challenges for the LogUp sum-check. If the prover can influence the LogUp challenge — for example, by choosing values in committed polynomials that bias the challenge toward specific values — they can craft proofs that pass for incorrect lookups, breaking the lookup table soundness.

**Example 4: LogUp Challenge Weakness** [HIGH]
```rust
// ❌ VULNERABLE: LogUp challenge uses only partial transcript
// Prover can choose their committed multiplicity polynomial values to
// influence the Fiat-Shamir challenge, then forge the LogUp relation
fn logup_challenge(
    committed_values: &[Fr],
) -> Fr {
    // MISSING: Prover's commitments to the multiplicity polynomial
    // are not included, allowing bias
    hash_to_field(&[committed_values.len() as u64])
}
```

---

### Pattern 5: Verifier-Side DoS via Unbounded Public Inputs

**Frequency**: 1/8 reports | **Validation**: Moderate

#### Root Cause

ZK verifier contracts or APIs that accept public inputs as `uint256` decimal strings (rather than validated field elements) may not check that values are less than the field prime. Supplying a value ≥ field prime forces arithmetic operations to panic (in Rust due to overflow/assertion) or consume excessive gas (in Solidity), causing DoS.

**Example 5: Oversized Public Input** [MEDIUM]
```rust
// ❌ VULNERABLE: verify() panics on inputs ≥ field prime
pub fn verify(proof: &Proof, public_inputs: &[BigUint]) -> bool {
    for input in public_inputs {
        // MISSING: input < FIELD_PRIME check
        let field_elem = Fr::from(input.clone()); // panics if input >= prime
    }
    // ...
}
```

**Fix:**
```rust
// ✅ SECURE: Validate all public inputs are valid field elements
pub fn verify(proof: &Proof, public_inputs: &[BigUint]) -> bool {
    for input in public_inputs {
        require!(input < &FIELD_PRIME, "Public input out of field range");
        let field_elem = Fr::from(input.clone());
    }
    // ...
}
```

---

### Pattern 6: Malicious Verifier Recovers Private Witness Values

**Frequency**: 1/8 reports | **Validation**: Moderate

#### Root Cause

In some ZK proof systems (particularly those using interactive protocols or weak Fiat-Shamir), a verifier that can choose its own challenges can extract private witness values. This breaks the zero-knowledge property. If the challenge is deterministic given the prover's first message, the verifier pre-computes the response and uses the algebraic relationship between response and witness to recover private data.

**Example 6: Witness Recovery via Deterministic Challenge** [MEDIUM]
```rust
// ❌ VULNERABLE: Challenge is fully determined by commitment (no verifier randomness)
// Malicious verifier pre-computes: challenge = H(commitment)
// Then recovers: witness = (response - challenge * r) / something
// where r is the blinding factor (also recoverable)
fn verify_schnorr_like(
    commitment: G1,
    response: Fr,
    witness: Fr  // LEAKED: response = r + challenge * witness
) -> bool {
    let challenge = H(commitment);  // deterministic
    // response = r + c * witness → reverse: witness = (response - r) / c
    commitment == G1::generator() * response - public_key * challenge
}
```

---

### Impact Analysis

#### Technical Impact
- Soundness broken → attacker proves false statements on-chain
- Zero-knowledge broken → private transaction data exposed
- Chain-wide state corruption possible in zkEVM if verifier is bypassed
- Gas DoS possible via unbounded decimal public input panics

#### Business Impact
- Funds stolen via false proof of ownership/balance claims
- User privacy violations (wallet addresses, transaction amounts exposed)
- Protocol halt via DoS on verifier API
- Regulatory/legal exposure for privacy-promise-breaking protocols

#### Affected Scenarios
- Any protocol using zkLogin, zkWallet, or off-chain ZK authentication
- Groth16/Plonk verifiers with recursive proof composition
- STARK-based systems using LogUp lookup arguments
- Fiat-Shamir based non-interactive proofs

---

### Secure Implementation

**Fix 1: Always Verify ZK Proofs On-Chain**
```solidity
// ✅ SECURE: Never accept ZK-authenticated actions without on-chain proof check
function executeZkLogin(
    address user,
    bytes calldata proof,
    bytes calldata publicKey,
    bytes calldata message
) external {
    // On-chain ZK proof verification — never skip this
    require(
        zkLoginVerifier.verifyProof(proof, publicKey, message),
        "ZK proof verification failed"
    );
    // Only execute after verified
    _execute(user);
}
```

**Fix 2: Hard-Code Trusted Verification Keys**
```solidity
// ✅ SECURE: Immutable VK prevents prover from substituting their own circuit
contract ZkVerifier {
    bytes32 public immutable CIRCUIT_VK_HASH;  // Set at deployment, never mutable
    
    constructor(bytes32 _vkHash) {
        CIRCUIT_VK_HASH = _vkHash;
    }
    
    function verifyWithTrustedVK(
        Proof calldata proof,
        uint256[] calldata publicInputs
    ) external view returns (bool) {
        // Verify VK hash matches the trusted circuit
        require(publicInputs[0] == uint256(CIRCUIT_VK_HASH), "Untrusted circuit");
        return _verifier.verify(proof, publicInputs);
    }
}
```

---

### Detection Patterns

```
1. verify_signature() function with conditional branch setting is_verified = true without proof check
2. Fiat-Shamir transcript that doesn't include ALL committed polynomials/values
3. Recursive verifier accepting VK root as public input without comparing to hardcoded constant
4. BigUint/decimal input parsing without field prime bounds check
5. Challenge = H(only_first_message) — look for missing second-round commitments in transcript
6. "acknowledged" / "off-chain verification" comments in ZK auth code
```

### Keywords for Search

`missing ZK proof verification`, `zkLogin bypass`, `Fiat-Shamir weakness`, `biased challenge`, `verification key root untrusted`, `recursion VK manipulation`, `Groth16 unsafe`, `Plonk verifier bypass`, `LogUp soundness`, `witness extraction`, `zero-knowledge broken`, `proof forgery`, `on-chain verification skipped`, `ZK authentication bypass`, `STARK verification DoS`, `unbounded public input`, `field prime overflow`, `Plonk trusted setup`, `recursive proof security`, `zk circuit soundness`

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`challenge`, `execute`, `executeZkLogin`, `fiat_shamir`, `groth16`, `groth16_verifier`, `logup`, `missing_verification|fiat_shamir_weakness|vk_root_untrusted|randomness_bias|witness_leakage`, `on_chain_verification`, `on_chain_verifier`, `plonk`, `plonk_verifier`, `proof_system`, `randomness`, `recursion`, `recursive_proof`, `stark`, `sui_move`, `verification_key`, `verify`, `verifyWithTrustedVK`, `vk_root`, `witness_privacy`, `zkLogin`, `zk_proof_verification`, `zk_rollup`
