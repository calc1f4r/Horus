---
name: "solodit-fetching"
description: "Fetch vulnerability reports from the Solodit/Cyfrin API for a given topic and store them in reports/<topic>/. Use when collecting raw audit findings for a new vulnerability topic, populating the reports/ directory, or preparing input for variant-template-writer."
---
Use the [solodit-fetching subagent](../../../.codex/agents/solodit-fetching.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `<topic>`.

Fetch vulnerability reports for topic `<topic>`.

## Workflow

1. Activate virtual environment: `source .venv/bin/activate`
2. Fetch primary topic: `python3 scripts/solodit_fetcher.py --keyword "<topic>" --output ./reports/<topic>_findings`
3. Fetch related protocols (e.g., Chainlink → any protocol using Chainlink oracles)
4. Deduplicate results
5. Verify output in `reports/<topic>_findings/`

## Rules

- Always activate venv first
- Always use `python3`
- Never apply quality filters (no `--quality` flag)
- Never add duplicate findings
- Always search related protocols that use the target feature

## Output

- `reports/<topic>_findings/` — Fetched vulnerability reports

## Related skills

- [variant-template-writer](../variant-template-writer/SKILL.md) — Consumes fetched reports to create DB entries
- [invariant-catcher](../invariant-catcher/SKILL.md) — Uses DB entries for vulnerability hunting
