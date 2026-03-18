<!-- AUTO-GENERATED from `.claude/resources/sui-prover-reference.md`; source_sha256=53e64c74697b9242a762853b4b2e901131293525a3915800046f8e345a556557 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/sui-prover-reference.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Sui Prover — Specification Reference

Complete reference for writing formal verification specs with the [Asymptotic Sui Prover](https://github.com/asymptotic-code/sui-prover). Specs are written in Move alongside (or in a separate package from) the target contract.

> **Official Documentation** (authoritative source — consult when in doubt):
> - [Asymptotic Home](https://info.asymptotic.tech/) — company hub
> - [Sui Prover Overview](https://info.asymptotic.tech/sui-prover) — entry point & examples
> - [Sui Prover Reference](https://info.asymptotic.tech/sui-prover-reference) — canonical spec API (`requires`, `ensures`, `asserts`, `old!`, ghost variables, loop invariants, attributes)
> - [Sui Prover FAQ](https://info.asymptotic.tech/sui-prover-faq) — composition, abort specs, compile errors, `no_opaque`, `ignore_abort`, `focus`

> **Note on `clone!` vs `old!`**: The official reference uses `old!(pool)` to capture pre-call state. This file uses `clone!(ref)` which is an equivalent alias. Both are valid; prefer `old!` when following the official docs.

---

## Installation

```bash
brew install asymptotic-code/sui-prover/sui-prover
```

### Move.toml Setup

The Sui Prover relies on implicit dependencies. **Remove** any direct dependencies to `Sui` and `MoveStdlib` from `Move.toml`:

```toml
# DELETE this line if present:
Sui = { git = "https://github.com/MystenLabs/sui.git", subdir = "crates/sui-framework/packages/sui-framework", rev = "framework/testnet", override = true }
```

If you need to reference Sui directly and this causes conflicts, put specs in a **separate package**.

---

## Running the Prover

Run from the directory containing `Move.toml`:

```bash
sui-prover
sui-prover --path ./my_project
sui-prover --verbose --timeout 60
```

---

## Writing Specifications

To verify a function, write a specification function annotated with `#[spec(prove)]`. The spec has the **same signature** as the function under test:

```move
#[spec(prove)]
fun my_function_spec(args): ReturnType {
    // 1. Preconditions assumed on arguments
    requires(precondition);

    // 2. Capture old state if needed
    let old_state = clone!(mutable_ref);

    // 3. Call the function under test
    let result = my_function(args);

    // 4. Postconditions that must hold
    ensures(postcondition);

    // 5. Return the result
    result
}
```

### How Specs Compose

- **Naming convention**: A spec named `<function_name>_spec` is automatically used as an opaque summary when the prover verifies other functions that call `<function_name>`. The prover substitutes the spec's `requires`/`ensures` contract instead of inlining the function body.
- **`#[spec(prove)]`**: The spec is verified by the prover. Without `prove`, the spec is not checked itself, but is still used when proving other functions that depend on it.
- **`#[spec(prove, focus)]`**: Only verify this spec (and other focused specs). Useful for debugging. **Do not commit `focus`** — it skips all non-focused specs.
- **`no_opaque`**: By default, when proving `bar_spec`, the prover uses `foo_spec` (if it exists) as an opaque summary for `foo`. Adding `#[spec(prove, no_opaque)]` forces the prover to also include the actual implementation of called functions, not just their specs.
- **Scenario specs**: A spec without the `_spec` naming convention and without a `target` attribute is a standalone scenario — it's verified but not used as a summary for other proofs.

### Cross-Module Specs

Use `target` to spec a function in a different module:

```move
module 0x43::foo_spec {
    #[spec(prove, target = foo::inc)]
    public fun inc_spec(x: u64): u64 {
        let res = foo::inc(x);
        ensures(res == x + 1);
        res
    }
}
```

To access private members/functions from a cross-module spec, add `#[spec_only]` getter functions to the target module. These are only visible to the prover, not included in regular compilation.

### Specifying Abort Conditions

Specs must comprehensively describe when a function aborts. Use `asserts` for this:

```move
fun foo(x: u64, y: u64): u64 {
    assert!(x < y);
    x
}

#[spec(prove)]
fun foo_spec(x: u64, y: u64): u64 {
    asserts(x < y);  // foo aborts unless x < y
    let res = foo(x, y);
    res
}
```

For **overflow aborts**, cast to a wider type in the assertion:

```move
#[spec(prove)]
fun add_spec(x: u64, y: u64): u64 {
    asserts((x as u128) + (y as u128) <= (u64::max_value!() as u128));
    let res = add(x, y);
    res
}
```

To **skip abort checking** entirely, use `ignore_abort`:

```move
#[spec(prove, ignore_abort)]
fun add_spec(x: u64, y: u64): u64 {
    let res = add(x, y);
    ensures(res == x + y);
    res
}
```

### Putting Specs in a Separate Package

Currently, specs may cause compile errors when placed alongside regular Move code due to prover-specific changes in the compilation pipeline. If this happens, create a separate package for specs and use the `target` attribute to reference functions in the original package.

---

## Core Specification Functions

Import with `use prover::prover::*`:

| Function | Description |
|----------|-------------|
| `requires(condition)` | Precondition assumed on arguments |
| `ensures(condition)` | Postcondition that must hold after the call |
| `asserts(condition)` | Assert condition is true, or function aborts |
| `clone!(ref)` | Capture a snapshot of a reference's value at this point |
| `implies(p, q)` | Logical implication (`!p \|\| q`) |
| `forall!<T>(\|x\| predicate(x))` | Universal quantification |
| `exists!<T>(\|x\| predicate(x))` | Existential quantification |
| `invariant!(\|\| { ... })` | Inline loop invariant (place before loop) |
| `.to_int()` | Convert primitive to unbounded `Integer` (spec-only) |
| `.to_real()` | Convert primitive to arbitrary-precision `Real` (spec-only) |
| `fresh<T>()` | Create an unconstrained value of type T |

---

## Mathematical Types (Spec-Only)

### `std::integer::Integer`

Arbitrary-precision integers. Convert from primitives using `.to_int()`:

```move
use std::integer::Integer;

#[spec(prove)]
fun integer_example_spec() {
    let a: Integer = 42u64.to_int();
    let b: Integer = 10u64.to_int();
    ensures(a.add(b) == 52u64.to_int());
    ensures(a.sub(b) == 32u64.to_int());
    ensures(a.mul(b) == 420u64.to_int());
}
```

**Methods:**

| Method | Description |
|--------|-------------|
| `add`, `sub`, `mul`, `div`, `mod` | Arithmetic operations |
| `neg`, `abs` | Negation, absolute value |
| `sqrt`, `pow` | Square root, exponentiation |
| `lt`, `gt`, `lte`, `gte` | Comparisons (return `bool`) |
| `bit_or`, `bit_and`, `bit_xor`, `bit_not` | Bitwise operations |
| `shl`, `shr` | Shift left/right |
| `is_pos`, `is_neg` | Sign checks |
| `to_u8`, `to_u64`, etc. | Convert back to primitive |
| `to_real` | Convert to Real |

**Conversions:**
- `42u64.to_int()` — unsigned interpretation
- `42u64.to_signed_int()` — signed interpretation (for two's complement)

### `std::real::Real`

Arbitrary-precision real numbers. Convert using `.to_real()`:

```move
use std::real::Real;

#[spec(prove)]
fun real_example_spec() {
    let x: Real = 16u64.to_real();
    ensures(x.sqrt() == 4u64.to_real());
    ensures(2u64.to_real().exp(3u64.to_int()) == 8u64.to_real());
}
```

**Methods:**

| Method | Description |
|--------|-------------|
| `add`, `sub`, `mul`, `div` | Arithmetic operations |
| `neg` | Negation |
| `sqrt` | Square root |
| `exp` | Exponentiation (takes Integer exponent) |
| `lt`, `gt`, `lte`, `gte` | Comparisons (return `bool`) |
| `to_integer` | Convert to Integer (truncates) |
| `to_u8`, `to_u64`, etc. | Convert to primitive (via Integer) |

### Fixed-Point Types: `Q32`, `Q64`, `Q128`

Signed fixed-point types with 32, 64, or 128 fractional bits. Import from `std::q32`, `std::q64`, `std::q128`.

```move
use std::q64::Q64;

#[spec(prove)]
fun fixed_point_example_spec(a: u64, b: u64) {
    requires(b > 0);
    let ratio: Q64 = Q64::quot(a.to_int(), b.to_int());
    ensures(ratio.floor().lte(a.to_int()));
}
```

**Methods:**

| Method | Description |
|--------|-------------|
| `quot(num, den)` | Create from fraction num/den |
| `add`, `sub`, `mul`, `div` | Arithmetic operations |
| `neg`, `abs` | Negation, absolute value |
| `sqrt`, `pow` | Square root, exponentiation |
| `lt`, `gt`, `lte`, `gte` | Comparisons (return `bool`) |
| `floor`, `ceil`, `round` | Rounding to Integer |
| `to_int`, `to_real` | Convert to Integer or Real |
| `is_pos`, `is_neg`, `is_int` | Predicates |
| `raw` | Access raw Integer representation (value * 2^bits) |

**Conversions to fixed-point:**
- `42u64.to_q32()` / `.to_q64()` / `.to_q128()` — from primitive
- `my_integer.to_q64()` — from Integer
- `my_real.to_q64()` — from Real
- `my_uq64_64.to_q64()` — from `UQ64_64`
- `my_uq32_32.to_q32()` — from `UQ32_32`
- `my_fp32.to_q32()` — from `FixedPoint32`

---

## Ghost Variables

Ghost variables are spec-only globals for propagating information between specifications. Import with `use prover::ghost::*`.

Ghost variables are declared with two type-level arguments: a key type and a value type. The key is usually a user struct or a spec-only struct:

```move
#[spec_only]
public struct MyGhostKey {}
```

### Declaring and Reading

```move
#[spec_only]
use prover::ghost::{declare_global, global};

#[spec(prove)]
fun ghost_example_spec() {
    declare_global<MyKey, bool>();
    ensures(*global<MyKey, bool>());
}
```

### Mutable Ghost Variables

```move
#[spec_only]
use prover::ghost::{declare_global_mut, borrow_mut, global};

#[spec(prove)]
fun ghost_mut_example_spec() {
    declare_global_mut<MyKey, u64>();
    let ghost_ref = borrow_mut<MyKey, u64>();
    *ghost_ref = 42;
    ensures(*global<MyKey, u64>() == 42);
}
```

### Verifying Event Emission

A common pattern: use ghost variables to verify events are emitted. The function that emits the event `requires` the ghost variable; the spec declares it and checks it with `ensures`:

```move
fun emit_large_withdraw_event() {
    event::emit(LargeWithdrawEvent { });
    requires(*global<LargeWithdrawEvent, bool>());
}

#[spec(prove)]
fun withdraw_spec<T>(pool: &mut Pool<T>, shares_in: Balance<LP<T>>): Balance<T> {
    declare_global<LargeWithdrawEvent, bool>();
    // ...
    if (shares_in_value >= LARGE_WITHDRAW_AMOUNT) {
        ensures(*global<LargeWithdrawEvent, bool>());
    };
    result
}
```

### Ghost Variables for `transfer::public_transfer`

When a spec involves `transfer::public_transfer` (directly or indirectly), declare ghost variables:

```move
#[spec_only]
use specs::transfer_spec::{SpecTransferAddress, SpecTransferAddressExists};

#[spec(prove, target = module::func_that_transfers)]
fun func_spec<T>(...) {
    ghost::declare_global_mut<SpecTransferAddress, address>();
    ghost::declare_global_mut<SpecTransferAddressExists, bool>();
    // ... rest of spec
    ensures(*ghost::global<SpecTransferAddressExists, bool>());
    ensures(*ghost::global<SpecTransferAddress, address>() == recipient);
}
```

---

## Vector Iterator Functions

Import with `use prover::vector_iter::*`:

| Function | Description |
|----------|-------------|
| `all!<T>(&vec, \|x\| pred(x))` | All elements satisfy predicate |
| `any!<T>(&vec, \|x\| pred(x))` | Any element satisfies predicate |
| `count!<T>(&vec, \|x\| pred(x))` | Count elements satisfying predicate |
| `map!<T, U>(&vec, \|x\| f(x))` | Transform vector elements |
| `filter!<T>(&vec, \|x\| pred(x))` | Filter vector elements |
| `find!<T>(&vec, \|x\| pred(x))` | Find first matching element |
| `find_index!<T>(&vec, \|x\| pred(x))` | Find index of first match |
| `find_indices!<T>(&vec, \|x\| pred(x))` | Find all matching indices |
| `sum<T>(&vec)` | Sum vector elements (returns `Integer`) |
| `sum_map!<T, U>(&vec, \|x\| f(x))` | Sum mapped elements |

All macros have `_range!` variants: `all_range!(&vec, start, end, |x| ...)`. The `sum` and `sum_range` functions are called without `!` (native functions, not macros).

Example:
```move
#[spec(prove)]
fun vector_spec() {
    let v = vector[2, 4, 6, 8];
    ensures(all!<u64>(&v, |x| is_even(x)));
    ensures(count!<u64>(&v, |x| *x > 5) == 2);
    ensures(sum(&v) == 20u64.to_int());
}
```

---

## Attributes Reference

### `#[spec(...)]` — Specification Functions

| Parameter | Description |
|-----------|-------------|
| `prove` | Verify this specification |
| `skip` | Skip verification |
| `focus` | Mark as focused (verify only focused specs). **Do not commit.** |
| `target = <PATH>` | Target external function (e.g., `target = 0x42::module::func`) |
| `include = <PATH>` | Include another spec's behavior |
| `ignore_abort` | Don't check abort conditions. Allows omitting `asserts` for aborts. |
| `no_opaque` | Include actual implementations of called functions, not just their specs. |
| `uninterpreted = <NAME>` | Treat pure function as uninterpreted |
| `extra_bpl = b"<file>"` | Load extra Boogie code |
| `boogie_opt = b"<opt>"` | Pass custom Boogie options |

Examples:
```move
#[spec(prove)]
#[spec(prove, focus)]
#[spec(prove, target = 0x42::foo::bar)]
#[spec(prove, ignore_abort)]
#[spec(prove, no_opaque)]
#[spec(prove, target = 0x42::foo::bar, include = 0x42::specs::helper_spec)]
```

### `#[ext(...)]` — Function Characteristics

| Parameter | Description |
|-----------|-------------|
| `pure` | Function is pure (deterministic, no side effects); usable in specs |
| `no_abort` | Function never aborts |
| `axiom` | Function is defined axiomatically |

Examples:
```move
#[ext(pure)]
fun max(a: u64, b: u64): u64 { if (a >= b) a else b }

#[ext(no_abort)]
fun safe_get(v: &vector<u64>, i: u64): u64 { ... }

#[ext(axiom)]
fun sqrt(x: u64): u64;  // No body, assumed correct
```

### `#[spec_only(...)]` — Specification-Only Items

Similar to `test_only`, `spec_only` makes annotated code only visible to the prover. Not included in regular compilation or test mode.

| Parameter | Description |
|-----------|-------------|
| (none) | Basic spec-only item |
| `(axiom)` | Axiom definition |
| `(inv_target = <TYPE>)` | Datatype invariant for specified type |
| `(loop_inv(target = <FUNC>))` | External loop invariant |
| `(loop_inv(target = <FUNC>, label = N))` | Loop invariant with label |
| `(include = <PATH>)` | Include spec module |
| `(extra_bpl = b"<file>")` | Load extra Boogie code |

Examples:
```move
#[spec_only]
fun helper_predicate(x: u64): bool { x > 0 }

#[spec_only(axiom)]
fun sqrt_axiom(x: u64): u64 { ... }

#[spec_only(inv_target = MyStruct)]
public fun MyStruct_inv(self: &MyStruct): bool {
    self.value > 0
}

#[spec_only(loop_inv(target = my_func_spec))]
fun loop_inv_for_my_func() { }
```

---

## Loop Invariants

Loop invariants are required when a spec has conditions over variables modified inside a loop.

### Inline Loop Invariants

Use the `invariant!` macro directly before a loop:

```move
#[spec(prove)]
fun sum_to_n_spec(n: u64): u128 {
    let mut sum: u128 = 0;
    let mut i: u64 = 0;

    invariant!(|| {
        ensures(i <= n);
        ensures(sum == (i as u128) * ((i as u128) + 1) / 2);
    });
    while (i < n) {
        i = i + 1;
        sum = sum + (i as u128);
    };

    ensures(sum == (n as u128) * ((n as u128) + 1) / 2);
    sum
}
```

### External Loop Invariants

Define loop invariants as separate functions:

```move
#[spec_only(loop_inv(target = sum_to_n_spec))]
#[ext(no_abort)]
fun sum_loop_inv(i: u64, n: u64, sum: u128): bool {
    i <= n && sum == (i as u128) * ((i as u128) + 1) / 2
}

#[spec(prove)]
fun sum_to_n_spec(n: u64): u128 {
    let mut sum: u128 = 0;
    let mut i: u64 = 0;
    while (i < n) {
        i = i + 1;
        sum = sum + (i as u128);
    };

    ensures(sum == (n as u128) * ((n as u128) + 1) / 2);
    sum
}
```

**Key points:**
- Invariant function parameters must match the loop variables
- Return a `bool` with conditions joined by `&&`
- Add `#[ext(no_abort)]` or `#[ext(pure)]` attribute
- For cloned values, use `__old_` prefix in parameter names (e.g., `__old_n` for `clone!(&n)`)
- For multiple loops, use `label = N` (0-indexed):

```move
#[spec_only(loop_inv(target = my_spec, label = 0))]
#[ext(no_abort)]
fun first_loop_inv(...): bool { ... }

#[spec_only(loop_inv(target = my_spec, label = 1))]
#[ext(no_abort)]
fun second_loop_inv(...): bool { ... }
```

---

## Datatype Invariants

```move
public struct PositiveNumber { value: u64 }

#[spec_only(inv_target = PositiveNumber)]
public fun PositiveNumber_inv(self: &PositiveNumber): bool {
    self.value > 0
}
```

The invariant is automatically checked on construction and modification.

If the invariant is in the same module as the type, you can use just `#[spec_only]` with the naming convention `<Type>_inv`.

---

## Quantifiers (`forall!` and `exists!`)

The `forall!` and `exists!` macros express universal and existential quantification over all valid values of a type.

```
forall!<T>(|x| predicate(x))   // true if predicate holds for every value of T
exists!<T>(|x| predicate(x))   // true if predicate holds for at least one value of T
```

**Lambda parameter is a reference.** Inside the lambda, `x` has type `&T`. Pass it directly to functions that take `&T`, or dereference with `*x` when a value is needed.

**The lambda must call a named pure function.** Inline expressions like `|x| *x + 10` are not supported.

### Pure Predicate Functions

Functions used as quantifier predicates must be annotated `#[ext(pure)]`:

```move
#[ext(pure)]
fun is_gte_0(x: &u64): bool { *x >= 0 }

#[ext(pure)]
fun is_10(x: &u64): bool { x == 10 }
```

### Basic Usage

```move
#[spec(prove)]
fun quantifier_example_spec() {
    ensures(forall!<u64>(|x| is_gte_0(x)));
    ensures(exists!<u64>(|x| is_10(x)));
}
```

### Extra Captured Arguments

Predicate functions can take additional parameters beyond the quantified variable:

```move
#[ext(pure)]
fun is_greater_or_equal(a: u64, x: u64, b: u64): bool {
    x >= a && x >= b
}

#[spec(prove)]
fun extra_args_spec(a: u64, b: u64) {
    ensures(exists!<u64>(|x| is_greater_or_equal(a, *x, b)));
}
```

### Common Quantifier Mistakes

| Mistake | Why it fails |
|---------|-------------|
| `\|x\| *x + 10` | Inline expression — must call a named pure function |
| Predicate uses `assert!` | Pure functions must not abort |
| Predicate calls non-deterministic code | Pure functions must be deterministic |
| Forgetting `#[ext(pure)]` | Predicate will not be recognized as pure |

---

## Common Abort Patterns

**Overflow/underflow** — Use `.to_int()` for arbitrary-precision arithmetic in asserts:
```move
// For: a + b
asserts(a.to_int().add(b.to_int()).lte(std::u64::max_value!().to_int()));

// For: a * b / c
let result = a.to_int().mul(b.to_int()).div(c.to_int());
asserts(result.lte(std::u64::max_value!().to_int()));
```

**Table/dynamic field access** — Assert existence before borrow:
```move
asserts(table.contains(key));
let value = table.borrow(key);
```

**Division** — Assert non-zero divisor:
```move
asserts(divisor != 0);
```

**`bag::contains_with_type` pattern** — `bag::contains<K>` does NOT connect with `bag::borrow<K, V>` in the prover, but `bag::contains_with_type<K, V>` does:
```move
// WRONG - prover can't connect contains with borrow
asserts(bag::contains(&bag, key));

// CORRECT
asserts(bag::contains_with_type<K, V>(&bag, key));
let value = bag::borrow<K, V>(&bag, key);
```

---

## Common Patterns

**Pure functions** — Mark with `#[ext(pure)]` to use in specs. Add to all pure getter/view functions:
```move
#[ext(pure)]
fun max(a: u64, b: u64): u64 { if (a >= b) { a } else { b } }
```

**Private struct field access** — Use `#[test_only]` accessor functions:
```move
// In implementation module:
#[test_only]
public fun get_field_name(s: &MyStruct): String { s.name }

// In spec:
ensures(module::get_field_name(&result) == expected);
```

**`no_opaque` for same-file public functions** — If functions `x` and `y` are both public, both have specs in one file, and `y` is called inside `x`, then `y`'s spec should have `no_opaque` so the prover uses the implementation when proving `x_spec`. Exception: if `y` has a loop with `requires(forall!(...))`, keep it opaque.

**`boogie_opt` for complex specs** — For specs with many calculations:
```move
#[spec(prove, target = module::complex_func, boogie_opt = b"vcsSplitOnEveryAssert")]
```

**Prefer `asserts` over `requires`** where possible. Use `requires` only for preconditions that truly constrain inputs.

**Ensures with table access** — When ensures use getters that internally call `table.borrow`, add a contains check first:
```move
module::set_value(storage, key, value);
ensures(module::contains(storage, key));       // MUST come first
ensures(module::get_value(storage, key) == value);
```

**Extra BPL prelude files** — When the prover fails with `use of undeclared function: $X_module_native_func$pure`, create a `.bpl` prelude file:
```move
#[spec_only(extra_bpl = b"mymodule_prelude.bpl")]
module specs::mymodule;
```

**Targeting external functions**:
```move
#[spec(prove, target = 0x2::transfer::public_transfer)]
fun public_transfer_spec<T: key + store>(obj: T, recipient: address) { ... }
```

**Asserts must come before the function call that could abort:**
```move
// WRONG: Assert after function call
let result = risky_function(a, b);
asserts(a != 0);  // Too late

// CORRECT: Assert before
asserts(a != 0);
let result = risky_function(a, b);
```

**Reuse asserts from proven specs.** When your function calls another function that already has a proven spec, copy all asserts from that spec.

**Early return guards** — When implementation has `if (x == y) { return }`, asserts for code after the early return must be guarded:
```move
if (x != y) {
    asserts(/* conditions for code after early return */);
};
```

---

## CLI Options

### General Options

| Flag | Description |
|------|-------------|
| `--timeout, -t <SECONDS>` | Verification timeout (default: 45) |
| `--verbose, -v` | Display detailed verification progress |
| `--keep-temp, -k` | Keep temporary .bpl files after verification |
| `--generate-only, -g` | Generate Boogie code without running verifier |
| `--dump-bytecode, -d` | Dump bytecode to file for debugging |
| `--no-counterexample-trace` | Don't display counterexample trace on failure |
| `--explain` | Explain verification outputs via LLM |
| `--ci` | Enable CI mode for continuous integration |

### Filtering Options

| Flag | Description |
|------|-------------|
| `--modules <NAMES>` | Verify only specified modules |
| `--functions <NAMES>` | Verify only specified functions |

### Advanced Options

| Flag | Description |
|------|-------------|
| `--skip-spec-no-abort` | Skip checking spec functions that do not abort |
| `--skip-fun-no-abort` | Skip checking `#[ext(no_abort)]` or `#[ext(pure)]` functions |
| `--split-paths <N>` | Split verification into separate proof goals per execution path |
| `--boogie-file-mode, -m <MODE>` | Boogie running mode: `function` (default) or `module` |
| `--use-array-theory` | Use array theory in Boogie encoding |
| `--no-bv-int-encoding` | Encode integers as bitvectors instead of mathematical integers |
| `--stats` | Dump control-flow graphs and function statistics |
| `--force-timeout` | Force kill boogie process if timeout is exceeded |

### Package Options

| Flag | Description |
|------|-------------|
| `--path, -p <PATH>` | Path to package directory with Move.toml |
| `--install-dir <PATH>` | Installation directory for compiled artifacts |
| `--force` | Force recompilation of all packages |
| `--skip-fetch-latest-git-deps` | Skip fetching latest git dependencies |

### Remote/Cloud Options

| Flag | Description |
|------|-------------|
| `--cloud` | Use cloud configuration for remote verification |
| `--cloud-config-path <PATH>` | Path to cloud config (default: `$HOME/.asymptotic/sui_prover.toml`) |
| `--cloud-config` | Create/update cloud configuration interactively |

---

## Debugging Verification Failures

### 1. Interpret the Error

**"Code aborts"** → Missing asserts. Add asserts to cover all abort paths in the function and nested calls. Trace through every function call and identify what can abort (overflow, table access, division by zero, assert! statements).

**"Assert does not hold"** → The assert condition is wrong. Recheck the logic.

### 2. Use Focus for Iterative Development

```move
#[spec(prove, focus, target = module::func)]  // Only verify this spec
```

Always use `focus` when developing a spec. Full suite takes very long.

### 3. Debugging Workflow

1. Add `focus` attribute to the spec you're working on
2. Run `sui-prover`
3. If "Code aborts": add missing asserts for abort conditions
4. If "Assert does not hold": fix the assert condition
5. Once passing with `focus`, remove `focus` and verify full suite

### 4. CLI Debugging Flags

```bash
sui-prover --verbose                    # Detailed output
sui-prover --functions my_failing_spec  # Filter to one function
sui-prover --keep-temp                  # Inspect generated .bpl files
sui-prover --generate-only --keep-temp  # Generate Boogie without running Z3
sui-prover --split-paths 4              # Split verification paths
sui-prover --timeout 120                # Increase timeout
```

---

## Interpreting Results

**Success**: `Verification successful for module::function_spec`

**Failure with counterexample**: Shows which assertion failed, variable values causing failure, and execution trace.

**Timeout**: Solver couldn't prove or disprove within the time limit. Try:
- Increasing `--timeout`
- Simplifying the specification
- Using `--split-paths`
- Adding `boogie_opt = b"vcsSplitOnEveryAssert"` to the spec
- Adding intermediate assertions
- Nested table access in ensures is a common timeout cause — consider dropping ensures and keeping abort coverage only

---

## Common Issues

| Issue | Solution |
|-------|----------|
| "Code aborts" | Missing asserts — add asserts for all abort paths in target and nested calls |
| "Assert does not hold" | Assert condition is wrong — recheck the logic |
| Timeout on complex specs | Add `boogie_opt=b"vcsSplitOnEveryAssert"`, increase `--timeout`, use `--split-paths` |
| Timeout from nested table ensures | Drop ensures, keep abort coverage only |
| "Function not found" | Check module path in `target = ...` attribute |
| Counterexample unclear | Use `--verbose`, add intermediate `ensures()` |
| Loop verification fails | Add/strengthen loop invariant (`invariant!` or external) |
| Pure function not usable in spec | Add `#[ext(pure)]` attribute; called functions also need it |
| Abort condition verification fails | Add `asserts()` for all abort paths, or use `ignore_abort` |
| Spec uses wrong function body | Check `no_opaque` — by default specs are used as opaque summaries |
| `bag::contains` not connecting | Use `bag::contains_with_type<K, V>` instead of `bag::contains<K>` |
| `undeclared function: $X_native$pure` | Create `.bpl` prelude file, use `extra_bpl` |
| `undeclared global variable` for transfers | Declare ghost variables for `SpecTransferAddress`/`SpecTransferAddressExists` |
| `UID object type not found` | Known bug — skip spec for functions that destructure structs to extract UID |
| Compile errors adding specs | Put specs in a separate package, use `target` attribute |

---

## Known Issues

### UID Tracking Bug After Struct Destructuring

When a function destructures a struct to extract a UID and then calls `dynamic_field::remove` on that local UID, the prover loses type information and fails with:
```
error[E0022]: UID object type not found: 5
```
**Workaround:** Do not write a spec for such functions. The `skip` attribute does NOT help because the error occurs during bytecode transformation.

### Method Syntax Limitations

Method syntax works only when the function is defined in the same module as the receiver type:
- `bag::contains(bag, key)` → `bag.contains(key)` ✓ (Bag defined in sui::bag)
- `dynamic_field::borrow(uid, key)` → cannot use method syntax (UID in sui::object, function in sui::dynamic_field)

---

## LP Withdraw Example (Complete)

Target function:
```move
module amm::simple_lp;

use sui::balance::{Balance, Supply, zero};

public struct LP<phantom T> has drop {}

public struct Pool<phantom T> has store {
    balance: Balance<T>,
    shares: Supply<LP<T>>,
}

public fun withdraw<T>(pool: &mut Pool<T>, shares_in: Balance<LP<T>>): Balance<T> {
    if (shares_in.value() == 0) {
        shares_in.destroy_zero();
        return zero()
    };

    let balance = pool.balance.value();
    let shares = pool.shares.supply_value();

    let balance_to_withdraw = (((shares_in.value() as u128) * (balance as u128))
        / (shares as u128)) as u64;

    pool.shares.decrease_supply(shares_in);
    pool.balance.split(balance_to_withdraw)
}
```

Specification proving share price does not decrease on withdrawal:
```move
#[spec_only]
use prover::prover::{requires, ensures};

#[spec(prove)]
fun withdraw_spec<T>(pool: &mut Pool<T>, shares_in: Balance<LP<T>>): Balance<T> {
    requires(shares_in.value() <= pool.shares.supply_value());

    let old_pool = clone!(pool);

    let result = withdraw(pool, shares_in);

    let old_balance = old_pool.balance.value().to_int();
    let new_balance = pool.balance.value().to_int();
    let old_shares = old_pool.shares.supply_value().to_int();
    let new_shares = pool.shares.supply_value().to_int();

    // Share price does not decrease: new_balance/new_shares >= old_balance/old_shares
    ensures(new_shares.mul(old_balance).lte(old_shares.mul(new_balance)));

    result
}
```

Key points:
- `requires(...)` specifies preconditions assumed on arguments
- `clone!(pool)` captures the state of a mutable reference before the call
- `.to_int()` converts to unbounded integers to avoid overflow in conditions
- `.mul()`, `.lte()` are spec-only operators on unbounded integers
- `ensures(...)` specifies postconditions that must hold after the call
