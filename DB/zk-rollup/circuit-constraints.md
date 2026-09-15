---
# Core Classification
protocol: generic
chain: everychain
category: zk_circuit
vulnerability_type: underconstrained_circuit|missing_constraint|arithmetic_overflow|hash_constraint

# Attack Vector Details
attack_type: proof_forgery|state_manipulation|execution_hijack
affected_component: circuit_constraints|pil_file|zkasm|air_constraints|binary_state_machine

# Technical Primitives
primitives:
  - PIL
  - zkasm
  - polynomial_identity_language
  - constraint_system
  - binary_state_machine
  - range_check
  - carry_bit
  - div_opcode
  - shr_opcode
  - comparison_circuit
  - JALR
  - SHA256_AIR
  - partial_sha256
  - hash_state
  - final_hash

# Impact Classification
severity: critical
impact: proof_forgery|fund_theft|state_corruption|execution_hijack
exploitability: 0.30
financial_impact: critical

# Context Tags
tags:
  - zk_rollup
  - circuit_audit
  - zkEVM
  - PIL
  - boojum
  - plonky2
  - polygon_zkevm
  - zkSync
  - scroll
  - soundness
  - underconstrained
  - missing_range_check

language: rust|circom|plonk|PIL
version: all

# Pattern Identity (Required)
root_cause_family: arithmetic_error
pattern_key: arithmetic_error | circuit_constraints | underconstrained_circuit

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - JALR
  - PIL
  - SHA256_AIR
  - binary_state_machine
  - borrow
  - carry_bit
  - comparison_circuit
  - constraint_system
  - div_opcode
  - final_hash
  - hash_state
  - partial_sha256
  - polynomial_identity_language
  - range_check
  - shr_opcode
  - zkasm
---

## References & Source Reports

### Missing PIL / AIR Constraints

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Fake SMT Inclusion via Missing PIL Constraint | `reports/zk_rollup_findings/2-missing-constraint-in-pil-leading-to-proving-fake-inclusion-in-the-smt.md` | CRITICAL | Trail of Bits |
| Execution Flow Hijack via Missing PIL Constraint | `reports/zk_rollup_findings/4-missing-constraint-in-pil-leading-to-execution-flow-hijack.md` | CRITICAL | Trail of Bits |
| Random Ether Addition via Incorrect ctx Assignment | `reports/zk_rollup_findings/3-incorrect-ctx-assignation-leading-to-addition-of-random-amount-of-ether-to-the.md` | CRITICAL | Trail of Bits |
| MaxMem Bug Halts Batch Verification | `reports/zk_rollup_findings/5-bug-in-maxmem-handling-can-halt-the-batch-verification.md` | HIGH | Trail of Bits |
| Underconstrained Carry in Binary State Machine | `reports/zk_rollup_findings/underconstrained-carry-value-in-the-binary-state-machine.md` | CRITICAL | Trail of Bits |

### Opcode Arithmetic Constraints

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Missing Range Constraint on DIV Remainder | `reports/zk_rollup_findings/h-01-missing-range-constraint-on-remainder-check-in-div-opcode-implementation.md` | HIGH | ChainLight |
| Missing Range Constraint on SHR Remainder | `reports/zk_rollup_findings/h-04-missing-constraint-on-remainder-in-shr-opcode-implementation.md` | HIGH | ChainLight |
| Insufficient Division Remainder Check | `reports/zk_rollup_findings/insufﬁcient-check-about-division-remainder.md` | HIGH | Multiple |
| pow_u32 Exponentiation for Even Exponent | `reports/zk_rollup_findings/incorrect-implementation-of-pow_u32-exponentiation-for-even-exponent.md` | HIGH | Multiple |

### RISC-V / VM Circuit Constraints

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| IsLtArraySubAir Soundness Issue | `reports/zk_rollup_findings/isltarraysubairis-unsound.md` | HIGH | Nethermind |
| JALR imm_sign Unconstrained | `reports/zk_rollup_findings/jalr-imm_signis-unconstrained.md` | HIGH | Nethermind |

### Hash Circuit Constraints

| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| SHA256 AIR Unconstrained final_hash at Last Block | `reports/zk_rollup_findings/sha256-air-doesnt-constrain-final_hash-at-the-last-block-but-this-value-is-read-.md` | HIGH | Nethermind |
| partial_sha256_var_interstitial Hash Collision | `reports/zk_rollup_findings/partial_sha256_var_interstitial-may-give-the-same-hash-state-h-for-different-dat.md` | HIGH | Multiple |

---

## Vulnerability Title

**ZK Circuit Under-Constraints and Missing Constraint Vulnerabilities**

### Overview

ZK circuit vulnerabilities occur when constraint systems (PIL, AIR, Boojum, Plonky2, RISC-V circuits) fail to fully constrain intermediate or output values, allowing a malicious prover to generate valid proofs for false statements. These are some of the most critical bugs in ZK systems — they fundamentally break the soundness guarantee of the proof system, enabling state forgery, funds theft, and execution hijacking.

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of arithmetic_error"
- Pattern key: `arithmetic_error | circuit_constraints | underconstrained_circuit`
- Interaction scope: `single_contract`
- Primary affected component(s): `circuit_constraints|pil_file|zkasm|air_constraints|binary_state_machine`
- High-signal code keywords: `JALR`, `PIL`, `SHA256_AIR`, `binary_state_machine`, `borrow`, `carry_bit`, `comparison_circuit`, `constraint_system`
- Typical sink / impact: `proof_forgery|fund_theft|state_corruption|execution_hijack`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `air_constraints.function -> binary_state_machine.function -> circuit_constraints.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Arithmetic operation on user-controlled input without overflow protection
- Signal 2: Casting between different-width integer types without bounds check
- Signal 3: Multiplication before division where intermediate product can exceed type max
- Signal 4: Accumulator variable can wrap around causing incorrect accounting

#### False Positive Guards

- Not this bug when: Solidity >= 0.8.0 with default checked arithmetic
- Safe if: SafeMath library used for all arithmetic on user-controlled values
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

In ZK proof systems, soundness requires that **every wire and intermediate value be fully constrained** by the circuit's polynomial identities. When a constraint is missing or incomplete, an adversary (typically the prover/sequencer) can assign arbitrary witness values that satisfy the remaining constraints while producing an incorrect computation result.

The root cause is typically:
- A computation result that is allocated (`alloc_without_values`) but never range-checked
- A carry, flag, or borrow bit whose range (`{0, 1}`) is not constrained
- A hash gadget that reads a column value at a row where the column is unconstrained
- A comparison circuit that can output `false` when the mathematical answer is `true`
- An opcode immediate (sign extension) whose sign bit is not enforced

---

### Pattern 1: Missing PIL Constraint for SMT Inclusion

**Frequency**: 1/431 reports | **Validation**: Strong (Polygon zkEVM)

#### Attack Scenario

1. Attacker targets a PIL constraint file (e.g., `storage.pil`) that verifies Sparse Merkle Tree inclusion proofs
2. Due to a missing polynomial identity, the prover can assign witness values that satisfy all present constraints while encoding a false inclusion proof
3. The resulting ZK proof verifies on-chain despite the false state claim
4. Attacker proves ownership/balance that does not exist → drains funds

**Example 1: Missing SMT Inclusion Constraint (PIL)** [CRITICAL]
```pil
// ❌ VULNERABLE: storage.pil - Missing constraint on SMT sibling node relationship
// The constraint ensuring that sibling_hash is correctly derived from the path
// is absent, allowing an attacker to forge arbitrary inclusion proofs

pol commit root, key, value, sibling;
pol commit hashed_sibling;

// Missing: constraint that hashed_sibling = Hash(sibling) when level is correct
// Without this, prover can assign hashed_sibling = root directly
```

**Fix:**
```pil
// ✅ SECURE: Add constraint ensuring sibling relationship is enforced at each level
pol commit inclusion_valid;
// Enforce: hashed_sibling must equal the hash of the actual sibling at each tree level
inclusion_valid * (hashed_sibling - poseidon(sibling_left, sibling_right)) = 0;
```

---

### Pattern 2: Underconstrained Carry Value in Binary State Machine

**Frequency**: 1/431 reports | **Validation**: Strong (Polygon zkEVM)

#### Attack Scenario

1. The binary state machine processes bitwise operations (AND, OR, XOR)
2. The carry bit between operations is allocated as a witness variable but **never constrained to {0, 1}**
3. An adversary sets carry = arbitrary field element, causing any bitwise operation to produce an attacker-chosen result
4. This allows bypassing any condition check relying on bitwise ops

**Example 2: Underconstrained Carry** [CRITICAL]
```pil
// ❌ VULNERABLE: binary.pil - carry bit not range-constrained
pol commit carry;         // carry should be in {0, 1}
pol commit result;
pol commit op_a, op_b;

// Constraint enforces: result = op_a XOR op_b + carry*2
// BUT carry is never constrained to {0, 1} → can be any field element!
result = op_a + op_b - 2*carry;  // missing: carry*(1-carry) = 0
```

**Fix:**
```pil
// ✅ SECURE: Add Boolean constraint on carry
carry * (1 - carry) = 0;   // Forces carry ∈ {0, 1}
result = op_a + op_b - 2*carry;
```

---

### Pattern 3: Missing Range Constraint on Division Remainder (zkEVM Opcode)

**Frequency**: 2/431 reports (DIV + SHR) | **Validation**: Strong (zkSync Era - ChainLight)

#### Root Cause

When implementing integer division (`a / b = q, remainder r`) in a ZK circuit, the standard approach allocates witness variables for `q` and `r`, then constrains: `q * b + r = a`. A critical additional constraint `0 ≤ r < b` must also be enforced. If the range constraint on `r` is missing, an adversary can assign `r = field.max` or any arbitrary value that still satisfies `q * b + r ≡ a (mod p)`.

#### Attack Scenario

1. Adversary crafts a transaction that performs a specific division (e.g., `SHR r1, 1`)
2. The witness generation produces incorrect `quotient = 0` for a specially crafted value (e.g., `1337`)
3. The circuit accepts this proof because `quotient * divisor + remainder ≡ dividend (mod p)` holds with an alternative assignment
4. The L2 VM executes the incorrect result while the ZK proof verifies on-chain
5. State computed by the sequencer diverges from what the circuit proves

**Example 3: Missing Remainder Range Check** [HIGH]
```rust
// ❌ VULNERABLE: zkevm_circuits/src/main_vm/opcodes/mul_div.rs
// allocate_div_result_unchecked - no constraint that 0 ≤ remainder < divisor
pub fn allocate_div_result_unchecked<F: SmallField, CS: ConstraintSystem<F>>(
    cs: &mut CS,
    a: &[UInt32<F>; 8],  // dividend
    b: &[UInt32<F>; 8],  // divisor
) -> ([UInt32<F>; 8], [UInt32<F>; 8]) {
    let quotient = cs.alloc_multiple_variables_without_values::<8>();
    let remainder = cs.alloc_multiple_variables_without_values::<8>();
    // Only constrains: quotient * b + remainder = a
    // MISSING: 0 ≤ remainder < b
    (quotient, remainder)
}
```

**Fix:**
```rust
// ✅ SECURE: Add range constraint: remainder < divisor
pub fn allocate_div_result_checked<F: SmallField, CS: ConstraintSystem<F>>(
    cs: &mut CS,
    a: &[UInt32<F>; 8],
    b: &[UInt32<F>; 8],
) -> ([UInt32<F>; 8], [UInt32<F>; 8]) {
    let (quotient, remainder) = allocate_div_result_unchecked(cs, a, b);
    // REQUIRED: enforce remainder < divisor
    // borrow = 1 means remainder < divisor (b - remainder > 0)
    let (_, borrow) = sub_with_borrow(cs, &remainder, b);
    Boolean::enforce_true(cs, &borrow);  // borrow=1 ↔ remainder < divisor
    (quotient, remainder)
}
```

---

### Pattern 4: IsLtArraySubAir Soundness Issue (RISC-V Circuit)

**Frequency**: 1/431 reports | **Validation**: Strong (Valida zkVM - Nethermind)

#### Root Cause

The `IsLtArraySubAir` circuit is supposed to compare two arrays lexicographically and output `true` if the first is strictly less than the second. The circuit tracks a `diff_marker` that selects the first position where a difference occurs. If the `diff_marker` can be satisfied even when it points to a position that does NOT differ (e.g., position 0 when all elements are equal), then `out = false` can be proven for `x < y`.

**Example 4: Unsound Comparison Circuit** [HIGH]
```rust
// ❌ VULNERABLE: IsLtArraySubAir
// diff_marker constraint can be satisfied even when position[0] is equal
// Allows proving (x < y) == false when x < y is true
fn eval<AB: AirBuilder>(&self, builder: &mut AB) {
    // ... diff_marker selects first differing position
    // Bug: accepts diff_marker[0] = 1 even if a[0] == b[0]
    // Attacker sets diff_marker[0] = 1, out = false, passes all constraints
}
```

**Fix:**
```rust
// ✅ SECURE: Enforce that diff_marker[i] = 1 implies a[i] != b[i]
// Use: diff_marker[i] * (a[i] - b[i]) must be nonzero when diff_marker[i] = 1
for i in 0..N {
    // If diff_marker[i] = 1, then a[i] ≠ b[i] must hold
    builder.assert_nonzero_when(diff_marker[i], a[i] - b[i]);
}
```

---

### Pattern 5: SHA256 AIR Unconstrained final_hash at Last Block

**Frequency**: 1/431 reports | **Validation**: Strong (Valida zkVM - Nethermind)

#### Root Cause

The `sha256-air` processes input data in 64-byte blocks. The `final_hash` column is constrained to the running hash state for all blocks **except the last one**. The `sha256` chip extension then reads the `final_hash` column to extract the overall hash result. However, since `final_hash` is unconstrained at the last block row, a prover can set it to any value, producing a forged hash output.

**Example 5: SHA256 Unconstrained Output** [HIGH]
```pil
// ❌ VULNERABLE: sha256-air
// final_hash is constrained for all rows EXCEPT the last block boundary
// The sha256_chip reads final_hash at exactly the last block boundary
// → if that value is unconstrained, the prover assigns any output

// sha256_chip reads:
let hash_output = sha256_air.final_hash[last_block_row]; // UNCONSTRAINED!
```

**Fix:**
```pil
// ✅ SECURE: Add constraint at last block row
// Enforce final_hash == current_hash_state at the last block (is_last = 1)
is_last * (final_hash - current_hash_state) = 0;
// Now final_hash is constrained at the row where sha256_chip reads it
```

---

### Pattern 6: partial_sha256_var_interstitial Hash Collision (Undersized Input)

**Frequency**: 1/431 reports | **Validation**: Moderate

#### Root Cause

`partial_sha256_var_interstitial` hashes `BLOCK_SIZE * floor(N / BLOCK_SIZE)` bytes, not `N` bytes. When `N < message_size` and `N mod BLOCK_SIZE != 0`, the last incomplete block is silently dropped. Two different inputs can produce the same intermediate hash state if they differ only in the dropped bytes.

**Example 6: Dropped Trailing Bytes** [HIGH]
```rust
// ❌ VULNERABLE: partial_sha256_var_interstitial
// Only hashes floor(N/64) complete 64-byte blocks
// Remaining N mod 64 bytes are SILENTLY IGNORED
fn partial_sha256_var_interstitial(state: HashState, msg: &[u8], message_size: usize) -> HashState {
    let complete_blocks = msg.len() / BLOCK_SIZE; // drops remainder
    for block in msg.chunks(BLOCK_SIZE).take(complete_blocks) {
        state = compress(state, block);
    }
    state // bytes [complete_blocks*64 .. N] never processed
}
```

---

### Pattern 7: JALR imm_sign Unconstrained (RISC-V zkVM)

**Frequency**: 1/431 reports | **Validation**: Strong (Valida zkVM)

#### Root Cause

In the JALR opcode circuit, there is an `imm_sign` flag that controls whether the 12-bit immediate is sign-extended. This flag is declared as a witness column but is **never constrained** to match the actual sign bit of the decoded immediate. An attacker can set `imm_sign = 1` (or `0`) regardless of the true immediate value, changing any JALR jump target.

**Example 7: Unconstrained Sign Extension Flag** [HIGH]
```rust
// ❌ VULNERABLE: jalr/core.rs
// imm_sign is allocated but not constrained to match immediate[11]
// Prover can freely choose imm_sign = 0 or 1 for any instruction
let imm_sign = cs.alloc_witness();  // No constraint: imm_sign == imm[11]
let extended_imm = if imm_sign == 1 { sign_extend(imm) } else { zero_extend(imm) };
// jump_target = rs1 + extended_imm ← attacker controls extended_imm
```

**Fix:**
```rust
// ✅ SECURE: Constrain imm_sign to equal the MSB of the immediate
// imm_sign must equal bit 11 of the immediate value
builder.assert_eq(imm_sign, imm_bits[11]);
```

---

### Impact Analysis

#### Technical Impact
- **Soundness violation**: The fundamental ZK guarantee — "you can only prove true statements" — is broken
- **State forgery**: Attacker can prove arbitrary state transitions (include fake token balances, ownership claims)
- **Execution hijacking**: Incorrect opcode results can alter control flow in user transactions
- **Hash forgery**: Incorrect hashes accepted in Merkle proofs, signature verification, etc.

#### Business Impact
- **Complete fund theft**: Attacker can forge inclusion proofs to claim funds not owned
- **Chain corruption**: State divergence between L2 execution and proven state
- **Loss of ZK property**: Private witnesses may be recoverable; computational integrity is void
- **Protocol halt**: Some bugs cause the verifier/prover to crash, halting the chain

#### Affected Scenarios
- Any zkEVM, zkVM, or ZK state machine (Polygon zkEVM, zkSync Era, Scroll, Valida, etc.)
- All opcode implementations depend on correct arithmetic constraint encoding
- Hash gadgets used in Merkle proof verification, signature verification, commitment schemes

---

### Secure Implementation

**Fix 1: Always Range-Check All Allocated Witnesses**
```rust
// ✅ SECURE: After allocating any witness variable, add explicit range constraints
// For a value expected to be in [0, 2^32), add:
let x = cs.alloc_witness();
// Enforce x fits in 32 bits
cs.range_check(x, 32);

// For Boolean flags:
let flag = cs.alloc_witness();
cs.enforce_boolean(flag);  // Constrains flag ∈ {0, 1}
```

**Fix 2: Verify Circuit Completeness with a Fuzzer**
```bash
# ✅ SECURE: Use a circuit fuzzer to find underconstrained wires
# Tools: ECNE, Picus, CODA, or custom mutation fuzzing
# For each witness variable, verify that there is no alternative assignment
# that satisfies all constraints while changing the output

# Example with ECNE (Equivalence Checking for Near-Equivalent circuits):
ecne check --circuit my_circuit.r1cs --witness my_witness.wtns
```

**Fix 3: Enforce Polynomial Identities for ALL Opcode Edge Cases**
```pil
// ✅ SECURE: For division a/b = q remainder r, enforce ALL three:
// (1) q * b + r = a           (correctness)
// (2) r < b                   (remainder bound)
// (3) r ≥ 0                   (non-negative remainder, usually guaranteed by range check)

pol commit q, r, a, b, borrow;
// (1) Division identity:
q * b + r - a = 0;
// (2) Remainder bound: b - r - 1 = borrow * 2^256 + diff, where borrow ∈ {0,1}
// If borrow = 1, then r < b (subtracting r from b did not underflow)
borrow * (1 - borrow) = 0;  // Boolean constraint on borrow
```

---

### Detection Patterns

#### Code Patterns to Look For

```
1. cs.alloc_multiple_variables_without_values() or alloc_witness() NOT followed by range checks
2. Boolean/bit flags declared in PIL/circom without (flag * (1 - flag) = 0) constraint
3. Division or modulo operations where only (q*b + r == a) is checked, not (r < b)
4. Comparison circuits where the "selecting" marker isn't constrained to match actual comparison
5. Hash gadgets reading values from unconstrained rows (e.g., last block in SHA256 AIR)
6. Sign extension flags (imm_sign, is_negative, carry) allocated as witnesses without constraints
7. Memory boundary values (maxMem, ptr_offset) not constrained within valid range
8. Functions named allocate_*_unchecked that return constraint-system variables
```

#### Grep Patterns
```bash
# Find unchecked allocations in Boojum/Plonky2 circuits:
grep -r "alloc_without_values\|alloc_multiple_variables_without_values\|from_variable_unchecked" --include="*.rs"

# Find PIL files without Boolean constraints on bit variables:
grep -rn "pol commit" --include="*.pil" | grep -v "carry.*1 - carry\|flag.*(1 - flag)"

# Find division operations without borrow/range check:
grep -rn "div_mod\|divmod\|allocate_div_result" --include="*.rs" | grep -v "range_check\|borrow"
```

---

### Keywords for Search

`PIL constraint missing`, `underconstrained circuit`, `zkEVM circuit bug`, `soundness violation`, `proof forgery`, `range check missing`, `carry bit unconstrained`, `Boolean constraint`, `polynomial identity language`, `AIR constraint`, `arithmetic intermediate representation`, `zkasm vulnerability`, `div opcode remainder constraint`, `sha256 air unconstrained`, `RISC-V zkVM circuit`, `witness extraction`, `completeness vs soundness`, `circuit audit`, `boojum circuit`, `plonky2 underconstrained`, `circom underconstrained`, `JALR sign extension unconstrained`, `binary state machine PIL`, `hash gadget unconstrained column`

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

`JALR`, `PIL`, `SHA256_AIR`, `binary_state_machine`, `boojum`, `borrow`, `carry_bit`, `circuit_audit`, `comparison_circuit`, `constraint_system`, `div_opcode`, `final_hash`, `hash_state`, `missing_range_check`, `partial_sha256`, `plonky2`, `polygon_zkevm`, `polynomial_identity_language`, `range_check`, `scroll`, `shr_opcode`, `soundness`, `underconstrained`, `underconstrained_circuit|missing_constraint|arithmetic_overflow|hash_constraint`, `zkEVM`, `zkSync`, `zk_circuit`, `zk_rollup`, `zkasm`
