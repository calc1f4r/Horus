---
name: finding-merger
description: Merge, cluster, and falsify raw findings from every discovery lane and round. Groups by root cause rather than symptom, re-reads cited code to attempt disproof, assigns severity with confidence, and guarantees no finding is silently dropped. Use after Phase 4 discovery, or standalone to triage findings from multiple sources.
argument-hint: "[audit-output-dir]"
context: fork
agent: finding-merger
---

Merge and triage all discovery findings in `$ARGUMENTS`.

## What it does

| Step | Output |
|------|--------|
| Ingest | Input ledger — one row per raw finding across all lanes and rounds |
| Cluster | Groups by root cause (Q2+Q3+Q4 of root-cause-analysis must match) |
| Falsify | Re-reads cited code, attempts disproof via 7 routes, records concrete disproofs |
| Compose | One entry per cluster built from the best evidence across all reporters |
| Score | Severity (Impact × Likelihood) and confidence as separate axes |

## Conservation rule

Every input finding lands in exactly one cluster **or** in Excluded Findings with a reason. The unaccounted count must be zero — it is reported explicitly.

## Output

- `audit-output/05-findings-triaged.md`

## Related skills

- [/audit-orchestrator](../audit-orchestrator/SKILL.md) — parent pipeline (Phase 5)
- [/finding-chain-synthesizer](../finding-chain-synthesizer/SKILL.md) — runs on this output
- [/issue-writer](../issue-writer/SKILL.md) — downstream polishing
