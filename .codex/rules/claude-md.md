---
paths:
  - "CLAUDE.md"
---

# CLAUDE.md Conventions

When editing `CLAUDE.md`:

- `CLAUDE.md` is the project-level system prompt — it is always loaded into every conversation
- Keep it under 400 lines — content beyond that risks being truncated in tight context windows
- The Quick Reference section must stay at the top and point to the correct Tier 1 router (`DB/index.json`)
- The Architecture section must reflect the current 4-tier search layout accurately
- The Agents table must list every agent in `.codex/agents/` with its correct purpose
- The Rules section must list every file in `.codex/rules/` with its path pattern
- The Common Commands section must include all frequently-used scripts
- Do not add agent-specific instructions here — those belong in the agent's own `.codex/agents/<name>.toml`
- Do not add vulnerability taxonomy or audit methodology here — those belong in `.codex/resources/`
- After adding a new agent, skill, or rule file, update the relevant section in CLAUDE.md
