---
paths:
  - ".codex/agents/*.toml"
---

# Agent File Rules

When editing agent definitions in `.codex/agents/`:

- Agents contain the full instructions — they are the source of truth for behavior
- Skills (`.agents/skills/*/SKILL.md`) are thin wrappers that delegate to agents via `context: fork`
- Agent frontmatter uses `tools` and `maxTurns`; skill frontmatter uses `allowed-tools` and `context`
- Never duplicate agent content into skill files — skills should only contain the task prompt
- Shared reference material lives in `.codex/resources/` — link to it, don't copy it
- When adding a new agent, also create a matching skill in `.agents/skills/<name>/SKILL.md`
