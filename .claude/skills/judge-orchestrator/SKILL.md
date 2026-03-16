---
name: judge-orchestrator
description: "Run a finding through all three platform judges (Sherlock, Cantina, Code4rena) in parallel, synthesize cross-platform verdicts, resolve divergences via two-round challenge protocol, and persist a memory log of decisions. Use when you need multi-platform severity consensus, want to know the best platform to submit to, or need cross-judge reasoning on a contested finding."
context: fork
agent: judge-orchestrator
argument-hint: <finding-text-or-path> [--platforms=sherlock,cantina,c4] [--primary=sherlock|cantina|c4] [--mode=consensus|compare] [--no-memory]
---

Run all three platform judges against the finding at `$ARGUMENTS`, synthesize their verdicts, and produce a cross-platform consensus report.

## What this runs

| Round | What happens |
|-------|-------------|
| **Load memory** | Reads `audit-output/judge-memory/` for prior similar findings |
| **Round 1** | Sherlock + Cantina + Code4rena judges run in parallel, independently |
| **Divergence check** | Compares verdicts; flags unexpected disagreements |
| **Round 2** | Each judge receives the other judges' reasoning and issues a challenge response (revised or held-firm) |
| **Synthesis** | Consensus verdict assembled; best-platform recommendation produced |
| **Memory write** | Verdict appended to `audit-output/judge-memory/verdict-log.md` |

## Platform severity models

| Platform | Model | Likelihood | Admin issues | Rounding |
|----------|-------|-----------|--------------|---------|
| Sherlock | Binary: H/M/Invalid | **Ignored** | README-dependent | MEDIUM if repeatable = 100% |
| Cantina | Impact × Likelihood matrix | **Core input** | Capped INFO | Capped LOW |
| Code4rena | 3-tier: H/M/QA | Contextual | QA/MEDIUM cap | Capped QA |

## Flags

- `--platforms=X,Y` — run only specified platforms (default: all three)
- `--primary=sherlock|cantina|c4` — weight one platform's verdict as authoritative
- `--mode=compare` — show per-platform verdicts only, no consensus synthesis
- `--no-memory` — skip memory read/write entirely
- `--memory-only` — query memory for similar findings only, do not spawn judges

## Output locations

```
audit-output/judge-memory/
  active-session.md    — Round 1 + Round 2 communication log (current session)
  verdict-log.md       — Append-only history of all past verdicts
  pattern-insights.md  — Synthesized cross-platform divergence patterns
```

## Related skills

- [/sherlock-judging](../sherlock-judging/SKILL.md) — Sherlock-only validation
- [/cantina-judge](../cantina-judge/SKILL.md) — Cantina-only validation
- [/code4rena-judge](../code4rena-judge/SKILL.md) — Code4rena-only validation
- [/issue-writer](../issue-writer/SKILL.md) — Polish finding for the recommended platform
- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — Full audit pipeline (uses judges in Phases 8/10)
