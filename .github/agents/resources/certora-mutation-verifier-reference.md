# Certora Mutation Verifier Reference

## Purpose

This reference covers running Certora mutation testing with `certoraMutate` and Gambit for Solidity projects.

## Source Docs

- https://docs.certora.com/en/latest/docs/gambit/mutation-verifier.html
- https://docs.certora.com/en/latest/docs/gambit/gambit.html

## Installation

Install Certora CLI (includes `certoraRun` and `certoraMutate`):

```bash
pip install certora-cli
```

If `certoraMutate` is missing after install:

```bash
pip install --upgrade certora-cli
```

Notes:
- On Linux, pip version 20.3+ is required by Certora docs.
- `CERTORAKEY` must be set before cloud runs.

## Basic Flow

1. Run a successful baseline verification (`certoraRun`) or provide an `Executed` run URL via `--orig_run`.
2. Add a `mutations` object to the `.conf` file.
3. Run `certoraMutate` on the `.conf`.
4. Review results in the mutations dashboard.

## Required Mutation Config Structure

The `.conf` file must include a top-level `mutations` object.

Minimal form:

```json
{
  "mutations": {
    "gambit": [
      {
        "filename": "contracts/MyContract.sol",
        "num_mutants": 5
      }
    ],
    "msg": "basic mutation configuration"
  }
}
```

Important behavior:
- All non-mutation settings remain controlled by the normal `.conf` fields.
- `gambit` is a list of Gambit mutation objects.
- Paths in mutation-verifier docs are treated as relative to current working directory.

## Mutation Sources

### Gambit-generated mutations

Use key: `mutations.gambit`.

Each object can include:
- `filename`
- `num_mutants`
- `mutations` (optional operator filter list)
- other Gambit options supported by Gambit config

### Manual mutations

Use key: `mutations.manual_mutants`.

Each manual mutant object requires:
- `file_to_mutate`
- `mutants_location`

Manual mutation notes:
- Patches must end with `.patch`.
- Patches should be valid `diff -u` format.
- Prefer one mutation per manual mutant for traceability.
- If `gambit` is omitted, `certoraMutate` runs only manual mutants.

## Original Run Modes

### Generate original run automatically

`certoraMutate` can submit baseline run with mutants.

### Reuse an existing baseline run

```bash
certoraMutate path/to/prover.conf --orig_run <executed_run_url>
```

Rules:
- The referenced run must have dashboard status `Executed`.
- Files from that run are downloaded locally.
- Use `--orig_run_dir` to control download location.

## CLI Options (Mutation Verifier)

Documented options include:
- `--orig_run`
- `--orig_run_dir`
- `--msg`
- `--gambit_only`
- `--dump_failed_collects`
- `--debug`

## Dashboard Statuses

Mutation test status values:
- `Running`: mutant verification jobs are still executing.
- `Calculating`: jobs finished; report is being aggregated.
- `Executed`: full report available.
- `Halted`: global time limit reached; partial report available.
- `Problem`: errors occurred; report usually unavailable.

## Report Metrics

From mutation report:
- Coverage: caught mutants / total tested mutants.
- Rules: rules that caught at least one mutant / all tested rules.
- Solo Rules: rules that uniquely caught a mutation / rules that caught at least one mutation.

## Troubleshooting

1. Missing Gambit binary on Linux ARM or Windows:
   - build Gambit from source (Rust/Cargo) per Gambit docs.
2. Mutation generation errors:
   - run with `--gambit_only` and inspect generated mutants.
3. Mutants not showing in report:
   - check compilation validity for manual mutants.
4. Suspect mutant-specific failures:
   - replay using artifacts from `.certora_internal/applied_mutants_dir`.
5. Package path issues:
   - ensure remapping source/target paths do not end with `/`.

## Gambit Notes Relevant to certoraMutate

- Gambit uses `solc`; compiler version must match project.
- Gambit config supports JSON object or array of objects.
- Relative paths in Gambit JSON are relative to the config file parent directory.
- `gambit mutate` output defaults to `gambit_out`.
