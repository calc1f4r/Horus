---
name: "certora-mutation-testing"
description: "Run a Certora mutation testing campaign using certoraMutate and Gambit. Generates invariant-driven mutations, validates baseline, executes the campaign, triages live mutants (equivalent / setup-artifact / true-spec-gap), and hardens CVL specs against true gaps. Use after certora-verification when baseline specs exist and mutation coverage assessment is needed."
---
Use the [certora-mutation-testing subagent](../../../.codex/agents/certora-mutation-testing.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<path-to-conf-file> <path-to-invariants-file>`.

Run a Certora mutation testing campaign. Arguments: `<path-to-conf-file>`

Expected input:
- `conf_path` — path to a working Certora `.conf` file (must have a passing `certoraRun` baseline)
- `invariant_suite_path` — path to invariant suite (`audit-output/02-invariants.md` or reviewed variant)

## What this produces

1. **Mutation campaign** — `certoraMutate` run with Gambit operators selected from invariant categories
2. **Generation sanity** — `--gambit_only` pass validates mutant generation before full submission
3. **Survivor triage** — every live mutant classified as equivalent, setup artifact, or true spec gap
4. **Hardening deltas** — minimal CVL edits for each true gap, rerun-validated
5. **Campaign report** — 8-section structured report in `mutation-reports/<campaign-name>.md`

## Example campaign config generated

```json
{
  "mutations": {
    "gambit": [
      {
        "filename": "src/Pool.sol",
        "num_mutants": 10,
        "mutations": ["binary-op-mutation", "require-mutation", "if-cond-mutation"],
        "seed": 42
      }
    ],
    "msg": "invariant-driven campaign"
  }
}
```

## Coverage target

≥80% mutation coverage before declaring a spec complete.

## Related skills

- [certora-verification](../certora-verification/SKILL.md) — Run this first to produce the baseline specs this consumes
- [invariant-writer](../invariant-writer/SKILL.md) — Produces the invariant suite used for operator selection
- [invariant-reviewer](../invariant-reviewer/SKILL.md) — Hardens invariants before mutation testing
- [halmos-verification](../halmos-verification/SKILL.md) — Alternative: symbolic testing approach
- [medusa-fuzzing](../medusa-fuzzing/SKILL.md) — Alternative: property-based fuzzing
