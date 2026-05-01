---
name: "finding-chain-synthesizer"
description: "Chains confirmed audit findings into multi-step exploit candidates and searches for a unique emergent exploit path. Use after findings are triaged, judge-validated, or confirmed, when CONFIRMED-REPORT.md, 05-findings-triaged.md, issues/, or judge outputs exist and the user asks to compose findings, chain bugs, find an exploit chain, or identify a unique exploit from confirmed issues."
---
Use the [finding-chain-synthesizer subagent](../../../.codex/agents/finding-chain-synthesizer.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `[audit-output-dir] [codebase-path]`.

# Finding Chain Synthesizer Skill

Invokes the `finding-chain-synthesizer` agent.

## Task

<arguments>

## Requirements

- Use only confirmed, valid, or judge-accepted findings as chain components.
- Do not chain raw candidate findings unless the user explicitly says to treat them as confirmed.
- Prefer `audit-output/CONFIRMED-REPORT.md`, `audit-output/10-deep-review.md`, `audit-output/08-pre-judge-results.md`, `audit-output/issues/*.md`, or `audit-output/05-findings-triaged.md`.
- Use maximum-depth reasoning across 2-5 step chains.

## Outputs

- `audit-output/exploit-chain-candidates.json`
- `audit-output/exploit-chain-candidates.md`
- `audit-output/exploit-chain-proofs/chain-NNN.md`
- `audit-output/exploit-chain-poc-handoff.md` when a unique exploit candidate exists
