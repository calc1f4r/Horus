name: solodit-fetching
description: "Fetch vulnerability reports from the Solodit/Cyfrin API for a given topic and store them in reports/<topic>/. Use when collecting raw audit findings for a new vulnerability topic, populating the reports/ directory, or preparing input for variant-template-writer."
context: fork
agent: solodit-fetching
argument-hint: <topic>
disable-model-invocation: true
---

<!-- AUTO-GENERATED from `.claude/skills/solodit-fetching/SKILL.md`; source_sha256=f9e38c0e9b832ac23035a127a5329edd9973b40d70998565446df1ec1c9743f0 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/skills/solodit-fetching/SKILL.md`.
> The original skill metadata below is preserved verbatim.
> For Codex/GPT use, load `codex/agents/solodit-fetching.md` as the implementation playbook.
> Follow any linked `codex/resources/*` references from that agent file.
> Relative skill links remain mirrored under `codex/skills/*`.

Fetch vulnerability reports for topic `$ARGUMENTS`.

## Workflow

1. Activate virtual environment: `source .venv/bin/activate`
2. Fetch primary topic: `python3 scripts/solodit_fetcher.py --keyword "$ARGUMENTS" --output ./reports/${ARGUMENTS}_findings`
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
