<!-- AUTO-GENERATED from `.claude/rules/agents.md`; source_sha256=e631da2926ed8a811c27bd550dc789c8352bd6a722d4a9c9083db9a52357975a -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/rules/agents.md`.
> This mirrored rule preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

---
paths:
  - "codex/agents/*.md"
---

# Agent File Rules

When editing agent definitions in `codex/agents/`:

- Agents contain the full instructions — they are the source of truth for behavior
- Skills (`codex/skills/*/SKILL.md`) are thin wrappers that delegate to agents via `context: fork`
- Agent frontmatter uses `tools` and `maxTurns`; skill frontmatter uses `allowed-tools` and `context`
- Never duplicate agent content into skill files — skills should only contain the task prompt
- Shared reference material lives in `codex/resources/` — link to it, don't copy it
- When adding a new agent, also create a matching skill in `codex/skills/<name>/SKILL.md`
