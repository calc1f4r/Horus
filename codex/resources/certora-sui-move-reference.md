<!-- AUTO-GENERATED from `.claude/resources/certora-sui-move-reference.md`; source_sha256=1a88a1c801c2eb64151b87b49d2c77441bc79bf05eb7b65cc648ef53d8f2cd80 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/certora-sui-move-reference.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Certora Sui Move Prover Reference

## Contents
- [CVLM type system](#cvlm-type-system)
- [Manifest functions](#manifest-functions)
- [Assertion primitives](#assertion-primitives)
- [Nondeterminism](#nondeterminism)
- [Ghost state](#ghost-state)
- [Shadow mappings](#shadow-mappings)
- [Hash functions](#hash-functions)
- [Parametric rules](#parametric-rules)
- [MathInt (arbitrary precision)](#mathint-arbitrary-precision)
- [Summaries](#summaries)
- [Platform summaries (certora_sui_summaries)](#platform-summaries)
- [Spec package setup (Move.toml)](#spec-package-setup)
- [CLI options](#cli-options)
- [Known pitfalls and mitigations](#known-pitfalls-and-mitigations)

---

## CVLM Type System

Specs for the Certora Sui Prover are written in Move, not CVL. The specification library is `cvlm` (CVL-Move).

### Core CVLM modules

| Module | Purpose |
|--------|---------|
| `cvlm::manifest` | Declares rules, summaries, ghosts, targets, invokers, shadows, hashes, field/function accessors |
| `cvlm::asserts` | `cvlm_assert`, `cvlm_assume_msg`, `cvlm_satisfy`, `cvlm_satisfy_msg`, `cvlm_assert_msg` |
| `cvlm::nondet` | `nondet<T>()` for nondeterministic values, `nondet_with` macro for constrained nondet |
| `cvlm::ghost` | `ghost_write`, `ghost_read`, `ghost_destroy` for manipulating ghost references |
| `cvlm::function` | `Function` struct for parametric rules, with `name()`, `module_name()`, `module_address()` |
| `cvlm::math_int` | `MathInt` arbitrary-precision integer with arithmetic operations |
| `cvlm::conversions` | `u256_to_address` conversion utility |
| `cvlm::internal_asserts` | `cvlm_internal_assert`, `cvlm_internal_assume` (for internal use) |

---

## Manifest Functions

Every CVLM spec module declares a `cvlm_manifest()` function that registers rules, summaries, ghosts, etc.

```move
module spec::rules;

use cvlm::manifest::{rule, no_abort_rule, summary, ghost, target, invoker, target_sanity, hash, shadow, field_access, function_access};

public fun cvlm_manifest() {
    // Declare a rule
    rule(b"my_rule_name");

    // Declare a rule that also asserts no aborts
    no_abort_rule(b"my_no_abort_rule");

    // Declare a summary replacing target_module::target_function
    summary(b"my_summary_fn", @target_pkg, b"target_module", b"target_function");

    // Declare a ghost variable/mapping
    ghost(b"my_ghost_fn");

    // Register target functions for parametric rules
    target(@target_pkg, b"module_name", b"function_name");

    // Register an invoker for parametric rules
    invoker(b"invoke");

    // Auto-generate sanity rules for all targets
    target_sanity();

    // Declare a hash function
    hash(b"my_hash_fn");

    // Declare a shadow mapping
    shadow(b"my_shadow_fn");

    // Declare a field accessor
    field_access(b"my_field_accessor", b"field_name");

    // Declare a function accessor
    function_access(b"my_fn_accessor", @target_pkg, b"target_module", b"target_fn");
}
```

### Manifest function reference

| Function | Purpose |
|----------|---------|
| `rule(name)` | Marks a function as a verification rule |
| `no_abort_rule(name)` | Rule that also asserts no code invoked by it can abort |
| `summary(name, addr, module, fn)` | Replaces a function body with a summary |
| `ghost(name)` | Declares a ghost variable/mapping function |
| `target(addr, module, fn)` | Registers a target function for parametric rules |
| `invoker(name)` | Names the function that invokes targets in parametric rules |
| `target_sanity()` | Auto-generates sanity rules for all registered targets |
| `hash(name)` | Declares a hash function returning unique u256 per arguments |
| `shadow(name)` | Replaces a struct's internal representation with a mapping |
| `field_access(name, field)` | Declares a field accessor for platform struct fields |
| `function_access(name, addr, module, fn)` | Declares access to a private function |

---

## Assertion Primitives

```move
use cvlm::asserts::{cvlm_assert, cvlm_assert_msg, cvlm_satisfy, cvlm_satisfy_msg, cvlm_assume_msg};

// Assert a condition (rule fails if false)
cvlm_assert(balance >= initial_balance);
cvlm_assert_msg(balance >= initial_balance, b"Balance must not decrease");

// Satisfy: ask the prover to find a state where condition is true (non-vacuity check)
cvlm_satisfy(true);
cvlm_satisfy_msg(true, b"Reached end of function");

// Assume: constrain the prover's search space
cvlm_assume_msg(amount > 0, b"Non-zero amount");
```

---

## Nondeterminism

```move
use cvlm::nondet::{nondet, nondet_with};

// Unconstrained nondeterministic value
let amount: u64 = nondet<u64>();

// Constrained nondeterministic value (with assumption)
let valid_amount: u64 = nondet_with(b"valid amount", |v| v > 0 && v < 1000000);
```

---

## Ghost State

Ghost variables/mappings provide global state for rules and summaries.

```move
// In manifest:
ghost(b"my_ghost_mapping");

// Declare as native function (returns reference for mappings, value for scalars):
native fun my_ghost_mapping(key: address): &mut u64;

// Read ghost value:
let val = cvlm::ghost::ghost_read(my_ghost_mapping(addr));

// Write ghost value:
cvlm::ghost::ghost_write(my_ghost_mapping(addr), new_value);

// Destroy value without drop ability:
cvlm::ghost::ghost_destroy(old_value);
```

Key points:
- Ghost mappings are initialized nondeterministically for each rule
- A ghost with no arguments acts as a global variable
- A ghost with arguments acts as a mapping
- Apply both `ghost` and `summary` to get `NONDET`-like behavior

---

## Shadow Mappings

Replace a struct's internal representation with a mapping for easier reasoning.

```move
// In manifest:
shadow(b"vec_map_shadow");

// Declare the shadow function:
native fun vec_map_shadow<K: copy, V>(map: &VecMap<K, V>, key: &K): &mut V;
```

Requirements:
- First parameter must be a reference to the shadowed struct
- Must return a reference type
- Generic shadows must match the struct's type parameters
- Any function that packs, unpacks, or accesses fields of the shadowed struct must be summarized

---

## Hash Functions

Unique u256 values computed from arguments.

```move
// In manifest:
hash(b"foo_to_u256");

// Declare:
native fun foo_to_u256<T>(x: &T): u256;
```

---

## Parametric Rules

Test a property against ALL registered target functions.

```move
public fun cvlm_manifest() {
    target(@my_pkg, b"module_a", b"func_1");
    target(@my_pkg, b"module_a", b"func_2");
    target(@my_pkg, b"module_b", b"func_3");
    invoker(b"invoke");
    rule(b"property_holds_for_all_functions");
}

// The invoker must be a native function. First param is Function, rest forwarded.
native fun invoke(target: Function, arg1: &mut MyStruct);

public fun property_holds_for_all_functions(
    state: &mut MyStruct,
    target: Function
) {
    let before = get_value(state);
    invoke(target, state);
    let after = get_value(state);
    cvlm_assert(after >= before);
    cvlm_satisfy(true);
}
```

The prover generates one sub-rule per (rule x target) combination.

### Function introspection

```move
use cvlm::function::Function;

let fn_name: vector<u8> = target.name();
let mod_name: vector<u8> = target.module_name();
let mod_addr: address = target.module_address();
```

---

## MathInt (Arbitrary Precision)

```move
use cvlm::math_int::MathInt;

// Construction
let a = MathInt::from_u64(42);
let b = MathInt::from_u256(value);
let z = MathInt::zero();
let o = MathInt::one();

// Arithmetic (never overflows)
let sum = MathInt::add(a, b);
let diff = MathInt::sub(a, b);
let prod = MathInt::mul(a, b);
let quot = MathInt::div(a, b);
let rem = MathInt::mod(a, b);
let power = MathInt::pow(a, b);

// Comparisons
MathInt::lt(a, b);  // <
MathInt::le(a, b);  // <=
MathInt::gt(a, b);  // >
MathInt::ge(a, b);  // >=

// Utilities
MathInt::max(a, b);
MathInt::min(a, b);
MathInt::neg(a);
MathInt::abs(a);

// Convert back
let result: u64 = MathInt::to_u64(sum);
let result256: u256 = MathInt::to_u256(sum);
```

---

## Summaries

Replace complex logic (e.g., loops) with logical approximations.

### Writing a summary

1. Expose needed fields via `#[test_only]` accessors in the target contract
2. Write the summary function in the spec package
3. Register in manifest with `summary()`

```move
// In manifest:
summary(b"find_idx_summary", @target_pkg, b"module_name", b"find_idx");

// Summary function (must be #[test_only]):
#[test_only]
public fun find_idx_summary(state: &MyStruct, target_value: u64): u64 {
    let result = nondet<u64>();
    cvlm_assume_msg(
        result <= state.items().length() &&
        (result == 0 || state.get_value(result - 1) > target_value),
        b"valid index"
    );
    result
}
```

### Ghost-as-summary (NONDET equivalent)

Apply both `ghost` and `summary` to the same function:
```move
ghost(b"nondet_external_call");
summary(b"nondet_external_call", @external_pkg, b"module", b"function");
```

---

## Platform Summaries

The `certora_sui_summaries` package provides pre-built summaries for Sui standard library and framework functions.

### Available summary modules

| Module | Covers |
|--------|--------|
| `std_ascii_summaries` | ASCII string operations |
| `std_bcs_summaries` | BCS serialization |
| `std_debug_summaries` | Debug printing |
| `std_num_summaries` | Power functions |
| `std_option_summaries` | Option type operations |
| `std_string_summaries` | UTF-8 string operations |
| `std_type_name_summaries` | Type name introspection |
| `std_vector_summaries` | Vector operations |
| `sui_address_summaries` | Address utilities |
| `sui_bcs_summaries` | Sui BCS operations |
| `sui_dynamic_field_summaries` | Dynamic fields |
| `sui_ecdsa_k1_summaries` | ECDSA secp256k1 |
| `sui_event_summaries` | Event emission |
| `sui_hash_summaries` | Hash functions |
| `sui_hex_summaries` | Hex encoding/decoding |
| `sui_object_summaries` | Object lifecycle (delete tracking) |
| `sui_system_sui_system_summaries` | Sui system operations |
| `sui_transfer_summaries` | Object transfer |
| `sui_tx_context_summaries` | Transaction context |
| `sui_vec_map_summaries` | VecMap operations |
| `sui_vec_set_summaries` | VecSet operations |

---

## Spec Package Setup

### Move.toml template

```toml
[package]
name = "spec"
edition = "2024.beta"

[dependencies]
# The contract being verified
my_contract = { local = "../path/to/contract" }
# CVLM specification library
cvlm = { git = "https://github.com/Certora/cvl-move-proto.git", subdir = "cvlm", rev = "main" }
# Sui platform summaries
certora_sui_summaries = { git = "https://github.com/Certora/cvl-move-proto.git", subdir = "certora_sui_summaries", rev = "main" }

[addresses]
spec = "0x0"
```

### Directory structure

```
project/
├── sources/           # Target contract sources
│   └── my_module.move
├── Move.toml          # Target contract manifest
└── spec/              # Verification specs
    ├── Move.toml      # Spec package manifest (see template above)
    └── sources/
        ├── rules.move
        ├── summaries.move
        └── ...
```

---

## CLI Options

### Running verification

```bash
# Basic run (from spec/ directory containing Move.toml)
certoraSuiProver.py --server production --prover_version "master"

# With verbose setup logging (recommended initially)
certoraSuiProver.py --java_args "-Dverbose.setup.helpers" --server production --prover_version "master"

# Run specific rules only
certoraSuiProver.py --rule my_rule_name --server production --prover_version "master"

# Exclude specific rules
certoraSuiProver.py --excludeRule slow_rule --server production --prover_version "master"

# Run for specific methods only
certoraSuiProver.py --method "module::function" --server production --prover_version "master"

# Exclude specific methods
certoraSuiProver.py --excludeMethod "module::helper" --server production --prover_version "master"
```

### Key CLI flags

| Flag | Purpose |
|------|---------|
| `--server production` | Use production Certora server |
| `--prover_version "master"` | Use latest prover version |
| `--rule <name>` | Verify only named rules |
| `--excludeRule <name>` | Skip named rules |
| `--method <module::fn>` | Verify only for named methods |
| `--excludeMethod <module::fn>` | Skip named methods |
| `--java_args "-Dverbose.setup.helpers"` | Verbose setup logging |

---

## Known Pitfalls and Mitigations

| Problem | Symptoms | Mitigation |
|---------|----------|------------|
| **Missing summaries** | Prover error on unsummarized platform calls | Add platform summaries from `certora_sui_summaries`, or write custom summaries |
| **Vacuous rules** | Rule passes trivially | Always include `cvlm_satisfy(true)` or `cvlm_satisfy_msg` in every rule |
| **Abort soundness in no_abort_rule** | Rule passes but actual function can abort | Ensure summaries accurately model abort behavior |
| **Shadowed struct access** | Prover error on field access of shadowed type | Summarize all functions that pack, unpack, or access fields of shadowed structs |
| **Ghost initialization** | Unexpected counterexamples | Ghost mappings are initialized nondeterministically — add `cvlm_assume_msg` constraints |
| **Loop timeouts** | Prover times out on unbounded loops | Write summaries to replace loops with logical approximations |
| **Missing test_only accessor** | Cannot access private fields from spec | Add `#[test_only]` accessor functions in the target contract |
| **Edition mismatch** | Build errors | Use `edition = "2024.beta"` in spec Move.toml |
| **Dependency resolution** | Move build fails | Ensure target contract path in Move.toml is correct, check `sui move build` works |
| **Nondeterministic overconstrain** | No valid witness for satisfy | Reduce `cvlm_assume_msg` constraints, check for contradictory assumptions |
