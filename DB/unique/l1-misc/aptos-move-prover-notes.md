---
protocol: aptos-core-move
chain: aptos
category: virtual_machine
vulnerability_type: vm_safety_invariants

root_cause_family: unsafe_vm_semantics
pattern_key: missing_bounds_invariant | move_vm_native | deep_recursion_or_overflow | crash_or_corruption

interaction_scope: single_contract
involved_contracts:
  - move-vm (interpreter/native functions)
  - move-prover (boogie pipeline)
path_keys:
  - missing_bounds_invariant | move_vm interpreter | deep_recursion | stack_overflow
  - unverified_native_assumptions | move-prover boogie pipeline | soundness_gap

attack_type: data_manipulation
affected_component: move virtual machine

primitives:
  - bytecode interpreter
  - recursion bounds
  - native function assumptions
  - formal verification (boogie)
  - monomorphization / code injection (prover pipeline)

code_keywords:
  - move_vm
  - interpreter
  - recursion
  - bounds
  - native functions
  - boogie
  - move-prover
  - monomorphization

severity: medium
impact: dos
tags:
  - move
  - aptos
  - vm
  - formal_verification
  - node_software
language: move
version: "docs snapshot (move-mono move-docs vm-security-and-correctness; move-prover report 2023-24)"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [VMSEC] | reports/other-l1_findings/aptos-core-third-party-move-mono-move-docs-vm-security-and-correctness-md.md | — (spec) | Move team (docs) | "VM Security & Correctness" — memory/recursion/bounds invariants |
| [PROV] | reports/other-l1_findings/aptos-core-third-party-move-move-prover-doc-report-main-impl-pdf.md | — (spec) | Move team | "Towards Practical Formal Verification" — prover architecture incl. transformations, injection, monomorphization |

## Aptos Move VM — Recursion/Bounds Safety Invariants and Prover-Soundness Notes (Reference Entry)

### Overview

Move's own security documentation defines the core VM invariants auditors must check Move-based chains against: recursion depth and arithmetic bounds are "difficult" invariants enforced at the interpreter/native boundary; the Move prover's Boogie pipeline (transformations, injection, monomorphization) is the layer where verification soundness can silently break. This entry records the hunt surface for Move VM audits rather than a single exploit.

#### Agent Quick View

- Root cause statement: "Move VM safety depends on interpreter-enforced bounds (recursion depth, arithmetic, pointer/global-memory invariants); node crashes or worse follow when native functions or bytecode paths assume these invariants rather than enforce them, and the prover can mask regressions when its transformation pipeline diverges from VM semantics."
- Pattern key: `missing_bounds_invariant | move_vm_native | deep_recursion_or_overflow | crash_or_corruption`
- Interaction scope: `single_contract` (VM internals) 
- Primary affected component(s): `move-vm interpreter, native functions, move-prover`
- Contracts / modules involved: `move-vm, move-prover (boogie backend)`
- High-signal code keywords: `interpreter`, `native functions`, `recursion`, `boogie`, `monomorphization`
- Typical sink / impact: `node crash (DoS) via deep recursion/arithmetic edge; false verification passes hiding real bugs`
- Validation strength: `moderate` (derived from Move team documentation, not a third-party finding)

#### Contract / Boundary Map

- Entry surface(s): any transaction executing Move bytecode; native function calls; prover runs in CI
- Contract hop(s): `Move bytecode -> move-vm interpreter -> native function implementations; Move source -> prover transformations -> Boogie`
- Trust boundary crossed: `bytecode (untrusted user code) -> VM (trusted) -> native layer (assumed safe)`
- Shared state or sync assumption: `prover model of VM semantics must match actual VM semantics`

#### Valid Bug Signals

- Signal 1: A native function performs recursion or slicing without explicit depth/length asserts, relying on caller guarantees
- Signal 2: Interpreter loop handling recursion depth treats depth as u64 without cap, or arithmetic on sizes can overflow before bounds check
- Signal 3: Prover pipeline changes (new transformation/injection step) land without soundness regression tests

#### False Positive Guards

- Not this bug when: bounds are enforced inside the native function itself, not by callers
- Safe if: recursion limits and max-value checks are VM-enforced constants applied uniformly
- Requires attacker control of: crafted Move bytecode/module (any user can publish modules on permissionless chains)

### Vulnerability Description

#### Root Cause

The Move VM docs (VMSEC) state that memory safety, transaction effects, and "difficult invariants" around recursion, bounds, arithmetic, and pointer/global storage are the core correctness obligations of the VM. Historically these are exactly where Move-family bugs cluster: deep recursion in deserialization/interpreter (stack overflow → node crash), missing bounds in native helpers, and arithmetic on user-controlled sizes. The prover report (PROV) documents the verification pipeline (transformations → injection → monomorphization → Boogie) whose fidelity determines whether verified code is actually safe.

#### Attack Scenario / Path Variants

**Path A: Deep recursion crash**
Path key: `missing_bounds_invariant | move_vm interpreter | deep_recursion`
1. Attacker publishes a Move module with deeply nested structures/calls within each allowed limit
2. Interpreter or a native helper recurses per nesting level without a hard depth cap
3. Node stack overflows; process crashes
4. Repeatable → liveness DoS on validators/execution nodes

**Path B: Native assumption mismatch**
Path key: `unverified_native_assumptions | native functions | invariant_divergence`
1. Native function trusts that bytecode-level checks already validated input sizes
2. A path (e.g., a new bytecode instruction or an upgrade) skips the bytecode check
3. Native layer processes out-of-bounds input → panic or memory corruption
4. Node crash or state corruption

**Path C: Prover soundness gap (developer-side)**
Path key: `prover_pipeline_divergence | move-prover | false_pass`
1. Transformation/injection step models semantics imprecisely (e.g., monomorphization corner cases)
2. Prover verifies the model, not the real VM behavior
3. Bug ships "verified" code that violates the intended invariant

#### Vulnerable Pattern Examples

**Example 1: Uncapped recursion in a native/interpreter helper** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE (pattern): recursion over user-controlled nesting with no depth cap
fn deserialize_nested(buf: &mut impl Buf) -> Value {
    let tag = buf.get_u8();
    match tag {
        SIGN_STRUCT => deserialize_nested(buf), // depth unbounded
        // ...
    }
}
```

**Example 2: Arithmetic before bounds check** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE (pattern): size arithmetic can overflow before the bounds assert
let total = header.len_field + body.len_field; // u64 overflow wraps
assert!(total <= MAX); // checked too late / on wrapped value
```

**Example 3: Native trusting bytecode-level validation** [Approx Vulnerability : MEDIUM]
```rust
// ❌ VULNERABLE (pattern): native assumes the verifier already bounded inputs
pub unsafe fn native_vector_borrow(args: &[NativeArg]) -> Value {
    let idx = args[1].as_u64() as usize; // verifier check skipped on this path
    args[0].borrow(idx) // OOB
}
```

### Impact Analysis

#### Technical Impact
- Node crashes (liveness DoS) from crafted modules/transactions
- Potential memory-safety failures in native layer (worst case)
- Verified-but-broken code if prover model diverges

#### Business Impact
- Chain liveness incidents; emergency hard forks; loss of confidence in Move safety claims

#### Affected Scenarios
- Any Move-VM chain (Aptos, Sui variants) after VM upgrades or new native functions
- Framework upgrades adding transformations to the prover pipeline

### Secure Implementation

**Fix 1: Enforce bounds at the enforcement point**
```rust
// ✅ SECURE: hard depth cap and checked arithmetic inside the recursing function
fn deserialize_nested(buf: &mut impl Buf, depth: u32) -> Result<Value> {
    ensure!(depth < MAX_DEPTH, E_DEPTH);
    let total = header.checked_add(body)?; // checked arithmetic before assert
    // ...
}
```

**Fix 2: Soundness regression suite for the prover**
```text
// ✅ SECURE: every prover transformation (injection, monomorphization, ...) carries
// differential tests: known-buggy modules must FAIL verification; known-safe must pass
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- move_vm
- interpreter.rs
- native functions
- recursion
- MAX_DEPTH
- boogie
- monomorphization
- move-prover
```

#### Code Patterns to Look For
```
- Recursive descent over user-controlled structures without a depth parameter
- usize casts of u64 user input
- Native functions documented as "assumes input verified elsewhere"
- Prover PRs adding transformations without corresponding soundness tests
```

#### Audit Checklist
- [ ] Grep the VM/native layer for recursion; verify each has a hard cap
- [ ] Check all size arithmetic for checked/overflow semantics
- [ ] Diff native-function assumptions against actual bytecode verifier guarantees
- [ ] For prover changes: confirm differential/soundness tests exist

### Real-World Examples

#### Related Reports
- Move documentation: "VM Security & Correctness" (memory, transaction effects, recursion bounds invariants)
- Move prover report: "Towards Practical Formal Verification" (architecture: transformations, injection, monomorphization → Boogie)

### Keywords for Search

`aptos`, `move`, `move vm`, `interpreter`, `native functions`, `recursion`, `stack overflow`, `bounds check`, `arithmetic overflow`, `move prover`, `boogie`, `formal verification`, `monomorphization`, `code injection`, `node crash`, `dos`, `sui`, `bytecode verifier`

### Related Vulnerabilities

- DB/unique/l1-misc/aptos-move-fund-pending-transactions.md (application-level Move bugs)
- DB/unique/l1-misc/avalanche-avalanchego-codec-recursion.md (Go recursion-depth DoS analogue)
