<!-- AUTO-GENERATED from `.claude/resources/certora-mutation-verifier-reference.md`; source_sha256=b748d2601056ca0dfe3fa53232405396de3b5ab712aea7eb214b95c2a609ff69 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/certora-mutation-verifier-reference.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Certora Mutation Verifier Reference

## Source Docs

- https://docs.certora.com/en/latest/docs/gambit/mutation-verifier.html
- https://docs.certora.com/en/latest/docs/gambit/gambit.html

---

## Installation

```bash
pip install certora-cli
pip install --upgrade certora-cli   # if certoraMutate is missing after install
```

Requirements:
- Python 3.8+
- pip 20.3+ (Linux)
- `CERTORAKEY` environment variable set for cloud runs
- `solc` matching the project's pragma

**Linux ARM / Windows — no prebuilt Gambit binary:**
```bash
# Requires Rust + Cargo
git clone https://github.com/Certora/gambit
cd gambit
cargo build --release
# Add ./target/release/gambit to PATH
```

**Mac / Linux x86-64:** prebuilt binaries ship with `certora-cli`.

---

## Basic Flow

1. Write and pass a baseline `certoraRun` verification.
2. Add a `mutations` object to the `.conf` file.
3. Run `certoraMutate path/to/conf.conf --gambit_only` (generation sanity).
4. Run `certoraMutate path/to/conf.conf` (full campaign).
5. Review results at `https://prover.certora.com/mutations`.
6. Triage live mutants; harden spec for true gaps.

---

## Configuration Fields

### Top-level `mutations` object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `gambit` | array of objects | no (if manual_mutants present) | Gambit-generated mutation config |
| `manual_mutants` | array of objects | no (if gambit present) | Custom patch-based mutants |
| `msg` | string | no | Campaign label shown in dashboard |

### `gambit` entry fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `filename` | string | yes | Path to target Solidity file (relative to project root) |
| `num_mutants` | integer | no | Max mutants to generate (downsampled from all possible) |
| `mutations` | array of strings | no | Operator names to apply; all operators used if omitted |
| `seed` | integer | no | Random seed for reproducible campaigns |
| `contract` | string | no | Limit mutations to a specific contract in the file |
| `functions` | array of strings | no | Limit mutations to specific functions |
| `solc_remappings` | array of strings | no | Import path remappings for Gambit compilation |

### `manual_mutants` entry fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file_to_mutate` | string | yes | Original Solidity file path |
| `mutants_location` | string | yes | Directory containing `.patch` files |

**Notes:**
- Paths are relative to the current working directory (not the conf file location).
- Paths must NOT end with `/`.
- Manual patches must be valid `diff -u` format with `.patch` extension.
- If `gambit` is omitted, only manual mutants run.

---

## Gambit Mutation Operators

| Operator | Transforms | Typical Targets |
|----------|-----------|-----------------|
| `binary-op-mutation` | Replaces binary operators (`+→-`, `*→/`, etc.) | arithmetic, conservation invariants |
| `require-mutation` | Negates or trivializes `require` conditions | access control, guards |
| `assignment-mutation` | Replaces RHS with `0` or alternate expression | storage initialization, accounting |
| `if-cond-mutation` | Replaces `if` condition with `true` or `false` | state machine guards |
| `if-statement-mutation` | Replaces `if` body | conditional state updates |
| `delete-expression-mutation` | Removes expression statements | storage writes, event emissions |
| `swap-arguments-operator-mutation` | Swaps operands: `a op b` → `b op a` | non-commutative operations |
| `elim-delegate-mutation` | Changes `delegatecall` → `call` | proxy contracts, upgrade patterns |
| `unary-operator-mutation` | Inserts or removes `!`, `~`, `-` | boolean guards, sign checks |

**Disabled operators (do not use in config):**
- `function-call-mutation`
- `swap-arguments-function-mutation`

### Operator → Invariant Category Mapping

```
access control / guards      → require-mutation, if-cond-mutation
arithmetic / precision       → binary-op-mutation, assignment-mutation, unary-operator-mutation
state transitions            → if-cond-mutation, if-statement-mutation, delete-expression-mutation
ordering / non-commutativity → swap-arguments-operator-mutation
delegatecall / proxy         → elim-delegate-mutation
conservation of value        → binary-op-mutation, assignment-mutation
```

---

## CLI Options

### `certoraMutate`

| Option | Description |
|--------|-------------|
| `path/to/conf.conf` | Positional: path to Certora conf file (required) |
| `--orig_run <url>` | Reuse an executed baseline run URL instead of running fresh |
| `--orig_run_dir <dir>` | Directory for downloaded original run artifacts |
| `--msg <string>` | Override campaign message (takes precedence over conf `msg`) |
| `--gambit_only` | Only generate mutants; do not submit prover jobs |
| `--dump_failed_collects <file>` | Write failed collection details to file |
| `--debug` | Enable verbose debug output |

### `--orig_run` rules

- The referenced run must have dashboard status `Executed`.
- Files from that run are downloaded locally before mutation jobs start.
- Use `--orig_run_dir` to control download location.
- If baseline rules or contract files changed since that run, create a fresh baseline.

---

## Dashboard Statuses

| Status | Meaning | Action |
|--------|---------|--------|
| `Running` | Prover jobs still executing | Wait |
| `Calculating` | Jobs done; report aggregating | Wait |
| `Executed` | Full report available | Analyze results |
| `Halted` | Global time limit hit | Treat as partial; reduce `num_mutants` for next run |
| `Problem` | Errors occurred | Re-run with `--debug`; check `CERTORAKEY` and conf |

---

## Report Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Coverage** | caught / total tested | ≥80% |
| **Rules** | rules catching ≥1 mutant / all tested rules | maximize |
| **Solo Rules** | rules uniquely catching ≥1 mutant / rules catching ≥1 | maximize (non-redundant spec) |

Counts to track per campaign:
- Total mutants generated
- Caught (spec falsified the mutant)
- Live (spec passed — must triage)
- Failed-invalid (compile/collect error — fix separately)
- Halted/Problem (infrastructure — exclude from coverage denominator)

---

## Gambit Output Structure

When `--gambit_only` or standalone `gambit mutate` runs, output appears in `gambit_out/`:

```
gambit_out/
  gambit_results.json     ← per-mutant metadata (operator, file, line, original/mutated snippet)
  mutants/                ← per-mutant modified Solidity files
  mutants.log             ← human-readable summary
  input_json/             ← compiler intermediates
```

`certoraMutate` also stores applied mutants in:
```
.certora_internal/applied_mutants_dir/
```

Use these artifacts to replay individual mutants:
```bash
certoraRun certora/conf/SpecName.conf --solc_allow_path .certora_internal/applied_mutants_dir/<mutant_id>
```

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `certoraMutate: command not found` | Old certora-cli | `pip install --upgrade certora-cli` |
| No Gambit binary (ARM/Windows) | Platform not supported by prebuilt | Build from source with `cargo build --release` |
| `0 mutants generated` | No matching code constructs for operators | Choose operators matching actual patterns in file |
| Mutant collection errors | Compilation failure in mutated file | Run `--gambit_only --debug`; inspect per-mutant error |
| Package path error | Trailing `/` in remapping | Remove trailing slashes from all remapping paths |
| `orig_run` not accepted | Run status is not `Executed` | Run fresh `certoraRun` to get a new executed baseline |
| Manual patch rejected | Invalid `diff -u` format or missing `.patch` | Validate with `patch --dry-run`; check extension |
| `Halted` with 0% coverage | Too many mutants for time budget | Reduce `num_mutants`; split files into separate campaigns |
| `Problem` with no report | Prover submission or auth failure | Check `CERTORAKEY`; check conf JSON syntax; re-run with `--debug` |
| All mutants live | Spec is vacuous | Check `rule_sanity`; add `satisfy` statements; verify rules are non-vacuous |
| Coverage 0% with passing rules | `rule_sanity: none` | Set `rule_sanity: basic` and re-run baseline |
| `applied_mutants_dir` empty | Gambit generation failed silently | Run `certoraMutate ... --gambit_only --debug` |

---

## Standalone Gambit Usage

For local mutant inspection without running the prover:

```bash
# Mutate a single file
gambit mutate --filename contracts/MyContract.sol

# Downsample mutants
gambit mutate --filename contracts/MyContract.sol --num_mutants 5

# Use a JSON config
gambit mutate --json gambit-config.json

# Show mutant summary
gambit summary

# Reproducible campaign
gambit mutate --filename contracts/MyContract.sol --seed 12345
```

Gambit JSON config example:
```json
[
  {
    "filename": "contracts/Pool.sol",
    "num_mutants": 10,
    "mutations": ["binary-op-mutation", "require-mutation"],
    "seed": 42
  }
]
```

Notes:
- Paths in Gambit JSON are relative to the config file's parent directory.
- `gambit mutate` output defaults to `gambit_out/` in current directory.
- Use `gambit summary` to inspect human-readable mutant descriptions before submitting.
