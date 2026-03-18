<!-- AUTO-GENERATED from `.claude/rules/skills.md`; source_sha256=f5ee5f6df1a3d20a666349f0bd173eb4cac7c59302b91644c655ca49795e9aed -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/rules/skills.md`.
> This mirrored rule preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

---
paths:
  - "codex/skills/*/SKILL.md"
---

# Skill File Rules

When editing skills in `codex/skills/`:

- Skills are thin invocation wrappers — keep under 500 lines (target ~30-50 lines)
- Every skill must have YAML frontmatter with at least `name` and `description`
- Skills that delegate to agents must set `context: fork` and `agent: <agent-name>`
- Use `$ARGUMENTS` for dynamic task input from the user
- Use `argument-hint` to show expected arguments during autocomplete
- Set `user-invocable: false` for sub-agent-only skills (personas, function-analyzer, system-synthesizer)
- Set `disable-model-invocation: true` for skills with side effects (db-quality-monitor)
- Reference global resources via relative path: `../../resources/<file>.md`
- Do NOT create per-skill `resources/` directories — use the global `codex/resources/` folder
- Include a "Related skills" section with links to upstream/downstream skills
