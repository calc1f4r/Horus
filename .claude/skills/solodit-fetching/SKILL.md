name: solodit-fetching
description: "Fetch vulnerability reports from the Solodit/Cyfrin API for a given topic and store them in reports/<topic>/. Use when collecting raw audit findings for a new vulnerability topic, populating the reports/ directory, or preparing input for variant-template-writer."
context: fork
agent: solodit-fetching
argument-hint: <topic>
---

Fetch vulnerability reports for topic `$ARGUMENTS`.

## Workflow

1. Activate virtual environment: `source .venv/bin/activate`
2. Fetch primary topic: `python3 solodit_fetcher.py --keyword "$ARGUMENTS" --output ./reports/${ARGUMENTS}_findings`
3. Fetch related protocols (e.g., Chainlink → any protocol using Chainlink oracles)
4. Deduplicate results
5. Verify output in `reports/${ARGUMENTS}_findings/`

## Rules

- Always activate venv first
- Always use `python3`
- Never apply quality filters (no `--quality` flag)
- Never add duplicate findings
- Always search related protocols that use the target feature

## Output

- `reports/<topic>_findings/` — Fetched vulnerability reports

## Related skills

- [/variant-template-writer](../variant-template-writer/SKILL.md) — Consumes fetched reports to create DB entries
- [/invariant-catcher](../invariant-catcher/SKILL.md) — Uses DB entries for vulnerability hunting
