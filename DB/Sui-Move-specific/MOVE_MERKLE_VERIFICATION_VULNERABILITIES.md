---
protocol: generic
chain: sui, aptos, movement
category: merkle_verification
vulnerability_type: proof_replay, verification_bypass, return_value_unchecked, missing_domain_separation
attack_type: fund_theft, unlimited_claims, proof_forgery
affected_component: merkle_tree, proof_verification, airdrop_claim, token_distribution
primitives:
  - merkle_proof
  - airdrop
  - token_distribution
  - hash_verification
  - leaf_index
  - domain_separation
severity: critical
impact: fund_loss, unlimited_claims
exploitability: 0.9
financial_impact: critical
tags:
  - move
  - sui
  - aptos
  - movement
  - merkle
  - proof
  - airdrop
  - verification
  - replay
  - hash
  - token_distribution
  - claim
language: move
version: all
---

## References
| # | Source | Protocol | Auditor | Severity |
|---|--------|----------|---------|----------|
| [R1] | reports/ottersec_move_audits/markdown/ethsign_merkle_token_distributor_audit_final.md | EthSign | OtterSec | CRITICAL |
| [R2] | reports/ottersec_move_audits/markdown/movement_merkle_airdrop_audit_final.md | Movedrop L2 | OtterSec | CRITICAL |

## Move Merkle Proof Verification Vulnerabilities

**Comprehensive patterns for Merkle proof replay, verification bypass, unchecked return values, and domain separation issues in Move-based airdrop and token distribution contracts across Aptos and Movement chains.**

### Overview

Merkle verification vulnerabilities are among the most severe findings in OtterSec Move audits. All 4 findings are rated CRITICAL or HIGH, found across 2 independent protocols. The consequences are catastrophic — complete drainage of airdrop/distribution funds. Move lacks a standard OpenZeppelin-equivalent Merkle library, so teams build custom implementations that frequently contain fundamental logic errors.

### Vulnerability Description

#### Root Cause Categories

1. **Proof replay** — Leaf index not included in hash, allowing proof reuse with different indices
2. **Verification logic flaw** — Comparison function misused, accepting wrong proof results
3. **Return value unchecked** — Verification function called but result not asserted
4. **Fee bypass** — Edge case in fee calculation returns 0 at maximum setting

---

## Pattern 1: Merkle Proof Replay via Missing Index in Hash — move-merkle-001

**Frequency**: 1/29 reports (Movedrop L2 [R2])
**Severity consensus**: CRITICAL
**Validation**: Weak — single protocol, but CRITICAL with universal applicability

### Attack Scenario
1. User has a valid Merkle proof for their allocation at leaf index N
2. Leaf hash = hash(address, amount) — index NOT included
3. Attacker resubmits the same proof with a different leaf index M
4. Since hash doesn't include index, verification passes for any index
5. Attacker claims allocation multiple times (once per index in the tree)

### Vulnerable Pattern Example

**Movedrop L2 — Leaf Index Not in Hash** [CRITICAL] [R2]
```move
// ❌ VULNERABLE: leaf_index not part of the leaf hash
public fun claim(
    user: &signer,
    airdrop: &mut AirdropConfig,
    leaf_index: u64,
    amount: u64,
    proof: vector<vector<u8>>,
) {
    let user_addr = signer::address_of(user);
    
    // ❌ Leaf hash does NOT include leaf_index
    let leaf = hash::sha3_256(bcs::to_bytes(&user_addr) + bcs::to_bytes(&amount));
    
    // Verify proof against root
    assert!(verify_merkle_proof(airdrop.root, leaf, proof, leaf_index), E_INVALID_PROOF);
    
    // Mark claimed using leaf_index as key
    assert!(!table::contains(&airdrop.claimed, leaf_index), E_ALREADY_CLAIMED);
    table::add(&mut airdrop.claimed, leaf_index, true);
    
    // ❌ Same proof works for ANY leaf_index since hash doesn't include it
    // Attacker: claim(index=0, proof), claim(index=1, proof), claim(index=2, proof)...
    transfer_tokens(airdrop, user_addr, amount);
}
```

### Secure Implementation
```move
// ✅ SECURE: Include leaf_index in hash to prevent replay
public fun claim(
    user: &signer,
    airdrop: &mut AirdropConfig,
    leaf_index: u64,
    amount: u64,
    proof: vector<vector<u8>>,
) {
    let user_addr = signer::address_of(user);
    
    // ✅ Leaf hash includes ALL claim parameters including index
    let leaf_data = vector::empty<u8>();
    vector::append(&mut leaf_data, bcs::to_bytes(&leaf_index));
    vector::append(&mut leaf_data, bcs::to_bytes(&user_addr));
    vector::append(&mut leaf_data, bcs::to_bytes(&amount));
    let leaf = hash::sha3_256(leaf_data);
    
    assert!(verify_merkle_proof(airdrop.root, leaf, proof, leaf_index), E_INVALID_PROOF);
    assert!(!table::contains(&airdrop.claimed, leaf_index), E_ALREADY_CLAIMED);
    table::add(&mut airdrop.claimed, leaf_index, true);
    
    transfer_tokens(airdrop, user_addr, amount);
}
```

---

## Pattern 2: Flawed Merkle Proof Verification Logic — move-merkle-002

**Frequency**: 1/29 reports (Movedrop L2 [R2])
**Severity consensus**: CRITICAL
**Validation**: Weak — single protocol, but severe and widely applicable

### Attack Scenario
1. Custom `compare_vectors` returns 0 (less), 1 (equal), 2 (greater)
2. Verification checks if computed hash < root (return value == 0)
3. Should check if computed hash == root (return value == 1)
4. ANY hash that is lexicographically less than root passes verification
5. Effectively no verification — attacker constructs any valid claim

### Vulnerable Pattern Example

**Movedrop L2 — Wrong Comparison Return Value** [CRITICAL] [R2]
```move
// ❌ VULNERABLE: Checks less-than instead of equal
public fun verify_merkle_proof(
    root: vector<u8>,
    computed_hash: vector<u8>,
    proof: vector<vector<u8>>,
    index: u64,
): bool {
    let i = 0;
    let current = computed_hash;
    
    while (i < vector::length(&proof)) {
        let sibling = vector::borrow(&proof, i);
        if (index % 2 == 0) {
            current = hash::sha3_256(current + *sibling);
        } else {
            current = hash::sha3_256(*sibling + current);
        };
        index = index / 2;
        i = i + 1;
    };
    
    // ❌ compare_vectors returns: 0=less, 1=equal, 2=greater
    // Should check == 1 (equal), but checks == 0 (less than)
    compare_vectors(&current, &root) == 0
    // Returns true when computed_hash < root, NOT when equal
    // Most random hashes will be < root ~50% of the time
}
```

### Secure Implementation
```move
// ✅ SECURE: Check equality, not ordering
public fun verify_merkle_proof(
    root: vector<u8>,
    computed_hash: vector<u8>,
    proof: vector<vector<u8>>,
    index: u64,
): bool {
    let current = computed_hash;
    let i = 0;
    
    while (i < vector::length(&proof)) {
        let sibling = vector::borrow(&proof, i);
        if (index % 2 == 0) {
            current = hash::sha3_256(current + *sibling);
        } else {
            current = hash::sha3_256(*sibling + current);
        };
        index = index / 2;
        i = i + 1;
    };
    
    // ✅ Check exact equality
    current == root
}
```

---

## Pattern 3: Unchecked Merkle Verification Return Value — move-merkle-003

**Frequency**: 1/29 reports (EthSign [R1])
**Severity consensus**: CRITICAL
**Validation**: Weak — single protocol, but CRITICAL universal pattern

### Attack Scenario
1. Merkle `verify()` function is called with proof data
2. Return value (bool) is NOT asserted or checked
3. Function returns false for invalid proofs, but execution continues
4. Anyone can submit any proof — all pass regardless of validity
5. Complete drainage of all distribution funds

### Vulnerable Pattern Example

**EthSign — Return Value Not Asserted** [CRITICAL] [R1]
```move
// ❌ VULNERABLE: Verification result ignored
public fun claim(
    user: &signer,
    distributor: &mut Distributor,
    amount: u64,
    proof: vector<vector<u8>>,
) {
    let user_addr = signer::address_of(user);
    let leaf = compute_leaf(user_addr, amount);
    
    // ❌ CRITICAL: Return value discarded!
    // Verification runs but result is NOT checked
    merkle::verify(distributor.root, leaf, proof);
    // Should be: assert!(merkle::verify(...), E_INVALID_PROOF);
    
    // Execution continues regardless of proof validity
    assert!(!is_claimed(distributor, user_addr), E_ALREADY_CLAIMED);
    mark_claimed(distributor, user_addr);
    
    // ❌ Invalid proof accepted — anyone can claim any amount
    let signer = get_distribution_signer(distributor.addr);
    primary_fungible_store::transfer(&signer, distributor.token, user_addr, amount);
}
```

### Secure Implementation
```move
// ✅ SECURE: Assert verification result
public fun claim(
    user: &signer,
    distributor: &mut Distributor,
    amount: u64,
    proof: vector<vector<u8>>,
) {
    let user_addr = signer::address_of(user);
    let leaf = compute_leaf(user_addr, amount);
    
    // ✅ ASSERT the return value
    assert!(merkle::verify(distributor.root, leaf, proof), E_INVALID_PROOF);
    
    assert!(!is_claimed(distributor, user_addr), E_ALREADY_CLAIMED);
    mark_claimed(distributor, user_addr);
    
    let signer = get_distribution_signer(distributor.addr);
    primary_fungible_store::transfer(&signer, distributor.token, user_addr, amount);
}
```

---

## Pattern 4: Fee Bypass at Maximum Fee Setting — move-merkle-004

**Frequency**: 1/29 reports (EthSign [R1])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol

### Vulnerable Pattern Example

**EthSign — MAX_FEE_BIPS Returns Zero Fee** [HIGH] [R1]
```move
// ❌ VULNERABLE: Edge case at maximum fee setting
const MAX_FEE_BIPS: u64 = 10000;  // 100%
const BIPS_PRECISION: u64 = 10000;

public fun calculate_fee(amount: u64, fee_bips: u64): u64 {
    if (fee_bips == MAX_FEE_BIPS) {
        // ❌ Special case returns 0 instead of full amount
        // Distributors set fee to MAX_FEE_BIPS to pay no fees
        return 0
    };
    (amount * fee_bips) / BIPS_PRECISION
}
```

### Secure Implementation
```move
// ✅ SECURE: MAX_FEE_BIPS returns full amount as fee
public fun calculate_fee(amount: u64, fee_bips: u64): u64 {
    assert!(fee_bips <= MAX_FEE_BIPS, E_INVALID_FEE);
    (amount * fee_bips) / BIPS_PRECISION
    // When fee_bips == 10000: returns amount * 10000 / 10000 = amount (100% fee)
}
```

---

### Impact Analysis

#### Technical Impact
- Complete drainage of all airdrop/distribution funds (3/4 findings) — CRITICAL
- Unlimited token claims per valid proof holder
- Verification completely bypassed (any caller, any proof, any amount)
- Fee revenue entirely bypassed at specific setting

#### Business Impact
- Total loss of distribution funds (EthSign: all distributor funds, Movedrop: all airdrop tokens)
- Token sell pressure from fraudulent claims
- Protocol reputation destroyed
- Legal liability from lost user allocations

#### Affected Scenarios
- Airdrop claim contracts (Movedrop L2)
- Token distribution platforms (EthSign)
- Any Move contract implementing custom Merkle verification
- Vesting/cliff claim systems with Merkle-based eligibility

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `hash(address, amount)` without leaf_index in airdrop claims
- Pattern 2: `compare_vectors(...) == 0` or `!= 0` in proof verification (should check == 1 or use ==)
- Pattern 3: `merkle::verify(root, leaf, proof)` without `assert!()` wrapper
- Pattern 4: `if (fee_bips == MAX)` with special-case return 0
- Pattern 5: Custom `verify_merkle_proof` that doesn't check final hash == root
```

#### Audit Checklist
- [ ] Leaf hash includes ALL claim parameters (index, address, amount, nonce)
- [ ] Merkle verification checks hash EQUALITY (not less-than or greater-than)
- [ ] `verify()` return value always wrapped in `assert!()`
- [ ] Fee calculation works correctly at boundary values (0, MAX, MAX-1)
- [ ] Claimed status uses address-based or unique key, not reusable index
- [ ] Domain separator included in leaf hash (prevents cross-contract proof reuse)

### Keywords for Search

> `merkle proof`, `merkle tree`, `airdrop claim`, `proof replay`, `leaf index`, `verify_merkle_proof`, `compare_vectors`, `hash`, `sha3_256`, `proof verification`, `return value`, `unchecked return`, `token distribution`, `claim`, `domain separation`, `fee bypass`, `MAX_FEE_BIPS`, `move merkle`, `aptos airdrop`, `movement airdrop`

### Related Vulnerabilities

- [MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md](MOVE_ACCESS_CONTROL_AUTHORIZATION_VULNERABILITIES.md) — Signer capability exposure in distributors
- [MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md](MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md) — Excessive claims pattern
