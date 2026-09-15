---
paths:
  - ".claude/agents/*.md"
---

# Agent File Rules

When editing agent definitions in `.claude/agents/`:

- Agents contain the full instructions — they are the source of truth for behavior
- Skills (`.claude/skills/*/SKILL.md`) are thin wrappers that delegate to agents via `context: fork`
- Agent frontmatter uses `tools` and `maxTurns`; skill frontmatter uses `allowed-tools` and `context`
- Never duplicate agent content into skill files — skills should only contain the task prompt
- Shared reference material lives in `.claude/resources/` — link to it, don't copy it
- When adding a new agent, also create a matching skill in `.claude/skills/<name>/SKILL.md`
